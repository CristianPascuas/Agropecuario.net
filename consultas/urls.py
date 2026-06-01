from django.urls import path

from . import views

urlpatterns = [
    path(
        'fichas/<int:codigo_ficha>/detalle-programaciones/',
        views.ficha_programaciones_detalle,
        name='ficha_programaciones_detalle',
    ),
    path('instructor/inicio/', views.instructor_inicio, name='instructor_inicio'),
    path('instructor/programaciones/', views.instructor_programaciones, name='instructor_programaciones'),
    path('instructor/reportes/', views.instructor_reportes, name='instructor_reportes'),
    path('dinamizador/inicio/', views.dinamizador_inicio, name='dinamizador_inicio'),
    path('dinamizador/programaciones/', views.dinamizador_programaciones, name='dinamizador_programaciones'),
    path('dinamizador/reportes/', views.dinamizador_reportes, name='dinamizador_reportes'),
    path('coordinador/inicio/', views.coordinador_inicio, name='coordinador_inicio'),
    path('coordinador/programaciones/', views.coordinador_programaciones, name='coordinador_programaciones'),
    path('coordinador/equipos/', views.coordinador_equipos, name='coordinador_equipos'),
    path(
        'api/coordinador/dinamizador/<int:id_dinamizador>/tipo/',
        views.api_coordinador_cambiar_tipo_dinamizador,
        name='api_coordinador_cambiar_tipo_dinamizador',
    ),
    path(
        'api/coordinador/instructor/<int:id_instructor>/promover/',
        views.api_coordinador_promover_instructor,
        name='api_coordinador_promover_instructor',
    ),
    path('coordinador/curricular/', views.coordinador_curricular, name='coordinador_curricular'),
    path('coordinador/reportes/', views.coordinador_reportes, name='coordinador_reportes'),
    # Administrador
    path('administrador/inicio/', views.administrador_inicio, name='administrador_inicio'),
    path('administrador/usuarios/', views.administrador_usuarios, name='administrador_usuarios'),
    path('api/administrador/usuarios/<int:id_usuario>/aprobar/', views.api_administrador_aprobar_usuario, name='api_administrador_aprobar_usuario'),
    path('api/administrador/usuarios/<int:id_usuario>/bloquear/', views.api_administrador_bloquear_usuario, name='api_administrador_bloquear_usuario'),
    path('api/administrador/usuarios/<int:id_usuario>/reintegrar/', views.api_administrador_reintegrar_usuario, name='api_administrador_reintegrar_usuario'),
    path('administrador/equipos/', views.administrador_equipos, name='administrador_equipos'),
    path('administrador/equipos/coordinador/<int:id_coordinador>/', views.administrador_coordinador_equipos, name='administrador_coordinador_equipos'),
    path('administrador/curricular/', views.administrador_curricular, name='administrador_curricular'),
    path('administrador/reportes/', views.administrador_reportes, name='administrador_reportes'),
]
