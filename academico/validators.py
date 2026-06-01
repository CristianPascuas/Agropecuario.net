from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta

from django.core.exceptions import ValidationError
from django.db.models import Exists, OuterRef, Q, Sum

from .models import Programacion, ProgramacionDia, Radicado


def politica_horas_mensuales(instructor) -> dict:
    """Politica mensual de horas por tipo de contrato.

    Contrato 0: max bloqueante 180, meta ideal 160, minimo 120.
    Contrato 1: max bloqueante 120, meta ideal 120, minimo 120.
    """
    tipo_contrato = int(getattr(instructor, 'tipo_contrato', 0) or 0)
    if tipo_contrato == 1:
        return {
            'maximo_bloqueante': 120.0,
            'meta_ideal': 120.0,
            'minimo_mensual': 120.0,
        }

    return {
        'maximo_bloqueante': 180.0,
        'meta_ideal': 160.0,
        'minimo_mensual': 120.0,
    }


def _horas_legacy_programacion(item: Programacion, desde: date | None = None, hasta: date | None = None) -> float:
    """Calcula horas de un registro legacy de Programacion para un rango dado."""
    inicio = item.fecha_inicio if desde is None else max(item.fecha_inicio, desde)
    fin = item.fecha_fin if hasta is None else min(item.fecha_fin, hasta)

    if fin < inicio:
        return 0.0

    dt_inicio = datetime.combine(inicio, item.hora_inicio)
    dt_fin = datetime.combine(inicio, item.hora_fin)
    if dt_fin <= dt_inicio:
        dt_fin = dt_fin + timedelta(days=1)

    horas_dia = (dt_fin - dt_inicio).total_seconds() / 3600.0
    dias = (fin - inicio).days + 1
    return max(0.0, horas_dia * dias)


def _legacy_programacion_sin_detalle(queryset):
    """Devuelve solo cabeceras legacy que no tienen detalle diario equivalente."""
    detalle_relacionado = ProgramacionDia.objects.filter(
        codigo_ficha_id=OuterRef('codigo_ficha_id'),
        id_competencia_id=OuterRef('id_competencia_id'),
        id_instructor_id=OuterRef('id_instructor_id'),
        fecha__gte=OuterRef('fecha_inicio'),
        fecha__lte=OuterRef('fecha_fin'),
    )
    return queryset.annotate(_tiene_detalle=Exists(detalle_relacionado)).filter(_tiene_detalle=False)


def horas_programadas_competencia_ficha(codigo_ficha_id: int, competencia_id: int) -> float:
    total_dia = (
        ProgramacionDia.objects.filter(
            codigo_ficha_id=codigo_ficha_id,
            id_competencia_id=competencia_id,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        ).aggregate(total=Sum('horas_dia'))['total']
        or 0
    )

    legacy = 0.0
    legacy_qs = _legacy_programacion_sin_detalle(
        Programacion.objects.filter(
            codigo_ficha_id=codigo_ficha_id,
            id_competencia_id=competencia_id,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        )
    )
    for item in legacy_qs:
        legacy += _horas_legacy_programacion(item)

    return float(total_dia) + legacy


def horas_programadas_instructor_mes(instructor_id: int, anio: int, mes: int) -> float:
    total_dia = (
        ProgramacionDia.objects.filter(
            id_instructor_id=instructor_id,
            fecha__year=anio,
            fecha__month=mes,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        ).aggregate(total=Sum('horas_dia'))['total']
        or 0
    )

    inicio_mes = date(anio, mes, 1)
    if mes == 12:
        fin_mes = date(anio, 12, 31)
    else:
        fin_mes = date(anio, mes + 1, 1) - timedelta(days=1)

    legacy = 0.0
    legacy_qs = _legacy_programacion_sin_detalle(
        Programacion.objects.filter(
            id_instructor_id=instructor_id,
            fecha_inicio__lte=fin_mes,
            fecha_fin__gte=inicio_mes,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        )
    )
    for item in legacy_qs:
        legacy += _horas_legacy_programacion(item, inicio_mes, fin_mes)

    return float(total_dia) + legacy


def horas_programadas_instructor_anio(instructor_id: int, anio: int) -> float:
    total_dia = (
        ProgramacionDia.objects.filter(
            id_instructor_id=instructor_id,
            fecha__year=anio,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        ).aggregate(total=Sum('horas_dia'))['total']
        or 0
    )

    inicio_anio = date(anio, 1, 1)
    fin_anio = date(anio, 12, 31)

    legacy = 0.0
    legacy_qs = _legacy_programacion_sin_detalle(
        Programacion.objects.filter(
            id_instructor_id=instructor_id,
            fecha_inicio__lte=fin_anio,
            fecha_fin__gte=inicio_anio,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        )
    )
    for item in legacy_qs:
        legacy += _horas_legacy_programacion(item, inicio_anio, fin_anio)

    return float(total_dia) + legacy


def validar_solape_instructor(
    fecha: date,
    codigo_ficha_id: int,
    instructor_id: int,
    excluir_programacion_id: int | None = None,
) -> None:
    conflicto = ProgramacionDia.objects.filter(
        fecha=fecha,
        codigo_ficha_id=codigo_ficha_id,
        id_instructor_id=instructor_id,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).exists()

    if not conflicto:
        conflicto_qs = Programacion.objects.filter(
            codigo_ficha_id=codigo_ficha_id,
            id_instructor_id=instructor_id,
            fecha_inicio__lte=fecha,
            fecha_fin__gte=fecha,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        )
        if excluir_programacion_id:
            conflicto_qs = conflicto_qs.exclude(id_programacion=excluir_programacion_id)
        conflicto = conflicto_qs.exists()

    if conflicto:
        raise ValidationError('Traslape: el instructor ya esta asignado en la misma ficha y fecha.')


def _intervalos_minutos(inicio: time, fin: time) -> list[tuple[int, int]]:
    inicio_min = (inicio.hour * 60) + inicio.minute
    fin_min = (fin.hour * 60) + fin.minute

    if fin_min <= inicio_min:
        return [(inicio_min, 24 * 60), (0, fin_min)]
    return [(inicio_min, fin_min)]


def _franjas_solapan(inicio_a: time, fin_a: time, inicio_b: time, fin_b: time) -> bool:
    for a_ini, a_fin in _intervalos_minutos(inicio_a, fin_a):
        for b_ini, b_fin in _intervalos_minutos(inicio_b, fin_b):
            if max(a_ini, b_ini) < min(a_fin, b_fin):
                return True
    return False


def _parse_fechas_radicado(item: Radicado) -> list[date]:
    raw = (getattr(item, 'dias_seleccionados', '') or '').strip()
    if raw:
        try:
            data = json.loads(raw)
        except (TypeError, ValueError):
            data = []
        if isinstance(data, list):
            fechas = []
            for valor in data:
                try:
                    fechas.append(date.fromisoformat(str(valor)))
                except ValueError:
                    continue
            if fechas:
                return sorted(set(fechas))

    return []


def _minutos_por_dia_radicado(item: Radicado) -> int:
    intervalos = _intervalos_minutos(item.hora_inicio, item.hora_fin)
    return sum(max(0, fin - ini) for ini, fin in intervalos)


def horas_radicados_aprobados_instructor_en_rango(
    instructor_id: int,
    inicio_rango: date,
    fin_rango: date,
    excluir_radicado_id: int | None = None,
) -> float:
    if fin_rango < inicio_rango:
        return 0.0

    radicados_qs = Radicado.objects.filter(
        id_instructor_id=instructor_id,
        aprobado=1,
    )
    if excluir_radicado_id:
        radicados_qs = radicados_qs.exclude(id_radicado=excluir_radicado_id)

    total_horas = 0.0
    for item in radicados_qs:
        dias_en_rango = [f for f in _parse_fechas_radicado(item) if inicio_rango <= f <= fin_rango]
        if not dias_en_rango:
            continue
        minutos_dia = _minutos_por_dia_radicado(item)
        total_horas += (minutos_dia * len(dias_en_rango)) / 60.0

    return total_horas


def horas_radicados_aprobados_instructor_mes(
    instructor_id: int,
    anio: int,
    mes: int,
    excluir_radicado_id: int | None = None,
) -> float:
    inicio_mes = date(anio, mes, 1)
    if mes == 12:
        fin_mes = date(anio, 12, 31)
    else:
        fin_mes = date(anio, mes + 1, 1) - timedelta(days=1)

    return horas_radicados_aprobados_instructor_en_rango(
        instructor_id,
        inicio_mes,
        fin_mes,
        excluir_radicado_id=excluir_radicado_id,
    )


def validar_solape_radicado_aprobado(
    fecha: date,
    instructor_id: int,
    hora_inicio: time,
    hora_fin: time,
) -> None:
    radicados = Radicado.objects.filter(
        id_instructor_id=instructor_id,
        aprobado=1,
    )

    for item in radicados:
        if fecha not in set(_parse_fechas_radicado(item)):
            continue
        if _franjas_solapan(hora_inicio, hora_fin, item.hora_inicio, item.hora_fin):
            raise ValidationError('Traslape: el instructor tiene un radicado aprobado en esta fecha y franja horaria.')


def validar_solape_ambiente(
    fecha: date,
    horario,
    ambiente_id: int,
    excluir_programacion_id: int | None = None,
) -> None:
    conflicto = ProgramacionDia.objects.filter(
        fecha=fecha,
        id_horario_id=horario.id_horario,
        codigo_ficha__id_ambiente_id=ambiente_id,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).exists()

    if conflicto:
        raise ValidationError('El ambiente ya esta ocupado en la misma fecha y horario.')

    hora_inicio, hora_fin = franja_horaria_desde_horario(horario)

    candidatos = Programacion.objects.filter(
        fecha_inicio__lte=fecha,
        fecha_fin__gte=fecha,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).filter(
        Q(id_ambiente_id=ambiente_id)
        | Q(id_ambiente__isnull=True, codigo_ficha__id_ambiente_id=ambiente_id)
    )
    if excluir_programacion_id:
        candidatos = candidatos.exclude(id_programacion=excluir_programacion_id)

    for item in candidatos:
        if _franjas_solapan(hora_inicio, hora_fin, item.hora_inicio, item.hora_fin):
            raise ValidationError('El ambiente ya esta ocupado en la misma fecha y horario.')


def validar_solape_usuario(fecha: date, id_horario_id: int, usuario_id: int) -> None:
    conflicto = ProgramacionDia.objects.filter(
        fecha=fecha,
        id_horario_id=id_horario_id,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).filter(
        Q(id_instructor_id=usuario_id) | Q(id_dinamizador_asignador_id=usuario_id)
    ).exists()

    if conflicto:
        raise ValidationError('El usuario ya esta comprometido en la misma fecha y horario.')


def _rango_semana_iso(fecha: date) -> tuple[date, date]:
    inicio = fecha - timedelta(days=fecha.weekday())
    fin = inicio + timedelta(days=6)
    return inicio, fin


def validar_instructor_tipo_competencia_semana(
    *,
    fecha: date,
    codigo_ficha_id: int,
    competencia,
    instructor_id: int,
) -> None:
    inicio_semana, fin_semana = _rango_semana_iso(fecha)
    tipo = competencia.tipo_competencia

    conflicto_dia = ProgramacionDia.objects.filter(
        codigo_ficha_id=codigo_ficha_id,
        fecha__range=(inicio_semana, fin_semana),
        id_competencia__tipo_competencia=tipo,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).exclude(id_instructor_id=instructor_id).exists()

    conflicto_legacy = Programacion.objects.filter(
        codigo_ficha_id=codigo_ficha_id,
        id_competencia__tipo_competencia=tipo,
        fecha_inicio__lte=fin_semana,
        fecha_fin__gte=inicio_semana,
        estado__in=['programada', 'ajustada', 'ejecutada'],
    ).exclude(id_instructor_id=instructor_id).exists()

    if conflicto_dia or conflicto_legacy:
        if tipo == 'tecnica':
            raise ValidationError('Traslape semanal: la ficha ya tiene un instructor tecnico diferente en esta semana.')
        raise ValidationError('Traslape semanal: la ficha ya tiene un instructor trasversal diferente en esta semana.')


def validar_horas_competencia(
    codigo_ficha_id: int,
    competencia_id: int,
    horas_adicionales: float,
    horas_max_competencia: int,
) -> None:
    total_actual = horas_programadas_competencia_ficha(codigo_ficha_id, competencia_id)
    if total_actual + horas_adicionales > float(horas_max_competencia):
        raise ValidationError('La programacion supera las horas maximas permitidas para la competencia.')


def validar_tope_mensual(instructor, fecha: date, horas_adicionales: float) -> None:
    total_actual = horas_programadas_instructor_mes(instructor.id_usuario, fecha.year, fecha.month)
    total_actual += horas_radicados_aprobados_instructor_mes(instructor.id_usuario, fecha.year, fecha.month)
    maximo = politica_horas_mensuales(instructor)['maximo_bloqueante']
    if total_actual + horas_adicionales > maximo:
        raise ValidationError('La asignacion supera el tope mensual del instructor.')


def validar_tope_anual(instructor, fecha: date, horas_adicionales: float) -> None:
    total_actual = horas_programadas_instructor_anio(instructor.id_usuario, fecha.year)
    if total_actual + horas_adicionales > float(instructor.horas_objetivo_anual):
        raise ValidationError('La asignacion supera el tope anual del instructor.')


def evaluar_minimo_mensual(instructor, anio: int, mes: int) -> dict:
    total_actual = horas_programadas_instructor_mes(instructor.id_usuario, anio, mes)
    total_actual += horas_radicados_aprobados_instructor_mes(instructor.id_usuario, anio, mes)
    minimo_mensual = politica_horas_mensuales(instructor)['minimo_mensual']
    return {
        'minimo': int(minimo_mensual),
        'actual': round(total_actual, 2),
        'cumple': total_actual >= minimo_mensual,
    }


def horas_por_dia_desde_horario(horario) -> int:
    """Convierte horas semanales de horario en carga diaria esperada para programacion."""
    if not horario or not horario.horas:
        return 0
    return max(1, int(round(float(horario.horas) / 5.0)))


def franja_horaria_desde_horario(horario) -> tuple[time, time]:
    """Deriva una franja horaria aproximada para mantener compatibilidad con Programacion."""
    nombre = (horario.horario or '').strip().lower()
    normalizado = nombre.replace('ñ', 'n')

    if 'man' in normalizado:
        return time(7, 0), time(13, 0)
    if 'tarde' in normalizado:
        return time(13, 0), time(18, 0)
    if 'noche' in normalizado:
        return time(18, 0), time(22, 0)

    inicio = time(7, 0)
    fin = time((7 + max(1, min(12, int(horario.horas)))) % 24, 0)
    if fin <= inicio:
        fin = time(23, 59)
    return inicio, fin
