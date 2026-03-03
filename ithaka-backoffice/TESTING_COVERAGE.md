# Testing y Coverage - Ithaka Backoffice

## 📊 Coverage de Tests con pytest-cov

Este proyecto usa **pytest** para testing y **pytest-cov** para medir la cobertura de código.

---

## 🚀 Comandos Principales

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con reporte de coverage
```bash
pytest --cov=app
```

### Coverage con reporte detallado
```bash
pytest --cov=app --cov-report=term-missing
```

### Generar reporte HTML
```bash
pytest --cov=app --cov-report=html
```

Luego abre el reporte en: `htmlcov/index.html`

### Coverage con líneas específicas faltantes
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

---

## 📁 Estructura de Tests

```
tests/
├── conftest.py                    # Fixtures compartidos
├── test_auth.py                   # Autenticación y JWT
├── test_usuarios.py               # CRUD de usuarios
├── test_casos.py                  # CRUD de casos + PATCH estado
├── test_emprendedores.py          # CRUD de emprendedores  
├── test_convocatorias.py          # CRUD de convocatorias
├── test_programas.py              # CRUD de programas
├── test_roles.py                  # CRUD de roles
├── test_catalogo_estados.py       # CRUD de catálogo estados
├── test_asignaciones.py           # Asignación de tutores
├── test_notas.py                  # Notas de casos
├── test_auditoria.py              # Sistema de auditoría
├── test_permisos.py               # Validación de permisos
├── test_export_casos.py           # Exportación CSV
└── test_flujos_completos.py       # Tests de integración
```

---

## 🎯 Objetivos de Coverage

| Categoría | Coverage Objetivo |
|-----------|------------------|
| **Endpoints** | > 90% |
| **Models** | > 80% |
| **Services** | > 85% |
| **Total** | > 85% |

---

## 📝 Ejemplos de Uso

### 1. Ejecutar tests de un archivo específico
```bash
pytest tests/test_casos.py
```

### 2. Ejecutar un test específico
```bash
pytest tests/test_casos.py::test_cambiar_estado_caso_admin
```

### 3. Ver tests lentos
```bash
pytest --durations=10
```

### 4. Ejecutar solo tests marcados
```bash
# Tests de integración
pytest -m integration

# Tests rápidos (unitarios)
pytest -m unit
```

### 5. Coverage de un módulo específico
```bash
pytest --cov=app.api.v1.endpoints.caso tests/test_casos.py
```

---

## 🔍 Interpretando el Reporte

### Reporte en Terminal
```
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
app/api/v1/endpoints/caso.py              150     10    93%   45-47, 120
app/api/v1/endpoints/usuario.py           120      5    96%   88-90
app/services/auditoria_service.py          50      2    96%   35, 42
---------------------------------------------------------------------
TOTAL                                    2500    150    94%
```

- **Stmts**: Líneas de código
- **Miss**: Líneas no cubiertas
- **Cover**: Porcentaje de cobertura
- **Missing**: Números de línea sin cubrir

### Reporte HTML
El reporte HTML muestra:
- ✅ Líneas ejecutadas en **verde**
- ❌ Líneas sin ejecutar en **rojo** 
- ⚠️ Líneas parcialmente cubiertas en **amarillo**

---

## ⚙️ Configuración

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short
```

### .coveragerc
```ini
[run]
source = app
omit = 
    */tests/*
    */__init__.py
    */main.py

[report]
precision = 2
show_missing = True
```

---

## 🧪 Escribir Tests

### Estructura de un Test
```python
def test_crear_caso_valido(client, headers_admin, emprendedor_test):
    """Descripción del test"""
    # Arrange (preparar datos)
    nuevo_caso = {
        "nombre_caso": "Test",
        "id_emprendedor": emprendedor_test.id_emprendedor
    }
    
    # Act (ejecutar acción)
    response = client.post("/api/v1/casos", json=nuevo_caso, headers=headers_admin)
    
    # Assert (verificar resultado)
    assert response.status_code == 201
    assert response.json()["nombre_caso"] == "Test"
```

### Fixtures Disponibles
- `client`: Cliente HTTP de prueba
- `db`: Sesión de base de datos de prueba
- `headers_admin/coordinador/tutor`: Headers con tokens JWT
- `usuario_admin/coordinador/tutor`: Usuarios de prueba
- `emprendedor_test`: Emprendedor de prueba
- `caso_test`: Caso de prueba
- `rol_admin/coordinador/tutor`: Roles de prueba

---

## 🎨 Buenas Prácticas

### ✅ DO
- Prueba casos exitosos Y casos de error
- Prueba permisos (Admin, Coordinador, Tutor)
- Prueba validaciones de datos
- Usa nombres descriptivos (`test_crear_caso_valido`)
- Agrupa tests con comentarios
- Verifica respuestas completas (status + body)

### ❌ DON'T
- No uses datos reales de producción
- No dependas del orden de ejecución
- No hagas tests que modifiquen estado global
- No ignores casos excepcionales

---

## 📈 CI/CD

### GitHub Actions (ejemplo)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 🐛 Debugging Tests

### Ver output completo
```bash
pytest -v -s
```

### Ver solo el primer fallo
```bash
pytest -x
```

### Modo debugging
```bash
pytest --pdb
```

---

## 📚 Recursos

- [Pytest Docs](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 🎯 Checklist para PRs

Antes de hacer merge:
- [ ] Todos los tests pasan
- [ ] Coverage > 85%
- [ ] Tests nuevos para código nuevo
- [ ] Tests de permisos incluidos
- [ ] Tests de casos de error
- [ ] Sin warnings de pytest

---

**Última actualización**: Marzo 2026  
**Maintained by**: Equipo Ithaka
