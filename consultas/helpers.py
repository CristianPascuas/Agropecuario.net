import calendar
from datetime import date

from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

from academico.models import Ficha, ProgramacionDia, ProgramacionDiaResultado, Radicado, Resultado, Usuario
from academico.validators import (
    franja_horaria_desde_horario,
    horas_programadas_instructor_anio,
    horas_programadas_instructor_mes,
)

from portal.core import MESES_ES, _rango_mes, _rol_slug

from programacion.helpers import _slot_desde_hora, _slot_desde_horario

from radicados.helpers import _fechas_radicado, _horas_radicados_usuario_en_rango

SLOTS_HORARIO = (
    ('manana', 'Mañana', '07:00 - 13:00'),
    ('tarde', 'Tarde', '13:00 - 18:00'),
    ('noche', 'Noche', '18:00 - 22:00'),
)

PALETA_COMBINACIONES = [
    '#E8F5E9',
    '#E3F2FD',
    '#FFF3E0',
    '#F3E5F5',
    '#E0F2F1',
    '#FFF8E1',
    '#FCE4EC',
    '#E8EAF6',
]


def _normalizar_texto_resultado(texto: str) -> str:
    if texto is None:
        return ''
    valor = str(texto)
    valor = valor.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    valor = valor.replace('\u000D\u000A', ' ').replace('\u000A', ' ').replace('\u000D', ' ')
    return ' '.join(valor.split())


def _seleccion_mes_anio_desde_request(request):
    hoy = timezone.localdate()

    try:
        anio = int(request.GET.get('anio', hoy.year))
    except (TypeError, ValueError):
        anio = hoy.year

    try:
        mes = int(request.GET.get('mes', hoy.month))
    except (TypeError, ValueError):
        mes = hoy.month

    if not (1 <= mes <= 12):
        mes = hoy.month

    if not (2000 <= anio <= 2100):
        anio = hoy.year

    return anio, mes


def _contexto_consulta_programaciones_usuario(request, usuario):
    busqueda = request.GET.get('q', '').strip()
    hoy = timezone.localdate()
    anio_seleccionado, mes_seleccionado = _seleccion_mes_anio_desde_request(request)
    inicio_mes, fin_mes = _rango_mes(anio_seleccionado, mes_seleccionado)

    rol_nombre = (getattr(usuario.id_rol, 'nombre', '') or '').strip().lower()
    # Tanto instructor como dinamizador deben ver en este calendario solo sus
    # asignaciones como instructor, no las que hayan sido asignadas a terceros.
    filtro_usuario = Q(id_instructor_id=usuario.id_usuario)

    dias_qs = ProgramacionDia.objects.filter(
        fecha__range=(inicio_mes, fin_mes),
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).filter(filtro_usuario)

    if busqueda:
        if busqueda.isdigit():
            dias_qs = dias_qs.filter(codigo_ficha_id=int(busqueda))
        else:
            dias_qs = dias_qs.none()

    dias_qs = dias_qs.select_related(
        'codigo_ficha',
        'codigo_ficha__id_programa_formacion',
        'id_competencia',
        'id_horario',
    ).order_by('fecha', 'id_horario__horario', 'codigo_ficha_id')

    dias = list(dias_qs)
    ids_dia = [item.id_programacion_dia for item in dias]
    ids_competencia = sorted({item.id_competencia_id for item in dias})

    if rol_nombre == 'dinamizador':
        fichas_qs = ProgramacionDia.objects.filter(
            estado__in=['programada', 'ajustada', 'ejecutada'],
            id_dinamizador_asignador_id=usuario.id_usuario,
        )
    else:
        fichas_qs = ProgramacionDia.objects.filter(
            estado__in=['programada', 'ajustada', 'ejecutada'],
        ).filter(filtro_usuario)
    ids_ficha = list(
        fichas_qs.values_list('codigo_ficha_id', flat=True).distinct()
    )
    fichas_programadas_qs = Ficha.objects.filter(codigo_ficha__in=ids_ficha)

    if busqueda:
        if busqueda.isdigit():
            fichas_programadas_qs = fichas_programadas_qs.filter(codigo_ficha=int(busqueda))
        else:
            fichas_programadas_qs = fichas_programadas_qs.none()

    fichas_programadas = fichas_programadas_qs.select_related(
        'id_programa_formacion',
        'id_horario',
        'id_ambiente',
        'codigo_municipio',
        'id_lider_ficha',
    ).order_by('-codigo_ficha')

    asignados_por_dia = {}
    if ids_dia:
        relaciones = ProgramacionDiaResultado.objects.filter(
            id_programacion_dia_id__in=ids_dia,
        ).select_related('id_resultado')
        for rel in relaciones:
            asignados_por_dia.setdefault(rel.id_programacion_dia_id, []).append(
                _normalizar_texto_resultado(rel.id_resultado.nombre)
            )

    resultados_por_competencia = {}
    if ids_competencia:
        for item in Resultado.objects.filter(id_competencia_id__in=ids_competencia).order_by('nombre'):
            resultados_por_competencia.setdefault(item.id_competencia_id, []).append(
                _normalizar_texto_resultado(item.nombre)
            )

    agenda = {}
    for item in dias:
        slot = _slot_desde_horario(item.id_horario)
        resultados = asignados_por_dia.get(item.id_programacion_dia)
        if not resultados:
            resultados = resultados_por_competencia.get(item.id_competencia_id, [])

        inicio_h, fin_h = franja_horaria_desde_horario(item.id_horario)
        if item.hora_inicio:
            inicio_h = item.hora_inicio
        if item.hora_fin:
            fin_h = item.hora_fin
        agenda.setdefault(item.fecha, {}).setdefault(slot, []).append(
            {
                'ficha': item.codigo_ficha_id,
                'competencia': item.id_competencia.nombre,
                'horario': f"{inicio_h.strftime('%H:%M')} - {fin_h.strftime('%H:%M')}",
                'resultados': resultados,
                'es_radicado': False,
                'etiqueta': f"Ficha {item.codigo_ficha_id}",
            }
        )

    radicados_aprobados = Radicado.objects.filter(
        id_instructor_id=usuario.id_usuario,
        aprobado=1,
    )
    if busqueda:
        radicados_aprobados = radicados_aprobados.none()

    radicados_en_mes = 0
    for radicado in radicados_aprobados:
        fechas_radicado = _fechas_radicado(radicado)
        if not fechas_radicado:
            continue

        slot = _slot_desde_hora(radicado.hora_inicio)
        horario = f"{radicado.hora_inicio.strftime('%H:%M')} - {radicado.hora_fin.strftime('%H:%M')}"
        detalle_radicado = [
            f"Nombre: {radicado.nombre_radicado}",
            f"Descripcion: {radicado.descripcion_radicado}",
            f"Empresa/Organizacion: {radicado.empresa_organizacion}",
            f"NIT: {radicado.nit}",
            f"Lugar: {radicado.lugar}",
            f"Horario: {horario}",
        ]

        for fecha in fechas_radicado:
            if not (inicio_mes <= fecha <= fin_mes):
                continue

            agenda.setdefault(fecha, {}).setdefault(slot, []).append(
                {
                    'ficha': None,
                    'competencia': 'Actividad adicional aceptada',
                    'horario': horario,
                    'resultados': detalle_radicado,
                    'es_radicado': True,
                    'etiqueta': 'Actividad adicional aceptada',
                }
            )
            radicados_en_mes += 1

    cal = calendar.Calendar(firstweekday=0)
    semanas = []
    for semana in cal.monthdatescalendar(anio_seleccionado, mes_seleccionado):
        fila = []
        for fecha in semana:
            in_month = fecha.month == mes_seleccionado
            agenda_dia = agenda.get(fecha, {})
            slots = []
            for key, etiqueta, rango in SLOTS_HORARIO:
                slots.append(
                    {
                        'key': key,
                        'label': etiqueta,
                        'rango': rango,
                        'items': agenda_dia.get(key, []),
                    }
                )

            tiene_asignaciones = any(bool(agenda_dia.get(key, [])) for key, _, _ in SLOTS_HORARIO)

            fila.append(
                {
                    'day': fecha.day,
                    'date': fecha.isoformat(),
                    'in_month': in_month,
                    'tiene_asignaciones': in_month and tiene_asignaciones,
                    'slots': slots,
                }
            )
        semanas.append(fila)

    return {
        'busqueda': busqueda,
        'anio_seleccionado': anio_seleccionado,
        'mes_seleccionado': mes_seleccionado,
        'anios_disponibles': list(range(hoy.year - 5, hoy.year + 6)),
        'meses_disponibles': [(idx, nombre) for idx, nombre in enumerate(MESES_ES) if idx],
        'fichas_programadas': fichas_programadas,
        'mes_actual': {
            'anio': anio_seleccionado,
            'mes': mes_seleccionado,
            'nombre': MESES_ES[mes_seleccionado],
            'semanas': semanas,
        },
        'total_asignaciones_mes': len(dias) + radicados_en_mes,
    }


def _obtener_ficha_para_consulta(usuario, codigo_ficha):
    rol = _rol_slug(usuario)
    base_qs = Ficha.objects.select_related(
        'id_programa_formacion',
        'id_horario',
        'id_ambiente',
        'codigo_municipio',
        'id_lider_ficha',
    )

    if rol == 'dinamizador':
        try:
            return base_qs.get(codigo_ficha=codigo_ficha, id_equipo_id=usuario.id_equipo_id)
        except Ficha.DoesNotExist as exc:
            raise Http404('No se encontró la ficha solicitada para tu equipo.') from exc

    if rol == 'instructor':
        acceso = ProgramacionDia.objects.filter(
            codigo_ficha_id=codigo_ficha,
            id_instructor_id=usuario.id_usuario,
        ).exists()
        if not acceso:
            raise Http404('No tienes acceso a esta ficha.')
        try:
            return base_qs.get(codigo_ficha=codigo_ficha)
        except Ficha.DoesNotExist as exc:
            raise Http404('No se encontró la ficha solicitada.') from exc

    raise Http404('No tienes acceso a esta vista.')


def _contexto_detalle_programaciones_ficha(request, usuario, ficha):
    anio_raw = (request.GET.get('anio') or '').strip()
    mes_raw = (request.GET.get('mes') or '').strip()
    instructor_raw = (request.GET.get('instructor_id') or '').strip()
    resultado_busqueda = (request.GET.get('resultado') or '').strip().lower()

    anio_inicio = ficha.fecha_inicio.year
    anio_fin = ficha.fecha_fin.year

    filtro_anio = None
    if anio_raw.isdigit():
        anio_valor = int(anio_raw)
        if anio_inicio <= anio_valor <= anio_fin:
            filtro_anio = anio_valor

    filtro_mes = None
    if mes_raw.isdigit():
        mes_valor = int(mes_raw)
        if 1 <= mes_valor <= 12:
            filtro_mes = mes_valor

    qs_base = ProgramacionDia.objects.filter(codigo_ficha_id=ficha.codigo_ficha).select_related(
        'id_instructor',
        'id_dinamizador_asignador',
        'id_competencia',
        'id_horario',
    )

    ids_instructores = sorted(
        {item for item in qs_base.values_list('id_instructor_id', flat=True) if item}
    )
    instructores_disponibles = Usuario.objects.filter(id_usuario__in=ids_instructores).order_by('nombre', 'apellido')

    filtro_instructor_id = None
    if instructor_raw.isdigit():
        instructor_valor = int(instructor_raw)
        if instructor_valor in ids_instructores:
            filtro_instructor_id = instructor_valor

    qs_filtrado = qs_base
    if filtro_anio:
        qs_filtrado = qs_filtrado.filter(fecha__year=filtro_anio)
    if filtro_mes:
        qs_filtrado = qs_filtrado.filter(fecha__month=filtro_mes)
    if filtro_instructor_id:
        qs_filtrado = qs_filtrado.filter(id_instructor_id=filtro_instructor_id)

    dias = list(qs_filtrado.order_by('fecha', 'id_horario__horario', 'id_programacion_dia'))

    ids_dia = [item.id_programacion_dia for item in dias]
    ids_competencia = sorted({item.id_competencia_id for item in dias})

    asignados_por_dia = {}
    if ids_dia:
        relaciones = ProgramacionDiaResultado.objects.filter(
            id_programacion_dia_id__in=ids_dia,
        ).select_related('id_resultado')
        for rel in relaciones:
            asignados_por_dia.setdefault(rel.id_programacion_dia_id, []).append(
                _normalizar_texto_resultado(rel.id_resultado.nombre)
            )

    resultados_por_competencia = {}
    if ids_competencia:
        for item in Resultado.objects.filter(id_competencia_id__in=ids_competencia).order_by('nombre'):
            resultados_por_competencia.setdefault(item.id_competencia_id, []).append(
                _normalizar_texto_resultado(item.nombre)
            )

    agenda = {}
    combinaciones = {}
    contador_items = 0
    for item in dias:
        combo_key = f"{item.id_instructor_id or 0}-{item.id_horario_id or 0}"
        if combo_key not in combinaciones:
            color = PALETA_COMBINACIONES[len(combinaciones) % len(PALETA_COMBINACIONES)]
            nombre_instructor = f"{item.id_instructor.nombre} {item.id_instructor.apellido}" if item.id_instructor else 'Sin instructor'
            nombre_horario = item.id_horario.horario if item.id_horario else (ficha.id_horario.horario if ficha.id_horario else 'Sin horario')
            combinaciones[combo_key] = {
                'color': color,
                'label': f"{nombre_instructor} | {nombre_horario}",
            }

        inicio_h, fin_h = franja_horaria_desde_horario(item.id_horario)
        if item.hora_inicio:
            inicio_h = item.hora_inicio
        if item.hora_fin:
            fin_h = item.hora_fin
        resultados = asignados_por_dia.get(item.id_programacion_dia)
        if not resultados:
            resultados = resultados_por_competencia.get(item.id_competencia_id, [])

        if resultado_busqueda and not any(resultado_busqueda in (nombre or '').lower() for nombre in resultados):
            continue

        nombre_dinamizador = (
            f"{item.id_dinamizador_asignador.nombre} {item.id_dinamizador_asignador.apellido}"
            if item.id_dinamizador_asignador
            else 'Sin dinamizador'
        )
        nombre_instructor = (
            f"{item.id_instructor.nombre} {item.id_instructor.apellido}"
            if item.id_instructor
            else 'Sin instructor'
        )

        contador_items += 1
        agenda.setdefault(item.fecha, []).append(
            {
                'id': contador_items,
                'color': combinaciones[combo_key]['color'],
                'dinamizador': nombre_dinamizador,
                'instructor': nombre_instructor,
                'horario': f"{inicio_h.strftime('%H:%M')} - {fin_h.strftime('%H:%M')}",
                'horas_dia': item.horas_dia,
                'competencia': item.id_competencia.nombre,
                'resultados': resultados,
                'estado': item.estado,
            }
        )

    cal = calendar.Calendar(firstweekday=0)
    meses_detalle = []
    cursor = date(ficha.fecha_inicio.year, ficha.fecha_inicio.month, 1)
    ultimo = date(ficha.fecha_fin.year, ficha.fecha_fin.month, 1)

    while cursor <= ultimo:
        if filtro_anio and cursor.year != filtro_anio:
            if cursor.month == 12:
                cursor = date(cursor.year + 1, 1, 1)
            else:
                cursor = date(cursor.year, cursor.month + 1, 1)
            continue
        if filtro_mes and cursor.month != filtro_mes:
            if cursor.month == 12:
                cursor = date(cursor.year + 1, 1, 1)
            else:
                cursor = date(cursor.year, cursor.month + 1, 1)
            continue

        semanas = []
        for semana in cal.monthdatescalendar(cursor.year, cursor.month):
            fila = []
            for fecha_actual in semana:
                in_month = fecha_actual.month == cursor.month
                in_range = in_month and ficha.fecha_inicio <= fecha_actual <= ficha.fecha_fin
                fila.append(
                    {
                        'day': fecha_actual.day,
                        'in_month': in_month,
                        'in_range': in_range,
                        'items': agenda.get(fecha_actual, []) if in_range else [],
                    }
                )
            semanas.append(fila)

        meses_detalle.append(
            {
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

    rol = _rol_slug(usuario)
    url_regreso = reverse('dinamizador_programaciones' if rol == 'dinamizador' else 'instructor_programaciones')

    return {
        'ficha': ficha,
        'horario_ficha': ficha.id_horario.horario if ficha.id_horario else 'Sin horario',
        'meses_detalle': meses_detalle,
        'total_registros': contador_items,
        'filtro_anio': filtro_anio,
        'filtro_mes': filtro_mes,
        'filtro_instructor_id': filtro_instructor_id,
        'filtro_resultado': request.GET.get('resultado', '').strip(),
        'anios_ficha': list(range(anio_inicio, anio_fin + 1)),
        'meses_filtro': [(idx, nombre) for idx, nombre in enumerate(MESES_ES) if idx],
        'instructores_disponibles': instructores_disponibles,
        'url_regreso': url_regreso,
    }


def _resumen_inicio_usuario(usuario):
    hoy = timezone.localdate()
    anio = hoy.year
    mes = hoy.month

    horas_mes = float(horas_programadas_instructor_mes(usuario.id_usuario, anio, mes))
    horas_anio = float(horas_programadas_instructor_anio(usuario.id_usuario, anio))

    inicio_mes, fin_mes = _rango_mes(anio, mes)
    inicio_anio = date(anio, 1, 1)
    fin_anio = date(anio, 12, 31)
    horas_mes += _horas_radicados_usuario_en_rango(usuario, inicio_mes, fin_mes)
    horas_anio += _horas_radicados_usuario_en_rango(usuario, inicio_anio, fin_anio)

    meta_mes = float(getattr(usuario, 'horas_max_mensual', 0) or 0)
    meta_anio = float(getattr(usuario, 'horas_objetivo_anual', 0) or 0)

    asignaciones_mes = ProgramacionDia.objects.filter(
        fecha__range=(inicio_mes, fin_mes),
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).filter(
        Q(id_instructor_id=usuario.id_usuario) | Q(id_dinamizador_asignador_id=usuario.id_usuario)
    ).count()

    return {
        'mes_nombre': MESES_ES[mes],
        'anio_actual': anio,
        'usuario_nombre': f"{usuario.nombre} {usuario.apellido}",
        'documento': usuario.documento,
        'email': usuario.email,
        'horas_mes_cumplidas': round(horas_mes, 2),
        'horas_mes_meta': round(meta_mes, 2),
        'horas_mes_faltantes': round(max(0.0, meta_mes - horas_mes), 2),
        'horas_anio_cumplidas': round(horas_anio, 2),
        'horas_anio_meta': round(meta_anio, 2),
        'horas_anio_faltantes': round(max(0.0, meta_anio - horas_anio), 2),
        'asignaciones_mes': asignaciones_mes,
    }
