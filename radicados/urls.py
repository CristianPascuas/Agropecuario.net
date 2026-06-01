from django.urls import path

from . import views

urlpatterns = [
    path('api/instructor/radicados/crear/', views.api_instructor_radicados_crear, name='api_instructor_radicados_crear'),
    path(
        'api/instructor/radicados/traslapes/<int:anio>/<int:mes>/',
        views.api_instructor_radicados_traslapes_mes,
        name='api_instructor_radicados_traslapes_mes',
    ),
    path('api/radicados/<int:id_radicado>/estado/', views.api_radicados_cambiar_estado, name='api_radicados_cambiar_estado'),
]
