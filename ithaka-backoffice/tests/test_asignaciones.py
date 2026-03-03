"""
Tests para el endpoint de Asignaciones
"""
import pytest
from app.models.asignacion import Asignacion
from app.models.caso import Caso


# =============================================================================
# TESTS: LISTAR ASIGNACIONES
# =============================================================================

def test_listar_asignaciones_admin(client, headers_admin):
    """Admin puede listar asignaciones"""
    response = client.get("/api/v1/asignaciones/", headers=headers_admin)
    assert response.status_code == 200


def test_listar_asignaciones_coordinador(client, headers_coordinador):
    """Coordinador puede listar asignaciones"""
    response = client.get("/api/v1/asignaciones/", headers=headers_coordinador)
    assert response.status_code == 200


def test_listar_asignaciones_tutor(client, headers_tutor):
    """Tutor puede listar asignaciones"""
    response = client.get("/api/v1/asignaciones/", headers=headers_tutor)
    assert response.status_code == 200


def test_listar_asignaciones_filtro_caso(client, db, headers_admin, caso_test, usuario_tutor):
    """Filtrar asignaciones por caso"""
    # Crear asignación
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get(
        f"/api/v1/asignaciones/?id_caso={caso_test.id_caso}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["id_caso"] == caso_test.id_caso


def test_listar_asignaciones_filtro_usuario(client, db, headers_admin, caso_test, usuario_tutor):
    """Filtrar asignaciones por usuario"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get(
        f"/api/v1/asignaciones/?id_usuario={usuario_tutor.id_usuario}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert all(a["id_usuario"] == usuario_tutor.id_usuario for a in data)


# =============================================================================
# TESTS: OBTENER ASIGNACIÓN POR ID
# =============================================================================

def test_obtener_asignacion_admin(client, db, headers_admin, caso_test, usuario_tutor):
    """Admin puede obtener asignación"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    
    response = client.get(
        f"/api/v1/asignaciones/{asignacion.id_asignacion}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["id_asignacion"] == asignacion.id_asignacion


def test_obtener_asignacion_inexistente(client, headers_admin):
    """Intentar obtener asignación inexistente"""
    response = client.get("/api/v1/asignaciones/99999", headers=headers_admin)
    assert response.status_code == 404


# =============================================================================
# TESTS: LISTAR POR CASO
# =============================================================================

def test_listar_asignaciones_por_caso(client, db, headers_admin, caso_test, usuario_tutor):
    """Listar asignaciones de un caso"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get(
        f"/api/v1/asignaciones/caso/{caso_test.id_caso}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_listar_asignaciones_caso_inexistente(client, headers_admin):
    """Intentar listar asignaciones de caso inexistente"""
    response = client.get("/api/v1/asignaciones/caso/99999", headers=headers_admin)
    assert response.status_code == 404


# =============================================================================
# TESTS: LISTAR POR USUARIO
# =============================================================================

def test_listar_asignaciones_por_usuario(client, db, headers_admin, caso_test, usuario_tutor):
    """Listar asignaciones de un usuario"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get(
        f"/api/v1/asignaciones/usuario/{usuario_tutor.id_usuario}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_listar_asignaciones_usuario_inexistente(client, headers_admin):
    """Intentar listar asignaciones de usuario inexistente"""
    response = client.get("/api/v1/asignaciones/usuario/99999", headers=headers_admin)
    assert response.status_code == 404


# =============================================================================
# TESTS: CREAR ASIGNACIÓN
# =============================================================================

def test_crear_asignacion_admin(client, headers_admin, caso_test, usuario_tutor):
    """Admin puede crear asignación"""
    nueva_asignacion = {
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["id_caso"] == caso_test.id_caso
    assert data["id_usuario"] == usuario_tutor.id_usuario


def test_crear_asignacion_coordinador(client, headers_coordinador, caso_test, usuario_tutor):
    """Coordinador puede crear asignación"""
    nueva_asignacion = {
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_coordinador
    )
    
    assert response.status_code == 201


def test_crear_asignacion_tutor_puede(client, headers_tutor, caso_test, usuario_tutor):
    """Tutor también puede crear asignaciones"""
    nueva_asignacion = {
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_tutor
    )
    
    assert response.status_code == 201


def test_crear_asignacion_usuario_no_tutor(client, headers_admin, caso_test, usuario_admin):
    """No se puede asignar usuario que no sea tutor"""
    nueva_asignacion = {
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_admin.id_usuario  # Admin, no Tutor
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_admin
    )
    
    assert response.status_code == 400
    assert "tutor" in response.json()["detail"].lower()


def test_crear_asignacion_duplicada(client, db, headers_admin, caso_test, usuario_tutor):
    """No se puede crear asignación duplicada"""
    # Crear primera asignación
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    # Intentar crear duplicada
    nueva_asignacion = {
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_admin
    )
    
    assert response.status_code == 400
    assert "asignado" in response.json()["detail"].lower()


def test_crear_asignacion_caso_inexistente(client, headers_admin, usuario_tutor):
    """No se puede asignar a caso inexistente"""
    nueva_asignacion = {
        "id_caso": 99999,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_admin
    )
    
    assert response.status_code == 404


def test_crear_asignacion_usuario_inexistente(client, headers_admin, caso_test):
    """No se puede asignar usuario inexistente"""
    nueva_asignacion = {
        "id_caso": caso_test.id_caso,
        "id_usuario": 99999
    }
    
    response = client.post(
        "/api/v1/asignaciones/",
        json=nueva_asignacion,
        headers=headers_admin
    )
    
    assert response.status_code == 404


# =============================================================================
# TESTS: ELIMINAR ASIGNACIÓN
# =============================================================================

def test_eliminar_asignacion_admin(client, db, headers_admin, caso_test, usuario_tutor):
    """Admin puede eliminar asignación"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    
    response = client.delete(
        f"/api/v1/asignaciones/{asignacion.id_asignacion}",
        headers=headers_admin
    )
    
    assert response.status_code == 204


def test_eliminar_asignacion_coordinador(client, db, headers_coordinador, caso_test, usuario_tutor):
    """Coordinador puede eliminar asignación"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    
    response = client.delete(
        f"/api/v1/asignaciones/{asignacion.id_asignacion}",
        headers=headers_coordinador
    )
    
    assert response.status_code == 204


def test_eliminar_asignacion_tutor_no_permitido(client, db, headers_tutor, caso_test, usuario_tutor):
    """Tutor puede eliminar asignaciones"""
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    
    response = client.delete(
        f"/api/v1/asignaciones/{asignacion.id_asignacion}",
        headers=headers_tutor
    )
    
    assert response.status_code == 204


def test_eliminar_asignacion_inexistente(client, headers_admin):
    """Intentar eliminar asignación inexistente"""
    response = client.delete("/api/v1/asignaciones/99999", headers=headers_admin)
    assert response.status_code == 404
