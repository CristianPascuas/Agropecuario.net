from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from academico.models import CoordinadorEquipo, EquipoEjecutor, Rol, Usuario

from portal.core import _contexto_base, _es_instructor_contrato, role_required

from radicados.helpers import _contexto_radicados

from .helpers import (
    _contexto_consulta_programaciones_usuario,
    _contexto_detalle_programaciones_ficha,
    _obtener_ficha_para_consulta,
    _resumen_inicio_usuario,
)


@role_required('instructor')
def instructor_inicio(request, usuario):
    contexto = _contexto_base(request, usuario, 'Inicio Instructor')
    contexto.update(
        {
            'resumen_inicio': _resumen_inicio_usuario(usuario),
            'es_instructor_contrato': _es_instructor_contrato(usuario),
        }
    )
    contexto.update(_contexto_radicados(usuario))
    return render(request, 'portal/instructor/inicio.html', contexto)


@role_required('instructor')
def instructor_programaciones(request, usuario):
    contexto = _contexto_base(request, usuario, 'Consultar programaciones')
    contexto.update(_contexto_consulta_programaciones_usuario(request, usuario))
    return render(request, 'portal/instructor/programaciones.html', contexto)


@role_required('instructor')
def instructor_reportes(request, usuario):
    return render(request, 'portal/instructor/reportes.html', _contexto_base(request, usuario, 'Reportes'))


@role_required('instructor', 'dinamizador')
def ficha_programaciones_detalle(request, usuario, codigo_ficha):
    ficha = _obtener_ficha_para_consulta(usuario, codigo_ficha)
    contexto = _contexto_detalle_programaciones_ficha(request, usuario, ficha)
    return render(request, 'portal/ficha_programaciones_detalle.html', contexto)


@role_required('dinamizador')
def dinamizador_inicio(request, usuario):
    contexto = _contexto_base(request, usuario, 'Inicio Dinamizador')
    contexto.update({'resumen_inicio': _resumen_inicio_usuario(usuario)})
    contexto.update(_contexto_radicados(usuario))
    return render(request, 'portal/dinamizador/inicio.html', contexto)


@role_required('dinamizador')
def dinamizador_programaciones(request, usuario):
    contexto = _contexto_base(request, usuario, 'Consultar programaciones')
    contexto.update(_contexto_consulta_programaciones_usuario(request, usuario))
    return render(request, 'portal/dinamizador/programaciones.html', contexto)


@role_required('dinamizador')
def dinamizador_reportes(request, usuario):
    return render(request, 'portal/dinamizador/reportes.html', _contexto_base(request, usuario, 'Reportes'))


@role_required('coordinador')
def coordinador_inicio(request, usuario):
    contexto = _contexto_base(request, usuario, 'Inicio Coordinador')
    contexto.update(_contexto_radicados(usuario))
    return render(request, 'portal/coordinador/inicio.html', contexto)


@role_required('coordinador')
def coordinador_programaciones(request, usuario):
    return render(
        request,
        'portal/coordinador/programaciones.html',
        _contexto_base(request, usuario, 'Consultar programaciones'),
    )


@role_required('coordinador')
def coordinador_equipos(request, usuario):
    equipo_coord = usuario.id_equipo_id

    dinamizadores = Usuario.objects.filter(
        activo=True,
        id_rol__nombre__icontains='dinamizador',
        id_equipo_id=equipo_coord,
    ).select_related('id_rol', 'id_equipo').order_by('nombre', 'apellido')

    lista_din = []
    for din in dinamizadores:
        lista_din.append({
            'id': din.id_usuario,
            'nombre': f"{din.nombre} {din.apellido}",
            'documento': din.documento,
            'equipo': din.id_equipo.nombre if din.id_equipo else 'Sin equipo',
            'tipo_dinamizador': din.tipo_dinamizador or 'instructor',
            'tipo_display': 'Coordinador' if din.tipo_dinamizador == 'coordinador' else 'Instructor',
        })

    instructores = Usuario.objects.filter(
        activo=True,
        id_rol__nombre__icontains='instr',
        id_equipo_id=equipo_coord,
    ).select_related('id_rol', 'id_equipo').order_by('nombre', 'apellido')

    # Excluir dinamizadores del listado de instructores
    lista_inst = []
    for inst in instructores:
        if 'dinamizador' in (inst.id_rol.nombre or '').lower():
            continue
        lista_inst.append({
            'id': inst.id_usuario,
            'nombre': f"{inst.nombre} {inst.apellido}",
            'documento': inst.documento,
            'equipo': inst.id_equipo.nombre if inst.id_equipo else 'Sin equipo',
        })

    contexto = _contexto_base(request, usuario, 'Equipos de ejecución')
    contexto['dinamizadores'] = lista_din
    contexto['instructores'] = lista_inst
    return render(request, 'portal/coordinador/equipos.html', contexto)


@role_required('coordinador')
@require_http_methods(['POST'])
def api_coordinador_cambiar_tipo_dinamizador(request, usuario, id_dinamizador):
    nuevo_tipo = (request.POST.get('tipo_dinamizador') or '').strip()
    if nuevo_tipo not in ('instructor', 'coordinador'):
        return HttpResponseBadRequest('Tipo inválido.')

    try:
        dinamizador = Usuario.objects.select_related('id_rol').get(
            id_usuario=id_dinamizador,
            activo=True,
            id_rol__nombre__icontains='dinamizador',
        )
    except Usuario.DoesNotExist:
        return HttpResponseBadRequest('Dinamizador no encontrado.')

    dinamizador.tipo_dinamizador = nuevo_tipo
    dinamizador.save(update_fields=['tipo_dinamizador'])

    return JsonResponse({
        'ok': True,
        'id': dinamizador.id_usuario,
        'tipo_dinamizador': nuevo_tipo,
        'tipo_display': 'Coordinador' if nuevo_tipo == 'coordinador' else 'Instructor',
    })


@role_required('coordinador')
def coordinador_curricular(request, usuario):
    return render(request, 'portal/coordinador/curricular.html', _contexto_base(request, usuario, 'Curricular'))


@role_required('coordinador')
@require_http_methods(['POST'])
def api_coordinador_promover_instructor(request, usuario, id_instructor):
    """Promover instructor a dinamizador-instructor. Solo instructores del mismo equipo."""
    equipo_coord = usuario.id_equipo_id
    try:
        instructor = Usuario.objects.select_related('id_rol').get(
            id_usuario=id_instructor,
            activo=True,
            id_equipo_id=equipo_coord,
        )
    except Usuario.DoesNotExist:
        return HttpResponseBadRequest('Instructor no encontrado en su equipo.')

    if 'instr' not in (instructor.id_rol.nombre or '').lower():
        return HttpResponseBadRequest('El usuario no es instructor.')
    if 'dinamizador' in (instructor.id_rol.nombre or '').lower():
        return HttpResponseBadRequest('El usuario ya es dinamizador.')

    try:
        rol_dinamizador = Rol.objects.get(nombre__icontains='dinamizador')
    except Rol.DoesNotExist:
        return HttpResponseBadRequest('Rol dinamizador no configurado en el sistema.')

    instructor.id_rol = rol_dinamizador
    instructor.tipo_dinamizador = 'instructor'
    instructor.save(update_fields=['id_rol', 'tipo_dinamizador'])

    return JsonResponse({
        'ok': True,
        'id': instructor.id_usuario,
        'nombre': f"{instructor.nombre} {instructor.apellido}",
    })


@role_required('coordinador')
def coordinador_reportes(request, usuario):
    return render(request, 'portal/coordinador/reportes.html', _contexto_base(request, usuario, 'Reportes'))


# ── Administrador ────────────────────────────────────────────────

@role_required('administrador')
def administrador_inicio(request, usuario):
    pendientes = Usuario.objects.filter(activo=False, sin_acceso=False).count()
    contexto = _contexto_base(request, usuario, 'Inicio Administrador')
    contexto['pendientes_count'] = pendientes
    return render(request, 'portal/administrador/inicio.html', contexto)


@role_required('administrador')
def administrador_usuarios(request, usuario):
    pendientes = Usuario.objects.filter(activo=False, sin_acceso=False).select_related('id_rol', 'id_equipo').order_by('-creado_en')
    activos = Usuario.objects.filter(activo=True).select_related('id_rol', 'id_equipo').order_by('nombre', 'apellido')
    sin_acceso = Usuario.objects.filter(activo=False, sin_acceso=True).select_related('id_rol', 'id_equipo').order_by('nombre', 'apellido')

    def _usuario_dict(u):
        rol_nombre = (u.id_rol.nombre or '').lower() if u.id_rol else ''
        es_admin = 'administrador' in rol_nombre
        return {
            'id': u.id_usuario,
            'nombre': f"{u.nombre} {u.apellido}",
            'documento': u.documento,
            'email': u.email,
            'rol': u.id_rol.nombre if u.id_rol else '',
            'equipo': u.id_equipo.nombre if u.id_equipo else 'Sin equipo',
            'equipo_id': str(u.id_equipo_id) if u.id_equipo_id else 'sin-equipo',
            'activo': u.activo,
            'sin_acceso': getattr(u, 'sin_acceso', False),
            'puede_bloquear': not es_admin,
            'puede_reintegrar': not es_admin,
        }

    contexto = _contexto_base(request, usuario, 'Usuarios')
    contexto['pendientes'] = [_usuario_dict(u) for u in pendientes]
    contexto['activos'] = [_usuario_dict(u) for u in activos]
    contexto['sin_acceso'] = [_usuario_dict(u) for u in sin_acceso]
    contexto['pendientes_count'] = pendientes.count()
    contexto['activos_count'] = activos.count()
    contexto['sin_acceso_count'] = sin_acceso.count()
    contexto['equipos_filtro'] = list(EquipoEjecutor.objects.order_by('nombre').values('id_equipo', 'nombre'))
    return render(request, 'portal/administrador/usuarios.html', contexto)


@role_required('administrador')
@require_http_methods(['POST'])
def api_administrador_aprobar_usuario(request, usuario, id_usuario):
    try:
        pendiente = Usuario.objects.get(id_usuario=id_usuario, activo=False, sin_acceso=False)
    except Usuario.DoesNotExist:
        return HttpResponseBadRequest('Usuario no encontrado o ya activo.')

    pendiente.activo = True
    pendiente.sin_acceso = False
    pendiente.save(update_fields=['activo', 'sin_acceso'])
    return JsonResponse({
        'ok': True,
        'id': pendiente.id_usuario,
        'nombre': f"{pendiente.nombre} {pendiente.apellido}",
    })


@role_required('administrador')
@require_http_methods(['POST'])
def api_administrador_bloquear_usuario(request, usuario, id_usuario):
    try:
        objetivo = Usuario.objects.select_related('id_rol').get(id_usuario=id_usuario, activo=True)
    except Usuario.DoesNotExist:
        return HttpResponseBadRequest('Usuario no encontrado o ya sin acceso.')

    rol_nombre = (objetivo.id_rol.nombre or '').lower()
    if 'administrador' in rol_nombre:
        return HttpResponseBadRequest('No se puede bloquear un administrador desde esta pantalla.')

    objetivo.activo = False
    objetivo.sin_acceso = True
    objetivo.save(update_fields=['activo', 'sin_acceso'])

    return JsonResponse({
        'ok': True,
        'id': objetivo.id_usuario,
        'nombre': f"{objetivo.nombre} {objetivo.apellido}",
    })


@role_required('administrador')
@require_http_methods(['POST'])
def api_administrador_reintegrar_usuario(request, usuario, id_usuario):
    try:
        objetivo = Usuario.objects.select_related('id_rol').get(id_usuario=id_usuario, activo=False, sin_acceso=True)
    except Usuario.DoesNotExist:
        return HttpResponseBadRequest('Usuario no encontrado en sin acceso.')

    objetivo.activo = True
    objetivo.sin_acceso = False
    objetivo.save(update_fields=['activo', 'sin_acceso'])

    return JsonResponse({
        'ok': True,
        'id': objetivo.id_usuario,
        'nombre': f"{objetivo.nombre} {objetivo.apellido}",
    })


@role_required('administrador')
def administrador_equipos(request, usuario):
    coordinadores_qs = Usuario.objects.filter(
        activo=True,
    ).filter(
        Q(id_rol__nombre__icontains='coordinador')
        | Q(id_rol__nombre__icontains='dinamizador', tipo_dinamizador='coordinador')
    ).select_related('id_rol', 'id_equipo').order_by('nombre', 'apellido')

    coordinadores = [
        {
            'id': item.id_usuario,
            'nombre': f"{item.nombre} {item.apellido}",
            'documento': item.documento,
            'rol': item.id_rol.nombre if item.id_rol else 'Coordinador',
        }
        for item in coordinadores_qs
    ]

    contexto = _contexto_base(request, usuario, 'Equipos')
    contexto['coordinadores'] = coordinadores
    return render(request, 'portal/administrador/equipos.html', contexto)


@role_required('administrador')
def administrador_coordinador_equipos(request, usuario, id_coordinador):
    coordinadores_qs = Usuario.objects.filter(
        activo=True,
    ).filter(
        Q(id_rol__nombre__icontains='coordinador')
        | Q(id_rol__nombre__icontains='dinamizador', tipo_dinamizador='coordinador')
    ).select_related('id_rol', 'id_equipo')

    try:
        coordinador = coordinadores_qs.get(id_usuario=id_coordinador)
    except Usuario.DoesNotExist:
        return HttpResponseBadRequest('Coordinador no encontrado.')

    relaciones = CoordinadorEquipo.objects.filter(id_coordinador=coordinador).select_related('id_equipo')

    # Si el coordinador no tiene enlaces aún, conectarlo a su equipo actual para no dejar la vista vacía.
    if not relaciones.exists() and coordinador.id_equipo_id:
        CoordinadorEquipo.objects.get_or_create(
            id_coordinador=coordinador,
            id_equipo_id=coordinador.id_equipo_id,
        )
        relaciones = CoordinadorEquipo.objects.filter(id_coordinador=coordinador).select_related('id_equipo')

    equipos = []
    for rel in relaciones.order_by('id_equipo__nombre'):
        eq = rel.id_equipo
        total_usuarios = Usuario.objects.filter(activo=True, id_equipo=eq).count()
        equipos.append({
            'id': eq.id_equipo,
            'nombre': eq.nombre,
            'tipo': eq.get_tipo_display(),
            'total_usuarios': total_usuarios,
        })

    equipo_activo_id = None
    miembros_equipo = []
    equipo_activo = None
    equipo_param = request.GET.get('equipo')
    if str(equipo_param or '').isdigit():
        equipo_activo_id = int(equipo_param)
        ids_permitidos = {item['id'] for item in equipos}
        if equipo_activo_id in ids_permitidos:
            equipo_activo = EquipoEjecutor.objects.filter(id_equipo=equipo_activo_id).first()

    if equipo_activo:
        miembros_qs = Usuario.objects.filter(
            activo=True,
            id_equipo_id=equipo_activo.id_equipo,
        ).filter(
            Q(id_rol__nombre__icontains='instr') | Q(id_rol__nombre__icontains='dinamizador')
        ).select_related('id_rol').order_by('nombre', 'apellido')

        for item in miembros_qs:
            rol_nombre = (item.id_rol.nombre or '').lower() if item.id_rol else ''
            tipo_usuario = 'Instructor'
            if 'dinamizador' in rol_nombre:
                subtipo = 'Coordinador' if item.tipo_dinamizador == 'coordinador' else 'Instructor'
                tipo_usuario = f"Dinamizador ({subtipo})"
            miembros_equipo.append({
                'nombre': f"{item.nombre} {item.apellido}",
                'documento': item.documento,
                'tipo_usuario': tipo_usuario,
                'correo': item.email,
            })

    contexto = _contexto_base(request, usuario, 'Equipos por coordinador')
    contexto['coordinador'] = {
        'id': coordinador.id_usuario,
        'nombre': f"{coordinador.nombre} {coordinador.apellido}",
        'documento': coordinador.documento,
        'rol': coordinador.id_rol.nombre if coordinador.id_rol else 'Coordinador',
    }
    contexto['equipos'] = equipos
    contexto['equipo_activo_id'] = equipo_activo_id
    contexto['equipo_activo'] = equipo_activo
    contexto['miembros_equipo'] = miembros_equipo
    return render(request, 'portal/administrador/coordinador_equipos.html', contexto)


@role_required('administrador')
def administrador_curricular(request, usuario):
    return render(request, 'portal/administrador/curricular.html', _contexto_base(request, usuario, 'Curricular'))


@role_required('administrador')
def administrador_reportes(request, usuario):
    return render(request, 'portal/administrador/reportes.html', _contexto_base(request, usuario, 'Reportes'))
