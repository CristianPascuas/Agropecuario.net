from django import forms
from django.db.models import Q

from academico.models import Ambiente, EquipoPrograma, Ficha, Horario, Municipio, ProgramaFormacion, Usuario


TIPO_FICHA_CHOICES = (
    ('Presencial', 'Presencial'),
    ('Virtual', 'Virtual'),
    ('Mixta', 'Mixta'),
)


def _etiqueta_horario(horario):
    base = (horario.horario or '').strip().lower()
    base_normalizado = base.replace('ñ', 'n')
    if 'man' in base_normalizado:
        return 'Mañana (7:00 a 13:00) - 30 horas/semana'
    if 'tarde' in base_normalizado:
        return 'Tarde (13:00 a 18:00) - 30 horas/semana'
    if 'noche' in base_normalizado:
        return 'Noche (18:00 a 22:00) - 20 horas/semana'
    return f"{horario.horario.title()} - {horario.horas} horas/semana"


class CrearFichaForm(forms.Form):
    codigo_ficha = forms.IntegerField(min_value=1, label='Codigo de ficha')
    id_programa_formacion = forms.ModelChoiceField(
        queryset=ProgramaFormacion.objects.none(),
        empty_label='Seleccionar...',
        label='Programa de formacion',
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de inicio',
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de fin',
    )
    id_horario = forms.ChoiceField(choices=(), label='Horario')
    id_lider_ficha = forms.ModelChoiceField(
        queryset=Usuario.objects.none(),
        empty_label='Seleccionar...',
        label='Lider de ficha',
    )
    id_ambiente = forms.ModelChoiceField(
        queryset=Ambiente.objects.none(),
        empty_label='Seleccionar...',
        label='Ambiente de formacion',
        required=True,
    )
    tipo_ficha = forms.ChoiceField(
        choices=(('', 'Seleccionar...'),) + TIPO_FICHA_CHOICES,
        label='Tipo de ficha',
    )
    codigo_municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        empty_label='Seleccionar...',
        label='Municipio de formacion',
    )

    def __init__(self, *args, usuario=None, ficha_actual=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        self.ficha_actual = ficha_actual

        programas_queryset = ProgramaFormacion.objects.none()
        if usuario and usuario.id_equipo_id:
            programas_ids = EquipoPrograma.objects.filter(
                id_equipo_id=usuario.id_equipo_id
            ).values_list('id_programa_formacion_id', flat=True)
            programas_queryset = ProgramaFormacion.objects.filter(
                id_programa_formacion__in=programas_ids
            ).order_by('nombre')

        self.fields['id_programa_formacion'].queryset = programas_queryset
        self.fields['codigo_municipio'].queryset = Municipio.objects.order_by('municipio')

        ambientes_queryset = Ambiente.objects.filter(codigo_municipio__isnull=False).order_by('ambiente')
        municipio_seleccionado = self.data.get('codigo_municipio') or self.initial.get('codigo_municipio')
        if municipio_seleccionado:
            try:
                ambientes_queryset = ambientes_queryset.filter(codigo_municipio_id=int(municipio_seleccionado))
            except (TypeError, ValueError):
                ambientes_queryset = Ambiente.objects.none()
        else:
            ambientes_queryset = Ambiente.objects.none()
        self.fields['id_ambiente'].queryset = ambientes_queryset

        instructores_queryset = Usuario.objects.none()
        if usuario and usuario.id_equipo_id:
            instructores_queryset = Usuario.objects.filter(
                activo=True,
                id_equipo_id=usuario.id_equipo_id,
            ).filter(
                Q(id_rol__nombre__icontains='instr') | Q(id_usuario=usuario.id_usuario)
            ).order_by('nombre', 'apellido')
        self.fields['id_lider_ficha'].queryset = instructores_queryset

        self.fields['id_programa_formacion'].label_from_instance = (
            lambda obj: f"{obj.codigo} - {obj.nombre.strip()}"
        )
        self.fields['id_ambiente'].label_from_instance = (
            lambda obj: f"{obj.ambiente.title()} - {(obj.codigo_municipio.municipio.title() if obj.codigo_municipio else 'Sin municipio')}"
        )
        self.fields['codigo_municipio'].label_from_instance = (
            lambda obj: obj.municipio.title()
        )
        self.fields['id_lider_ficha'].label_from_instance = (
            lambda obj: f"{obj.nombre} {obj.apellido} ({obj.documento})"
        )

        horario_choices = [('', 'Seleccionar...')]
        for horario in Horario.objects.order_by('id_horario'):
            horario_choices.append((str(horario.id_horario), _etiqueta_horario(horario)))
        self.fields['id_horario'].choices = horario_choices

    def clean_codigo_ficha(self):
        codigo = self.cleaned_data['codigo_ficha']
        qs = Ficha.objects.filter(codigo_ficha=codigo)
        if self.ficha_actual:
            qs = qs.exclude(codigo_ficha=self.ficha_actual.codigo_ficha)
        if qs.exists():
            raise forms.ValidationError('Este codigo de ficha ya existe.')
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        ambiente = cleaned_data.get('id_ambiente')
        municipio = cleaned_data.get('codigo_municipio')
        horario_id = cleaned_data.get('id_horario')

        if not ambiente:
            self.add_error('id_ambiente', 'Selecciona un ambiente existente.')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', 'La fecha fin no puede ser menor que la fecha de inicio.')

        if fecha_inicio and fecha_fin and ambiente and horario_id:
            conflicto = Ficha.objects.filter(
                id_ambiente=ambiente,
                id_horario_id=int(horario_id),
                fecha_inicio__lte=fecha_fin,
                fecha_fin__gte=fecha_inicio,
            )
            if self.ficha_actual:
                conflicto = conflicto.exclude(codigo_ficha=self.ficha_actual.codigo_ficha)

            if conflicto.exists():
                self.add_error(
                    'id_ambiente',
                    'Ya existe una ficha en este ambiente, mismo horario y dentro del mismo lapso de fechas.',
                )

        if ambiente and municipio and ambiente.codigo_municipio_id != municipio.codigo_municipio:
            self.add_error(
                'id_ambiente',
                'El ambiente seleccionado no pertenece al municipio de formacion elegido.',
            )

        if self.usuario and not self.usuario.id_equipo_id:
            raise forms.ValidationError('Tu usuario no tiene equipo asignado. No es posible crear fichas.')

        if self.usuario and self.fields['id_lider_ficha'].queryset.count() == 0:
            raise forms.ValidationError(
                'No hay instructores activos en tu equipo y tampoco se encontró dinamizador asignado para liderar la ficha.'
            )

        return cleaned_data
