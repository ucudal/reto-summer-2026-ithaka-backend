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
-- Las contraseñas están indicadas en comentario al lado para pruebas
INSERT INTO usuario (nombre, apellido, email, password_hash, activo, id_rol) VALUES
('Lucía', 'Gómez', 'lucia.gomez@example.com', 'pbkdf2$sha256$10000$abc123$hashedpassword1', TRUE, 1), -- pass: lucia123
('Diego', 'Martínez', 'diego.martinez@example.com', 'pbkdf2$sha256$10000$def456$hashedpassword2', TRUE, 2), -- pass: diego123
('Carla', 'Fernández', 'carla.fernandez@example.com', 'pbkdf2$sha256$10000$ghi789$hashedpassword3', TRUE, 3); -- pass: carla123

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
-- CATALOGO_ESTADOS
-- =====================================
-- Postulaciones
INSERT INTO catalogo_estados (nombre_estado, tipo_caso) VALUES
('Postulado', 'Postulacion'),
('En revisión', 'Postulacion'),
('Evaluar', 'Postulacion'),
('En pausa', 'Postulacion'),
('Rechazado', 'Postulacion'),
('Aprobado', 'Postulacion'),
('En proyecto', 'Postulacion');

-- Proyectos
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

-- =====================================
-- CATALOGO_APOYO
-- =====================================
INSERT INTO catalogo_apoyo (nombre, descripcion, activo) VALUES
('Ningún apoyo adicional (No UCU y no valor estratégico)', '', TRUE),
('IPE Postulación VIN ANII/ANDE', '', TRUE),
('IPE Postulación Semilla ANDE', '', TRUE),
('IPE Emprendedores innovadores ANII', '', TRUE),
('Otros Financiamientos', '', TRUE),
('Programa de incubación general', '', TRUE),
('Cursos de Uruguay Emprendedor', '', TRUE),
('Valida Lab UCU', '', TRUE),
('Mentoría / Tutoría', '', TRUE),
('Ingreso al catálogo de emprendimientos', '', TRUE),
('Acceso a laboratorios (Industrial, Alimentos, Química, electrónica, IoT)', '', TRUE),
('Club de beneficios', '', TRUE),
('Centro Ignis (Industrias creativas)', '', TRUE),
('Comunidad UCU', '', TRUE),
('Actividades de Networking', '', TRUE),
('Tema para retos FIT', '', TRUE),
('Becario/s', '', TRUE),
('Sesión de IA (investigación mercado, estrategias, etc)', '', TRUE),
('Otras', '', TRUE);

-- =====================================
-- APOYO
-- =====================================
INSERT INTO apoyo (id_catalogo_apoyo, fecha_inicio, fecha_fin, id_caso, id_programa) VALUES
(1, '2026-01-16', '2026-02-16', 1, 1),
(2, '2026-01-21', '2026-03-21', 2, 2),
(3, '2026-02-02', '2026-04-02', 3, 3);

-- =====================================
-- APOYO_SOLICITADO
-- =====================================
INSERT INTO apoyo_solicitado (id_catalogo_apoyo, id_caso) VALUES
(1, 1),
(2, 2),
(3, 3);

-- =====================================
-- ASIGNACION
-- =====================================
INSERT INTO asignacion (id_usuario, id_caso, fecha_asignacion) VALUES
(2, 1, '2026-01-16 09:00:00'),
(3, 2, '2026-01-21 10:00:00'),
(2, 3, '2026-02-02 11:00:00'),
(3, 4, '2026-02-11 09:30:00');

-- =====================================
-- NOTA
-- =====================================
INSERT INTO nota (contenido, tipo_nota, fecha, id_usuario, id_caso) VALUES
('Revisión inicial realizada', 'Interna', '2026-01-16 09:30:00', 2, 1),
('Se requiere feedback del equipo', 'Interna', '2026-01-21 10:30:00', 3, 2),
('Prototipo aprobado por mentor', 'Interna', '2026-02-02 11:30:00', 2, 3),
('Idea de telemedicina evaluada', 'Interna', '2026-02-11 10:00:00', 3, 4);

-- =====================================
-- AUDITORIA
-- =====================================
INSERT INTO auditoria (accion, valor_anterior, valor_nuevo, id_usuario, id_caso, timestamp) VALUES
('Caso creado', NULL, 'EcoApp - Reciclaje Inteligente', 2, 1, '2026-01-15 11:00:00'),
('Caso actualizado', 'Idea', 'MVP en desarrollo', 3, 2, '2026-01-20 15:30:00'),
('Caso asignado', NULL, 'EduPlay asignado a tutor', 2, 3, '2026-02-02 11:00:00'),
('Caso revisado', NULL, 'HealthConnect evaluación inicial', 3, 4, '2026-02-10 17:30:00');