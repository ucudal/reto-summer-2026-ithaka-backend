# 📋 CHECKLIST - Archivos Pendientes de Implementar

Este documento lista todos los archivos que faltan implementar en el proyecto.

## ✅ COMPLETADOS

### Tu parte (Emprendedor, Caso, Estados):
- [x] `app/models/emprendedor.py`
- [x] `app/models/caso.py`
- [x] `app/models/catalogo_estados.py`
- [x] `app/schemas/emprendedor.py`
- [x] `app/schemas/caso.py`
- [x] `app/schemas/catalogo_estados.py`
- [x] `app/api/v1/endpoints/emprendedores.py` ✨ **CON JWT**
- [x] `app/api/v1/endpoints/caso.py` ✨ **CON JWT**
- [x] `app/api/v1/endpoints/catalogo_estados.py` ✨ **CON JWT**

### JWT y Autenticación:
- [x] `app/core/security.py` - Hash, JWT, verify, get_current_user, require_role
- [x] `app/models/rol.py` ✨ **NUEVO**
- [x] `app/models/usuario.py` ✨ **NUEVO**
- [x] `app/schemas/auth.py` - LoginRequest, LoginResponse, UsuarioActual
- [x] `app/api/v1/endpoints/auth.py` - Login, /me, logout ✨ **COMPLETO**
- [x] `scripts/create_admin.py` - Script para crear admin inicial
- [x] `GUIA_JWT.md` - Documentación completa de JWT

## ⏳ PENDIENTES (Para tus compañeros)

### 📦 Models (6 archivos)
- [ ] `app/models/convocatoria.py`
- [ ] `app/models/programa.py`
- [ ] `app/models/apoyo.py`
- [ ] `app/models/asignacion.py`
- [ ] `app/models/nota.py`
- [ ] `app/models/auditoria.py`

### 📝 Schemas (8 archivos)
- [ ] `app/schemas/rol.py` (opcional, si quieren CRUD completo)
- [ ] `app/schemas/usuario.py` (para endpoints de usuarios)
- [ ] `app/schemas/convocatoria.py`
- [ ] `app/schemas/programa.py`
- [ ] `app/schemas/apoyo.py`
- [ ] `app/schemas/asignacion.py`
- [ ] `app/schemas/nota.py`
- [ ] `app/schemas/auditoria.py`

### 🛣️ Endpoints (8 archivos)
- [ ] `app/api/v1/endpoints/rol.py` (opcional, GET público + CRUD admin)
- [ ] `app/api/v1/endpoints/usuario.py` ⚠️ **IMPORTANTE para gestión de usuarios**
- [ ] `app/api/v1/endpoints/convocatoria.py`
- [ ] `app/api/v1/endpoints/programa.py`
- [ ] `app/api/v1/endpoints/apoyo.py`
- [ ] `app/api/v1/endpoints/asignacion.py`
- [ ] `app/api/v1/endpoints/nota.py`
- [ ] `app/api/v1/endpoints/auditoria.py`

## 📚 TEMPLATES DISPONIBLES
- `app/models/TEMPLATE.py` - Template para crear modelos
- `app/schemas/TEMPLATE.py` - Template para crear schemas
- `app/api/v1/endpoints/TEMPLATE.py` - Template para crear endpoints

## 📋 PASOS PARA IMPLEMENTAR UN ARCHIVO

### 1️⃣ Implementar un Model
1. Abrir `app/models/TEMPLATE.py` como referencia
2. Abrir `ithaka_backoffice.sql` para ver las columnas de la tabla
3. Copiar el código comentado del archivo vacío (ej: `rol.py`)
4. Descomentar y completar según el template y el SQL
5. Importar en `app/models/__init__.py`

### 2️⃣ Implementar un Schema
1. Abrir `app/schemas/TEMPLATE.py` como referencia
2. Abrir `ithaka_backoffice.sql` para ver los campos
3. Copiar el código comentado del archivo vacío (ej: `rol.py`)
4. Descomentar y completar según el template
5. Importar en `app/schemas/__init__.py`

### 3️⃣ Implementar un Endpoint
1. Abrir `app/api/v1/endpoints/TEMPLATE.py` como referencia
2. Copiar el código comentado del archivo vacío (ej: `rol.py`)
3. Descomentar y completar según el template
4. Incluir el router en `app/api/v1/api.py`

## ⚠️ IMPORTANTE

### Al implementar Models:
- Revisar el SQL para tipos de datos correctos
- Agregar foreign keys si las tiene
- Comentar relationships si el modelo relacionado no existe todavía

### Al implementar Schemas:
- Los campos con `default` en SQL son opcionales
- NO exponer password_hash en Response schemas
- Usar `from_attributes = True` en Response schemas

### Al implementar Endpoints:
- Usar `**model_dump()` para crear objetos (con `**`)
- Usar `exclude_unset=True` en Updates
- Hashear passwords antes de guardarlos (Usuario)

## 🔗 ORDEN RECOMENDADO DE IMPLEMENTACIÓN

Por dependencias, implementar en este orden:

1. **Sin dependencias:**
   - rol
   - programa

2. **Dependen de rol:**
   - usuario

3. **Depende de emprendedor (ya hecho):**
   - convocatoria (opcional para caso)

4. **Dependen de caso (ya hecho) y otros:**
   - apoyo (depende de caso y programa)
   - asignacion (depende de caso y usuario)
   - nota (depende de caso y usuario)
   - auditoria (depende de caso y usuario)

## 🎯 PROGRESO GENERAL

**Total:** 33 archivos (incluyendo JWT)
- ✅ Completados: 16 (48%) 🎉
- ⏳ Pendientes: 17 (52%)

**Desglose por categoría:**
- Models: 5/11 completos (45%)
- Schemas: 4/11 completos (36%)
- Endpoints: 4/11 completos (36%)
- Core/Scripts: 3/3 completos (100%) ✅

---

**Última actualización:** 19 de febrero de 2026
**🔐 JWT COMPLETAMENTE IMPLEMENTADO Y FUNCIONAL**
