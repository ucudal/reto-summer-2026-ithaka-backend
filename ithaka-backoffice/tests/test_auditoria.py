"""
Tests específicos de auditoría
"""
import pytest


def test_auditoria_se_crea_al_crear_caso(client, db, headers_admin, emprendedor_test):
    """Crear caso debe generar registro de auditoría"""
    from app.models.auditoria import Auditoria
    from app.models.catalogo_estados import CatalogoEstados
    from app.models.convocatoria import Convocatoria
    
    estado = db.query(CatalogoEstados).first()
    convocatoria = db.query(Convocatoria).first()
    
    response = client.post(
        "/api/v1/casos",
        json={
            "nombre_caso": "Caso de auditoría",
            "id_emprendedor": emprendedor_test.id_emprendedor,
            "id_convocatoria": convocatoria.id_convocatoria
        },
        headers=headers_admin
    )
    
    assert response.status_code == 201
    caso_id = response.json()["id_caso"]
    
    # Verificar auditoría
    auditoria = db.query(Auditoria).filter(
        Auditoria.id_caso == caso_id,
        Auditoria.accion.like("%cre%")
    ).first()
    
    assert auditoria is not None
    assert auditoria.id_usuario is not None  # Usuario actual registrado


def test_auditoria_registra_actualizacion_caso(client, db, headers_admin, caso_test):
    """Actualizar caso debe generar auditoría"""
    from app.models.auditoria import Auditoria
    from app.models.catalogo_estados import CatalogoEstados
    
    # Crear nuevo estado
    nuevo_estado = CatalogoEstados(
        nombre_estado="Revisión",
        tipo_caso="Postulacion"
    )
    db.add(nuevo_estado)
    db.commit()
    
    # Actualizar caso
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


def test_auditoria_registra_eliminacion_usuario(client, db, headers_admin, usuario_admin):
    """Desactivar usuario debe generar auditoría"""
    from app.models.auditoria import Auditoria
    from app.models.rol import Rol
    from app.models.usuario import Usuario
    
    rol = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
    
    # Crear usuario
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Usuario",
            "apellido": "Test",
            "email": "test@test.com",
            "password": "password123",
            "id_rol": rol.id_rol
        },
        headers=headers_admin
    )
    
    usuario_id = response.json()["id_usuario"]
    
    # Desactivar usuario
    response = client.delete(
        f"/api/v1/usuarios/{usuario_id}",
        headers=headers_admin
    )
    
    assert response.status_code == 204
    
    # Verificar auditoría: id_usuario es quien ejecuta la acción (el admin)
    auditoria = db.query(Auditoria).filter(
        Auditoria.id_usuario == usuario_admin.id_usuario,
        Auditoria.accion.like("%desactiv%")
    ).first()
    
    assert auditoria is not None
    assert "Usuario Test" in auditoria.valor_anterior or "Usuario Test" in auditoria.valor_nuevo


def test_admin_puede_ver_toda_auditoria(client, db, headers_admin, headers_coordinador, headers_tutor, caso_test, usuario_admin, usuario_coordinador, usuario_tutor):
    """Admin puede ver toda la auditoría del sistema"""
    from app.models.auditoria import Auditoria
    from app.models.asignacion import Asignacion
    
    # Asignar caso al tutor
    asignacion = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
    db.add(asignacion)
    
    # Crear auditorías de diferentes usuarios
    auditoria1 = Auditoria(
        accion="Acción del admin",
        id_usuario=usuario_admin.id_usuario,
        id_caso=caso_test.id_caso
    )
    auditoria2 = Auditoria(
        accion="Acción del coordinador",
        id_usuario=usuario_coordinador.id_usuario,
        id_caso=caso_test.id_caso
    )
    auditoria3 = Auditoria(
        accion="Acción del tutor",
        id_usuario=usuario_tutor.id_usuario,
        id_caso=caso_test.id_caso
    )
    db.add_all([auditoria1, auditoria2, auditoria3])
    db.commit()
    
    # Admin lista auditoría
    response = client.get("/api/v1/auditoria", headers=headers_admin)
    assert response.status_code == 200
    auditorias = response.json()
    
    # Debe ver todas (mínimo 3)
    assert len(auditorias) >= 3


def test_coordinador_puede_ver_toda_auditoria(client, db, headers_coordinador, caso_test, usuario_tutor):
    """Coordinador puede ver toda la auditoría"""
    from app.models.auditoria import Auditoria
    
    auditoria = Auditoria(
        accion="Acción del tutor",
        id_usuario=usuario_tutor.id_usuario,
        id_caso=caso_test.id_caso
    )
    db.add(auditoria)
    db.commit()
    
    response = client.get("/api/v1/auditoria", headers=headers_coordinador)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_tutor_solo_ve_su_auditoria(client, db, headers_tutor, caso_test, usuario_admin, usuario_tutor):
    """Tutor solo puede ver su propio historial"""
    from app.models.auditoria import Auditoria
    from app.models.asignacion import Asignacion
    
    # Asignar caso al tutor
    asignacion = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
    db.add(asignacion)
    
    # Crear auditorías
    auditoria_tutor = Auditoria(
        accion="Acción del tutor",
        id_usuario=usuario_tutor.id_usuario,
        id_caso=caso_test.id_caso
    )
    auditoria_admin = Auditoria(
        accion="Acción del admin",
        id_usuario=usuario_admin.id_usuario,
        id_caso=caso_test.id_caso
    )
    db.add_all([auditoria_tutor, auditoria_admin])
    db.commit()
    
    # Tutor consulta su auditoría
    response = client.get(
        f"/api/v1/auditoria/staff/{usuario_tutor.id_usuario}",
        headers=headers_tutor
    )
    
    assert response.status_code == 200
    auditorias = response.json()
    
    # Solo debe ver sus acciones
    for auditoria in auditorias:
        assert auditoria["id_usuario"] == usuario_tutor.id_usuario


def test_tutor_no_puede_ver_auditoria_de_otros(client, headers_tutor, usuario_admin):
    """Tutor no puede ver auditoría de otros usuarios"""
    response = client.get(
        f"/api/v1/auditoria/staff/{usuario_admin.id_usuario}",
        headers=headers_tutor
    )
    
    assert response.status_code == 403


def test_auditoria_contiene_valores_cambiados(client, db, headers_admin, caso_test):
    """Auditoría debe contener valor_anterior y valor_nuevo"""
    from app.models.auditoria import Auditoria
    from app.models.catalogo_estados import CatalogoEstados
    
    # Crear estado
    nuevo_estado = CatalogoEstados(
        nombre_estado="Aprobado",
        tipo_caso="Postulacion"
    )
    db.add(nuevo_estado)
    db.commit()
    
    estado_anterior = caso_test.id_estado
    
    # Actualizar caso
    response = client.put(
        f"/api/v1/casos/{caso_test.id_caso}",
        json={"id_estado": nuevo_estado.id_estado},
        headers=headers_admin
    )
    
    assert response.status_code == 200
    
    # Verificar auditoría con valores
    auditoria = db.query(Auditoria).filter(
        Auditoria.id_caso == caso_test.id_caso,
        Auditoria.accion.like("%actualiz%")
    ).first()
    
    assert auditoria is not None
    assert auditoria.valor_anterior is not None
    assert auditoria.valor_nuevo is not None


def test_auditoria_registra_creacion_usuario(client, db, headers_admin, usuario_admin):
    """Crear usuario debe generar auditoría"""
    from app.models.auditoria import Auditoria
    from app.models.rol import Rol
    
    rol = db.query(Rol).filter(Rol.nombre_rol == "Coordinador").first()
    
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Nuevo",
            "apellido": "Usuario",
            "email": "nuevo@test.com",
            "password": "password123",
            "id_rol": rol.id_rol
        },
        headers=headers_admin
    )
    
    assert response.status_code == 201
    usuario_id = response.json()["id_usuario"]
    
    # Verificar auditoría: id_usuario es quien ejecuta la acción (el admin)
    auditoria = db.query(Auditoria).filter(
        Auditoria.id_usuario == usuario_admin.id_usuario,
        Auditoria.accion.like("%cre%")
    ).first()
    
    assert auditoria is not None
    assert "Nuevo Usuario" in auditoria.valor_nuevo
