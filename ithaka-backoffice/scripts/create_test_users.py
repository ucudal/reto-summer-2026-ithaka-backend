"""
Script para crear usuarios de prueba

Ejecutar con:
    python -m scripts.create_test_users

O desde Docker:
    docker exec -it ithaka_api python -m scripts.create_test_users
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


def create_test_users():
    """Crear usuarios de prueba para testing"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("🔧 CREANDO USUARIOS DE PRUEBA")
        print("="*70 + "\n")
        
        # Obtener roles
        rol_admin = db.query(Rol).filter(Rol.nombre_rol == "Admin").first()
        rol_coordinador = db.query(Rol).filter(Rol.nombre_rol == "Coordinador").first()
        rol_tutor = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
        
        if not all([rol_admin, rol_coordinador, rol_tutor]):
            print("❌ ERROR: Faltan roles en la base de datos")
            print("   Asegúrate de haber ejecutado ithaka_inserts.sql primero")
            return
        
        # Definir usuarios a crear
        usuarios = [
            {
                "nombre": "Admin",
                "apellido": "Sistema",
                "email": "admin@ithaka.com",
                "password": "admin123",
                "id_rol": rol_admin.id_rol,
                "rol_nombre": "Admin"
            },
            {
                "nombre": "María",
                "apellido": "González",
                "email": "coordinador@ithaka.com",
                "password": "coord123",
                "id_rol": rol_coordinador.id_rol,
                "rol_nombre": "Coordinador"
            },
            {
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "tutor1@ithaka.com",
                "password": "tutor123",
                "id_rol": rol_tutor.id_rol,
                "rol_nombre": "Tutor"
            },
            {
                "nombre": "Ana",
                "apellido": "Rodríguez",
                "email": "tutor2@ithaka.com",
                "password": "tutor123",
                "id_rol": rol_tutor.id_rol,
                "rol_nombre": "Tutor"
            }
        ]
        
        usuarios_creados = []
        usuarios_existentes = []
        
        # Crear cada usuario
        for user_data in usuarios:
            # Verificar si ya existe
            existing = db.query(Usuario).filter(Usuario.email == user_data["email"]).first()
            
            if existing:
                usuarios_existentes.append({
                    "nombre": existing.nombre,
                    "email": existing.email,
                    "rol": user_data["rol_nombre"]
                })
                continue
            
            # Crear nuevo usuario
            nuevo_usuario = Usuario(
                nombre=user_data["nombre"],
                apellido=user_data["apellido"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                id_rol=user_data["id_rol"],
                activo=True
            )
            
            db.add(nuevo_usuario)
            db.flush()
            
            usuarios_creados.append({
                "id": nuevo_usuario.id_usuario,
                "nombre": user_data["nombre"],
                "apellido": user_data["apellido"],
                "email": user_data["email"],
                "password": user_data["password"],
                "rol": user_data["rol_nombre"]
            })
        
        db.commit()
        
        # Mostrar resultados
        print("✅ USUARIOS CREADOS EXITOSAMENTE\n")
        print("-" * 70)
        
        if usuarios_creados:
            for user in usuarios_creados:
                print(f"\n👤 {user['rol']}: {user['nombre']} {user['apellido']}")
                print(f"   📧 Email:    {user['email']}")
                print(f"   🔑 Password: {user['password']}")
                print(f"   🆔 ID:       {user['id']}")
        
        if usuarios_existentes:
            print("\n\n⚠️  USUARIOS QUE YA EXISTÍAN\n")
            print("-" * 70)
            for user in usuarios_existentes:
                print(f"\n👤 {user['rol']}: {user['nombre']}")
                print(f"   📧 Email: {user['email']}")
        
        print("\n" + "=" * 70)
        print("\n🚀 CÓMO USAR:")
        print("-" * 70)
        print("\n1. Inicia el servidor:")
        print("   docker-compose up -d")
        print("\n2. Ve a la documentación:")
        print("   http://localhost:8000/docs")
        print("\n3. Haz login en POST /api/v1/auth/login con cualquier usuario:")
        print("   {")
        print('     "email": "admin@ithaka.com",')
        print('     "password": "admin123"')
        print("   }")
        print("\n4. Copia el access_token de la respuesta")
        print("\n5. Click en 'Authorize' (arriba derecha)")
        print("   Pega: Bearer <tu_token>")
        print("\n6. Ahora puedes usar todos los endpoints\n")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()
