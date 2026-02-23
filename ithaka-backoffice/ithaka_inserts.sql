
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
INSERT INTO usuario (nombre, apellido, email, password_hash, activo, id_rol) VALUES 
('Juan', 'Pérez', 'juan.perez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIHe.8YY7O', TRUE, 1),
('María', 'González', 'maria.gonzalez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIHe.8YY7O', TRUE, 2),
('Pedro', 'Rodríguez', 'pedro.rodriguez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIHe.8YY7O', TRUE, 3);


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
INSERT INTO catalogo_estados (nombre_estado, tipo_caso) VALUES 
('Postulado', 'postulacion'),
('En evaluación', 'postulacion'),
('En programa', 'proyecto'),
('Activo', 'proyecto'),
('Finalizado', 'proyecto'),
('Rechazado', 'postulacion');


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
INSERT INTO caso (nombre_caso, descripcion, datos_chatbot, consentimiento_datos, id_emprendedor, id_convocatoria, id_estado, fecha_creacion) VALUES 
('EcoApp - Reciclaje Inteligente',
 'Aplicación móvil para facilitar el reciclaje urbano mediante gamificación',
 '{"sector":"Tecnología","modelo":"B2C","estado_producto":"MVP en desarrollo"}',
 TRUE, 1, 1, 2, '2026-01-15 11:00:00'),

('AgriTech Solutions',
 'Plataforma de agricultura de precisión con IoT para pequeños productores',
 '{"sector":"AgTech","modelo":"B2B","estado_producto":"Idea validada"}',
 TRUE, 2, 1, 3, '2026-01-20 15:00:00'),

('EduPlay',
 'Plataforma educativa gamificada para niños de primaria',
 '{"sector":"EdTech","modelo":"B2B2C","estado_producto":"Prototipo"}',
 TRUE, 3, 1, 1, '2026-02-01 10:00:00'),

('HealthConnect',
 'Telemedicina accesible para zonas rurales',
 '{"sector":"HealthTech","modelo":"B2C","estado_producto":"Solo idea"}',
 TRUE, 4, 1, 1, '2026-02-10 17:00:00');


-- =====================================
-- ASIGNACIONES
-- =====================================
INSERT INTO asignacion (id_usuario, id_caso, fecha_asignacion) VALUES 
(2, 1, '2026-01-16 09:00:00'),
(3, 2, '2026-01-21 10:00:00'),
(2, 3, '2026-02-02 11:00:00'),
(3, 4, '2026-02-11 09:30:00');