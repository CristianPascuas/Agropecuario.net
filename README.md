# agrepecuario.net — Sistema de Programación Académica SENA

Sistema web para la gestión y programación académica de fichas de formación del **SENA**, orientado a digitalizar y controlar el proceso de radicación, programación mensual de competencias y seguimiento por resultados de aprendizaje de los instructores SENA.

## Características principales

- Autenticación por sesión con control de roles (administrador, coordinador, dinamizador, instructor)
- Gestión de fichas de formación, programas, competencias y resultados de aprendizaje
- Programación mensual de fichas por resultado
- Radicación de solicitudes con seguimiento de estado
- Panel por rol con vistas diferenciadas
- API interna para operaciones de programación vía JSON
- Backend MySQL compatible con MariaDB mediante driver personalizado (`db_backends/mysql_compat`)

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | Django 5.2.8 |
| Base de datos | MySQL / MariaDB |
| Driver DB | PyMySQL 1.1.2 + backend personalizado |
| Plantillas | Django Templates (HTML) |
| Idioma / Zona | `es-co` / `America/Bogota` |

## Requisitos previos

- Python 3.11+
- MySQL 8+ o MariaDB 10.6+
- WAMP / XAMPP o servidor MySQL local

---

## Instalación

### 1. Clonar e instalar dependencias

```bash
git clone <url-del-repositorio>
cd agrepecuario.net

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

### 2. Crear la base de datos

Importar el script SQL incluido en el proyecto:

```bash
mysql -u root -p < "db/agrepecuario_net V5.sql"
```

### 3. Configurar variables de entorno

Crear un archivo `.env` en la raíz (o definir las variables directamente). Los valores por defecto están orientados a desarrollo local:

```
DB_NAME=agrepecuario_net
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=cambia_esto_en_produccion
```

> En `settings.py` se leen automáticamente con `os.getenv()`; si no se definen, usa los valores predeterminados locales.

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Iniciar el servidor

```bash
python manage.py runserver
```

Acceder en: `http://127.0.0.1:8000`

---

## Estructura de la aplicación

| Módulo | Responsabilidad |
|--------|----------------|
| `academico/` | Modelos principales, autenticación, registro/login |
| `portal/` | Portal por roles, lógica de sesión, vistas de cada perfil |
| `programacion/` | Programación mensual de fichas por resultado y API interna |
| `radicados/` | Creación y seguimiento de radicados |
| `consultas/` | Consultas y reportes |
| `config/` | Configuración Django (settings, URLs raíz, WSGI/ASGI) |
| `db_backends/` | Backend MySQL/MariaDB personalizado para compatibilidad |

## Roles del sistema

| Rol | Acceso |
|-----|--------|
| Administrador | Gestión completa: usuarios, equipos, curricular, reportes |
| Coordinador | Fichas de su equipo, programaciones, reportes |
| Dinamizador | Programación mensual de fichas asignadas |
| Instructor | Visualización de programaciones propias y radicados |

## Seguridad

- La `SECRET_KEY` por defecto es solo para desarrollo. **Reemplazarla siempre en producción.**
- `DEBUG = True` solo en desarrollo; desactivar en producción y configurar `ALLOWED_HOSTS`.
- Las credenciales de base de datos deben gestionarse mediante variables de entorno, nunca en el código fuente.
 