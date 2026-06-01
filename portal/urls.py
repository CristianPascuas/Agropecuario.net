from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.portal_home, name='portal_home'),
    path('', include('radicados.urls')),
    path('', include('programacion.urls')),
    path('', include('consultas.urls')),
]
