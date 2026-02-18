# Importar Base de Datos a Docker

Esta guía explica cómo importar tu base de datos existente al contenedor de PostgreSQL en Docker.

## Prerrequisitos

- Docker Desktop instalado y corriendo
- Archivo de dump SQL (ej: `ithaka_backoffice.sql`)

## Pasosbackoffice

### 1. Levantar solo la base de datos

Primero levanta únicamente el contenedor de PostgreSQL:

```powershell
docker-compose up -d db
```

Espera unos segundos a que la base de datos esté lista. Puedes verificar con:

```powershell
docker-compose logs db
```

### 2. Importar el dump SQL

Ejecuta este comando desde la carpeta `ithaka-`:

```powershell
Get-Content ithaka_backoffice.sql | docker exec -i ithaka_postgres psql -U postgres -d ithaka_db
```

**Nota**: Asegúrate de que el archivo `ithaka_backoffice.sql` esté en la misma carpeta.

### 3. Verificar la importación

Conéctate a la base de datos para verificar que las tablas se importaron:

```powershell
docker exec -it ithaka_postgres psql -U postgres -d ithaka_db
```

Dentro de psql, ejecuta:

```sql
\dt
```

Esto mostrará todas las tablas importadas. Para salir de psql escribe `\q`

### 4. Levantar la API

Una vez importados los datos, levanta toda la aplicación:

```powershell
docker-compose up
```

## Conectar con pgAdmin

Puedes seguir usando pgAdmin para administrar la base de datos en Docker:

**Configuración de conexión:**
- Host: `localhost`
- Puerto: `5432` (el que está en tu `.env`)
- Usuario: `postgres` (el que está en tu `.env`)
- Password: La contraseña de tu `.env`
- Base de datos: `ithaka_db`

## Comandos útiles

```powershell
# Ver logs de la base de datos
docker-compose logs db

# Detener todos los contenedores
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra los datos)
docker-compose down -v

# Reiniciar solo la base de datos
docker-compose restart db
```

## Notas importantes

- Los datos se guardan en un volumen de Docker llamado `postgres_data`
- Si haces `docker-compose down` los datos persisten
- Solo se borran con `docker-compose down -v`
- Tu base de datos local de pgAdmin NO se ve afectada
