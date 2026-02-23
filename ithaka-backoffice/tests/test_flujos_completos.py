"""
Tests de flujos completos end-to-end
"""
import pytest


def test_flujo_completo_creacion_caso_y_asignacion(client, db, headers_admin, headers_tutor, usuario_tutor):
    """
    Flujo completo:
    1. Admin crea emprendedor
    2. Admin crea caso
    3. Admin asigna caso al tutor
    4. Tutor puede ver el caso
    5. Tutor agrega nota
    6. Se genera auditoría
    """
    from app.models.auditoria import Auditoria
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    # 1. Admin crea emprendedor
    response = client.post(
        "/api/v1/emprendedores",
        json={
            "nombre": "Laura",
            "apellido": "Fernández",
            "documento_identidad": "99887766",
            "email": "laura@test.com",
            "telefono": "099111222"
        },
        headers=headers_admin
    )
    assert response.status_code == 201
    emprendedor_id = response.json()["id_emprendedor"]
    
    # 2. Admin crea caso
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    response = client.post(
        "/api/v1/casos",
        json={
            "nombre_caso": "Caso Laura Fernández",
            "id_emprendedor": emprendedor_id,
            "id_convocatoria": convocatoria.id_convocatoria
        },
        headers=headers_admin
    )
    assert response.status_code == 201
    caso_id = response.json()["id_caso"]
    
    # 3. Admin asigna caso al tutor
    response = client.post(
        "/api/v1/asignaciones",
        json={
            "id_caso": caso_id,
            "id_usuario": usuario_tutor.id_usuario
        },
        headers=headers_admin
    )
    assert response.status_code == 201
    
    # 4. Tutor puede ver el caso asignado
    response = client.get(
        f"/api/v1/casos/{caso_id}",
        headers=headers_tutor
    )
    assert response.status_code == 200
    assert response.json()["id_caso"] == caso_id
    
    # 5. Tutor agrega nota al caso
    response = client.post(
        "/api/v1/notas",
        json={
            "contenido": "Primera reunión realizada exitosamente",
            "id_caso": caso_id,
            "id_usuario": usuario_tutor.id_usuario
        },
        headers=headers_tutor
    )
    assert response.status_code == 201
    nota_id = response.json()["id_nota"]
    
    # 6. Verificar que se generó auditoría
    auditorias = db.query(Auditoria).filter(
        Auditoria.id_caso == caso_id
    ).all()
    assert len(auditorias) >= 2  # Mínimo: creación caso + asignación


def test_flujo_tutor_solo_ve_casos_asignados(client, db, headers_admin, headers_tutor, usuario_tutor, emprendedor_test):
    """
    Verificar que Tutor solo ve casos asignados:
    1. Crear dos casos
    2. Asignar solo uno al tutor
    3. Tutor debe ver solo 1 caso
    """
    from app.models.caso import Caso
    from app.models.asignacion import Asignacion
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    # Crear caso 1 (asignado al tutor)
    caso1 = Caso(
        nombre_caso="Caso asignado al tutor",
        id_emprendedor=emprendedor_test.id_emprendedor,
        id_estado=estado.id_estado,
        id_convocatoria=convocatoria.id_convocatoria
    )
    db.add(caso1)
    db.flush()
    
    asignacion1 = Asignacion(id_caso=caso1.id_caso, id_usuario=usuario_tutor.id_usuario)
    db.add(asignacion1)
    
    # Crear caso 2 (NO asignado al tutor)
    caso2 = Caso(
        nombre_caso="Caso NO asignado al tutor",
        id_emprendedor=emprendedor_test.id_emprendedor,
        id_estado=estado.id_estado,
        id_convocatoria=convocatoria.id_convocatoria
    )
    db.add(caso2)
    db.commit()
    
    # Listar casos como tutor
    response = client.get("/api/v1/casos", headers=headers_tutor)
    assert response.status_code == 200
    casos = response.json()
    
    # Debe ver solo 1 caso
    assert len(casos) == 1
    assert casos[0]["id_caso"] == caso1.id_caso
    
    # Intentar acceder al caso no asignado debe fallar
    response = client.get(
        f"/api/v1/casos/{caso2.id_caso}",
        headers=headers_tutor
    )
    assert response.status_code == 403


def test_flujo_cambio_estado_caso_con_auditoria(client, db, headers_admin, caso_test):
    """
    Flujo de cambio de estado de caso con auditoría:
    1. Admin cambia estado del caso
    2. Se registra en auditoría
    """
    from app.models.auditoria import Auditoria
    from app.models.catalogo_estados import CatalogoEstados
    
    # Crear otro estado
    nuevo_estado = CatalogoEstados(
        nombre_estado="En Evaluación",
        tipo_caso="Postulacion"
    )
    db.add(nuevo_estado)
    db.commit()
    
    # Cambiar estado del caso
    response = client.put(
        f"/api/v1/casos/{caso_test.id_caso}",
        json={"id_estado": nuevo_estado.id_estado},
        headers=headers_admin
    )
    assert response.status_code == 200
    
    # Verificar auditoría
    auditoria = db.query(Auditoria).filter(
        Auditoria.id_caso == caso_test.id_caso,
        Auditoria.accion.like("%actualiz%")
    ).first()
    
    assert auditoria is not None


def test_flujo_gestion_notas_por_tutor(client, db, headers_tutor, caso_test, usuario_tutor):
    """
    Flujo completo de gestión de notas por Tutor:
    1. Asignar caso
    2. Crear nota
    3. Actualizar nota
    4. Listar notas
    5. Eliminar nota
    """
    from app.models.asignacion import Asignacion
    
    # 1. Asignar caso al tutor
    asignacion = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
    db.add(asignacion)
    db.commit()
    
    # 2. Crear nota
    response = client.post(
        "/api/v1/notas",
        json={
            "contenido": "Nota inicial",
            "id_caso": caso_test.id_caso,
            "id_usuario": usuario_tutor.id_usuario
        },
        headers=headers_tutor
    )
    assert response.status_code == 201
    nota_id = response.json()["id_nota"]
    
    # 3. Actualizar nota
    response = client.put(
        f"/api/v1/notas/{nota_id}",
        json={"contenido": "Nota actualizada"},
        headers=headers_tutor
    )
    assert response.status_code == 200
    assert response.json()["contenido"] == "Nota actualizada"
    
    # 4. Listar notas del caso
    response = client.get(
        "/api/v1/notas",
        params={"id_caso": caso_test.id_caso},
        headers=headers_tutor
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # 5. Eliminar nota
    response = client.delete(
        f"/api/v1/notas/{nota_id}",
        headers=headers_tutor
    )
    assert response.status_code == 204


def test_flujo_asignacion_multiple_tutores(client, db, headers_admin, headers_tutor, caso_test, usuario_tutor):
    """
    Varios tutores pueden estar asignados al mismo caso
    """
    from app.models.usuario import Usuario
    from app.models.asignacion import Asignacion
    from app.core.security import hash_password
    
    # Crear segundo tutor
    rol_tutor = db.query(Usuario).filter(Usuario.id_usuario == usuario_tutor.id_usuario).first().rol
    
    tutor2 = Usuario(
        nombre="Tutor2",
        apellido="Test",
        email="tutor2@test.com",
        password_hash=hash_password("tutor123"),
        activo=True,
        id_rol=rol_tutor.id_rol
    )
    db.add(tutor2)
    db.commit()
    
    # Asignar caso a ambos tutores
    asig1 = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
    asig2 = Asignacion(id_caso=caso_test.id_caso, id_usuario=tutor2.id_usuario)
    db.add_all([asig1, asig2])
    db.commit()
    
    # Verificar asignaciones
    response = client.get(
        f"/api/v1/asignaciones/caso/{caso_test.id_caso}",
        headers=headers_admin
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_flujo_desactivar_reactivar_usuario(client, db, headers_admin):
    """
    Flujo de desactivar y reactivar usuario
    """
    from app.models.rol import Rol
    
    rol_coordinador = db.query(Rol).filter(Rol.nombre_rol == "Coordinador").first()
    
    # Crear usuario
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Usuario",
            "apellido": "Temporal",
            "email": "temporal@test.com",
            "password": "password123",
            "id_rol": rol_coordinador.id_rol
        },
        headers=headers_admin
    )
    assert response.status_code == 201
    usuario_id = response.json()["id_usuario"]
    
    # Desactivar usuario
    response = client.delete(
        f"/api/v1/usuarios/{usuario_id}",
        headers=headers_admin
    )
    assert response.status_code == 204
    
    # Verificar que está inactivo
    response = client.get(
        f"/api/v1/usuarios/{usuario_id}",
        headers=headers_admin
    )
    assert response.status_code == 200
    assert response.json()["activo"] == False
    
    # Reactivar usuario
    response = client.put(
        f"/api/v1/usuarios/{usuario_id}/reactivar",
        headers=headers_admin
    )
    assert response.status_code == 200
    assert response.json()["activo"] == True


def test_asignacion_solo_permite_tutores(client, db, headers_admin, caso_test, usuario_coordinador, usuario_admin):
    """
    Verificar que solo se pueden asignar tutores a casos.
    Coordinadores y Admins no pueden ser asignados.
    """
    # Intentar asignar coordinador (debe fallar)
    response = client.post(
        "/api/v1/asignaciones",
        json={
            "id_caso": caso_test.id_caso,
            "id_usuario": usuario_coordinador.id_usuario
        },
        headers=headers_admin
    )
    assert response.status_code == 400
    assert "Tutor" in response.json()["detail"]
    
    # Intentar asignar admin (debe fallar)
    response = client.post(
        "/api/v1/asignaciones",
        json={
            "id_caso": caso_test.id_caso,
            "id_usuario": usuario_admin.id_usuario
        },
        headers=headers_admin
    )
    assert response.status_code == 400
    assert "Tutor" in response.json()["detail"]


def test_asignacion_duplicada_no_permitida(client, db, headers_admin, caso_test, usuario_tutor):
    """
    Verificar que no se puede asignar el mismo tutor dos veces al mismo caso
    """
    from app.models.asignacion import Asignacion
    
    # Crear primera asignación
    asignacion = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
    db.add(asignacion)
    db.commit()
    
    # Intentar crear asignación duplicada (debe fallar)
    response = client.post(
        "/api/v1/asignaciones",
        json={
            "id_caso": caso_test.id_caso,
            "id_usuario": usuario_tutor.id_usuario
        },
        headers=headers_admin
    )
    assert response.status_code == 400
    assert "ya está asignado" in response.json()["detail"]
