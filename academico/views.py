from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import json
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import LoginForm, RegistroForm
from .models import CoordinadorEquipo, Rol, TipoDoc, Usuario

SESSION_USER_ID_KEY = 'usuario_id'


def _obtener_usuario_sesion(request):
	user_id = request.session.get(SESSION_USER_ID_KEY)
	if not user_id:
		return None
	try:
		return Usuario.objects.get(id_usuario=user_id, activo=True)
	except Usuario.DoesNotExist:
		return None


def _verificar_contrasena(contrasena_ingresada, contrasena_guardada):
	if not contrasena_guardada:
		return False
	if contrasena_guardada == contrasena_ingresada:
		return True
	try:
		return check_password(contrasena_ingresada, contrasena_guardada)
	except ValueError:
		return False


def login_view(request):
	if _obtener_usuario_sesion(request):
		return redirect('portal_home')

	form = LoginForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		documento = form.cleaned_data['documento'].strip()
		contrasena = form.cleaned_data['contrasena']

		try:
			usuario = Usuario.objects.get(documento=documento)
		except Usuario.DoesNotExist:
			messages.error(request, 'Documento o contraseña inválidos.')
			return render(request, 'academico/login.html', {'form': form})

		if not usuario.activo:
			if getattr(usuario, 'sin_acceso', False):
				messages.error(request, 'Tu cuenta no tiene acceso al sistema. Contacta al administrador para reintegro.')
			else:
				messages.warning(request, 'Tu cuenta está pendiente de aprobación por un administrador.')
			return render(request, 'academico/login.html', {'form': form})

		if not _verificar_contrasena(contrasena, usuario.contrasena):
			messages.error(request, 'Documento o contraseña inválidos.')
			return render(request, 'academico/login.html', {'form': form})

		if usuario.contrasena == contrasena:
			usuario.contrasena = make_password(contrasena)
			usuario.save(update_fields=['contrasena'])

		request.session[SESSION_USER_ID_KEY] = usuario.id_usuario
		return redirect('portal_home')

	return render(request, 'academico/login.html', {'form': form})


def registro_view(request):
	form = RegistroForm(request.POST or None)

	coordinador_equipos_map = {}
	relaciones = CoordinadorEquipo.objects.select_related('id_coordinador', 'id_equipo').order_by('id_equipo__nombre')
	for rel in relaciones:
		coord_id = str(rel.id_coordinador_id)
		coordinador_equipos_map.setdefault(coord_id, [])
		coordinador_equipos_map[coord_id].append(
			{
				'id': str(rel.id_equipo_id),
				'nombre': rel.id_equipo.nombre,
			}
		)

	if request.method == 'POST' and form.is_valid():
		documento = form.cleaned_data['documento'].strip()
		email = form.cleaned_data['email'].strip().lower()

		if Usuario.objects.filter(documento=documento).exists():
			form.add_error('documento', 'Este documento ya está registrado.')
			return render(request, 'academico/registro.html', {'form': form})

		if Usuario.objects.filter(email=email).exists():
			form.add_error('email', 'Este correo ya está registrado.')
			return render(request, 'academico/registro.html', {'form': form})

		try:
			tipo_doc = TipoDoc.objects.get(id_tipodoc=int(form.cleaned_data['tipo_documento']))
			rol = Rol.objects.get(id_rol=int(form.cleaned_data['rol']))
		except (TipoDoc.DoesNotExist, Rol.DoesNotExist, ValueError, TypeError):
			messages.error(request, 'No se pudo registrar por datos inválidos en tipo de documento o rol.')
			return render(request, 'academico/registro.html', {'form': form})

		equipo = None
		rol_nombre = rol.nombre.lower()
		tipo_contrato = int(form.cleaned_data['tipo_contrato'])
		horas_max_mensual = 160
		horas_objetivo_anual = 1680
		horas_min_mensual = 120
		horas_min_anual = 1680

		if form.cleaned_data.get('equipo'):
			equipo = form.cleaned_data['equipo']

		if tipo_contrato == 1:
			horas_max_mensual = 120
			horas_objetivo_anual = 1200
			horas_min_mensual = 120
			horas_min_anual = 1000

		Usuario.objects.create(
			nombre=form.cleaned_data['nombre'].strip(),
			apellido=form.cleaned_data['apellido'].strip(),
			documento=documento,
			id_tipodoc=tipo_doc,
			id_rol=rol,
			id_equipo_id=int(equipo) if equipo else None,
			tipo_contrato=tipo_contrato,
			activo=False,
			sin_acceso=False,
			email=email,
			contrasena=make_password(form.cleaned_data['contrasena']),
			horas_max_mensual=horas_max_mensual,
			horas_objetivo_anual=horas_objetivo_anual,
			horas_min_mensual=horas_min_mensual,
			horas_min_anual=horas_min_anual,
			tipo_dinamizador=None,
			creado_en=timezone.now(),
		)

		messages.success(request, 'Cuenta creada. Un administrador debe aprobar tu registro antes de poder iniciar sesión.')
		return redirect('login')

	return render(
		request,
		'academico/registro.html',
		{
			'form': form,
			'coordinador_equipos_map_json': json.dumps(coordinador_equipos_map),
		},
	)


def inicio(request):
	usuario = _obtener_usuario_sesion(request)
	if not usuario:
		return redirect('login')
	return redirect('portal_home')


def logout_view(request):
    request.session.flush()
    return redirect('login')
