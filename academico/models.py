
import os

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


TIPO_COMPETENCIA_CHOICES = (
    ('tecnica', 'Técnica'),
    ('trasversal', 'Trasversal'),
)

TIPO_EQUIPO_CHOICES = (
    (0, 'Trasversal'),
    (1, 'Tecnica'),
)

ESTADO_PROGRAMACION_CHOICES = (
    ('programada', 'Programada'),
    ('ajustada', 'Ajustada'),
    ('reemplazada', 'Reemplazada'),
    ('ejecutada', 'Ejecutada'),
    ('cancelada', 'Cancelada'),
)

TIPO_DINAMIZADOR_CHOICES = (
    ('instructor', 'Dinamizador-Instructor'),
    ('coordinador', 'Dinamizador-Coordinador'),
)


class Ambiente(models.Model):
    id_ambiente = models.AutoField(primary_key=True)
    ambiente = models.CharField(max_length=120)
    lugar = models.CharField(max_length=100)
    codigo_municipio = models.ForeignKey(
        'Municipio',
        models.DO_NOTHING,
        db_column='codigo_municipio',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'ambiente'

    def __str__(self):
        return f"{self.ambiente} ({self.lugar})"


class Competencia(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=30)
    id_programa_formacion = models.ForeignKey('ProgramaFormacion', models.DO_NOTHING, db_column='id_programa_formacion')
    nombre = models.CharField(max_length=180)
    tipo_competencia = models.CharField(max_length=10, choices=TIPO_COMPETENCIA_CHOICES)
    horas_max = models.IntegerField()

    class Meta:
        db_table = 'competencia'
        unique_together = (('id_programa_formacion', 'codigo'),)


class EquipoEjecutor(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=120)
    tipo = models.PositiveSmallIntegerField(choices=TIPO_EQUIPO_CHOICES, default=1)
    creado_en = models.DateTimeField()

    class Meta:
        db_table = 'equipo_ejecutor'

    def __str__(self):
        return self.nombre


class EquipoPrograma(models.Model):
    id_equipo_programa = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(EquipoEjecutor, models.DO_NOTHING, db_column='id_equipo')
    id_programa_formacion = models.ForeignKey('ProgramaFormacion', models.DO_NOTHING, db_column='id_programa_formacion')

    class Meta:
        db_table = 'equipo_programa'
        unique_together = (('id_equipo', 'id_programa_formacion'),)


class Ficha(models.Model):
    codigo_ficha = models.IntegerField(primary_key=True)
    id_programa_formacion = models.ForeignKey('ProgramaFormacion', models.DO_NOTHING, db_column='id_programa_formacion')
    id_equipo = models.ForeignKey(EquipoEjecutor, models.DO_NOTHING, db_column='id_equipo')
    id_lider_ficha = models.ForeignKey(
        'Usuario',
        models.DO_NOTHING,
        db_column='id_lider_ficha',
        related_name='fichas_lideradas',
        blank=True,
        null=True,
    )
    id_horario = models.ForeignKey('Horario', models.DO_NOTHING, db_column='id_horario', blank=True, null=True)
    tipo_ficha = models.CharField(max_length=40)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    codigo_municipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='codigo_municipio')
    id_ambiente = models.ForeignKey(Ambiente, models.DO_NOTHING, db_column='id_ambiente')

    class Meta:
        db_table = 'ficha'


class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    horario = models.CharField(unique=True, max_length=120)
    horas = models.SmallIntegerField()

    class Meta:
        db_table = 'horario'

    def __str__(self):
        return f"{self.horario} ({self.horas}h)"


class Municipio(models.Model):
    codigo_municipio = models.IntegerField(primary_key=True)
    municipio = models.CharField(max_length=120)

    class Meta:
        db_table = 'municipio'

    def __str__(self):
        return self.municipio


class ProgramaFormacion(models.Model):
    id_programa_formacion = models.AutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=40)
    nombre = models.CharField(max_length=180)
    horas_max = models.IntegerField()
    horas_lectiva = models.IntegerField()
    horas_productivas = models.IntegerField()

    class Meta:
        db_table = 'programa_formacion'

    def __str__(self):
        return f"{self.codigo} - {self.nombre.strip()}"


class Programacion(models.Model):
    id_programacion = models.AutoField(primary_key=True)
    codigo_ficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='codigo_ficha')
    id_ambiente = models.ForeignKey(
        Ambiente,
        models.DO_NOTHING,
        db_column='id_ambiente',
        blank=True,
        null=True,
    )
    id_competencia = models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia')
    id_instructor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_instructor', related_name='programaciones_instructor')
    id_dinamizador_asignador = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_dinamizador_asignador', related_name='programaciones_dinamizador')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    mes_operativo = models.PositiveSmallIntegerField(blank=True, null=True)
    anio_operativo = models.PositiveSmallIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_PROGRAMACION_CHOICES, default='programada')
    creado_en = models.DateTimeField()
    modificado_en = models.DateTimeField(blank=True, null=True)
    razon_cambio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'programacion'


class ProgramacionDia(models.Model):
    id_programacion_dia = models.AutoField(primary_key=True)
    fecha = models.DateField()
    horas_dia = models.PositiveSmallIntegerField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, default='programada')
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(blank=True, null=True)

    codigo_ficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='codigo_ficha')
    id_competencia = models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia')
    id_instructor = models.ForeignKey(
        'Usuario',
        models.DO_NOTHING,
        db_column='id_instructor',
        related_name='programaciones_dia_instructor',
    )
    id_dinamizador_asignador = models.ForeignKey(
        'Usuario',
        models.DO_NOTHING,
        db_column='id_dinamizador_asignador',
        related_name='programaciones_dia_dinamizador',
    )
    id_usuario_modificacion = models.ForeignKey(
        'Usuario',
        models.DO_NOTHING,
        db_column='id_usuario_modificacion',
        related_name='programaciones_dia_modificadas',
        blank=True,
        null=True,
    )
    id_horario = models.ForeignKey(Horario, models.DO_NOTHING, db_column='id_horario')

    class Meta:
        db_table = 'programacion_dia'
        unique_together = (('codigo_ficha', 'fecha', 'id_instructor'),)


class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    id_competencia = models.ForeignKey(Competencia, models.DO_NOTHING, db_column='id_competencia')
    nombre = models.CharField(max_length=180)

    class Meta:
        db_table = 'resultado'


class ProgramacionDiaResultado(models.Model):
    id_programacion_dia_resultado = models.AutoField(primary_key=True)
    id_programacion_dia = models.ForeignKey(ProgramacionDia, models.DO_NOTHING, db_column='id_programacion_dia')
    id_resultado = models.ForeignKey(Resultado, models.DO_NOTHING, db_column='id_resultado')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'programacion_dia_resultado'
        unique_together = (('id_programacion_dia', 'id_resultado'),)


class ProgramacionResultado(models.Model):
    id_programacion_resultado = models.AutoField(primary_key=True)
    id_programacion = models.ForeignKey(Programacion, models.DO_NOTHING, db_column='id_programacion')
    id_resultado = models.ForeignKey(Resultado, models.DO_NOTHING, db_column='id_resultado')
    horas_objetivo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    horas_dictadas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programacion_resultado'
        unique_together = (('id_programacion', 'id_resultado'),)


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80)

    class Meta:
        db_table = 'rol'

    def __str__(self):
        return self.nombre


class TipoDoc(models.Model):
    id_tipodoc = models.AutoField(primary_key=True)
    tipodoc = models.CharField(unique=True, max_length=30)

    class Meta:
        db_table = 'tipo_doc'

    def __str__(self):
        return self.tipodoc


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(unique=True, max_length=30)
    id_tipodoc = models.ForeignKey(TipoDoc, models.DO_NOTHING, db_column='id_tipodoc')
    id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='id_rol')
    id_equipo = models.ForeignKey(EquipoEjecutor, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)
    tipo_contrato = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)
    sin_acceso = models.BooleanField(default=False)
    email = models.CharField(unique=True, max_length=120)
    contrasena = models.CharField(max_length=255)
    horas_objetivo_anual = models.IntegerField(default=1680)
    horas_max_mensual = models.PositiveSmallIntegerField(default=160)
    horas_min_mensual = models.PositiveSmallIntegerField(default=140)
    horas_min_anual = models.IntegerField(default=1680)
    tipo_dinamizador = models.CharField(
        max_length=15,
        choices=TIPO_DINAMIZADOR_CHOICES,
        blank=True,
        null=True,
    )
    creado_en = models.DateTimeField()

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.documento})"


class CoordinadorEquipo(models.Model):
    id_coordinador_equipo = models.AutoField(primary_key=True)
    id_coordinador = models.ForeignKey(
        Usuario,
        models.DO_NOTHING,
        db_column='id_coordinador',
        related_name='coordinador_equipos',
    )
    id_equipo = models.ForeignKey(
        EquipoEjecutor,
        models.DO_NOTHING,
        db_column='id_equipo',
        related_name='equipos_por_coordinador',
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coordinador_equipo'
        unique_together = (('id_coordinador', 'id_equipo'),)

    def __str__(self):
        return f"{self.id_coordinador} -> {self.id_equipo}"


def ruta_archivo_radicado(instance, filename):
    instructor = getattr(instance, 'id_instructor', None)
    if instructor is not None:
        nombre_usuario = f"{instructor.nombre} {instructor.apellido}".strip()
        if not nombre_usuario:
            nombre_usuario = str(getattr(instructor, 'documento', '') or '').strip()
        if not nombre_usuario:
            nombre_usuario = f"usuario-{getattr(instructor, 'id_usuario', 'sin-id')}"
    else:
        nombre_usuario = 'sin-usuario'

    carpeta_usuario = slugify(nombre_usuario) or 'sin-usuario'
    carpeta_fecha = timezone.localdate().isoformat()

    base, _ext = os.path.splitext(filename or '')
    nombre_base = slugify(base) or 'archivo'
    return f"radicados/{carpeta_usuario}/{carpeta_fecha}/{nombre_base}.pdf"


class Radicado(models.Model):
    id_radicado = models.AutoField(primary_key=True)
    nombre_radicado = models.CharField(max_length=180)
    tipo_radicado = models.PositiveSmallIntegerField()
    descripcion_radicado = models.TextField()
    empresa_organizacion = models.CharField(max_length=180, blank=True, default='')
    nit = models.CharField(max_length=40, blank=True, default='')
    lugar = models.CharField(max_length=180, blank=True, default='')
    dias_seleccionados = models.TextField(blank=True, default='')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    archivo_excel = models.FileField(upload_to=ruta_archivo_radicado)
    aprobado = models.PositiveSmallIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    id_instructor = models.ForeignKey(
        Usuario,
        models.DO_NOTHING,
        db_column='id_instructor',
        related_name='radicados_instructor',
    )

    class Meta:
        db_table = 'radicado'
