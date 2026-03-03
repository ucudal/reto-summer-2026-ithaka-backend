"""
Tests para el endpoint de Catálogo de Estados
"""
import pytest
from app.models.catalogo_estados import CatalogoEstados


# =============================================================================
# TESTS: LISTAR ESTADOS
# =============================================================================

def test_listar_estados_admin(client, db, headers_admin):
    """Admin puede listar estados"""
    response = client.get("/api/v1/catalogo-estados/", headers=headers_admin)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_estados_coordinador(client, headers_coordinador):
    """Coordinador puede listar estados"""
    response = client.get("/api/v1/catalogo-estados/", headers=headers_coordinador)
    assert response.status_code == 200


def test_listar_estados_tutor(client, headers_tutor):
    """Tutor puede listar estados"""
    response = client.get("/api/v1/catalogo-estados/", headers=headers_tutor)
    assert response.status_code == 200


def test_listar_estados_filtro_tipo_caso(client, db, headers_admin):
    """Filtrar estados por tipo_caso"""
    # Crear estado de proyecto
    estado_proyecto = CatalogoEstados(
        nombre_estado="En desarrollo",
        tipo_caso="proyecto"
    )
    db.add(estado_proyecto)
    db.commit()
    
    response = client.get(
        "/api/v1/catalogo-estados/?tipo_caso=proyecto",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    # Todos deben ser tipo proyecto (case-insensitive)
    for estado in data:
        assert estado["tipo_caso"].lower() == "proyecto"


def test_listar_estados_sin_autenticacion(client):
    """No se puede listar sin autenticación"""
    response = client.get("/api/v1/catalogo-estados/")
    assert response.status_code == 401


def test_listar_estados_normaliza_minusculas(client, db, headers_admin):
    """Los estados se devuelven en minúsculas"""
    response = client.get("/api/v1/catalogo-estados/", headers=headers_admin)
    assert response.status_code == 200
    
    data = response.json()
    for estado in data:
        # Verificar que están en minúscula
        assert estado["nombre_estado"] == estado["nombre_estado"].lower()
        assert estado["tipo_caso"] == estado["tipo_caso"].lower()


# =============================================================================
# TESTS: OBTENER ESTADO POR ID
# =============================================================================

def test_obtener_estado_admin(client, db, headers_admin):
    """Admin puede obtener estado"""
    estado = db.query(CatalogoEstados).first()
    
    response = client.get(
        f"/api/v1/catalogo-estados/{estado.id_estado}",
        headers=headers_admin
    )
    assert response.status_code == 200


def test_obtener_estado_inexistente(client, headers_admin):
    """Intentar obtener estado inexistente"""
    response = client.get("/api/v1/catalogo-estados/99999", headers=headers_admin)
    assert response.status_code == 404


def test_obtener_estado_coordinador(client, db, headers_coordinador):
    """Coordinador puede obtener estado"""
    estado = db.query(CatalogoEstados).first()
    
    response = client.get(
        f"/api/v1/catalogo-estados/{estado.id_estado}",
        headers=headers_coordinador
    )
    assert response.status_code == 200


# =============================================================================
# TESTS: CREAR ESTADO
# =============================================================================

def test_crear_estado_admin(client, headers_admin):
    """Admin puede crear estado"""
    nuevo_estado = {
        "nombre_estado": "aprobado",
        "tipo_caso": "postulacion"
    }
    
    response = client.post(
        "/api/v1/catalogo-estados/",
        json=nuevo_estado,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre_estado"] == nuevo_estado["nombre_estado"]
    assert "id_estado" in data


def test_crear_estado_coordinador_no_permitido(client, headers_coordinador):
    """Coordinador no puede crear estado"""
    nuevo_estado = {
        "nombre_estado": "Test",
        "tipo_caso": "postulacion"
    }
    
    response = client.post(
        "/api/v1/catalogo-estados/",
        json=nuevo_estado,
        headers=headers_coordinador
    )
    
    assert response.status_code == 403


def test_crear_estado_tutor_no_permitido(client, headers_tutor):
    """Tutor no puede crear estado"""
    response = client.post(
        "/api/v1/catalogo-estados/",
        json={"nombre_estado": "Test", "tipo_caso": "postulacion"},
        headers=headers_tutor
    )
    assert response.status_code == 403


# =============================================================================
# TESTS: ACTUALIZAR ESTADO
# =============================================================================

def test_actualizar_estado_admin(client, db, headers_admin):
    """Admin puede actualizar estado"""
    estado = db.query(CatalogoEstados).first()
    
    actualizacion = {
        "nombre_estado": "actualizado"
    }
    
    response = client.put(
        f"/api/v1/catalogo-estados/{estado.id_estado}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["nombre_estado"] == "actualizado"


def test_actualizar_estado_coordinador_no_permitido(client, db, headers_coordinador):
    """Coordinador no puede actualizar estado"""
    estado = db.query(CatalogoEstados).first()
    
    response = client.put(
        f"/api/v1/catalogo-estados/{estado.id_estado}",
        json={"nombre_estado": "Test"},
        headers=headers_coordinador
    )
    
    assert response.status_code == 403


def test_actualizar_estado_inexistente(client, headers_admin):
    """Intentar actualizar estado inexistente"""
    response = client.put(
        "/api/v1/catalogo-estados/99999",
        json={"nombre_estado": "Test"},
        headers=headers_admin
    )
    assert response.status_code == 404


# =============================================================================
# TESTS: ELIMINAR ESTADO
# =============================================================================

def test_eliminar_estado_admin(client, db, headers_admin):
    """Admin puede eliminar estado sin casos"""
    estado = CatalogoEstados(
        nombre_estado="A Eliminar",
        tipo_caso="postulacion"
    )
    db.add(estado)
    db.commit()
    db.refresh(estado)
    
    response = client.delete(
        f"/api/v1/catalogo-estados/{estado.id_estado}",
        headers=headers_admin
    )
    
    assert response.status_code == 204


def test_eliminar_estado_con_casos_no_permitido(client, db, headers_admin, caso_test):
    """No se puede eliminar estado con casos asociados"""
    # El caso_test usa un estado, intentar eliminarlo
    response = client.delete(
        f"/api/v1/catalogo-estados/{caso_test.id_estado}",
        headers=headers_admin
    )
    
    assert response.status_code == 400


def test_eliminar_estado_coordinador_no_permitido(client, db, headers_coordinador):
    """Coordinador no puede eliminar estado"""
    estado = db.query(CatalogoEstados).first()
    
    response = client.delete(
        f"/api/v1/catalogo-estados/{estado.id_estado}",
        headers=headers_coordinador
    )
    
    assert response.status_code == 403
