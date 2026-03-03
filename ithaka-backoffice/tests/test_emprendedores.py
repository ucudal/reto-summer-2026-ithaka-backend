"""
Tests para el endpoint de Emprendedores
"""
import pytest
from app.models.emprendedor import Emprendedor
from app.models.caso import Caso
from app.models.asignacion import Asignacion


# =============================================================================
# TESTS: LISTAR EMPRENDEDORES
# =============================================================================

def test_listar_emprendedores_vacio(client, headers_admin):
    """Test listar cuando no hay emprendedores"""
    response = client.get("/api/v1/emprendedores/", headers=headers_admin)
    assert response.status_code == 200
    assert response.json() == []


def test_listar_emprendedores_admin(client, db, headers_admin, emprendedor_test):
    """Admin puede ver todos los emprendedores"""
    response = client.get("/api/v1/emprendedores/", headers=headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["nombre"] == emprendedor_test.nombre
    assert data[0]["apellido"] == emprendedor_test.apellido


def test_listar_emprendedores_coordinador(client, headers_coordinador, emprendedor_test):
    """Coordinador puede ver todos los emprendedores"""
    response = client.get("/api/v1/emprendedores/", headers=headers_coordinador)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_listar_emprendedores_tutor_sin_casos(client, headers_tutor):
    """Tutor sin casos asignados no ve emprendedores"""
    response = client.get("/api/v1/emprendedores/", headers=headers_tutor)
    assert response.status_code == 200
    assert response.json() == []


def test_listar_emprendedores_tutor_con_caso_asignado(
    client, db, headers_tutor, emprendedor_test, caso_test, usuario_tutor
):
    """Tutor solo ve emprendedores de sus casos asignados"""
    # Asignar caso al tutor
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get("/api/v1/emprendedores/", headers=headers_tutor)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id_emprendedor"] == emprendedor_test.id_emprendedor


def test_listar_emprendedores_sin_autenticacion(client):
    """No se puede listar sin autenticación"""
    response = client.get("/api/v1/emprendedores/")
    assert response.status_code == 401


def test_listar_emprendedores_con_paginacion(client, db, headers_admin):
    """Test de paginación"""
    # Crear varios emprendedores
    for i in range(5):
        emp = Emprendedor(
            nombre=f"Nombre{i}",
            apellido=f"Apellido{i}",
            documento_identidad=f"1234567{i}",
            email=f"test{i}@example.com"
        )
        db.add(emp)
    db.commit()
    
    # Obtener solo 2
    response = client.get("/api/v1/emprendedores/?skip=0&limit=2", headers=headers_admin)
    assert response.status_code == 200
    assert len(response.json()) == 2


# =============================================================================
# TESTS: OBTENER EMPRENDEDOR POR ID
# =============================================================================

def test_obtener_emprendedor_admin(client, headers_admin, emprendedor_test):
    """Admin puede obtener cualquier emprendedor"""
    response = client.get(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        headers=headers_admin
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == emprendedor_test.nombre
    assert data["email"] == emprendedor_test.email


def test_obtener_emprendedor_coordinador(client, headers_coordinador, emprendedor_test):
    """Coordinador puede obtener cualquier emprendedor"""
    response = client.get(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        headers=headers_coordinador
    )
    assert response.status_code == 200


def test_obtener_emprendedor_tutor_sin_acceso(client, headers_tutor, emprendedor_test):
    """Tutor no puede ver emprendedor si no tiene caso asignado"""
    response = client.get(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        headers=headers_tutor
    )
    assert response.status_code == 403
    assert "No tienes acceso" in response.json()["detail"]


def test_obtener_emprendedor_tutor_con_acceso(
    client, db, headers_tutor, emprendedor_test, caso_test, usuario_tutor
):
    """Tutor puede ver emprendedor si tiene caso asignado"""
    # Asignar caso
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        headers=headers_tutor
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == emprendedor_test.nombre


def test_obtener_emprendedor_inexistente(client, headers_admin):
    """Intentar obtener emprendedor que no existe"""
    response = client.get("/api/v1/emprendedores/99999", headers=headers_admin)
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]


def test_obtener_emprendedor_sin_autenticacion(client, emprendedor_test):
    """No se puede obtener emprendedor sin autenticación"""
    response = client.get(f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}")
    assert response.status_code == 401


# =============================================================================
# TESTS: CREAR EMPRENDEDOR
# =============================================================================

def test_crear_emprendedor_admin(client, db, headers_admin):
    """Admin puede crear emprendedor"""
    nuevo_emprendedor = {
        "nombre": "María",
        "apellido": "González",
        "documento_identidad": "87654321",
        "email": "maria@example.com",
        "telefono": "099888777"
    }
    
    response = client.post(
        "/api/v1/emprendedores/",
        json=nuevo_emprendedor,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == nuevo_emprendedor["nombre"]
    assert data["email"] == nuevo_emprendedor["email"]
    assert "id_emprendedor" in data


def test_crear_emprendedor_campos_minimos(client, db, headers_admin):
    """Crear emprendedor con campos mínimos requeridos"""
    nuevo_emprendedor = {
        "nombre": "Pedro",
        "apellido": "López",
        "documento_identidad": "11223344",
        "email": "pedro@example.com"
    }
    
    response = client.post(
        "/api/v1/emprendedores/",
        json=nuevo_emprendedor,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Pedro"
    assert data["telefono"] is None or data["telefono"] == ""


def test_crear_emprendedor_coordinador_no_permitido(client, headers_coordinador):
    """Coordinador no puede crear emprendedor"""
    nuevo_emprendedor = {
        "nombre": "Test",
        "apellido": "Test",
        "documento_identidad": "12345678",
        "email": "test@test.com"
    }
    
    response = client.post(
        "/api/v1/emprendedores/",
        json=nuevo_emprendedor,
        headers=headers_coordinador
    )
    
    assert response.status_code == 403


def test_crear_emprendedor_tutor_no_permitido(client, headers_tutor):
    """Tutor no puede crear emprendedor"""
    nuevo_emprendedor = {
        "nombre": "Test",
        "apellido": "Test",
        "documento_identidad": "12345678",
        "email": "test@test.com"
    }
    
    response = client.post(
        "/api/v1/emprendedores/",
        json=nuevo_emprendedor,
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_crear_emprendedor_email_invalido(client, headers_admin):
    """Validar email inválido"""
    nuevo_emprendedor = {
        "nombre": "Test",
        "apellido": "Test",
        "documento_identidad": "12345678",
        "email": "esto-no-es-un-email"
    }
    
    response = client.post(
        "/api/v1/emprendedores/",
        json=nuevo_emprendedor,
        headers=headers_admin
    )
    
    assert response.status_code == 422


def test_crear_emprendedor_sin_autenticacion(client):
    """No se puede crear emprendedor sin autenticación"""
    nuevo_emprendedor = {
        "nombre": "Test",
        "apellido": "Test",
        "documento_identidad": "12345678",
        "email": "test@test.com"
    }
    
    response = client.post("/api/v1/emprendedores/", json=nuevo_emprendedor)
    assert response.status_code == 401


# =============================================================================
# TESTS: ACTUALIZAR EMPRENDEDOR
# =============================================================================

def test_actualizar_emprendedor_admin(client, db, headers_admin, emprendedor_test):
    """Admin puede actualizar emprendedor"""
    actualizacion = {
        "telefono": "099999999",
        "email": "nuevo_email@example.com"
    }
    
    response = client.put(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["telefono"] == actualizacion["telefono"]
    assert data["email"] == actualizacion["email"]


def test_actualizar_emprendedor_parcial(client, db, headers_admin, emprendedor_test):
    """Actualización parcial de emprendedor"""
    email_original = emprendedor_test.email
    actualizacion = {
        "nombre": "NuevoNombre"
    }
    
    response = client.put(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "NuevoNombre"
    assert data["email"] == email_original  # Email no cambió


def test_actualizar_emprendedor_inexistente(client, headers_admin):
    """Intentar actualizar emprendedor inexistente"""
    response = client.put(
        "/api/v1/emprendedores/99999",
        json={"nombre": "Test"},
        headers=headers_admin
    )
    assert response.status_code == 404


def test_actualizar_emprendedor_coordinador_no_permitido(
    client, headers_coordinador, emprendedor_test
):
    """Coordinador no puede actualizar emprendedor"""
    response = client.put(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        json={"nombre": "Test"},
        headers=headers_coordinador
    )
    assert response.status_code == 403


def test_actualizar_emprendedor_tutor_no_permitido(
    client, headers_tutor, emprendedor_test
):
    """Tutor no puede actualizar emprendedor"""
    response = client.put(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}",
        json={"nombre": "Test"},
        headers=headers_tutor
    )
    assert response.status_code == 403


# =============================================================================
# TESTS: OBTENER CASOS DE EMPRENDEDOR
# =============================================================================

def test_obtener_casos_emprendedor(client, emprendedor_test, caso_test):
    """Obtener casos de un emprendedor"""
    response = client.get(
        f"/api/v1/emprendedores/{emprendedor_test.id_emprendedor}/casos"
    )
    
    assert response.status_code == 200
    casos = response.json()
    assert len(casos) >= 1
    assert casos[0]["id_emprendedor"] == emprendedor_test.id_emprendedor


def test_obtener_casos_emprendedor_sin_casos(client, db, headers_admin):
    """Emprendedor sin casos retorna lista vacía"""
    emprendedor = Emprendedor(
        nombre="Sin",
        apellido="Casos",
        documento_identidad="99999999",
        email="sincasos@example.com"
    )
    db.add(emprendedor)
    db.commit()
    db.refresh(emprendedor)
    
    response = client.get(f"/api/v1/emprendedores/{emprendedor.id_emprendedor}/casos")
    assert response.status_code == 200
    assert response.json() == []


def test_obtener_casos_emprendedor_inexistente(client):
    """Intentar obtener casos de emprendedor inexistente"""
    response = client.get("/api/v1/emprendedores/99999/casos")
    assert response.status_code == 404
