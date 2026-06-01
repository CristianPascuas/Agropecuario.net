
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('academico.urls')),
    path('portal/', include('portal.urls')),
]
