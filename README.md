# reto-summer-2026-ithaka-backend
Proyecto Ithaka 2.0

DOCUMENTACIÓN TÉCNICA DEL PROYECTO: Ithaka Backoffice

1. Propósito del documento

Este documento está pensado como entrega formal y referencia completa para cualquier desarrollador, integrador o auditor externo que necesite comprender la lógica, los endpoints, la estructura de la base de datos y las decisiones de diseño del proyecto "Ithaka Backoffice".

Describe: 
- Estructura general del repositorio y archivos clave.
- Flujo de autenticación y seguridad.
- Todos los endpoints expuestos por la API: rutas, métodos, parámetros, validaciones, roles, schemas de entrada y salida, ejemplos y errores esperados.
- Modelos de datos (tablas), columnas, relaciones, restricciones y comportamiento (soft delete, JSON fields, check constraints).
- Servicios auxiliares (auditoría, exportación CSV) y sus contratos.
- Consideraciones, riesgos y recomendaciones para mantenimiento y evolución.

Audiencia: desarrolladores backend, QA, DevOps, integradores.


2. Estructura del proyecto 

Raíz relevante: `ithaka-backoffice/app`

Carpetas principales:
- `app/api/v1/endpoints/` : Routers por recurso (auth, usuarios, casos, apoyos, asignaciones, notas, roles, convocatorias, catalogos, auditoria, metricas)
- `app/models/` : Modelos SQLAlchemy que representan tablas (Usuario, Rol, Caso, Emprendedor, Convocatoria, CatalogoEstados, CatalogoApoyo, Apoyo, ApoyoSolicitado, Programa, Asignacion, Nota, Auditoria)
- `app/schemas/` : Pydantic schemas para validación de requests/responses (uno por recurso)
- `app/db/` : Configuración de base de datos (engine, SessionLocal) y dependencia `get_db`
- `app/core/` : Configuración y seguridad (`config.py` y `security.py`)
- `app/services/` : Servicios auxiliares reutilizables (auditoría, exportación)
- `app/api/deps.py` : Dependencias comunes (get_db, etc.) — usado por endpoints
- `tests/` : Tests unitarios/integración

Archivo de configuración: `app/core/config.py` (usa `.env` por default). La conexión a DB se construye con variables POSTGRES_*.

SQL de estructura: `ithaka_backoffice.sql` en raíz del repositorio (útil para revisar el DDL real en PostgreSQL).



3. Cómo levantar localmente (resumen operativo)

Requisitos previos:
- Python 3.10+ (ver `requirements.txt`)
- PostgreSQL si se quiere usar DB real (o SQLite para pruebas locales si se ajusta la URL)

Variables de entorno (ver `app/core/config.py`):
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_SERVER (default localhost)
- POSTGRES_PORT (default 5432)
- SECRET_KEY (JWT secret)
- ALGORITHM (HS256 por default)
- ACCESS_TOKEN_EXPIRE_MINUTES (ej: 30)
- REFRESH_TOKEN_EXPIRE_DAYS (ej: 30)

Comandos básicos:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# Exportar env vars o crear .env con las keys
uvicorn app.main:app --reload --port 8000

Nota: el proyecto no incluye migraciones automáticas (Alembic). El DDL está en `ithaka_backoffice.sql` y los modelos están en `app/models/`.


4. Seguridad y autenticación
Tipo: JWT (JSON Web Tokens)
Mecanismo:
- Login con `POST /api/v1/auth/login` (body: `email`, `password`). Respuesta: access_token y refresh_token.
- `access_token` tiene expiración corta (`ACCESS_TOKEN_EXPIRE_MINUTES`, por defecto 30 minutos).
- `refresh_token` tiene expiración mayor (`REFRESH_TOKEN_EXPIRE_DAYS`).
- Para endpoints protegidos, se usa el header: `Authorization: Bearer {access_token}`.

Funciones clave en `app/core/security.py`:
- `hash_password(password)` : bcrypt para hashear contraseña.
- `verify_password(plain, hash)` : compara plain con hash.
- `create_access_token(data, expires_delta)` : genera JWT con `exp` y firma con `SECRET_KEY`.
- `create_refresh_token(data, expires_delta)` : token de refresh similar.
- `decode_access_token(token)` / `decode_refresh_token(token)` : decodifican y validan.
- `security` : `HTTPBearer()` para integrarse con Swagger UI.
- `get_current_user(credentials, db)` : dependency que extrae el usuario a partir del access token.
- `require_role(allowed_roles)` : fábrica de dependencia que valida que `current_user.rol.nombre_rol` esté en `allowed_roles`.

Notas importantes:
- El logout no invalida tokens por defecto: `POST /api/v1/auth/logout` está implementado para logging, pero la invalidación real solo existe si se implementa blacklist/tabla de tokens.
- `require_role` compara exactamente el nombre del rol. Mantener consistencia en nombres (`Admin`, `Coordinador`, `Tutor`, etc.). Cambiar mayúsculas/minúsculas puede romper verificaciones.


5. Base de datos: modelos, columnas y relaciones
Resumen general: la app usa SQLAlchemy ORM. El engine se crea en `app/db/database.py` con `create_engine(settings.DATABASE_URL)`. Las sesiones se crean con `SessionLocal` y la dependencia `get_db` en `app/db/session.py` cierra la sesión al terminar.

Para cada tabla se indica: columnas, propósito, relaciones, restricciones y notas.

5.1 `usuario` (app/models/usuario.py)
- Tabla: `usuario`
- Columnas:
  - `id_usuario` INTEGER PRIMARY KEY AUTOINCREMENT/serial
  - `nombre` VARCHAR(150) NOT NULL
  - `apellido` VARCHAR(150) NULL
  - `email` VARCHAR(150) NOT NULL UNIQUE
  - `password_hash` TEXT NOT NULL
  - `activo` BOOLEAN NOT NULL DEFAULT TRUE
  - `id_rol` INTEGER NOT NULL FK -> `rol.id_rol`
- Propósito: Almacenar cuentas de acceso del personal que administra o interactúa con la plataforma (credenciales, estado y rol).
- Relaciones:
  - `rol` : relationship hacia `Rol` (many-to-one). Back-populates: `usuarios` en `Rol`.
  - Puede relacionarse a `Asignacion`, `Nota`, `Auditoria` (referencias en otros modelos y endpoints).
- Observaciones:
  - Se usa `activo` para soft-delete (no se borran físicamente los usuarios para preservar auditorías y relaciones).
  - `password_hash` NUNCA se expone por schemas de respuesta.

5.2 `rol` (app/models/rol.py)
- Tabla: `rol`
- Columnas:
  - `id_rol` INTEGER PK
  - `nombre_rol` VARCHAR(50) NOT NULL UNIQUE
- Relaciones:
  - `usuarios` (one-to-many)
- Observaciones:
  - Los endpoints de `rol` validan unicidad y no permiten eliminar roles con usuarios asociados.
- Propósito: Definir niveles de permiso y agrupar permisos por tipo para asignarlos a `usuario`.

5.3 `emprendedor` (app/models/emprendedor.py)
- Tabla: `emprendedor`
- Columnas: `id_emprendedor`, `nombre`, `apellido`, `email`, `telefono`, `documento_identidad`, `pais_residencia`, `ciudad_residencia`, `campus_ucu`, `relacion_ucu`, `facultad_ucu`, `canal_llegada`, `motivacion`, `fecha_registro`.
- Relaciones: `casos` (un emprendedor puede tener muchos casos).
- Observaciones: Los endpoints no eliminan emprendedores por integridad.
- Propósito: Guardar la información de las personas emprendedoras que postulan o participan en proyectos, para vincularla con sus `casos`.

5.4 `convocatoria` (app/models/convocatoria.py)
- Tabla: `convocatoria`
- Columnas: `id_convocatoria`, `nombre`, `fecha_cierre`.
- Relaciones: `casos` back_populates con `Caso.convocatoria`.
- Observaciones: Eliminación física está deshabilitada por integridad (endpoints comentados).
- Propósito: Representar una convocatoria o llamada a postulación, para agrupar casos por periodo/edición.

5.5 `catalogo_estados` (app/models/catalogo_estados.py)
- Tabla: `catalogo_estados`
- Columnas: `id_estado`, `nombre_estado`, `tipo_caso`.
- Restricciones: `CheckConstraint(lower(tipo_caso) IN ('postulacion','proyecto'))`.
- Observaciones: El modelo valida y normaliza `nombre_estado` y `tipo_caso` a minúsculas con `@validates`.
- Propósito: Mantener el catálogo de estados posibles para clasificar y controlar el flujo de los `caso` según su `tipo_caso`.

5.6 `caso` (app/models/caso.py)
- Tabla: `caso`
- Columnas:
  - `id_caso` INTEGER PK
  - `fecha_creacion` DateTime DEFAULT now()
  - `nombre_caso` VARCHAR(200) NOT NULL
  - `descripcion` TEXT
  - `datos_chatbot` JSON (JSON/JSONB según DB)
  - `id_emprendedor` FK -> `emprendedor.id_emprendedor` NOT NULL
  - `id_convocatoria` FK -> `convocatoria.id_convocatoria` NULLABLE
  - `id_estado` FK -> `catalogo_estados.id_estado` NOT NULL
- Relaciones:
  - `emprendedor` backref `casos`
  - `convocatoria` back_populates `casos`
  - `estado` backref `casos`
  - `asignaciones` relationship con `Asignacion` (back_populates)
- Observaciones:
  - `datos_chatbot` puede contener estructura libre JSON. En PostgreSQL conviene JSONB y consultas del tipo `datos_chatbot->>'campo'`.
  - Muchos endpoints devuelven una vista serializada del caso con campos calculados (nombre_estado, tipo_caso, tutor_nombre, etc.).
- Propósito: Entidad principal que representa una postulación o proyecto de un emprendedor; centraliza estado, datos del chatbot, convocatoria y relaciones con asignaciones, apoyos y notas.

5.7 `catalogo_apoyo` (app/models/catalogo_apoyo.py)
- Tabla: `catalogo_apoyo`
- Columnas: `id_catalogo_apoyo`, `nombre` UNIQUE NOT NULL, `descripcion`, `activo` BOOLEAN.
- Propósito: Tipos/categorías de apoyo.


5.8 `apoyo` (app/models/apoyo.py)
- Tabla: `apoyo`
- Columnas: `id_apoyo`, `id_catalogo_apoyo` FK, `fecha_inicio`, `fecha_fin`, `id_caso` FK NOT NULL, `id_programa` FK NOT NULL.
- Observaciones: Representa apoyos efectivamente otorgados a un caso.
- Propósito: Registrar intervenciones/beneficios concretos asignados a un caso (fechas, programa y tipo de apoyo), para seguimiento y reporting.

5.9 `apoyo_solicitado` (app/models/apoyo_solicitado.py)
- Tabla: `apoyo_solicitado`
- Columnas: `id_apoyo_solicitado`, `id_catalogo_apoyo` FK NOT NULL, `id_caso` FK NOT NULL.
- Propósito: Indica qué tipos de apoyo solicitó el caso (lista de preferencias/solicitudes).

5.10 `programa` (app/models/programa.py)
- Tabla: `programa`
- Columnas: `id_programa`, `nombre`, `activo`.
- Relaciones: `apoyos` (backref desde `Apoyo`).
- Propósito: Modelar las líneas o programas institucionales que financian o administran apoyos a los casos.

5.11 `asignacion` (app/models/asignacion.py)
- Tabla: `asignacion`
- Columnas: `id_asignacion`, `fecha_asignacion` TIMESTAMP DEFAULT now(), `id_usuario` FK NOT NULL, `id_caso` FK NOT NULL.
- Relaciones: `usuario` (backref `asignaciones`), `caso` back_populates `asignaciones`.
- Observaciones: Un tutor puede estar asignado a múltiples casos; una asignación es única por par (id_usuario, id_caso) validada en lógica del endpoint.
- Propósito: Registrar qué usuario (tutor) está responsable de un caso en un momento dado, para control de responsabilidades y notificaciones.

5.12 `nota` (app/models/nota.py)
- Tabla: `nota`
- Columnas: `id_nota`, `contenido`, `tipo_nota`, `fecha` TIMESTAMP DEFAULT now(), `id_usuario` FK NOT NULL, `id_caso` FK NOT NULL.
- Propósito: Registro de anotaciones o seguimientos realizados por staff.

5.13 `auditoria` (app/models/auditoria.py)
- Tabla: `auditoria`
- Columnas: `id_auditoria`, `timestamp`, `accion`, `valor_anterior`, `valor_nuevo`, `id_usuario` FK NOT NULL, `id_caso` FK NULLABLE.
- Observaciones: Registro de trazabilidad de acciones. Los helpers en `app/services/auditoria_service.py` serializan valores (JSON/text) y añaden el registro a la sesión, pero NO hacen commit.
- Propósito: Mantener un historial inmutable de cambios y acciones relevantes del sistema para auditoría, investigación y trazabilidad.


6. Endpoints: descripción detallada por recurso

NOTA: todos los endpoints están bajo el prefijo base `/api/v1` (convención del proyecto). A continuación se listan rutas, métodos, roles y comportamiento.

6.1 AUTH (`app/api/v1/endpoints/auth.py`)
- POST /api/v1/auth/login
  - Body: `LoginRequest` ({"email":EmailStr, "password":str}).
  - Respuesta: `LoginResponse` ({access_token, refresh_token, token_type, ACCESS_TOKEN_EXPIRE_MINUTES, usuario}).
  - Lógica: valida credenciales, verifica `usuario.activo`, crea `access_token` y `refresh_token` con payload `{ sub, email, rol }`.
  - Errores: 401 si email no existe o password incorrecto; 403 si usuario inactivo.

- GET /api/v1/auth/me
  - Requiere Authorization Bearer token.
  - Respuesta: `UsuarioActual` (id_usuario, nombre, email, rol).
  - Lógica: `get_current_user` decodifica token y recupera usuario de la DB.

- POST /api/v1/auth/logout
  - Requiere Authorization.
  - No invalida tokens por defecto. Se puede usar para auditoría o agregar blacklist si se implementa.
  - Respuesta: message "Logout exitoso".

- POST /api/v1/auth/refresh
  - Body: `RefreshRequest` ({refresh_token}).
  - Respuesta: `RefreshResponse` ({access_token, token_type}).
  - Lógica: decodifica refresh token, valida usuario activo y genera nuevo access token.
  - Errores: 401 si refresh token inválido o usuario inactivo.

6.2 USUARIOS (`app/api/v1/endpoints/usuario.py`)
- GET /api/v1/usuarios/
  - Roles: Admin, Coordinador
  - Query params: `skip`, `limit`.
  - Respuesta: List[`UsuarioResponse`].

- GET /api/v1/usuarios/{usuario_id}
  - Roles: Admin, Coordinador, Tutor (pero Tutor solo su propio perfil).
  - Errores: 403 si Tutor intenta ver otro usuario; 404 si usuario no existe.

- POST /api/v1/usuarios/
  - Roles: Admin
  - Body: `UsuarioCreate` (incluye `password`).
  - Lógica: valida rol existente, valida email único, hashea password con `hash_password`, crea `Usuario`, registra auditoría (`registrar_auditoria_general`) y commit.
  - Errores: 400 si rol inválido o email registrado.

- PUT /api/v1/usuarios/{usuario_id}
  - Roles: Admin, Coordinador, Tutor (pero no Admin puede cambiar su propio rol; Coordinador/Tutor solo su perfil)
  - Body: `UsuarioUpdate` (campos opcionales)
  - Lógica: validaciones de email único, solo Admin puede cambiar `id_rol` y no puede cambiar su propio rol.

- DELETE /api/v1/usuarios/{usuario_id}
  - Roles: Admin
  - Lógica: soft-delete (set `activo=False`). Protecciones: no puedes desactivar tu propio usuario. Auditoría registrada.
  - Respuesta: 204 No Content

- PUT /api/v1/usuarios/{usuario_id}/reactivar
  - Roles: Admin
  - Lógica: vuelve a poner `activo=True`.

6.3 ROLES (`app/api/v1/endpoints/rol.py`)
- GET /api/v1/roles/ (Admin)
- GET /api/v1/roles/{rol_id} (Admin)
- POST /api/v1/roles/ (Admin) Body: `RolCreate`.
  - Valida unicidad `nombre_rol`.
- PUT /api/v1/roles/{rol_id} (Admin)
  - Valida no duplicar nombre.
- DELETE /api/v1/roles/{rol_id} (Admin)
  - Solo permitido si no hay usuarios con ese rol. En caso contrario retorna 400 con conteo.

6.4 PROGRAMAS (`app/api/v1/endpoints/programa.py`)
- GET /api/v1/programas/ (Admin, Coordinador, Tutor)
- GET /api/v1/programas/{programa_id}
- POST /api/v1/programas/ (Admin o Coordinador)
- PUT /api/v1/programas/{programa_id} (Admin o Coordinador)
- DELETE /api/v1/programas/{programa_id} (Admin)
  - Validación: no permitir eliminar si hay `Apoyo` relacionados (cuenta y retorna 400 si >0).

6.5 CONVOCATORIAS (`app/api/v1/endpoints/convocatoria.py`)
- GET /api/v1/convocatorias/
- GET /api/v1/convocatorias/{id}
- POST /api/v1/convocatorias/ (Admin y Coordinador)
  - Registra auditoría con `registrar_auditoria_general` (nota: en código hay TODO temporal que usa id_usuario=1). Asegurarse de reemplazar por `current_user.id_usuario` cuando se estabilice JWT en todos los endpoints.
- PUT /api/v1/convocatorias/{id} (Admin y Coordinador)
- DELETE: deshabilitado por integridad (comentado).

6.6 EMPRENDEDORES (`app/api/v1/endpoints/emprendedores.py`)
- GET /api/v1/emprendedores/
  - Si `current_user` es Tutor, se filtra para devolver solo emprendedores con casos asignados a ese tutor.
- GET /api/v1/emprendedores/{id}
  - Tutor puede ver solo si tiene caso asignado al emprendedor.
- POST /api/v1/emprendedores/ (Admin)
- PUT /api/v1/emprendedores/{id} (Admin)
- GET /api/v1/emprendedores/{id}/casos -> devuelve `emprendedor.casos`.
- DELETE: deshabilitado (comentado) para preservar integridad referencial.

6.7 CASOS (`app/api/v1/endpoints/caso.py`)
- GET /api/v1/casos/
  - Filtros: `id_estado`, `tipo_caso`, `nombre_estado`, `id_emprendedor`, `id_convocatoria`, `id_tutor`.
  - Si `current_user` es Tutor, devuelve sólo casos asignados a ese tutor.
  - Devuelve una estructura normalizada con campos calculados: `nombre_estado`, `tipo_caso`, `emprendedor` (nombre completo), `convocatoria`, `tutor_nombre`, `id_tutor`, `asignacion`.

- GET /api/v1/casos/export
  - Exporta CSV (usa `ExportService`). Parámetro `con_tutores` determina formato con tutores.
  - Respuesta: CSV en `Response` con `Content-Disposition`.
  - Nota: exportar grandes volúmenes en memoria puede ser pesado; considerar streaming.

- GET /api/v1/casos/{caso_id}
  - Devuelve detalle del caso incluyendo programa de apoyo si existe, datos_chatbot, tutor, asignacion.
  - Tutor solo si está asignado.

- POST /api/v1/casos/
  - Roles: Admin
  - Body: `CasoCreate` (no requiere `id_estado`; backend asigna estado 'postulado' buscando en `CatalogoEstados` por nombre 'postulado' y tipo 'postulacion'). Si estado no existe, retorna 500 con mensaje.
  - Lógica: valida foreign keys (emprendedor, convocatoria) y maneja `IntegrityError` con mensajes legibles.
  - Registra auditoría con `registrar_auditoria_caso` antes del commit.

- PUT /api/v1/casos/{caso_id}
  - Roles: Admin, Coordinador, Tutor (Tutor sólo si está asignado al caso)
  - Body: `CasoUpdate` (campos opcionales). Se usa `model_dump(exclude_unset=True)` para aplicar solo cambios.
  - Registra auditoría con `valor_anterior` y `valor_nuevo` si hay cambios.
  - Manejo de `IntegrityError` para foreign keys inválidas.

6.8 APOYOS (`app/api/v1/endpoints/apoyo.py`)
- GET /api/v1/apoyos/
  - Filtros: `id_caso`, `id_programa`.
  - Si Tutor, se filtra a apoyos de casos asignados.

- GET /api/v1/apoyos/{apoyo_id}
  - Tutor solo si caso asignado.

- GET /api/v1/apoyos/caso/{id_caso}
  - Lista apoyos de un caso; verifica existencia del caso y autorización.

- POST /api/v1/apoyos/
  - Roles: Admin, Coordinador
  - Body: `ApoyoCreate`.
  - Lógica: valida existencia de `caso` y `programa`; crea `Apoyo`, busca `Asignacion` del caso para determinar `id_usuario` que registra auditoría. Si `id_catalogo_apoyo` es enviado, busca nombre en `CatalogoApoyo` para registrar texto legible.
  - Registra auditoría usando `registrar_auditoria_caso` y commit.

- PUT /api/v1/apoyos/{apoyo_id}` (Admin, Coordinador)
- DELETE /api/v1/apoyos/{apoyo_id}` (Admin, Coordinador)

6.9 APOYOS SOLICITADOS (`app/api/v1/endpoints/apoyo_solicitado.py`)
- GET /api/v1/apoyo_solicitado/
- GET /api/v1/apoyo_solicitado/caso/{id_caso}
- GET /api/v1/apoyo_solicitado/{id}
- POST /api/v1/apoyo_solicitado/
  - Roles: Admin, Coordinador
  - Body: `ApoyoSolicitadoCreate` (id_catalogo_apoyo, id_caso)
  - Verifica existencia de caso y catálogo.
- PUT /api/v1/apoyo_solicitado/{id}
  - Solo permite cambiar `id_catalogo_apoyo`.
- DELETE /api/v1/apoyo_solicitado/{id}`

6.10 ASIGNACIONES (`app/api/v1/endpoints/asignacion.py`)
- GET /api/v1/asignaciones/
  - Filtros: `id_caso`, `id_usuario`.
- GET /api/v1/asignaciones/{id}
- GET /api/v1/asignaciones/caso/{id_caso}
- GET /api/v1/asignaciones/usuario/{id_usuario}
- POST /api/v1/asignaciones/
  - Roles: Admin, Coordinador, Tutor
  - Body: `AsignacionCreate` (id_usuario, id_caso)
  - Validaciones:
    - `id_usuario` debe existir y su rol debe ser `Tutor`.
    - No permitir duplicados (mismo tutor en mismo caso) — ver consulta que valida existencia.
    - Registrar auditoría con `registrar_auditoria_caso`.
- PUT /api/v1/asignaciones/{id} : permite cambiar `id_usuario` (validar que sea Tutor)
- DELETE /api/v1/asignaciones/{id} : elimina asignación y registra auditoría.

6.11 NOTAS (`app/api/v1/endpoints/nota.py`)
- GET /api/v1/notas/
  - Filtros: `id_caso`, `id_usuario`. Tutor solo ve notas de casos asignados.
- GET /api/v1/notas/{id}
- POST /api/v1/notas/
  - Roles: Admin, Coordinador, Tutor (pero Tutor solo puede crear notas en casos asignados)
  - `NotaCreate` requiere `contenido`, `tipo_nota`, `id_usuario`, `id_caso`.
  - Validaciones explícitas: `tipo_nota` obligatorio y no vacío.
  - Se registra auditoría `nota_creada` con `valor_nuevo` JSON.
- PUT /api/v1/notas/{id} : Tutor solo puede actualizar sus propias notas.
- DELETE /api/v1/notas/{id} : Tutor solo puede eliminar sus propias notas; auditoría registrada.

6.12 CATALOGOS (apoyos y estados)
- `catalogo_apoyos` (`app/api/v1/endpoints/catalogo_apoyos.py`)
  - CRUD básico, Admin para crear/actualizar/eliminar; list y get disponibles para todos los roles.
  - Maneja `ProgrammingError` si la tabla no existe (mensajes de error amigables).
  - Manejo de `IntegrityError` para unique constraint y retorno 409.

- `catalogo_estados` (`app/api/v1/endpoints/catalogo_estados.py`)
  - CRUD (Admin para crear/actualizar/eliminar). Devuelve `nombre_estado` y `tipo_caso` en minúscula para consistencia.
  - `tipo_caso` debe ser `postulacion` o `proyecto` (CheckConstraint a nivel DB).

6.13 AUDITORÍA (`app/api/v1/endpoints/auditoria.py`)
- GET /api/v1/auditoria/ (Admin, Coordinador)
- GET /api/v1/auditoria/staff/{id_usuario} (Admin, Coordinador, Tutor — coordinador/tutor solo su propio historial)
  - Filtros: `id_caso`, `accion`, `skip`, `limit`
- GET /api/v1/auditoria/{id}` (Admin, Coordinador)
- Observación: Los registros de auditoría son de solo lectura vía API.

6.14 MÉTRICAS / DASHBOARD (`app/api/v1/endpoints/metricas/dashboard.py`)
- GET /api/v1/metricas/dashboard
  - Parámetros: `id_convocatoria` opcional.
  - Retorna estructura compleja con:
    - `totales` (postulaciones, proyectos, proyectos incubados, tutores, emprendedores, apoyos)
    - `proyectos_por_estado` y `postulaciones_por_estado` con `cantidad` y `porcentaje`.
    - `distribucion_apoyos` por nombre del `CatalogoApoyo`.
  - Implementación: consultas SQLAlchemy con `func.count`, `join`, `group_by`, y uso de `case` para ordenar estados por lista deseada (POSTULACION_ORDER y PROYECTO_ORDER).


7. Servicios auxiliares

7.1 Auditoría (`app/services/auditoria_service.py`)
- Funciones:
  - `_serializar_valor(valor)` : convierte estructuras a string/JSON para almacenar en la columna `valor_anterior` y `valor_nuevo`.
  - `registrar_auditoria_caso(db, accion, id_usuario, id_caso, valor_anterior, valor_nuevo)` : crea registro de `Auditoria` y lo añade a la sesión (NO hace commit).
  - `registrar_auditoria_general(db, accion, id_usuario, valor_anterior, valor_nuevo, id_caso=None)` : similar pero para auditorías no necesariamente ligadas a casos.
- Importante: estos helpers no ejecutan `db.commit()`. Se espera que el llamador ejecute commit en la transacción principal. Esto evita inconsistencias (auditoría y operación en la misma transacción).

7.2 Exportación (`app/services/export_service.py`)
- `construir_query_casos(...)` : centraliza la construcción de queries reutilizables para listados y exportaciones (considera joins según filtros y rol del `current_user`).
- `exportar_casos_csv(...)` : genera CSV en memoria (StringIO) con campos del caso y datos del emprendedor.
- `exportar_casos_con_tutores_csv(...)` : genera CSV con información de tutores y asignaciones.
- `generar_nombre_archivo(tipo_reporte)` : retorna filename con timestamp.
- Observación: Genera CSV en memoria; para conjuntos grandes, preferible stream o paginación para evitar consumo excesivo de memoria.


8. Manejo de errores y patrones de transacción

- Uso de `db.flush()` antes de commit en algunos endpoints para obtener ids generados (ej: crear usuario, crear caso). Si `db.flush()` falla por `IntegrityError`, se hace `db.rollback()` y se convierte el error a HTTP con mensaje legible.
- `IntegrityError` es capturado en varios endpoints y mapeado a 400/409 según contexto (unique constraint -> 409).
- Muchos endpoints llaman a funciones de auditoría antes del `db.commit()`.


9. Tests

Carpeta `tests/` contiene pruebas existentes: `test_auditoria.py`, `test_auth.py`, `test_casos.py`, `test_export_casos.py`, `test_flujos_completos.py`, `test_permisos.py`, `test_usuarios.py`.

Recomendación: ejecutar la suite tras configurar variables de entorno y una base de datos de test. Asegurarse de que la DB de test tenga el DDL aplicado (o usar fixtures que creen tablas en memoria).


10. Riesgos, decisiones de diseño y recomendaciones (para futuro desarrollo y mantenimiento)

10.1 Migrations
- Actualmente no se observan migraciones automáticas. Recomiendo integrar Alembic para gestionar cambios en el schema y evitar divergencias entre modelos y la base de datos en producción.

10.2 Tokens y logout
- Implementar un mecanismo de revocación/blacklist de refresh/access tokens si se requiere invalidación inmediata en logout (ej: tabla `revoked_tokens` o cache Redis con TTL).

10.3 Exportación de grandes volúmenes
- `ExportService` construye y escribe en memoria. Para grandes datos usar streaming (StreamingResponse) o exportar por lotes y almacenar temporalmente en S3 o disco.

10.4 Transaccionalidad y auditoría
- Las funciones de auditoría no hacen commit: esto está correcto. Asegúrese de llamar a `registrar_auditoria_*` dentro de la transacción y antes de `db.commit()` para que auditoría y cambio sean atómicos.

10.5 Índices y performance
- Añadir índices en columnas que se filtran frecuentemente: `Usuario.email` ya tiene index, `Caso.id_emprendedor`, `Caso.id_estado`, `Apoyo.id_caso`, etc. Revisar y añadir índices adicionales según métricas de uso.

10.6 CheckConstraints y normalización
- `catalogo_estados` tiene CheckConstraint en minúsculas. En la capa de aplicación se normaliza, pero asegurar que inserciones directas a DB respeten la convención.

10.7 Manejo de datos JSON
- `datos_chatbot` es JSON libre. Documentar el esquema esperado (key names y tipos) si el chatbot o el frontend consumen estructura específica.

10.8 Borrado lógico vs físico
- `Usuario` usa `activo` (soft delete). Otras tablas no usan soft delete. Consistencia: decidir estrategia (soft delete) para entidades críticas si se requiere mantener historial.

10.9 Nombres de rol y comparación
- `require_role` compara texto exacto. Para evitar errores, crear constantes o enumeración centralizada de roles y utilizarla en creaciones y comprobaciones.

10.10 Manejo de errores DB
- Varios endpoints capturan `IntegrityError` y comparan contenido de `e.orig` buscando la palabra "foreign key" o "unique". Esto funciona pero depende del mensaje del driver DB. Mejor usar inspección más robusta (SQLAlchemy `e.orig.pgcode` en Postgres) o manejar con migraciones que definan constraints con nombres predecibles.


11. Guía rápida para extender el proyecto

Añadir nuevo recurso (ejemplo: `evento`):
1. Crear modelo SQLAlchemy en `app/models/evento.py` siguiendo `TEMPLATE.py` y añadir a `app/models/__init__.py`.
2. Crear schemas Pydantic en `app/schemas/evento.py` (Create/Update/Response).
3. Crear endpoints en `app/api/v1/endpoints/evento.py` con router y dependencias `get_db`, `require_role` si necesario.
4. Añadir pruebas en `tests/test_evento.py`.
5. Si el modelo modifica DB, crear migración Alembic (recomendado) o actualizar `ithaka_backoffice.sql`.


12. Documentos y recursos auxiliares en el repo

- `ithaka_backoffice.sql` - DDL completo de la base de datos (examinar para conocer constraints, tipos y orden real de creación)
- `README.md` - Información general del proyecto
- `app/core/config.py` - Variables de configuración y `DATABASE_URL` builder
- `app/core/security.py` - Lógica JWT y validaciones (leer con atención para entender el flujo de autenticación)
- `app/services/auditoria_service.py` - Helpers para auditoría
- `app/services/export_service.py` - Lógica de exportación CSV y query builder reutilizable


13. Conclusión

Este documento reúne la descripción funcional y técnica necesaria para que un tercero entienda cómo interactuar con la API, cómo funcionan las reglas de negocio principales, la organización de la base de datos y las decisiones clave tomadas en el diseño.

