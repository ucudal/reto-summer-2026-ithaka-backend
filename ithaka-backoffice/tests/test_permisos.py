"""
Tests de permisos por rol (RBAC)
"""
import pytest


class TestPermisosUsuarios:
    """Tests de permisos en endpoints de usuarios"""
    
    def test_admin_puede_listar_usuarios(self, client, headers_admin):
        response = client.get("/api/v1/usuarios", headers=headers_admin)
        assert response.status_code == 200
    
    def test_coordinador_puede_listar_usuarios(self, client, headers_coordinador):
        response = client.get("/api/v1/usuarios", headers=headers_coordinador)
        assert response.status_code == 200
    
    def test_tutor_no_puede_listar_usuarios(self, client, headers_tutor):
        response = client.get("/api/v1/usuarios", headers=headers_tutor)
        assert response.status_code == 403
    
    def test_admin_puede_crear_usuario(self, client, headers_admin, rol_tutor):
        response = client.post(
            "/api/v1/usuarios",
            json={
                "nombre": "Nuevo",
                "apellido": "Usuario",
                "email": "nuevo@test.com",
                "password": "password123",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 201
    
    def test_coordinador_no_puede_crear_usuario(self, client, headers_coordinador, rol_tutor):
        response = client.post(
            "/api/v1/usuarios",
            json={
                "nombre": "Nuevo",
                "apellido": "Usuario",
                "email": "nuevo@test.com",
                "password": "password123",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_coordinador
        )
        assert response.status_code == 403
    
    def test_tutor_puede_ver_su_propio_perfil(self, client, headers_tutor, usuario_tutor):
        response = client.get(
            f"/api/v1/usuarios/{usuario_tutor.id_usuario}",
            headers=headers_tutor
        )
        assert response.status_code == 200
    
    def test_tutor_no_puede_ver_perfil_ajeno(self, client, headers_tutor, usuario_admin):
        response = client.get(
            f"/api/v1/usuarios/{usuario_admin.id_usuario}",
            headers=headers_tutor
        )
        assert response.status_code == 403


class TestPermisosRoles:
    """Tests de permisos en endpoints de roles"""
    
    def test_admin_puede_listar_roles(self, client, headers_admin):
        response = client.get("/api/v1/roles", headers=headers_admin)
        assert response.status_code == 200
    
    def test_coordinador_no_puede_listar_roles(self, client, headers_coordinador):
        response = client.get("/api/v1/roles", headers=headers_coordinador)
        assert response.status_code == 403
    
    def test_tutor_no_puede_listar_roles(self, client, headers_tutor):
        response = client.get("/api/v1/roles", headers=headers_tutor)
        assert response.status_code == 403


class TestPermisosCasos:
    """Tests de permisos en endpoints de casos"""
    
    def test_admin_puede_listar_casos(self, client, headers_admin, caso_test):
        response = client.get("/api/v1/casos", headers=headers_admin)
        assert response.status_code == 200
    
    def test_coordinador_puede_listar_casos(self, client, headers_coordinador, caso_test):
        response = client.get("/api/v1/casos", headers=headers_coordinador)
        assert response.status_code == 200
    
    def test_tutor_puede_listar_casos(self, client, headers_tutor):
        """Tutor puede listar pero solo ve casos asignados"""
        response = client.get("/api/v1/casos", headers=headers_tutor)
        assert response.status_code == 200
        # Sin asignaciones, debe ver lista vacía
        assert response.json() == []
    
    def test_admin_puede_crear_caso(self, client, headers_admin, emprendedor_test, db):
        from app.models.catalogo_estados import CatalogoEstados
        from app.models.convocatoria import Convocatoria
        
        estado = db.query(CatalogoEstados).first()
        convocatoria = db.query(Convocatoria).first()
        
        response = client.post(
            "/api/v1/casos",
            json={
                "nombre_caso": "Caso de prueba",
                "id_emprendedor": emprendedor_test.id_emprendedor,
                "id_convocatoria": convocatoria.id_convocatoria
            },
            headers=headers_admin
        )
        assert response.status_code == 201
    
    def test_coordinador_no_puede_crear_caso(self, client, headers_coordinador, emprendedor_test, db):
        from app.models.catalogo_estados import CatalogoEstados
        from app.models.convocatoria import Convocatoria
        
        estado = db.query(CatalogoEstados).first()
        convocatoria = db.query(Convocatoria).first()
        
        response = client.post(
            "/api/v1/casos",
            json={
                "nombre_caso": "Caso coordinador",
                "id_emprendedor": emprendedor_test.id_emprendedor,
                "id_convocatoria": convocatoria.id_convocatoria
            },
            headers=headers_coordinador
        )
        assert response.status_code == 403
    
    def test_tutor_no_puede_crear_caso(self, client, headers_tutor, emprendedor_test, db):
        from app.models.catalogo_estados import CatalogoEstados
        from app.models.convocatoria import Convocatoria
        
        estado = db.query(CatalogoEstados).first()
        convocatoria = db.query(Convocatoria).first()
        
        response = client.post(
            "/api/v1/casos",
            json={
                "nombre_caso": "Caso tutor",
                "id_emprendedor": emprendedor_test.id_emprendedor,
                "id_convocatoria": convocatoria.id_convocatoria
            },
            headers=headers_tutor
        )
        assert response.status_code == 403


class TestPermisosNotas:
    """Tests de permisos en endpoints de notas"""
    
    def test_tutor_solo_puede_editar_sus_propias_notas(self, client, db, headers_tutor, headers_coordinador, caso_test, usuario_tutor, usuario_coordinador):
        """Tutor solo puede editar notas que él mismo creó"""
        from app.models.nota import Nota
        from app.models.asignacion import Asignacion
        
        # Asignar caso al tutor
        asignacion = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
        db.add(asignacion)
        db.commit()
        
        # Coordinador crea una nota
        nota = Nota(
            contenido="Nota del coordinador",
            id_caso=caso_test.id_caso,
            id_usuario=usuario_coordinador.id_usuario
        )
        db.add(nota)
        db.commit()
        db.refresh(nota)
        
        # Tutor intenta editar nota del coordinador
        response = client.put(
            f"/api/v1/notas/{nota.id_nota}",
            json={"contenido": "Intento de edición"},
            headers=headers_tutor
        )
        assert response.status_code == 403
    
    def test_tutor_puede_editar_su_propia_nota(self, client, db, headers_tutor, caso_test, usuario_tutor):
        """Tutor SÍ puede editar sus propias notas"""
        from app.models.nota import Nota
        from app.models.asignacion import Asignacion
        
        # Asignar caso al tutor
        asignacion = Asignacion(id_caso=caso_test.id_caso, id_usuario=usuario_tutor.id_usuario)
        db.add(asignacion)
        db.commit()
        
        # Tutor crea su propia nota
        nota = Nota(
            contenido="Mi nota",
            id_caso=caso_test.id_caso,
            id_usuario=usuario_tutor.id_usuario
        )
        db.add(nota)
        db.commit()
        db.refresh(nota)
        
        # Tutor edita su propia nota
        response = client.put(
            f"/api/v1/notas/{nota.id_nota}",
            json={"contenido": "Nota actualizada"},
            headers=headers_tutor
        )
        assert response.status_code == 200


class TestPermisosEmprendedores:
    """Tests de permisos en endpoints de emprendedores"""
    
    def test_admin_puede_crear_emprendedor(self, client, headers_admin):
        response = client.post(
            "/api/v1/emprendedores",
            json={
                "nombre": "María",
                "apellido": "García",
                "documento_identidad": "87654321",
                "email": "maria@test.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 201
    
    def test_coordinador_puede_crear_emprendedor(self, client, headers_coordinador):
        """Coordinador NO puede crear emprendedor (solo Admin)"""
        response = client.post(
            "/api/v1/emprendedores",
            json={
                "nombre": "Pedro",
                "apellido": "López",
                "documento_identidad": "11223344",
                "email": "pedro@test.com"
            },
            headers=headers_coordinador
        )
        assert response.status_code == 403
    
    def test_tutor_no_puede_crear_emprendedor(self, client, headers_tutor):
        response = client.post(
            "/api/v1/emprendedores",
            json={
                "nombre": "Ana",
                "apellido": "Martínez",
                "documento_identidad": "55667788",
                "email": "ana@test.com"
            },
            headers=headers_tutor
        )
        assert response.status_code == 403


class TestPermisosAuditoria:
    """Tests de permisos en endpoints de auditoría"""
    
    def test_admin_puede_ver_toda_auditoria(self, client, headers_admin):
        response = client.get("/api/v1/auditoria", headers=headers_admin)
        assert response.status_code == 200
    
    def test_coordinador_puede_ver_toda_auditoria(self, client, headers_coordinador):
        response = client.get("/api/v1/auditoria", headers=headers_coordinador)
        assert response.status_code == 200
    
    def test_tutor_no_puede_ver_toda_auditoria(self, client, headers_tutor):
        response = client.get("/api/v1/auditoria", headers=headers_tutor)
        assert response.status_code == 403
    
    def test_tutor_puede_ver_su_propia_auditoria(self, client, headers_tutor, usuario_tutor):
        """Tutor puede ver su propio historial"""
        response = client.get(
            f"/api/v1/auditoria/staff/{usuario_tutor.id_usuario}",
            headers=headers_tutor
        )
        assert response.status_code == 200
    
    def test_tutor_no_puede_ver_auditoria_ajena(self, client, headers_tutor, usuario_admin):
        """Tutor NO puede ver historial de otros"""
        response = client.get(
            f"/api/v1/auditoria/staff/{usuario_admin.id_usuario}",
            headers=headers_tutor
        )
        assert response.status_code == 403
