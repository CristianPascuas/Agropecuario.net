from __future__ import annotations

import csv
import hashlib
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from academico.models import EquipoEjecutor, Rol, TipoDoc, Usuario


DEFAULT_PASSWORD = '12345678'
CSV_DEFAULT = Path('db') / 'equipos_javier.csv'
SANDRA_EXCLUSION = 'SANDRA MERCEDES DIAZ LALINDE'
COORDINADOR_COMPLEMENTARIOS = 'JAVIER MAURICIO PALOMINO'
SKIP_MARKERS = {'CONTRATISTA', 'PLANTA', 'TOTAL'}


TEAM_DEFINITIONS = {
    1: {
        'name': 'SISTEMAS',
        'aliases': {
            'SISTEMAS',
            'ADSO',
            'SISTMAS TELEINFORMATICO',
            'SISTEMAS TELE INFORMATICOS',
            'SISTEMAS TELINFORMATICOS',
        },
    },
    2: {
        'name': 'GESTION DE LA SEGURIDAD Y SALUD EN EL TRABAJO',
        'aliases': {
            'GESTION DE LA SEGURIDAD Y SALUD EN EL TRABAJO',
            'ENTRENADOR PARA TRABAJO EN ALTURAS',
        },
    },
    3: {
        'name': 'GESTION TALENTO HUMANO',
        'aliases': {
            'GESTION TALENTO HUMANO',
            'COORDINACION EN SISTEMAS INTEGRADOS DE GESTION',
            'COORDINACION EN SISTEMAS INTEGRADOS DE GESTION - MERCADOS',
            'COORDINACION EN SISTEMAS INTEGRADOS DE GESTION - CONTABILIDAD',
        },
    },
    4: {
        'name': 'DESARROLLO DE PROCESOS DE MERCADEO',
        'aliases': {
            'DESARROLLO DE PROCESOS DE MERCADEO',
            'DESARROLLO DE PROCESOS DE MERCADEO - INGLES',
        },
    },
    5: {
        'name': 'TRANSVERSALES',
        'aliases': {
            'TRANSVERSALES',
            'FORTALECIMIENTO DE LA INTEGRALIDAD EN LOS PROCESOS INSTITUCIONALES - TRANSVERSAL',
            'ANALISIS Y DESARROLLO DE SOFTWARE - TRAMSVERSAL',
            'ANALISIS Y DESARROLLO DE SOFTWARE - TRANSVERSAL',
            'COORDINACION EN SISTEMAS INTEGRADOS DE GESTION - TRANSVERSAL',
            'DESARROLLO PUBLICITARIO - TRANSVERSAL',
            'COORDINACION DE PROCESOS LOGISTICOS - TRANSVERSAL',
            'GESTION TALENTO HUMANO - TRANASVERSAL',
        },
    },
    6: {
        'name': 'AGROINDUSTRIA',
        'aliases': {
            'AGROINDUSTRIA',
            'DESARROLLO DE HABILIDADES SENSORIALES EN CAFE - AGROINDUSTRIA',
            'DESARROLLO DE HABILIDADES SENSORIALES EN CAFE',
            'TRANSFORMACION DEL CACAO Y ELABORACION DE PRODUCTOS DE CHOCOLATERIA INDUSTRIAL',
            'AGROINDUSTRIA ALIMENTARIA',
            'ELABORACION ARTESANAL DE PRODUCTOS DE PANIFICACION',
            'TOSTION DE CAFE NIVEL I',
            'SERVICIOS DE BARISMO',
            'PROCESAMIENTO DE ALIMENTOS - ECONOMIA POPULAR (JOSE ALIRIO)',
            'PROCESAMIENTO DE FRUTAS Y VERDURAS - GUAPI',
        },
    },
    7: {
        'name': 'VIRTUALES',
        'aliases': {
            'VIRTUALES',
            'ANALISIS Y DESARROLLO DE SOFTWARE - VIRTUAL',
            'COORDINACION DE PROCESOS LOGISTICOS - VIRTUAL',
            'GESTION AGROEMPRESARIAL - VIRTUAL',
            'PRODUCCION PECUARIA - VIRTUAL',
            'OPERACIONES DE COMERCIO EXTERIOR - VIRTUAL',
            'DESARROLLO PUBLICITARIO - VIRTUAL',
            'COMPLEMENTARIA VIRTUAL SIN IDIOMAS - VIRTUAL',
            'MANEJO DE HERRAMIENTAS MICROSOFT OFFICE 2016 EXCEL - VIRTUAL',
            'GESTION DE LA SEGURIDAD Y SALUD EN EL TRABAJO - VIRTUAL',
            'DESARROLLO DE PROCESOS DE MERCADEO - VIRTUAL',
            'ENGLISH DOES WORK - LEVEL 1 - VIRTUAL',
            'INSTITUCIONAL DE LA ENSENANZA DE IDIOMAS - INGLES - VIRTUAL',
        },
    },
    8: {
        'name': 'COMPLEMENTARIOS',
        'aliases': {
            'COMPLEMENTARIOS',
            'GESTION TALENTO HUMANO - COMPLEMENTARIA',
            'COMPORTAMIENTO EMPRESARIAL - COMPLEMENTARIA',
            'GESTION AGROEMPRESARIAL - COMPLEMENTARIA',
            'EMPRENDIMIENTO EN UNIDADES PRODUCTIVAS - COMPLEMENTARIA',
            'COSTOS POR ORDENES DE PRODUCCION EN LAS MIPYMES - COMPLEMENTARIA',
        },
    },
}


TEAM_LOOKUP = {}
for team_id, definition in TEAM_DEFINITIONS.items():
    for alias in definition['aliases']:
        TEAM_LOOKUP[alias] = team_id


@dataclass
class ImportRow:
    line_no: int
    source_kind: str
    raw_program: str
    team_id: int
    team_name: str
    full_name: str
    raw_document: str
    raw_email: str
    role_slug: str
    tipo_contrato: int


def normalize_key(value: str) -> str:
    cleaned = unicodedata.normalize('NFKD', value or '')
    cleaned = ''.join(char for char in cleaned if not unicodedata.combining(char))
    cleaned = cleaned.upper()
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def clean_name(value: str) -> str:
    value = re.sub(r'\s+', ' ', (value or '').strip())
    return value


def split_name(full_name: str) -> tuple[str, str]:
    tokens = clean_name(full_name).split()
    if not tokens:
        return 'SIN', 'NOMBRE'
    if len(tokens) == 1:
        return tokens[0].title(), tokens[0].title()
    if len(tokens) == 2:
        return tokens[0].title(), tokens[1].title()
    return ' '.join(token.title() for token in tokens[:-2]), ' '.join(token.title() for token in tokens[-2:])


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


def strip_suffixes(program_label: str) -> str:
    normalized = normalize_key(program_label)
    for suffix in (' - PLANTA LIDER', ' - PLANTA'):
        if normalized.endswith(suffix):
            normalized = normalized[: -len(suffix)].strip()
            break
    return normalized


def generate_document(seed: str, used_documents: set[str]) -> str:
    digest = hashlib.sha1(seed.encode('utf-8')).hexdigest()
    digits = ''.join(str(int(char, 16) % 10) for char in digest)
    candidate = '9' + digits[:9]
    counter = 1
    while candidate in used_documents:
        suffix = str(counter)
        candidate = ('9' + digits[: 9 - len(suffix)] + suffix)[:10]
        counter += 1
    return candidate


def generate_email(document: str, used_emails: set[str]) -> str:
    base = f'sin-correo-{document}@import.local'
    if base not in used_emails:
        return base
    counter = 2
    while True:
        candidate = f'sin-correo-{document}-{counter}@import.local'
        if candidate not in used_emails:
            return candidate
        counter += 1


class Command(BaseCommand):
    help = 'Importa equipos y usuarios desde db/equipos_javier.csv. Dry-run por defecto; usa --apply para persistir.'

    def add_arguments(self, parser):
        parser.add_argument('--csv', default=str(CSV_DEFAULT), help='Ruta del CSV a importar.')
        parser.add_argument('--apply', action='store_true', help='Aplica cambios en base de datos.')

    def handle(self, *args, **options):
        csv_path = Path(options['csv'])
        if not csv_path.is_absolute():
            csv_path = Path.cwd() / csv_path
        if not csv_path.exists():
            raise CommandError(f'No existe el archivo CSV: {csv_path}')

        tipo_doc = TipoDoc.objects.filter(id_tipodoc=1).first()
        if not tipo_doc:
            raise CommandError('No existe TipoDoc con id_tipodoc=1.')

        roles = {
            'instructor': Rol.objects.filter(nombre__icontains='instru').first(),
            'dinamizador': Rol.objects.filter(nombre__iexact='dinamizador').first(),
            'coordinador': Rol.objects.filter(nombre__icontains='coordinador').first(),
        }
        if not roles['instructor'] or not roles['dinamizador']:
            raise CommandError('No se encontraron los roles requeridos para instructor y dinamizador.')

        parsed_rows, parse_summary = self.parse_csv(csv_path)
        teams = self.resolve_teams(apply=options['apply'])
        result = self.import_rows(
            parsed_rows=parsed_rows,
            tipo_doc=tipo_doc,
            roles=roles,
            teams=teams,
            apply=options['apply'],
        )

        mode_label = 'APPLY' if options['apply'] else 'DRY-RUN'
        self.stdout.write(self.style.SUCCESS(f'Importacion equipos_javier [{mode_label}]'))
        self.stdout.write(f"Filas numeradas: {parse_summary['numbered_rows']}")
        self.stdout.write(f"Filas PLANTA LIDER: {parse_summary['leader_rows']}")
        self.stdout.write(f"Filas PLANTA: {parse_summary['planta_rows']}")
        self.stdout.write(f"Filas a importar: {len(parsed_rows)}")
        self.stdout.write(f"Equipos creados: {result['teams_created']}")
        self.stdout.write(f"Equipos actualizados: {result['teams_updated']}")
        self.stdout.write(f"Usuarios creados: {result['users_created']}")
        self.stdout.write(f"Usuarios actualizados: {result['users_updated']}")
        self.stdout.write(f"Usuarios sin cambios: {result['users_unchanged']}")
        self.stdout.write(f"Documentos generados: {result['generated_documents']}")
        self.stdout.write(f"Emails generados: {result['generated_emails']}")

        if parse_summary['unmapped_programs']:
            self.stdout.write(self.style.WARNING('Programas no mapeados:'))
            for item in sorted(parse_summary['unmapped_programs']):
                self.stdout.write(f'  - {item}')

        if result['warnings']:
            self.stdout.write(self.style.WARNING('Advertencias:'))
            for warning in result['warnings']:
                self.stdout.write(f'  - {warning}')

        self.stdout.write(
            'Nota: el equipo 8 usa a Javier Mauricio Palomino como referente operativo, '
            'pero el modelo actual no soporta un coordinador multi-equipo sin duplicar usuario.'
        )

    def parse_csv(self, csv_path: Path) -> tuple[list[ImportRow], dict[str, object]]:
        parsed_rows: list[ImportRow] = []
        summary = {
            'numbered_rows': 0,
            'leader_rows': 0,
            'planta_rows': 0,
            'unmapped_programs': set(),
        }

        with csv_path.open('r', encoding='utf-8-sig', newline='') as handle:
            reader = csv.reader(handle, delimiter=';')
            for line_no, row in enumerate(reader, start=1):
                row = (row + ['', '', '', '', ''])[:5]
                first, second, third, fourth, fifth = [value.strip() for value in row]

                if not any([first, second, third, fourth, fifth]):
                    continue

                normalized_second = normalize_key(second)
                if normalized_second.startswith('COORDINACION TITULADA'):
                    continue
                if normalized_second in SKIP_MARKERS:
                    continue

                if first.isdigit():
                    summary['numbered_rows'] += 1
                    team_id = TEAM_LOOKUP.get(normalize_key(second))
                    if not team_id:
                        summary['unmapped_programs'].add(second)
                        continue
                    parsed_rows.append(
                        ImportRow(
                            line_no=line_no,
                            source_kind='instructor_csv',
                            raw_program=second,
                            team_id=team_id,
                            team_name=TEAM_DEFINITIONS[team_id]['name'],
                            full_name=third,
                            raw_document=fourth,
                            raw_email=fifth,
                            role_slug='instructor',
                            tipo_contrato=0,
                        )
                    )
                    continue

                if third and 'PLANTA LIDER' in normalized_second:
                    summary['leader_rows'] += 1
                    canonical_program = strip_suffixes(second)
                    team_id = TEAM_LOOKUP.get(canonical_program)
                    if not team_id:
                        summary['unmapped_programs'].add(second)
                        continue
                    full_name = clean_name(third)
                    role_slug = 'dinamizador'
                    if normalize_key(full_name) == SANDRA_EXCLUSION:
                        role_slug = 'instructor'
                    parsed_rows.append(
                        ImportRow(
                            line_no=line_no,
                            source_kind='planta_lider',
                            raw_program=second,
                            team_id=team_id,
                            team_name=TEAM_DEFINITIONS[team_id]['name'],
                            full_name=full_name,
                            raw_document=fourth,
                            raw_email=fifth,
                            role_slug=role_slug,
                            tipo_contrato=1,
                        )
                    )
                    continue

                if third and 'PLANTA' in normalized_second:
                    summary['planta_rows'] += 1
                    canonical_program = strip_suffixes(second)
                    team_id = TEAM_LOOKUP.get(canonical_program)
                    if not team_id:
                        summary['unmapped_programs'].add(second)
                        continue
                    parsed_rows.append(
                        ImportRow(
                            line_no=line_no,
                            source_kind='planta',
                            raw_program=second,
                            team_id=team_id,
                            team_name=TEAM_DEFINITIONS[team_id]['name'],
                            full_name=third,
                            raw_document=fourth,
                            raw_email=fifth,
                            role_slug='instructor',
                            tipo_contrato=1,
                        )
                    )

        summary['unmapped_programs'] = sorted(summary['unmapped_programs'])
        return parsed_rows, summary

    def resolve_teams(self, apply: bool) -> dict[int, EquipoEjecutor | None]:
        now = timezone.now()
        existing = {normalize_key(team.nombre): team for team in EquipoEjecutor.objects.all()}
        teams: dict[int, EquipoEjecutor | None] = {}
        self._teams_created = 0
        self._teams_updated = 0

        if apply:
            for team_id, definition in TEAM_DEFINITIONS.items():
                canonical_name = definition['name']
                key = normalize_key(canonical_name)
                team = existing.get(key)
                if team:
                    changed = False
                    if team.nombre != canonical_name:
                        team.nombre = canonical_name
                        changed = True
                    if team.tipo != 1:
                        team.tipo = 1
                        changed = True
                    if changed:
                        team.save(update_fields=['nombre', 'tipo'])
                        self._teams_updated += 1
                else:
                    team = EquipoEjecutor.objects.create(
                        nombre=canonical_name,
                        tipo=1,
                        creado_en=now,
                    )
                    self._teams_created += 1
                teams[team_id] = team
        else:
            for team_id in TEAM_DEFINITIONS:
                teams[team_id] = existing.get(normalize_key(TEAM_DEFINITIONS[team_id]['name']))
        return teams

    def import_rows(
        self,
        parsed_rows: Iterable[ImportRow],
        tipo_doc: TipoDoc,
        roles: dict[str, Rol | None],
        teams: dict[int, EquipoEjecutor | None],
        apply: bool,
    ) -> dict[str, object]:
        existing_users = list(Usuario.objects.select_related('id_equipo', 'id_rol').all())
        by_document = {user.documento: user for user in existing_users if user.documento}
        by_email = {user.email.lower(): user for user in existing_users if user.email}
        by_name: dict[str, list[Usuario]] = {}
        for user in existing_users:
            by_name.setdefault(normalize_key(f'{user.nombre} {user.apellido}'), []).append(user)

        used_documents = set(by_document.keys())
        used_emails = set(by_email.keys())
        password_hash = make_password(DEFAULT_PASSWORD)
        summary = {
            'teams_created': getattr(self, '_teams_created', 0),
            'teams_updated': getattr(self, '_teams_updated', 0),
            'users_created': 0,
            'users_updated': 0,
            'users_unchanged': 0,
            'generated_documents': 0,
            'generated_emails': 0,
            'warnings': [],
        }

        def process_row(row: ImportRow):
            full_name = clean_name(row.full_name)
            normalized_name = normalize_key(full_name)
            document = clean_document(row.raw_document)
            email = clean_email(row.raw_email)

            user = None
            if document and document in by_document:
                user = by_document[document]
            elif email and email in by_email:
                user = by_email[email]
            else:
                candidates = by_name.get(normalized_name, [])
                if len(candidates) == 1:
                    user = candidates[0]

            if user is None:
                if not document:
                    document = generate_document(f'{normalized_name}-{row.line_no}', used_documents)
                    summary['generated_documents'] += 1
                elif document in used_documents:
                    document = generate_document(f'{normalized_name}-{row.line_no}-{document}', used_documents)
                    summary['generated_documents'] += 1

                if not email or email in used_emails:
                    email = generate_email(document, used_emails)
                    summary['generated_emails'] += 1
            else:
                if not document:
                    document = user.documento or generate_document(f'{normalized_name}-{row.line_no}', used_documents)
                    if document != user.documento:
                        summary['generated_documents'] += 1
                if not email:
                    email = user.email or generate_email(document, used_emails)
                    if email != user.email:
                        summary['generated_emails'] += 1
                elif email in used_emails and email != user.email.lower():
                    email = generate_email(document, used_emails)
                    summary['generated_emails'] += 1

            used_documents.add(document)
            used_emails.add(email)
            first_name, last_name = split_name(full_name)
            role = roles[row.role_slug]
            team = teams[row.team_id]
            if apply and team is None:
                raise CommandError(f'No se pudo resolver el equipo {row.team_name}.')

            if row.tipo_contrato == 1:
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
                if apply:
                    user = Usuario.objects.create(
                        nombre=first_name,
                        apellido=last_name,
                        documento=document,
                        id_tipodoc=tipo_doc,
                        id_rol=role,
                        id_equipo=team,
                        tipo_contrato=row.tipo_contrato,
                        activo=True,
                        email=email,
                        contrasena=password_hash,
                        horas_max_mensual=horas_max_mensual,
                        horas_objetivo_anual=horas_objetivo_anual,
                        horas_min_mensual=horas_min_mensual,
                        horas_min_anual=horas_min_anual,
                        creado_en=timezone.now(),
                    )
                    by_document[document] = user
                    by_email[email] = user
                    by_name.setdefault(normalized_name, []).append(user)
                return

            changed_fields = []
            updates = {
                'nombre': first_name,
                'apellido': last_name,
                'documento': document,
                'id_tipodoc': tipo_doc,
                'id_rol': role,
                'id_equipo': team,
                'tipo_contrato': row.tipo_contrato,
                'activo': True,
                'email': email,
                'contrasena': password_hash,
                'horas_max_mensual': horas_max_mensual,
                'horas_objetivo_anual': horas_objetivo_anual,
                'horas_min_mensual': horas_min_mensual,
                'horas_min_anual': horas_min_anual,
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
            else:
                summary['users_unchanged'] += 1

        if apply:
            with transaction.atomic():
                for row in parsed_rows:
                    process_row(row)
        else:
            for row in parsed_rows:
                process_row(row)

        existing_coordinator = Usuario.objects.filter(
            id_rol=roles['coordinador'],
            nombre__iexact='Javier Mauricio',
            apellido__icontains='Palomino',
        ).first()
        if existing_coordinator is None:
            summary['warnings'].append(
                f'No se encontró al coordinador {COORDINADOR_COMPLEMENTARIOS}; el equipo 8 quedará sin referente explícito en el modelo.'
            )

        return summary
