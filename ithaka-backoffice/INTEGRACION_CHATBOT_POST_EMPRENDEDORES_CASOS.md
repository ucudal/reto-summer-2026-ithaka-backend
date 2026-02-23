# Integración Chatbot -> POST Emprendedores y POST Casos (Ithaka Backoffice)

## Objetivo
Definir el contrato real para que el chatbot cree correctamente:
1. Emprendedores
2. Casos asociados en la base de datos

## Base URL
- `http://localhost:8000`
- Prefijo API: `/api/v1`

## Autenticación y permisos
Ambos endpoints de creación requieren JWT con rol **Admin**:
- `POST /api/v1/emprendedores/`
- `POST /api/v1/casos/`

Headers requeridos en ambos:
- `Content-Type: application/json`
- `Authorization: Bearer <access_token>`

### Obtener token
Endpoint:
- `POST /api/v1/auth/login`

Request:
```json
{
  "email": "admin@ithaka.com",
  "password": "admin123"
}
```

---

## 1) Crear Emprendedor

### Endpoint
- `POST /api/v1/emprendedores/`

### Campos del body

| Campo | Tipo | Requerido | Validación |
|---|---|---|---|
| `nombre` | string | Sí | min 1, max 150 |
| `apellido` | string | Sí | min 1, max 150 |
| `email` | string | Sí | email válido, max 150 |
| `telefono` | string | No | max 50 |
| `documento_identidad` | string | No | max 50 |
| `pais_residencia` | string | No | max 100 |
| `ciudad_residencia` | string | No | max 100 |
| `campus_ucu` | string | No | max 100 |
| `relacion_ucu` | string | No | max 100 |
| `facultad_ucu` | string | No | max 100 |
| `canal_llegada` | string | No | max 100 |
| `motivacion` | string | No | texto libre |

### Mínimo payload válido

```json
{
  "nombre": "Ana",
  "apellido": "Perez",
  "email": "ana.perez@example.com"
}
```

### Ejemplo request completo
```json
{
  "nombre": "Maria",
  "apellido": "Gonzalez",
  "email": "maria.gonzalez@ejemplo.com",
  "telefono": "+59899123456",
  "relacion_ucu": "Estudiante",
  "canal_llegada": "ChatBot",
  "motivacion": "Quiero validar mi startup."
}
```

### Respuesta esperada (201)
Devuelve el emprendedor creado con:
- `id_emprendedor`
- `fecha_registro`
- todos los campos del recurso

Importante:
- `fecha_registro` **no se envía** en el request; se genera automáticamente.

---

## 2) Crear Caso

### Endpoint
- `POST /api/v1/casos/`

Importante: la ruta correcta es **`/casos/`** (no `/caso/`).

### Campos del body

| Campo | Tipo | Requerido | Validación/Regla |
|---|---|---|---|
| `nombre_caso` | string | Sí | max 200 |
| `descripcion` | string/null | No | texto libre |
| `datos_chatbot` | object/null | No | JSON válido |
| `consentimiento_datos` | boolean | No | default `false` si no se envía |
| `id_emprendedor` | int | Sí | FK a `emprendedor.id_emprendedor` |
| `id_convocatoria` | int/null | No | FK a `convocatoria.id_convocatoria` |

### Mínimo payload válido

```json
{
  "nombre_caso": "Idea inicial",
  "id_emprendedor": 15
}
```

Notas sobre ese mínimo:
- `id_emprendedor` debe existir.

### Ejemplo request completo
```json
{
  "nombre_caso": "Plataforma de tutoría IA",
  "descripcion": "MVP para acompañar estudiantes universitarios.",
  "datos_chatbot": {
    "sector": "EdTech",
    "fase": "idea-validada",
    "equipo": 2
  },
  "consentimiento_datos": true,
  "id_emprendedor": 15,
  "id_convocatoria": 1
}
```

### Respuesta esperada (201)
Devuelve el caso creado con:
- `id_caso`
- `fecha_creacion`
- todos los campos del recurso

Además, al crear caso se registra auditoría (`accion = "Caso creado"`).

Importante:
- `fecha_creacion` **no se envía** en el request; se genera automáticamente.

---

## Flujo recomendado para el chatbot

1. Login (`POST /api/v1/auth/login`) y guardar `access_token`.
2. Crear emprendedor (`POST /api/v1/emprendedores/`).
3. Guardar `id_emprendedor` de la respuesta.
4. Opcional: obtener `id_convocatoria` en `GET /api/v1/convocatorias/`.
5. Crear caso (`POST /api/v1/casos/`) usando el `id_emprendedor` recién creado. El backend asigna `Postulado` automáticamente.

---

## Errores esperables

| HTTP | Cuándo ocurre |
|---|---|
| `401` | Token faltante/inválido/expirado |
| `403` | Token válido pero rol distinto de `Admin` |
| `422` | Error de validación del payload |
| `500` | Error de BD no manejado (por ejemplo FK inexistente) |

---

## Notas operativas

- El backend actual no define unicidad de email en tabla `emprendedor`.
- Si el equipo IA necesita deduplicar emprendedores, debe hacerlo en su lógica de integración.
- `datos_chatbot` es el campo recomendado para guardar respuestas estructuradas del asistente.
