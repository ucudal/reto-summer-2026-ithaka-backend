"""
Tests para el endpoint de Convocatorias
"""
import pytest
from datetime import datetime, timedelta
from app.models.convocatoria import Convocatoria


# =============================================================================
# TESTS: LISTAR CONVOCATORIAS
# =============================================================================

def test_listar_convocatorias_admin(client, db, headers_admin):
    """Admin puede listar convocatorias"""
    response = client.get("/api/v1/convocatorias/", headers=headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Hay una convocatoria por defecto


def test_listar_convocatorias_coordinador(client, headers_coordinador):
    """Coordinador puede listar convocatorias"""
    response = client.get("/api/v1/convocatorias/", headers=headers_coordinador)
    assert response.status_code == 200


def test_listar_convocatorias_tutor(client, headers_tutor):
    """Tutor puede listar convocatorias"""
    response = client.get("/api/v1/convocatorias/", headers=headers_tutor)
    assert response.status_code == 200


def test_listar_convocatorias_sin_autenticacion(client):
    """No se puede listar sin autenticación"""
    response = client.get("/api/v1/convocatorias/")
    assert response.status_code == 401


def test_listar_convocatorias_con_paginacion(client, db, headers_admin):
    """Test de paginación"""
    # Crear varias convocatorias
    for i in range(5):
        conv = Convocatoria(
            nombre=f"Convocatoria {i}",
            fecha_cierre=datetime.now() + timedelta(days=30)
        )
        db.add(conv)
    db.commit()
    
    response = client.get("/api/v1/convocatorias/?skip=0&limit=3", headers=headers_admin)
    assert response.status_code == 200
    assert len(response.json()) == 3


# =============================================================================
# TESTS: OBTENER CONVOCATORIA POR ID
# =============================================================================

def test_obtener_convocatoria_admin(client, db, headers_admin):
    """Admin puede obtener convocatoria"""
    convocatoria = db.query(Convocatoria).first()
    
    response = client.get(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        headers=headers_admin
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == convocatoria.nombre


def test_obtener_convocatoria_coordinador(client, db, headers_coordinador):
    """Coordinador puede obtener convocatoria"""
    convocatoria = db.query(Convocatoria).first()
    
    response = client.get(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        headers=headers_coordinador
    )
    assert response.status_code == 200


def test_obtener_convocatoria_tutor(client, db, headers_tutor):
    """Tutor puede obtener convocatoria"""
    convocatoria = db.query(Convocatoria).first()
    
    response = client.get(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        headers=headers_tutor
    )
    assert response.status_code == 200


def test_obtener_convocatoria_inexistente(client, headers_admin):
    """Intentar obtener convocatoria que no existe"""
    response = client.get("/api/v1/convocatorias/99999", headers=headers_admin)
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"]


# =============================================================================
# TESTS: CREAR CONVOCATORIA
# =============================================================================

def test_crear_convocatoria_admin(client, db, headers_admin):
    """Admin puede crear convocatoria"""
    nueva_convocatoria = {
        "nombre": "Convocatoria 2027",
        "descripcion": "Nueva convocatoria para el 2027",
        "fecha_cierre": "2027-12-31T23:59:59"
    }
    
    response = client.post(
        "/api/v1/convocatorias/",
        json=nueva_convocatoria,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == nueva_convocatoria["nombre"]
    assert "id_convocatoria" in data


def test_crear_convocatoria_coordinador(client, headers_coordinador):
    """Coordinador puede crear convocatoria"""
    nueva_convocatoria = {
        "nombre": "Convocatoria Coord",
        "fecha_cierre": "2027-06-30T23:59:59"
    }
    
    response = client.post(
        "/api/v1/convocatorias/",
        json=nueva_convocatoria,
        headers=headers_coordinador
    )
    
    assert response.status_code == 201


def test_crear_convocatoria_tutor_no_permitido(client, headers_tutor):
    """Tutor no puede crear convocatoria"""
    nueva_convocatoria = {
        "nombre": "Test",
        "fecha_cierre": "2027-12-31T23:59:59"
    }
    
    response = client.post(
        "/api/v1/convocatorias/",
        json=nueva_convocatoria,
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_crear_convocatoria_campos_minimos(client, headers_admin):
    """Crear convocatoria con campos mínimos"""
    nueva_convocatoria = {
        "nombre": "Convocatoria Mínima",
        "fecha_cierre": "2027-12-31T23:59:59"
    }
    
    response = client.post(
        "/api/v1/convocatorias/",
        json=nueva_convocatoria,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Convocatoria Mínima"


def test_crear_convocatoria_sin_nombre(client, headers_admin):
    """Validar que nombre es requerido"""
    nueva_convocatoria = {
        "fecha_cierre": "2027-12-31T23:59:59"
    }
    
    response = client.post(
        "/api/v1/convocatorias/",
        json=nueva_convocatoria,
        headers=headers_admin
    )
    
    assert response.status_code == 422


# =============================================================================
# TESTS: ACTUALIZAR CONVOCATORIA
# =============================================================================

def test_actualizar_convocatoria_admin(client, db, headers_admin):
    """Admin puede actualizar convocatoria"""
    convocatoria = db.query(Convocatoria).first()
    
    actualizacion = {
        "nombre": "Nombre Actualizado"
    }
    
    response = client.put(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nombre Actualizado"


def test_actualizar_convocatoria_coordinador(client, db, headers_coordinador):
    """Coordinador puede actualizar convocatoria"""
    convocatoria = db.query(Convocatoria).first()
    
    response = client.put(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        json={"nombre": "Nuevo Nombre"},
        headers=headers_coordinador
    )
    
    assert response.status_code == 200


def test_actualizar_convocatoria_tutor_no_permitido(client, db, headers_tutor):
    """Tutor no puede actualizar convocatoria"""
    convocatoria = db.query(Convocatoria).first()
    
    response = client.put(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        json={"nombre": "Test"},
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_actualizar_convocatoria_parcial(client, db, headers_admin):
    """Actualización parcial de convocatoria"""
    from datetime import datetime
    convocatoria = db.query(Convocatoria).first()
    nombre_original = convocatoria.nombre
    
    actualizacion = {
        "fecha_cierre": "2027-06-30T00:00:00"
    }
    
    response = client.put(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nombre_original  # Nombre no cambió


def test_actualizar_convocatoria_inexistente(client, headers_admin):
    """Intentar actualizar convocatoria inexistente"""
    response = client.put(
        "/api/v1/convocatorias/99999",
        json={"nombre": "Test"},
        headers=headers_admin
    )
    assert response.status_code == 404


# =============================================================================
# TESTS: AUDITORÍA
# =============================================================================

def test_crear_convocatoria_registra_auditoria(client, db, headers_admin):
    """Crear convocatoria registra en auditoría"""
    from app.models.auditoria import Auditoria
    
    nueva_convocatoria = {
        "nombre": "Convocatoria con Auditoría",
        "fecha_cierre": "2027-12-31T23:59:59"
    }
    
    response = client.post(
        "/api/v1/convocatorias/",
        json=nueva_convocatoria,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    
    # Verificar auditoría
    auditoria = db.query(Auditoria).filter(
        Auditoria.accion == "Convocatoria creada"
    ).first()
    
    assert auditoria is not None
    assert "Convocatoria con Auditoría" in auditoria.valor_nuevo


def test_actualizar_convocatoria_registra_auditoria(client, db, headers_admin):
    """Actualizar convocatoria registra en auditoría"""
    from app.models.auditoria import Auditoria
    
    convocatoria = db.query(Convocatoria).first()
    
    response = client.put(
        f"/api/v1/convocatorias/{convocatoria.id_convocatoria}",
        json={"nombre": "Convocatoria Auditada"},
        headers=headers_admin
    )
    
    assert response.status_code == 200
    
    # Verificar auditoría
    auditoria = db.query(Auditoria).filter(
        Auditoria.accion == "Convocatoria actualizada"
    ).first()
    
    assert auditoria is not None
