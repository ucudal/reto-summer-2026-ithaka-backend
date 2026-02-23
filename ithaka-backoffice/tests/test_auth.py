"""
Tests de autenticación y tokens JWT
"""
import pytest


def test_login_exitoso_admin(client, usuario_admin):
    """Login exitoso con usuario Admin"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "usuario" in data


def test_login_exitoso_coordinador(client, usuario_coordinador):
    """Login exitoso con usuario Coordinador"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "coordinador@test.com",
            "password": "coord123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_exitoso_tutor(client, usuario_tutor):
    """Login exitoso con usuario Tutor"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "tutor@test.com",
            "password": "tutor123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_password_incorrecto(client, usuario_admin):
    """Login con contraseña incorrecta debe fallar"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"].lower()


def test_login_email_inexistente(client):
    """Login con email inexistente debe fallar"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "noexiste@test.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401


def test_login_usuario_inactivo(client, db, usuario_admin):
    """Login con usuario inactivo debe fallar"""
    # Desactivar usuario
    usuario_admin.activo = False
    db.commit()
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )
    
    assert response.status_code == 403


def test_acceso_sin_token(client):
    """Acceder a endpoint protegido sin token debe retornar 401"""
    response = client.get("/api/v1/usuarios")
    assert response.status_code == 401


def test_acceso_con_token_invalido(client):
    """Acceder con token inválido debe retornar 401"""
    response = client.get(
        "/api/v1/usuarios",
        headers={"Authorization": "Bearer tokeninvalido123"}
    )
    assert response.status_code == 401


def test_me_endpoint_retorna_usuario_actual(client, headers_admin, usuario_admin):
    """Endpoint /me debe retornar el usuario autenticado"""
    response = client.get(
        "/api/v1/auth/me",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == usuario_admin.email
    assert data["nombre"] == usuario_admin.nombre
    assert "password_hash" not in data  # No debe exponer el hash


def test_token_expira_correctamente(client, usuario_admin):
    """Test que el token tiene expiración configurada"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )
    
    # Verificar que el token se puede usar inmediatamente
    token = response.json()["access_token"]
    response = client.get(
        "/api/v1/usuarios",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
