# 🔐 GUÍA DE AUTENTICACIÓN JWT

## ✅ IMPLEMENTACIÓN COMPLETADA

### 📁 Archivos creados/actualizados:

#### 1. **Core de seguridad** ✅
- `app/core/security.py` - Funciones JWT (hash, verify, create_token, get_current_user, require_role)

#### 2. **Modelos** ✅
- `app/models/rol.py` - Modelo de roles
- `app/models/usuario.py` - Modelo de usuarios con password_hash

#### 3. **Schemas** ✅
- `app/schemas/auth.py` - LoginRequest, LoginResponse, UsuarioActual

#### 4. **Endpoints** ✅
- `app/api/v1/endpoints/auth.py` - Login, /me, logout
- `app/api/v1/endpoints/caso.py` - PROTEGIDO con JWT
- `app/api/v1/endpoints/emprendedores.py` - PROTEGIDO con JWT
- `app/api/v1/endpoints/catalogo_estados.py` - POST/PUT/DELETE con admin

#### 5. **Router** ✅
- `app/api/v1/api.py` - Auth incluido en el router principal

#### 6. **Scripts** ✅
- `scripts/create_admin.py` - Crear usuario admin inicial

---

## 🚀 CÓMO PROBAR

### Paso 1: Levantar el servidor

```bash
cd ithaka-backoffice
docker-compose up --build
```

### Paso 2: Crear usuario admin

**Opción A - Desde fuera del contenedor:**
```bash
docker exec -it ithaka-backoffice python -m scripts.create_admin
```

**Opción B - Desde dentro del contenedor:**
```bash
docker exec -it ithaka-backoffice bash
python -m scripts.create_admin
exit
```

**Salida esperada:**
```
✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE
📧 Email:    admin@ithaka.com
🔑 Password: admin123
```

### Paso 3: Ir a Swagger
```
http://localhost:8000/docs
```

### Paso 4: Hacer login

1. Busca el endpoint: **POST /api/v1/auth/login**
2. Click en "Try it out"
3. Pega este JSON:
```json
{
  "email": "admin@ithaka.com",
  "password": "admin123"
}
```
4. Click "Execute"

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@ithaka.com",
    "rol": "admin"
  }
}
```

### Paso 5: Configurar el token en Swagger

1. **COPIA** el `access_token` de la respuesta (sin las comillas)
2. Click en el botón **"Authorize"** (arriba a la derecha, ícono de candado)
3. En el campo "Value" escribe: `Bearer <tu_token>`
   - Ejemplo: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
4. Click "Authorize"
5. Click "Close"

**🎉 ¡Listo! Ahora puedes usar todos los endpoints protegidos**

---

## 🧪 ENDPOINTS PARA PROBAR

### ✅ Endpoints que FUNCIONAN CON TOKEN:

#### GET /api/v1/auth/me
```
Devuelve información del usuario logueado
```

#### GET /api/v1/casos
```
Lista todos los casos (requiere JWT)
```

#### POST /api/v1/casos
```json
{
  "id_emprendedor": 1,
  "id_estado": 1,
  "tipo_caso": "Postulacion",
  "descripcion": "Nueva postulación de prueba"
}
```

#### GET /api/v1/emprendedores/1
```
Obtener emprendedor (requiere JWT)
```

#### POST /api/v1/estados (SOLO ADMIN)
```json
{
  "nombre_estado": "En Revisión",
  "tipo_caso": "Postulacion",
  "descripcion": "Postulación en proceso de revisión"
}
```

### ❌ Endpoints que FALLAN SIN TOKEN:

Si intentas usar cualquier endpoint protegido SIN el token:
```json
{
  "detail": "No autorizado. Token no proporcionado o inválido."
}
```

Si intentas un endpoint de admin sin ser admin:
```json
{
  "detail": "No tienes permisos suficientes. Se requiere rol: admin"
}
```

---

## 📋 PROTECCIÓN POR ENDPOINT

### 🔓 PÚBLICOS (Sin JWT):
- `POST /api/v1/auth/login`
- `GET /api/v1/estados` (catálogo público)
- `GET /api/v1/estados/{id}`

### 🔒 PROTEGIDOS (Requieren JWT):
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`
- `GET /api/v1/casos`
- `GET /api/v1/casos/{id}`
- `POST /api/v1/casos`
- `PUT /api/v1/casos/{id}`
- `PUT /api/v1/casos/{id}/cambiar_estado`
- `GET /api/v1/emprendedores/{id}`
- `PUT /api/v1/emprendedores/{id}`
- `GET /api/v1/emprendedores/{id}/casos`

### 🔐 SOLO ADMIN (Requieren JWT + rol admin):
- `DELETE /api/v1/casos/{id}`
- `DELETE /api/v1/emprendedores/{id}`
- `POST /api/v1/estados`
- `PUT /api/v1/estados/{id}`
- `DELETE /api/v1/estados/{id}`

---

## 🔧 TROUBLESHOOTING

### Problema: "Import fastapi could not be resolved"
**Solución:** Es solo un warning del linter. El código funciona en Docker.

### Problema: "Usuario admin ya existe"
**Solución:** El admin ya fue creado. Usa las credenciales anteriores.

### Problema: "Email o password incorrectos"
**Solución:** Verifica que usas `admin@ithaka.com` y `admin123`

### Problema: "Token inválido o expirado"
**Solución:** 
1. Haz login nuevamente en `/auth/login`
2. Copia el NUEVO token
3. Click "Authorize" y pega el nuevo token

### Problema: "No tienes permisos suficientes"
**Solución:** Ese endpoint requiere rol admin. Verifica con `/auth/me` que tu rol sea "admin".

---

## 🎯 SIGUIENTE PASO: Frontend

### Para usar desde JavaScript/React:

```javascript
// 1. LOGIN
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin@ithaka.com',
    password: 'admin123'
  })
});

const data = await response.json();
const token = data.access_token;

// Guardar token
localStorage.setItem('access_token', token);

// 2. USAR ENDPOINTS PROTEGIDOS
const casosResponse = await fetch('http://localhost:8000/api/v1/casos', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const casos = await casosResponse.json();
```

---

## 📝 NOTAS IMPORTANTES

1. **Token expira en 30 minutos** - Configurable en `.env` (ACCESS_TOKEN_EXPIRE_MINUTES)
2. **Password hasheado con bcrypt** - Nunca se guarda en texto plano
3. **SECRET_KEY debe ser secreta** - Cambia `clave-secreta-para-jwt` en producción
4. **Logout es del lado del cliente** - El token no se invalida en el servidor (agregar blacklist si lo necesitas)
5. **GET /emprendedores es PÚBLICO** - Por si quieres mostrar directorio público
6. **POST /emprendedores es PÚBLICO** - Por si permites auto-registro

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] Docker corriendo (`docker-compose up`)
- [ ] Admin creado (`python -m scripts.create_admin`)
- [ ] Login funciona (POST /auth/login devuelve token)
- [ ] /me funciona (GET /auth/me con token devuelve usuario)
- [ ] Endpoint protegido funciona (GET /casos con token devuelve 200)
- [ ] Endpoint sin token falla (GET /casos sin token devuelve 401)
- [ ] Endpoint admin funciona (DELETE /casos con admin devuelve 204)
- [ ] Endpoint admin falla sin rol (DELETE con usuario normal devuelve 403)

**Si todo esto funciona: ¡JWT está completamente implementado! 🎉**
