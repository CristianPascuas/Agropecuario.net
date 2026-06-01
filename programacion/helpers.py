import calendar
from datetime import date, datetime, timedelta

from django.core.exceptions import ValidationError
from django.db.models import Exists, OuterRef, Q
from django.http import Http404
from django.utils import timezone

from academico.models import Competencia, Ficha, Programacion, ProgramacionDia, Radicado, Resultado, Usuario
from academico.validators import (
    evaluar_minimo_mensual,
    franja_horaria_desde_horario,
    horas_programadas_competencia_ficha,
    horas_programadas_instructor_anio,
    horas_programadas_instructor_mes,
    politica_horas_mensuales,
)

from portal.core import MESES_ES, _rango_mes

from radicados.helpers import _fechas_radicado, _franjas_solapan, _horas_radicados_usuario_en_rango

SESSION_PROGRAMACION_TEST_MODE_KEY = 'programacion_modo_pruebas'


def _meses_en_rango(fecha_inicio, fecha_fin):
    meses = []
    cursor = date(fecha_inicio.year, fecha_inicio.month, 1)
    ultimo = date(fecha_fin.year, fecha_fin.month, 1)
    cal = calendar.Calendar(firstweekday=0)

    while cursor <= ultimo:
        semanas = []
        for semana in cal.monthdayscalendar(cursor.year, cursor.month):
            fila = []
            for dia in semana:
                if dia == 0:
                    fila.append({'day': 0, 'in_range': False})
                    continue

                dia_actual = date(cursor.year, cursor.month, dia)
                fila.append(
                    {
                        'day': dia,
                        'in_range': fecha_inicio <= dia_actual <= fecha_fin,
                    }
                )
            semanas.append(fila)

        meses.append(
            {
                'id': f"mes-{cursor.year}-{cursor.month}",
                'nombre': f"{MESES_ES[cursor.month]} {cursor.year}",
                'anio': cursor.year,
                'mes': cursor.month,
                'semanas': semanas,
            }
        )

        if cursor.month == 12:
            cursor = date(cursor.year + 1, 1, 1)
        else:
            cursor = date(cursor.year, cursor.month + 1, 1)

    return meses


def _slot_desde_horario(horario) -> str:
    inicio, _ = franja_horaria_desde_horario(horario)
    return _slot_desde_hora(inicio)


def _slot_desde_hora(hora_inicio) -> str:
    inicio = hora_inicio
    if inicio.hour < 12:
        return 'manana'
    if inicio.hour < 18:
        return 'tarde'
    return 'noche'


def _fechas_ajuste_noche_auto(ficha, dinamizador, instructor, anio: int, mes: int) -> list[str]:
    """
    Fechas del mes donde aplica ajuste automático 19:00-22:00 (3h) para una
    programación nocturna, por coexistir con jornada de tarde del instructor o
    del dinamizador en el mismo día.
    """
    if not ficha.id_horario or _slot_desde_horario(ficha.id_horario) != 'noche':
        return []

    user_ids = {dinamizador.id_usuario}
    if instructor is not None:
        user_ids.add(instructor.id_usuario)

    filtros_usuario = Q(id_instructor_id__in=user_ids) | Q(id_dinamizador_asignador_id__in=user_ids)
    fechas_qs = (
        ProgramacionDia.objects.filter(
            fecha__year=anio,
            fecha__month=mes,
            estado__in=['programada', 'ajustada', 'ejecutada'],
            id_horario__horario__icontains='tarde',
        )
        .filter(filtros_usuario)
        .values_list('fecha', flat=True)
        .distinct()
        .order_by('fecha')
    )
    return [item.isoformat() for item in fechas_qs]


def _obtener_ficha_dinamizador(usuario, codigo_ficha):
    try:
        return Ficha.objects.select_related(
            'id_programa_formacion',
            'id_horario',
            'id_ambiente',
            'codigo_municipio',
            'id_lider_ficha',
        ).get(codigo_ficha=codigo_ficha, id_equipo_id=usuario.id_equipo_id)
    except Ficha.DoesNotExist as exc:
        raise Http404('No se encontró la ficha solicitada para tu equipo.') from exc


def _validar_mes_en_rango_ficha(ficha, anio, mes):
    inicio_mes = date(anio, mes, 1)
    if mes == 12:
        fin_mes = date(anio, 12, 31)
    else:
        fin_mes = date(anio, mes + 1, 1) - timedelta(days=1)
    if fin_mes < ficha.fecha_inicio or inicio_mes > ficha.fecha_fin:
        raise Http404('El mes solicitado no está dentro del rango de la ficha.')
    return inicio_mes, fin_mes


def _modo_pruebas_programacion_activo(request):
    return bool(request.session.get(SESSION_PROGRAMACION_TEST_MODE_KEY, False))


def _estado_mes_relativo(anio, mes, hoy=None):
    hoy_ref = hoy or timezone.localdate()
    objetivo = (int(anio), int(mes))
    actual = (hoy_ref.year, hoy_ref.month)
    if objetivo < actual:
        return 'pasado'
    if objetivo == actual:
        return 'actual'
    return 'futuro'


def _fecha_apertura_creacion_futuros(hoy=None):
    hoy_ref = hoy or timezone.localdate()
    if hoy_ref.month == 12:
        inicio_siguiente = date(hoy_ref.year + 1, 1, 1)
    else:
        inicio_siguiente = date(hoy_ref.year, hoy_ref.month + 1, 1)
    return inicio_siguiente - timedelta(days=14)


def _ventana_creacion_futuros_abierta(hoy=None):
    hoy_ref = hoy or timezone.localdate()
    return hoy_ref >= _fecha_apertura_creacion_futuros(hoy_ref)


def _politica_programacion_mes(anio, mes, hoy=None, modo_pruebas=False):
    hoy_ref = hoy or timezone.localdate()
    estado = _estado_mes_relativo(anio, mes, hoy_ref)
    fecha_apertura = _fecha_apertura_creacion_futuros(hoy_ref)
    ventana_abierta = _ventana_creacion_futuros_abierta(hoy_ref)

    if modo_pruebas:
        return {
            'es_mes_pasado': estado == 'pasado',
            'es_mes_actual': estado == 'actual',
            'es_mes_futuro': estado == 'futuro',
            'ventana_abierta_futuros': True,
            'fecha_apertura_futuros': fecha_apertura,
            'permite_crear': True,
            'permite_editar': True,
            'mensaje_creacion': 'Modo pruebas activo: limitantes de creación desactivadas.',
            'mensaje_edicion': 'Modo pruebas activo: limitantes de edición desactivadas.',
        }

    permite_crear = estado == 'futuro' and ventana_abierta
    permite_editar = estado == 'actual'

    if estado == 'pasado':
        mensaje_creacion = 'No se permite crear programación en meses pasados.'
        mensaje_edicion = 'No se permite editar programación de meses pasados.'
    elif estado == 'actual':
        mensaje_creacion = 'En el mes actual solo se permite editar programación ya asignada.'
        mensaje_edicion = ''
    else:
        if ventana_abierta:
            mensaje_creacion = ''
        else:
            mensaje_creacion = (
                'La programación de meses futuros se habilita en las últimas 2 semanas '
                f'del mes actual. Apertura: {fecha_apertura.isoformat()}.'
            )
        mensaje_edicion = 'La edición solo está habilitada para el mes actual.'

    return {
        'es_mes_pasado': estado == 'pasado',
        'es_mes_actual': estado == 'actual',
        'es_mes_futuro': estado == 'futuro',
        'ventana_abierta_futuros': ventana_abierta,
        'fecha_apertura_futuros': fecha_apertura,
        'permite_crear': permite_crear,
        'permite_editar': permite_editar,
        'mensaje_creacion': mensaje_creacion,
        'mensaje_edicion': mensaje_edicion,
    }


def _calendario_mes_ficha(ficha, anio, mes, instructor_id=None, ambiente_id=None):
    inicio_mes, fin_mes = _validar_mes_en_rango_ficha(ficha, anio, mes)
    cal = calendar.Calendar(firstweekday=0)
    ambiente_validado = ambiente_id or ficha.id_ambiente_id

    ocupacion_ficha = set(
        ProgramacionDia.objects.filter(
            codigo_ficha_id=ficha.codigo_ficha,
            fecha__range=(inicio_mes, fin_mes),
            id_horario_id=ficha.id_horario_id,
        ).values_list('fecha', flat=True)
    )

    ocupacion_ambiente = set(
        ProgramacionDia.objects.filter(
            codigo_ficha__id_ambiente_id=ambiente_validado,
            fecha__range=(inicio_mes, fin_mes),
            id_horario_id=ficha.id_horario_id,
        ).values_list('fecha', flat=True)
    )

    ocupacion_instructor = {}
    ocupacion_radicado = set()
    if instructor_id:
        instructor_dias_qs = (
            ProgramacionDia.objects.filter(
                id_instructor_id=instructor_id,
                fecha__range=(inicio_mes, fin_mes),
                id_horario_id=ficha.id_horario_id,
            )
            .values('fecha', 'codigo_ficha_id', 'id_horario__horario')
        )
        for entry in instructor_dias_qs:
            fkey = entry['fecha']
            if fkey not in ocupacion_instructor:
                ocupacion_instructor[fkey] = []
            ocupacion_instructor[fkey].append({
                'codigo_ficha': entry['codigo_ficha_id'],
                'jornada': entry['id_horario__horario'] or '',
            })

        if ficha.id_horario_id:
            hora_inicio_ficha, hora_fin_ficha = franja_horaria_desde_horario(ficha.id_horario)
            radicados_qs = Radicado.objects.filter(
                id_instructor_id=instructor_id,
                aprobado=1,
            )
            for item in radicados_qs:
                if not _franjas_solapan(hora_inicio_ficha, hora_fin_ficha, item.hora_inicio, item.hora_fin):
                    continue
                for fecha_item in _fechas_radicado(item):
                    if inicio_mes <= fecha_item <= fin_mes:
                        ocupacion_radicado.add(fecha_item)

    semanas = []
    for semana in cal.monthdayscalendar(anio, mes):
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append({'day': 0, 'in_range': False})
                continue

            fecha_actual = date(anio, mes, dia)
            in_range = ficha.fecha_inicio <= fecha_actual <= ficha.fecha_fin
            fila.append(
                {
                    'day': dia,
                    'date': fecha_actual.isoformat(),
                    'in_range': in_range,
                    'es_domingo': fecha_actual.isoweekday() == 7,
                    'ocupada_ficha': in_range and fecha_actual in ocupacion_ficha,
                    'ocupada_ambiente': in_range and fecha_actual in ocupacion_ambiente,
                    'ocupada_instructor': in_range and fecha_actual in ocupacion_instructor,
                    'instructor_info': ocupacion_instructor.get(fecha_actual, []) if in_range else [],
                    'ocupada_radicado': in_range and fecha_actual in ocupacion_radicado,
                }
            )
        semanas.append(fila)

    return {
        'nombre': f"{MESES_ES[mes]} {anio}",
        'anio': anio,
        'mes': mes,
        'semanas': semanas,
    }


def _competencias_programa_con_contador(ficha):
    competencias = Competencia.objects.filter(
        id_programa_formacion_id=ficha.id_programa_formacion_id
    ).order_by('nombre')

    data = []
    for item in competencias:
        usadas = horas_programadas_competencia_ficha(ficha.codigo_ficha, item.id_competencia)
        restantes = max(0.0, float(item.horas_max) - usadas)
        data.append(
            {
                'id': item.id_competencia,
                'nombre': item.nombre,
                'tipo': item.tipo_competencia,
                'horas_max': float(item.horas_max),
                'horas_programadas': round(usadas, 2),
                'horas_restantes': round(restantes, 2),
            }
        )
    return data


def _fechas_programadas_competencia_ficha(ficha, competencia):
    fechas = set(
        ProgramacionDia.objects.filter(
            codigo_ficha_id=ficha.codigo_ficha,
            id_competencia_id=competencia.id_competencia,
        ).values_list('fecha', flat=True)
    )

    detalle_relacionado = ProgramacionDia.objects.filter(
        codigo_ficha_id=OuterRef('codigo_ficha_id'),
        id_competencia_id=OuterRef('id_competencia_id'),
        id_instructor_id=OuterRef('id_instructor_id'),
        fecha__gte=OuterRef('fecha_inicio'),
        fecha__lte=OuterRef('fecha_fin'),
    )
    legacy_qs = (
        Programacion.objects.filter(
            codigo_ficha_id=ficha.codigo_ficha,
            id_competencia_id=competencia.id_competencia,
        )
        .annotate(_tiene_detalle=Exists(detalle_relacionado))
        .filter(_tiene_detalle=False)
    )
    for item in legacy_qs:
        inicio = max(item.fecha_inicio, ficha.fecha_inicio)
        fin = min(item.fecha_fin, ficha.fecha_fin)
        if fin < inicio:
            continue
        cursor = inicio
        while cursor <= fin:
            fechas.add(cursor)
            cursor = cursor + timedelta(days=1)

    return sorted(fechas)


def _resumen_instructor(instructor, anio, mes):
    mes_actual = float(horas_programadas_instructor_mes(instructor.id_usuario, anio, mes))
    anio_actual = float(horas_programadas_instructor_anio(instructor.id_usuario, anio))

    inicio_mes, fin_mes = _rango_mes(anio, mes)
    inicio_anio = date(anio, 1, 1)
    fin_anio = date(anio, 12, 31)
    mes_actual += _horas_radicados_usuario_en_rango(instructor, inicio_mes, fin_mes)
    anio_actual += _horas_radicados_usuario_en_rango(instructor, inicio_anio, fin_anio)

    minimo = evaluar_minimo_mensual(instructor, anio, mes)
    politica = politica_horas_mensuales(instructor)
    return {
        'id': instructor.id_usuario,
        'nombre': f"{instructor.nombre} {instructor.apellido}",
        'horas_mes': round(mes_actual, 2),
        'horas_anio': round(anio_actual, 2),
        'max_mensual': int(politica['meta_ideal']),
        'max_mensual_bloqueante': int(politica['maximo_bloqueante']),
        'objetivo_anual': int(instructor.horas_objetivo_anual),
        'minimo_mensual': minimo,
        'minimo_anual': {
            'minimo': int(getattr(instructor, 'horas_min_anual', instructor.horas_objetivo_anual)),
            'actual': round(anio_actual, 2),
            'cumple': anio_actual >= float(getattr(instructor, 'horas_min_anual', instructor.horas_objetivo_anual)),
        },
    }


def _parse_horario_especial_payload(payload, horario_base):
    if not isinstance(payload, dict):
        return None
    if not payload.get('habilitado'):
        return None

    hora_inicio_raw = str(payload.get('hora_inicio') or '').strip()
    hora_fin_raw = str(payload.get('hora_fin') or '').strip()
    if not hora_inicio_raw or not hora_fin_raw:
        raise ValidationError('Debes indicar hora de inicio y fin para el horario especial.')

    try:
        hora_inicio = datetime.strptime(hora_inicio_raw, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_raw, '%H:%M').time()
    except ValueError as exc:
        raise ValidationError('Formato de hora inválido para horario especial (usa HH:MM).') from exc

    base_inicio, base_fin = franja_horaria_desde_horario(horario_base)
    if hora_inicio < base_inicio or hora_fin > base_fin:
        raise ValidationError(
            f'El horario especial debe estar dentro del rango base {base_inicio.strftime("%H:%M")}-{base_fin.strftime("%H:%M")}.',
        )

    if hora_fin <= hora_inicio:
        raise ValidationError('La hora fin debe ser mayor que la hora inicio en el horario especial.')

    return {
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
    }


def _obtener_programacion_de_ficha(ficha, id_programacion):
    try:
        return Programacion.objects.select_related(
            'codigo_ficha',
            'id_competencia',
            'id_instructor',
            'id_ambiente',
        ).get(
            id_programacion=id_programacion,
            codigo_ficha_id=ficha.codigo_ficha,
        )
    except Programacion.DoesNotExist as exc:
        raise Http404('No se encontró la programación solicitada para esta ficha.') from exc


def _anio_mes_programacion(programacion):
    anio = int(programacion.anio_operativo or programacion.fecha_inicio.year)
    mes = int(programacion.mes_operativo or programacion.fecha_inicio.month)
    return anio, mes
