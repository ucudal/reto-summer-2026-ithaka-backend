
-- =====================================
-- ROLES
-- =====================================
INSERT INTO rol (nombre_rol) VALUES 
('Admin'),
('Coordinador'),
('Tutor');


-- =====================================
-- USUARIOS
-- =====================================
-- Los usuarios se crean con el script:
-- python -m scripts.create_test_users
-- Esto permite tener contraseñas visibles para pruebas


-- =====================================
-- EMPRENDEDORES
-- =====================================
INSERT INTO emprendedor (nombre, apellido, email, telefono, documento_identidad, pais_residencia, ciudad_residencia, campus_ucu, relacion_ucu, facultad_ucu, canal_llegada, motivacion, fecha_registro) VALUES 
('Ana', 'Martínez', 'ana.martinez@example.com', '+59891234567', '12345678', 'Uruguay', 'Montevideo', 'Campus Montevideo', 'Estudiante', 'Ingeniería', 'Web', 'Quiero desarrollar mi startup tecnológica', '2026-01-15 10:30:00'),
('Carlos', 'López', 'carlos.lopez@example.com', '+59892345678', '23456789', 'Uruguay', 'Montevideo', 'Campus Montevideo', 'Egresado', 'Empresariales', 'Referido', 'Tengo una idea de negocio sostenible', '2026-01-20 14:45:00'),
('Laura', 'Fernández', 'laura.fernandez@example.com', '+59893456789', '34567890', 'Uruguay', 'Salto', 'Campus Salto', 'Estudiante', 'Comunicación', 'Chatbot', 'Proyecto social con impacto', '2026-02-01 09:15:00'),
('Diego', 'Silva', 'diego.silva@example.com', '+54911567890', '45678901', 'Argentina', 'Buenos Aires', NULL, 'Externo', NULL, 'LinkedIn', 'Innovación en educación', '2026-02-10 16:20:00');


-- =====================================
-- CONVOCATORIAS
-- =====================================
INSERT INTO convocatoria (nombre, fecha_cierre) VALUES 
('Convocatoria Summer 2026', '2026-03-31 23:59:59'),
('Convocatoria Winter 2026', '2026-09-30 23:59:59');


-- =====================================
-- ESTADOS
-- =====================================


-- -------------------------
-- POSTULACIONES
-- -------------------------
INSERT INTO catalogo_estados (nombre_estado, tipo_caso) VALUES 
('Postulado', 'Postulacion'),
('En revisión', 'Postulacion'),
('Evaluar', 'Postulacion'),
('En pausa', 'Postulacion'),
('Rechazado', 'Postulacion'),
('Aprobado', 'Postulacion'),
('En proyecto', 'Postulacion');

-- -------------------------
-- PROYECTOS
-- -------------------------
INSERT INTO catalogo_estados (nombre_estado, tipo_caso) VALUES
('En Pausa', 'Proyecto'),
('VIN', 'Proyecto'),
('Semilla ANDE', 'Proyecto'),
('Semilla ANII', 'Proyecto'),
('Realizado', 'Proyecto'),
('Egresado', 'Proyecto'),
('Cancelado', 'Proyecto');



-- =====================================
-- PROGRAMAS
-- =====================================
INSERT INTO programa (nombre, activo) VALUES 
('Programa Incubación', TRUE),
('Programa Aceleración', TRUE),
('Programa Mentorías', TRUE);


-- =====================================
-- CASOS
-- =====================================
INSERT INTO caso (nombre_caso, descripcion, datos_chatbot, id_emprendedor, id_convocatoria, id_estado, fecha_creacion) VALUES 
('EcoApp - Reciclaje Inteligente',
 'Aplicación móvil para facilitar el reciclaje urbano mediante gamificación',
 '{"sector":"Tecnología","modelo":"B2C","estado_producto":"MVP en desarrollo"}',
 1, 1, 2, '2026-01-15 11:00:00'),

('AgriTech Solutions',
 'Plataforma de agricultura de precisión con IoT para pequeños productores',
 '{"sector":"AgTech","modelo":"B2B","estado_producto":"Idea validada"}',
 2, 1, 3, '2026-01-20 15:00:00'),

('EduPlay',
 'Plataforma educativa gamificada para niños de primaria',
 '{"sector":"EdTech","modelo":"B2B2C","estado_producto":"Prototipo"}',
 3, 1, 1, '2026-02-01 10:00:00'),

('HealthConnect',
 'Telemedicina accesible para zonas rurales',
 '{"sector":"HealthTech","modelo":"B2C","estado_producto":"Solo idea"}',
 4, 1, 1, '2026-02-10 17:00:00');

-- CATALOGO APOYO

INSERT INTO catalogo_apoyo (nombre, descripcion) VALUES
('Ningún apoyo adicional (No UCU y no valor estratégico)', ''),
('IPE Postulación VIN ANII/ANDE', ''),
('IPE Postulación Semilla ANDE', ''),
('IPE Emprendedores innovadores ANII', ''),
('Otros Financiamientos', ''),
('Programa de incubación general', ''),
('Cursos de Uruguay Emprendedor', ''),
('Valida Lab UCU', ''),
('Mentoría / Tutoría', ''),
('Ingreso al catálogo de emprendimientos', ''),
('Acceso a laboratorios (Industrial, Alimentos Química, electrónica, IoT)', ''),
('Club de beneficios', ''),
('Centro Ignis (Industrias creativas)', ''),
('Comunidad UCU', ''),
('Actividades de Networking', ''),
('Tema para retos FIT', ''),
('Becario/s', ''),
('Sesión de IA (investigación mercado, estrategias, etc)', ''),
('Otras', '');


-- -- =====================================
-- -- ASIGNACIONES
-- -- =====================================
-- INSERT INTO asignacion (id_usuario, id_caso, fecha_asignacion) VALUES 
-- (2, 1, '2026-01-16 09:00:00'),
-- (3, 2, '2026-01-21 10:00:00'),
-- (2, 3, '2026-02-02 11:00:00'),
-- (3, 4, '2026-02-11 09:30:00');

-- COMENTADA PORQUE NO HAY USUARIOS. EJECUTAR DESPUÉS DE LA CREACIÓN DE USUARIOS