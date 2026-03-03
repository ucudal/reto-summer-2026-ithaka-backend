from app.schemas.emprendedor import EmprendedorCreate

# Test con email largo (151 caracteres)
long_email = "a" * 142 + "@test.com"  # 142 + 9 = 151 caracteres
print(f"Email length: {len(long_email)}")
print(f"Email: {long_email}")

try:
    emprendedor = EmprendedorCreate(
        nombre="Test",
        apellido="Test",
        email=long_email
    )
    print("✗ FALLO: Email largo fue aceptado")
    print(f"Email creado: {emprendedor.email}")
except ValueError as e:
    print(f"✓ CORRECTO: Email largo rechazado con error: {e}")

# Test con email válido
short_email = "test@example.com"
print(f"\nEmail length: {len(short_email)}")
try:
    emprendedor = EmprendedorCreate(
        nombre="Test",
        apellido="Test",
        email=short_email
    )
    print(f"✓ CORRECTO: Email válido aceptado: {emprendedor.email}")
except ValueError as e:
    print(f"✗ FALLO: Email válido rechazado con error: {e}")
