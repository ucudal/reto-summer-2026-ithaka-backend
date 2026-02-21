-- =========================
-- TABLA ROL
-- =========================
CREATE TABLE rol (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- =========================
-- TABLA USUARIO
-- =========================
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    apellido VARCHAR(150),
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    id_rol INTEGER NOT NULL,
    FOREIGN KEY (id_rol)
        REFERENCES rol(id_rol)
        ON DELETE RESTRICT
);

-- =========================
-- TABLA EMPRENDEDOR
-- =========================
CREATE TABLE emprendedor (
    id_emprendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    apellido VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(50),
    documento_identidad VARCHAR(50),
    pais_residencia VARCHAR(100),
    ciudad_residencia VARCHAR(100),
    campus_ucu VARCHAR(100),
    relacion_ucu VARCHAR(100),
    facultad_ucu VARCHAR(100),
    canal_llegada VARCHAR(100),
    motivacion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- TABLA CONVOCATORIA
-- =========================
CREATE TABLE convocatoria (
    id_convocatoria SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    fecha_cierre TIMESTAMP
);

-- =========================
-- TABLA CATALOGO_ESTADOS
-- =========================
CREATE TABLE catalogo_estados (
    id_estado SERIAL PRIMARY KEY,
    nombre_estado VARCHAR(100) NOT NULL,
    tipo_caso VARCHAR(100) NOT NULL
);

-- =========================
-- TABLA CASO
-- =========================
CREATE TABLE caso (
    id_caso SERIAL PRIMARY KEY,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre_caso VARCHAR(200) NOT NULL,
    descripcion TEXT,
    datos_chatbot JSONB,
    consentimiento_datos BOOLEAN DEFAULT FALSE,
    id_emprendedor INTEGER NOT NULL,
    id_convocatoria INTEGER,
    id_estado INTEGER NOT NULL,

    FOREIGN KEY (id_emprendedor)
        REFERENCES emprendedor(id_emprendedor)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_convocatoria)
        REFERENCES convocatoria(id_convocatoria)
        ON DELETE SET NULL,

    FOREIGN KEY (id_estado)
        REFERENCES catalogo_estados(id_estado)
        ON DELETE RESTRICT
);

-- =========================
-- TABLA PROGRAMA
-- =========================
CREATE TABLE programa (
    id_programa SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- =========================
-- TABLA APOYO
-- =========================
CREATE TABLE apoyo (
    id_apoyo SERIAL PRIMARY KEY,
    tipo_apoyo VARCHAR(150) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    id_caso INTEGER NOT NULL,
    id_programa INTEGER NOT NULL,

    FOREIGN KEY (id_caso)
        REFERENCES caso(id_caso)
        ON DELETE CASCADE,

    FOREIGN KEY (id_programa)
        REFERENCES programa(id_programa)
        ON DELETE RESTRICT
);

-- =========================
-- TABLA APOYO_SOLICITADO
-- =========================
CREATE TABLE apoyo_solicitado (
    id_apoyo_solicitado SERIAL PRIMARY KEY,
    categoria_apoyo VARCHAR(150) NOT NULL,
    id_caso INTEGER NOT NULL,

    FOREIGN KEY (id_caso)
        REFERENCES caso(id_caso)
        ON DELETE CASCADE
);

-- =========================
-- TABLA ASIGNACION
-- =========================
CREATE TABLE asignacion (
    id_asignacion SERIAL PRIMARY KEY,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    id_caso INTEGER NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_caso)
        REFERENCES caso(id_caso)
        ON DELETE CASCADE
);

-- =========================
-- TABLA NOTA
-- =========================
CREATE TABLE nota (
    id_nota SERIAL PRIMARY KEY,
    contenido TEXT NOT NULL,
    tipo_nota VARCHAR(50) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    id_caso INTEGER NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_caso)
        REFERENCES caso(id_caso)
        ON DELETE CASCADE
);

-- =========================
-- TABLA AUDITORIA
-- =========================
CREATE TABLE auditoria (
    id_auditoria SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accion VARCHAR(150) NOT NULL,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    id_usuario INTEGER NOT NULL,
    id_caso INTEGER,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_caso)
        REFERENCES caso(id_caso)
        ON DELETE CASCADE
);