# ENDPOINTS PARA CHATBOT - API ITHAKA

**Base URL:** `http://localhost:8000`

---

## 1. Crear Emprendedor

Primero deben crear el emprendedor en el sistema.

### Endpoint
```
POST /api/v1/emprendedores/
```

### URL Completa
```
http://localhost:8000/api/v1/emprendedores/
```

### Headers
```json
{
  "Content-Type": "application/json"
}
```

### Body (JSON)
```json
{
  "nombre": "Juan Pérez",
  "email": "juan.perez@example.com",
  "telefono": "+598 99 123 456",
  "vinculo_institucional": "Estudiante UCU"
}
```

### Campos Requeridos y Opcionales

| Campo | Tipo | Requerido | Descripción | Ejemplo |
|-------|------|-----------|-------------|---------|
| `nombre` | string | ✅ Sí | Nombre completo del emprendedor | "Juan Pérez" |
| `email` | string | ✅ Sí | Email válido | "juan.perez@example.com" |
| `telefono` | string | ❌ No | Teléfono de contacto | "+598 99 123 456" |
| `vinculo_institucional` | string | ❌ No | Relación con UCU | "Estudiante UCU", "Egresado", "Externo" |

### Respuesta Exitosa (201 Created)
```json
{
  "id_emprendedor": 4,
  "nombre": "Juan Pérez",
  "email": "juan.perez@example.com",
  "telefono": "+598 99 123 456",
  "vinculo_institucional": "Estudiante UCU",
  "fecha_registro": "2026-02-20T14:30:00"
}
```

**⚠️ IMPORTANTE:** Guardar el `id_emprendedor` de la respuesta para usarlo en el siguiente paso.

---

## 2. Crear Caso (Postulación)

Una vez creado el emprendedor, pueden crear el caso asociado a ese emprendedor.

### Endpoint
```
POST /api/v1/caso/
```

### URL Completa
```
http://localhost:8000/api/v1/caso/
```

### Headers
```json
{
  "Content-Type": "application/json"
}
```

### Body (JSON)
```json
{
  "nombre_caso": "App de delivery sustentable",
  "descripcion": "Aplicación móvil para entregas ecológicas en Montevideo",
  "datos_chatbot": {
    "interes": "alto",
    "canal": "web",
    "respuesta1": "...",
    "respuesta2": "..."
  },
  "consentimiento_datos": true,
  "id_emprendedor": 4,
  "id_convocatoria": 1,
  "id_estado": 1
}
```

### Campos Requeridos y Opcionales

| Campo | Tipo | Requerido | Descripción | Ejemplo |
|-------|------|-----------|-------------|---------|
| `nombre_caso` | string | ✅ Sí | Nombre del proyecto/caso | "App de delivery sustentable" |
| `descripcion` | string | ❌ No | Descripción detallada | "Aplicación móvil para..." |
| `datos_chatbot` | object | ❌ No | Objeto JSON con respuestas del chatbot | `{"interes": "alto", ...}` |
| `consentimiento_datos` | boolean | ✅ Sí | Si dio consentimiento | `true` o `false` |
| `id_emprendedor` | integer | ✅ Sí | ID del emprendedor (paso 1) | `4` |
| `id_convocatoria` | integer | ❌ No | ID de la convocatoria | `1`, `2`, `3` o `null` |
| `id_estado` | integer | ✅ Sí | Estado inicial del caso | `1` (ver tabla abajo) |

### Estados Disponibles

| ID | Nombre | Tipo | Descripción |
|----|--------|------|-------------|
| `1` | Postulado | Postulacion | **Estado inicial recomendado** |
| `2` | En Evaluación | Postulacion | Para casos en revisión |
| `3` | Aprobado Proyecto | Proyecto | Para proyectos aprobados |

**Recomendación:** Usar siempre `"id_estado": 1` para nuevas postulaciones desde el chatbot.

### Respuesta Exitosa (201 Created)
```json
{
  "id_caso": 5,
  "fecha_creacion": "2026-02-20T14:30:00",
  "nombre_caso": "App de delivery sustentable",
  "descripcion": "Aplicación móvil para entregas ecológicas en Montevideo",
  "datos_chatbot": {
    "interes": "alto",
    "canal": "web",
    "respuesta1": "...",
    "respuesta2": "..."
  },
  "consentimiento_datos": true,
  "id_emprendedor": 4,
  "id_convocatoria": 1,
  "id_estado": 1
}
```

---

## Flujo Completo de Integración

```
┌─────────────────────────────────────────────────────────┐
│ PASO 1: Crear Emprendedor                              │
│ POST /api/v1/emprendedores/                            │
│                                                         │
│ Body: { nombre, email, telefono, vinculo }             │
│                                                         │
│ ──────────────────────────────────────────────────────→│
│                                                         │
│ Respuesta: { id_emprendedor: 4, ... }                 │
└─────────────────────────────────────────────────────────┘
                          ↓
                  Guardar id_emprendedor
                          ↓
┌─────────────────────────────────────────────────────────┐
│ PASO 2: Crear Caso                                     │
│ POST /api/v1/caso/                                     │
│                                                         │
│ Body: {                                                │
│   nombre_caso,                                         │
│   descripcion,                                         │
│   datos_chatbot: {...},                                │
│   consentimiento_datos: true,                          │
│   id_emprendedor: 4,  ← Usar el ID del paso 1         │
│   id_estado: 1        ← Siempre usar 1 (Postulado)    │
│ }                                                       │
│                                                         │
│ ──────────────────────────────────────────────────────→│
│                                                         │
│ Respuesta: { id_caso: 5, ... }                         │
└─────────────────────────────────────────────────────────┘
```

---

## Ejemplo Completo con cURL

### 1. Crear Emprendedor
```bash
curl -X POST "http://localhost:8000/api/v1/emprendedores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María González",
    "email": "maria.gonzalez@ucu.edu.uy",
    "telefono": "+598 99 876 543",
    "vinculo_institucional": "Estudiante UCU"
  }'
```

### 2. Crear Caso (usando el id_emprendedor de la respuesta anterior)
```bash
curl -X POST "http://localhost:8000/api/v1/caso/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_caso": "Plataforma educativa online",
    "descripcion": "Sistema de gestión de aprendizaje para estudiantes universitarios",
    "datos_chatbot": {
      "pregunta1": "¿Cuál es tu idea?",
      "respuesta1": "Una plataforma educativa...",
      "pregunta2": "¿Tienes equipo?",
      "respuesta2": "Sí, somos 3 personas"
    },
    "consentimiento_datos": true,
    "id_emprendedor": 4,
    "id_convocatoria": 1,
    "id_estado": 1
  }'
```

---

## Códigos de Respuesta HTTP

| Código | Descripción | Solución |
|--------|-------------|----------|
| `201 Created` | ✅ Creado exitosamente | - |
| `400 Bad Request` | ❌ Datos inválidos | Revisar formato de los datos |
| `404 Not Found` | ❌ ID no existe | Verificar que `id_emprendedor` o `id_estado` existan |
| `422 Unprocessable Entity` | ❌ Error de validación | Revisar campos requeridos o formato (ej: email) |
| `500 Internal Server Error` | ❌ Error del servidor | Contactar con el equipo de backend |

---

## Documentación Interactiva

Pueden probar los endpoints directamente desde el navegador:

- **Swagger UI (recomendado):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

En Swagger UI pueden:
- Ver todos los endpoints disponibles
- Probar las llamadas directamente desde el navegador
- Ver ejemplos de request/response
- Validar el formato de los datos

---

## Notas Importantes

1. **Email único:** El email del emprendedor debe ser único. Si intentan crear dos emprendedores con el mismo email, recibirán un error.

2. **Campo `datos_chatbot`:** Pueden guardar cualquier estructura JSON que necesiten aquí. Es completamente flexible.

3. **Consentimiento:** El campo `consentimiento_datos` es importante para cumplir con políticas de privacidad.

4. **Convocatoria:** Si no tienen una convocatoria específica, pueden:
   - Enviar `"id_convocatoria": null`
   - O usar `1`, `2` o `3` si existen esas convocatorias en la BD

---
