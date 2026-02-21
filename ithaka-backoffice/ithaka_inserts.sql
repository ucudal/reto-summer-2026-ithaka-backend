-- Roles
INSERT INTO rol (nombre_rol) VALUES 
    ('Admin'),
    ('Coordinador'),
    ('Tutor');

-- Usuarios
INSERT INTO usuario (nombre, email, password_hash, activo, id_rol) VALUES 
    ('Juan Pérez', 'juan.perez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIHe.8YY7O', TRUE, 1),
    ('María González', 'maria.gonzalez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIHe.8YY7O', TRUE, 2),
    ('Pedro Rodríguez', 'pedro.rodriguez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIHe.8YY7O', TRUE, 3);

-- Emprendedores
INSERT INTO emprendedor (nombre, apellido, email, telefono, documento_identidad, pais_residencia, ciudad_residencia, campus_ucu, relacion_ucu, facultad_ucu, canal_llegada, motivacion, fecha_registro) VALUES 
    ('Ana', 'Martínez', 'ana.martinez@example.com', '+598 91 234 567', '12345678', 'Uruguay', 'Montevideo', 'Campus Montevideo', 'Estudiante', 'Ingeniería', 'Web', 'Quiero desarrollar mi startup tecnológica', '2026-01-15 10:30:00'),
    ('Carlos', 'López', 'carlos.lopez@example.com', '+598 92 345 678', '23456789', 'Uruguay', 'Montevideo', 'Campus Montevideo', 'Egresado', 'Empresariales', 'Referido', 'Tengo una idea de negocio sostenible', '2026-01-20 14:45:00'),
    ('Laura', 'Fernández', 'laura.fernandez@example.com', '+598 93 456 789', '34567890', 'Uruguay', 'Salto', 'Campus Salto', 'Estudiante', 'Comunicación', 'Chatbot', 'Proyecto social con impacto', '2026-02-01 09:15:00'),
    ('Diego', 'Silva', 'diego.silva@example.com', '+598 94 567 890', '45678901', 'Argentina', 'Buenos Aires', NULL, 'Externo', NULL, 'LinkedIn', 'Innovación en educación', '2026-02-10 16:20:00');

-- Convocatorias
INSERT INTO convocatoria (nombre, fecha_cierre) VALUES 
    ('Convocatoria Summer 2026', '2026-03-31 23:59:59'),
    ('Convocatoria Winter 2026', '2026-09-30 23:59:59');

-- Catálogo de Estados
INSERT INTO catalogo_estados (nombre_estado, tipo_caso) VALUES 
    ('Postulado', 'postulacion'),
    ('En evaluación', 'postulacion'),
    ('En programa', 'proyecto'),
    ('Activo', 'proyecto'),
    ('Finalizado', 'proyecto'),
    ('Rechazado', 'postulacion');

-- Programas
INSERT INTO programa (nombre, activo) VALUES 
    ('Programa Incubación', TRUE),
    ('Programa Aceleración', TRUE),
    ('Programa Mentorías', TRUE);

-- Casos
INSERT INTO caso (nombre_caso, descripcion, datos_chatbot, consentimiento_datos, id_emprendedor, id_convocatoria, id_estado, fecha_creacion) VALUES 
    ('EcoApp - Reciclaje Inteligente', 
     'Aplicación móvil para facilitar el reciclaje urbano mediante gamificación', 
     '{"pregunta1": "Tecnología", "pregunta2": "Impacto ambiental", "pregunta3": "B2C", "pregunta4": "MVP en desarrollo", "pregunta5": "1-2 personas", "pregunta6": "Sí", "pregunta7": "Financiamiento y mentoría", "pregunta8": "Próximos 6 meses", "pregunta9": "Uruguay", "pregunta10": "Medio ambiente"}',
     TRUE, 1, 1, 2, '2026-01-15 11:00:00'),
    
    ('AgriTech Solutions', 
     'Plataforma de agricultura de precisión con IoT para pequeños productores', 
     '{"pregunta1": "AgTech", "pregunta2": "Aumentar productividad agrícola", "pregunta3": "B2B", "pregunta4": "Idea validada", "pregunta5": "3-4 personas", "pregunta6": "Sí", "pregunta7": "Acceso a inversores", "pregunta8": "Este año", "pregunta9": "Uruguay y región", "pregunta10": "Agricultura"}',
     TRUE, 2, 1, 3, '2026-01-20 15:00:00'),
    
    ('EduPlay', 
     'Plataforma educativa gamificada para niños de primaria', 
     '{"pregunta1": "EdTech", "pregunta2": "Mejorar aprendizaje", "pregunta3": "B2B2C", "pregunta4": "Prototipo", "pregunta5": "2-3 personas", "pregunta6": "No", "pregunta7": "Desarrollo tecnológico", "pregunta8": "Próximo año", "pregunta9": "Uruguay", "pregunta10": "Educación"}',
     TRUE, 3, 1, 1, '2026-02-01 10:00:00'),
    
    ('HealthConnect', 
     'Telemedicina accesible para zonas rurales', 
     '{"pregunta1": "HealthTech", "pregunta2": "Acceso a salud", "pregunta3": "B2C", "pregunta4": "Solo idea", "pregunta5": "1 persona", "pregunta6": "No", "pregunta7": "Validación y networking", "pregunta8": "En 2 años", "pregunta9": "Latinoamérica", "pregunta10": "Salud"}',
     TRUE, 4, 1, 1, '2026-02-10 17:00:00');

-- Asignaciones
INSERT INTO asignacion (id_usuario, id_caso, fecha_asignacion) VALUES 
    (2, 1, '2026-01-16 09:00:00'),
    (3, 2, '2026-01-21 10:00:00'),
    (2, 3, '2026-02-02 11:00:00'),
    (3, 4, '2026-02-11 09:30:00');

-- Apoyos otorgados
INSERT INTO apoyo (tipo_apoyo, fecha_inicio, fecha_fin, id_caso, id_programa) VALUES 
    ('Incubación inicial', '2026-02-01', '2026-05-31', 2, 1),
    ('Mentoría técnica', '2026-02-15', '2026-03-15', 2, 3);

-- Apoyos solicitados
INSERT INTO apoyo_solicitado (categoria_apoyo, id_caso) VALUES 
    ('Financiamiento', 1),
    ('Mentoría', 1),
    ('Networking', 1),
    ('Acceso a inversores', 2),
    ('Validación de mercado', 2),
    ('Desarrollo tecnológico', 3),
    ('Mentoría pedagógica', 3),
    ('Validación', 4),
    ('Networking', 4);

-- Notas
INSERT INTO nota (contenido, tipo_nota, id_usuario, id_caso, fecha) VALUES 
    ('Primera reunión realizada. Emprendedor muy motivado, tiene claro el problema a resolver.', 'comentario_postulante', 2, 1, '2026-01-16 14:30:00'),
    ('Equipo técnico sólido. Recomiendo pasar a fase de incubación.', 'nota_staff', 3, 2, '2026-01-22 11:00:00'),
    ('Proyecto aceptado en programa de incubación. Inicio: 1 de febrero.', 'comentario_postulante', 3, 2, '2026-01-25 16:00:00'),
    ('Necesita trabajar más en la propuesta de valor. Agendar segunda reunión.', 'nota_staff', 2, 3, '2026-02-03 10:15:00'),
    ('Idea interesante pero muy temprana. Sugerimos volver cuando tenga más avance.', 'comentario_postulante', 3, 4, '2026-02-12 15:45:00');

-- Auditoría
INSERT INTO auditoria (accion, valor_anterior, valor_nuevo, id_usuario, id_caso, timestamp) VALUES 
    -- Caso 1: EcoApp
    ('Asignación de staff', NULL, 'María González', 2, 1, '2026-01-16 09:00:00'),
    ('Cambio de estado', 'Postulado', 'En evaluación', 2, 1, '2026-01-16 09:05:00'),
    
    -- Caso 2: AgriTech Solutions
    ('Asignación de staff', NULL, 'Pedro Rodríguez', 3, 2, '2026-01-21 10:00:00'),
    ('Cambio de estado', 'Postulado', 'En programa', 3, 2, '2026-01-25 16:05:00'),
    ('Apoyo otorgado', NULL, 'Incubación inicial - Programa Incubación', 3, 2, '2026-02-01 09:00:00'),
    ('Apoyo otorgado', NULL, 'Mentoría técnica - Programa Mentorías', 3, 2, '2026-02-15 10:00:00'),
    
    -- Caso 3: EduPlay
    ('Asignación de staff', NULL, 'María González', 2, 3, '2026-02-02 11:00:00'),
    ('Cambio de estado', 'Postulado', 'En evaluación', 2, 3, '2026-02-02 11:05:00'),
    
    -- Caso 4: HealthConnect
    ('Asignación de staff', NULL, 'Pedro Rodríguez', 3, 4, '2026-02-11 09:30:00');