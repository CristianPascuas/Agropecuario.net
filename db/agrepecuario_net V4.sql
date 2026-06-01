-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-04-2026 a las 14:41:12
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
  `lugar` varchar(100) NOT NULL,
  `codigo_municipio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ambiente`
--

INSERT INTO `ambiente` (`id_ambiente`, `ambiente`, `lugar`, `codigo_municipio`) VALUES
(1, 'TICs-1', 'SENA CENTRO AGREPUCUARIO', 19001),
(2, 'Tics-1', 'SENA Timbio', 19809),
(3, 'TICs-2', 'SENA CENTRO AGROPECUARIO', 19001);

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
(76, 'Can view equipo programa', 19, 'view_equipoprograma'),
(77, 'Can add programacion dia', 20, 'add_programaciondia'),
(78, 'Can change programacion dia', 20, 'change_programaciondia'),
(79, 'Can delete programacion dia', 20, 'delete_programaciondia'),
(80, 'Can view programacion dia', 20, 'view_programaciondia'),
(81, 'Can add instructor meta', 21, 'add_instructormeta'),
(82, 'Can change instructor meta', 21, 'change_instructormeta'),
(83, 'Can delete instructor meta', 21, 'delete_instructormeta'),
(84, 'Can view instructor meta', 21, 'view_instructormeta'),
(85, 'Can add instructor carga', 22, 'add_instructorcarga'),
(86, 'Can change instructor carga', 22, 'change_instructorcarga'),
(87, 'Can delete instructor carga', 22, 'delete_instructorcarga'),
(88, 'Can view instructor carga', 22, 'view_instructorcarga'),
(89, 'Can add instructor carga config', 23, 'add_instructorcargaconfig'),
(90, 'Can change instructor carga config', 23, 'change_instructorcargaconfig'),
(91, 'Can delete instructor carga config', 23, 'delete_instructorcargaconfig'),
(92, 'Can view instructor carga config', 23, 'view_instructorcargaconfig'),
(93, 'Can add programacion dia resultado', 24, 'add_programaciondiaresultado'),
(94, 'Can change programacion dia resultado', 24, 'change_programaciondiaresultado'),
(95, 'Can delete programacion dia resultado', 24, 'delete_programaciondiaresultado'),
(96, 'Can view programacion dia resultado', 24, 'view_programaciondiaresultado'),
(97, 'Can add programacion dia historial', 25, 'add_programaciondiahistorial'),
(98, 'Can change programacion dia historial', 25, 'change_programaciondiahistorial'),
(99, 'Can delete programacion dia historial', 25, 'delete_programaciondiahistorial'),
(100, 'Can view programacion dia historial', 25, 'view_programaciondiahistorial'),
(101, 'Can add radicado', 26, 'add_radicado'),
(102, 'Can change radicado', 26, 'change_radicado'),
(103, 'Can delete radicado', 26, 'delete_radicado'),
(104, 'Can view radicado', 26, 'view_radicado');

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
(22, 'academico', 'instructorcarga'),
(23, 'academico', 'instructorcargaconfig'),
(21, 'academico', 'instructormeta'),
(10, 'academico', 'municipio'),
(18, 'academico', 'programacion'),
(20, 'academico', 'programaciondia'),
(25, 'academico', 'programaciondiahistorial'),
(24, 'academico', 'programaciondiaresultado'),
(11, 'academico', 'programaformacion'),
(26, 'academico', 'radicado'),
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
(19, 'sessions', '0001_initial', '2026-03-09 13:57:30.858562'),
(43, 'academico', '0001_squashed_0007_remove_radicado_fechas', '2026-03-25 10:27:45.301504'),
(44, 'academico', '0001_squashed_0013_set_planta_hour_limits', '2026-03-25 15:31:58.323237'),
(45, 'academico', '0002_drop_legacy_usuario_hour_columns', '2026-03-25 15:31:58.326870'),
(46, 'academico', '0003_alter_ambiente_ambiente', '2026-03-25 15:31:58.329747'),
(47, 'academico', '0004_programaciondia_horario_especial', '2026-03-25 15:31:58.332593'),
(48, 'academico', '0005_radicado', '2026-03-25 15:31:58.335565'),
(49, 'academico', '0006_radicado_dias_seleccionados', '2026-03-25 15:31:58.338895'),
(50, 'academico', '0007_remove_radicado_fechas', '2026-03-25 15:31:58.341805'),
(51, 'academico', '0002_rename_equipo_activo_to_tipo', '2026-03-25 16:31:00.502867'),
(52, 'academico', '0003_radicado_campos_actividad_extra', '2026-04-06 15:10:55.738399'),
(53, 'academico', '0004_alter_radicado_archivo_excel', '2026-04-07 14:03:01.402129'),
(54, 'academico', '0005_add_tipo_dinamizador', '2026-04-09 13:04:51.143318'),
(55, 'academico', '0006_populate_tipo_dinamizador', '2026-04-09 13:04:51.164376');

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
('3jw49vrygwswfdjuxnhmidcu4j94157n', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0LvG:09CIVqUcXu-3NIT8BRYf5b0KHTGqhWL89ZEpYb6wCg4', '2026-03-25 15:56:34.766669'),
('7ioc37whvt89j71m41sei97dozsg1cdn', 'eyJ1c3VhcmlvX2lkIjoxMTN9:1wArhw:FVDVbKIJ7KXwdNBoIBO-UORaWn1W1TPp9czOLeSNrhg', '2026-04-23 15:54:16.392047'),
('7jm05heduxy49rx6nt29mpcv67hqpewl', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0Wy4:t6n-LXMRVFpI8z7PBrJ_-bs7EjkO5g2aCMF3u66WLko', '2026-03-26 03:44:12.795367'),
('7pstrrsxvzbsk6h0nn3algszu1rak0vw', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0U9Z:5w1WeZV860YDIWmFujKxk2oIZ9UTUp7uJbFu7yREhE4', '2026-03-26 00:43:53.558477'),
('8a9om7lcqmjqceparzd3bli5wg3oz4uj', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0WtL:QCCDyNCaW2lo8M8XhJWlnI9cttv9T7ATWkNpf1UOFfY', '2026-03-26 03:39:19.070312'),
('93kk5uxu1v6gs8ln3rrq7us6gq7xi523', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0Wt4:DLoKAoimEcneqzWXdcM3hgBf7wranHrYfyFANz-zNAk', '2026-03-26 03:39:02.748475'),
('dgui984nh0wglvqbvk9u2yadb47bpu14', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0XDk:l1_noraLFR0YvXloKldexaDBieggJ58teeII5ZNafXc', '2026-03-26 04:00:24.929540'),
('dl9mce7wjkr4o7amqct0f34cl69w33xt', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0WOL:A-BIkA-E4pNoDYjpknMpwnJuA8mpyPJzQ6JskCPc3Co', '2026-03-26 03:07:17.611569'),
('fb0yknc84wri8xpgxd736icmpnwjqsik', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0WMg:V_BCQ4hK1LMHKXR0nmVwW-5jRJnlzdXw5Op23Ap-JJw', '2026-03-26 03:05:34.284113'),
('g3qd7kj84cdorpt3yu9o6an4df5pgty6', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0TP8:HGCSbj-7zOkkr7bx7ToN9PXaciZgbUUbcz7tpCrRHEk', '2026-03-25 23:55:54.872604'),
('g5fskpqpyx5mt4ccymbrvd9y2n2jggoi', 'eyJ1c3VhcmlvX2lkIjo2fQ:1vzdgb:JuDouI-DNYbiyVrC0zTc4AyRuRRcrtORxXyX2QFQdfw', '2026-03-23 16:42:29.993486'),
('jbukchptio5j9q40bkiuudzx2lupmmgr', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0Ok8:3SBsQcNshW-pts10bNtlG-g1CHhQpFGVOVpFRUJ3Tn0', '2026-03-25 18:57:16.621780'),
('l44zzhpzeazw1iggi2aezb6ohgle65kd', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0XaK:5AXtL1YHaYfnBykVKeQcCAnvX05cK4_o8s-Avw9qqgw', '2026-03-26 04:23:44.392958'),
('lo2cgi451983d1tnbgrkzj1skdyind4y', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0U4f:llOkRFlFND8Ojw4QddPrm1bR0-8q8VnyRovhDQzQz8w', '2026-03-26 00:38:49.733928'),
('npe3vqr2nqifj1vogpuun856uxu68wrq', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0U7n:wLonYJrh6fH6VB4O4PPAjDqC4Jl7Y3zI4Y6HBxKYsYY', '2026-03-26 00:42:03.024007'),
('nv62low61ui3ud9x0vo4yglyi8t0t65g', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0WWf:O-RgaKvjokmmM-WMyQXmPDm2uU-1NaZXd7MQMYcuueA', '2026-03-26 03:15:53.174223'),
('olehsx696b7pcqswyg1z1k1xd4jymh97', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0XZi:YIkWrSllM6ibiTThDBtQLX-rH-riPAshBsB7cInacdU', '2026-03-26 04:23:06.547147'),
('opws2l9sjqi44uerfachc8j4ukvnw9k8', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0WFk:QWVU7NjaVkTNr2J-xZptq8sn-5-hG0XoOVuBWuNhaJM', '2026-03-26 02:58:24.069018'),
('qwi0bmzvlqnlonyfe06g51kpeaq5b09u', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0Wxo:2B2rnpSYnh9oQwDaXbLVO6VBiCs2sSH40S0XjDr7mGg', '2026-03-26 03:43:56.340299'),
('tg0zzco7xnje9tf3mvhdc24bo4s3h4wa', 'e30:1vzcAI:alXHmDFJ6Tkmu2hkZggbv_Q8YaJbueo4_594Q2_yiOw', '2026-03-23 15:05:02.836085'),
('uqdbpznlu3c5mgvifh0fpemx00vxg6n9', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0OpT:7TwbdG6cKemWBn9TmZ8r6wBZR720Fy11pUze5kVvgIs', '2026-03-25 19:02:47.404192'),
('x0sooc0d4gqi0e6emfl0v7q0z57qgjqa', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0OnQ:fhWT8r_2fX3CPXGKEtjmEzRlT6vUO2Qq4HpYHOw7-lk', '2026-03-25 19:00:40.031604'),
('zqtre5tapqxj9r3wbv8x4090rpjhyua0', 'eyJ1c3VhcmlvX2lkIjo4fQ:1w0Wsj:TDdbs-PaouqLJzoBMTZFZl2UtlEYE7BxCV5anSo-Ehw', '2026-03-26 03:38:41.562447');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo_ejecutor`
--

CREATE TABLE `equipo_ejecutor` (
  `id_equipo` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `tipo` smallint(5) UNSIGNED NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `equipo_ejecutor`
--

INSERT INTO `equipo_ejecutor` (`id_equipo`, `nombre`, `tipo`, `creado_en`) VALUES
(1, 'SISTEMAS (TICS)', 0, '2026-03-05 01:59:11'),
(2, 'GESTION DE LA SEGURIDAD Y SALUD EN EL TRABAJO', 1, '2026-03-13 19:33:52'),
(3, 'GESTION TALENTO HUMANO', 1, '2026-03-13 19:33:52'),
(4, 'BILINGÜISMO - DESARROLLO DE PROCESOS DE MERCADEO', 0, '2026-03-13 19:33:52'),
(5, 'TRANSVERSALES', 0, '2026-03-13 19:33:52'),
(6, 'AGROINDUSTRIA', 1, '2026-03-13 19:33:52'),
(7, 'VIRTUALES', 1, '2026-03-13 19:33:52'),
(8, 'COMPLEMENTARIOS', 0, '2026-03-13 19:33:52');

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
(1, 1, 1),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha`
--

CREATE TABLE `ficha` (
  `codigo_ficha` int(11) NOT NULL,
  `id_programa_formacion` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `id_lider_ficha` int(11) DEFAULT NULL,
  `id_horario` int(11) DEFAULT NULL,
  `tipo_ficha` varchar(40) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `codigo_municipio` int(11) NOT NULL,
  `id_ambiente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ficha`
--

INSERT INTO `ficha` (`codigo_ficha`, `id_programa_formacion`, `id_equipo`, `id_lider_ficha`, `id_horario`, `tipo_ficha`, `fecha_inicio`, `fecha_fin`, `codigo_municipio`, `id_ambiente`) VALUES
(3071104, 1, 1, 9, 1, 'Presencial', '2024-08-12', '2026-06-08', 19001, 1);

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
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `anio_operativo` smallint(5) UNSIGNED DEFAULT NULL CHECK (`anio_operativo` >= 0),
  `estado` varchar(20) NOT NULL,
  `mes_operativo` smallint(5) UNSIGNED DEFAULT NULL CHECK (`mes_operativo` >= 0),
  `id_ambiente` int(11) DEFAULT NULL,
  `modificado_en` datetime(6) DEFAULT NULL,
  `razon_cambio` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion_dia`
--

CREATE TABLE `programacion_dia` (
  `id_programacion_dia` int(11) NOT NULL,
  `codigo_ficha` int(11) NOT NULL,
  `id_competencia` int(11) NOT NULL,
  `id_instructor` int(11) NOT NULL,
  `id_dinamizador_asignador` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `id_horario` int(11) NOT NULL,
  `horas_dia` decimal(5,2) NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) NOT NULL DEFAULT 'programada',
  `id_usuario_modificacion` int(11) DEFAULT NULL,
  `modificado_en` datetime(6) DEFAULT NULL,
  `hora_fin` time(6) DEFAULT NULL,
  `hora_inicio` time(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion_dia_resultado`
--

CREATE TABLE `programacion_dia_resultado` (
  `id_programacion_dia_resultado` int(11) NOT NULL,
  `creado_en` datetime(6) NOT NULL,
  `id_programacion_dia` int(11) NOT NULL,
  `id_resultado` int(11) NOT NULL
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
-- Estructura de tabla para la tabla `radicado`
--

CREATE TABLE `radicado` (
  `id_radicado` int(11) NOT NULL,
  `nombre_radicado` varchar(180) NOT NULL,
  `tipo_radicado` smallint(5) UNSIGNED NOT NULL CHECK (`tipo_radicado` >= 0),
  `descripcion_radicado` longtext NOT NULL,
  `hora_inicio` time(6) NOT NULL,
  `hora_fin` time(6) NOT NULL,
  `archivo_excel` varchar(100) NOT NULL,
  `aprobado` smallint(5) UNSIGNED NOT NULL CHECK (`aprobado` >= 0),
  `creado_en` datetime(6) NOT NULL,
  `id_instructor` int(11) NOT NULL,
  `dias_seleccionados` longtext NOT NULL,
  `empresa_organizacion` varchar(180) NOT NULL,
  `nit` varchar(40) NOT NULL,
  `lugar` varchar(180) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `radicado`
--

INSERT INTO `radicado` (`id_radicado`, `nombre_radicado`, `tipo_radicado`, `descripcion_radicado`, `hora_inicio`, `hora_fin`, `archivo_excel`, `aprobado`, `creado_en`, `id_instructor`, `dias_seleccionados`, `empresa_organizacion`, `nit`, `lugar`) VALUES
(6, 'Radicado 1', 2, 'esfafe', '09:45:00.000000', '11:45:00.000000', 'radicados/felix-afranio-mage-imbachi/2026-04-09/informe-programa-de-formacion-titulada-9_qYsQv3m.pdf', 0, '2026-04-09 14:45:48.025022', 8, '[\"2026-04-09\", \"2026-04-10\", \"2026-04-13\", \"2026-04-14\", \"2026-04-15\", \"2026-04-16\", \"2026-04-17\"]', 'wqewqe', '12212312', 'dasdasds');

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
(1, 'instructor'),
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
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `horas_max_mensual` smallint(5) UNSIGNED NOT NULL CHECK (`horas_max_mensual` >= 0),
  `horas_min_mensual` smallint(5) UNSIGNED NOT NULL CHECK (`horas_min_mensual` >= 0),
  `horas_objetivo_anual` int(11) NOT NULL,
  `tipo_contrato` smallint(5) UNSIGNED NOT NULL CHECK (`tipo_contrato` >= 0),
  `horas_min_anual` int(11) NOT NULL,
  `tipo_dinamizador` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre`, `apellido`, `documento`, `id_tipodoc`, `id_rol`, `id_equipo`, `activo`, `email`, `contrasena`, `creado_en`, `horas_max_mensual`, `horas_min_mensual`, `horas_objetivo_anual`, `tipo_contrato`, `horas_min_anual`, `tipo_dinamizador`) VALUES
(7, 'Javier Mauricio', 'Palomino', '1061712232', 1, 3, 1, 1, 'herneycristiancoordinador@gmail.com', 'pbkdf2_sha256$1000000$YGJszz4cG1CQUtLDLaoilf$lGgkpXgvBXASZPdPBLZJtkLHPYHVJO+0KdhDIpmS7NU=', '2026-03-09 22:00:09', 160, 140, 1680, 0, 1680, NULL),
(8, 'Felix Afranio', 'Mage Imbachi', '1061712231', 1, 2, 1, 1, 'magefelix@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-09 22:01:27', 120, 100, 1200, 1, 1000, 'instructor'),
(9, 'Moises', 'Garcia Vargas', '3233336969', 1, 1, 1, 1, 'moisog@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-12 09:12:49', 160, 140, 1680, 0, 1680, NULL),
(10, 'Helvin Ricardo', 'Lopez Tobar', '9465379731', 1, 2, 2, 1, 'sin-correo-9465379731@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, 'instructor'),
(11, 'Yuri Milena', 'Fernandez Perez', '3233213522', 1, 1, 2, 1, 'milenaf1922@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(12, 'Ludy Viviana', 'Espinosa Espinosa', '3122028759', 1, 1, 2, 1, 'luddyvivi@yahoo.es', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(13, 'Isabella', 'Collazos Garcia', '3116155188', 1, 1, 2, 1, 'isacollazosgarcia@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(14, 'Edith Lorena', 'Valverde Rosero', '3168141935', 1, 1, 2, 1, 'lorenaval23@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(15, 'Monica Alejandra', 'Rosero Pajoy', '3127583909', 1, 1, 2, 1, 'alejita16_24@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(16, 'Carlos Arturo', 'Cajigas Muñoz', '3113575427', 1, 1, 2, 1, 'carloscajigas08@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(17, 'Maribel', 'Sanchez Garcia', '3007918306', 1, 1, 2, 1, 'maribel.sanchezsst@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(18, 'Juan Ruben', 'Ceron Valverde', '3014771755', 1, 1, 2, 1, 'rubcero@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(19, 'Mauricio', 'Ahumada Caicedo', '9286633642', 1, 1, 1, 1, 'sin-correo-9286633642@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(20, 'Wilmer Javier', 'Peña Capote', '3105121186', 1, 1, 1, 1, 'wilpe88@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(21, 'Esmeralda', 'Betancur Lopez', '3007023454', 1, 1, 1, 1, 'workesme@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(22, 'Michel Orlando', 'Hoyos Burbano', '3137142125', 1, 1, 1, 1, 'michel.burbano.h@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(23, 'Rene Alejandro', 'Mosquera Reyes', '3147990710', 1, 1, 1, 1, 'rramosing@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(24, 'Diego Fernando', 'Bucheli Rojas', '3166223681', 1, 1, 1, 1, 'diegobuchelirojas@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(25, 'James', 'Nixon Cuellar', '3114029326', 1, 1, 1, 1, 'jamescuellar66@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(26, 'Yensi', 'Acosta Guzmán', '9333569352', 1, 2, 3, 1, 'sin-correo-9333569352@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, 'instructor'),
(27, 'Nilton Adrian', 'Quinayas Ceron', '3148350120', 1, 1, 3, 1, 'naquinayas@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(28, 'Mario Hernan', 'Perez Uni', '3127707092', 1, 1, 3, 1, 'mariope0615@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(29, 'Luciano De', 'Escobar Muñoz', '3113715570', 1, 1, 3, 1, 'lucianoescobarm@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(30, 'Cristian Dario', 'Atencio Molina', '3122409033', 1, 1, 3, 1, 'cristianatencio00@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(31, 'Victor Alexis', 'Quilindo Elvira', '3012419163', 1, 1, 3, 1, 'victoralexisquilindo@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(32, 'Alex', 'Jimenez Juspian', '3174409019', 1, 1, 3, 1, 'jimalexandre@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(33, 'Sandra Mercedes', 'Diaz Lalinde', '9022050650', 1, 1, 3, 1, 'sin-correo-9022050650@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(34, 'Dario Bernardo', 'Montufar Blanco', '9005344966', 1, 1, 3, 1, 'sin-correo-9005344966@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(35, 'Jose Robinson', 'Valencia Felantana', '9684041996', 1, 1, 3, 1, 'sin-correo-9684041996@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(36, 'Angela Stella', 'Paredes Florez', '3206903211', 1, 1, 3, 1, 'angepaflo1@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(37, 'Leidy Susana', 'Ruiz Velasco', '9016041513', 1, 2, 4, 1, 'sin-correo-9016041513@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, 'instructor'),
(38, 'Danny Harold', 'Jamauca Pantoja', '9821532301', 1, 1, 4, 1, 'sin-correo-9821532301@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(39, 'Anggie Daniela', 'Castillo Escobar', '3023862130', 1, 1, 4, 1, 'danielacastilloe30@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(40, 'Diana Marcela', 'Burbano Sanchez', '3137520507', 1, 1, 4, 1, 'diana.bur05@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(41, 'Diana Mireya', 'Rivera Muñoz', '3105985996', 1, 1, 4, 1, 'dmriveram141@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(42, 'William Hernan', 'Valencia Gallego', '3217733927', 1, 1, 4, 1, 'williamval37@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(43, 'Pablo Cesar', 'Cuadros Villa', '3016319515', 1, 1, 4, 1, 'pablo_please@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(44, 'Neyla Rocio', 'Guzman Leon', '3163090905', 1, 1, 4, 1, 'neru-10@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(45, 'Rosalba', 'Muñoz Rodríguez', '9755701029', 1, 2, 5, 1, 'sin-correo-9755701029@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, 'instructor'),
(46, 'Diana Alejandra', 'Ahumada Caicedo', '3142743634', 1, 1, 5, 1, 'alejandraahumada1927@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(47, 'Karen Elizabeth', 'Luna Delacruz', '3002194608', 1, 1, 5, 1, 'elilunadelacruz@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(48, 'Sandra Lorena', 'Taborda Erazo', '3156479594', 1, 1, 5, 1, 'salotaercarher@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(49, 'Connye Johana', 'Betancourt Arenas', '3215509391', 1, 1, 5, 1, 'connyebeta@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(50, 'Ana Maria', 'Avila Ordoñez', '3187955501', 1, 1, 5, 1, 'marianavila04122023@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(51, 'Hernan Alonso', 'Reyes Valencia', '3158132000', 1, 1, 5, 1, 'hernanrey28@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(52, 'Jhonnatan Fernando', 'Medina Caicedo', '3122394785', 1, 1, 5, 1, 'jhonpepemedina@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(53, 'Marco Eliecer', 'Riascos Montenegro', '3105138957', 1, 1, 5, 1, 'markos072008@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(54, 'Yuly Lorena', 'Ordoñez Barco', '3106299823', 1, 1, 5, 1, 'yuli.loren@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(55, 'Beatriz Adriana', 'Flor Hurtado', '3178000044', 1, 1, 5, 1, 'adrs7777@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(56, 'Viviana', 'Cifuentes Mulcue', '9504422559', 1, 2, 6, 1, 'sin-correo-9504422559@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, 'instructor'),
(57, 'Maria Alejandra', 'Ayerbe Rios', '9675207288', 1, 1, 6, 1, 'sin-correo-9675207288@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(58, 'Alex Javier', 'Bacca Narvaez', '9894403971', 1, 1, 6, 1, 'sin-correo-9894403971@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(59, 'Ruben', 'Dario Escobar', '9234620454', 1, 1, 6, 1, 'sin-correo-9234620454@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(60, 'Johanna', 'España Muñoz', '9296613663', 1, 1, 6, 1, 'sin-correo-9296613663@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(61, 'Maria Fernanda', 'Guaca Sandoval', '9461064940', 1, 1, 6, 1, 'sin-correo-9461064940@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(62, 'Fabian Javier', 'Lasso Ordoñez', '9115439080', 1, 1, 6, 1, 'sin-correo-9115439080@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(63, 'Oscar Libardo', 'Pencue Fierro', '9233640508', 1, 1, 6, 1, 'sin-correo-9233640508@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(64, 'Luis Alfonso', 'Sarria Gallego', '9658072700', 1, 1, 6, 1, 'sin-correo-9658072700@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(65, 'Luz Nelly', 'Villalba Gualteros', '9799254036', 1, 1, 6, 1, 'sin-correo-9799254036@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(66, 'Yulena Gisel', 'Beltran Quinayas', '3145895003', 1, 1, 6, 1, 'beltrangisel731@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(67, 'Carlos Arturo', 'Valencia Carvajal', '3116144770', 1, 1, 6, 1, 'arthurovalencia112@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(68, 'Cristian Alberto', 'Trochez Mosquera', '3148731461', 1, 1, 6, 1, 'cristrochez89@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(69, 'Bibiana Alexandra', 'Astaiza Lopez', '3206482013', 1, 1, 6, 1, 'bastaiza@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(70, 'Manuel Arcadio', 'Alvarez Sanchez', '3015021180', 1, 1, 6, 1, 'manuelalvarez24@yahoo.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(71, 'Jose Kenedy', 'Lasso Martinez', '3216073703', 1, 1, 6, 1, 'juanjose217777@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(72, 'Alvaro', 'Garzon Garzon', '3122384487', 1, 1, 6, 1, 'alvarogarzon76@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(73, 'Yohn Faber', 'Pacheco Marin', '3234485757', 1, 1, 6, 1, 'faber323@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(74, 'Seidy Vanessa', 'Vidal Prado', '3136151200', 1, 1, 6, 1, 'vanessitavidal421@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(75, 'Flora Janeth', 'Sinisterra Ruiz', '3216455727', 1, 1, 6, 1, 'florsinis@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(76, 'Ricardo Oswaldo', 'Jaramillo Solarte', '9375721862', 1, 1, 7, 1, 'sin-correo-9375721862@import.local', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 120, 100, 1200, 1, 1000, NULL),
(77, 'Diego Fernando', 'Bolaños Chamorro', '3008503879', 1, 1, 7, 1, 'diegobolanos.pro@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(78, 'Diego Fernando', 'Alegria Castrillon', '3175035203', 1, 1, 7, 1, 'diegofer0419@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(79, 'Adrian Danilo', 'Astudillo Talaga', '3127318581', 1, 1, 7, 1, 'astudillo.danilo@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(80, 'Andrea', 'Carvajal Obando', '3173831167', 1, 1, 7, 1, 'andreacarvajalobando@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(81, 'Betsy Alejandra', 'Rojas Mosquera', '3117237583', 1, 1, 7, 1, 'keroppi07@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(82, 'Mauricio', 'Quintero Gutierrez', '3235812652', 1, 1, 7, 1, 'mauricioquintero1994@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(83, 'Fabian Horacio', 'Garces Ordoñez', '3128347070', 1, 1, 7, 1, 'fhgar08@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(84, 'Enmanuel', 'Latorre Vidal', '3176811433', 1, 1, 7, 1, 'elatorrevi@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(85, 'Gerardo Andres', 'Quiñones Artunduaga', '3104183267', 1, 1, 7, 1, 'gdoandres.quinones@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(86, 'Iris Samady', 'Trujillo Coaji', '3218745916', 1, 1, 7, 1, 'samy-2781@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(87, 'Nelly Mercedes', 'Camues Viteri', '3154287000', 1, 1, 7, 1, 'kmuviteri@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(88, 'Maricela Del', 'Pilar Salazar', '3154321284', 1, 1, 7, 1, 'ms0649615@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(89, 'Maritza Vanessa', 'Santander Moreano', '3122173824', 1, 1, 7, 1, 'vanessasantander23@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(90, 'Sonia', 'Yaneth Betancourt', '3128452603', 1, 1, 7, 1, 'soniabetsa@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(91, 'Luz Viviana', 'Calderon Urbano', '3226665921', 1, 1, 7, 1, 'calderonvivi1995@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(92, 'Martha Lucia', 'Campiño Barrera', '3214732882', 1, 1, 7, 1, 'mlcampino@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(93, 'Shirley Viviana', 'Aguilera Gonzalez', '3115205131', 1, 1, 7, 1, 'vivianaguilera1105@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(94, 'Deiby Cristina', 'Alban Fernandez', '3147722567', 1, 1, 7, 1, 'cristinaalban90@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(95, 'Alba Nury', 'Osorio Alzate', '3148151658', 1, 1, 7, 1, 'albanury585@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(96, 'Elsa', 'Jordan Bonilla', '3013928164', 1, 1, 7, 1, 'ejordanb@sena.edu.co', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(97, 'Zulma', 'Meneses', '3187150097', 1, 1, 7, 1, 'zulma_mile7@yahoo.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(98, 'Martha Lucia', 'Rangel Muñoz', '3102595397', 1, 1, 7, 1, 'marthalurangel@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(99, 'Martha Elena', 'Muñoz Sanchez', '3233934170', 1, 1, 7, 1, 'marticamunoz123@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(100, 'Jose Angel', 'Duarte Palechor', '3205503113', 1, 1, 7, 1, 'joseduarte@unicauca.edu.co', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(101, 'Andres Felipe', 'Salazar Diaz', '3105105592', 1, 1, 7, 1, 'andressalazar20@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(102, 'Jesus Eduardo', 'Muñoz Orozco', '3117979505', 1, 1, 7, 1, 'eduardo9j@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(103, 'Alejandro', 'Velasco Chaves', '3103623334', 1, 1, 7, 1, 'alevelcha@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(104, 'Martha Lucia', 'Muñoz Satizabal', '3107348350', 1, 1, 8, 1, 'martalumu@mail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(105, 'Fabian Andres', 'Vidal Bonilla', '3215347417', 1, 1, 8, 1, 'favianvidal117@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(106, 'Carolina', 'Mosquera Angulo', '3006149723', 1, 1, 8, 1, 'caromosque@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(107, 'Andres Fernando', 'Ausecha Obando', '3172244310', 1, 1, 8, 1, 'andres.afa90@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(108, 'Maria Del Carmen', 'Quintero Manquillo', '3108976254', 1, 1, 8, 1, 'heberlauro6@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(109, 'Juan Andres', 'Agredo Ruge', '3106214205', 1, 1, 8, 1, 'jaruge07@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(110, 'Franklin Andres', 'Caicedo Quinayas', '3135462084', 1, 1, 8, 1, 'facaicedoq@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(111, 'Paola Andrea', 'Meneses Urbano', '3107458882', 1, 1, 8, 1, 'andreameneses72@hotmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(112, 'Helbert', 'Franklyn Arboleda', '3103992180', 1, 1, 8, 1, 'helbertharboleda@gmail.com', 'pbkdf2_sha256$600000$cJFoqcRGhBnAQD7o6cS1zV$W1LprqYH7FLgkQNPNoEP+q4d+EZA25X6g6nDif7dq9Q=', '2026-03-13 19:33:52', 160, 140, 1680, 0, 1680, NULL),
(113, 'Cristian', 'Pascuas', '1061712230', 1, 5, NULL, 1, 'herneycristian@gmail.com', 'pbkdf2_sha256$1000000$paXi7zqDPq47NVdD97LccT$IAWkyS2GeCnp0BAlHpnSV6eHp5WTZP5lemXYZY3IWJo=', '2026-04-09 20:54:08', 160, 120, 1680, 0, 1680, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ambiente`
--
ALTER TABLE `ambiente`
  ADD PRIMARY KEY (`id_ambiente`),
  ADD KEY `ambiente_codigo_municipio_a0705f36_fk_municipio_codigo_municipio` (`codigo_municipio`);

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
  ADD KEY `idx_ficha_ambiente` (`id_ambiente`),
  ADD KEY `idx_ficha_lider` (`id_lider_ficha`);

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
  ADD KEY `idx_programacion_dinamizador` (`id_dinamizador_asignador`),
  ADD KEY `programacion_id_ambiente_c3964033_fk_ambiente_id_ambiente` (`id_ambiente`);

--
-- Indices de la tabla `programacion_dia`
--
ALTER TABLE `programacion_dia`
  ADD PRIMARY KEY (`id_programacion_dia`),
  ADD UNIQUE KEY `uq_prog_dia_instructor` (`id_instructor`,`fecha`,`id_horario`),
  ADD KEY `idx_prog_dia_ficha_fecha` (`codigo_ficha`,`fecha`),
  ADD KEY `idx_prog_dia_amb_hor` (`id_horario`,`fecha`),
  ADD KEY `fk_prog_dia_competencia` (`id_competencia`),
  ADD KEY `fk_prog_dia_dinamizador` (`id_dinamizador_asignador`),
  ADD KEY `programacion_dia_codigo_ficha_a6fbdb0d` (`codigo_ficha`),
  ADD KEY `programacion_dia_id_usuario_modificac_cb724a9d_fk_usuario_i` (`id_usuario_modificacion`);

--
-- Indices de la tabla `programacion_dia_resultado`
--
ALTER TABLE `programacion_dia_resultado`
  ADD PRIMARY KEY (`id_programacion_dia_resultado`),
  ADD UNIQUE KEY `programacion_dia_resulta_id_programacion_dia_id_r_05b14daf_uniq` (`id_programacion_dia`,`id_resultado`),
  ADD KEY `programacion_dia_res_id_resultado_0a278d5b_fk_resultado` (`id_resultado`);

--
-- Indices de la tabla `programa_formacion`
--
ALTER TABLE `programa_formacion`
  ADD PRIMARY KEY (`id_programa_formacion`),
  ADD UNIQUE KEY `uq_programa_codigo` (`codigo`);

--
-- Indices de la tabla `radicado`
--
ALTER TABLE `radicado`
  ADD PRIMARY KEY (`id_radicado`),
  ADD KEY `radicado_id_instructor_537c447e_fk_usuario_id_usuario` (`id_instructor`);

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
  MODIFY `id_ambiente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT de la tabla `equipo_ejecutor`
--
ALTER TABLE `equipo_ejecutor`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `equipo_programa`
--
ALTER TABLE `equipo_programa`
  MODIFY `id_equipo_programa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `id_horario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `programacion`
--
ALTER TABLE `programacion`
  MODIFY `id_programacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `programacion_dia`
--
ALTER TABLE `programacion_dia`
  MODIFY `id_programacion_dia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=202;

--
-- AUTO_INCREMENT de la tabla `programacion_dia_resultado`
--
ALTER TABLE `programacion_dia_resultado`
  MODIFY `id_programacion_dia_resultado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;

--
-- AUTO_INCREMENT de la tabla `programa_formacion`
--
ALTER TABLE `programa_formacion`
  MODIFY `id_programa_formacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `radicado`
--
ALTER TABLE `radicado`
  MODIFY `id_radicado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

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
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=114;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ambiente`
--
ALTER TABLE `ambiente`
  ADD CONSTRAINT `ambiente_codigo_municipio_a0705f36_fk_municipio_codigo_municipio` FOREIGN KEY (`codigo_municipio`) REFERENCES `municipio` (`codigo_municipio`);

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
  ADD CONSTRAINT `fk_ficha_lider` FOREIGN KEY (`id_lider_ficha`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_ficha_municipio` FOREIGN KEY (`codigo_municipio`) REFERENCES `municipio` (`codigo_municipio`),
  ADD CONSTRAINT `fk_ficha_programa` FOREIGN KEY (`id_programa_formacion`) REFERENCES `programa_formacion` (`id_programa_formacion`);

--
-- Filtros para la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD CONSTRAINT `fk_programacion_competencia` FOREIGN KEY (`id_competencia`) REFERENCES `competencia` (`id_competencia`),
  ADD CONSTRAINT `fk_programacion_dinamizador` FOREIGN KEY (`id_dinamizador_asignador`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_programacion_ficha` FOREIGN KEY (`codigo_ficha`) REFERENCES `ficha` (`codigo_ficha`),
  ADD CONSTRAINT `fk_programacion_instructor` FOREIGN KEY (`id_instructor`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `programacion_id_ambiente_c3964033_fk_ambiente_id_ambiente` FOREIGN KEY (`id_ambiente`) REFERENCES `ambiente` (`id_ambiente`);

--
-- Filtros para la tabla `programacion_dia`
--
ALTER TABLE `programacion_dia`
  ADD CONSTRAINT `fk_prog_dia_competencia` FOREIGN KEY (`id_competencia`) REFERENCES `competencia` (`id_competencia`),
  ADD CONSTRAINT `fk_prog_dia_dinamizador` FOREIGN KEY (`id_dinamizador_asignador`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_prog_dia_ficha` FOREIGN KEY (`codigo_ficha`) REFERENCES `ficha` (`codigo_ficha`),
  ADD CONSTRAINT `fk_prog_dia_horario` FOREIGN KEY (`id_horario`) REFERENCES `horario` (`id_horario`),
  ADD CONSTRAINT `fk_prog_dia_instructor` FOREIGN KEY (`id_instructor`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `programacion_dia_id_usuario_modificac_cb724a9d_fk_usuario_i` FOREIGN KEY (`id_usuario_modificacion`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `programacion_dia_resultado`
--
ALTER TABLE `programacion_dia_resultado`
  ADD CONSTRAINT `programacion_dia_res_id_programacion_dia_52da6255_fk_programac` FOREIGN KEY (`id_programacion_dia`) REFERENCES `programacion_dia` (`id_programacion_dia`),
  ADD CONSTRAINT `programacion_dia_res_id_resultado_0a278d5b_fk_resultado` FOREIGN KEY (`id_resultado`) REFERENCES `resultado` (`id_resultado`);

--
-- Filtros para la tabla `radicado`
--
ALTER TABLE `radicado`
  ADD CONSTRAINT `radicado_id_instructor_537c447e_fk_usuario_id_usuario` FOREIGN KEY (`id_instructor`) REFERENCES `usuario` (`id_usuario`);

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
