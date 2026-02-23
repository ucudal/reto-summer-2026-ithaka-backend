# Ithaka Backoffice API

API para gestión de postulaciones del Centro de Emprendimiento e Innovación - UCU

## 🚀 Levantar el servidor

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crear archivo `.env` con:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ithaka_db
SECRET_KEY=tu_secret_key_aqui
```

### 3. Iniciar servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

---

## 🗄️ Configurar Base de Datos

### Crear base de datos

```bash
psql -U postgres
CREATE DATABASE ithaka_db;
\q
```

### Importar estructura y datos

```bash
# Importar estructura de tablas
psql -U postgres -d ithaka_db -f ithaka_backoffice.sql

# Importar datos iniciales
psql -U postgres -d ithaka_db -f ithaka_inserts.sql
```

---

## 📤 Exportar datos (Dump)

### Exportar solo estructura

```bash
pg_dump -U postgres -d ithaka_db --schema-only > estructura.sql
```

### Exportar solo datos

```bash
pg_dump -U postgres -d ithaka_db --data-only > datos.sql
```

### Exportar todo (estructura + datos)

```bash
pg_dump -U postgres -d ithaka_db > backup_completo.sql
```

### Exportar tabla específica

```bash
pg_dump -U postgres -d ithaka_db -t nombre_tabla > tabla.sql
```

---

## 🐳 Usar con Docker (Opcional)

### Levantar servicios

```bash
docker-compose up -d
```

### Importar datos a Docker

```bash
Get-Content ithaka_backoffice.sql | docker exec -i ithaka_postgres psql -U postgres -d ithaka_db
```

### Ver logs

```bash
docker-compose logs -f
```

### Detener servicios

```bash
docker-compose down
```
