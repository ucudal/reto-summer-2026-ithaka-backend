# Permisos de Acceso por Rol - Backend Ithaka

## Resumen de Roles

El sistema Ithaka maneja 3 roles principales de usuario:

- **Admin**: Acceso total al sistema, gestión de usuarios, configuración general
- **Coordinador**: Gestión completa de casos, asignaciones, estados y reportes (fusiona permisos de operador y coordinador del documento)
- **Tutor**: Acceso limitado a casos asignados, puede agregar notas y ver información

---

## 📋 Matriz de Permisos por Endpoint

### 🔐 Autenticación
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `POST /api/v1/auth/login` | ✅ | ✅ | ✅ | Login de usuario |
| `POST /api/v1/auth/logout` | ✅ | ✅ | ✅ | Logout de usuario |
| `POST /api/v1/auth/refresh` | ✅ | ✅ | ✅ | Renovar token JWT |
| `GET /api/v1/auth/me` | ✅ | ✅ | ✅ | Ver perfil propio |

---

### 👥 Usuarios
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/usuarios` | ✅ | ✅ | ❌ | Listar todos los usuarios |
| `GET /api/v1/usuarios/{id}` | ✅ | ✅ | 🟡¹ | Ver usuario (¹solo su propio perfil para Tutor) |
| `POST /api/v1/usuarios` | ✅ | ❌ | ❌ | Crear nuevo usuario |
| `PUT /api/v1/usuarios/{id}` | ✅ | 🟡¹ | 🟡¹ | Actualizar usuario (¹solo su propio perfil) |
| `DELETE /api/v1/usuarios/{id}` | ✅ | ❌ | ❌ | Eliminar usuario |

---

### 🎭 Roles
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/roles` | ✅ | ❌ | ❌ | Listar roles del sistema |
| `GET /api/v1/roles/{id}` | ✅ | ❌ | ❌ | Ver rol específico |
| `POST /api/v1/roles` | ✅ | ❌ | ❌ | Crear nuevo rol |
| `PUT /api/v1/roles/{id}` | ✅ | ❌ | ❌ | Actualizar rol |
| `DELETE /api/v1/roles/{id}` | ✅ | ❌ | ❌ | Eliminar rol |

---

### 👤 Emprendedores
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/emprendedores` | ✅ | ✅ | ✅² | Listar emprendedores (²solo de casos asignados) |
| `GET /api/v1/emprendedores/{id}` | ✅ | ✅ | ✅² | Ver emprendedor (²si tiene caso asignado) |
| `POST /api/v1/emprendedores` | ✅ | ✅ | ❌ | Crear emprendedor |
| `PUT /api/v1/emprendedores/{id}` | ✅ | ✅ | ❌ | Actualizar emprendedor |
| `DELETE /api/v1/emprendedores/{id}` | ✅ | ❌ | ❌ | Eliminar emprendedor |

---

### 📁 Casos (Core del Sistema)
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/casos` | ✅ | ✅ | ✅² | Listar casos (²solo asignados) |
| `GET /api/v1/casos/{id}` | ✅ | ✅ | ✅² | Ver caso específico (²si está asignado) |
| `POST /api/v1/casos` | ✅ | ❌ | ❌ | Crear nuevo caso |
| `PUT /api/v1/casos/{id}` | ✅ | ✅ | ✅² | Actualizar caso (²solo casos asignados) |
| `DELETE /api/v1/casos/{id}` | ✅ | ❌ | ❌ | Eliminar caso |
| `GET /api/v1/casos/{id}/historial` | ✅ | ✅ | ✅² | Ver historial completo (²si está asignado) |

---

### 📊 Catálogo de Estados
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/estados` | ✅ | ✅ | ✅ | Listar estados disponibles |
| `GET /api/v1/estados/{id}` | ✅ | ✅ | ✅ | Ver estado específico |
| `POST /api/v1/estados` | ✅ | ❌ | ❌ | Crear nuevo estado |
| `PUT /api/v1/estados/{id}` | ✅ | ❌ | ❌ | Actualizar estado |
| `DELETE /api/v1/estados/{id}` | ✅ | ❌ | ❌ | Eliminar estado |

---

### 📝 Notas
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/notas` | ✅ | ✅ | ✅² | Listar notas (²solo de casos asignados) |
| `GET /api/v1/notas/{id}` | ✅ | ✅ | ✅² | Ver nota (²si es de caso asignado) |
| `GET /api/v1/notas/caso/{id_caso}` | ✅ | ✅ | ✅² | Ver notas de un caso (²si está asignado) |
| `POST /api/v1/notas` | ✅ | ✅ | ✅² | Crear nota (²solo en casos asignados) |
| `PUT /api/v1/notas/{id}` | ✅ | ✅ | 🟡³ | Actualizar nota (³solo sus propias notas) |
| `DELETE /api/v1/notas/{id}` | ✅ | ✅ | 🟡³ | Eliminar nota (³solo sus propias notas) |

---

### 📋 Auditoría
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/auditoria` | ✅ | ✅ | ❌ | Listar todos los registros |
| `GET /api/v1/auditoria/{id}` | ✅ | ✅ | ❌ | Ver registro específico |
| `GET /api/v1/auditoria/staff/{id_usuario}` | ✅ | 🟡⁴ | 🟡⁴ | Ver acciones de usuario (⁴solo sus propias acciones) |

---

### 📢 Convocatorias
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/convocatorias` | ✅ | ✅ | ✅ | Listar convocatorias |
| `GET /api/v1/convocatorias/{id}` | ✅ | ✅ | ✅ | Ver convocatoria |
| `POST /api/v1/convocatorias` | ✅ | ✅ | ❌ | Crear convocatoria |
| `PUT /api/v1/convocatorias/{id}` | ✅ | ✅ | ❌ | Actualizar convocatoria |
| `DELETE /api/v1/convocatorias/{id}` | ✅ | ❌ | ❌ | Eliminar convocatoria |

---

### 🎓 Programas
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/programas` | ✅ | ✅ | ✅ | Listar programas |
| `GET /api/v1/programas/{id}` | ✅ | ✅ | ✅ | Ver programa |
| `POST /api/v1/programas` | ✅ | ✅ | ❌ | Crear programa |
| `PUT /api/v1/programas/{id}` | ✅ | ✅ | ❌ | Actualizar programa |
| `DELETE /api/v1/programas/{id}` | ✅ | ❌ | ❌ | Eliminar programa |

---

### 🤝 Asignaciones
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/asignaciones` | ✅ | ✅ | ✅ | Listar asignaciones |
| `GET /api/v1/asignaciones/{id}` | ✅ | ✅ | ✅ | Ver asignación |
| `GET /api/v1/asignaciones/caso/{id_caso}` | ✅ | ✅ | ✅ | Ver asignaciones de un caso |
| `GET /api/v1/asignaciones/usuario/{id_usuario}` | ✅ | ✅ | ✅ | Ver asignaciones de usuario |
| `POST /api/v1/asignaciones` | ✅ | ✅ | ✅ | Crear asignación |
| `DELETE /api/v1/asignaciones/{id}` | ✅ | ✅ | ✅ | Eliminar asignación |

---

### 🎯 Apoyos
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/apoyos` | ✅ | ✅ | ✅⁷ | Listar apoyos (⁷solo de casos asignados) |
| `GET /api/v1/apoyos/{id}` | ✅ | ✅ | ✅⁷ | Ver apoyo (⁷si es de caso asignado) |
| `GET /api/v1/apoyos/caso/{id_caso}` | ✅ | ✅ | ✅⁷ | Ver apoyos de un caso (⁷si está asignado) |
| `POST /api/v1/apoyos` | ✅ | ✅ | ❌ | Crear apoyo |
| `PUT /api/v1/apoyos/{id}` | ✅ | ✅ | ❌ | Actualizar apoyo |
| `DELETE /api/v1/apoyos/{id}` | ✅ | ✅ | ❌ | Eliminar apoyo |

---

### 📌 Apoyos Solicitados
| Endpoint | Admin | Coordinador | Tutor | Descripción |
|----------|:-----:|:-----------:|:-----:|-------------|
| `GET /api/v1/apoyos-solicitados` | ✅ | ✅ | ✅⁷ | Listar apoyos solicitados (⁷solo de casos asignados) |
| `GET /api/v1/apoyos-solicitados/{id}` | ✅ | ✅ | ✅⁷ | Ver apoyo solicitado (⁷si es de caso asignado) |
| `GET /api/v1/apoyos-solicitados/caso/{id_caso}` | ✅ | ✅ | ✅⁷ | Ver apoyos solicitados de un caso (⁷si está asignado) |
| `POST /api/v1/apoyos-solicitados` | ✅ | ✅ | ❌ | Crear apoyo solicitado |
| `PUT /api/v1/apoyos-solicitados/{id}` | ✅ | ✅ | ✅⁷ | Actualizar apoyo solicitado (⁷solo de casos asignados) |
| `DELETE /api/v1/apoyos-solicitados/{id}` | ✅ | ✅ | ❌ | Eliminar apoyo solicitado |

---

## 📝 Leyenda

- ✅ **Acceso completo** al endpoint
- ❌ **Sin acceso** - Retorna 403 Forbidden
- 🟡 **Acceso condicional** - Solo bajo ciertas condiciones (ver notas al pie)

### Notas Especiales

¹ **Perfil propio**: Los usuarios Tutor pueden ver/editar **solo su propio perfil**. El Coordinador puede ver todos los usuarios.

² **Casos asignados**: Los Tutores solo ven información de casos que les fueron **asignados explícitamente**

³ **Notas propias**: Los Tutores solo pueden editar y eliminar **sus propias notas**, no las de otros usuarios

⁴ **Auditoría propia**: Coordinadores y Tutores solo ven su **propio historial de acciones**

⁷ **Contexto de caso**: Los Tutores solo ven apoyos vinculados a **casos que tienen asignados**

---

## 🔒 Implementación de Seguridad

### Decorador `@require_role()`

Los endpoints están protegidos usando el decorador personalizado:

```python
from app.core.security import require_role

@router.get("/usuarios")
def listar_usuarios(
    current_user: Usuario = Depends(require_role(["admin"]))
):
    # Solo admin puede ejecutar esto
    ...

@router.get("/casos")
def listar_casos(
    current_user: Usuario = Depends(require_role(["admin", "coordinador"]))
):
    # Admin y Coordinador pueden ejecutar esto
    ...
```

### Validación de Acceso a Recursos

Para endpoints con acceso condicional (🟡), se valida en el código:

```python
@router.get("/casos/{caso_id}")
def obtener_caso(
    caso_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    
    # Si es tutor, verificar que está asignado al caso
    if current_user.rol.nombre_rol == "tutor":
        asignacion = db.query(Asignacion).filter(
            Asignacion.id_caso == caso_id,
            Asignacion.id_usuario == current_user.id_usuario
        ).first()
        
        if not asignacion:
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a este caso"
            )
    
    return caso
```

---

## 🚀 Casos de Uso por Rol

### Admin
- Gestión completa del sistema
- Creación y eliminación de usuarios
- Configuración de roles, estados, programas
- Acceso total a auditoría y reportes

### Coordinador
- Gestión operativa de casos
- Asignación de casos a tutores
- Creación de convocatorias y programas
- Gestión de apoyos y estados de casos
- Acceso a reportes y auditoría general

### Tutor
- Visualización de casos asignados
- Agregar notas y seguimiento
- Consultar información de emprendedores
- Ver apoyos de sus casos
- Acceso limitado a su propia auditoría

---

## 🔄 Flujo de Autorización

```
1. Usuario hace login → Recibe JWT con rol
2. Usuario accede a endpoint → Middleware valida JWT
3. Decorador @require_role() verifica si el rol está permitido
4. Si acceso condicional (🟡) → Valida permisos específicos en DB
5. Si autorizado → Ejecuta endpoint
6. Si no autorizado → Retorna 403 Forbidden
```

---

## ⚠️ Importante

- **TODOS** los endpoints (excepto `/auth/login`) requieren autenticación JWT
- Los permisos se validan tanto a nivel de **rol** como de **recurso**
- La **auditoría** registra todas las acciones de modificación de datos
- Los **Tutores** operan bajo un modelo de "acceso por asignación"

---

## 📊 Resumen Estadístico

| Recurso | Endpoints Totales | Admin | Coordinador | Tutor |
|---------|:-----------------:|:-----:|:-----------:|:-----:|
| Autenticación | 4 | 4 | 4 | 4 |
| Usuarios | 5 | 5 | 5 | 1* |
| Roles | 5 | 5 | 0 | 0 |
| Emprendedores | 5 | 5 | 4 | 3* |
| Casos | 6 | 6 | 6 | 6* |
| Estados | 5 | 5 | 2 | 2 |
| Notas | 6 | 6 | 6 | 6* |
| Auditoría | 3 | 3 | 3 | 1* |
| Convocatorias | 5 | 5 | 4 | 2 |
| Programas | 5 | 5 | 4 | 2 |
| Asignaciones | 6 | 6 | 6 | 6 |
| Apoyos | 6 | 6 | 6 | 4* |
| Apoyos Solicitados | 6 | 6 | 6 | 5* |
| **TOTAL** | **67** | **67** | **67** | **50*** |

*\* Acceso condicional basado en asignaciones y permisos específicos*

---

**Última actualización**: 2026-02-21  
**Versión**: 1.0  
**Proyecto**: Ithaka Backoffice API