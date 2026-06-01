from django.shortcuts import redirect

from .core import _obtener_usuario_sesion, _rol_slug


def portal_home(request):
    usuario = _obtener_usuario_sesion(request)
    if not usuario:
        return redirect('login')

    rol = _rol_slug(usuario)
    if rol == 'administrador':
        return redirect('administrador_inicio')
    if rol == 'dinamizador':
        return redirect('dinamizador_inicio')
    if rol == 'coordinador':
        return redirect('coordinador_inicio')
    return redirect('instructor_inicio')

