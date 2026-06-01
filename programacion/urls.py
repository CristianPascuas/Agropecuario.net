from django.urls import path

from . import views

urlpatterns = [
    path('dinamizador/programar-fichas/', views.dinamizador_programar_fichas, name='dinamizador_programar_fichas'),
    path(
        'api/dinamizador/ambientes/crear/',
        views.api_dinamizador_crear_ambiente,
        name='api_dinamizador_crear_ambiente',
    ),
    path(
        'dinamizador/fichas/<int:codigo_ficha>/eliminar/',
        views.dinamizador_eliminar_ficha,
        name='dinamizador_eliminar_ficha',
    ),
    path(
        'dinamizador/programacion/modo-pruebas/',
        views.dinamizador_toggle_modo_pruebas_programacion,
        name='dinamizador_toggle_modo_pruebas_programacion',
    ),
    path(
        'dinamizador/fichas/<int:codigo_ficha>/programacion/',
        views.dinamizador_ficha_programacion,
        name='dinamizador_ficha_programacion',
    ),
    path(
        'dinamizador/fichas/<int:codigo_ficha>/programacion/<int:anio>/<int:mes>/',
        views.dinamizador_ficha_programacion_mes,
        name='dinamizador_ficha_programacion_mes',
    ),
    path(
        'dinamizador/fichas/<int:codigo_ficha>/programacion/<int:id_programacion>/eliminar/',
        views.dinamizador_eliminar_programacion,
        name='dinamizador_eliminar_programacion',
    ),
    path(
        'api/dinamizador/fichas/<int:codigo_ficha>/programacion/<int:anio>/<int:mes>/datos/',
        views.api_ficha_programacion_mes_datos,
        name='api_ficha_programacion_mes_datos',
    ),
    path(
        'api/dinamizador/fichas/<int:codigo_ficha>/programacion/<int:anio>/<int:mes>/guardar/',
        views.api_ficha_programacion_mes_guardar,
        name='api_ficha_programacion_mes_guardar',
    ),
    path(
        'api/dinamizador/fichas/<int:codigo_ficha>/programacion/<int:id_programacion>/detalle/',
        views.api_ficha_programacion_detalle,
        name='api_ficha_programacion_detalle',
    ),
    path(
        'api/dinamizador/fichas/<int:codigo_ficha>/programacion/<int:anio>/<int:mes>/<int:id_programacion>/editar/',
        views.api_ficha_programacion_editar,
        name='api_ficha_programacion_editar',
    ),
]
