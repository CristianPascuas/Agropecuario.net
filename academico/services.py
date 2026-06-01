from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone

from .models import Competencia, CoordinadorEquipo, EquipoEjecutor, Programacion, ProgramacionDia, ProgramacionDiaResultado, ProgramacionResultado, Resultado, Usuario
from .validators import (
    evaluar_minimo_mensual,
    franja_horaria_desde_horario,
    horas_radicados_aprobados_instructor_mes,
    horas_por_dia_desde_horario,
    horas_programadas_competencia_ficha,
    horas_programadas_instructor_anio,
    horas_programadas_instructor_mes,
    politica_horas_mensuales,
    validar_solape_ambiente,
    validar_solape_instructor,
    validar_instructor_tipo_competencia_semana,
    validar_solape_radicado_aprobado,
    validar_solape_usuario,
)


@dataclass
class DiaRechazado:
    fecha: date
    motivo: str


@dataclass
class ResultadoPrevalidacion:
    fechas_validas: list[date]
    fechas_rechazadas: list[DiaRechazado]
    avisos: list[str]
    horas_por_dia: int


def _round2(valor: float) -> float:
    return round(float(valor or 0.0) + 1e-9, 2)


def _distribuir_horas_equilibrado(total: float, resultado_ids: list[int]) -> dict[int, float]:
    if not resultado_ids:
        return {}
    total = _round2(total)
    base = _round2(total / len(resultado_ids))
    distribucion = {rid: base for rid in resultado_ids}
    acumulado = _round2(sum(distribucion.values()))
    ajuste = _round2(total - acumulado)
    distribucion[resultado_ids[-1]] = _round2(distribucion[resultado_ids[-1]] + ajuste)
    return distribucion


def _normalizar_horas_resultados_competencia(
    competencia: Competencia,
    horas_objetivo_total: float | None,
    horas_resultados: dict[int, float] | None,
) -> dict:
    resultados_competencia = list(
        Resultado.objects.filter(id_competencia_id=competencia.id_competencia).order_by('id_resultado')
    )
    resultado_ids = [item.id_resultado for item in resultados_competencia]
    horas_max = _round2(float(competencia.horas_max or 0))
    recomendado = _round2(horas_max * 0.75)

    if not resultado_ids:
        return {
            'objetivo_horas': 0.0,
            'recomendado_horas': recomendado,
            'horas_max': horas_max,
            'porcentaje_objetivo': 0.0,
            'horas_resultados_map': {},
            'resultados_competencia': [],
        }

    objetivo = 0.0 if horas_objetivo_total is None else _round2(horas_objetivo_total)
    if objetivo < 0:
        objetivo = 0.0
    if objetivo > horas_max:
        objetivo = horas_max

    mapa = {}
    if horas_resultados:
        for rid in resultado_ids:
            mapa[rid] = _round2(float(horas_resultados.get(rid, 0.0)))
        suma_actual = _round2(sum(mapa.values()))
        if resultado_ids and abs(suma_actual - objetivo) > 0.01:
            mapa = _distribuir_horas_equilibrado(objetivo, resultado_ids)
    else:
        mapa = _distribuir_horas_equilibrado(objetivo, resultado_ids)

    return {
        'objetivo_horas': objetivo,
        'recomendado_horas': recomendado,
        'horas_max': horas_max,
        'porcentaje_objetivo': _round2((objetivo / horas_max) * 100) if horas_max > 0 else 0.0,
        'horas_resultados_map': mapa,
        'resultados_competencia': resultados_competencia,
    }


def _es_instructor(usuario: Usuario) -> bool:
    nombre_rol = (usuario.id_rol.nombre or '').lower()
    return 'instr' in nombre_rol


def _puede_autoasignarse(dinamizador: Usuario) -> bool:
    return getattr(dinamizador, 'tipo_dinamizador', None) != 'coordinador'


def instructores_tecnicos_para_ficha(ficha, dinamizador: Usuario):
    base = Usuario.objects.filter(
        activo=True,
        id_equipo_id=ficha.id_equipo_id,
    ).select_related('id_rol', 'id_equipo')
    qs = base.filter(id_rol__nombre__icontains='instr')
    if _puede_autoasignarse(dinamizador):
        qs = qs | base.filter(id_usuario=dinamizador.id_usuario)
    return qs


def instructores_trasversales(equipo_filtro_id: int | None = None):
    qs = Usuario.objects.filter(activo=True, id_rol__nombre__icontains='instr').select_related('id_rol', 'id_equipo')
    if equipo_filtro_id:
        qs = qs.filter(id_equipo_id=equipo_filtro_id)
    return qs


def _es_coordinador(usuario: Usuario) -> bool:
    rol_nombre = (getattr(getattr(usuario, 'id_rol', None), 'nombre', '') or '').lower()
    return ('coordinador' in rol_nombre) or ('dinamizador' in rol_nombre and getattr(usuario, 'tipo_dinamizador', None) == 'coordinador')


def ids_equipos_disponibles_para_dinamizador(dinamizador: Usuario) -> set[int]:
    coordinador_id = None

    if _es_coordinador(dinamizador):
        coordinador_id = dinamizador.id_usuario
    elif getattr(dinamizador, 'id_equipo_id', None):
        relacion_directa = CoordinadorEquipo.objects.filter(
            id_equipo_id=dinamizador.id_equipo_id,
        ).values_list('id_coordinador_id', flat=True).first()
        if relacion_directa:
            coordinador_id = int(relacion_directa)

    if coordinador_id:
        ids = set(
            CoordinadorEquipo.objects.filter(id_coordinador_id=coordinador_id)
            .values_list('id_equipo_id', flat=True)
        )
        if ids:
            return ids

    if getattr(dinamizador, 'id_equipo_id', None):
        return {int(dinamizador.id_equipo_id)}

    return set()


def instructores_trasversales_para_dinamizador(
    dinamizador: Usuario,
    equipo_filtro_id: int | None = None,
):
    equipos_permitidos = ids_equipos_disponibles_para_dinamizador(dinamizador)
    qs = Usuario.objects.filter(
        activo=True,
        id_rol__nombre__icontains='instr',
    ).select_related('id_rol', 'id_equipo')

    if equipos_permitidos:
        qs = qs.filter(id_equipo_id__in=equipos_permitidos)
    else:
        qs = qs.none()

    if equipo_filtro_id:
        qs = qs.filter(id_equipo_id=equipo_filtro_id)
    return qs


def instructores_elegibles(ficha, dinamizador: Usuario, competencia: Competencia, equipo_filtro_id: int | None = None):
    if competencia.tipo_competencia == 'tecnica':
        return instructores_tecnicos_para_ficha(ficha, dinamizador).distinct().order_by('nombre', 'apellido')

    qs = instructores_trasversales_para_dinamizador(
        dinamizador,
        equipo_filtro_id=equipo_filtro_id,
    ).distinct().order_by('nombre', 'apellido')
    if dinamizador.activo:
        equipo_dinamizador = getattr(dinamizador, 'id_equipo', None)
        tipo_equipo_dinamizador = int(getattr(equipo_dinamizador, 'tipo', 1) or 1)
        dinamizador_en_equipo_filtrado = (
            not equipo_filtro_id
            or int(equipo_filtro_id) == int(getattr(dinamizador, 'id_equipo_id', 0) or 0)
        )
        incluir_dinamizador = (tipo_equipo_dinamizador == 0) or dinamizador_en_equipo_filtrado

        if not incluir_dinamizador or not _puede_autoasignarse(dinamizador):
            return qs

        ids_qs = qs.values_list('id_usuario', flat=True)
        return Usuario.objects.filter(
            Q(id_usuario__in=ids_qs) | Q(id_usuario=dinamizador.id_usuario),
            activo=True,
        ).select_related('id_rol', 'id_equipo').distinct().order_by('nombre', 'apellido')
    return qs


def prevalidar_programacion_dias(
    *,
    ficha,
    dinamizador: Usuario,
    instructor: Usuario,
    ambiente,
    competencia: Competencia,
    horario,
    fechas: list[date],
    horario_especial: dict | None = None,
) -> ResultadoPrevalidacion:
    if not fechas:
        raise ValidationError('Debes seleccionar al menos un dia de calendario.')

    hora_inicio_prog, hora_fin_prog, horas_dia = _franja_y_horas_programacion(horario, horario_especial)

    fechas_ordenadas = sorted(set(fechas))
    validas: list[date] = []
    rechazadas: list[DiaRechazado] = []
    avisos: list[str] = []

    total_competencia_base = horas_programadas_competencia_ficha(ficha.codigo_ficha, competencia.id_competencia)
    delta_competencia = 0.0

    cache_mes: dict[tuple[int, int], float] = {}
    delta_mes: dict[tuple[int, int], float] = {}

    cache_anio: dict[int, float] = {}
    delta_anio: dict[int, float] = {}
    politica_horas = politica_horas_mensuales(instructor)

    for fecha in fechas_ordenadas:
        if fecha < ficha.fecha_inicio or fecha > ficha.fecha_fin:
            rechazadas.append(DiaRechazado(fecha=fecha, motivo='Dia fuera del rango permitido por la ficha.'))
            continue

        if fecha.isoweekday() == 7:
            rechazadas.append(DiaRechazado(fecha=fecha, motivo='No se permite programar en domingos.'))
            continue

        try:
            validar_solape_instructor(fecha, ficha.codigo_ficha, instructor.id_usuario)
            validar_solape_ambiente(fecha, horario, ambiente.id_ambiente)
            validar_solape_usuario(fecha, horario.id_horario, instructor.id_usuario)
            validar_solape_radicado_aprobado(
                fecha=fecha,
                instructor_id=instructor.id_usuario,
                hora_inicio=hora_inicio_prog,
                hora_fin=hora_fin_prog,
            )
            validar_instructor_tipo_competencia_semana(
                fecha=fecha,
                codigo_ficha_id=ficha.codigo_ficha,
                competencia=competencia,
                instructor_id=instructor.id_usuario,
            )
        except ValidationError as exc:
            rechazadas.append(DiaRechazado(fecha=fecha, motivo=str(exc.message)))
            continue

        llave_mes = (fecha.year, fecha.month)
        if llave_mes not in cache_mes:
            cache_mes[llave_mes] = horas_programadas_instructor_mes(instructor.id_usuario, fecha.year, fecha.month)
            cache_mes[llave_mes] += horas_radicados_aprobados_instructor_mes(
                instructor.id_usuario,
                fecha.year,
                fecha.month,
            )
            delta_mes[llave_mes] = 0.0

        if fecha.year not in cache_anio:
            cache_anio[fecha.year] = horas_programadas_instructor_anio(instructor.id_usuario, fecha.year)
            delta_anio[fecha.year] = 0.0

        proyectado_mes = cache_mes[llave_mes] + delta_mes[llave_mes] + horas_dia
        maximo_bloqueante = politica_horas['maximo_bloqueante']
        if proyectado_mes > maximo_bloqueante:
            rechazadas.append(
                DiaRechazado(
                    fecha=fecha,
                    motivo=(
                        'Supera el tope mensual permitido del instructor '
                        f'({int(maximo_bloqueante)}h).'
                    ),
                )
            )
            continue

        meta_ideal = politica_horas['meta_ideal']
        if proyectado_mes > meta_ideal:
            aviso_mes = (
                f'Aviso: en {llave_mes[1]}/{llave_mes[0]} se supera la meta mensual del instructor '
                f'({int(meta_ideal)}h).'
            )
            if aviso_mes not in avisos:
                avisos.append(aviso_mes)

        proyectado_anio = cache_anio[fecha.year] + delta_anio[fecha.year] + horas_dia
        if proyectado_anio > float(instructor.horas_objetivo_anual):
            aviso_anio = (
                f'Aviso: en {fecha.year} se supera la meta anual del instructor '
                f'({instructor.horas_objetivo_anual}h).'
            )
            if aviso_anio not in avisos:
                avisos.append(aviso_anio)

        proyectado_competencia = total_competencia_base + delta_competencia + horas_dia
        if proyectado_competencia > float(competencia.horas_max):
            rechazadas.append(DiaRechazado(fecha=fecha, motivo='Supera las horas maximas de la competencia.'))
            continue

        validas.append(fecha)
        delta_mes[llave_mes] += horas_dia
        delta_anio[fecha.year] += horas_dia
        delta_competencia += horas_dia

    return ResultadoPrevalidacion(
        fechas_validas=validas,
        fechas_rechazadas=rechazadas,
        avisos=avisos,
        horas_por_dia=horas_dia,
    )


def guardar_programacion_dias(
    *,
    ficha,
    dinamizador: Usuario,
    instructor: Usuario,
    ambiente,
    competencia: Competencia,
    horario,
    fechas: list[date],
    asignaciones_resultados: list[dict] | None = None,
    horario_especial: dict | None = None,
    horas_objetivo_total: float | None = None,
    horas_resultados: dict[int, float] | None = None,
    programacion_existente: Programacion | None = None,
):
    """Guarda cabecera en Programacion y detalle por dia en ProgramacionDia en una transaccion."""
    horas_config = _normalizar_horas_resultados_competencia(
        competencia=competencia,
        horas_objetivo_total=horas_objetivo_total,
        horas_resultados=horas_resultados,
    )

    validacion = prevalidar_programacion_dias(
        ficha=ficha,
        dinamizador=dinamizador,
        instructor=instructor,
        ambiente=ambiente,
        competencia=competencia,
        horario=horario,
        fechas=fechas,
        horario_especial=horario_especial,
    )

    if not validacion.fechas_validas:
        return {
            'cabecera': None,
            'creadas': 0,
            'rechazadas': [{'fecha': item.fecha.isoformat(), 'motivo': item.motivo} for item in validacion.fechas_rechazadas],
            'avisos': validacion.avisos,
            'horas_por_dia': validacion.horas_por_dia,
            'horas_totales_nuevas': 0,
            'resultados_asignados': 0,
            'objetivo_horas': horas_config['objetivo_horas'],
            'recomendado_horas': horas_config['recomendado_horas'],
            'porcentaje_objetivo': horas_config['porcentaje_objetivo'],
            'horas_resultados': [
                {
                    'resultado_id': item.id_resultado,
                    'nombre': item.nombre,
                    'horas': horas_config['horas_resultados_map'].get(item.id_resultado, 0.0),
                    'fijada': False,
                }
                for item in horas_config['resultados_competencia']
            ],
        }

    fecha_inicio = min(validacion.fechas_validas)
    fecha_fin = max(validacion.fechas_validas)
    hora_inicio, hora_fin, _ = _franja_y_horas_programacion(horario, horario_especial)

    with transaction.atomic():
        if programacion_existente is None:
            cabecera = Programacion.objects.create(
                codigo_ficha=ficha,
                id_ambiente=ambiente,
                id_competencia=competencia,
                id_instructor=instructor,
                id_dinamizador_asignador=dinamizador,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                mes_operativo=fecha_inicio.month,
                anio_operativo=fecha_inicio.year,
                estado='programada',
                creado_en=timezone.now(),
            )
        else:
            cabecera = programacion_existente
            cabecera.codigo_ficha = ficha
            cabecera.id_ambiente = ambiente
            cabecera.id_competencia = competencia
            cabecera.id_instructor = instructor
            cabecera.id_dinamizador_asignador = dinamizador
            cabecera.fecha_inicio = fecha_inicio
            cabecera.fecha_fin = fecha_fin
            cabecera.hora_inicio = hora_inicio
            cabecera.hora_fin = hora_fin
            cabecera.mes_operativo = fecha_inicio.month
            cabecera.anio_operativo = fecha_inicio.year
            cabecera.modificado_en = timezone.now()
            cabecera.save(
                update_fields=[
                    'codigo_ficha',
                    'id_ambiente',
                    'id_competencia',
                    'id_instructor',
                    'id_dinamizador_asignador',
                    'fecha_inicio',
                    'fecha_fin',
                    'hora_inicio',
                    'hora_fin',
                    'mes_operativo',
                    'anio_operativo',
                    'modificado_en',
                ]
            )

        detalle = []
        for fecha in validacion.fechas_validas:
            detalle.append(
                ProgramacionDia.objects.create(
                    codigo_ficha=ficha,
                    id_competencia=competencia,
                    id_instructor=instructor,
                    id_dinamizador_asignador=dinamizador,
                    id_horario=horario,
                    fecha=fecha,
                    horas_dia=validacion.horas_por_dia,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    estado='programada',
                )
            )

        asignados_resultados = 0
        if asignaciones_resultados:
            detalle_por_fecha = {item.fecha: item for item in detalle}
            resultado_ids = {int(item['resultado_id']) for item in asignaciones_resultados}
            resultados_validos = {
                item.id_resultado: item
                for item in Resultado.objects.filter(
                    id_resultado__in=resultado_ids,
                    id_competencia_id=competencia.id_competencia,
                )
            }

            for asignacion in asignaciones_resultados:
                resultado_id = int(asignacion['resultado_id'])
                if resultado_id not in resultados_validos:
                    continue

                fecha_inicio = asignacion['fecha_inicio']
                fecha_fin = asignacion['fecha_fin']
                if fecha_fin < fecha_inicio:
                    fecha_inicio, fecha_fin = fecha_fin, fecha_inicio

                for fecha_item, dia_item in detalle_por_fecha.items():
                    if not (fecha_inicio <= fecha_item <= fecha_fin):
                        continue
                    _, creado = ProgramacionDiaResultado.objects.get_or_create(
                        id_programacion_dia=dia_item,
                        id_resultado_id=resultado_id,
                    )
                    if creado:
                        asignados_resultados += 1

        _aplicar_regla_noche_jornada_doble(validacion.fechas_validas)

        detalle_ids = [item.id_programacion_dia for item in detalle]
        horas_dictadas_qs = (
            ProgramacionDiaResultado.objects.filter(id_programacion_dia_id__in=detalle_ids)
            .values('id_resultado_id')
            .annotate(total=Sum('id_programacion_dia__horas_dia'))
        )
        horas_dictadas_map = {
            int(item['id_resultado_id']): _round2(float(item['total'] or 0.0))
            for item in horas_dictadas_qs
        }

        resultado_ids_competencia = [item.id_resultado for item in horas_config['resultados_competencia']]
        ProgramacionResultado.objects.filter(id_programacion=cabecera).exclude(
            id_resultado_id__in=resultado_ids_competencia,
        ).delete()

        for item in horas_config['resultados_competencia']:
            ProgramacionResultado.objects.update_or_create(
                id_programacion=cabecera,
                id_resultado=item,
                defaults={
                    'horas_objetivo': horas_config['horas_resultados_map'].get(item.id_resultado, 0.0),
                    'horas_dictadas': horas_dictadas_map.get(item.id_resultado, 0.0),
                },
            )

    detalle_ids = [item.id_programacion_dia for item in detalle]
    horas_totales_nuevas = (
        ProgramacionDia.objects.filter(id_programacion_dia__in=detalle_ids).aggregate(total=Sum('horas_dia'))['total']
        or 0
    )

    minimo_mes = evaluar_minimo_mensual(instructor, fecha_inicio.year, fecha_inicio.month)

    return {
        'cabecera': cabecera,
        'creadas': len(validacion.fechas_validas),
        'rechazadas': [{'fecha': item.fecha.isoformat(), 'motivo': item.motivo} for item in validacion.fechas_rechazadas],
        'avisos': validacion.avisos,
        'horas_por_dia': validacion.horas_por_dia,
        'horas_totales_nuevas': horas_totales_nuevas,
        'resultados_asignados': asignados_resultados,
        'minimo_mes': minimo_mes,
        'objetivo_horas': horas_config['objetivo_horas'],
        'recomendado_horas': horas_config['recomendado_horas'],
        'porcentaje_objetivo': horas_config['porcentaje_objetivo'],
        'horas_resultados': [
            {
                'resultado_id': item.id_resultado,
                'nombre': item.nombre,
                'horas': horas_config['horas_resultados_map'].get(item.id_resultado, 0.0),
                'fijada': True,
            }
            for item in horas_config['resultados_competencia']
        ],
    }


def detalle_programacion_para_edicion(programacion: Programacion) -> dict:
    dias_qs = ProgramacionDia.objects.filter(
        codigo_ficha_id=programacion.codigo_ficha_id,
        id_competencia_id=programacion.id_competencia_id,
        id_instructor_id=programacion.id_instructor_id,
        fecha__range=(programacion.fecha_inicio, programacion.fecha_fin),
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).order_by('fecha', 'id_programacion_dia')

    dias = list(dias_qs)
    fechas = [item.fecha for item in dias]
    hora_inicio_dia = None
    hora_fin_dia = None
    if dias:
        hora_inicio_dia = dias[0].hora_inicio or programacion.hora_inicio
        hora_fin_dia = dias[0].hora_fin or programacion.hora_fin

    resultados_por_id: dict[int, dict] = defaultdict(lambda: {'resultado_id': None, 'nombre': '', 'fechas': []})
    relaciones = ProgramacionDiaResultado.objects.filter(
        id_programacion_dia__in=dias_qs,
    ).select_related('id_programacion_dia', 'id_resultado').order_by('id_resultado_id', 'id_programacion_dia__fecha')

    for rel in relaciones:
        resultado_id = rel.id_resultado_id
        bucket = resultados_por_id[resultado_id]
        bucket['resultado_id'] = resultado_id
        bucket['nombre'] = rel.id_resultado.nombre
        bucket['fechas'].append(rel.id_programacion_dia.fecha)

    asignaciones_resultados = []
    for item in resultados_por_id.values():
        if not item['fechas']:
            continue
        fecha_inicio = min(item['fechas'])
        fecha_fin = max(item['fechas'])
        asignaciones_resultados.append(
            {
                'resultado_id': item['resultado_id'],
                'nombre': item['nombre'],
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
            }
        )

    resultados_config_qs = ProgramacionResultado.objects.filter(
        id_programacion_id=programacion.id_programacion,
    ).select_related('id_resultado').order_by('id_resultado_id')

    if resultados_config_qs.exists():
        horas_resultados = [
            {
                'resultado_id': item.id_resultado_id,
                'nombre': item.id_resultado.nombre,
                'horas': _round2(float(item.horas_objetivo or 0.0)),
                'horas_fijadas': True,
            }
            for item in resultados_config_qs
        ]
        objetivo_horas = _round2(sum(item['horas'] for item in horas_resultados))
        recomendado_horas = _round2(float(programacion.id_competencia.horas_max or 0) * 0.75)
        porcentaje_objetivo = _round2((objetivo_horas / float(programacion.id_competencia.horas_max)) * 100) if float(programacion.id_competencia.horas_max or 0) > 0 else 0.0
    else:
        horas_config = _normalizar_horas_resultados_competencia(
            competencia=programacion.id_competencia,
            horas_objetivo_total=None,
            horas_resultados=None,
        )
        objetivo_horas = horas_config['objetivo_horas']
        recomendado_horas = horas_config['recomendado_horas']
        porcentaje_objetivo = horas_config['porcentaje_objetivo']
        horas_resultados = [
            {
                'resultado_id': item.id_resultado,
                'nombre': item.nombre,
                'horas': horas_config['horas_resultados_map'].get(item.id_resultado, 0.0),
                'horas_fijadas': False,
            }
            for item in horas_config['resultados_competencia']
        ]

    return {
        'id_programacion': programacion.id_programacion,
        'codigo_ficha': programacion.codigo_ficha_id,
        'competencia_id': programacion.id_competencia_id,
        'instructor_id': programacion.id_instructor_id,
        'ambiente_id': programacion.id_ambiente_id,
        'estado': programacion.estado,
        'fecha_inicio': programacion.fecha_inicio,
        'fecha_fin': programacion.fecha_fin,
        'hora_inicio': hora_inicio_dia.strftime('%H:%M') if hora_inicio_dia else '',
        'hora_fin': hora_fin_dia.strftime('%H:%M') if hora_fin_dia else '',
        'usa_horario_especial': bool(
            hora_inicio_dia
            and hora_fin_dia
            and (hora_inicio_dia != programacion.hora_inicio or hora_fin_dia != programacion.hora_fin)
        ),
        'fechas': [item.isoformat() for item in fechas],
        'asignaciones_resultados': [
            {
                'resultado_id': item['resultado_id'],
                'nombre': item['nombre'],
                'fecha_inicio': item['fecha_inicio'].isoformat(),
                'fecha_fin': item['fecha_fin'].isoformat(),
            }
            for item in asignaciones_resultados
        ],
        'objetivo_horas': objetivo_horas,
        'recomendado_horas': recomendado_horas,
        'porcentaje_objetivo': porcentaje_objetivo,
        'horas_resultados': horas_resultados,
    }


def editar_programacion_existente(
    *,
    programacion: Programacion,
    dinamizador: Usuario,
    ambiente,
    fechas: list[date],
    asignaciones_resultados: list[dict] | None = None,
    horario_especial: dict | None = None,
    horas_objetivo_total: float | None = None,
    horas_resultados: dict[int, float] | None = None,
) -> dict:
    if programacion.estado in ('cancelada', 'reemplazada'):
        raise ValidationError('La programación seleccionada no puede ser editada por su estado actual.')

    ficha = programacion.codigo_ficha
    competencia = programacion.id_competencia
    instructor = programacion.id_instructor
    horario = ficha.id_horario

    if not horario:
        raise ValidationError('La ficha no tiene horario asociado.')

    fechas_unicas = sorted(set(fechas))
    if not fechas_unicas:
        raise ValidationError('Debes seleccionar al menos un día para actualizar la programación.')

    with transaction.atomic():
        rango_anterior = (programacion.fecha_inicio, programacion.fecha_fin)

        dias_previos_qs = ProgramacionDia.objects.filter(
            codigo_ficha_id=ficha.codigo_ficha,
            id_competencia_id=competencia.id_competencia,
            id_instructor_id=instructor.id_usuario,
            fecha__range=rango_anterior,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        )
        fechas_previas = list(dias_previos_qs.values_list('fecha', flat=True).distinct())

        # En edición se reemplaza el detalle diario completo de la misma cabecera.
        ProgramacionDiaResultado.objects.filter(id_programacion_dia__in=dias_previos_qs).delete()
        dias_previos_qs.delete()

        resultado_nuevo = guardar_programacion_dias(
            ficha=ficha,
            dinamizador=dinamizador,
            instructor=instructor,
            ambiente=ambiente,
            competencia=competencia,
            horario=horario,
            fechas=fechas_unicas,
            asignaciones_resultados=asignaciones_resultados or [],
            horario_especial=horario_especial,
            horas_objetivo_total=horas_objetivo_total,
            horas_resultados=horas_resultados,
            programacion_existente=programacion,
        )

        if resultado_nuevo.get('cabecera') is None:
            raise ValidationError('No fue posible crear la programación editada con las fechas seleccionadas.')

        cabecera_nueva = resultado_nuevo['cabecera']
        cabecera_nueva.estado = 'ajustada'
        cabecera_nueva.modificado_en = timezone.now()
        cabecera_nueva.razon_cambio = f'Edicion aplicada sobre programación #{programacion.id_programacion}.'
        cabecera_nueva.save(update_fields=['estado', 'modificado_en', 'razon_cambio'])

        fechas_afectadas = sorted(set(fechas_previas) | set(fechas_unicas))
        _aplicar_regla_noche_jornada_doble(fechas_afectadas)

    return {
        'programacion_anterior_id': programacion.id_programacion,
        'programacion_nueva_id': cabecera_nueva.id_programacion,
        'resultado': resultado_nuevo,
    }


def _franja_y_horas_programacion(horario, horario_especial: dict | None = None) -> tuple[time, time, int]:
    base_inicio, base_fin = franja_horaria_desde_horario(horario)
    horas_base = horas_por_dia_desde_horario(horario)
    if horas_base <= 0:
        raise ValidationError('No se pudo determinar las horas por dia del horario seleccionado.')

    if not horario_especial:
        return base_inicio, base_fin, horas_base

    hora_inicio = horario_especial.get('hora_inicio')
    hora_fin = horario_especial.get('hora_fin')
    if not isinstance(hora_inicio, time) or not isinstance(hora_fin, time):
        raise ValidationError('Horario especial inválido: hora de inicio/fin obligatorias.')

    if hora_inicio < base_inicio or hora_fin > base_fin:
        raise ValidationError(
            f'El horario especial debe estar dentro del rango base {base_inicio.strftime("%H:%M")}-{base_fin.strftime("%H:%M")}.',
        )

    if hora_fin <= hora_inicio:
        raise ValidationError('La hora fin del horario especial debe ser mayor que la hora inicio.')

    horas_reales = (datetime.combine(date.today(), hora_fin) - datetime.combine(date.today(), hora_inicio)).total_seconds() / 3600.0
    if horas_reales <= 0:
        raise ValidationError('El horario especial debe representar al menos una hora de clase.')

    if abs(horas_reales - round(horas_reales)) > 1e-9:
        raise ValidationError('Por ahora el horario especial solo admite horas completas (sin fracciones).')

    return hora_inicio, hora_fin, int(round(horas_reales))


def _normalizar_nombre_horario(horario_nombre: str) -> str:
    return (horario_nombre or '').strip().lower().replace('ñ', 'n')


def _es_horario_tarde(horario_nombre: str) -> bool:
    return 'tarde' in _normalizar_nombre_horario(horario_nombre)


def _es_horario_noche(horario_nombre: str) -> bool:
    return 'noche' in _normalizar_nombre_horario(horario_nombre)


def _aplicar_regla_noche_jornada_doble(fechas: list[date] | set[date]) -> None:
    """
    Regla automática:
    Si un instructor o dinamizador tiene asignación en tarde y noche el mismo día,
    la asignación de noche se ajusta a 19:00-22:00 (3h).
    """
    if not fechas:
        return

    fechas_unicas = sorted(set(fechas))
    inicio_noche_ajustada = time(19, 0)
    fin_noche_ajustada = time(22, 0)

    for fecha_item in fechas_unicas:
        dias = list(
            ProgramacionDia.objects.filter(
                fecha=fecha_item,
                estado__in=['programada', 'ajustada', 'ejecutada'],
            ).select_related('id_horario')
        )

        if not dias:
            continue

        usuarios_tarde: set[int] = set()
        usuarios_noche: set[int] = set()

        for dia in dias:
            nombre_horario = dia.id_horario.horario if dia.id_horario else ''
            if _es_horario_tarde(nombre_horario):
                usuarios_tarde.add(dia.id_instructor_id)
                usuarios_tarde.add(dia.id_dinamizador_asignador_id)
            if _es_horario_noche(nombre_horario):
                usuarios_noche.add(dia.id_instructor_id)
                usuarios_noche.add(dia.id_dinamizador_asignador_id)

        usuarios_doble_jornada = usuarios_tarde & usuarios_noche
        if not usuarios_noche:
            continue

        for dia in dias:
            nombre_horario = dia.id_horario.horario if dia.id_horario else ''
            if not _es_horario_noche(nombre_horario):
                continue

            aplica_ajuste = (
                dia.id_instructor_id in usuarios_doble_jornada
                or dia.id_dinamizador_asignador_id in usuarios_doble_jornada
            )

            if aplica_ajuste:
                nuevo_inicio = inicio_noche_ajustada
                nuevo_fin = fin_noche_ajustada
                nuevas_horas = 3
            else:
                nuevo_inicio, nuevo_fin = franja_horaria_desde_horario(dia.id_horario)
                nuevas_horas = horas_por_dia_desde_horario(dia.id_horario)

            if (
                dia.hora_inicio != nuevo_inicio
                or dia.hora_fin != nuevo_fin
                or dia.horas_dia != nuevas_horas
            ):
                dia.hora_inicio = nuevo_inicio
                dia.hora_fin = nuevo_fin
                dia.horas_dia = nuevas_horas
                dia.modificado_en = timezone.now()
                dia.save(update_fields=['hora_inicio', 'hora_fin', 'horas_dia', 'modificado_en'])
