"""
Tests para el endpoint de Programas
"""
import pytest
from app.models.programa import Programa
from app.models.apoyo import Apoyo


# =============================================================================
# TESTS: LISTAR PROGRAMAS
# =============================================================================

def test_listar_programas_admin(client, db, headers_admin):
    """Admin puede listar programas"""
    response = client.get("/api/v1/programas/", headers=headers_admin)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_programas_coordinador(client, headers_coordinador):
    """Coordinador puede listar programas"""
    response = client.get("/api/v1/programas/", headers=headers_coordinador)
    assert response.status_code == 200


def test_listar_programas_tutor(client, headers_tutor):
    """Tutor puede listar programas"""
    response = client.get("/api/v1/programas/", headers=headers_tutor)
    assert response.status_code == 200


def test_listar_programas_sin_autenticacion(client):
    """No se puede listar sin autenticación"""
    response = client.get("/api/v1/programas/")
    assert response.status_code == 401


# =============================================================================
# TESTS: OBTENER PROGRAMA POR ID
# =============================================================================

def test_obtener_programa_admin(client, db, headers_admin):
    """Admin puede obtener programa"""
    programa = db.query(Programa).first()
    
    response = client.get(
        f"/api/v1/programas/{programa.id_programa}",
        headers=headers_admin
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == programa.nombre


def test_obtener_programa_inexistente(client, headers_admin):
    """Intentar obtener programa inexistente"""
    response = client.get("/api/v1/programas/99999", headers=headers_admin)
    assert response.status_code == 404


# =============================================================================
# TESTS: CREAR PROGRAMA
# =============================================================================

def test_crear_programa_admin(client, headers_admin):
    """Admin puede crear programa"""
    nuevo_programa = {
        "nombre": "Programa de Aceleración",
        "descripcion": "Programa para acelerar emprendimientos",
        "activo": True
    }
    
    response = client.post(
        "/api/v1/programas/",
        json=nuevo_programa,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == nuevo_programa["nombre"]
    assert "id_programa" in data


def test_crear_programa_coordinador(client, headers_coordinador):
    """Coordinador puede crear programa"""
    nuevo_programa = {
        "nombre": "Programa Coordinador",
        "activo": True
    }
    
    response = client.post(
        "/api/v1/programas/",
        json=nuevo_programa,
        headers=headers_coordinador
    )
    
    assert response.status_code == 201


def test_crear_programa_tutor_no_permitido(client, headers_tutor):
    """Tutor no puede crear programa"""
    nuevo_programa = {
        "nombre": "Test",
        "activo": True
    }
    
    response = client.post(
        "/api/v1/programas/",
        json=nuevo_programa,
        headers=headers_tutor
    )
    
    assert response.status_code == 403


# =============================================================================
# TESTS: ACTUALIZAR PROGRAMA
# =============================================================================

def test_actualizar_programa_admin(client, db, headers_admin):
    """Admin puede actualizar programa"""
    programa = db.query(Programa).first()
    
    actualizacion = {
        "nombre": "Programa Actualizado",
        "activo": False
    }
    
    response = client.put(
        f"/api/v1/programas/{programa.id_programa}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["nombre"] == "Programa Actualizado"


def test_actualizar_programa_coordinador(client, db, headers_coordinador):
    """Coordinador puede actualizar programa"""
    programa = db.query(Programa).first()
    
    response = client.put(
        f"/api/v1/programas/{programa.id_programa}",
        json={"nombre": "Nuevo Nombre"},
        headers=headers_coordinador
    )
    
    assert response.status_code == 200


def test_actualizar_programa_tutor_no_permitido(client, db, headers_tutor):
    """Tutor no puede actualizar programa"""
    programa = db.query(Programa).first()
    
    response = client.put(
        f"/api/v1/programas/{programa.id_programa}",
        json={"nombre": "Test"},
        headers=headers_tutor
    )
    
    assert response.status_code == 403


# =============================================================================
# TESTS: ELIMINAR PROGRAMA
# =============================================================================

def test_eliminar_programa_admin(client, db, headers_admin):
    """Admin puede eliminar programa sin referencias"""
    programa = Programa(
        nombre="Programa a Eliminar",
        activo=True
    )
    db.add(programa)
    db.commit()
    db.refresh(programa)
    
    response = client.delete(
        f"/api/v1/programas/{programa.id_programa}",
        headers=headers_admin
    )
    
    assert response.status_code == 204


def test_eliminar_programa_con_apoyos_no_permitido(client, db, headers_admin, caso_test):
    """No se puede eliminar programa con apoyos asociados"""
    from app.models.catalogo_apoyo import CatalogoApoyo
    
    programa = Programa(
        nombre="Programa con Apoyos",
        activo=True
    )
    db.add(programa)
    db.commit()
    db.refresh(programa)
    
    # Crear apoyo asociado
    catalogo = db.query(CatalogoApoyo).first()
    apoyo = Apoyo(
        id_caso=caso_test.id_caso,
        id_programa=programa.id_programa,
        id_catalogo_apoyo=catalogo.id_catalogo_apoyo
    )
    db.add(apoyo)
    db.commit()
    
    response = client.delete(
        f"/api/v1/programas/{programa.id_programa}",
        headers=headers_admin
    )
    
    assert response.status_code == 400
    assert "apoyos" in response.json()["detail"].lower()


def test_eliminar_programa_coordinador_no_permitido(client, db, headers_coordinador):
    """Coordinador no puede eliminar programa"""
    programa = db.query(Programa).first()
    
    response = client.delete(
        f"/api/v1/programas/{programa.id_programa}",
        headers=headers_coordinador
    )
    
    assert response.status_code == 403


def test_eliminar_programa_inexistente(client, headers_admin):
    """Intentar eliminar programa inexistente"""
    response = client.delete("/api/v1/programas/99999", headers=headers_admin)
    assert response.status_code == 404
