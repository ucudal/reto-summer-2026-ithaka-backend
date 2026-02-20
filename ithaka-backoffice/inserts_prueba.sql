-- Inserts de prueba para Ithaka Backoffice 

-- ROL
INSERT INTO rol (id_rol, nombre_rol) VALUES
(1, 'Administrador'),
(2, 'Coordinador'),
(3, 'Evaluador');

-- USUARIO
INSERT INTO usuario (id_usuario, nombre, email, password_hash, activo, id_rol) VALUES
(1, 'Admin Uno', 'admin1@ithaka.test', '$2b$12$hashadmin1', TRUE, 1),
(2, 'Coord Uno', 'coord1@ithaka.test', '$2b$12$hashcoord1', TRUE, 2),
(3, 'Eval Uno', 'eval1@ithaka.test', '$2b$12$hasheval1', TRUE, 3),
(4, 'Usuario Inactivo', 'inactive@ithaka.test', '$2b$12$hashinactive', FALSE, 2);

-- EMPRENDEDOR
INSERT INTO emprendedor (id_emprendedor, nombre, email, telefono, vinculo_institucional, fecha_registro) VALUES
(1, 'Emprendedor A', 'emp_a@ithaka.test', '+56911111111', 'Universidad X', '2026-01-10 09:00:00'),
(2, 'Emprendedor B', 'emp_b@ithaka.test', '+56922222222', 'Incubadora Y', '2026-01-15 10:30:00'),
(3, 'Emprendedor C', 'emp_c@ithaka.test', '+56933333333', 'Comunidad Z', '2026-01-20 11:45:00');

-- CONVOCATORIA
INSERT INTO convocatoria (id_convocatoria, nombre, fecha_cierre) VALUES
(1, 'Convocatoria Enero', '2026-03-31 23:59:59'),
(2, 'Convocatoria Abril', '2026-06-30 23:59:59'),
(3, 'Convocatoria Agosto', '2026-09-30 23:59:59');

-- CATALOGO_ESTADOS
INSERT INTO catalogo_estados (id_estado, nombre_estado, tipo_caso) VALUES
(1, 'Postulado', 'Postulacion'),
(2, 'En Evaluación', 'Postulacion'),
(3, 'Aprobado Proyecto', 'Proyecto');

-- PROGRAMA
INSERT INTO programa (id_programa, nombre, activo) VALUES
(1, 'Programa Semilla', TRUE),
(2, 'Programa Crecimiento', TRUE),
(3, 'Programa Internacional', FALSE);

-- CASO
INSERT INTO caso (id_caso, fecha_creacion, nombre_caso, descripcion, datos_chatbot, consentimiento_datos, id_emprendedor, id_convocatoria, id_estado) VALUES
(1, '2026-01-11 08:00:00', 'Caso A', 'Descripción breve A', '{"interes":"alto","canal":"web"}', TRUE, 1, 1, 1),
(2, '2026-01-16 09:15:00', 'Caso B', 'Descripción breve B', '{"interes":"medio","canal":"email"}', FALSE, 2, 2, 2),
(3, '2026-01-21 10:30:00', 'Caso C', 'Descripción breve C', '{"interes":"bajo","canal":"telefono"}', TRUE, 3, 3, 3);

-- APOYO
INSERT INTO apoyo (id_apoyo, tipo_apoyo, fecha_inicio, fecha_fin, id_caso, id_programa) VALUES
(1, 'Mentoría', '2026-02-01', '2026-03-01', 1, 1),
(2, 'Capacitación', '2026-02-15', '2026-04-15', 2, 2),
(3, 'Financiamiento', '2026-03-01', '2026-09-01', 3, 1);

-- ASIGNACION
INSERT INTO asignacion (id_asignacion, fecha_asignacion, id_usuario, id_caso) VALUES
(1, '2026-01-12 12:00:00', 1, 1),
(2, '2026-01-17 13:00:00', 2, 2),
(3, '2026-01-22 14:00:00', 3, 3);

-- NOTA
INSERT INTO nota (id_nota, contenido, fecha, id_usuario, id_caso) VALUES
(1, 'Nota inicial del administrador', '2026-01-12 12:05:00', 1, 1),
(2, 'Observación de coordinación', '2026-01-17 13:10:00', 2, 2),
(3, 'Comentario del evaluador', '2026-01-22 14:20:00', 3, 3);

-- AUDITORIA
INSERT INTO auditoria (id_auditoria, timestamp, accion, valor_anterior, valor_nuevo, id_usuario, id_caso) VALUES
(1, '2026-01-12 12:06:00', 'Creación de caso', NULL, 'Caso creado (id=1)', 1, 1),
(2, '2026-01-17 13:11:00', 'Cambio de estado', 'Postulado', 'En Evaluación', 2, 2),
(3, '2026-01-22 14:21:00', 'Actualización nota', 'Nota vieja', 'Nota actualizada', 3, 3);