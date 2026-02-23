"""
Fixtures compartidos para todos los tests
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configurar variables de entorno ANTES de importar la app
os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_PASSWORD"] = "test_password"
os.environ["POSTGRES_DB"] = "test_db"
os.environ["SECRET_KEY"] = "test_secret_key_for_testing_only_not_secure"

from main import app
from app.db.database import Base
from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.emprendedor import Emprendedor
from app.models.caso import Caso
from app.models.catalogo_estados import CatalogoEstados
from app.models.convocatoria import Convocatoria
from app.models.programa import Programa

# Base de datos de prueba en memoria (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Mantener una sola conexión para SQLite en memoria
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Base de datos limpia para cada test.
    Se crea y destruye para cada función de test.
    """
    # Limpiar tablas existentes antes de crear
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Crear datos básicos que todos los tests necesitan
    _crear_datos_basicos(db)
    
    try:
        yield db
    finally:
        db.rollback()  # Rollback cualquier transacción pendiente
        db.close()
        # NO hacemos drop_all aquí porque otros fixtures pueden seguir usando el engine


@pytest.fixture(scope="function")
def client(db):
    """
    Cliente de pruebas con la base de datos de test inyectada
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def rol_admin(db):
    """Rol de Admin"""
    rol = db.query(Rol).filter(Rol.nombre_rol == "Admin").first()
    return rol


@pytest.fixture
def rol_coordinador(db):
    """Rol de Coordinador"""
    rol = db.query(Rol).filter(Rol.nombre_rol == "Coordinador").first()
    return rol


@pytest.fixture
def rol_tutor(db):
    """Rol de Tutor"""
    rol = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
    return rol


@pytest.fixture
def usuario_admin(db, rol_admin):
    """Usuario Admin de prueba"""
    usuario = Usuario(
        nombre="Admin",
        apellido="Test",
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        activo=True,
        id_rol=rol_admin.id_rol
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture
def usuario_coordinador(db, rol_coordinador):
    """Usuario Coordinador de prueba"""
    usuario = Usuario(
        nombre="Coordinador",
        apellido="Test",
        email="coordinador@test.com",
        password_hash=hash_password("coord123"),
        activo=True,
        id_rol=rol_coordinador.id_rol
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture
def usuario_tutor(db, rol_tutor):
    """Usuario Tutor de prueba"""
    usuario = Usuario(
        nombre="Tutor",
        apellido="Test",
        email="tutor@test.com",
        password_hash=hash_password("tutor123"),
        activo=True,
        id_rol=rol_tutor.id_rol
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture
def admin_token(usuario_admin):
    """Token JWT de Admin"""
    return create_access_token({"sub": str(usuario_admin.id_usuario)})


@pytest.fixture
def coordinador_token(usuario_coordinador):
    """Token JWT de Coordinador"""
    return create_access_token({"sub": str(usuario_coordinador.id_usuario)})


@pytest.fixture
def tutor_token(usuario_tutor):
    """Token JWT de Tutor"""
    return create_access_token({"sub": str(usuario_tutor.id_usuario)})


@pytest.fixture
def emprendedor_test(db):
    """Emprendedor de prueba"""
    emprendedor = Emprendedor(
        nombre="Juan",
        apellido="Pérez",
        documento_identidad="12345678",
        email="juan.perez@test.com",
        telefono="099123456"
    )
    db.add(emprendedor)
    db.commit()
    db.refresh(emprendedor)
    return emprendedor


@pytest.fixture
def caso_test(db, emprendedor_test):
    """Caso de prueba"""
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    caso = Caso(
        nombre_caso="Caso de prueba",
        descripcion="Este es un caso de prueba",
        id_emprendedor=emprendedor_test.id_emprendedor,
        id_estado=estado.id_estado,
        id_convocatoria=convocatoria.id_convocatoria
    )
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


def _crear_datos_basicos(db):
    """Crear datos básicos necesarios para los tests"""
    
    # Crear roles
    roles = [
        Rol(nombre_rol="Admin"),
        Rol(nombre_rol="Coordinador"),
        Rol(nombre_rol="Tutor")
    ]
    db.add_all(roles)
    db.commit()
    
    # Crear estado default
    estado = CatalogoEstados(
        nombre_estado="Postulado",
        tipo_caso="Postulacion"
    )
    db.add(estado)
    db.commit()
    
    # Crear convocatoria default
    from datetime import datetime
    convocatoria = Convocatoria(
        nombre="Convocatoria Test 2026",
        fecha_cierre=datetime(2026, 12, 31)
    )
    db.add(convocatoria)
    db.commit()
    
    # Crear programa default
    programa = Programa(
        nombre="Programa Test",
        activo=True
    )
    db.add(programa)
    db.commit()


@pytest.fixture
def headers_admin(admin_token):
    """Headers con token de Admin"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def headers_coordinador(coordinador_token):
    """Headers con token de Coordinador"""
    return {"Authorization": f"Bearer {coordinador_token}"}


@pytest.fixture
def headers_tutor(tutor_token):
    """Headers con token de Tutor"""
    return {"Authorization": f"Bearer {tutor_token}"}
