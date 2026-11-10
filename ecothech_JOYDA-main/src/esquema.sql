CREATE DATABASE IF NOT EXISTS ecotech CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ecotech;

CREATE TABLE IF NOT EXISTS empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(30),
    correo VARCHAR(100),
    fecha_inicio DATE,
    salario DECIMAL(12,2)
);

CREATE TABLE IF NOT EXISTS departamento (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    gerente_id INT NULL
);

CREATE TABLE IF NOT EXISTS proyecto (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    id_departamento INT NULL
);

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    horas_trabajadas DECIMAL(5,2) NOT NULL,
    descripcion VARCHAR(200),
    id_empleado INT NOT NULL,
    id_proyecto INT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    empleado_id INT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'empleado'
);

CREATE TABLE IF NOT EXISTS asignacion_proyecto (
    id_empleado INT NOT NULL,
    id_proyecto INT NOT NULL,
    PRIMARY KEY (id_empleado, id_proyecto)
);

CREATE TABLE IF NOT EXISTS indicador_api (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fuente VARCHAR(50) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    verificado_en DATETIME NOT NULL,
    UNIQUE KEY uq_observacion (fuente, codigo, fecha)
);