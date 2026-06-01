import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.http import Http404
from django.views.decorators.http import require_http_methods

from academico.models import Radicado

from portal.core import _puede_radicar, _rol_slug, role_required

from .helpers import (
    TIPOS_ACTIVIDAD_EXTRA,
    _archivo_es_pdf,
    _detalle_carga_radicado,
    _estado_radicado,
    _fecha_traslape_radicado_instructor_por_dias,
    _fechas_traslape_programacion_instructor_mes,
    _parse_fechas_radicado_json,
    _puede_aprobar_radicado,
    _resumen_fechas_radicado,
    _validar_tope_mensual_radicados_aprobados,
)


@role_required('instructor', 'dinamizador')
@require_http_methods(['POST'])
def api_instructor_radicados_crear(request, usuario):
    if not _puede_radicar(usuario):
        return HttpResponseForbidden('No tienes permisos para radicar actividades adicionales.')

    nombre_radicado = (request.POST.get('nombre_radicado') or '').strip()
    tipo_radicado_raw = (request.POST.get('tipo_radicado') or '').strip()
    descripcion_radicado = (request.POST.get('descripcion_radicado') or '').strip()
    empresa_organizacion = (request.POST.get('empresa_organizacion') or '').strip()
    nit = (request.POST.get('nit') or '').strip()
    lugar = (request.POST.get('lugar') or '').strip()
    dias_seleccionados_raw = (request.POST.get('dias_seleccionados') or '').strip()
    hora_inicio_raw = (request.POST.get('hora_inicio') or '').strip()
    hora_fin_raw = (request.POST.get('hora_fin') or '').strip()
    archivo_excel = request.FILES.get('archivo_adjunto') or request.FILES.get('archivo_excel')

    if not nombre_radicado:
        return HttpResponseBadRequest('El nombre de la actividad adicional es obligatorio.')

    try:
        tipo_radicado = int(tipo_radicado_raw)
    except ValueError:
        return HttpResponseBadRequest('Tipo de actividad adicional invalido.')

    if tipo_radicado not in set(TIPOS_ACTIVIDAD_EXTRA.keys()):
        return HttpResponseBadRequest('Tipo de actividad adicional invalido.')

    if not descripcion_radicado:
        return HttpResponseBadRequest('La descripcion de la actividad adicional es obligatoria.')

    if not empresa_organizacion:
        return HttpResponseBadRequest('El campo EMPRESA/ ORGANIZACION es obligatorio.')

    if not nit:
        return HttpResponseBadRequest('El NIT es obligatorio.')

    if not lugar:
        return HttpResponseBadRequest('El lugar es obligatorio.')

    fechas_radicado = _parse_fechas_radicado_json(dias_seleccionados_raw)
    if not fechas_radicado:
        return HttpResponseBadRequest('Debes seleccionar al menos un dia en el calendario.')

    try:
        hora_inicio = datetime.strptime(hora_inicio_raw, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_raw, '%H:%M').time()
    except ValueError:
        return HttpResponseBadRequest('Horas invalidas para la actividad adicional.')

    if hora_fin <= hora_inicio:
        return HttpResponseBadRequest('La hora fin debe ser mayor que la hora inicio.')

    try:
        _validar_tope_mensual_radicados_aprobados(
            usuario,
            fechas_radicado,
            hora_inicio,
            hora_fin,
        )
    except ValidationError as exc:
        return HttpResponseBadRequest(exc.message)

    fecha_traslape = _fecha_traslape_radicado_instructor_por_dias(
        instructor=usuario,
        fechas=fechas_radicado,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
    )

    if fecha_traslape:
        return HttpResponseBadRequest(
            f'La actividad adicional presenta traslape con una programacion asignada al instructor en la fecha {fecha_traslape.isoformat()}.',
        )

    if not archivo_excel:
        return HttpResponseBadRequest('Debes adjuntar un archivo PDF.')

    if not _archivo_es_pdf(archivo_excel):
        return HttpResponseBadRequest('Solo se permite adjuntar archivos PDF (.pdf).')

    radicado = Radicado.objects.create(
        nombre_radicado=nombre_radicado,
        tipo_radicado=tipo_radicado,
        descripcion_radicado=descripcion_radicado,
        empresa_organizacion=empresa_organizacion,
        nit=nit,
        lugar=lugar,
        dias_seleccionados=json.dumps([f.isoformat() for f in fechas_radicado]),
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        archivo_excel=archivo_excel,
        id_instructor=usuario,
        aprobado=0,
    )

    estado_valor, estado_texto = _estado_radicado(radicado.aprobado)
    tipo_texto = TIPOS_ACTIVIDAD_EXTRA.get(int(radicado.tipo_radicado or 0), 'Otros')
    detalle = _detalle_carga_radicado(radicado)
    responsable = f"{usuario.nombre} {usuario.apellido}".strip()
    search_text = ' '.join(
        [
            radicado.nombre_radicado or '',
            tipo_texto,
            radicado.descripcion_radicado or '',
            radicado.empresa_organizacion or '',
            radicado.nit or '',
            radicado.lugar or '',
            responsable,
            detalle['fecha_inicio'],
            detalle['fecha_fin'],
        ]
    ).lower()

    return JsonResponse(
        {
            'ok': True,
            'radicado': {
                'id': radicado.id_radicado,
                'nombre': radicado.nombre_radicado,
                'tipo': int(radicado.tipo_radicado or 0),
                'tipo_texto': tipo_texto,
                'descripcion': radicado.descripcion_radicado,
                'empresa_organizacion': radicado.empresa_organizacion,
                'nit': radicado.nit,
                'lugar': radicado.lugar,
                'fecha': _resumen_fechas_radicado(radicado),
                'fecha_inicio': detalle['fecha_inicio'],
                'fecha_fin': detalle['fecha_fin'],
                'dias_total': detalle['dias_total'],
                'horas_diarias': detalle['horas_diarias'],
                'horas_totales': detalle['horas_totales'],
                'archivo_url': radicado.archivo_excel.url if radicado.archivo_excel else '',
                'responsable': responsable,
                'aprobado': estado_valor,
                'estado_texto': estado_texto,
                'search_text': search_text,
            },
        }
    )


@role_required('instructor', 'dinamizador')
@require_http_methods(['GET'])
def api_instructor_radicados_traslapes_mes(request, usuario, anio, mes):
    if mes < 1 or mes > 12:
        return HttpResponseBadRequest('Mes inválido.')

    hora_inicio_raw = (request.GET.get('hora_inicio') or '').strip()
    hora_fin_raw = (request.GET.get('hora_fin') or '').strip()

    if not hora_inicio_raw or not hora_fin_raw:
        return JsonResponse({'fechas_bloqueadas': []})

    try:
        hora_inicio = datetime.strptime(hora_inicio_raw, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_raw, '%H:%M').time()
    except ValueError:
        return HttpResponseBadRequest('Horas inválidas para calcular traslapes.')

    if hora_fin <= hora_inicio:
        return HttpResponseBadRequest('La hora fin debe ser mayor que la hora inicio.')

    fechas = _fechas_traslape_programacion_instructor_mes(usuario, anio, mes, hora_inicio, hora_fin)
    return JsonResponse({'fechas_bloqueadas': [f.isoformat() for f in fechas]})


@role_required('dinamizador', 'coordinador')
@require_http_methods(['POST'])
def api_radicados_cambiar_estado(request, usuario, id_radicado):
    accion = (request.POST.get('accion') or '').strip().lower()
    if accion == 'aprobar':
        nuevo_estado = 1
    elif accion == 'rechazar':
        nuevo_estado = 2
    elif accion == 'revisar':
        nuevo_estado = 3
    else:
        return HttpResponseBadRequest('Accion invalida para la actividad adicional.')

    try:
        radicado = Radicado.objects.get(id_radicado=id_radicado)
    except Radicado.DoesNotExist as exc:
        raise Http404('No se encontro la actividad adicional solicitada.') from exc

    if not _puede_aprobar_radicado(usuario, radicado):
        return HttpResponseForbidden('No tienes permisos para gestionar esta actividad adicional.')

    if int(radicado.aprobado or 0) in (1, 2):
        return HttpResponseBadRequest('La actividad adicional ya fue gestionada y no puede cambiar de estado.')

    if nuevo_estado == 1:
        fechas_radicado = _parse_fechas_radicado_json(radicado.dias_seleccionados)
        try:
            _validar_tope_mensual_radicados_aprobados(
                radicado.id_instructor,
                fechas_radicado,
                radicado.hora_inicio,
                radicado.hora_fin,
                excluir_radicado_id=radicado.id_radicado,
            )
        except ValidationError as exc:
            return HttpResponseBadRequest(exc.message)

    radicado.aprobado = nuevo_estado
    radicado.save(update_fields=['aprobado'])

    estado_valor, estado_texto = _estado_radicado(radicado.aprobado)
    return JsonResponse(
        {
            'ok': True,
            'id': radicado.id_radicado,
            'estado': estado_valor,
            'estado_texto': estado_texto,
        }
    )
