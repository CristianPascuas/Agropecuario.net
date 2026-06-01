from django.contrib import admin
from .models import (
	Ambiente,
	Competencia,
	EquipoEjecutor,
	EquipoPrograma,
	Ficha,
	Horario,
	Municipio,
	Programacion,
	ProgramacionDia,
	ProgramaFormacion,
	Resultado,
	Rol,
	TipoDoc,
	Usuario,
)

admin.site.register(Ambiente)
admin.site.register(Competencia)
admin.site.register(EquipoEjecutor)
admin.site.register(EquipoPrograma)
admin.site.register(Ficha)
admin.site.register(Horario)
admin.site.register(Municipio)
admin.site.register(Programacion)
admin.site.register(ProgramacionDia)
admin.site.register(ProgramaFormacion)
admin.site.register(Resultado)
admin.site.register(Rol)
admin.site.register(TipoDoc)
admin.site.register(Usuario)
