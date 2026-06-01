from django.urls import path

from .views import inicio, login_view, logout_view, registro_view

urlpatterns = [
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', logout_view, name='logout'),
]
