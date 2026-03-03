"""
Tests para el endpoint de Roles
"""
import pytest
from app.models.rol import Rol


# =============================================================================
# TESTS: LISTAR ROLES
# =============================================================================

def test_listar_roles_admin(client, headers_admin):
    """Admin puede listar roles"""
    response = client.get("/api/v1/roles/", headers=headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # Admin, Coordinador, Tutor


def test_listar_roles_coordinador_no_permitido(client, headers_coordinador):
    """Coordinador no puede listar roles"""
    response = client.get("/api/v1/roles/", headers=headers_coordinador)
    assert response.status_code == 403


def test_listar_roles_tutor_no_permitido(client, headers_tutor):
    """Tutor no puede listar roles"""
    response = client.get("/api/v1/roles/", headers=headers_tutor)
    assert response.status_code == 403


def test_listar_roles_sin_autenticacion(client):
    """No se puede listar sin autenticación"""
    response = client.get("/api/v1/roles/")
    assert response.status_code == 401


# =============================================================================
# TESTS: OBTENER ROL POR ID
# =============================================================================

def test_obtener_rol_admin(client, db, headers_admin, rol_admin):
    """Admin puede obtener rol"""
    response = client.get(
        f"/api/v1/roles/{rol_admin.id_rol}",
        headers=headers_admin
    )
    assert response.status_code == 200
    assert response.json()["nombre_rol"] == "Admin"


def test_obtener_rol_inexistente(client, headers_admin):
    """Intentar obtener rol inexistente"""
    response = client.get("/api/v1/roles/99999", headers=headers_admin)
    assert response.status_code == 404


def test_obtener_rol_coordinador_no_permitido(client, db, headers_coordinador, rol_admin):
    """Coordinador no puede obtener rol"""
    response = client.get(
        f"/api/v1/roles/{rol_admin.id_rol}",
        headers=headers_coordinador
    )
    assert response.status_code == 403


# =============================================================================
# TESTS: CREAR ROL
# =============================================================================

def test_crear_rol_admin(client, db, headers_admin):
    """Admin puede crear rol"""
    nuevo_rol = {
        "nombre_rol": "Supervisor"
    }
    
    response = client.post(
        "/api/v1/roles/",
        json=nuevo_rol,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre_rol"] == "Supervisor"
    assert "id_rol" in data


def test_crear_rol_duplicado(client, headers_admin):
    """No se puede crear rol con nombre duplicado"""
    nuevo_rol = {
        "nombre_rol": "Admin"  # Ya existe
    }
    
    response = client.post(
        "/api/v1/roles/",
        json=nuevo_rol,
        headers=headers_admin
    )
    
    assert response.status_code == 400
    assert "existe" in response.json()["detail"].lower()


def test_crear_rol_coordinador_no_permitido(client, headers_coordinador):
    """Coordinador no puede crear rol"""
    response = client.post(
        "/api/v1/roles/",
        json={"nombre_rol": "Test"},
        headers=headers_coordinador
    )
    assert response.status_code == 403


# =============================================================================
# TESTS: ACTUALIZAR ROL
# =============================================================================

def test_actualizar_rol_admin(client, db, headers_admin):
    """Admin puede actualizar rol"""
    # Crear rol para actualizar
    rol = Rol(nombre_rol="RolActualizable")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    
    actualizacion = {
        "nombre_rol": "RolActualizado"
    }
    
    response = client.put(
        f"/api/v1/roles/{rol.id_rol}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["nombre_rol"] == "RolActualizado"


def test_actualizar_rol_nombre_duplicado(client, db, headers_admin, rol_tutor):
    """No se puede actualizar a nombre duplicado"""
    # Crear nuevo rol
    rol = Rol(nombre_rol="RolNuevo")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    
    # Intentar cambiar a nombre existente
    actualizacion = {
        "nombre_rol": "Tutor"  # Ya existe
    }
    
    response = client.put(
        f"/api/v1/roles/{rol.id_rol}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 400


def test_actualizar_rol_inexistente(client, headers_admin):
    """Intentar actualizar rol inexistente"""
    response = client.put(
        "/api/v1/roles/99999",
        json={"nombre_rol": "Test"},
        headers=headers_admin
    )
    assert response.status_code == 404


def test_actualizar_rol_coordinador_no_permitido(client, db, headers_coordinador, rol_tutor):
    """Coordinador no puede actualizar rol"""
    response = client.put(
        f"/api/v1/roles/{rol_tutor.id_rol}",
        json={"nombre_rol": "Test"},
        headers=headers_coordinador
    )
    assert response.status_code == 403


# =============================================================================
# TESTS: ELIMINAR ROL
# =============================================================================

def test_eliminar_rol_admin(client, db, headers_admin):
    """Admin puede eliminar rol sin usuarios"""
    rol = Rol(nombre_rol="RolAEliminar")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    
    response = client.delete(
        f"/api/v1/roles/{rol.id_rol}",
        headers=headers_admin
    )
    
    assert response.status_code == 204


def test_eliminar_rol_con_usuarios_no_permitido(client, headers_admin, rol_admin):
    """No se puede eliminar rol con usuarios asociados"""
    response = client.delete(
        f"/api/v1/roles/{rol_admin.id_rol}",
        headers=headers_admin
    )
    
    assert response.status_code == 400


def test_eliminar_rol_inexistente(client, headers_admin):
    """Intentar eliminar rol inexistente"""
    response = client.delete("/api/v1/roles/99999", headers=headers_admin)
    assert response.status_code == 404


def test_eliminar_rol_coordinador_no_permitido(client, db, headers_coordinador):
    """Coordinador no puede eliminar rol"""
    rol = Rol(nombre_rol="Test")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    
    response = client.delete(
        f"/api/v1/roles/{rol.id_rol}",
        headers=headers_coordinador
    )
    assert response.status_code == 403
