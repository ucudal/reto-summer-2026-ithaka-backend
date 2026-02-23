"""
Tests específicos de endpoints de casos
"""
import pytest


def test_listar_casos_vacio(client, headers_admin):
    """Listar casos sin datos debe retornar lista vacía"""
    response = client.get("/api/v1/casos", headers=headers_admin)
    assert response.status_code == 200
    assert response.json() == []


def test_crear_caso_valido(client, db, headers_admin, emprendedor_test):
    """Crear caso con datos válidos"""
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    response = client.post(
        "/api/v1/casos",
        json={
            "nombre_caso": "Caso de prueba",
            "id_emprendedor": emprendedor_test.id_emprendedor,
            "id_estado": estado.id_estado,
            "id_convocatoria": convocatoria.id_convocatoria
        },
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["id_emprendedor"] == emprendedor_test.id_emprendedor
    assert data["id_estado"] == estado.id_estado


def test_crear_caso_emprendedor_inexistente(client, db, headers_admin):
    """Crear caso con emprendedor inexistente debe fallar"""
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    response = client.post(
        "/api/v1/casos",
        json={
            "nombre_caso": "Caso inexistente",
            "id_emprendedor": 99999,
            "id_estado": estado.id_estado,
            "id_convocatoria": convocatoria.id_convocatoria
        },
        headers=headers_admin
    )
    
    assert response.status_code in [400, 404, 422]


def test_obtener_caso_por_id(client, headers_admin, caso_test):
    """Obtener caso específico por ID"""
    response = client.get(
        f"/api/v1/casos/{caso_test.id_caso}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id_caso"] == caso_test.id_caso


def test_obtener_caso_inexistente(client, headers_admin):
    """Obtener caso inexistente debe retornar 404"""
    response = client.get(
        "/api/v1/casos/99999",
        headers=headers_admin
    )
    
    assert response.status_code == 404


def test_actualizar_caso(client, db, headers_admin, caso_test):
    """Actualizar estado de caso"""
    from app.models.catalogo_estados import CatalogoEstados
    
    nuevo_estado = CatalogoEstados(
        nombre_estado="Completado",
        tipo_caso="Postulacion"
    )
    db.add(nuevo_estado)
    db.commit()
    
    response = client.put(
        f"/api/v1/casos/{caso_test.id_caso}",
        json={"id_estado": nuevo_estado.id_estado},
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["id_estado"] == nuevo_estado.id_estado


def test_eliminar_caso_no_implementado(client, headers_admin, caso_test):
    """DELETE de casos puede estar deshabilitado por integridad"""
    response = client.delete(
        f"/api/v1/casos/{caso_test.id_caso}",
        headers=headers_admin
    )
    
    # Puede retornar 405 (método no permitido) o 403 dependiendo de implementación
    assert response.status_code in [403, 404, 405]


def test_tutor_no_ve_caso_no_asignado(client, headers_tutor, caso_test):
    """Tutor no puede ver caso que no le fue asignado"""
    response = client.get(
        f"/api/v1/casos/{caso_test.id_caso}",
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_tutor_ve_caso_asignado(client, db, headers_tutor, caso_test, usuario_tutor):
    """Tutor SÍ puede ver caso asignado"""
    from app.models.asignacion import Asignacion
    
    # Asignar caso
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    response = client.get(
        f"/api/v1/casos/{caso_test.id_caso}",
        headers=headers_tutor
    )
    
    assert response.status_code == 200
    assert response.json()["id_caso"] == caso_test.id_caso


def test_coordinador_puede_ver_todos_casos(client, headers_coordinador, caso_test):
    """Coordinador puede ver todos los casos"""
    response = client.get(
        f"/api/v1/casos/{caso_test.id_caso}",
        headers=headers_coordinador
    )
    
    assert response.status_code == 200


def test_listar_casos_con_filtro_emprendedor(client, db, headers_admin, emprendedor_test, caso_test):
    """Filtrar casos por emprendedor"""
    response = client.get(
        "/api/v1/casos",
        params={"id_emprendedor": emprendedor_test.id_emprendedor},
        headers=headers_admin
    )
    
    assert response.status_code == 200
    casos = response.json()
    
    # Debe retornar al menos el caso_test
    assert len(casos) >= 1
    
    # Todos los casos retornados deben tener el campo emprendedor (nombre)
    emprendedor_nombre_completo = f"{emprendedor_test.nombre} {emprendedor_test.apellido}"
    for caso in casos:
        assert caso["emprendedor"] == emprendedor_nombre_completo


def test_crear_multiples_casos_mismo_emprendedor(client, db, headers_admin, emprendedor_test):
    """Un emprendedor puede tener múltiples casos"""
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    # Crear primer caso
    response1 = client.post(
        "/api/v1/casos",
        json={
            "nombre_caso": "Primer caso",
            "id_emprendedor": emprendedor_test.id_emprendedor,
            "id_estado": estado.id_estado,
            "id_convocatoria": convocatoria.id_convocatoria
        },
        headers=headers_admin
    )
    
    # Crear segundo caso
    response2 = client.post(
        "/api/v1/casos",
        json={
            "nombre_caso": "Segundo caso",
            "id_emprendedor": emprendedor_test.id_emprendedor,
            "id_estado": estado.id_estado,
            "id_convocatoria": convocatoria.id_convocatoria
        },
        headers=headers_admin
    )
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response1.json()["id_caso"] != response2.json()["id_caso"]
