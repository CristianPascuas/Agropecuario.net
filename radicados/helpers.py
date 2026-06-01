import json
from datetime import date, timedelta

from django.core.exceptions import ValidationError

from academico.models import Programacion, ProgramacionDia, Radicado
from academico.validators import franja_horaria_desde_horario, horas_radicados_aprobados_instructor_mes

from portal.core import _es_instructor_contrato, _puede_radicar, _rango_mes, _rol_slug

TIPOS_ACTIVIDAD_EXTRA = {
    1: 'Normalización y Certificación de Competencias Laborales',
    2: 'Diseño y Desarrollo Curricular',
    3: 'Actividades de Emprendimiento',
    4: 'Seguimiento y Desarrollo Etapa Práctica',
    5: 'Formación y Capacitación',
    6: 'Permiso Sindical',
    7: 'Unidad Productiva',
    8: 'Proyectos de Investigación Aplicada',
    9: 'Fortalecimiento del Idioma para Instructores',
    10: 'Otros',
}

LIMITE_HORAS_RADICADOS_MENSUAL = 80.0


def _archivo_es_pdf(archivo):
    if not archivo:
        return False

    nombre = str(getattr(archivo, 'name', '') or '').strip().lower()
    if not nombre.endswith('.pdf'):
        return False

    content_type = str(getattr(archivo, 'content_type', '') or '').strip().lower()
    if content_type and ('pdf' not in content_type) and (content_type != 'application/octet-stream'):
        return False

    return True


def _intervalos_minutos(inicio, fin):
    inicio_min = (inicio.hour * 60) + inicio.minute
    fin_min = (fin.hour * 60) + fin.minute

    if fin_min <= inicio_min:
        return [(inicio_min, 24 * 60), (0, fin_min)]
    return [(inicio_min, fin_min)]


def _franjas_solapan(inicio_a, fin_a, inicio_b, fin_b):
    for a_ini, a_fin in _intervalos_minutos(inicio_a, fin_a):
        for b_ini, b_fin in _intervalos_minutos(inicio_b, fin_b):
            if max(a_ini, b_ini) < min(a_fin, b_fin):
                return True
    return False


def _minutos_por_dia_radicado(radicado):
    intervalos = _intervalos_minutos(radicado.hora_inicio, radicado.hora_fin)
    return sum(max(0, fin - ini) for ini, fin in intervalos)


def _parse_fechas_radicado_json(raw_value):
    if not raw_value:
        return []
    try:
        data = json.loads(raw_value)
    except (TypeError, ValueError):
        return []
    if not isinstance(data, list):
        return []

    fechas = set()
    for item in data:
        try:
            fechas.add(date.fromisoformat(str(item)))
        except ValueError:
            continue
    return sorted(fechas)


def _fechas_radicado(item):
    return _parse_fechas_radicado_json(getattr(item, 'dias_seleccionados', ''))


def _resumen_fechas_radicado(item):
    fechas = _fechas_radicado(item)
    if not fechas:
        return ''

    if len(fechas) == 1:
        return fechas[0].isoformat()

    if len(fechas) <= 3:
        return ', '.join(f.isoformat() for f in fechas)

    return f"{len(fechas)} dias ({fechas[0].isoformat()} a {fechas[-1].isoformat()})"


def _horas_radicados_usuario_en_rango(usuario, inicio_rango, fin_rango):
    if fin_rango < inicio_rango:
        return 0.0

    radicados_qs = Radicado.objects.filter(
        id_instructor_id=usuario.id_usuario,
        aprobado=1,
    )

    total_horas = 0.0
    for item in radicados_qs:
        dias_en_rango = [f for f in _fechas_radicado(item) if inicio_rango <= f <= fin_rango]
        if not dias_en_rango:
            continue
        minutos_dia = _minutos_por_dia_radicado(item)
        total_horas += (minutos_dia * len(dias_en_rango)) / 60.0

    return total_horas


def _horas_radicado_proyectadas_por_mes(fechas, hora_inicio, hora_fin):
    if not fechas:
        return {}

    minutos_dia = sum(max(0, fin - ini) for ini, fin in _intervalos_minutos(hora_inicio, hora_fin))
    horas_dia = minutos_dia / 60.0
    if horas_dia <= 0:
        return {}

    horas_por_mes = {}
    for fecha_item in sorted(set(fechas)):
        llave = (fecha_item.year, fecha_item.month)
        horas_por_mes[llave] = horas_por_mes.get(llave, 0.0) + horas_dia

    return horas_por_mes


def _validar_tope_mensual_radicados_aprobados(
    instructor,
    fechas,
    hora_inicio,
    hora_fin,
    *,
    excluir_radicado_id=None,
):
    horas_nuevas_por_mes = _horas_radicado_proyectadas_por_mes(fechas, hora_inicio, hora_fin)
    if not horas_nuevas_por_mes:
        return

    for (anio, mes), horas_nuevas in horas_nuevas_por_mes.items():
        horas_aprobadas = horas_radicados_aprobados_instructor_mes(
            instructor.id_usuario,
            anio,
            mes,
            excluir_radicado_id=excluir_radicado_id,
        )
        if horas_aprobadas + horas_nuevas > LIMITE_HORAS_RADICADOS_MENSUAL:
            raise ValidationError(
                (
                    'El instructor supera el tope mensual de radicados aprobados '
                    f'({int(LIMITE_HORAS_RADICADOS_MENSUAL)}h) en {mes}/{anio}.'
                )
            )


def _fecha_traslape_radicado_instructor_por_dias(instructor, fechas, hora_inicio, hora_fin):
    if not fechas:
        return None

    fecha_min = min(fechas)
    fecha_max = max(fechas)
    fechas_set = set(fechas)

    dias_programados = ProgramacionDia.objects.filter(
        id_instructor_id=instructor.id_usuario,
        fecha__in=fechas,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).select_related('id_horario')

    for item in dias_programados:
        inicio_prog, fin_prog = franja_horaria_desde_horario(item.id_horario)
        if item.hora_inicio:
            inicio_prog = item.hora_inicio
        if item.hora_fin:
            fin_prog = item.hora_fin

        if _franjas_solapan(hora_inicio, hora_fin, inicio_prog, fin_prog):
            return item.fecha

    programaciones_legacy = Programacion.objects.filter(
        id_instructor_id=instructor.id_usuario,
        fecha_inicio__lte=fecha_max,
        fecha_fin__gte=fecha_min,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    )

    for item in programaciones_legacy:
        if _franjas_solapan(hora_inicio, hora_fin, item.hora_inicio, item.hora_fin):
            inicio_solape = max(fecha_min, item.fecha_inicio)
            fin_solape = min(fecha_max, item.fecha_fin)
            if inicio_solape > fin_solape:
                continue

            cursor = inicio_solape
            while cursor <= fin_solape:
                if cursor in fechas_set:
                    return cursor
                cursor = cursor + timedelta(days=1)

    return None


def _fechas_traslape_programacion_instructor_mes(instructor, anio, mes, hora_inicio, hora_fin):
    inicio_mes, fin_mes = _rango_mes(anio, mes)
    fechas = set()

    dias_programados = ProgramacionDia.objects.filter(
        id_instructor_id=instructor.id_usuario,
        fecha__range=(inicio_mes, fin_mes),
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).select_related('id_horario')

    for item in dias_programados:
        inicio_prog, fin_prog = franja_horaria_desde_horario(item.id_horario)
        if item.hora_inicio:
            inicio_prog = item.hora_inicio
        if item.hora_fin:
            fin_prog = item.hora_fin
        if _franjas_solapan(hora_inicio, hora_fin, inicio_prog, fin_prog):
            fechas.add(item.fecha)

    legacy_qs = Programacion.objects.filter(
        id_instructor_id=instructor.id_usuario,
        fecha_inicio__lte=fin_mes,
        fecha_fin__gte=inicio_mes,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    )
    for item in legacy_qs:
        if not _franjas_solapan(hora_inicio, hora_fin, item.hora_inicio, item.hora_fin):
            continue
        cursor = max(item.fecha_inicio, inicio_mes)
        tope = min(item.fecha_fin, fin_mes)
        while cursor <= tope:
            fechas.add(cursor)
            cursor = cursor + timedelta(days=1)

    return sorted(fechas)


def _estado_radicado(aprobado):
    estado = int(aprobado or 0)
    if estado == 1:
        return estado, 'Aceptado'
    if estado == 2:
        return estado, 'Rechazado'
    if estado == 3:
        return estado, 'Revisado'
    return 0, 'En espera'


def _puede_aprobar_radicado(usuario_actual, radicado):
    rol_actual = _rol_slug(usuario_actual)
    if rol_actual == 'coordinador':
        return True
    if rol_actual != 'dinamizador':
        return False

    creador = radicado.id_instructor
    if not creador:
        return False
    return _es_instructor_contrato(creador)


def _formato_horas(valor):
    texto = f"{float(valor):.2f}"
    return texto.rstrip('0').rstrip('.') or '0'


def _detalle_carga_radicado(item):
    fechas = _fechas_radicado(item)
    if not fechas:
        return {
            'fecha_inicio': '-',
            'fecha_fin': '-',
            'dias_total': 0,
            'horas_diarias': '0',
            'horas_totales': '0',
        }

    minutos_dia = _minutos_por_dia_radicado(item)
    horas_diarias = minutos_dia / 60.0
    horas_totales = horas_diarias * len(fechas)

    return {
        'fecha_inicio': fechas[0].isoformat(),
        'fecha_fin': fechas[-1].isoformat(),
        'dias_total': len(fechas),
        'horas_diarias': _formato_horas(horas_diarias),
        'horas_totales': _formato_horas(horas_totales),
    }


def _contexto_radicados(usuario):
    rol = _rol_slug(usuario)
    radicados_qs = Radicado.objects.select_related('id_instructor').order_by('-creado_en', '-id_radicado')
    if rol == 'instructor':
        radicados_qs = radicados_qs.filter(id_instructor_id=usuario.id_usuario)

    radicados = []
    for item in radicados_qs:
        estado_valor, estado_texto = _estado_radicado(item.aprobado)
        tipo_valor = int(item.tipo_radicado or 0)
        tipo_texto = TIPOS_ACTIVIDAD_EXTRA.get(tipo_valor, 'Otros')
        responsable = f"{item.id_instructor.nombre} {item.id_instructor.apellido}" if item.id_instructor else 'Sin instructor'
        detalle = _detalle_carga_radicado(item)
        search_text = ' '.join(
            [
                item.nombre_radicado or '',
                tipo_texto,
                item.descripcion_radicado or '',
                item.empresa_organizacion or '',
                item.nit or '',
                item.lugar or '',
                responsable,
                detalle['fecha_inicio'],
                detalle['fecha_fin'],
            ]
        ).lower()
        radicados.append(
            {
                'id': item.id_radicado,
                'nombre': item.nombre_radicado,
                'tipo': tipo_valor,
                'tipo_texto': tipo_texto,
                'descripcion': item.descripcion_radicado,
                'empresa_organizacion': item.empresa_organizacion,
                'nit': item.nit,
                'lugar': item.lugar,
                'fecha': _resumen_fechas_radicado(item),
                'fecha_inicio': detalle['fecha_inicio'],
                'fecha_fin': detalle['fecha_fin'],
                'dias_total': detalle['dias_total'],
                'horas_diarias': detalle['horas_diarias'],
                'horas_totales': detalle['horas_totales'],
                'archivo_url': item.archivo_excel.url if item.archivo_excel else '',
                'estado': estado_valor,
                'estado_texto': estado_texto,
                'puede_aprobar': _puede_aprobar_radicado(usuario, item),
                'responsable': responsable,
                'search_text': search_text,
            }
        )

    return {
        'radicados': radicados,
        'tipos_actividad_extra': TIPOS_ACTIVIDAD_EXTRA,
        'puede_gestionar_radicados': rol in ('dinamizador', 'coordinador'),
        'puede_radicar': _puede_radicar(usuario),
    }
