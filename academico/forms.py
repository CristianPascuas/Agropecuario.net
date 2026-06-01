from django import forms
from django.db.models import Q

from .models import CoordinadorEquipo, EquipoEjecutor, Rol, TipoDoc, Usuario


class LoginForm(forms.Form):
    documento = forms.CharField(max_length=30, label='Número de documento')
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    apellido = forms.CharField(max_length=100, label='Apellido')
    documento = forms.CharField(max_length=30, label='Número de documento')
    tipo_documento = forms.ChoiceField(choices=(), label='Tipo de documento')
    rol = forms.ChoiceField(choices=(), label='Rol')
    coordinador = forms.ChoiceField(choices=(), label='Coordinador', required=False)
    tipo_contrato = forms.ChoiceField(
        choices=(
            ('0', 'Contrato'),
            ('1', 'Planta'),
        ),
        initial='0',
        label='Tipo de contrato',
    )
    equipo = forms.ChoiceField(choices=(), label='Equipo', required=False)
    email = forms.EmailField(max_length=120, label='Correo electrónico')
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'].choices = [('', 'Seleccionar...')] + [
            (str(item.id_tipodoc), item.tipodoc) for item in TipoDoc.objects.order_by('tipodoc')
        ]
        roles_permitidos = Rol.objects.filter(
            nombre__iregex=r'(instr|coordinador)',
        ).exclude(nombre__icontains='dinamizador').exclude(nombre__icontains='administrador').order_by('nombre')
        self.fields['rol'].choices = [('', 'Seleccionar...')] + [
            (str(item.id_rol), item.nombre.title()) for item in roles_permitidos
        ]

        coordinadores = Usuario.objects.filter(
            activo=True,
        ).filter(
            Q(id_rol__nombre__icontains='coordinador')
            | Q(id_rol__nombre__icontains='dinamizador', tipo_dinamizador='coordinador')
        ).order_by('nombre', 'apellido')
        self.fields['coordinador'].choices = [('', 'Seleccionar...')] + [
            (str(item.id_usuario), f"{item.nombre} {item.apellido}") for item in coordinadores
        ]

        rol_id = self.data.get('rol') if self.is_bound else self.initial.get('rol')
        coordinador_id = self.data.get('coordinador') if self.is_bound else self.initial.get('coordinador')
        rol_nombre = ''
        if rol_id and str(rol_id).isdigit():
            rol_obj = Rol.objects.filter(id_rol=int(rol_id)).first()
            rol_nombre = (rol_obj.nombre or '').lower() if rol_obj else ''

        if 'instructor' in rol_nombre:
            if coordinador_id and str(coordinador_id).isdigit():
                equipos_qs = EquipoEjecutor.objects.filter(
                    equipos_por_coordinador__id_coordinador_id=int(coordinador_id),
                ).distinct().order_by('nombre')
                self.fields['equipo'].choices = [('', 'Seleccionar...')] + [
                    (str(item.id_equipo), item.nombre) for item in equipos_qs
                ]
            else:
                self.fields['equipo'].choices = [('', 'Seleccionar coordinador primero...')]
        else:
            self.fields['equipo'].choices = [('', 'Seleccionar...')] + [
                (str(item.id_equipo), item.nombre) for item in EquipoEjecutor.objects.order_by('nombre')
            ]

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')

        rol_id = cleaned_data.get('rol')
        equipo = cleaned_data.get('equipo')
        coordinador = cleaned_data.get('coordinador')

        rol_nombre = ''
        if rol_id:
            try:
                rol_nombre = Rol.objects.get(id_rol=int(rol_id)).nombre.lower()
            except (Rol.DoesNotExist, ValueError, TypeError):
                self.add_error('rol', 'El rol seleccionado no es válido.')
                return cleaned_data

        if 'instructor' in rol_nombre and not equipo and 'equipo' not in self.errors:
            self.add_error('equipo', 'Debe seleccionar un equipo para el rol instructor.')

        if 'instructor' in rol_nombre and not coordinador:
            self.add_error('coordinador', 'Debe seleccionar un coordinador para el rol instructor.')

        if 'instructor' in rol_nombre and coordinador and equipo:
            try:
                coordinador_id = int(coordinador)
                equipo_id = int(equipo)
            except (TypeError, ValueError):
                self.add_error('coordinador', 'El coordinador seleccionado no es válido.')
                return cleaned_data

            coordinador_valido = Usuario.objects.filter(
                id_usuario=coordinador_id,
                activo=True,
            ).filter(
                Q(id_rol__nombre__icontains='coordinador')
                | Q(id_rol__nombre__icontains='dinamizador', tipo_dinamizador='coordinador')
            ).exists()
            if not coordinador_valido:
                self.add_error('coordinador', 'El coordinador seleccionado no es válido.')
                return cleaned_data

            pertenece_al_ecosistema = CoordinadorEquipo.objects.filter(
                id_coordinador_id=coordinador_id,
                id_equipo_id=equipo_id,
            ).exists()
            if not pertenece_al_ecosistema:
                self.add_error('equipo', 'Debe seleccionar un equipo del ecosistema del coordinador elegido.')

        if 'coordinador' in rol_nombre and not equipo and 'equipo' not in self.errors:
            self.add_error('equipo', 'Debe seleccionar un equipo para el rol coordinador.')

        return cleaned_data