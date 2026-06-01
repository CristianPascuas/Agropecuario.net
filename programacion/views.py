import json
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from academico.models import Ambiente, Competencia, EquipoEjecutor, Ficha, Horario, Municipio, Programacion, ProgramacionDia, ProgramacionDiaResultado, ProgramacionResultado, Resultado, Usuario
from academico.services import (
    detalle_programacion_para_edicion,
    editar_programacion_existente,
    guardar_programacion_dias,
    ids_equipos_disponibles_para_dinamizador,
    instructores_elegibles,
)
from academico.validators import (
    franja_horaria_desde_horario,
    horas_por_dia_desde_horario,
    horas_programadas_competencia_ficha,
)

from portal.core import MESES_ES, _contexto_base, role_required

from .forms import CrearFichaForm
from .helpers import (
    SESSION_PROGRAMACION_TEST_MODE_KEY,
    _anio_mes_programacion,
    _calendario_mes_ficha,
    _competencias_programa_con_contador,
    _fechas_ajuste_noche_auto,
    _fechas_programadas_competencia_ficha,
    _meses_en_rango,
    _modo_pruebas_programacion_activo,
    _obtener_ficha_dinamizador,
    _obtener_programacion_de_ficha,
    _parse_horario_especial_payload,
    _politica_programacion_mes,
    _resumen_instructor,
    _validar_mes_en_rango_ficha,
)


def _round2(valor: float) -> float:
    return round(float(valor or 0.0) + 1e-9, 2)


def _distribucion_equitativa(total: float, resultado_ids: list[int]) -> dict[int, float]:
    if not resultado_ids:
        return {}
    total = _round2(total)
    base = _round2(total / len(resultado_ids))
    distribucion = {rid: base for rid in resultado_ids}
    ajuste = _round2(total - _round2(sum(distribucion.values())))
    distribucion[resultado_ids[-1]] = _round2(distribucion[resultado_ids[-1]] + ajuste)
    return distribucion


def _parse_horas_resultados_competencia(competencia, objetivo_raw, horas_raw):
    resultados = list(Resultado.objects.filter(id_competencia_id=competencia.id_competencia).order_by('id_resultado'))
    resultado_ids = [item.id_resultado for item in resultados]
    horas_max = _round2(float(competencia.horas_max or 0.0))
    recomendado = _round2(horas_max * 0.75)

    if not resultado_ids:
        return {
            'objetivo_horas': 0.0,
            'recomendado_horas': recomendado,
            'porcentaje_objetivo': 0.0,
            'horas_resultados_map': {},
            'aviso': '',
            'resultados': [],
        }

    if objetivo_raw in (None, ''):
        objetivo = 0.0
    else:
        try:
            objetivo = _round2(float(objetivo_raw))
        except (TypeError, ValueError):
            raise ValidationError('El objetivo de horas de competencia es inválido.')

    if objetivo < 0:
        raise ValidationError('El objetivo de horas de competencia no puede ser negativo.')
    if objetivo > horas_max:
        raise ValidationError('El objetivo de horas no puede superar el 100% de la competencia.')

    horas_map = {}
    if isinstance(horas_raw, list):
        for item in horas_raw:
            try:
                rid = int(item.get('resultado_id'))
                horas = _round2(float(item.get('horas')))
            except (TypeError, ValueError):
                raise ValidationError('La distribución de horas por resultado es inválida.')
            if horas < 0:
                raise ValidationError('Las horas por resultado no pueden ser negativas.')
            horas_map[rid] = horas
    elif isinstance(horas_raw, dict):
        for rid_raw, horas_raw_valor in horas_raw.items():
            try:
                rid = int(rid_raw)
                horas = _round2(float(horas_raw_valor))
            except (TypeError, ValueError):
                raise ValidationError('La distribución de horas por resultado es inválida.')
            if horas < 0:
                raise ValidationError('Las horas por resultado no pueden ser negativas.')
            horas_map[rid] = horas

    if not horas_map:
        horas_map = _distribucion_equitativa(objetivo, resultado_ids)
    else:
        faltantes = [rid for rid in resultado_ids if rid not in horas_map]
        extras = [rid for rid in horas_map.keys() if rid not in set(resultado_ids)]
        if extras:
            raise ValidationError('Debes enviar horas para todos los resultados de la competencia seleccionada.')
        # Resultados faltantes se completan con 0
        for rid in faltantes:
            horas_map[rid] = 0.0

        suma_horas = _round2(sum(horas_map.values()))
        if suma_horas > horas_max + 0.01:
            raise ValidationError('La suma de horas por resultado supera las horas máximas de la competencia.')

    aviso = ''
    if objetivo < recomendado:
        aviso = 'Aviso: estás por debajo del 75% recomendado para esta competencia.'

    return {
        'objetivo_horas': objetivo,
        'recomendado_horas': recomendado,
        'porcentaje_objetivo': _round2((objetivo / horas_max) * 100) if horas_max > 0 else 0.0,
        'horas_resultados_map': horas_map,
        'aviso': aviso,
        'resultados': resultados,
    }


def _resumen_resultados_competencia_ficha(ficha, competencia):
    resultados = list(
        Resultado.objects.filter(id_competencia_id=competencia.id_competencia).order_by('id_resultado')
    )
    resultado_ids = [item.id_resultado for item in resultados]

    horas_max = _round2(float(competencia.horas_max or 0.0))
    recomendado = _round2(horas_max * 0.75)

    horas_dictadas_qs = (
        ProgramacionResultado.objects.filter(
            id_programacion__codigo_ficha_id=ficha.codigo_ficha,
            id_programacion__estado__in=['programada', 'ajustada', 'ejecutada'],
            id_resultado_id__in=resultado_ids,
        )
        .values('id_resultado_id')
        .annotate(total=Sum('horas_dictadas'))
    )
    horas_dictadas_map = {
        int(item['id_resultado_id']): _round2(float(item['total'] or 0.0))
        for item in horas_dictadas_qs
    }

    legacy_horas_qs = (
        ProgramacionDiaResultado.objects.filter(
            id_programacion_dia__codigo_ficha_id=ficha.codigo_ficha,
            id_resultado_id__in=resultado_ids,
            id_programacion_dia__estado__in=['programada', 'ajustada', 'ejecutada'],
        )
        .values('id_resultado_id')
        .annotate(total=Sum('id_programacion_dia__horas_dia'))
    )
    legacy_horas_map = {
        int(item['id_resultado_id']): _round2(float(item['total'] or 0.0))
        for item in legacy_horas_qs
    }

    if not horas_dictadas_map:
        horas_dictadas_map = dict(legacy_horas_map)
    else:
        for rid in resultado_ids:
            if _round2(horas_dictadas_map.get(rid, 0.0)) <= 0 and _round2(legacy_horas_map.get(rid, 0.0)) > 0:
                horas_dictadas_map[rid] = legacy_horas_map[rid]

    objetivos_qs = (
        ProgramacionResultado.objects.filter(
            id_programacion__codigo_ficha_id=ficha.codigo_ficha,
            id_resultado_id__in=resultado_ids,
        )
        .select_related('id_resultado')
        .order_by('id_resultado_id', '-id_programacion_id')
    )
    objetivos_map = {}
    objetivos_fijadas_map = {}
    for item in objetivos_qs:
        rid = int(item.id_resultado_id)
        if rid in objetivos_map:
            continue
        objetivos_map[rid] = _round2(float(item.horas_objetivo or 0.0))
        objetivos_fijadas_map[rid] = True

    if not objetivos_map:
        objetivos_map = {rid: 0.0 for rid in resultado_ids}
        objetivos_fijadas_map = {rid: False for rid in resultado_ids}
    else:
        for rid in resultado_ids:
            objetivos_map.setdefault(rid, 0.0)
            objetivos_fijadas_map.setdefault(rid, False)

    objetivo_horas = _round2(sum(objetivos_map.get(rid, 0.0) for rid in resultado_ids))

    data = []
    for item in resultados:
        objetivo_item = _round2(objetivos_map.get(item.id_resultado, 0.0))
        dictadas_item = _round2(horas_dictadas_map.get(item.id_resultado, 0.0))
        data.append(
            {
                'id': item.id_resultado,
                'nombre': item.nombre,
                'horas_objetivo': objetivo_item,
                'horas_fijadas': bool(objetivos_fijadas_map.get(item.id_resultado, False)),
                'horas_dictadas': dictadas_item,
                'horas_pendientes': _round2(max(0.0, objetivo_item - dictadas_item)),
            }
        )

    return {
        'resultados': data,
        'objetivo_horas': objetivo_horas,
        'recomendado_horas': recomendado,
        'porcentaje_objetivo': _round2((objetivo_horas / horas_max) * 100) if horas_max > 0 else 0.0,
    }


def _resultados_catalogo_programa_ficha(ficha):
    resultados = (
        Resultado.objects.filter(
            id_competencia__id_programa_formacion_id=ficha.id_programa_formacion_id,
        )
        .select_related('id_competencia')
        .order_by('id_competencia__nombre', 'nombre')
    )
    return [
        {
            'id': item.id_resultado,
            'nombre': item.nombre,
            'competencia_id': item.id_competencia_id,
            'competencia_nombre': item.id_competencia.nombre,
            'competencia_tipo': item.id_competencia.tipo_competencia,
            'label': f"{item.nombre} ({item.id_competencia.nombre})",
        }
        for item in resultados
    ]


@role_required('dinamizador')
def dinamizador_programar_fichas(request, usuario):
    modo_form_activo = 'crear'
    ficha_edicion = None
    if request.method == 'POST':
        modo_form_activo = (request.POST.get('modo_form') or 'crear').strip().lower()
        if modo_form_activo == 'editar':
            codigo_original = request.POST.get('codigo_ficha_original')
            if not (codigo_original and str(codigo_original).isdigit()):
                messages.error(request, 'No se recibió la ficha a editar.')
                return redirect('dinamizador_programar_fichas')
            try:
                ficha_edicion = Ficha.objects.get(
                    codigo_ficha=int(codigo_original),
                    id_equipo_id=usuario.id_equipo_id,
                )
            except Ficha.DoesNotExist:
                messages.error(request, 'No se encontró la ficha para editar o no pertenece a tu equipo.')
                return redirect('dinamizador_programar_fichas')

    form = CrearFichaForm(request.POST or None, usuario=usuario, ficha_actual=ficha_edicion)
    busqueda = request.GET.get('q', '').strip()
    ambientes_catalogo = list(
        Ambiente.objects.filter(codigo_municipio__isnull=False)
        .values('id_ambiente', 'ambiente', 'codigo_municipio_id')
        .order_by('ambiente')
    )
    municipios_catalogo = list(
        Municipio.objects.order_by('municipio').values('codigo_municipio', 'municipio')
    )

    if request.method == 'POST' and form.is_valid():
        horario = Horario.objects.get(id_horario=int(form.cleaned_data['id_horario']))
        if modo_form_activo == 'editar' and ficha_edicion:
            ficha_edicion.id_programa_formacion = form.cleaned_data['id_programa_formacion']
            ficha_edicion.id_lider_ficha = form.cleaned_data['id_lider_ficha']
            ficha_edicion.id_horario = horario
            ficha_edicion.tipo_ficha = form.cleaned_data['tipo_ficha']
            ficha_edicion.fecha_inicio = form.cleaned_data['fecha_inicio']
            ficha_edicion.fecha_fin = form.cleaned_data['fecha_fin']
            ficha_edicion.codigo_municipio = form.cleaned_data['codigo_municipio']
            ficha_edicion.id_ambiente = form.cleaned_data['id_ambiente']
            ficha_edicion.save()
            messages.success(request, f'Ficha {ficha_edicion.codigo_ficha} actualizada correctamente.')
        else:
            Ficha.objects.create(
                codigo_ficha=form.cleaned_data['codigo_ficha'],
                id_programa_formacion=form.cleaned_data['id_programa_formacion'],
                id_equipo_id=usuario.id_equipo_id,
                id_lider_ficha=form.cleaned_data['id_lider_ficha'],
                id_horario=horario,
                tipo_ficha=form.cleaned_data['tipo_ficha'],
                fecha_inicio=form.cleaned_data['fecha_inicio'],
                fecha_fin=form.cleaned_data['fecha_fin'],
                codigo_municipio=form.cleaned_data['codigo_municipio'],
                id_ambiente=form.cleaned_data['id_ambiente'],
            )
            messages.success(request, 'Ficha creada correctamente.')
        return redirect('dinamizador_programar_fichas')

    fichas_recientes = Ficha.objects.none()
    if usuario.id_equipo_id:
        fichas_queryset = Ficha.objects.filter(id_equipo_id=usuario.id_equipo_id)

        if busqueda:
            if busqueda.isdigit():
                fichas_queryset = fichas_queryset.filter(codigo_ficha=int(busqueda))
            else:
                fichas_queryset = fichas_queryset.none()

        fichas_recientes = (
            fichas_queryset
            .select_related('id_programa_formacion', 'id_horario', 'id_ambiente', 'codigo_municipio', 'id_lider_ficha')
            .order_by('-codigo_ficha')[:50]
        )

    contexto = _contexto_base(request, usuario, 'Programar fichas')
    contexto.update(
        {
            'form': form,
            'fichas_recientes': fichas_recientes,
            'busqueda': busqueda,
            'ambientes_catalogo': ambientes_catalogo,
            'municipios_catalogo': municipios_catalogo,
            'modo_form_activo': modo_form_activo,
        }
    )
    return render(
        request,
        'portal/dinamizador/programar_fichas.html',
        contexto,
    )


@role_required('dinamizador')
@require_http_methods(['POST'])
def api_dinamizador_crear_ambiente(request, usuario):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('JSON inválido.')

    municipio_id = payload.get('codigo_municipio')
    ambiente_nombre = (payload.get('ambiente') or '').strip()
    lugar = (payload.get('lugar') or '').strip()

    if not municipio_id:
        return HttpResponseBadRequest('El municipio es obligatorio.')
    if not ambiente_nombre:
        return HttpResponseBadRequest('El nombre del ambiente es obligatorio.')
    if not lugar:
        return HttpResponseBadRequest('El lugar del ambiente es obligatorio.')

    try:
        municipio = Municipio.objects.get(codigo_municipio=int(municipio_id))
    except (TypeError, ValueError, Municipio.DoesNotExist):
        return HttpResponseBadRequest('Municipio inválido.')

    ambiente_obj = Ambiente.objects.filter(
        codigo_municipio=municipio,
        ambiente__iexact=ambiente_nombre,
        lugar__iexact=lugar,
    ).first()

    creado = False
    if not ambiente_obj:
        ambiente_obj = Ambiente.objects.create(
            codigo_municipio=municipio,
            ambiente=ambiente_nombre,
            lugar=lugar,
        )
        creado = True

    return JsonResponse(
        {
            'creado': creado,
            'ambiente': {
                'id_ambiente': ambiente_obj.id_ambiente,
                'ambiente': ambiente_obj.ambiente,
                'lugar': ambiente_obj.lugar,
                'codigo_municipio_id': ambiente_obj.codigo_municipio_id,
                'municipio': municipio.municipio,
            },
        }
    )


@role_required('dinamizador')
@require_http_methods(['POST'])
def dinamizador_eliminar_ficha(request, usuario, codigo_ficha):
    try:
        ficha = Ficha.objects.get(codigo_ficha=codigo_ficha, id_equipo_id=usuario.id_equipo_id)
    except Ficha.DoesNotExist:
        messages.error(request, 'No se encontró la ficha para eliminar o no pertenece a tu equipo.')
        return redirect('dinamizador_programar_fichas')

    try:
        with transaction.atomic():
            dias_ids = list(
                ProgramacionDia.objects.filter(codigo_ficha_id=ficha.codigo_ficha).values_list('id_programacion_dia', flat=True)
            )
            if dias_ids:
                ProgramacionDiaResultado.objects.filter(id_programacion_dia_id__in=dias_ids).delete()

            ProgramacionDia.objects.filter(codigo_ficha_id=ficha.codigo_ficha).delete()
            ProgramacionResultado.objects.filter(id_programacion__codigo_ficha_id=ficha.codigo_ficha).delete()
            Programacion.objects.filter(codigo_ficha_id=ficha.codigo_ficha).delete()
            ficha.delete()
    except Exception:
        messages.error(request, 'No fue posible eliminar la ficha. Intenta de nuevo.')
        return redirect('dinamizador_programar_fichas')

    messages.success(request, f'Ficha {codigo_ficha} eliminada junto con sus programaciones.')
    return redirect('dinamizador_programar_fichas')


@role_required('dinamizador')
@require_http_methods(['POST'])
def dinamizador_toggle_modo_pruebas_programacion(request, usuario):
    actual = _modo_pruebas_programacion_activo(request)
    activar_raw = (request.POST.get('activar') or '').strip().lower()

    if activar_raw in ('1', 'true', 'on', 'activar'):
        nuevo = True
    elif activar_raw in ('0', 'false', 'off', 'desactivar'):
        nuevo = False
    else:
        nuevo = not actual

    request.session[SESSION_PROGRAMACION_TEST_MODE_KEY] = bool(nuevo)
    request.session.modified = True

    siguiente = (request.POST.get('next') or '').strip()
    if not siguiente.startswith('/'):
        siguiente = reverse('dinamizador_programar_fichas')
    return redirect(siguiente)


@role_required('dinamizador')
def dinamizador_ficha_programacion(request, usuario, codigo_ficha):
    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)

    programaciones = Programacion.objects.filter(codigo_ficha_id=ficha.codigo_ficha).select_related(
        'id_competencia', 'id_instructor', 'id_dinamizador_asignador'
    ).order_by('-fecha_inicio', '-id_programacion')

    hoy = timezone.localdate()
    modo_pruebas = _modo_pruebas_programacion_activo(request)
    total_dia = (
        ProgramacionDia.objects.filter(
            codigo_ficha_id=ficha.codigo_ficha,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        ).aggregate(total=Sum('horas_dia'))['total']
        or 0
    )

    if total_dia > 0:
        total_horas_completadas = float(total_dia)
    else:
        total_horas_completadas = 0.0
        for item in programaciones:
            inicio = datetime.combine(item.fecha_inicio, item.hora_inicio)
            fin = datetime.combine(item.fecha_inicio, item.hora_fin)
            if fin <= inicio:
                fin = fin + timedelta(days=1)
            horas_dia = (fin - inicio).total_seconds() / 3600.0
            dias = (item.fecha_fin - item.fecha_inicio).days + 1
            if dias < 1:
                dias = 1
            total_horas_completadas += horas_dia * dias

    total_horas_completadas = min(total_horas_completadas, float(ficha.id_programa_formacion.horas_lectiva))

    meses_rango = _meses_en_rango(ficha.fecha_inicio, ficha.fecha_fin)
    meses_rango = [
        {
            **item,
            **_politica_programacion_mes(item['anio'], item['mes'], hoy, modo_pruebas=modo_pruebas),
        }
        for item in meses_rango
    ]

    for item in programaciones:
        anio_item, mes_item = _anio_mes_programacion(item)
        politica_item = _politica_programacion_mes(anio_item, mes_item, hoy, modo_pruebas=modo_pruebas)
        item.anio_operativo_ui = anio_item
        item.mes_operativo_ui = mes_item
        item.permite_editar_ui = politica_item['permite_editar']
        item.motivo_edicion_ui = politica_item['mensaje_edicion']

    contexto = _contexto_base(request, usuario, f'Programacion ficha {ficha.codigo_ficha}')
    contexto.update(
        {
            'ficha': ficha,
            'programaciones': programaciones,
            'meses_rango': meses_rango,
            'modo_pruebas_programacion': modo_pruebas,
            'total_horas_programa': ficha.id_programa_formacion.horas_max,
            'total_horas_lectiva': ficha.id_programa_formacion.horas_lectiva,
            'total_horas_completadas': round(total_horas_completadas, 2),
        }
    )
    return render(request, 'portal/dinamizador/ficha_programacion.html', contexto)


@role_required('dinamizador')
@require_http_methods(['POST'])
def dinamizador_eliminar_programacion(request, usuario, codigo_ficha, id_programacion):
    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)
    programacion = _obtener_programacion_de_ficha(ficha, id_programacion)

    anio_prog, mes_prog = _anio_mes_programacion(programacion)
    politica_prog = _politica_programacion_mes(
        anio_prog,
        mes_prog,
        modo_pruebas=_modo_pruebas_programacion_activo(request),
    )
    if not politica_prog['permite_editar']:
        messages.error(request, politica_prog['mensaje_edicion'])
        return redirect('dinamizador_ficha_programacion', codigo_ficha=ficha.codigo_ficha)

    detalle = detalle_programacion_para_edicion(programacion)
    fechas_detalle = list(detalle.get('fechas') or [])

    with transaction.atomic():
        dias_qs = ProgramacionDia.objects.filter(
            codigo_ficha_id=ficha.codigo_ficha,
            id_competencia_id=programacion.id_competencia_id,
            id_instructor_id=programacion.id_instructor_id,
            estado__in=['programada', 'ajustada', 'ejecutada'],
        )
        if fechas_detalle:
            dias_qs = dias_qs.filter(fecha__in=fechas_detalle)
        else:
            dias_qs = dias_qs.filter(fecha__range=(programacion.fecha_inicio, programacion.fecha_fin))

        ProgramacionDiaResultado.objects.filter(id_programacion_dia__in=dias_qs).delete()
        dias_eliminados = dias_qs.count()
        dias_qs.delete()

        ProgramacionResultado.objects.filter(id_programacion_id=programacion.id_programacion).delete()
        programacion.delete()

    messages.success(
        request,
        f'Se eliminó la programación #{id_programacion}. Días eliminados: {dias_eliminados}.',
    )
    return redirect('dinamizador_ficha_programacion', codigo_ficha=ficha.codigo_ficha)


@role_required('dinamizador')
def dinamizador_ficha_programacion_mes(request, usuario, codigo_ficha, anio, mes):
    if mes < 1 or mes > 12:
        raise Http404('Mes inválido.')

    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)
    _validar_mes_en_rango_ficha(ficha, anio, mes)
    modo_pruebas = _modo_pruebas_programacion_activo(request)
    politica_mes = _politica_programacion_mes(anio, mes, modo_pruebas=modo_pruebas)

    calendario_mes = _calendario_mes_ficha(ficha, anio, mes)
    competencias = _competencias_programa_con_contador(ficha)
    resultados_catalogo = _resultados_catalogo_programa_ficha(ficha)
    equipos_permitidos_ids = ids_equipos_disponibles_para_dinamizador(usuario)
    equipos = EquipoEjecutor.objects.filter(id_equipo__in=equipos_permitidos_ids).order_by('nombre')
    ambientes_otros = Ambiente.objects.filter(
        codigo_municipio_id=ficha.codigo_municipio_id,
    ).exclude(id_ambiente=ficha.id_ambiente_id).order_by('ambiente')
    horas_por_dia = horas_por_dia_desde_horario(ficha.id_horario)
    hora_inicio_base, hora_fin_base = franja_horaria_desde_horario(ficha.id_horario)

    meses = _meses_en_rango(ficha.fecha_inicio, ficha.fecha_fin)
    prev_mes = None
    next_mes = None
    for idx, item in enumerate(meses):
        if item['anio'] == anio and item['mes'] == mes:
            if idx > 0:
                prev_mes = {'anio': meses[idx - 1]['anio'], 'mes': meses[idx - 1]['mes']}
            if idx < len(meses) - 1:
                next_mes = {'anio': meses[idx + 1]['anio'], 'mes': meses[idx + 1]['mes']}
            break

    contexto = _contexto_base(request, usuario, f'Programacion mensual ficha {ficha.codigo_ficha}')
    contexto.update(
        {
            'ficha': ficha,
            'anio': anio,
            'mes': mes,
            'nombre_mes': MESES_ES[mes],
            'calendario_mes': calendario_mes,
            'competencias': competencias,
            'resultados_catalogo': resultados_catalogo,
            'equipos': equipos,
            'ambientes_otros': ambientes_otros,
            'horas_por_dia': horas_por_dia,
            'hora_inicio_base': hora_inicio_base.strftime('%H:%M'),
            'hora_fin_base': hora_fin_base.strftime('%H:%M'),
            'prev_mes': prev_mes,
            'next_mes': next_mes,
            'politica_mes': politica_mes,
            'modo_pruebas_programacion': modo_pruebas,
        }
    )
    return render(request, 'portal/dinamizador/ficha_programacion_mes.html', contexto)


@role_required('dinamizador')
@require_http_methods(['GET'])
def api_ficha_programacion_mes_datos(request, usuario, codigo_ficha, anio, mes):
    if mes < 1 or mes > 12:
        return HttpResponseBadRequest('Mes inválido.')

    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)
    _validar_mes_en_rango_ficha(ficha, anio, mes)
    modo_pruebas = _modo_pruebas_programacion_activo(request)
    politica_mes = _politica_programacion_mes(anio, mes, modo_pruebas=modo_pruebas)

    competencia_id = request.GET.get('competencia_id')
    instructor_id = request.GET.get('instructor_id')
    equipo_filtro = request.GET.get('equipo_filtro_id')
    ambiente_id = request.GET.get('ambiente_id')

    ambiente_valor = ficha.id_ambiente_id
    if ambiente_id:
        try:
            ambiente_valor = int(ambiente_id)
        except ValueError:
            return HttpResponseBadRequest('Ambiente inválido.')
        if not Ambiente.objects.filter(
            id_ambiente=ambiente_valor,
            codigo_municipio_id=ficha.codigo_municipio_id,
        ).exists():
            return HttpResponseBadRequest('El ambiente no pertenece al municipio de formacion de la ficha.')

    competencias = _competencias_programa_con_contador(ficha)
    resultados_catalogo = _resultados_catalogo_programa_ficha(ficha)
    equipos_permitidos_ids = ids_equipos_disponibles_para_dinamizador(usuario)
    competencia = None
    instructores_data = []
    resultados_data = []
    fechas_resultados_data = []

    if competencia_id:
        try:
            competencia = Competencia.objects.get(
                id_competencia=int(competencia_id),
                id_programa_formacion_id=ficha.id_programa_formacion_id,
            )
        except (ValueError, Competencia.DoesNotExist):
            return HttpResponseBadRequest('Competencia inválida para la ficha.')

        equipo_filtro_id = None
        if equipo_filtro:
            try:
                equipo_filtro_id = int(equipo_filtro)
            except ValueError:
                return HttpResponseBadRequest('Filtro de equipo inválido.')
            if equipo_filtro_id not in equipos_permitidos_ids:
                return HttpResponseBadRequest('El equipo no pertenece al ecosistema disponible para este dinamizador.')

        instructores = instructores_elegibles(
            ficha,
            usuario,
            competencia,
            equipo_filtro_id=equipo_filtro_id,
        )
        instructores_data = [
            {
                'id': item.id_usuario,
                'nombre': f"{item.nombre} {item.apellido}",
                'documento': item.documento,
                'equipo': item.id_equipo.nombre if item.id_equipo else '',
            }
            for item in instructores
        ]
        resumen_resultados = _resumen_resultados_competencia_ficha(ficha, competencia)
        resultados_data = resumen_resultados['resultados']
        fechas_resultados_data = [item.isoformat() for item in _fechas_programadas_competencia_ficha(ficha, competencia)]
    else:
        resumen_resultados = {
            'objetivo_horas': 0.0,
            'recomendado_horas': 0.0,
            'porcentaje_objetivo': 0.0,
        }

    resumen = None
    instructor = None
    if instructor_id:
        try:
            instructor = Usuario.objects.select_related('id_rol', 'id_equipo').get(id_usuario=int(instructor_id), activo=True)
        except (ValueError, Usuario.DoesNotExist):
            return HttpResponseBadRequest('Instructor inválido.')
        resumen = _resumen_instructor(instructor, anio, mes)

    fechas_ajuste_noche_auto = _fechas_ajuste_noche_auto(ficha, usuario, instructor, anio, mes)

    calendario_mes = _calendario_mes_ficha(
        ficha,
        anio,
        mes,
        instructor_id=int(instructor_id) if instructor_id and instructor_id.isdigit() else None,
        ambiente_id=ambiente_valor,
    )

    return JsonResponse(
        {
            'ficha': {
                'codigo': ficha.codigo_ficha,
                'programa': ficha.id_programa_formacion.nombre,
                'horario': ficha.id_horario.horario if ficha.id_horario else '',
            },
            'mes': {'anio': anio, 'mes': mes, 'nombre': MESES_ES[mes]},
            'calendario': calendario_mes,
            'competencias': competencias,
            'resultados_catalogo': resultados_catalogo,
            'instructores': instructores_data,
            'resultados_competencia': resultados_data,
            'fechas_resultados_competencia': fechas_resultados_data,
            'objetivo_competencia_horas': resumen_resultados['objetivo_horas'],
            'recomendado_competencia_horas': resumen_resultados['recomendado_horas'],
            'porcentaje_objetivo_competencia': resumen_resultados['porcentaje_objetivo'],
            'resumen_instructor': resumen,
            'fechas_ajuste_noche_auto': fechas_ajuste_noche_auto,
            'politica_mes': {
                'permite_crear': politica_mes['permite_crear'],
                'permite_editar': politica_mes['permite_editar'],
                'es_mes_actual': politica_mes['es_mes_actual'],
                'es_mes_pasado': politica_mes['es_mes_pasado'],
                'es_mes_futuro': politica_mes['es_mes_futuro'],
                'ventana_abierta_futuros': politica_mes['ventana_abierta_futuros'],
                'fecha_apertura_futuros': politica_mes['fecha_apertura_futuros'].isoformat(),
                'mensaje_creacion': politica_mes['mensaje_creacion'],
                'mensaje_edicion': politica_mes['mensaje_edicion'],
                'modo_pruebas': modo_pruebas,
            },
        }
    )


@role_required('dinamizador')
@require_http_methods(['POST'])
def api_ficha_programacion_mes_guardar(request, usuario, codigo_ficha, anio, mes):
    if mes < 1 or mes > 12:
        return HttpResponseBadRequest('Mes inválido.')

    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)
    _validar_mes_en_rango_ficha(ficha, anio, mes)
    politica_mes = _politica_programacion_mes(anio, mes, modo_pruebas=_modo_pruebas_programacion_activo(request))
    if not politica_mes['permite_crear']:
        return HttpResponseBadRequest(politica_mes['mensaje_creacion'])

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('JSON inválido.')

    competencia_id = payload.get('competencia_id')
    instructor_id = payload.get('instructor_id')
    ambiente_id = payload.get('ambiente_id')
    fechas_raw = payload.get('fechas') or []
    asignaciones_resultados_raw = payload.get('asignaciones_resultados') or []
    objetivo_competencia_raw = payload.get('objetivo_competencia_horas')
    horas_resultados_raw = payload.get('horas_resultados') or []
    equipo_filtro = payload.get('equipo_filtro_id')
    horario_especial_raw = payload.get('horario_especial')

    if not competencia_id or not instructor_id:
        return HttpResponseBadRequest('Competencia e instructor son obligatorios.')

    ambiente_valor = ficha.id_ambiente_id
    if ambiente_id not in (None, '', 0, '0'):
        try:
            ambiente_valor = int(ambiente_id)
        except ValueError:
            return HttpResponseBadRequest('Ambiente inválido.')

    try:
        ambiente = Ambiente.objects.get(
            id_ambiente=ambiente_valor,
            codigo_municipio_id=ficha.codigo_municipio_id,
        )
    except Ambiente.DoesNotExist:
        return HttpResponseBadRequest('El ambiente seleccionado no existe o no pertenece al municipio de la ficha.')

    try:
        competencia = Competencia.objects.get(
            id_competencia=int(competencia_id),
            id_programa_formacion_id=ficha.id_programa_formacion_id,
        )
    except (ValueError, Competencia.DoesNotExist):
        return HttpResponseBadRequest('Competencia inválida para la ficha.')

    equipo_filtro_id = None
    equipos_permitidos_ids = ids_equipos_disponibles_para_dinamizador(usuario)
    if equipo_filtro not in (None, '', 0, '0'):
        try:
            equipo_filtro_id = int(equipo_filtro)
        except ValueError:
            return HttpResponseBadRequest('Filtro de equipo inválido.')
        if equipo_filtro_id not in equipos_permitidos_ids:
            return HttpResponseBadRequest('El equipo no pertenece al ecosistema disponible para este dinamizador.')

    elegibles = instructores_elegibles(
        ficha,
        usuario,
        competencia,
        equipo_filtro_id=equipo_filtro_id,
    )
    try:
        instructor = elegibles.get(id_usuario=int(instructor_id))
    except (ValueError, Usuario.DoesNotExist):
        return HttpResponseBadRequest('Instructor no elegible para la competencia seleccionada.')

    fechas = []
    for item in fechas_raw:
        try:
            fecha = date.fromisoformat(str(item))
        except ValueError:
            return HttpResponseBadRequest('Formato de fecha inválido en la selección de días.')
        if fecha.year != anio or fecha.month != mes:
            return HttpResponseBadRequest('Todas las fechas deben pertenecer al mes seleccionado.')
        fechas.append(fecha)

    asignaciones_resultados = []
    fechas_permitidas_resultados = set(fechas)

    for item in asignaciones_resultados_raw:
        try:
            resultado_id = int(item.get('resultado_id'))
            fecha_inicio = date.fromisoformat(str(item.get('fecha_inicio')))
            fecha_fin = date.fromisoformat(str(item.get('fecha_fin')))
        except (TypeError, ValueError):
            return HttpResponseBadRequest('Asignacion de resultados invalida.')

        if fecha_inicio < ficha.fecha_inicio or fecha_inicio > ficha.fecha_fin or fecha_fin < ficha.fecha_inicio or fecha_fin > ficha.fecha_fin:
            return HttpResponseBadRequest('El rango de resultados debe estar dentro de la duracion de la ficha.')

        if fecha_inicio not in fechas_permitidas_resultados or fecha_fin not in fechas_permitidas_resultados:
            return HttpResponseBadRequest('El rango de resultados solo puede usar los dias seleccionados en esta programación.')

        asignaciones_resultados.append(
            {
                'resultado_id': resultado_id,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
            }
        )

    if not asignaciones_resultados:
        return HttpResponseBadRequest('Debes seleccionar al menos un resultado con el check.')

    try:
        horas_competencia_cfg = _parse_horas_resultados_competencia(
            competencia,
            objetivo_competencia_raw,
            horas_resultados_raw,
        )
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    if not ficha.id_horario:
        return HttpResponseBadRequest('La ficha no tiene horario asociado.')

    try:
        horario_especial = _parse_horario_especial_payload(horario_especial_raw, ficha.id_horario)
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    try:
        resultado = guardar_programacion_dias(
            ficha=ficha,
            dinamizador=usuario,
            instructor=instructor,
            ambiente=ambiente,
            competencia=competencia,
            horario=ficha.id_horario,
            fechas=fechas,
            asignaciones_resultados=asignaciones_resultados,
            horario_especial=horario_especial,
            horas_objetivo_total=horas_competencia_cfg['objetivo_horas'],
            horas_resultados=horas_competencia_cfg['horas_resultados_map'],
        )
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    resumen_instructor = _resumen_instructor(instructor, anio, mes)
    horas_competencia = horas_programadas_competencia_ficha(ficha.codigo_ficha, competencia.id_competencia)
    resultado_json = dict(resultado)
    cabecera = resultado_json.get('cabecera')
    if cabecera is not None:
        resultado_json['cabecera'] = getattr(cabecera, 'pk', cabecera)

    if horas_competencia_cfg['aviso']:
        avisos = list(resultado_json.get('avisos') or [])
        if horas_competencia_cfg['aviso'] not in avisos:
            avisos.append(horas_competencia_cfg['aviso'])
        resultado_json['avisos'] = avisos

    return JsonResponse(
        {
            'resultado': resultado_json,
            'resumen_instructor': resumen_instructor,
            'competencia': {
                'id': competencia.id_competencia,
                'horas_max': competencia.horas_max,
                'horas_programadas': round(horas_competencia, 2),
                'horas_restantes': round(max(0.0, float(competencia.horas_max) - horas_competencia), 2),
                'objetivo_horas': horas_competencia_cfg['objetivo_horas'],
                'recomendado_horas': horas_competencia_cfg['recomendado_horas'],
                'porcentaje_objetivo': horas_competencia_cfg['porcentaje_objetivo'],
            },
        }
    )


@role_required('dinamizador')
@require_http_methods(['GET'])
def api_ficha_programacion_detalle(request, usuario, codigo_ficha, id_programacion):
    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)
    programacion = _obtener_programacion_de_ficha(ficha, id_programacion)
    anio_prog, mes_prog = _anio_mes_programacion(programacion)
    politica_prog = _politica_programacion_mes(
        anio_prog,
        mes_prog,
        modo_pruebas=_modo_pruebas_programacion_activo(request),
    )
    if not politica_prog['permite_editar']:
        return HttpResponseBadRequest(politica_prog['mensaje_edicion'])

    detalle = detalle_programacion_para_edicion(programacion)
    horas_competencia = horas_programadas_competencia_ficha(ficha.codigo_ficha, programacion.id_competencia_id)

    return JsonResponse(
        {
            'programacion': {
                'id': detalle['id_programacion'],
                'estado': detalle['estado'],
                'competencia_id': detalle['competencia_id'],
                'competencia_nombre': programacion.id_competencia.nombre,
                'instructor_id': detalle['instructor_id'],
                'instructor_nombre': f"{programacion.id_instructor.nombre} {programacion.id_instructor.apellido}",
                'ambiente_id': detalle['ambiente_id'],
                'fecha_inicio': detalle['fecha_inicio'].isoformat(),
                'fecha_fin': detalle['fecha_fin'].isoformat(),
                'hora_inicio': detalle['hora_inicio'],
                'hora_fin': detalle['hora_fin'],
                'usa_horario_especial': detalle['usa_horario_especial'],
                'fechas': detalle['fechas'],
                'asignaciones_resultados': detalle['asignaciones_resultados'],
                'objetivo_horas': detalle.get('objetivo_horas', 0),
                'recomendado_horas': detalle.get('recomendado_horas', 0),
                'porcentaje_objetivo': detalle.get('porcentaje_objetivo', 0),
                'horas_resultados': detalle.get('horas_resultados', []),
            },
            'competencia': {
                'id': programacion.id_competencia_id,
                'horas_max': programacion.id_competencia.horas_max,
                'horas_programadas': round(horas_competencia, 2),
                'horas_restantes': round(max(0.0, float(programacion.id_competencia.horas_max) - horas_competencia), 2),
            },
        }
    )


@role_required('dinamizador')
@require_http_methods(['POST'])
def api_ficha_programacion_editar(request, usuario, codigo_ficha, anio, mes, id_programacion):
    if mes < 1 or mes > 12:
        return HttpResponseBadRequest('Mes inválido.')

    ficha = _obtener_ficha_dinamizador(usuario, codigo_ficha)
    _validar_mes_en_rango_ficha(ficha, anio, mes)
    politica_mes = _politica_programacion_mes(anio, mes, modo_pruebas=_modo_pruebas_programacion_activo(request))
    if not politica_mes['permite_editar']:
        return HttpResponseBadRequest(politica_mes['mensaje_edicion'])

    programacion = _obtener_programacion_de_ficha(ficha, id_programacion)
    anio_prog, mes_prog = _anio_mes_programacion(programacion)
    if anio_prog != anio or mes_prog != mes:
        return HttpResponseBadRequest('La programación seleccionada no corresponde al mes en edición.')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('JSON inválido.')

    fechas_raw = payload.get('fechas') or []
    ambiente_id = payload.get('ambiente_id')
    asignaciones_resultados_raw = payload.get('asignaciones_resultados') or []
    objetivo_competencia_raw = payload.get('objetivo_competencia_horas')
    horas_resultados_raw = payload.get('horas_resultados') or []
    horario_especial_raw = payload.get('horario_especial')

    ambiente_valor = programacion.id_ambiente_id or ficha.id_ambiente_id
    if ambiente_id not in (None, '', 0, '0'):
        try:
            ambiente_valor = int(ambiente_id)
        except ValueError:
            return HttpResponseBadRequest('Ambiente inválido.')

    try:
        ambiente = Ambiente.objects.get(
            id_ambiente=ambiente_valor,
            codigo_municipio_id=ficha.codigo_municipio_id,
        )
    except Ambiente.DoesNotExist:
        return HttpResponseBadRequest('El ambiente seleccionado no existe o no pertenece al municipio de la ficha.')

    fechas = []
    for item in fechas_raw:
        try:
            fecha = date.fromisoformat(str(item))
        except ValueError:
            return HttpResponseBadRequest('Formato de fecha inválido en la selección de días.')
        if fecha.year != anio or fecha.month != mes:
            return HttpResponseBadRequest('Todas las fechas deben pertenecer al mes seleccionado.')
        fechas.append(fecha)

    if not fechas:
        return HttpResponseBadRequest('Debes seleccionar al menos un día para editar la programación.')

    if not ficha.id_horario:
        return HttpResponseBadRequest('La ficha no tiene horario asociado.')

    try:
        horario_especial = _parse_horario_especial_payload(horario_especial_raw, ficha.id_horario)
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    asignaciones_resultados = []
    fechas_permitidas_resultados = set(fechas)

    for item in asignaciones_resultados_raw:
        try:
            resultado_id = int(item.get('resultado_id'))
            fecha_inicio = date.fromisoformat(str(item.get('fecha_inicio')))
            fecha_fin = date.fromisoformat(str(item.get('fecha_fin')))
        except (TypeError, ValueError):
            return HttpResponseBadRequest('Asignacion de resultados invalida.')

        if fecha_inicio < ficha.fecha_inicio or fecha_inicio > ficha.fecha_fin or fecha_fin < ficha.fecha_inicio or fecha_fin > ficha.fecha_fin:
            return HttpResponseBadRequest('El rango de resultados debe estar dentro de la duracion de la ficha.')

        if fecha_inicio not in fechas_permitidas_resultados or fecha_fin not in fechas_permitidas_resultados:
            return HttpResponseBadRequest('El rango de resultados solo puede usar los dias seleccionados en esta programación.')

        asignaciones_resultados.append(
            {
                'resultado_id': resultado_id,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
            }
        )

    if not asignaciones_resultados:
        return HttpResponseBadRequest('Debes seleccionar al menos un resultado con el check.')

    try:
        horas_competencia_cfg = _parse_horas_resultados_competencia(
            programacion.id_competencia,
            objetivo_competencia_raw,
            horas_resultados_raw,
        )
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    try:
        edicion = editar_programacion_existente(
            programacion=programacion,
            dinamizador=usuario,
            ambiente=ambiente,
            fechas=fechas,
            asignaciones_resultados=asignaciones_resultados,
            horario_especial=horario_especial,
            horas_objetivo_total=horas_competencia_cfg['objetivo_horas'],
            horas_resultados=horas_competencia_cfg['horas_resultados_map'],
        )
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    resultado_json = dict(edicion['resultado'])
    cabecera = resultado_json.get('cabecera')
    if cabecera is not None:
        resultado_json['cabecera'] = getattr(cabecera, 'pk', cabecera)

    if horas_competencia_cfg['aviso']:
        avisos = list(resultado_json.get('avisos') or [])
        if horas_competencia_cfg['aviso'] not in avisos:
            avisos.append(horas_competencia_cfg['aviso'])
        resultado_json['avisos'] = avisos

    instructor = programacion.id_instructor
    resumen_instructor = _resumen_instructor(instructor, anio, mes)
    horas_competencia = horas_programadas_competencia_ficha(ficha.codigo_ficha, programacion.id_competencia_id)

    return JsonResponse(
        {
            'edicion': {
                'programacion_anterior_id': edicion['programacion_anterior_id'],
                'programacion_nueva_id': edicion['programacion_nueva_id'],
            },
            'resultado': resultado_json,
            'resumen_instructor': resumen_instructor,
            'competencia': {
                'id': programacion.id_competencia_id,
                'horas_max': programacion.id_competencia.horas_max,
                'horas_programadas': round(horas_competencia, 2),
                'horas_restantes': round(max(0.0, float(programacion.id_competencia.horas_max) - horas_competencia), 2),
                'objetivo_horas': horas_competencia_cfg['objetivo_horas'],
                'recomendado_horas': horas_competencia_cfg['recomendado_horas'],
                'porcentaje_objetivo': horas_competencia_cfg['porcentaje_objetivo'],
            },
        }
    )
