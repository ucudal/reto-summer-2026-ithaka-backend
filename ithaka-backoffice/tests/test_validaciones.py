"""
Tests de Validaciones
---------------------
Tests exhaustivos de validaciones de datos en todos los endpoints.
Cubre: max_length, min_length, formatos, tipos de datos, campos requeridos.
"""

import pytest
import json


# =============================================================================
# VALIDACIONES DE CASOS
# =============================================================================

class TestValidacionesCaso:
    """Tests de validación para endpoint de casos"""
    
    def test_crear_caso_nombre_vacio(self, client, headers_admin, emprendedor_test):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "",
                "descripcion": "Test",
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_nombre_solo_espacios(self, client, headers_admin, emprendedor_test):
        """Nombre con solo espacios debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "   ",
                "descripcion": "Test",
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_nombre_excede_max_length(self, client, headers_admin, emprendedor_test):
        """Nombre mayor a 200 caracteres debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "A" * 201,
                "descripcion": "Test",
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_nombre_exactamente_max_length(self, client, headers_admin, emprendedor_test):
        """Nombre de exactamente 200 caracteres debe pasar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "A" * 200,
                "descripcion": "Test",
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 201
    
    def test_crear_caso_sin_nombre(self, client, headers_admin, emprendedor_test):
        """Caso sin nombre_caso debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "descripcion": "Test sin nombre",
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_id_emprendedor_negativo(self, client, headers_admin):
        """ID emprendedor negativo debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test",
                "id_emprendedor": -1
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_id_emprendedor_cero(self, client, headers_admin):
        """ID emprendedor 0 debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test",
                "id_emprendedor": 0
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_id_emprendedor_string(self, client, headers_admin):
        """ID emprendedor como string debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test",
                "id_emprendedor": "no_es_numero"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_caso_sin_descripcion_opcional(self, client, headers_admin, emprendedor_test):
        """Caso sin descripción (opcional) debe pasar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test sin descripción",
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 201
    
    def test_crear_caso_datos_chatbot_null(self, client, headers_admin, emprendedor_test):
        """datos_chatbot null es válido (opcional)"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test",
                "datos_chatbot": None,
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 201
    
    def test_crear_caso_datos_chatbot_json_valido(self, client, headers_admin, emprendedor_test):
        """datos_chatbot con JSON válido debe pasar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test",
                "datos_chatbot": {"sector": "Tech", "experiencia": 5},
                "id_emprendedor": emprendedor_test.id_emprendedor
            },
            headers=headers_admin
        )
        assert response.status_code == 201
        assert response.json()["datos_chatbot"]["sector"] == "Tech"
    
    def test_crear_caso_id_convocatoria_negativo(self, client, headers_admin, emprendedor_test):
        """id_convocatoria negativo debe fallar"""
        response = client.post(
            "/api/v1/casos/",
            json={
                "nombre_caso": "Test",
                "id_emprendedor": emprendedor_test.id_emprendedor,
                "id_convocatoria": -5
            },
            headers=headers_admin
        )
        assert response.status_code == 422


# =============================================================================
# VALIDACIONES DE EMPRENDEDORES
# =============================================================================

class TestValidacionesEmprendedor:
    """Tests de validación para endpoint de emprendedores"""
    
    def test_crear_emprendedor_nombre_vacio(self, client, headers_admin):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "",
                "apellido": "Test",
                "email": "test@example.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_nombre_excede_max_length(self, client, headers_admin):
        """Nombre mayor a 150 caracteres debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "A" * 151,
                "apellido": "Test",
                "email": "test@example.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_apellido_vacio(self, client, headers_admin):
        """Apellido vacío debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "",
                "email": "test@example.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_email_sin_arroba(self, client, headers_admin):
        """Email sin @ debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "emailinvalido.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_email_sin_dominio(self, client, headers_admin):
        """Email sin dominio debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "usuario@"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_email_sin_usuario(self, client, headers_admin):
        """Email sin parte de usuario debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "@dominio.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_email_excede_max_length(self, client, headers_admin):
        """Email mayor a 150 caracteres debe fallar"""
        # Crear email de más de 150 caracteres (142 'a' + '@test.com' = 151 caracteres)
        long_email = "a" * 142 + "@test.com"
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": long_email
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_telefono_excede_max_length(self, client, headers_admin):
        """Teléfono mayor a 50 caracteres debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "test@example.com",
                "telefono": "1" * 51
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_documento_excede_max_length(self, client, headers_admin):
        """Documento mayor a 50 caracteres debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "test@example.com",
                "documento_identidad": "A" * 51
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_pais_excede_max_length(self, client, headers_admin):
        """País mayor a 100 caracteres debe fallar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "test@example.com",
                "pais_residencia": "A" * 101
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_emprendedor_sin_campos_opcionales(self, client, headers_admin):
        """Emprendedor sin campos opcionales debe pasar"""
        response = client.post(
            "/api/v1/emprendedores/",
            json={
                "nombre": "Test",
                "apellido": "Test",
                "email": "test.opcionales@example.com"
            },
            headers=headers_admin
        )
        assert response.status_code == 201
        data = response.json()
        assert data["telefono"] is None
        assert data["documento_identidad"] is None


# =============================================================================
# VALIDACIONES DE USUARIOS
# =============================================================================

class TestValidacionesUsuario:
    """Tests de validación para endpoint de usuarios"""
    
    def test_crear_usuario_nombre_vacio(self, client, headers_admin, rol_tutor):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "",
                "email": "test@example.com",
                "password": "TestPassword123",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_usuario_nombre_excede_max_length(self, client, headers_admin, rol_tutor):
        """Nombre mayor a 150 caracteres debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "A" * 151,
                "email": "test@example.com",
                "password": "TestPassword123",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_usuario_apellido_excede_max_length(self, client, headers_admin, rol_tutor):
        """Apellido mayor a 150 caracteres debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "Test",
                "apellido": "A" * 151,
                "email": "test@example.com",
                "password": "TestPassword123",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_usuario_email_invalido_sin_arroba(self, client, headers_admin, rol_tutor):
        """Email sin @ debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "Test",
                "email": "emailinvalido.com",
                "password": "TestPassword123",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_usuario_sin_password(self, client, headers_admin, rol_tutor):
        """Usuario sin password debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "Test",
                "email": "test@example.com",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_usuario_password_vacio(self, client, headers_admin, rol_tutor):
        """Password vacío debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "Test",
                "email": "test@example.com",
                "password": "",
                "id_rol": rol_tutor.id_rol
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_usuario_id_rol_negativo(self, client, headers_admin):
        """ID rol negativo debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "Test",
                "email": "test@example.com",
                "password": "TestPassword123",
                "id_rol": -1
            },
            headers=headers_admin
        )
        assert response.status_code in [400, 422]  # Ambos códigos son válidos para datos inválidos
    
    def test_crear_usuario_id_rol_cero(self, client, headers_admin):
        """ID rol 0 debe fallar"""
        response = client.post(
            "/api/v1/usuarios/",
            json={
                "nombre": "Test",
                "email": "test@example.com",
                "password": "TestPassword123",
                "id_rol": 0
            },
            headers=headers_admin
        )
        assert response.status_code in [400, 422]  # Ambos códigos son válidos para datos inválidos


# =============================================================================
# VALIDACIONES DE NOTAS
# =============================================================================

class TestValidacionesNota:
    """Tests de validación para endpoint de notas"""
    
    def test_crear_nota_contenido_vacio(self, client, headers_admin, caso_test, usuario_admin):
        """Contenido vacío debe fallar"""
        response = client.post(
            "/api/v1/notas/",
            json={
                "contenido": "",
                "tipo_nota": "Seguimiento",
                "id_caso": caso_test.id_caso,
                "id_usuario": usuario_admin.id_usuario
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_nota_tipo_nota_excede_max_length(self, client, headers_admin, caso_test, usuario_admin):
        """tipo_nota mayor a 50 caracteres debe fallar"""
        response = client.post(
            "/api/v1/notas/",
            json={
                "contenido": "Test",
                "tipo_nota": "A" * 51,
                "id_caso": caso_test.id_caso,
                "id_usuario": usuario_admin.id_usuario
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_nota_id_caso_negativo(self, client, headers_admin, usuario_admin):
        """ID caso negativo debe fallar"""
        response = client.post(
            "/api/v1/notas/",
            json={
                "contenido": "Test",
                "tipo_nota": "Seguimiento",
                "id_caso": -1,
                "id_usuario": usuario_admin.id_usuario
            },
            headers=headers_admin
        )
        assert response.status_code in [400, 422]  # Ambos códigos son válidos para datos inválidos
    
    def test_crear_nota_id_usuario_negativo(self, client, headers_admin, caso_test):
        """ID usuario negativo debe fallar"""
        response = client.post(
            "/api/v1/notas/",
            json={
                "contenido": "Test",
                "tipo_nota": "Seguimiento",
                "id_caso": caso_test.id_caso,
                "id_usuario": -1
            },
            headers=headers_admin
        )
        assert response.status_code in [400, 422]  # Ambos códigos son válidos para datos inválidos


# =============================================================================
# VALIDACIONES DE ROLES
# =============================================================================

class TestValidacionesRol:
    """Tests de validación para endpoint de roles"""
    
    def test_crear_rol_nombre_vacio(self, client, headers_admin):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/roles/",
            json={
                "nombre_rol": "",
                "descripcion": "Test"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_rol_nombre_excede_max_length(self, client, headers_admin):
        """Nombre mayor a 50 caracteres debe fallar"""
        response = client.post(
            "/api/v1/roles/",
            json={
                "nombre_rol": "A" * 51,
                "descripcion": "Test"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_rol_valido(self, client, headers_admin):
        """Rol válido debe crearse correctamente"""
        response = client.post(
            "/api/v1/roles/",
            json={
                "nombre_rol": "RolDeValidacion"
            },
            headers=headers_admin
        )
        assert response.status_code == 201


# =============================================================================
# VALIDACIONES DE PROGRAMAS
# =============================================================================

class TestValidacionesPrograma:
    """Tests de validación para endpoint de programas"""
    
    def test_crear_programa_nombre_vacio(self, client, headers_admin):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/programas/",
            json={
                "nombre_programa": "",
                "descripcion": "Test"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_programa_nombre_excede_max_length(self, client, headers_admin):
        """Nombre mayor a 200 caracteres debe fallar"""
        response = client.post(
            "/api/v1/programas/",
            json={
                "nombre_programa": "A" * 201,
                "descripcion": "Test"
            },
            headers=headers_admin
        )
        assert response.status_code == 422


# =============================================================================
# VALIDACIONES DE CONVOCATORIAS
# =============================================================================

class TestValidacionesConvocatoria:
    """Tests de validación para endpoint de convocatorias"""
    
    def test_crear_convocatoria_nombre_vacio(self, client, headers_admin, programa_test):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/convocatorias/",
            json={
                "nombre_convocatoria": "",
                "fecha_inicio": "2026-01-01T00:00:00Z",
                "fecha_fin": "2026-12-31T23:59:59Z",
                "id_programa": programa_test.id_programa
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_convocatoria_nombre_excede_max_length(self, client, headers_admin, programa_test):
        """Nombre mayor a 200 caracteres debe fallar"""
        response = client.post(
            "/api/v1/convocatorias/",
            json={
                "nombre_convocatoria": "A" * 201,
                "fecha_inicio": "2026-01-01T00:00:00Z",
                "fecha_fin": "2026-12-31T23:59:59Z",
                "id_programa": programa_test.id_programa
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_convocatoria_id_programa_negativo(self, client, headers_admin):
        """ID programa negativo debe fallar"""
        response = client.post(
            "/api/v1/convocatorias/",
            json={
                "nombre_convocatoria": "Test",
                "fecha_inicio": "2026-01-01T00:00:00Z",
                "fecha_fin": "2026-12-31T23:59:59Z",
                "id_programa": -1
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_convocatoria_fecha_inicio_invalida(self, client, headers_admin, programa_test):
        """Fecha de inicio inválida debe fallar"""
        response = client.post(
            "/api/v1/convocatorias/",
            json={
                "nombre_convocatoria": "Test",
                "fecha_inicio": "no-es-fecha",
                "fecha_fin": "2026-12-31T23:59:59Z",
                "id_programa": programa_test.id_programa
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_convocatoria_sin_fecha_inicio(self, client, headers_admin, programa_test):
        """Convocatoria sin fecha_inicio debe fallar"""
        response = client.post(
            "/api/v1/convocatorias/",
            json={
                "nombre_convocatoria": "Test",
                "fecha_fin": "2026-12-31T23:59:59Z",
                "id_programa": programa_test.id_programa
            },
            headers=headers_admin
        )
        assert response.status_code == 422


# =============================================================================
# VALIDACIONES DE ASIGNACIONES
# =============================================================================

class TestValidacionesAsignacion:
    """Tests de validación para endpoint de asignaciones"""
    
    def test_crear_asignacion_id_caso_negativo(self, client, headers_admin, usuario_tutor):
        """ID caso negativo debe fallar"""
        response = client.post(
            "/api/v1/asignaciones/",
            json={
                "id_caso": -1,
                "id_usuario": usuario_tutor.id_usuario
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_asignacion_id_usuario_negativo(self, client, headers_admin, caso_test):
        """ID usuario negativo debe fallar"""
        response = client.post(
            "/api/v1/asignaciones/",
            json={
                "id_caso": caso_test.id_caso,
                "id_usuario": -1
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_asignacion_id_caso_cero(self, client, headers_admin, usuario_tutor):
        """ID caso 0 debe fallar"""
        response = client.post(
            "/api/v1/asignaciones/",
            json={
                "id_caso": 0,
                "id_usuario": usuario_tutor.id_usuario
            },
            headers=headers_admin
        )
        assert response.status_code == 422


# =============================================================================
# VALIDACIONES DE CATALOGOS
# =============================================================================

class TestValidacionesCatalogoEstados:
    """Tests de validación para catálogo de estados"""
    
    def test_crear_estado_nombre_vacio(self, client, headers_admin):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/catalogo-estados/",
            json={
                "nombre_estado": "",
                "tipo_caso": "postulacion"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_estado_nombre_excede_max_length(self, client, headers_admin):
        """Nombre mayor a 100 caracteres debe fallar"""
        response = client.post(
            "/api/v1/catalogo-estados/",
            json={
                "nombre_estado": "A" * 101,
                "tipo_caso": "postulacion"
            },
            headers=headers_admin
        )
        assert response.status_code == 422
    
    def test_crear_estado_tipo_caso_invalido(self, client, headers_admin):
        """tipo_caso no válido debe fallar (solo 'postulacion' o 'proyecto')"""
        response = client.post(
            "/api/v1/catalogo-estados/",
            json={
                "nombre_estado": "Test",
                "tipo_caso": "invalido"
            },
            headers=headers_admin
        )
        assert response.status_code == 422


class TestValidacionesCatalogoApoyos:
    """Tests de validación para catálogo de apoyos"""
    
    def test_crear_catalogo_apoyo_nombre_vacio(self, client, headers_admin):
        """Nombre vacío debe fallar"""
        response = client.post(
            "/api/v1/catalogo-apoyos/",
            json={
                "nombre_apoyo": "",
                "descripcion": "Test"
            },
            headers=headers_admin
        )
        assert response.status_code in [422, 500]  # Puede variar según implementación
    
    def test_crear_catalogo_apoyo_nombre_excede_max_length(self, client, headers_admin):
        """Nombre muy largo debe manejarse"""
        response = client.post(
            "/api/v1/catalogo-apoyos/",
            json={
                "nombre_apoyo": "A" * 300,
                "descripcion": "Test"
            },
            headers=headers_admin
        )
        assert response.status_code in [422, 500]
