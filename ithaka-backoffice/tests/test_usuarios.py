"""
Tests específicos de endpoints de usuarios
"""
import pytest


def test_listar_usuarios(client, headers_admin, usuario_admin, usuario_coordinador, usuario_tutor):
    """Listar usuarios debe retornar todos los usuarios activos"""
    response = client.get("/api/v1/usuarios", headers=headers_admin)
    
    assert response.status_code == 200
    usuarios = response.json()
    assert len(usuarios) >= 3  # Mínimo los 3 usuarios de fixture


def test_crear_usuario_valido(client, db, headers_admin):
    """Crear usuario con datos válidos"""
    from app.models.rol import Rol
    
    rol = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
    
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan.perez@test.com",
            "password": "password123",
            "id_rol": rol.id_rol
        },
        headers=headers_admin
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Juan"
    assert data["email"] == "juan.perez@test.com"
    assert "password_hash" not in data  # No debe exponer hash
    assert "password" not in data


def test_crear_usuario_email_duplicado(client, db, headers_admin, usuario_admin):
    """Crear usuario con email existente debe fallar"""
    from app.models.rol import Rol
    
    rol = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
    
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Otro",
            "apellido": "Usuario",
            "email": usuario_admin.email,  # Email duplicado
            "password": "password123",
            "id_rol": rol.id_rol
        },
        headers=headers_admin
    )
    
    assert response.status_code in [400, 409, 422]


def test_crear_usuario_email_invalido(client, db, headers_admin):
    """Crear usuario con email inválido debe fallar"""
    from app.models.rol import Rol
    
    rol = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
    
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "emailinvalido",  # Sin @
            "password": "password123",
            "id_rol": rol.id_rol
        },
        headers=headers_admin
    )
    
    assert response.status_code == 422


def test_obtener_usuario_por_id(client, headers_admin, usuario_admin):
    """Obtener usuario específico por ID"""
    response = client.get(
        f"/api/v1/usuarios/{usuario_admin.id_usuario}",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id_usuario"] == usuario_admin.id_usuario
    assert data["email"] == usuario_admin.email
    assert "password_hash" not in data


def test_obtener_usuario_inexistente(client, headers_admin):
    """Obtener usuario inexistente debe retornar 404"""
    response = client.get(
        "/api/v1/usuarios/99999",
        headers=headers_admin
    )
    
    assert response.status_code == 404


def test_actualizar_usuario(client, headers_admin, usuario_tutor):
    """Actualizar datos de usuario"""
    response = client.put(
        f"/api/v1/usuarios/{usuario_tutor.id_usuario}",
        json={
            "nombre": "NuevoNombre",
            "apellido": "NuevoApellido"
        },
        headers=headers_admin
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "NuevoNombre"
    assert data["apellido"] == "NuevoApellido"


def test_desactivar_usuario(client, db, headers_admin, usuario_tutor):
    """Desactivar usuario (soft delete)"""
    response = client.delete(
        f"/api/v1/usuarios/{usuario_tutor.id_usuario}",
        headers=headers_admin
    )
    
    assert response.status_code == 204
    
    # Verificar que el usuario está inactivo
    db.refresh(usuario_tutor)
    assert usuario_tutor.activo == False


def test_reactivar_usuario(client, db, headers_admin, usuario_tutor):
    """Reactivar usuario desactivado"""
    # Primero desactivar
    usuario_tutor.activo = False
    db.commit()
    
    # Reactivar
    response = client.put(
        f"/api/v1/usuarios/{usuario_tutor.id_usuario}/reactivar",
        headers=headers_admin
    )
    
    assert response.status_code == 200
    assert response.json()["activo"] == True


def test_cambiar_password(client, headers_admin, usuario_tutor):
    """Cambiar contraseña de usuario"""
    # TODO: Endpoint /password no existe aún, se debe implementar
    pytest.skip("Endpoint de cambio de password no implementado")
    
    response = client.put(
        f"/api/v1/usuarios/{usuario_tutor.id_usuario}/password",
        json={"password": "nuevapassword123"},
        headers=headers_admin
    )
    
    assert response.status_code == 200
    
    # Intentar login con nueva contraseña
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": usuario_tutor.email,
            "password": "nuevapassword123"
        }
    )
    
    assert login_response.status_code == 200


def test_usuario_no_puede_cambiar_rol_propio(client, db, headers_tutor, usuario_tutor):
    """Usuario no puede cambiar su propio rol"""
    from app.models.rol import Rol
    
    rol_admin = db.query(Rol).filter(Rol.nombre_rol == "Admin").first()
    
    response = client.put(
        f"/api/v1/usuarios/{usuario_tutor.id_usuario}",
        json={"id_rol": rol_admin.id_rol},
        headers=headers_tutor
    )
    
    # Debería fallar (403 o campos ignorados)
    assert response.status_code in [403, 422]


def test_tutor_puede_actualizar_su_perfil(client, headers_tutor, usuario_tutor):
    """Tutor puede actualizar su propio perfil (datos básicos)"""
    response = client.put(
        f"/api/v1/usuarios/{usuario_tutor.id_usuario}",
        json={
            "nombre": "NombreActualizado",
            "telefono": "099888777"
        },
        headers=headers_tutor
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "NombreActualizado"


def test_listar_usuarios_solo_activos(client, db, headers_admin, usuario_tutor):
    """Listar usuarios solo debe mostrar activos por defecto"""
    # Desactivar usuario
    usuario_tutor.activo = False
    db.commit()
    
    response = client.get("/api/v1/usuarios", headers=headers_admin)
    
    assert response.status_code == 200
    usuarios = response.json()
    
    # No debe incluir usuario inactivo
    ids_usuarios = [u["id_usuario"] for u in usuarios]
    assert usuario_tutor.id_usuario not in ids_usuarios


def test_password_hasheado_correctamente(client, db, headers_admin):
    """Verificar que password se guarda hasheado"""
    from app.models.rol import Rol
    from app.models.usuario import Usuario
    
    rol = db.query(Rol).filter(Rol.nombre_rol == "Tutor").first()
    
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nombre": "Test",
            "apellido": "Hash",
            "email": "testhash@test.com",
            "password": "plainpassword",
            "id_rol": rol.id_rol
        },
        headers=headers_admin
    )
    
    assert response.status_code == 201
    usuario_id = response.json()["id_usuario"]
    
    # Verificar en BD que password está hasheado
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    assert usuario.password_hash != "plainpassword"
    assert usuario.password_hash.startswith("$2b$")  # bcrypt hash
