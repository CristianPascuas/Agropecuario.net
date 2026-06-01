from functools import wraps
from datetime import date, timedelta

from django.shortcuts import redirect

from academico.models import Usuario

SESSION_USER_ID_KEY = 'usuario_id'

MESES_ES = [
    '',
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre',
]


def _rango_mes(anio: int, mes: int):
    inicio = date(anio, mes, 1)
    if mes == 12:
        fin = date(anio, 12, 31)
    else:
        fin = date(anio, mes + 1, 1) - timedelta(days=1)
    return inicio, fin


def _obtener_usuario_sesion(request):
    user_id = request.session.get(SESSION_USER_ID_KEY)
    if not user_id:
        return None
    try:
        return Usuario.objects.select_related('id_rol').get(id_usuario=user_id, activo=True)
    except Usuario.DoesNotExist:
        return None


def _rol_slug(usuario):
    nombre = (usuario.id_rol.nombre or '').lower()
    if 'administrador' in nombre:
        return 'administrador'
    if 'instr' in nombre:
        return 'instructor'
    if 'dinamizador' in nombre:
        return 'dinamizador'
    if 'coordinador' in nombre or 'curricular' in nombre:
        return 'coordinador'
    return 'instructor'


def _es_dinamizador_instructor(usuario):
    return _rol_slug(usuario) == 'dinamizador' and getattr(usuario, 'tipo_dinamizador', None) == 'instructor'


def _es_dinamizador_coordinador(usuario):
    return _rol_slug(usuario) == 'dinamizador' and getattr(usuario, 'tipo_dinamizador', None) == 'coordinador'


def _puede_radicar(usuario):
    rol = _rol_slug(usuario)
    if rol == 'instructor':
        return True
    if rol == 'dinamizador':
        return _es_dinamizador_instructor(usuario)
    return False


def _puede_autoasignarse_instructor(usuario):
    return _es_dinamizador_instructor(usuario)


def _es_instructor_contrato(usuario):
    return _rol_slug(usuario) == 'instructor' and int(getattr(usuario, 'tipo_contrato', 0) or 0) == 0


def _menu_por_rol(rol_slug):
    menus = {
        'instructor': [
            {'label': 'Inicio', 'url_name': 'instructor_inicio'},
            {'label': 'Consultar programaciones', 'url_name': 'instructor_programaciones'},
            {'label': 'Reportes', 'url_name': 'instructor_reportes'},
        ],
        'dinamizador': [
            {'label': 'Inicio', 'url_name': 'dinamizador_inicio'},
            {'label': 'Consultar programaciones', 'url_name': 'dinamizador_programaciones'},
            {'label': 'Programar fichas', 'url_name': 'dinamizador_programar_fichas'},
            {'label': 'Reportes', 'url_name': 'dinamizador_reportes'},
        ],
        'coordinador': [
            {'label': 'Inicio', 'url_name': 'coordinador_inicio'},
            {'label': 'Consultar programaciones', 'url_name': 'coordinador_programaciones'},
            {'label': 'Equipos de ejecucion', 'url_name': 'coordinador_equipos'},
            {'label': 'Reportes', 'url_name': 'coordinador_reportes'},
        ],
        'administrador': [
            {'label': 'Inicio', 'url_name': 'administrador_inicio'},
            {'label': 'Usuarios', 'url_name': 'administrador_usuarios'},
            {'label': 'Equipos', 'url_name': 'administrador_equipos'},
            {'label': 'Curricular', 'url_name': 'administrador_curricular'},
            {'label': 'Reportes', 'url_name': 'administrador_reportes'},
        ],
    }
    return menus.get(rol_slug, menus['instructor'])


def _contexto_base(request, usuario, titulo):
    rol = _rol_slug(usuario)
    return {
        'usuario': usuario,
        'titulo': titulo,
        'rol_slug': rol,
        'menu_items': _menu_por_rol(rol),
        'ruta_actual': request.resolver_match.url_name if request.resolver_match else '',
    }


def role_required(*roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            usuario = _obtener_usuario_sesion(request)
            if not usuario:
                return redirect('login')
            if _rol_slug(usuario) not in roles_permitidos:
                return redirect('portal_home')
            return view_func(request, usuario, *args, **kwargs)

        return wrapper

    return decorator
