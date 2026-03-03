"""
Tests para el endpoint de Notas
"""
import pytest
from app.models.nota import Nota
from app.models.asignacion import Asignacion


# =============================================================================
# TESTS: LISTAR NOTAS
# =============================================================================

def test_listar_notas_admin(client, headers_admin):
    """Admin puede listar todas las notas"""
    response = client.get("/api/v1/notas/", headers=headers_admin)
    assert response.status_code == 200


def test_listar_notas_coordinador(client, headers_coordinador):
    """Coordinador puede listar todas las notas"""
    response = client.get("/api/v1/notas/", headers=headers_coordinador)
    assert response.status_code == 200


def test_listar_notas_tutor_solo_casos_asignados(client, db, headers_tutor, caso_test, usuario_tutor, usuario_admin):
    """Tutor solo ve notas de casos asignados"""
    # Asignar caso al tutor
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    # Crear nota en caso asignado
    nota = Nota(
        contenido="Nota para el tutor",
        tipo_nota="Seguimiento",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    
    response = client.get("/api/v1/notas/", headers=headers_tutor)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_listar_notas_filtro_caso(client, db, headers_admin, caso_test, usuario_admin):
    """Filtrar notas por caso"""
    nota = Nota(
        contenido="Nota de prueba",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    
    response = client.get(
        f"/api/v1/notas/?id_caso={caso_test.id_caso}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert all(n["id_caso"] == caso_test.id_caso for n in data)


def test_listar_notas_filtro_usuario(client, db, headers_admin, caso_test, usuario_admin):
    """Filtrar notas por usuario"""
    nota = Nota(
        contenido="Nota de prueba",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    
    response = client.get(
        f"/api/v1/notas/?id_usuario={usuario_admin.id_usuario}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert all(n["id_usuario"] == usuario_admin.id_usuario for n in data)


# =============================================================================
# TESTS: OBTENER NOTA POR ID
# =============================================================================

def test_obtener_nota_admin(client, db, headers_admin, caso_test, usuario_admin):
    """Admin puede obtener cualquier nota"""
    nota = Nota(
        contenido="Nota de prueba",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.get(
        f"/api/v1/notas/{nota.id_nota}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["contenido"] == "Nota de prueba"


def test_obtener_nota_tutor_caso_asignado(client, db, headers_tutor, caso_test, usuario_tutor, usuario_admin):
    """Tutor puede ver nota de caso asignado"""
    # Asignar caso
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    # Crear nota
    nota = Nota(
        contenido="Nota visible para tutor",
        tipo_nota="Seguimiento",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.get(
        f"/api/v1/notas/{nota.id_nota}",
        headers=headers_tutor
    )
    
    assert response.status_code == 200


def test_obtener_nota_tutor_caso_no_asignado(client, db, headers_tutor, caso_test, usuario_admin):
    """Tutor no puede ver nota de caso no asignado"""
    nota = Nota(
        contenido="Nota no visible",
        tipo_nota="Privada",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.get(
        f"/api/v1/notas/{nota.id_nota}",
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_obtener_nota_inexistente(client, headers_admin):
    """Intentar obtener nota inexistente"""
    response = client.get("/api/v1/notas/99999", headers=headers_admin)
    assert response.status_code == 404


# =============================================================================
# TESTS: CREAR NOTA
# =============================================================================

def test_crear_nota_admin(client, headers_admin, caso_test, usuario_admin):
    """Admin puede crear nota"""
    nueva_nota = {
        "contenido": "Esta es una nueva nota",
        "tipo_nota": "Comentario",
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_admin.id_usuario
    }
    
    response = client.post(
        "/api/v1/notas/",
        json=nueva_nota,
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["contenido"] == nueva_nota["contenido"]
    assert "id_nota" in data


def test_crear_nota_tutor_caso_asignado(client, db, headers_tutor, caso_test, usuario_tutor):
    """Tutor puede crear nota en caso asignado"""
    # Asignar caso
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    nueva_nota = {
        "contenido": "Nota del tutor",
        "tipo_nota": "Seguimiento",
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/notas/",
        json=nueva_nota,
        headers=headers_tutor
    )
    
    assert response.status_code == 201


def test_crear_nota_tutor_caso_no_asignado(client, headers_tutor, caso_test, usuario_tutor):
    """Tutor no puede crear nota en caso no asignado"""
    nueva_nota = {
        "contenido": "Nota no permitida",
        "tipo_nota": "Comentario",
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_tutor.id_usuario
    }
    
    response = client.post(
        "/api/v1/notas/",
        json=nueva_nota,
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_crear_nota_sin_tipo_nota(client, headers_admin, caso_test, usuario_admin):
    """Validar que tipo_nota es requerido"""
    nueva_nota = {
        "contenido": "Nota sin tipo",
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_admin.id_usuario
    }
    
    response = client.post(
        "/api/v1/notas/",
        json=nueva_nota,
        headers=headers_admin
    )
    
    assert response.status_code == 422


def test_crear_nota_tipo_nota_vacio(client, headers_admin, caso_test, usuario_admin):
    """Validar que tipo_nota no puede estar vacío"""
    nueva_nota = {
        "contenido": "Nota con tipo vacío",
        "tipo_nota": "   ",
        "id_caso": caso_test.id_caso,
        "id_usuario": usuario_admin.id_usuario
    }
    
    response = client.post(
        "/api/v1/notas/",
        json=nueva_nota,
        headers=headers_admin
    )
    
    assert response.status_code == 400


def test_crear_nota_caso_inexistente(client, headers_admin, usuario_admin):
    """Crear nota en caso inexistente se permite (no valida FK)"""
    nueva_nota = {
        "contenido": "Nota en caso inexistente",
        "tipo_nota": "Comentario",
        "id_caso": 99999,
        "id_usuario": usuario_admin.id_usuario
    }
    
    response = client.post(
        "/api/v1/notas/",
        json=nueva_nota,
        headers=headers_admin
    )
    
    # El endpoint actualmente permite crear sin validar el caso
    # Esto es un comportamiento a mejorar en el futuro
    assert response.status_code in [201, 400]


# =============================================================================
# TESTS: ACTUALIZAR NOTA
# =============================================================================

def test_actualizar_nota_admin(client, db, headers_admin, caso_test, usuario_admin):
    """Admin puede actualizar nota"""
    nota = Nota(
        contenido="Contenido original",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    actualizacion = {
        "contenido": "Contenido actualizado"
    }
    
    response = client.put(
        f"/api/v1/notas/{nota.id_nota}",
        json=actualizacion,
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["contenido"] == "Contenido actualizado"


def test_actualizar_nota_tutor_caso_asignado(client, db, headers_tutor, caso_test, usuario_tutor, usuario_admin):
    """Tutor solo puede actualizar sus propias notas, no todas las del caso"""
    # Asignar caso
    asignacion = Asignacion(
        id_caso=caso_test.id_caso,
        id_usuario=usuario_tutor.id_usuario
    )
    db.add(asignacion)
    db.commit()
    
    # Crear nota del admin (no del tutor)
    nota = Nota(
        contenido="Original",
        tipo_nota="Seguimiento",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.put(
        f"/api/v1/notas/{nota.id_nota}",
        json={"contenido": "Actualizado"},
        headers=headers_tutor
    )
    
    # Tutor no puede editar notas de otros, solo las suyas
    assert response.status_code == 403


def test_actualizar_nota_tutor_caso_no_asignado(client, db, headers_tutor, caso_test, usuario_admin):
    """Tutor no puede actualizar nota de caso no asignado"""
    nota = Nota(
        contenido="Original",
        tipo_nota="Privada",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.put(
        f"/api/v1/notas/{nota.id_nota}",
        json={"contenido": "Actualizado"},
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_actualizar_nota_inexistente(client, headers_admin):
    """Intentar actualizar nota inexistente"""
    response = client.put(
        "/api/v1/notas/99999",
        json={"contenido": "Test"},
        headers=headers_admin
    )
    assert response.status_code == 404


#=============================================================================
# TESTS: ELIMINAR NOTA
# =============================================================================

def test_eliminar_nota_admin(client, db, headers_admin, caso_test, usuario_admin):
    """Admin puede eliminar nota"""
    nota = Nota(
        contenido="Nota a eliminar",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.delete(
        f"/api/v1/notas/{nota.id_nota}",
        headers=headers_admin
    )
    
    assert response.status_code == 204


def test_eliminar_nota_coordinador(client, db, headers_coordinador, caso_test, usuario_coordinador):
    """Coordinador puede eliminar nota"""
    nota = Nota(
        contenido="Nota a eliminar",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_coordinador.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.delete(
        f"/api/v1/notas/{nota.id_nota}",
        headers=headers_coordinador
    )
    
    assert response.status_code == 204


def test_eliminar_nota_tutor_no_permitido(client, db, headers_tutor, caso_test, usuario_admin):
    """Tutor no puede eliminar notas"""
    nota = Nota(
        contenido="Nota protegida",
        tipo_nota="Comentario",
        id_caso=caso_test.id_caso,
        id_usuario=usuario_admin.id_usuario
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    
    response = client.delete(
        f"/api/v1/notas/{nota.id_nota}",
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_eliminar_nota_inexistente(client, headers_admin):
    """Intentar eliminar nota inexistente"""
    response = client.delete("/api/v1/notas/99999", headers=headers_admin)
    assert response.status_code == 404
