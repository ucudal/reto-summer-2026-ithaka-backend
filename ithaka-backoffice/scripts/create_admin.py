"""
Script para crear un usuario administrador inicial

Ejecutar con:
    python -m scripts.create_admin

O desde Docker:
    docker exec -it ithaka-backoffice python -m scripts.create_admin
"""

import sys
import os

# Agregar el directorio padre al path para que pueda importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.core.security import hash_password
from app.core.config import settings


def create_admin():
    """Crear usuario administrador si no existe"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("🔍 Verificando si existe rol 'admin'...")
        
        # 1. Verificar/crear rol admin
        rol_admin = db.query(Rol).filter(Rol.nombre_rol == "admin").first()
        
        if not rol_admin:
            print("📝 Creando rol 'admin'...")
            rol_admin = Rol(
                nombre_rol="admin",
                descripcion="Administrador del sistema con acceso completo"
            )
            db.add(rol_admin)
            db.commit()
            db.refresh(rol_admin)
            print(f"✅ Rol 'admin' creado con ID: {rol_admin.id_rol}")
        else:
            print(f"✅ Rol 'admin' ya existe con ID: {rol_admin.id_rol}")
        
        # 2. Verificar si ya existe usuario admin
        admin_user = db.query(Usuario).filter(Usuario.email == "admin@ithaka.com").first()
        
        if admin_user:
            print(f"⚠️  Usuario admin ya existe: {admin_user.email}")
            print(f"   Nombre: {admin_user.nombre}")
            print(f"   ID: {admin_user.id_usuario}")
            print(f"   Rol: {admin_user.rol.nombre_rol if admin_user.rol else 'Sin rol'}")
            return
        
        # 3. Crear usuario admin
        print("\n📝 Creando usuario administrador...")
        
        password = "admin123"  # Password por defecto
        hashed_password = hash_password(password)
        
        admin = Usuario(
            nombre="Administrador",
            apellido="Sistema",
            email="admin@ithaka.com",
            password_hash=hashed_password,
            id_rol=rol_admin.id_rol,
            activo=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("\n" + "="*60)
        print("✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
        print("="*60)
        print(f"\n📧 Email:    admin@ithaka.com")
        print(f"🔑 Password: {password}")
        print(f"👤 ID:       {admin.id_usuario}")
        print(f"🎭 Rol:      {admin.rol.nombre_rol}")
        print("\n⚠️  IMPORTANTE: Cambia este password después del primer login")
        print("="*60 + "\n")
        
        print("\n🚀 Cómo usar:")
        print("1. Inicia el servidor: docker-compose up")
        print("2. Ve a: http://localhost:8000/docs")
        print("3. Click en 'Authorize' (arriba a la derecha)")
        print("4. Haz login en POST /api/v1/auth/login")
        print("5. Copia el access_token de la respuesta")
        print("6. Pégalo en 'Authorize' con formato: Bearer <tu_token>")
        print("7. Ahora puedes usar todos los endpoints protegidos\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
