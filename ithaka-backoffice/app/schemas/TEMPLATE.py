"""
TEMPLATE PARA CREAR SCHEMAS
============================

Este es un template que pueden copiar para crear nuevos archivos de schemas.

¿QUÉ ES UN SCHEMA?
------------------
Un schema de Pydantic define:
- Cómo validar los datos que recibe la API (request)
- Cómo formatear los datos que devuelve la API (response)
- La documentación automática en Swagger

PASOS PARA USAR ESTE TEMPLATE:
-------------------------------
1. Copiar este archivo como: nombre_tabla.py (ej: rol.py, programa.py)
2. Reemplazar TODAS las apariciones de RECURSO con tu tabla (ej: Rol, Programa)
3. Definir los campos según tu modelo de base de datos
4. Importar en app/schemas/__init__.py
5. Usar en tus endpoints

EJEMPLO REAL:
-------------
Ver: app/schemas/emprendedor.py (bien completo y documentado)
Ver: app/schemas/caso.py
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from typing import Optional


# ============================================================
# SCHEMA BASE
# ============================================================

class RECURSOBase(BaseModel):
    """
    Campos comunes a todas las operaciones de RECURSO
    
    Aquí van los campos que se usan tanto para crear como para actualizar.
    NO incluyas el ID ni campos autogenerados (created_at, etc.)
    """
    
    # EJEMPLO 1: Campo obligatorio de texto
    nombre: str = Field(
        ...,  # ... = campo requerido (obligatorio)
        min_length=1,
        max_length=100,
        description="Nombre del recurso",
        examples=["Ejemplo de nombre"]
    )
    
    # EJEMPLO 2: Campo opcional de texto
    descripcion: Optional[str] = Field(
        None,  # None = campo opcional
        max_length=500,
        description="Descripción del recurso",
        examples=["Una descripción de ejemplo"]
    )
    
    # EJEMPLO 3: Campo numérico entero
    cantidad: int = Field(
        ...,
        ge=0,  # ge = greater or equal (mayor o igual a 0)
        le=1000,  # le = less or equal (menor o igual a 1000)
        description="Cantidad disponible",
        examples=[10]
    )
    
    # EJEMPLO 4: Campo numérico decimal
    precio: Optional[float] = Field(
        None,
        ge=0.0,
        description="Precio en USD",
        examples=[99.99]
    )
    
    # EJEMPLO 5: Email (validación automática)
    # email: EmailStr = Field(
    #     ...,
    #     max_length=150,
    #     description="Email de contacto",
    #     examples=["ejemplo@dominio.com"]
    # )
    
    # EJEMPLO 6: Fecha
    # fecha_inicio: date = Field(
    #     ...,
    #     description="Fecha de inicio",
    #     examples=["2026-02-15"]
    # )
    
    # EJEMPLO 7: Boolean
    # activo: bool = Field(
    #     True,  # valor por defecto
    #     description="Indica si está activo",
    #     examples=[True]
    # )
    
    # EJEMPLO 8: Foreign Key (relación con otra tabla)
    # id_categoria: int = Field(
    #     ...,
    #     description="ID de la categoría asociada",
    #     examples=[1]
    # )


# ============================================================
# SCHEMA PARA CREAR (POST)
# ============================================================

class RECURSOCreate(RECURSOBase):
    """
    Schema para crear un nuevo RECURSO (POST)
    
    Hereda todos los campos de RECURSOBase.
    Aquí puedes agregar campos que SOLO se usan al crear.
    
    Uso en endpoint:
        @router.post("/", status_code=201)
        def crear_recurso(recurso: RECURSOCreate, db: Session = Depends(get_db)):
            nuevo = RECURSO(**recurso.model_dump())
            db.add(nuevo)
            db.commit()
            db.refresh(nuevo)
            return nuevo
    """
    pass  # Si no hay campos adicionales, dejar pass


# ============================================================
# SCHEMA PARA ACTUALIZAR (PUT)
# ============================================================

class RECURSOUpdate(BaseModel):
    """
    Schema para actualizar un RECURSO existente (PUT)
    
    IMPORTANTE: Todos los campos son opcionales (Optional)
    porque el usuario puede querer actualizar solo algunos campos.
    
    Uso en endpoint:
        @router.put("/{id}")
        def actualizar_recurso(
            id: int, 
            recurso: RECURSOUpdate, 
            db: Session = Depends(get_db)
        ):
            obj = db.query(RECURSO).filter(RECURSO.id_recurso == id).first()
            if not obj:
                raise HTTPException(status_code=404, detail="No encontrado")
            
            # exclude_unset=True solo actualiza los campos que vinieron
            update_data = recurso.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(obj, field, value)
            
            db.commit()
            db.refresh(obj)
            return obj
    """
    # Todos los campos de RECURSOBase pero opcionales
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    cantidad: Optional[int] = Field(None, ge=0, le=1000)
    precio: Optional[float] = Field(None, ge=0.0)


# ============================================================
# SCHEMA PARA RESPUESTA (GET)
# ============================================================

class RECURSOResponse(RECURSOBase):
    """
    Schema para devolver datos de un RECURSO (GET)
    
    Incluye campos que NO se envían al crear pero SÍ se devuelven al leer:
    - ID (clave primaria)
    - Timestamps (created_at, updated_at)
    - Campos calculados
    
    Uso en endpoint:
        @router.get("/{id}", response_model=RECURSOResponse)
        def obtener_recurso(id: int, db: Session = Depends(get_db)):
            recurso = db.query(RECURSO).filter(RECURSO.id_recurso == id).first()
            if not recurso:
                raise HTTPException(status_code=404, detail="No encontrado")
            return recurso
    """
    # ID de la tabla (siempre va en Response)
    id_recurso: int = Field(
        ...,
        description="ID único del recurso",
        examples=[1]
    )
    
    # Timestamps (si tu tabla los tiene)
    created_at: datetime = Field(
        ...,
        description="Fecha de creación"
    )
    
    # updated_at: Optional[datetime] = Field(
    #     None,
    #     description="Fecha de última actualización"
    # )
    
    class Config:
        """
        Configuración de Pydantic
        
        from_attributes = True permite convertir objetos SQLAlchemy
        en objetos Pydantic automáticamente.
        
        IMPORTANTE: SIEMPRE poner esto en los Response schemas
        """
        from_attributes = True


# ============================================================
# NOTAS IMPORTANTES
# ============================================================

"""
TIPOS DE DATOS MÁS COMUNES:
---------------------------
- str: Texto
- int: Número entero
- float: Número decimal
- bool: True/False
- date: Fecha (año-mes-día)
- datetime: Fecha y hora
- EmailStr: Email (valida formato automáticamente)
- Optional[Tipo]: Hace que el campo sea opcional

VALIDACIONES CON Field():
-------------------------
- ... : Campo obligatorio
- None: Campo opcional
- min_length=X: Mínimo de caracteres
- max_length=X: Máximo de caracteres
- ge=X: Greater or Equal (mayor o igual)
- le=X: Less or Equal (menor o igual)
- gt=X: Greater Than (mayor que)
- lt=X: Less Than (menor que)
- description="...": Descripción en Swagger
- examples=[...]: Ejemplos en Swagger

FOREIGN KEYS:
-------------
Si tu tabla tiene foreign keys (relaciones), solo necesitas el ID:

    id_categoria: int = Field(
        ...,
        description="ID de la categoría",
        examples=[1]
    )

No necesitas incluir el objeto completo, solo el ID.

PASOS FINALES:
--------------
1. Una vez creado tu schema (ej: rol.py):
   
2. Importarlo en app/schemas/__init__.py:
   
   from app.schemas.rol import (
       RolBase,
       RolCreate,
       RolUpdate,
       RolResponse
   )

3. Usarlo en tu endpoint (app/api/v1/endpoints/rol.py):
   
   from app.schemas.rol import RolCreate, RolUpdate, RolResponse
   
   @router.post("/", response_model=RolResponse)
   def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
       ...

ARCHIVOS DE EJEMPLO COMPLETOS:
-------------------------------
- app/schemas/emprendedor.py ← MUY completo y bien documentado
- app/schemas/caso.py
- app/schemas/catalogo_estados.py
"""
