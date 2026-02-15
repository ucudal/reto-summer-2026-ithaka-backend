"""
Schemas EMPRENDEDOR
-------------------
Define cómo se validan y serializan los datos de emprendedores.

Los schemas sirven para:
- Validar datos que recibe la API (request)
- Formatear datos que devuelve la API (response)
- Documentar automáticamente en Swagger/OpenAPI
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ============================================================
# SCHEMAS BASE
# ============================================================

class EmprendedorBase(BaseModel):
    """
    Campos comunes a todas las operaciones de emprendedor
    """
    nombre: str = Field(
        ...,  # ... = campo requerido
        min_length=1,
        max_length=150,
        description="Nombre completo del emprendedor",
        examples=["Juan Pérez"]
    )
    
    email: EmailStr = Field(
        ...,  # EmailStr valida automáticamente el formato de email
        max_length=150,
        description="Email del emprendedor",
        examples=["juan.perez@example.com"]
    )
    
    telefono: Optional[str] = Field(
        None,  # None = campo opcional
        max_length=50,
        description="Teléfono de contacto",
        examples=["+598 99 123 456"]
    )
    
    vinculo_institucional: Optional[str] = Field(
        None,
        max_length=150,
        description="Relación con la institución",
        examples=["Estudiante UCU", "Egresado", "Externo"]
    )


# ============================================================
# SCHEMAS PARA CREAR (POST)
# ============================================================

class EmprendedorCreate(EmprendedorBase):
    """
    Schema para crear un nuevo emprendedor (POST)
    
    Uso en endpoint:
        @router.post("/")
        def crear_emprendedor(emprendedor: EmprendedorCreate):
            ...
    """
    pass  # Hereda todos los campos de EmprendedorBase


# ============================================================
# SCHEMAS PARA ACTUALIZAR (PUT/PATCH)
# ============================================================

class EmprendedorUpdate(BaseModel):
    """
    Schema para actualizar un emprendedor (PUT)
    
    Todos los campos son opcionales porque puede que solo
    quieras actualizar algunos campos, no todos.
    """
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=150)
    telefono: Optional[str] = Field(None, max_length=50)
    vinculo_institucional: Optional[str] = Field(None, max_length=150)


# ============================================================
# SCHEMAS PARA RESPUESTA (GET)
# ============================================================

class EmprendedorResponse(EmprendedorBase):
    """
    Schema para devolver datos de un emprendedor (GET)
    
    Incluye campos adicionales como ID y fecha de registro
    que no se envían al crear, pero sí se devuelven al leer.
    
    Uso en endpoint:
        @router.get("/{id}", response_model=EmprendedorResponse)
        def obtener_emprendedor(id: int):
            ...
    """
    id_emprendedor: int = Field(
        ...,
        description="ID único del emprendedor",
        examples=[1]
    )
    
    fecha_registro: datetime = Field(
        ...,
        description="Fecha y hora de registro en el sistema"
    )
    
    class Config:
        """
        Configuración de Pydantic
        
        from_attributes = True permite convertir objetos SQLAlchemy
        en objetos Pydantic automáticamente
        
        Antes se llamaba orm_mode = True (en versiones viejas de Pydantic)
        """
        from_attributes = True


# ============================================================
# SCHEMAS PARA LISTAS
# ============================================================

class EmprendedorListResponse(BaseModel):
    """
    Schema para devolver una lista de emprendedores
    
    Uso en endpoint:
        @router.get("/", response_model=EmprendedorListResponse)
        def listar_emprendedores():
            ...
    """
    total: int = Field(
        ...,
        description="Cantidad total de emprendedores",
        examples=[25]
    )
    
    emprendedores: list[EmprendedorResponse] = Field(
        ...,
        description="Lista de emprendedores"
    )


# ============================================================
# EJEMPLO DE USO EN ENDPOINTS
# ============================================================
"""
from app.schemas.emprendedor import (
    EmprendedorCreate, 
    EmprendedorUpdate, 
    EmprendedorResponse,
    EmprendedorListResponse
)

# Crear emprendedor
@router.post("/", response_model=EmprendedorResponse, status_code=201)
def crear_emprendedor(
    emprendedor: EmprendedorCreate,
    db: Session = Depends(get_db)
):
    nuevo_emprendedor = Emprendedor(**emprendedor.model_dump())
    db.add(nuevo_emprendedor)
    db.commit()
    db.refresh(nuevo_emprendedor)
    return nuevo_emprendedor


# Obtener emprendedor por ID
@router.get("/{id}", response_model=EmprendedorResponse)
def obtener_emprendedor(id: int, db: Session = Depends(get_db)):
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == id
    ).first()
    
    if not emprendedor:
        raise HTTPException(status_code=404, detail="Emprendedor no encontrado")
    
    return emprendedor


# Actualizar emprendedor
@router.put("/{id}", response_model=EmprendedorResponse)
def actualizar_emprendedor(
    id: int,
    emprendedor_update: EmprendedorUpdate,
    db: Session = Depends(get_db)
):
    emprendedor = db.query(Emprendedor).filter(
        Emprendedor.id_emprendedor == id
    ).first()
    
    if not emprendedor:
        raise HTTPException(status_code=404, detail="Emprendedor no encontrado")
    
    # Actualizar solo los campos que se enviaron
    for campo, valor in emprendedor_update.model_dump(exclude_unset=True).items():
        setattr(emprendedor, campo, valor)
    
    db.commit()
    db.refresh(emprendedor)
    return emprendedor


# Listar emprendedores
@router.get("/", response_model=EmprendedorListResponse)
def listar_emprendedores(db: Session = Depends(get_db)):
    emprendedores = db.query(Emprendedor).all()
    
    return {
        "total": len(emprendedores),
        "emprendedores": emprendedores
    }
"""
