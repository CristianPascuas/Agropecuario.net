from __future__ import annotations

import csv
import hashlib
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone

from academico.models import CoordinadorEquipo, EquipoEjecutor, Rol, TipoDoc, Usuario


DEFAULT_PASSWORD = '12345678'


@dataclass
class InputRow:
    line_no: int
    team_name: str
    full_name: str
    role_slug: str
    raw_email: str
    raw_phone: str


def normalize_key(value: str) -> str:
    cleaned = unicodedata.normalize('NFKD', value or '')
    cleaned = ''.join(ch for ch in cleaned if not unicodedata.combining(ch))
    cleaned = cleaned.upper()
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def clean_text(value: str) -> str:
    return re.sub(r'\s+', ' ', (value or '').strip())


def split_name(full_name: str) -> tuple[str, str]:
    tokens = clean_text(full_name).split()
    if not tokens:
        return 'SIN', 'NOMBRE'
    if len(tokens) == 1:
        return tokens[0].title(), tokens[0].title()
    if len(tokens) == 2:
        return tokens[0].title(), tokens[1].title()
    return ' '.join(t.title() for t in tokens[:-2]), ' '.join(t.title() for t in tokens[-2:])


def clean_document(value: str) -> str:
    return re.sub(r'\D+', '', value or '')


def clean_email(value: str) -> str:
    cleaned = (value or '').strip().strip('"').strip("'")
    cleaned = cleaned.replace('\t', '').replace(' ', '').lower()
    if not cleaned:
        return ''
    try:
        validate_email(cleaned)
    except ValidationError:
        return ''
    return cleaned


def document_candidate_from_seed(seed: str) -> str:
    digest = hashlib.sha1(seed.encode('utf-8')).hexdigest()
    digits = ''.join(str(int(c, 16) % 10) for c in digest)
    return '3' + digits[:9]


def generate_document(seed: str, used_documents: set[str]) -> str:
    digest = hashlib.sha1(seed.encode('utf-8')).hexdigest()
    digits = ''.join(str(int(c, 16) % 10) for c in digest)
    candidate = document_candidate_from_seed(seed)
    counter = 1
    while candidate in used_documents:
        suffix = str(counter)
        candidate = ('3' + digits[: 9 - len(suffix)] + suffix)[:10]
        counter += 1
    return candidate


def generate_email(base_name: str, document: str, used_emails: set[str]) -> str:
    stem = normalize_key(base_name).lower().replace(' ', '.')
    stem = re.sub(r'[^a-z0-9._-]+', '', stem) or 'usuario'
    base = f'{stem}.{document}@import.local'
    if base not in used_emails:
        return base
    idx = 2
    while True:
        candidate = f'{stem}.{document}.{idx}@import.local'
        if candidate not in used_emails:
            return candidate
        idx += 1


class Command(BaseCommand):
    help = 'Importa ecosistemas/equipos y usuarios desde el CSV de Franco. Usa --apply para persistir.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', default='', help='Ruta del CSV. Si se omite, se busca en db/.')
        parser.add_argument('--coordinador-nombre', default='Franco', help='Nombre del coordinador nuevo.')
        parser.add_argument('--coordinador-apellido', default='Por Definir', help='Apellido del coordinador nuevo.')
        parser.add_argument('--apply', action='store_true', help='Aplica cambios en base de datos.')

    def handle(self, *args, **options):
        csv_path = self._resolve_csv_path(options['csv'])
        rows = self._parse_csv(csv_path)

        if not rows:
            raise CommandError('No se encontraron filas validas para importar.')

        tipo_doc = TipoDoc.objects.filter(id_tipodoc=1).first()
        if not tipo_doc:
            raise CommandError('No existe TipoDoc id=1 (CC).')

        rol_instructor = Rol.objects.filter(nombre__icontains='instru').first()
        rol_dinamizador = Rol.objects.filter(nombre__iexact='dinamizador').first()
        rol_coordinador = Rol.objects.filter(nombre__icontains='coordinador').first()
        if not rol_instructor or not rol_dinamizador or not rol_coordinador:
            raise CommandError('No se encontraron los roles requeridos: instructor, dinamizador, coordinador.')

        apply_changes = bool(options['apply'])
        result = self._import_rows(
            rows=rows,
            tipo_doc=tipo_doc,
            rol_instructor=rol_instructor,
            rol_dinamizador=rol_dinamizador,
            apply=apply_changes,
        )

        coordinador, coord_result = self._ensure_coordinator(
            nombre=options['coordinador_nombre'],
            apellido=options['coordinador_apellido'],
            tipo_doc=tipo_doc,
            rol_coordinador=rol_coordinador,
            apply=apply_changes,
        )

        links_result = self._link_coordinator_teams(
            coordinador=coordinador,
            team_names=result['team_names'],
            apply=apply_changes,
        )

        mode_label = 'APPLY' if apply_changes else 'DRY-RUN'
        self.stdout.write(self.style.SUCCESS(f'Importacion ecosistema Franco [{mode_label}]'))
        self.stdout.write(f'CSV: {csv_path}')
        self.stdout.write(f'Filas validas: {len(rows)}')
        self.stdout.write(f'Equipos creados: {result["teams_created"]}')
        self.stdout.write(f'Equipos existentes usados: {result["teams_existing"]}')
        self.stdout.write(f'Usuarios creados: {result["users_created"]}')
        self.stdout.write(f'Usuarios actualizados: {result["users_updated"]}')
        self.stdout.write(f'Documentos generados: {result["generated_documents"]}')
        self.stdout.write(f'Correos generados: {result["generated_emails"]}')
        self.stdout.write(f'Coordinador Franco: {coord_result}')
        self.stdout.write(f'Vinculos coordinador-equipo creados: {links_result["created"]}')
        self.stdout.write(f'Vinculos coordinador-equipo ya existentes: {links_result["existing"]}')
        if links_result['missing']:
            self.stdout.write(f'Equipos sin vinculo por no existir aun: {links_result["missing"]}')

    def _resolve_csv_path(self, csv_arg: str) -> Path:
        if csv_arg:
            path = Path(csv_arg)
            if not path.is_absolute():
                path = Path.cwd() / path
            if not path.exists():
                raise CommandError(f'No existe CSV: {path}')
            return path

        db_dir = Path.cwd() / 'db'
        matches = sorted(db_dir.glob('Instructores por coordin*FRANCO.csv'))
        if not matches:
            raise CommandError('No se encontro el CSV de Franco en db/.')
        return matches[0]

    def _parse_csv(self, csv_path: Path) -> list[InputRow]:
        parsed: list[InputRow] = []
        with csv_path.open('r', encoding='utf-8-sig', newline='') as handle:
            reader = csv.reader(handle, delimiter=';')
            for line_no, row in enumerate(reader, start=1):
                row = (row + ['', '', '', '', '', ''])[:6]
                _, team, full_name, role_marker, email, phone = [clean_text(item) for item in row]

                if not any([team, full_name, role_marker, email, phone]):
                    continue

                if normalize_key(team) == 'EQUIPO EJECUTOR':
                    continue

                if not team or not full_name:
                    continue

                role_slug = 'dinamizador' if 'DINAMIZADOR' in normalize_key(role_marker) else 'instructor'
                parsed.append(
                    InputRow(
                        line_no=line_no,
                        team_name=team,
                        full_name=full_name,
                        role_slug=role_slug,
                        raw_email=email,
                        raw_phone=phone,
                    )
                )
        return parsed

    def _import_rows(self, rows, tipo_doc, rol_instructor, rol_dinamizador, apply: bool) -> dict[str, int]:
        now = timezone.now()
        team_existing = {normalize_key(t.nombre): t for t in EquipoEjecutor.objects.all()}
        by_document = {u.documento: u for u in Usuario.objects.select_related('id_rol', 'id_equipo') if u.documento}
        by_email = {u.email.lower(): u for u in Usuario.objects.all() if u.email}
        used_documents = set(by_document.keys())
        used_emails = set(by_email.keys())

        password_hash = make_password(DEFAULT_PASSWORD)
        summary = {
            'teams_created': 0,
            'teams_existing': 0,
            'users_created': 0,
            'users_updated': 0,
            'generated_documents': 0,
            'generated_emails': 0,
            'team_names': set(),
        }

        def get_or_create_team(team_name: str):
            key = normalize_key(team_name)
            team = team_existing.get(key)
            if team:
                summary['teams_existing'] += 1
                return team
            if not apply:
                summary['teams_created'] += 1
                team = EquipoEjecutor(nombre=team_name, tipo=1, creado_en=now)
                team_existing[key] = team
                return team
            team = EquipoEjecutor.objects.create(nombre=team_name, tipo=1, creado_en=now)
            summary['teams_created'] += 1
            team_existing[key] = team
            return team

        def import_row(item: InputRow):
            team = get_or_create_team(item.team_name)
            summary['team_names'].add(item.team_name)
            role = rol_dinamizador if item.role_slug == 'dinamizador' else rol_instructor
            tipo_contrato = 1 if item.role_slug == 'dinamizador' else 0
            seed = f'{item.line_no}-{item.full_name}-{item.team_name}'

            raw_doc = clean_document(item.raw_phone)
            raw_mail = clean_email(item.raw_email)

            user = None
            if raw_doc and raw_doc in by_document:
                user = by_document[raw_doc]
            elif raw_mail and raw_mail in by_email:
                user = by_email[raw_mail]
            elif not raw_doc:
                deterministic_doc = document_candidate_from_seed(seed)
                if deterministic_doc in by_document:
                    user = by_document[deterministic_doc]

            nombre, apellido = split_name(item.full_name)
            documento = raw_doc
            if not documento and user is not None:
                documento = user.documento
            if not documento or (documento in used_documents and (not user or user.documento != documento)):
                documento = generate_document(seed, used_documents)
                summary['generated_documents'] += 1

            email = raw_mail
            if not email and user is not None and user.email:
                email = user.email.lower()
            if not email or (email in used_emails and (not user or user.email.lower() != email)):
                email = generate_email(item.full_name, documento, used_emails)
                summary['generated_emails'] += 1

            if user is None:
                user = by_document.get(documento) or by_email.get(email)

            used_documents.add(documento)
            used_emails.add(email)

            if tipo_contrato == 1:
                horas_max_mensual = 120
                horas_objetivo_anual = 1200
                horas_min_mensual = 120
                horas_min_anual = 1000
            else:
                horas_max_mensual = 160
                horas_objetivo_anual = 1680
                horas_min_mensual = 120
                horas_min_anual = 1680

            if user is None:
                summary['users_created'] += 1
                if not apply:
                    return
                user = Usuario.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    documento=documento,
                    id_tipodoc=tipo_doc,
                    id_rol=role,
                    id_equipo=team if getattr(team, 'pk', None) else None,
                    tipo_contrato=tipo_contrato,
                    activo=True,
                    sin_acceso=False,
                    email=email,
                    contrasena=password_hash,
                    horas_max_mensual=horas_max_mensual,
                    horas_objetivo_anual=horas_objetivo_anual,
                    horas_min_mensual=horas_min_mensual,
                    horas_min_anual=horas_min_anual,
                    tipo_dinamizador='instructor' if item.role_slug == 'dinamizador' else None,
                    creado_en=timezone.now(),
                )
                by_document[documento] = user
                by_email[email] = user
                return

            changed_fields = []
            updates = {
                'nombre': nombre,
                'apellido': apellido,
                'documento': documento,
                'id_tipodoc': tipo_doc,
                'id_rol': role,
                'id_equipo': team if getattr(team, 'pk', None) else user.id_equipo,
                'tipo_contrato': tipo_contrato,
                'activo': True,
                'sin_acceso': False,
                'email': email,
                'horas_max_mensual': horas_max_mensual,
                'horas_objetivo_anual': horas_objetivo_anual,
                'horas_min_mensual': horas_min_mensual,
                'horas_min_anual': horas_min_anual,
                'tipo_dinamizador': 'instructor' if item.role_slug == 'dinamizador' else None,
            }
            for field_name, new_value in updates.items():
                current_value = getattr(user, field_name)
                current_cmp = current_value.pk if hasattr(current_value, 'pk') else current_value
                new_cmp = new_value.pk if hasattr(new_value, 'pk') else new_value
                if current_cmp != new_cmp:
                    setattr(user, field_name, new_value)
                    changed_fields.append(field_name)

            if changed_fields:
                summary['users_updated'] += 1
                if apply:
                    user.save(update_fields=changed_fields)

        if apply:
            with transaction.atomic():
                for row in rows:
                    import_row(row)
        else:
            for row in rows:
                import_row(row)

        return summary

    def _ensure_coordinator(self, nombre, apellido, tipo_doc, rol_coordinador, apply: bool) -> tuple[Usuario | None, str]:
        nombre = clean_text(nombre) or 'Franco'
        apellido = clean_text(apellido) or 'Por Definir'

        existing = Usuario.objects.filter(
            nombre__iexact=nombre,
            apellido__iexact=apellido,
        ).first()

        if existing:
            changed = []
            if existing.id_rol_id != rol_coordinador.id_rol:
                existing.id_rol = rol_coordinador
                changed.append('id_rol')
            if existing.tipo_contrato != 0:
                existing.tipo_contrato = 0
                changed.append('tipo_contrato')
            if not existing.activo:
                existing.activo = True
                changed.append('activo')
            if getattr(existing, 'sin_acceso', False):
                existing.sin_acceso = False
                changed.append('sin_acceso')
            if existing.tipo_dinamizador is not None:
                existing.tipo_dinamizador = None
                changed.append('tipo_dinamizador')
            if changed and apply:
                existing.save(update_fields=changed)
            status = f'actualizado ({nombre} {apellido})' if changed else f'sin cambios ({nombre} {apellido})'
            return existing, status

        used_documents = set(Usuario.objects.values_list('documento', flat=True))
        used_emails = set(email.lower() for email in Usuario.objects.values_list('email', flat=True) if email)
        documento = generate_document(f'coordinador-{nombre}-{apellido}', used_documents)
        correo = generate_email(f'{nombre}.{apellido}.coordinador', documento, used_emails)

        if not apply:
            return None, f'creado en dry-run ({nombre} {apellido})'

        coordinator = Usuario.objects.create(
            nombre=nombre.title(),
            apellido=apellido.title(),
            documento=documento,
            id_tipodoc=tipo_doc,
            id_rol=rol_coordinador,
            id_equipo=None,
            tipo_contrato=0,
            activo=True,
            sin_acceso=False,
            email=correo,
            contrasena=make_password(DEFAULT_PASSWORD),
            horas_max_mensual=160,
            horas_objetivo_anual=1680,
            horas_min_mensual=120,
            horas_min_anual=1680,
            tipo_dinamizador=None,
            creado_en=timezone.now(),
        )
        return coordinator, f'creado ({nombre} {apellido})'

    def _link_coordinator_teams(self, coordinador, team_names: set[str], apply: bool) -> dict[str, int]:
        if not team_names:
            return {'created': 0, 'existing': 0, 'missing': 0}

        if coordinador is None:
            return {'created': 0, 'existing': 0, 'missing': len(team_names)}

        keys = {normalize_key(name) for name in team_names if name}
        equipos = {
            normalize_key(eq.nombre): eq
            for eq in EquipoEjecutor.objects.all()
            if normalize_key(eq.nombre) in keys
        }

        created = 0
        existing = 0
        missing = 0

        for key in keys:
            equipo = equipos.get(key)
            if not equipo:
                missing += 1
                continue

            if apply:
                _, was_created = CoordinadorEquipo.objects.get_or_create(
                    id_coordinador=coordinador,
                    id_equipo=equipo,
                )
                if was_created:
                    created += 1
                else:
                    existing += 1
                continue

            relation_exists = CoordinadorEquipo.objects.filter(
                id_coordinador=coordinador,
                id_equipo=equipo,
            ).exists()
            if relation_exists:
                existing += 1
            else:
                created += 1

        return {'created': created, 'existing': existing, 'missing': missing}
