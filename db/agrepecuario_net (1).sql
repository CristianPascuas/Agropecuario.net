-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-03-2026 a las 23:38:58
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo_miembro`
--

CREATE TABLE `equipo_miembro` (
  `id_equipo_miembro` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `rol_en_equipo` enum('coordinador','dinamizador','instructor') NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_vinculacion` date NOT NULL DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo_programa`
--

CREATE TABLE `equipo_programa` (
  `id_equipo_programa` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `id_programa_formacion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(4, 'curricular');

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
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `email` varchar(120) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
-- Indices de la tabla `competencia`
--
ALTER TABLE `competencia`
  ADD PRIMARY KEY (`id_competencia`),
  ADD UNIQUE KEY `uq_competencia_codigo_programa` (`id_programa_formacion`,`codigo`),
  ADD KEY `idx_competencia_programa` (`id_programa_formacion`);

--
-- Indices de la tabla `equipo_ejecutor`
--
ALTER TABLE `equipo_ejecutor`
  ADD PRIMARY KEY (`id_equipo`),
  ADD UNIQUE KEY `uq_equipo_nombre` (`nombre`);

--
-- Indices de la tabla `equipo_miembro`
--
ALTER TABLE `equipo_miembro`
  ADD PRIMARY KEY (`id_equipo_miembro`),
  ADD UNIQUE KEY `uq_usuario_un_equipo` (`id_usuario`),
  ADD KEY `idx_equipo_miembro_equipo` (`id_equipo`),
  ADD KEY `idx_equipo_miembro_rol` (`rol_en_equipo`);

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
-- AUTO_INCREMENT de la tabla `competencia`
--
ALTER TABLE `competencia`
  MODIFY `id_competencia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `equipo_ejecutor`
--
ALTER TABLE `equipo_ejecutor`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `equipo_miembro`
--
ALTER TABLE `equipo_miembro`
  MODIFY `id_equipo_miembro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `equipo_programa`
--
ALTER TABLE `equipo_programa`
  MODIFY `id_equipo_programa` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id_resultado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tipo_doc`
--
ALTER TABLE `tipo_doc`
  MODIFY `id_tipodoc` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `competencia`
--
ALTER TABLE `competencia`
  ADD CONSTRAINT `fk_competencia_programa` FOREIGN KEY (`id_programa_formacion`) REFERENCES `programa_formacion` (`id_programa_formacion`);

--
-- Filtros para la tabla `equipo_miembro`
--
ALTER TABLE `equipo_miembro`
  ADD CONSTRAINT `fk_equipo_miembro_equipo` FOREIGN KEY (`id_equipo`) REFERENCES `equipo_ejecutor` (`id_equipo`),
  ADD CONSTRAINT `fk_equipo_miembro_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

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
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`),
  ADD CONSTRAINT `fk_usuario_tipodoc` FOREIGN KEY (`id_tipodoc`) REFERENCES `tipo_doc` (`id_tipodoc`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
