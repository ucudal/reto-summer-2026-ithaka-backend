"""
TEMPLATE PARA CREAR MODELS
===========================

Este es un template que pueden copiar para crear nuevos archivos de modelos.

¿QUÉ ES UN MODEL?
-----------------
Un modelo de SQLAlchemy representa una tabla en PostgreSQL.
Define:
- Nombre de la tabla
- Columnas y sus tipos
- Claves primarias y foráneas
- Relaciones con otras tablas

PASOS PARA USAR ESTE TEMPLATE:
-------------------------------
1. Copiar este archivo como: nombre_tabla.py (ej: rol.py, programa.py)
2. Reemplazar RECURSO con tu tabla (ej: Rol, Programa)
3. Definir las columnas según tu dump SQL (ithaka_backoffice.sql)
4. Definir relaciones si las hay
5. Importar en app/models/__init__.py
6. ¡Listo! SQLAlchemy creará/leerá la tabla automáticamente

EJEMPLO REAL:
-------------
Ver: app/models/emprendedor.py (bien documentado)
Ver: app/models/caso.py
Ver: app/models/catalogo_estados.py
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class RECURSO(Base):
    """
    Modelo RECURSO
    --------------
    Representa la tabla 'nombre_tabla' en PostgreSQL.
    
    Descripción: [Explicar qué almacena esta tabla]
    
    Ejemplo de uso:
        recurso = RECURSO(
            nombre="Ejemplo",
            descripcion="Una descripción",
            activo=True
        )
        db.add(recurso)
        db.commit()
    """
    
    # ============================================================
    # CONFIGURACIÓN DE LA TABLA
    # ============================================================
    
    __tablename__ = "nombre_tabla"  # ← Nombre exacto de la tabla en PostgreSQL
    
    
    # ============================================================
    # CLAVE PRIMARIA
    # ============================================================
    
    id_recurso = Column(
        Integer, 
        primary_key=True,  # Marca esta columna como clave primaria
        index=True,        # Crea un índice para búsquedas rápidas
        autoincrement=True # PostgreSQL genera el ID automáticamente
    )
    
    
    # ============================================================
    # COLUMNAS DE LA TABLA
    # ============================================================
    
    # EJEMPLO 1: Texto corto obligatorio
    nombre = Column(
        String(100),      # String(N) = VARCHAR(N) en PostgreSQL
        nullable=False,   # nullable=False = NOT NULL (obligatorio)
        index=True        # Crea índice si haces búsquedas por este campo
    )
    
    # EJEMPLO 2: Texto corto opcional
    descripcion_corta = Column(
        String(255)       # Sin nullable=False = nullable=True (opcional)
    )
    
    # EJEMPLO 3: Texto largo (sin límite de caracteres)
    descripcion = Column(
        Text              # Text = para textos largos (sin límite)
    )
    
    # EJEMPLO 4: Número entero
    cantidad = Column(
        Integer,
        nullable=False,
        default=0         # default = valor por defecto si no se especifica
    )
    
    # EJEMPLO 5: Número decimal
    precio = Column(
        Float             # Float = números decimales (REAL en PostgreSQL)
    )
    
    # EJEMPLO 6: Boolean (Verdadero/Falso)
    activo = Column(
        Boolean,
        nullable=False,
        default=True
    )
    
    # EJEMPLO 7: Fecha (año-mes-día)
    fecha_inicio = Column(
        Date              # Date = solo fecha (sin hora)
    )
    
    # EJEMPLO 8: Fecha y hora
    created_at = Column(
        DateTime,         # DateTime = fecha y hora completas
        default=datetime.utcnow,  # IMPORTANTE: sin paréntesis ()
        nullable=False
    )
    
    # EJEMPLO 9: Fecha y hora de actualización
    # updated_at = Column(
    #     DateTime,
    #     default=datetime.utcnow,
    #     onupdate=datetime.utcnow  # Se actualiza automáticamente
    # )
    
    
    # ============================================================
    # FOREIGN KEYS (CLAVES FORÁNEAS)
    # ============================================================
    
    # EJEMPLO 10: Foreign Key (relación con otra tabla)
    id_categoria = Column(
        Integer,
        ForeignKey('categoria.id_categoria'),  # 'tabla.columna'
        nullable=False
    )
    
    # Otra Foreign Key opcional
    # id_usuario = Column(
    #     Integer,
    #     ForeignKey('usuario.id_usuario'),
    #     nullable=True  # Puede ser NULL
    # )
    
    
    # ============================================================
    # RELATIONSHIPS (RELACIONES CON OTRAS TABLAS)
    # ============================================================
    
    # RELACIÓN: Un recurso pertenece a una categoría
    # categoria = relationship(
    #     "Categoria",          # Nombre de la clase del modelo relacionado
    #     back_populates="recursos"  # Nombre del relationship en Categoria
    # )
    
    # RELACIÓN INVERSA: Un recurso puede tener muchos detalles
    # detalles = relationship(
    #     "Detalle",
    #     back_populates="recurso",
    #     cascade="all, delete-orphan"  # Si se borra el recurso, se borran los detalles
    # )


# ============================================================
# NOTAS IMPORTANTES
# ============================================================

"""
TIPOS DE COLUMNAS MÁS COMUNES:
-------------------------------
- Integer: Números enteros
- String(N): Texto hasta N caracteres (VARCHAR)
- Text: Texto sin límite
- Float: Números decimales
- Boolean: True/False
- Date: Solo fecha (2026-02-15)
- DateTime: Fecha y hora (2026-02-15 14:30:00)

PROPIEDADES DE COLUMNAS:
-------------------------
- primary_key=True: Es la clave primaria
- nullable=False: Campo obligatorio (NOT NULL)
- nullable=True: Campo opcional (NULL) [por defecto]
- default=valor: Valor por defecto
- index=True: Crear índice para búsquedas rápidas
- unique=True: Los valores deben ser únicos

FOREIGN KEYS:
-------------
Define la relación con otra tabla:

    id_categoria = Column(
        Integer,
        ForeignKey('categoria.id_categoria')
    )

Formato: ForeignKey('nombre_tabla.nombre_columna')

RELATIONSHIPS:
--------------
Define cómo acceder a objetos relacionados:

    # En el modelo Recurso:
    categoria = relationship("Categoria", back_populates="recursos")
    
    # En el modelo Categoria:
    recursos = relationship("Recurso", back_populates="categoria")

Entonces puedes hacer:
    recurso.categoria.nombre
    categoria.recursos  # Lista de todos los recursos de esa categoría

TIPOS DE RELACIONES:
--------------------

1. UNO A MUCHOS (One-to-Many):
   Un usuario tiene muchos casos
   
   # En Usuario:
   casos = relationship("Caso", back_populates="usuario")
   
   # En Caso:
   id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
   usuario = relationship("Usuario", back_populates="casos")

2. MUCHOS A UNO (Many-to-One):
   Muchos casos pertenecen a un estado
   
   # En Caso:
   id_estado = Column(Integer, ForeignKey('catalogo_estados.id_estado'))
   estado = relationship("CatalogoEstados", back_populates="casos")
   
   # En CatalogoEstados:
   casos = relationship("Caso", back_populates="estado")

3. MUCHOS A MUCHOS (Many-to-Many):
   Requiere tabla intermedia
   
   # Tabla asociación
   asociacion = Table('tabla_intermedia', Base.metadata,
       Column('id_tabla1', Integer, ForeignKey('tabla1.id')),
       Column('id_tabla2', Integer, ForeignKey('tabla2.id'))
   )

CASCADE:
--------
Controla qué pasa cuando se elimina un registro relacionado:

- cascade="all, delete": Si se borra el padre, se borran los hijos
- cascade="all, delete-orphan": Lo mismo + borra hijos huérfanos
- cascade="save-update": Solo sincroniza al guardar (default)

CONVENCIONES DE NOMBRES:
-------------------------
- Tabla: minúsculas con guión bajo (emprendedor, catalogo_estados)
- Modelo: PascalCase (Emprendedor, CatalogoEstados)
- Columna: minúsculas con guión bajo (id_emprendedor, fecha_inicio)

EJEMPLO COMPLETO DE INDEX:
---------------------------
Si vas a buscar frecuentemente por un campo, agrégale index=True:

    email = Column(String(150), nullable=False, index=True)

Esto hace que las búsquedas sean más rápidas:
    db.query(Usuario).filter(Usuario.email == "..").first()

PASOS FINALES:
--------------
1. Una vez creado tu modelo (ej: rol.py):
   
2. Importarlo en app/models/__init__.py:
   
   from app.models.rol import Rol

3. ¡SQLAlchemy ya puede usar tu tabla!
   
   roles = db.query(Rol).all()
   nuevo_rol = Rol(nombre="Admin", descripcion="Administrador")

DÓNDE VER LAS COLUMNAS DE TU TABLA:
------------------------------------
Abre el archivo: ithaka_backoffice.sql
Busca: CREATE TABLE nombre_tabla (
Y verás todas las columnas y sus tipos.

Mapeo SQL → SQLAlchemy:
- VARCHAR(N) → String(N)
- TEXT → Text
- INTEGER → Integer
- REAL / NUMERIC → Float
- BOOLEAN → Boolean
- DATE → Date
- TIMESTAMP → DateTime

ARCHIVOS DE EJEMPLO COMPLETOS:
-------------------------------
- app/models/emprendedor.py ← Simple, bien documentado
- app/models/caso.py ← Con foreign keys
- app/models/catalogo_estados.py
- app/models/usuario.py ← Con relaciones más complejas
"""
