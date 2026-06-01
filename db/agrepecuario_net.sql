-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-03-2026 a las 17:10:34
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `agrepecuario_net`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ambiente`
--

CREATE TABLE `ambiente` (
  `id_ambiente` int(11) NOT NULL,
  `ambiente` varchar(120) NOT NULL,
  `lugar` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ambiente`
--

INSERT INTO `ambiente` (`id_ambiente`, `ambiente`, `lugar`) VALUES
(1, 'ambiente 1', 'sena centro '),
(2, 'ambiente 2', 'sena centro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add ambiente', 7, 'add_ambiente'),
(26, 'Can change ambiente', 7, 'change_ambiente'),
(27, 'Can delete ambiente', 7, 'delete_ambiente'),
(28, 'Can view ambiente', 7, 'view_ambiente'),
(29, 'Can add equipo ejecutor', 8, 'add_equipoejecutor'),
(30, 'Can change equipo ejecutor', 8, 'change_equipoejecutor'),
(31, 'Can delete equipo ejecutor', 8, 'delete_equipoejecutor'),
(32, 'Can view equipo ejecutor', 8, 'view_equipoejecutor'),
(33, 'Can add horario', 9, 'add_horario'),
(34, 'Can change horario', 9, 'change_horario'),
(35, 'Can delete horario', 9, 'delete_horario'),
(36, 'Can view horario', 9, 'view_horario'),
(37, 'Can add municipio', 10, 'add_municipio'),
(38, 'Can change municipio', 10, 'change_municipio'),
(39, 'Can delete municipio', 10, 'delete_municipio'),
(40, 'Can view municipio', 10, 'view_municipio'),
(41, 'Can add programa formacion', 11, 'add_programaformacion'),
(42, 'Can change programa formacion', 11, 'change_programaformacion'),
(43, 'Can delete programa formacion', 11, 'delete_programaformacion'),
(44, 'Can view programa formacion', 11, 'view_programaformacion'),
(45, 'Can add rol', 12, 'add_rol'),
(46, 'Can change rol', 12, 'change_rol'),
(47, 'Can delete rol', 12, 'delete_rol'),
(48, 'Can view rol', 12, 'view_rol'),
(49, 'Can add tipo doc', 13, 'add_tipodoc'),
(50, 'Can change tipo doc', 13, 'change_tipodoc'),
(51, 'Can delete tipo doc', 13, 'delete_tipodoc'),
(52, 'Can view tipo doc', 13, 'view_tipodoc'),
(53, 'Can add ficha', 14, 'add_ficha'),
(54, 'Can change ficha', 14, 'change_ficha'),
(55, 'Can delete ficha', 14, 'delete_ficha'),
(56, 'Can view ficha', 14, 'view_ficha'),
(57, 'Can add competencia', 15, 'add_competencia'),
(58, 'Can change competencia', 15, 'change_competencia'),
(59, 'Can delete competencia', 15, 'delete_competencia'),
(60, 'Can view competencia', 15, 'view_competencia'),
(61, 'Can add resultado', 16, 'add_resultado'),
(62, 'Can change resultado', 16, 'change_resultado'),
(63, 'Can delete resultado', 16, 'delete_resultado'),
(64, 'Can view resultado', 16, 'view_resultado'),
(65, 'Can add usuario', 17, 'add_usuario'),
(66, 'Can change usuario', 17, 'change_usuario'),
(67, 'Can delete usuario', 17, 'delete_usuario'),
(68, 'Can view usuario', 17, 'view_usuario'),
(69, 'Can add programacion', 18, 'add_programacion'),
(70, 'Can change programacion', 18, 'change_programacion'),
(71, 'Can delete programacion', 18, 'delete_programacion'),
(72, 'Can view programacion', 18, 'view_programacion'),
(73, 'Can add equipo programa', 19, 'add_equipoprograma'),
(74, 'Can change equipo programa', 19, 'change_equipoprograma'),
(75, 'Can delete equipo programa', 19, 'delete_equipoprograma'),
(76, 'Can view equipo programa', 19, 'view_equipoprograma');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `competencia`
--

CREATE TABLE `competencia` (
  `id_competencia` int(11) NOT NULL,
  `codigo` varchar(30) NOT NULL,
  `id_programa_formacion` int(11) NOT NULL,
  `nombre` varchar(180) NOT NULL,
  `tipo_competencia` enum('tecnica','trasversal') NOT NULL,
  `horas_max` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `competencia`
--

INSERT INTO `competencia` (`id_competencia`, `codigo`, `id_programa_formacion`, `nombre`, `tipo_competencia`, `horas_max`) VALUES
(1, '220201501', 1, 'APLICACIÓN DE CONOCIMIENTOS DE LAS CIENCIAS NATURALES DE ACUERDO CON\nSITUACIONES DEL CONTEXTO PRODUCTIVO Y SOCIAL', 'trasversal', 48),
(2, '220601501', 1, 'APLICAR PRÁCTICAS  DE PROTECCIÓN AMBIENTAL, SEGURIDAD Y SALUD EN EL TRABAJO\r\nDE ACUERDO CON LAS POLÍTICAS ORGANIZACIONALES  Y LA NORMATIVIDAD VIGENTE.', 'trasversal', 48),
(3, '220501098', 1, 'Controlar la calidad del servicio de software de acuerdo con los estándares técnicos\r\n', 'tecnica', 144),
(4, '220501096', 1, 'DESARROLLAR LA SOLUCIÓN DE SOFTWARE DE ACUERDO CON EL DISEÑO Y\r\nMETODOLOGÍAS DE DESARROLL', 'tecnica', 1008),
(5, '220501095', 1, 'Diseñar la solución de software de acuerdo con procedimientos y requisitos técnicos\r\n', 'tecnica', 336),
(6, '210201501', 1, 'Ejercer derechos fundamentales del trabajo en el marco de la constitución política y los convenios\r\ninternacionales.', 'trasversal', 48),
(7, '240201526', 1, 'Enrique Low Murtra-Interactuar en el contexto productivo y social de acuerdo con principios  éticos\r\npara la construcción de una cultura de paz.', 'trasversal', 48),
(8, '220501092', 1, 'Establecer requisitos de la solución de software de acuerdo con estándares y procedimiento técnico\r\n', 'tecnica', 144),
(9, '220501094', 1, 'Estructurar propuesta técnica de servicio de tecnología de la información según requisitos técnicos y normativa', 'tecnica', 144),
(10, '220501093', 1, 'Evaluar requisitos de la solución de software de acuerdo con metodologías de análisis y estándares\r\n', 'tecnica', 288),
(11, '230101507', 1, 'GENERAR HÁBITOS SALUDABLES DE VIDA MEDIANTE LA APLICACIÓN DE PROGRAMAS DE \r\nACTIVIDAD FÍSICA EN LOS CONTEXTOS PRODUCTIVOS Y SOCIALES', 'trasversal', 48),
(12, '240201529', 1, 'Gestionar procesos propios de la cultura emprendedora y empresarial de acuerdo con el perfil\r\npersonal y los requerimientos de los contextos productivo y social', 'trasversal', 48),
(13, '220501097', 1, 'Implementar la solución de software de acuerdo con los requisitos de operación y modelos de referencia', 'tecnica', 144),
(14, '240202501', 1, 'INTERACTUAR EN LENGUA INGLESA DE FORMA ORAL Y ESCRITA DENTRO DE CONTEXTOS\r\nSOCIALES Y LABORALES SEGÚN LOS CRITERIOS ESTABLECIDOS POR EL MARCO COMÚN\r\nEUROPEO DE REFERENCIA PARA LAS ', 'trasversal', 384),
(15, '240201064', 1, 'Orientar investigación formativa según referentes técnicos\r\n', 'trasversal', 48),
(16, '240201528', 1, 'Razonar cuantitativamente frente a situaciones susceptibles de ser abordadas de manera matemática\r\nen contextos laborales, sociales y personales.', 'trasversal', 48),
(17, '240201530', 1, 'Resultado de Aprendizaje de la Inducción.', 'trasversal', 48),
(18, '220501046', 1, 'Utilizar herramientas informáticas de acuerdo con las necesidades de manejo de información\r\n', 'trasversal', 48),
(19, '220601501', 2, 'APLICAR PRÁCTICAS  DE PROTECCIÓN AMBIENTAL, SEGURIDAD Y SALUD EN EL TRABAJO\r\nDE ACUERDO CON LAS POLÍTICAS ORGANIZACIONALES  Y LA NORMATIVIDAD VIGENTE.', 'trasversal', 48),
(20, '240201524', 2, 'DESARROLLAR PROCESOS DE COMUNICACIÓN EFICACES Y EFECTIVOS, TENIENDO EN\r\nCUENTA SITUACIONES  DE ORDEN SOCIAL, PERSONAL Y PRODUCTIVO', 'trasversal', 48),
(21, '210201501', 2, 'Ejercer derechos fundamentales del trabajo en el marco de la constitución política y los convenios\r\ninternacionales.', 'trasversal', 48),
(22, '240201526', 2, 'Enrique Low Murtra-Interactuar en el contexto productivo y social de acuerdo con principios  éticos\r\npara la construcción de una cultura de paz', 'trasversal', 48),
(23, '280102129', 2, 'Evaluar red de acuerdo con procedimientos de telecomunicaciones y normativa técnica\r\n', 'tecnica', 336),
(24, '240201533', 2, 'Fomentar cultura emprendedora según habilidades y competencias personales\r\n', 'trasversal', 48),
(25, '230101507', 2, 'GENERAR HÁBITOS SALUDABLES DE VIDA MEDIANTE LA APLICACIÓN DE PROGRAMAS DE\r\nACTIVIDAD FÍSICA EN LOS CONTEXTOS PRODUCTIVOS Y SOCIALES', 'trasversal', 48),
(26, '240202501', 2, 'INTERACTUAR EN LENGUA INGLESA DE FORMA ORAL Y ESCRITA DENTRO DE CONTEXTOS\r\nSOCIALES Y LABORALES SEGÚN LOS CRITERIOS ESTABLECIDOS POR EL MARCO COMÚN\r\nEUROPEO DE REFERENCIA PARA LAS ', 'trasversal', 192),
(27, '220501001', 2, 'Mantener equipos de cómputo según procedimiento técnico\r\n', 'tecnica', 336),
(28, '220501121', 2, 'Operar herramientas informáticas y digitales de acuerdo con protocolos y manuales técnicos\r\n', 'tecnica', 240),
(29, '240201530', 2, 'Resultado de Aprendizaje de la Inducción.\r\n', 'trasversal', 48);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'academico', 'ambiente'),
(15, 'academico', 'competencia'),
(8, 'academico', 'equipoejecutor'),
(19, 'academico', 'equipoprograma'),
(14, 'academico', 'ficha'),
(9, 'academico', 'horario'),
(10, 'academico', 'municipio'),
(18, 'academico', 'programacion'),
(11, 'academico', 'programaformacion'),
(16, 'academico', 'resultado'),
(12, 'academico', 'rol'),
(13, 'academico', 'tipodoc'),
(17, 'academico', 'usuario'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'academico', '0001_initial', '2026-03-09 13:57:29.983493'),
(2, 'contenttypes', '0001_initial', '2026-03-09 13:57:30.136925'),
(3, 'auth', '0001_initial', '2026-03-09 13:57:30.477536'),
(4, 'admin', '0001_initial', '2026-03-09 13:57:30.579336'),
(5, 'admin', '0002_logentry_remove_auto_add', '2026-03-09 13:57:30.585996'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-09 13:57:30.594044'),
(7, 'contenttypes', '0002_remove_content_type_name', '2026-03-09 13:57:30.661934'),
(8, 'auth', '0002_alter_permission_name_max_length', '2026-03-09 13:57:30.700485'),
(9, 'auth', '0003_alter_user_email_max_length', '2026-03-09 13:57:30.713801'),
(10, 'auth', '0004_alter_user_username_opts', '2026-03-09 13:57:30.721136'),
(11, 'auth', '0005_alter_user_last_login_null', '2026-03-09 13:57:30.757844'),
(12, 'auth', '0006_require_contenttypes_0002', '2026-03-09 13:57:30.759865'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2026-03-09 13:57:30.767155'),
(14, 'auth', '0008_alter_user_username_max_length', '2026-03-09 13:57:30.781932'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2026-03-09 13:57:30.791872'),
(16, 'auth', '0010_alter_group_name_max_length', '2026-03-09 13:57:30.805013'),
(17, 'auth', '0011_update_proxy_permissions', '2026-03-09 13:57:30.819572'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2026-03-09 13:57:30.829503'),
(19, 'sessions', '0001_initial', '2026-03-09 13:57:30.858562');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('tg0zzco7xnje9tf3mvhdc24bo4s3h4wa', 'e30:1vzcAI:alXHmDFJ6Tkmu2hkZggbv_Q8YaJbueo4_594Q2_yiOw', '2026-03-23 15:05:02.836085');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo_ejecutor`
--

CREATE TABLE `equipo_ejecutor` (
  `id_equipo` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipo_ejecutor`
--

INSERT INTO `equipo_ejecutor` (`id_equipo`, `nombre`, `activo`, `creado_en`) VALUES
(1, 'Equipo Ejecutor 1', 1, '2026-03-05 01:59:11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo_programa`
--

CREATE TABLE `equipo_programa` (
  `id_equipo_programa` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `id_programa_formacion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `equipo_programa`
--

INSERT INTO `equipo_programa` (`id_equipo_programa`, `id_equipo`, `id_programa_formacion`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha`
--

CREATE TABLE `ficha` (
  `codigo_ficha` int(11) NOT NULL,
  `id_programa_formacion` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `id_horario` int(11) DEFAULT NULL,
  `tipo_ficha` varchar(40) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `codigo_municipio` int(11) NOT NULL,
  `id_ambiente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `id_horario` int(11) NOT NULL,
  `horario` varchar(120) NOT NULL,
  `horas` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horario`
--

INSERT INTO `horario` (`id_horario`, `horario`, `horas`) VALUES
(1, 'mañana', 30),
(2, 'tarde', 30),
(3, 'noche', 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `municipio`
--

CREATE TABLE `municipio` (
  `codigo_municipio` int(11) NOT NULL,
  `municipio` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `municipio`
--

INSERT INTO `municipio` (`codigo_municipio`, `municipio`) VALUES
(19001, 'popayan'),
(19809, 'timbio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion`
--

CREATE TABLE `programacion` (
  `id_programacion` int(11) NOT NULL,
  `codigo_ficha` int(11) NOT NULL,
  `id_competencia` int(11) NOT NULL,
  `id_instructor` int(11) NOT NULL,
  `id_dinamizador_asignador` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programa_formacion`
--

CREATE TABLE `programa_formacion` (
  `id_programa_formacion` int(11) NOT NULL,
  `codigo` varchar(40) NOT NULL,
  `nombre` varchar(180) NOT NULL,
  `horas_max` int(11) NOT NULL,
  `horas_lectiva` int(11) NOT NULL,
  `horas_productivas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `programa_formacion`
--

INSERT INTO `programa_formacion` (`id_programa_formacion`, `codigo`, `nombre`, `horas_max`, `horas_lectiva`, `horas_productivas`) VALUES
(1, '228118', 'ANALISIS Y DESARROLLO DE SOFTWARE.\r\n', 3984, 3120, 864),
(2, '233108', 'SISTEMAS TELINFORMATICOS', 2304, 1440, 864);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultado`
--

CREATE TABLE `resultado` (
  `id_resultado` int(11) NOT NULL,
  `id_competencia` int(11) NOT NULL,
  `nombre` varchar(180) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `resultado`
--

INSERT INTO `resultado` (`id_resultado`, `id_competencia`, `nombre`) VALUES
(1, 1, 'IDENTIFICAR LOS PRINCIPIOS Y LEYES DE LA FÍSICA EN LA SOLUCIÓN DE PROBLEMAS DE ACUERDO AL\r\nCONTEXTO PRODUCTIVO.'),
(2, 1, ' SOLUCIONAR PROBLEMAS ASOCIADOS CON EL SECTOR PRODUCTIVO CON BASE EN LOS PRINCIPIOS Y\r\nLEYES DE LA FÍSICA.'),
(3, 1, 'VERIFICAR LAS TRANSFORMACIONES FÍSICAS DE LA MATERIA UTILIZANDO HERRAMIENTAS'),
(4, 1, 'PROPONER ACCIONES DE MEJORA EN LOS PROCESOS PRODUCTIVOS DE ACUERDO CON LOS PRINCIPIOS\r\nY LEYES DE LA FÍSICA.'),
(5, 2, 'ANALIZAR LAS ESTRATEGIAS PARA LA PREVENCIÓN Y CONTROL DE LOS IMPACTOS AMBIENTALES Y DE ACCIDENTES Y ENFERMEDADES LABORALES (ATEL) DE ACUERDO CON LAS POLÍTICAS ORGANIZACIONALES Y\r\nE'),
(6, 2, 'IMPLEMENTAR ESTRATEGIAS PARA EL CONTROL DE LOS IMPACTOS AMBIENTALES Y DE LOS ACCIDENTES\r\nY ENFERMEDADES   DE ACUERDO  CON LOS PLANES Y PROGRAMAS  ESTABLECIDOS POR LA ORGANIZACIÓN.'),
(7, 2, 'REALIZAR SEGUIMIENTO Y ACOMPAÑAMIENTO AL DESARROLLO DE LOS PLANES Y PROGRAMAS\r\nAMBIENTALES Y SST, SEGÚN EL  ÁREA DE DESEMPEÑO.'),
(8, 2, 'PROPONER ACCIONES DE MEJORA PARA EL MANEJO AMBIENTAL Y EL CONTROL DE LA SST, DE ACUERDO\r\nCON ESTRATEGIAS DE TRABAJO, COLABORATIVO, COOPERATIVO Y COORDINADO EN EL CONTEXTO\r\nPRODUCTI'),
(9, 3, 'INCORPORAR ACTIVIDADES DE ASEGURAMIENTO DE LA CALIDAD DEL SOFTWARE DE ACUERDO CON\r\nESTÁNDARES DE LA INDUSTRIA.'),
(10, 3, 'VERIFICAR LA CALIDAD DEL SOFTWARE DE ACUERDO CON LAS PRÁCTICAS ASOCIADAS EN LOS\r\nPROCESOS DE DESARROLLO.'),
(11, 3, 'REALIZAR ACTIVIDADES DE MEJORA DE LA CALIDAD DEL SOFTWARE A PARTIR DE LOS RESULTADOS DE LA\r\nVERIFICACIÓN.'),
(12, 4, 'PLANEAR ACTIVIDADES DE CONSTRUCCIÓN DEL SOFTWARE DE ACUERDO CON EL DISEÑO ESTABLECIDO.\r\n'),
(13, 4, 'CONSTRUIR LA BASE DE DATOS PARA EL SOFTWARE A PARTIR DEL MODELO DE DATOS.\r\n'),
(14, 4, 'CREAR COMPONENTES FRONT-END DEL SOFTWARE DE ACUERDO CON EL DISEÑO.\r\n'),
(15, 4, 'CODIFICAR EL SOFTWARE DE ACUERDO CON EL DISEÑO ESTABLECIDO.\r\n'),
(16, 4, 'REALIZAR PRUEBAS AL SOFTWARE PARA VERIFICAR SU FUNCIONALIDAD.\r\n'),
(17, 5, 'ELABORAR LOS ARTEFACTOS DE DISEÑO DEL SOFTWARE SIGUIENDO LAS PRÁCTICAS DE LA\r\nMETODOLOGÍA SELECCIONADA.'),
(18, 5, 'ESTRUCTURAR EL MODELO DE DATOS DEL SOFTWARE DE ACUERDO CON LAS ESPECIFICACIONES DEL\r\nANÁLISIS.'),
(19, 5, 'DETERMINAR LAS CARACTERÍSTICAS TÉCNICAS DE LA INTERFAZ GRÁFICA DEL SOFTWARE ADOPTANDO\r\nESTÁNDARES.'),
(20, 5, 'VERIFICAR LOS ENTREGABLES DE LA FASE DE DISEÑO DEL SOFTWARE DE ACUERDO CON LO\r\nESTABLECIDO EN EL INFORME DE ANÁLISIS.'),
(21, 6, 'Reconocer el trabajo como factor de movilidad social y transformación vital con referencia a la fenomenología y a los\r\nderechos fundamentales en el trabajo.'),
(22, 6, 'Valorar la importancia de la ciudadanía laboral con base en el estudio de los derechos humanos y fundamentales en el\r\ntrabajo.'),
(23, 6, 'Practicar los derechos fundamentales en el trabajo de acuerdo con la Constitución Política y los Convenios\r\nInternacionales.'),
(24, 6, 'Participar en acciones solidarias teniendo en cuenta el ejercicio de los derechos humanos, de los pueblos y de la\r\nnaturaleza.'),
(25, 7, 'PROMOVER MI DIGNIDAD Y LA DEL OTRO A PARTIR DE LOS PRINCIPIOS Y VALORES ÉTICOS COMO APORTE\r\nEN LA INSTAURACIÓN DE UNA CULTURA DE PAZ.'),
(26, 7, 'ESTABLECER RELACIONES DE CRECIMIENTO PERSONAL Y COMUNITARIO A PARTIR DEL BIEN COMÚN\r\nCOMO APORTE PARA EL DESARROLLO SOCIAL.'),
(27, 7, 'PROMOVER EL USO RACIONAL DE LOS RECURSOS NATURALES A PARTIR DE CRITERIOS DE\r\nSOSTENIBILIDAD Y SUSTENTABILIDAD ÉTICA Y NORMATIVA VIGENTE.'),
(28, 7, 'CONTRIBUIR CON EL FORTALECIMIENTO DE LA CULTURA DE PAZ A PARTIR DE LA DIGNIDAD HUMANA Y LAS\r\nESTRATEGIAS PARA LA TRANSFORMACIÓN DE CONFLICTOS.'),
(29, 8, 'CARACTERIZAR LOS PROCESOS DE LA ORGANIZACIÓN DE ACUERDO CON EL SOFTWARE A CONSTRUIR.\r\n'),
(30, 8, 'RECOLECTAR INFORMACIÓN DEL SOFTWARE A CONSTRUIR DE ACUERDO CON LAS NECESIDADES DEL\r\nCLIENTE.'),
(31, 8, 'ESTABLECER LOS REQUISITOS DEL SOFTWARE DE ACUERDO CON LA INFORMACIÓN RECOLECTADA.\r\n'),
(32, 8, 'VALIDAR EL INFORME DE REQUISITOS DE ACUERDO CON LAS NECESIDADES DEL CLIENTE.\r\n'),
(33, 9, 'DEFINIR ESPECIFICACIONES TÉCNICAS DEL SOFTWARE DE ACUERDO CON LAS CARACTERÍSTICAS DEL\r\nSOFTWARE A CONSTRUIR.'),
(34, 9, 'ELABORAR PROPUESTA TÉCNICA DEL SOFTWARE DE ACUERDO CON LAS ESPECIFICACIONES TÉCNICAS\r\nDEFINIDAS.'),
(35, 9, 'VALIDAR LAS CONDICIONES DE LA PROPUESTA TÉCNICA DEL SOFTWARE DE ACUERDO CON LOS\r\nINTERESES DE LAS PARTES.'),
(36, 10, 'PLANEAR ACTIVIDADES DE ANÁLISIS DE ACUERDO CON LA METODOLOGÍA SELECCIONADA.\r\n'),
(37, 10, 'MODELAR LAS FUNCIONES DEL SOFTWARE DE ACUERDO CON EL INFORME DE REQUISITOS.\r\n'),
(38, 10, 'DESARROLLAR PROCESOS LÓGICOS A TRAVÉS DE LA IMPLEMENTACIÓN DE ALGORITMOS.\r\n'),
(39, 10, 'VERIFICAR LOS MODELOS REALIZADOS EN LA FASE DE ANÁLISIS DE ACUERDO CON LO ESTABLECIDO EN\r\nEL INFORME DE REQUISITOS.'),
(40, 11, 'DESARROLLAR HABILIDADES PSICOMOTRICES EN EL CONTEXTO PRODUCTIVO Y SOCIAL.\r\n'),
(41, 11, 'PRACTICAR HÁBITOS SALUDABLES MEDIANTE LA APLICACIÓN DE  FUNDAMENTOS DE NUTRICIÓN E\r\n'),
(42, 11, 'EJECUTAR ACTIVIDADES DE ACONDICIONAMIENTO FÍSICO ORIENTADAS HACIA EL MEJORAMIENTO DE LA\r\nCONDICIÓN FÍSICA EN LOS CONTEXTOS PRODUCTIVO Y SOCIAL.'),
(43, 11, 'IMPLEMENTAR UN PLAN DE ERGONOMÍA Y PAUSAS ACTIVAS SEGÚN LAS CARACTERÍSTICAS DE LA\r\nFUNCIÓN PRODUCTIVA.'),
(44, 12, 'INTEGRAR ELEMENTOS DE LA CULTURA EMPRENDEDORA TENIENDO EN CUENTA EL PERFIL PERSONAL Y\r\nEL CONTEXTO DE DESARROLLO SOCIAL.'),
(45, 12, 'CARACTERIZAR LA IDEA DE NEGOCIO TENIENDO EN CUENTA LAS OPORTUNIDADES Y NECESIDADES DEL\r\nSECTOR PRODUCTIVO Y SOCIAL.'),
(46, 12, 'ESTRUCTURAR EL PLAN DE NEGOCIO DE ACUERDO CON LAS CARACTERÍSTICAS EMPRESARIALES Y\r\nTENDENCIAS DE MERCADO.'),
(47, 12, 'VALORAR LA PROPUESTA DE NEGOCIO CONFORME CON SU ESTRUCTURA Y NECESIDADES DEL SECTOR\r\nPRODUCTIVO Y SOCIAL.'),
(48, 13, 'PLANEAR ACTIVIDADES DE IMPLANTACIÓN DEL SOFTWARE DE ACUERDO CON LAS CONDICIONES DEL\r\nSISTEMA.'),
(49, 13, 'DESPLEGAR EL SOFTWARE DE ACUERDO CON LA ARQUITECTURA Y LAS POLÍTICAS ESTABLECIDAS.\r\n'),
(50, 13, 'DOCUMENTAR EL PROCESO DE IMPLANTACIÓN DE SOFTWARE SIGUIENDO ESTÁNDARES DE CALIDAD.\r\n'),
(51, 13, 'IMPLANTAR EL SOFTWARE DE ACUERDO CON LOS NIVELES DE SERVICIO ESTABLECIDOS CON EL CLIENTE.\r\n'),
(52, 14, 'COMPRENDER INFORMACIÓN SOBRE SITUACIONES COTIDIANAS Y LABORALES ACTUALES Y FUTURAS A\r\nTRAVÉS DE INTERACCIONES SOCIALES DE FORMA ORAL Y ESCRITA.'),
(53, 14, 'INTERCAMBIAR OPINIONES SOBRE SITUACIONES COTIDIANAS Y LABORALES ACTUALES, PASADAS Y\r\nFUTURAS EN CONTEXTOS SOCIALES ORALES Y ESCRITOS.'),
(54, 14, 'DISCUTIR SOBRE POSIBLES SOLUCIONES A PROBLEMAS DENTRO DE UN RANGO VARIADO DE CONTEXTOS\r\nSOCIALES Y LABORALES.'),
(55, 14, 'IMPLEMENTAR ACCIONES DE MEJORA RELACIONADAS CON EL USO DE EXPRESIONES, ESTRUCTURAS Y\r\nDESEMPEÑO SEGÚN LOS RESULTADOS DE APRENDIZAJE FORMULADOS PARA EL PROGRAMA.'),
(56, 14, 'PRESENTAR UN PROCESO PARA LA REALIZACIÓN DE UNA ACTIVIDAD EN SU QUEHACER LABORAL DE\r\nACUERDO CON LOS PROCEDIMIENTOS ESTABLECIDOS DESDE SU PROGRAMA DE FORMACIÓN.'),
(57, 14, 'EXPLICAR LAS FUNCIONES DE SU OCUPACIÓN LABORAL USANDO EXPRESIONES DE ACUERDO AL NIVEL\r\nREQUERIDO POR EL PROGRAMA DE FORMACIÓN.'),
(58, 14, 'ANALIZAR EL CONTEXTO PRODUCTIVO SEGÚN SUS CARACTERÍSTICAS Y NECESIDADES.\r\n'),
(59, 15, 'ESTRUCTURAR EL PROYECTO DE ACUERDO A CRITERIOS DE LA INVESTIGACIÓN.\r\n'),
(60, 15, 'ARGUMENTAR ASPECTOS TEÓRICOS DEL PROYECTO SEGÚN REFERENTES NACIONALES E\r\n'),
(61, 15, 'PROPONER SOLUCIONES A LAS NECESIDADES DEL CONTEXTO SEGÚN RESULTADOS DE LA\r\n'),
(62, 16, 'IDENTIFICAR MODELOS MATEMÁTICOS DE ACUERDO CON LOS REQUERIMIENTOS DEL PROBLEMA\r\nPLANTEADO  EN CONTEXTOS SOCIALES Y PRODUCTIVO.'),
(63, 16, 'PLANTEAR PROBLEMAS MATEMÁTICOS A PARTIR DE SITUACIONES GENERADAS EN EL CONTEXTO SOCIAL\r\nY PRODUCTIVO.'),
(64, 16, 'RESOLVER PROBLEMAS MATEMÁTICOS A PARTIR DE SITUACIONES GENERADAS EN EL CONTEXTO SOCIAL\r\nY PRODUCTIVO.'),
(65, 15, 'PROPONER ACCIONES DE MEJORA FRENTE A LOS RESULTADOS DE LOS PROCEDIMIENTOS MATEMÁTICOS\r\nDE ACUERDO CON EL PROBLEMA PLANTEADO.'),
(66, 17, 'IDENTIFICAR LA DINÁMICA ORGANIZACIONAL DEL SENA Y EL ROL DE LA FORMACIÓN PROFESIONAL\r\nINTEGRAL DE ACUERDO CON SU PROYECTO DE VIDA Y EL DESARROLLO PROFESIONAL.'),
(67, 18, 'ALISTAR HERRAMIENTAS DE TECNOLOGÍAS DE LA INFORMACIÓN Y LA COMUNICACIÓN (TIC), DE ACUERDO\r\nCON LAS NECESIDADES DE PROCESAMIENTO DE INFORMACIÓN Y COMUNICACIÓN.'),
(68, 18, 'APLICAR FUNCIONALIDADES DE HERRAMIENTAS Y SERVICIOS TIC, DE ACUERDO CON MANUALES DE USO,\r\nPROCEDIMIENTOS ESTABLECIDOS Y BUENAS PRÁCTICAS.'),
(69, 18, 'EVALUAR LOS RESULTADOS, DE ACUERDO CON LOS REQUERIMIENTOS.\r\n'),
(70, 18, 'OPTIMIZAR LOS RESULTADOS, DE ACUERDO CON LA VERIFICACIÓN.\r\n'),
(71, 19, 'VERIFICAR LAS CONDICIONES AMBIENTALES Y DE SST ACORDE CON LOS LINEAMIENTOS ESTABLECIDOS\r\nPARA EL ÁREA DE DESEMPEÑO LABORAL.'),
(72, 19, 'REPORTAR LAS CONDICIONES Y ACTOS QUE AFECTEN LA PROTECCIÓN DEL MEDIO AMBIENTE Y LA SST, DE\r\nACUERDO CON LOS LINEAMIENTOS ESTABLECIDOS EN EL CONTEXTO ORGANIZACIONAL Y SOCIAL.'),
(73, 19, 'EFECTUAR LAS ACCIONES PARA LA PREVENCIÓN Y CONTROL DE LA PROBLEMÁTICA AMBIENTAL Y DE SST,\r\nTENIENDO EN CUENTA LOS PROCEDIMIENTOS ESTABLECIDOS POR LA ORGANIZACIÓN.'),
(74, 19, 'INTERPRETAR LOS PROBLEMAS AMBIENTALES Y DE SST TENIENDO EN CUENTA LOS PLANES Y PROGRAMAS\r\nESTABLECIDOS POR LA ORGANIZACIÓN Y EL ENTORNO SOCIAL.'),
(75, 20, 'INTERPRETAR EL SENTIDO DE LA COMUNICACIÓN COMO MEDIO DE EXPRESIÓN SOCIAL, CULTURAL, LABORAL\r\nY ARTÍSTICA.'),
(76, 20, 'VALIDAR LA IMPORTANCIA DE LOS PROCESOS COMUNICATIVOS TENIENDO EN CUENTA CRITERIOS DE LÓGICA\r\nY RACIONALIDAD'),
(77, 20, 'DECODIFICAR MENSAJES COMUNICATIVOS EN SITUACIONES DE LA VIDA SOCIAL Y LABORAL, TENIENDO EN\r\nCUENTA EL CONTEXTO DE LA COMUNICACIÓN.'),
(78, 20, 'APLICAR ACCIONES DE MEJORAMIENTO EN EL DESARROLLO DE PROCESOS COMUNICATIVOS SEGÚN\r\nREQUERIMIENTOS DEL CONTEXTO.'),
(79, 21, 'RECONOCER EL TRABAJO COMO FACTOR DE MOVILIDAD SOCIAL Y TRANSFORMACIÓN VITAL CON\r\nREFERENCIA A LA FENOMENOLOGÍA Y A LOS DERECHOS FUNDAMENTALES EN EL TRABAJO (12)'),
(80, 21, 'VALORAR LA IMPORTANCIA DE LA CIUDADANÍA LABORAL CON BASE EN EL ESTUDIO DE LOS DERECHOS\r\nHUMANOS Y FUNDAMENTALES EN EL TRABAJO. (3)'),
(81, 21, 'PRACTICAR LOS DERECHOS FUNDAMENTALES EN EL TRABAJO DE ACUERDO CON LA CONSTITUCIÓN\r\nPOLÍTICA Y LOS CONVENIOS INTERNACIONALES. (4-5)'),
(82, 21, 'PARTICIPAR EN ACCIONES SOLIDARIAS TENIENDO EN CUENTA EL EJERCICIO DE LOS DERECHOS\r\nHUMANOS, DE LOS PUEBLOS Y DE LA NATURALEZA. (6)'),
(83, 22, 'CONTRIBUIR CON EL FORTALECIMIENTO DE LA CULTURA DE PAZ A PARTIR DE LA DIGNIDAD HUMANA Y LAS\r\nESTRATEGIAS PARA LA TRANSFORMACIÓN DE CONFLICTOS'),
(84, 22, 'PROMOVER EL USO RACIONAL DE LOS RECURSOS NATURALES A PARTIR DE CRITERIOS DE SOSTENIBILIDAD\r\nY'),
(85, 22, 'PROMOVER MI DIGNIDAD Y LA DEL OTRO A PARTIR DE LOS PRINCIPIOS Y VALORES ÉTICOS COMO APORTE EN\r\nLA'),
(86, 22, 'ESTABLECER RELACIONES DE CRECIMIENTO PERSONAL Y COMUNITARIO A PARTIR DEL BIEN COMÚN COMO\r\nAPORTE PARA EL DESARROLLO SOCIAL.'),
(87, 23, 'DEFINIR LOS PARÁMETROS Y RECURSOS DE LA RED DE ACUERDO CON NORMATIVA DE\r\nTELECOMUNICACIONES'),
(88, 23, 'COMPROBAR LA CONECTIVIDAD DE LA RED, DE ACUERDO CON NORMATIVA DE\r\nTELECOMUNICACIONES Y ORDEN DE TRABAJO'),
(89, 23, 'DOCUMENTAR LAS ACCIONES REALIZADAS EN LA RED DE ACUERDO CON LA NORMATIVA\r\n'),
(90, 24, 'ESTABLECER CARACTERÍSTICAS Y COMPETENCIAS EMPRENDEDORAS PERSONALES DE ACUERDO CON\r\nSUS POTENCIALIDADES, OBJETIVOS Y EL ENTORNO.'),
(91, 24, 'APROPIAR EL PROCESO DE TOMA DE DECISIONES PERSONALES EN SU COTIDIANIDAD, SEGÚN EL\r\nCOMPORTAMIENTO EMPRENDEDOR'),
(92, 24, 'EMPLEAR CAPACIDAD CREATIVA E INNOVADORA SEGÚN ESTRATEGIA EMPRENDEDORA.\r\n'),
(93, 24, 'RELACIONAR LA IMPORTANCIA DE LA NEGOCIACIÓN CON EL EMPRENDIMIENTO SEGÚN LAS NECESIDADES\r\nY ELEMENTOS DE LA NEGOCIACIÓN.'),
(94, 25, 'PRACTICAR HÁBITOS SALUDABLES MEDIANTE LA APLICACIÓN DE FUNDAMENTOS DE NUTRICIÓN E HIGIENE.\r\n'),
(95, 25, 'IMPLEMENTAR UN PLAN DE ERGONOMÍA Y PAUSAS ACTIVAS SEGÚN LAS CARACTERÍSTICAS DE LA FUNCIÓN\r\nPRODUCTIVA.'),
(96, 25, 'DESARROLLAR HABILIDADES PSICOMOTRICES EN EL CONTEXTO PRODUCTIVO Y SOCIAL.\r\n'),
(97, 25, 'EJECUTAR ACTIVIDADES DE ACONDICIONAMIENTO FÍSICO ORIENTADAS HACIA EL MEJORAMIENTO DE LA\r\nCONDICIÓN FÍSICA EN LOS CONTEXTOS PRODUCTIVO Y SOCIAL.'),
(98, 26, 'COMPRENDER INFORMACIÓN BÁSICA, ORAL Y ESCRITA, EN INGLÉS ACERCA DE SÍ MISMO, DE LAS\r\nPERSONAS Y DE SU CONTEXTO INMEDIATO EN REALIDADES PRESENTES'),
(99, 26, 'DESCRIBIR DE FORMA ORAL Y ESCRITA, EN INGLÉS BÁSICO, PERSONAS, SITUACIONES Y LUGARES DE\r\nACUERDO CON SU CONTEXTO LABORAL Y PERSONAL INMEDIATO'),
(100, 26, 'PARTICIPAR EN INTERCAMBIOS CONVERSACIONALES EN INGLÉS BÁSICO, DE FORMA ORAL Y ESCRITA, EN\r\nDIFERENTES SITUACIONES SOCIALES Y LABORALES'),
(101, 26, 'COMUNICARSE CON UN VISITANTE O COLEGA DE UN CONTEXTO LABORAL COTIDIANO, DE FORMA ORAL Y ESCRITA, EN INGLÉS BÁSICO.\r\n'),
(102, 26, 'INTERCAMBIAR INFORMACIÓN BÁSICA. EN INGLÉS, SOBRE SUS EXPERIENCIAS PASADAS, EN UN\r\nCONTEXTO INMEDIATO.'),
(103, 26, 'PONER EN PRÁCTICA VOCABULARIO BÁSICO Y EXPRESIONES COMUNES DE SU ÁREA OCUPACIONAL,\r\nUSANDO FRASES SENCILLAS, EN FORMA ORAL Y ESCRITA.'),
(104, 27, 'PREPARAR EL MANTENIMIENTO DE LOS EQUIPOS DE CÓMPUTO DE ACUERDO CON PROCEDIMIENTOS\r\nTÉCNICOS Y ADMINISTRATIVOS'),
(105, 27, 'REALIZAR MANTENIMIENTO INTEGRAL DE LOS SISTEMAS DE CÓMPUTO SEGÚN PROCEDIMIENTO Y\r\nMANUALES TÉCNICOS'),
(106, 27, 'VERIFICAR LA OPERACIÓN DEL SISTEMA COMPUTACIONAL DE ACUERDO CON LOS PROCEDIMIENTOS\r\nTÉCNICOS'),
(107, 27, 'DOCUMENTAR EL MANTENIMIENTO DEL EQUIPO DE CÓMPUTO SEGÚN PROCEDIMIENTO TÉCNICO\r\n'),
(108, 28, 'CARACTERIZAR HERRAMIENTAS INFORMÁTICAS SEGÚN CONTEXTO TECNOLÓGICO DE LA\r\nORGANIZACIÓN'),
(109, 28, 'IMPLEMENTAR COMPONENTES DE LAS HERRAMIENTAS TECNOLÓGICAS SEGÚN PROCEDIMIENTOS DE\r\nLA ORGANIZACIÓN'),
(110, 28, 'PLANIFICAR LA INFORMACIÓN SEGÚN CRITERIOS DE CIBERSEGURIDAD\r\n'),
(111, 28, 'DOCUMENTAR LA GESTIÓN DE LA INFORMACIÓN DE ACUERDO A PROTOCOLOS ESTABLECIDOS\r\n'),
(112, 29, 'IDENTIFICAR LA DINÁMICA ORGANIACIONAL DEL SENA Y EL ROL DE LA FORMACIÓN PROFESIONAL INTEGRAL DE ACUERDO CON SU PROYECTO DE VIDA Y EL DESARROLLO PROFESIONAL');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id_rol` tinyint(4) NOT NULL,
  `nombre` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `nombre`) VALUES
(1, 'instrucctor'),
(2, 'dinamizador'),
(3, 'coordinador'),
(5, 'administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_doc`
--

CREATE TABLE `tipo_doc` (
  `id_tipodoc` tinyint(4) NOT NULL,
  `tipodoc` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_doc`
--

INSERT INTO `tipo_doc` (`id_tipodoc`, `tipodoc`) VALUES
(1, 'CC'),
(2, 'CE'),
(3, 'PASAPORTE');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `documento` varchar(30) NOT NULL,
  `id_tipodoc` tinyint(4) NOT NULL,
  `id_rol` tinyint(4) NOT NULL,
  `id_equipo` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `email` varchar(120) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre`, `apellido`, `documento`, `id_tipodoc`, `id_rol`, `id_equipo`, `activo`, `email`, `contrasena`, `creado_en`) VALUES
(1, 'Cris', 'Coordinador', '100000001', 1, 3, 1, 1, 'cris.coordinador@agrepecuario.net', '123456', '2026-03-05 01:54:56'),
(2, 'Cris', 'Dinamizador 1', '100000002', 1, 2, 1, 1, 'cris.dinamizador1@agrepecuario.net', '123456', '2026-03-05 01:54:56'),
(3, 'Cris', 'Dinamizador 2', '100000003', 1, 2, NULL, 1, 'cris.dinamizador2@agrepecuario.net', '123456', '2026-03-05 01:54:56'),
(4, 'Wilmer', 'Instructor', '100000004', 1, 1, 1, 1, 'wilmer@agrepecuario.net', '123456', '2026-03-05 01:54:56'),
(5, 'Moises', 'Instructor', '100000005', 1, 1, NULL, 1, 'moises@agrepecuario.net', '123456', '2026-03-05 01:54:56');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ambiente`
--
ALTER TABLE `ambiente`
  ADD PRIMARY KEY (`id_ambiente`),
  ADD UNIQUE KEY `uq_ambiente_nombre` (`ambiente`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `competencia`
--
ALTER TABLE `competencia`
  ADD PRIMARY KEY (`id_competencia`),
  ADD UNIQUE KEY `uq_competencia_codigo_programa` (`id_programa_formacion`,`codigo`),
  ADD KEY `idx_competencia_programa` (`id_programa_formacion`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `equipo_ejecutor`
--
ALTER TABLE `equipo_ejecutor`
  ADD PRIMARY KEY (`id_equipo`),
  ADD UNIQUE KEY `uq_equipo_nombre` (`nombre`);

--
-- Indices de la tabla `equipo_programa`
--
ALTER TABLE `equipo_programa`
  ADD PRIMARY KEY (`id_equipo_programa`),
  ADD UNIQUE KEY `uq_equipo_programa` (`id_equipo`,`id_programa_formacion`),
  ADD KEY `idx_equipo_programa_programa` (`id_programa_formacion`);

--
-- Indices de la tabla `ficha`
--
ALTER TABLE `ficha`
  ADD PRIMARY KEY (`codigo_ficha`),
  ADD KEY `idx_ficha_programa` (`id_programa_formacion`),
  ADD KEY `idx_ficha_equipo` (`id_equipo`),
  ADD KEY `idx_ficha_horario` (`id_horario`),
  ADD KEY `idx_ficha_municipio` (`codigo_municipio`),
  ADD KEY `idx_ficha_ambiente` (`id_ambiente`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`id_horario`),
  ADD UNIQUE KEY `uq_horario_nombre` (`horario`);

--
-- Indices de la tabla `municipio`
--
ALTER TABLE `municipio`
  ADD PRIMARY KEY (`codigo_municipio`);

--
-- Indices de la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD PRIMARY KEY (`id_programacion`),
  ADD KEY `idx_programacion_ficha` (`codigo_ficha`),
  ADD KEY `idx_programacion_competencia` (`id_competencia`),
  ADD KEY `idx_programacion_instructor` (`id_instructor`),
  ADD KEY `idx_programacion_dinamizador` (`id_dinamizador_asignador`);

--
-- Indices de la tabla `programa_formacion`
--
ALTER TABLE `programa_formacion`
  ADD PRIMARY KEY (`id_programa_formacion`),
  ADD UNIQUE KEY `uq_programa_codigo` (`codigo`);

--
-- Indices de la tabla `resultado`
--
ALTER TABLE `resultado`
  ADD PRIMARY KEY (`id_resultado`),
  ADD KEY `idx_resultado_competencia` (`id_competencia`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `tipo_doc`
--
ALTER TABLE `tipo_doc`
  ADD PRIMARY KEY (`id_tipodoc`),
  ADD UNIQUE KEY `uq_tipodoc` (`tipodoc`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `uq_usuario_documento` (`documento`),
  ADD UNIQUE KEY `uq_usuario_email` (`email`),
  ADD KEY `idx_usuario_equipo` (`id_equipo`),
  ADD KEY `idx_usuario_rol` (`id_rol`),
  ADD KEY `idx_usuario_tipodoc` (`id_tipodoc`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ambiente`
--
ALTER TABLE `ambiente`
  MODIFY `id_ambiente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `competencia`
--
ALTER TABLE `competencia`
  MODIFY `id_competencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `equipo_ejecutor`
--
ALTER TABLE `equipo_ejecutor`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `equipo_programa`
--
ALTER TABLE `equipo_programa`
  MODIFY `id_equipo_programa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `id_horario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `programacion`
--
ALTER TABLE `programacion`
  MODIFY `id_programacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `programa_formacion`
--
ALTER TABLE `programa_formacion`
  MODIFY `id_programa_formacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `resultado`
--
ALTER TABLE `resultado`
  MODIFY `id_resultado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tipo_doc`
--
ALTER TABLE `tipo_doc`
  MODIFY `id_tipodoc` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `competencia`
--
ALTER TABLE `competencia`
  ADD CONSTRAINT `fk_competencia_programa` FOREIGN KEY (`id_programa_formacion`) REFERENCES `programa_formacion` (`id_programa_formacion`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `equipo_programa`
--
ALTER TABLE `equipo_programa`
  ADD CONSTRAINT `fk_equipo_programa_equipo` FOREIGN KEY (`id_equipo`) REFERENCES `equipo_ejecutor` (`id_equipo`),
  ADD CONSTRAINT `fk_equipo_programa_programa` FOREIGN KEY (`id_programa_formacion`) REFERENCES `programa_formacion` (`id_programa_formacion`);

--
-- Filtros para la tabla `ficha`
--
ALTER TABLE `ficha`
  ADD CONSTRAINT `fk_ficha_ambiente` FOREIGN KEY (`id_ambiente`) REFERENCES `ambiente` (`id_ambiente`),
  ADD CONSTRAINT `fk_ficha_equipo` FOREIGN KEY (`id_equipo`) REFERENCES `equipo_ejecutor` (`id_equipo`),
  ADD CONSTRAINT `fk_ficha_horario` FOREIGN KEY (`id_horario`) REFERENCES `horario` (`id_horario`),
  ADD CONSTRAINT `fk_ficha_municipio` FOREIGN KEY (`codigo_municipio`) REFERENCES `municipio` (`codigo_municipio`),
  ADD CONSTRAINT `fk_ficha_programa` FOREIGN KEY (`id_programa_formacion`) REFERENCES `programa_formacion` (`id_programa_formacion`);

--
-- Filtros para la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD CONSTRAINT `fk_programacion_competencia` FOREIGN KEY (`id_competencia`) REFERENCES `competencia` (`id_competencia`),
  ADD CONSTRAINT `fk_programacion_dinamizador` FOREIGN KEY (`id_dinamizador_asignador`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_programacion_ficha` FOREIGN KEY (`codigo_ficha`) REFERENCES `ficha` (`codigo_ficha`),
  ADD CONSTRAINT `fk_programacion_instructor` FOREIGN KEY (`id_instructor`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `resultado`
--
ALTER TABLE `resultado`
  ADD CONSTRAINT `fk_resultado_competencia` FOREIGN KEY (`id_competencia`) REFERENCES `competencia` (`id_competencia`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `fk_usuario_equipo` FOREIGN KEY (`id_equipo`) REFERENCES `equipo_ejecutor` (`id_equipo`),
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`),
  ADD CONSTRAINT `fk_usuario_tipodoc` FOREIGN KEY (`id_tipodoc`) REFERENCES `tipo_doc` (`id_tipodoc`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
