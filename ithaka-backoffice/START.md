# 🎉 PROYECTO CONFIGURADO - LÉEME PRIMERO

## ✅ Lo que acabo de crear para ti

### 📊 Modelos (11 archivos)
Todos los modelos SQLAlchemy con explicaciones detalladas:
- [app/models/](app/models/)

### 🌐 API Completa  
- ✅ Estructura de carpetas API v1
- ✅ [app/api/deps.py](app/api/deps.py) - Dependencies
- ✅ [app/api/v1/api.py](app/api/v1/api.py) - Router principal
- ✅ [app/api/v1/endpoints/emprendedores.py](app/api/v1/endpoints/emprendedores.py) - **Ejemplo COMPLETO**
- ✅ [app/api/v1/endpoints/TEMPLATE.py](app/api/v1/endpoints/TEMPLATE.py) - **Template para copiar**

### ⚙️ Configuración
- ✅ [app/core/config.py](app/core/config.py) - Manejo de variables de entorno
- ✅ [.env.example](.env.example) - Template de variables
- ✅ [requirements.txt](requirements.txt) - Todas las dependencias

### 📚 Documentación
- ✅ [GUIA_ENDPOINTS.md](GUIA_ENDPOINTS.md) - **Guía paso a paso**
- ✅ [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) - Vista completa
- ✅ [TODO.md](TODO.md) - Qué falta hacer
- ✅ Este archivo (START.md)

## 🚀 PASOS PARA EMPEZAR (EN ORDEN)

### 1️⃣ Crear archivo .env

```bash
# Copiar el template
copy .env.example .env

# O en Linux/Mac:
cp .env.example .env
```

Luego editar `.env` con tus datos reales de PostgreSQL:
```env
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ithaka_db
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

Si da error, crear un entorno virtual primero:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3️⃣ Cargar la base de datos

```bash
# Conectarse a PostgreSQL y crear la base de datos
psql -U postgres
CREATE DATABASE ithaka_db;
\q

# Cargar el dump
psql -U postgres -d ithaka_db -f dump.sql
```

### 4️⃣ Probar que funciona

```bash
uvicorn main:app --reload
```

Debería mostrar:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 5️⃣ Ver la documentación

Abrir navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Deberías ver el endpoint de emprendedores ya funcionando.

## 👥 DIVIDIRSE EL TRABAJO

Cada compañero puede empezar a crear sus endpoints:

### Persona 1: Casos (PRIORIDAD ALTA)
```bash
# 1. Crear schemas
app/schemas/caso.py

# 2. Crear endpoints
app/api/v1/endpoints/casos.py

# 3. Registrar en api.py
```

Ver [GUIA_ENDPOINTS.md](GUIA_ENDPOINTS.md) para detalles.

### Persona 2: Usuarios + Auth
```bash
app/schemas/usuario.py
app/api/v1/endpoints/usuarios.py
app/api/v1/endpoints/auth.py
```

### Persona 3: Convocatorias + Programas
```bash
app/schemas/convocatoria.py
app/schemas/programa.py
app/api/v1/endpoints/convocatorias.py
app/api/v1/endpoints/programas.py
```

### Persona 4: Asignaciones + Notas + Stats
```bash
app/schemas/asignacion.py
app/schemas/nota.py
app/api/v1/endpoints/asignaciones.py
app/api/v1/endpoints/notas.py
app/api/v1/endpoints/stats.py
```

## 📖 Documentos Importantes

1. **[GUIA_ENDPOINTS.md](GUIA_ENDPOINTS.md)** ← **LEER PRIMERO**
   - Cómo crear nuevos endpoints
   - Template para copiar
   - Ejemplos de código

2. **[ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md)**
   - Visualización completa del proyecto
   - Flujo de datos
   - División de responsabilidades

3. **[TODO.md](TODO.md)**
   - Qué está hecho
   - Qué falta hacer
   - Plan de acción

4. **[app/models/](app/models/)**
   - Todos los modelos con explicaciones
   - Revisar para entender la estructura de la DB

5. **[app/api/v1/endpoints/emprendedores.py](app/api/v1/endpoints/emprendedores.py)**
   - Ejemplo completo funcionando
   - COPIAR este patrón para otros endpoints

6. **[app/api/v1/endpoints/TEMPLATE.py](app/api/v1/endpoints/TEMPLATE.py)**
   - Template listo para copiar
   - Reemplazar nombres y listo

## ⚠️ Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'pydantic_settings'"
```bash
pip install pydantic-settings
```

### Error: "could not connect to server: Connection refused"
- PostgreSQL no está corriendo
- Verificar datos en .env

### Error: "relation does not exist"
- No cargaste el dump en la base de datos
- Ejecutar: `psql -U postgres -d ithaka_db -f dump.sql`

### Los endpoints no aparecen en /docs
- Verificar que importaste el router en `api.py`
- Verificar que lo agregaste con `api_router.include_router()`

## 🆘 Necesitas Ayuda?

1. Lee la documentación relevante (arriba)
2. Revisa el código de ejemplo en `emprendedores.py`
3. Usa el `TEMPLATE.py`
4. Pregunta en el grupo

## ✨ Próximos Pasos

1. ✅ Configurar .env
2. ✅ Instalar dependencias
3. ✅ Cargar base de datos
4. ✅ Probar que funciona
5. 📝 Crear schemas (ver TODO.md)
6. 🌐 Crear endpoints (copiar template)
7. 🔐 Implementar autenticación
8. 🧪 Testing

---

**¡El proyecto está listo para que todos trabajen en paralelo!**

Cada uno puede crear sus endpoints independientemente usando el template y la guía.

🚀 **¡Éxitos con el proyecto!**
