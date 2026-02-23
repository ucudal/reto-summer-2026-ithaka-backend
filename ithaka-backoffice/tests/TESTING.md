# Guía de Testing - Ithaka Backend

Guía rápida para ejecutar todos los tests automatizados del sistema.

## Instalación

Activar las dependencias de testing en `requirements.txt`:

```bash
# Descomentar estas líneas en requirements.txt:
pytest>=7.4.0
httpx>=0.24.0
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Tests con output detallado
```bash
pytest -v
```

### Tests con output de prints
```bash
pytest -s
```

### Tests de un archivo específico
```bash
pytest tests/test_auth.py
pytest tests/test_permisos.py
pytest tests/test_auditoria.py
pytest tests/test_flujos_completos.py
```

### Tests de una clase específica
```bash
pytest tests/test_permisos.py::TestPermisosUsuarios
pytest tests/test_permisos.py::TestPermisosCasos
```

### Test individual
```bash
pytest tests/test_auth.py::test_login_exitoso_admin
pytest tests/test_permisos.py::TestPermisosNotas::test_tutor_solo_puede_editar_sus_propias_notas
```

### Tests con cobertura
```bash
# Instalar coverage
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest --cov=app --cov-report=html

# Ver reporte (se genera en htmlcov/index.html)
```

### Tests en paralelo (más rápido)
```bash
# Instalar xdist
pip install pytest-xdist

# Ejecutar en paralelo
pytest -n auto
```

## Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas (DB, usuarios, tokens)
├── test_auth.py             # Tests de autenticación y JWT
├── test_permisos.py         # Tests de RBAC por rol
├── test_auditoria.py        # Tests de auditoría
└── test_flujos_completos.py # Tests end-to-end
```

## Fixtures Disponibles

Las siguientes fixtures están configuradas en `conftest.py`:

- `db`: Sesión de base de datos SQLite in-memory
- `client`: FastAPI TestClient
- `rol_admin`, `rol_coordinador`, `rol_tutor`: Roles del sistema
- `usuario_admin`, `usuario_coordinador`, `usuario_tutor`: Usuarios de prueba
- `admin_token`, `coordinador_token`, `tutor_token`: Tokens JWT
- `headers_admin`, `headers_coordinador`, `headers_tutor`: Headers con Bearer tokens
- `emprendedor_test`: Emprendedor de prueba
- `caso_test`: Caso de prueba

## Comandos Útiles

### Ver motivo de fallos
```bash
pytest --tb=short  # Traceback corto
pytest --tb=line   # Una línea por fallo
pytest --tb=no     # Sin traceback (solo resumen)
```

### Ejecutar solo tests que fallaron
```bash
pytest --lf
```

### Detener al primer fallo
```bash
pytest -x
```

### Ver duración de tests
```bash
pytest --durations=10  # Top 10 tests más lentos
```

### Modo verbose + sin captura de output
```bash
pytest -v -s
```

## Categorías de Tests

### 1. **test_auth.py** - Autenticación
- ✅ Login con credenciales válidas (Admin, Coordinador, Tutor)
- ✅ Login con credenciales inválidas
- ✅ Login con usuario inactivo
- ✅ Acceso sin token (401)
- ✅ Acceso con token inválido
- ✅ Endpoint `/me` retorna usuario actual
- ✅ Token no expone `password_hash`

### 2. **test_permisos.py** - RBAC
#### Permisos de Usuarios
- ✅ Admin/Coordinador pueden listar usuarios
- ✅ Tutor NO puede listar usuarios
- ✅ Admin puede crear usuarios
- ✅ Coordinador NO puede crear usuarios
- ✅ Tutor puede ver su perfil, no ajenos

#### Permisos de Roles
- ✅ Solo Admin puede gestionar roles

#### Permisos de Casos
- ✅ Admin/Coordinador pueden listar todos los casos
- ✅ Tutor solo ve casos asignados
- ✅ Solo Admin puede crear casos
- ✅ Coordinador/Tutor no pueden crear casos

#### Permisos de Notas
- ✅ Tutor solo puede editar/eliminar sus propias notas
- ✅ No puede editar notas de otros usuarios

#### Permisos de Emprendedores
- ✅ Admin/Coordinador pueden crear emprendedores
- ✅ Tutor no puede crear emprendedores

#### Permisos de Auditoría
- ✅ Admin/Coordinador ven toda la auditoría
- ✅ Tutor solo ve su propio historial
- ✅ Tutor no puede ver historial ajeno

### 3. **test_auditoria.py** - Auditoría
- ✅ Se crea auditoría al crear caso
- ✅ Se registra actualización de caso
- ✅ Se registra eliminación/desactivación de usuario
- ✅ Se registra creación de usuario
- ✅ Admin/Coordinador ven toda la auditoría
- ✅ Tutor solo ve su auditoría
- ✅ Auditoría contiene valores cambiados
- ✅ Auditoría registra usuario actual (`current_user`)

### 4. **test_flujos_completos.py** - E2E
- ✅ Flujo completo: Crear emprendedor → Crear caso → Asignar → Agregar nota
- ✅ Tutor solo ve casos asignados (filtrado correcto)
- ✅ Cambio de estado con auditoría
- ✅ Gestión completa de notas (CRUD)
- ✅ Asignación múltiple (varios tutores en un caso)
- ✅ Desactivar y reactivar usuario

## CI/CD

Para integrar en GitHub Actions:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -v --cov=app
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pytest'"
```bash
pip install pytest httpx
```

### Error: Base de datos bloqueada
Los tests usan SQLite in-memory, no deberían tener este problema. Si ocurre, verificar que no haya sesiones abiertas sin cerrar.

### Tests fallan por dependencias circulares
Verificar imports en `conftest.py` y que `__init__.py` esté presente en `tests/`.

### Token expirado en tests
Los tokens generados en fixtures son válidos por 30 minutos. Si un test tarda más, regenerar token.

## Mejores Prácticas

1. **Ejecutar tests antes de cada commit**
   ```bash
   pytest -v
   ```

2. **Tests deben ser independientes**: Cada test debe poder ejecutarse solo
   ```bash
   pytest tests/test_auth.py::test_login_exitoso_admin
   ```

3. **Usar fixtures**: No duplicar código de setup

4. **Tests descriptivos**: Nombres claros sobre qué se prueba

5. **Verificar cobertura**: Apuntar a >80% de cobertura
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

## Contacto

Para reportar problemas con los tests, crear Issue en el repositorio.
