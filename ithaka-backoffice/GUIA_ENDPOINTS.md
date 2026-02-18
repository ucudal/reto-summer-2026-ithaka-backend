# 📘 Guía para Crear Endpoints

Esta guía explica cómo cada integrante del equipo puede crear sus propios endpoints.

## 🏗️ Estructura Actual

```
app/
├── api/
│   ├── deps.py                      # Dependencies compartidas
│   └── v1/
│       ├── api.py                   # Router principal (AQUÍ se agregan los routers)
│       └── endpoints/
│           ├── emprendedores.py     # ✅ Ejemplo completo funcionando
│           └── TEMPLATE.py          # 📋 Template para copiar
```

## 📝 Pasos para Crear Nuevos Endpoints

### 1️⃣ Copiar el Template

```bash
# Duplica TEMPLATE.py con el nombre de tu recurso
cp app/api/v1/endpoints/TEMPLATE.py app/api/v1/endpoints/casos.py
```

### 2️⃣ Reemplazar Nombres

En el archivo nuevo, buscar y reemplazar:
- `RECURSO` → Tu modelo (ej: `Caso`, `Usuario`, `Convocatoria`)
- `recurso` → En minúscula (ej: `caso`, `usuario`, `convocatoria`)
- `recursos` → Plural (ej: `casos`, `usuarios`, `convocatorias`)

### 3️⃣ Importar el Modelo

```python
from app.models import Caso  # Tu modelo
```

### 4️⃣ Registrar en api.py

Abrir `app/api/v1/api.py` y agregar:

```python
# Importar tu router
from app.api.v1.endpoints import casos

# Incluirlo en el api_router
api_router.include_router(
    casos.router,
    prefix="/casos",      # URL será /api/v1/casos
    tags=["casos"]        # Tag en la documentación
)
```

### 5️⃣ Probar

Iniciar el servidor y visitar: `http://localhost:8000/docs`

Verás tus endpoints en la documentación interactiva.

## 📚 Recursos Sugeridos por Persona

Divídanse los endpoints entre el equipo:

| Recurso | Archivo | Endpoints Principales |
|---------|---------|----------------------|
| Emprendedores | `emprendedores.py` | ✅ YA EXISTE |
| Casos | `casos.py` | CRUD + filtros por estado |
| Usuarios | `usuarios.py` | CRUD + cambiar rol |
| Convocatorias | `convocatorias.py` | CRUD + casos por convocatoria |
| Programas | `programas.py` | CRUD + apoyos del programa |
| Apoyos | `apoyos.py` | CRUD + asignar a casos |
| Asignaciones | `asignaciones.py` | Asignar tutores a casos |
| Notas | `notas.py` | CRUD + listar por caso |
| Estadísticas | `stats.py` | Conteos, gráficos |
| Autenticación | `auth.py` | Login, logout, cambiar password |

## 🎯 Ejemplos de Endpoints Comunes

### Listar con Filtros

```python
@router.get("/")
def listar_casos(
    estado: Optional[str] = None,
    emprendedor_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Caso)
    
    if estado:
        query = query.join(CatalogoEstados).filter(
            CatalogoEstados.nombre_estado == estado
        )
    
    if emprendedor_id:
        query = query.filter(Caso.id_emprendedor == emprendedor_id)
    
    casos = query.offset(skip).limit(limit).all()
    return casos
```

### Endpoint de Acción

```python
@router.post("/{caso_id}/asignar-tutor")
def asignar_tutor(
    caso_id: int,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    # Verificar que existen
    caso = db.query(Caso).filter(Caso.id_caso == caso_id).first()
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not caso or not usuario:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    # Crear asignación
    asignacion = Asignacion(id_caso=caso_id, id_usuario=usuario_id)
    db.add(asignacion)
    db.commit()
    
    return {"mensaje": "Tutor asignado correctamente"}
```

### Búsqueda de Texto

```python
@router.get("/buscar")
def buscar_emprendedores(
    q: str,  # Parámetro de búsqueda
    db: Session = Depends(get_db)
):
    emprendedores = db.query(Emprendedor).filter(
        or_(
            Emprendedor.nombre.ilike(f"%{q}%"),
            Emprendedor.email.ilike(f"%{q}%")
        )
    ).all()
    return emprendedores
```

## 🔧 Consejos Importantes

### ✅ DO (Hacer)

- Usar `status_code` apropiado en cada endpoint
- Manejar errores con `HTTPException`
- Implementar paginación en listas (`skip`, `limit`)
- Documentar cada endpoint con docstring
- Validar que los recursos existan antes de operar
- Usar `Depends(get_db)` para la sesión de BD

### ❌ DON'T (No Hacer)

- NO exponer `password_hash` en responses
- NO olvidar `db.commit()` después de cambios
- NO dejar endpoints sin autenticación (implementar después)
- NO hacer queries muy complejas sin optimizar
- NO olvidar cerrar la sesión (Depends lo hace automático)

## 🧪 Probar los Endpoints

### Opción 1: Swagger UI (Recomendado)
1. Iniciar servidor: `uvicorn main:app --reload`
2. Ir a: `http://localhost:8000/docs`
3. Probar directamente desde el navegador

### Opción 2: Thunder Client (VS Code)
1. Instalar extensión "Thunder Client"
2. Crear requests y probar

### Opción 3: curl
```bash
# GET
curl http://localhost:8000/api/v1/emprendedores

# POST
curl -X POST http://localhost:8000/api/v1/emprendedores \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","email":"test@example.com"}'
```

## 🆘 Problemas Comunes

### Error: "Router not found"
→ Verifica que importaste el router en `api.py`

### Error: "Table doesn't exist"
→ Asegúrate de haber cargado el dump en PostgreSQL

### Error: "Column doesn't exist"
→ Verifica que el nombre de la columna coincida con el modelo

### Error: "Circular import"
→ Importa solo lo necesario, evita `from app.models import *`

## 📞 Necesitas Ayuda?

1. Revisa `emprendedores.py` como referencia
2. Usa `TEMPLATE.py` como base
3. Consulta la documentación de FastAPI: https://fastapi.tiangolo.com
4. Pregunta en el grupo del proyecto

---

**¡Éxito creando los endpoints!** 🚀
