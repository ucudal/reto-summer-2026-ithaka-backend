# Ithaka Backoffice API

API para gestión de postulaciones del Centro de Emprendimiento e Innovación - UCU

## 🚀 Levantar el servidor

### 1. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ithaka_db
SECRET_KEY=tu_secret_key_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Iniciar servicios

```bash
docker-compose up -d
```

El servidor estará disponible en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

## 🗄️ Importar base de datos

```bash
Get-Content ithaka_backoffice.sql | docker exec -i ithaka_postgres psql -U postgres -d ithaka_db
Get-Content ithaka_inserts.sql | docker exec -i ithaka_postgres psql -U postgres -d ithaka_db
```

## 📤 Exportar base de datos (Dump)

```bash
docker exec ithaka_postgres pg_dump -U postgres ithaka_db > backup.sql
```

## 🔧 Comandos útiles

```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down
```
