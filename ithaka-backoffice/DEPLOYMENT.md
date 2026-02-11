# Guía de Deployment - Ithaka Backoffice API

## 🚀 Subir el proyecto a GitHub

### 1. Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre sugerido: `ithaka-backoffice-api`
3. Descripción: "API para gestión de postulaciones - Centro de Emprendimiento UCU"
4. Visibilidad: Privado (recomendado) o Público
5. NO inicialices con README, .gitignore ni licencia (ya los tienes)

### 2. Subir el código

```bash
# Desde la carpeta del proyecto
cd ithaka-backoffice

# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: FastAPI minimal setup for Ithaka backoffice"

# Conectar con GitHub (reemplaza TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/ithaka-backoffice-api.git

# Subir el código
git branch -M main
git push -u origin main
```

### 3. Verificar GitHub Actions

Una vez subido el código, GitHub Actions ejecutará automáticamente:
- Instalación de dependencias
- Pruebas de health check
- Build de la imagen Docker
- Pruebas del contenedor

Puedes ver el estado en la pestaña "Actions" de tu repositorio.

## 🐳 Deployment con Docker

### Opción 1: Docker local

```bash
# Build
docker build -t ithaka-backoffice .

# Run
docker run -d -p 8000:8000 --name ithaka-api ithaka-backoffice

# Ver logs
docker logs -f ithaka-api

# Detener
docker stop ithaka-api
docker rm ithaka-api
```

### Opción 2: Docker Compose

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## ☁️ Deployment a Cloud

### Render.com (Gratuito)

1. Ve a https://render.com
2. Conecta tu repositorio de GitHub
3. Crea un nuevo "Web Service"
4. Configuración:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.11

### Railway.app (Gratuito)

1. Ve a https://railway.app
2. Conecta tu repositorio de GitHub
3. Railway detectará automáticamente el Dockerfile
4. Deployment automático

### Google Cloud Run

```bash
# Autenticar
gcloud auth login

# Build y push
gcloud builds submit --tag gcr.io/TU-PROYECTO/ithaka-backoffice

# Deploy
gcloud run deploy ithaka-backoffice \
  --image gcr.io/TU-PROYECTO/ithaka-backoffice \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### AWS App Runner

1. Ve a AWS App Runner en la consola
2. Crea un nuevo servicio desde código fuente
3. Conecta tu repositorio de GitHub
4. Configuración:
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8080`

## 🔧 Variables de Entorno para Producción

Crea un archivo `.env` (NO lo subas a Git, ya está en .gitignore):

```env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@host:5432/ithaka
SECRET_KEY=tu-clave-secreta-super-segura
CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

## 📊 Monitoreo

### Health Check Endpoint

```bash
# Verificar que la API está funcionando
curl https://tu-api.com/health
```

### Logs

```bash
# Docker
docker logs -f ithaka-api

# Docker Compose
docker-compose logs -f
```

## 🔒 Seguridad para Producción

Antes de ir a producción, considera:

1. **Variables de entorno**: Usar servicios como AWS Secrets Manager o variables de entorno del host
2. **HTTPS**: Asegurar que todo el tráfico sea HTTPS
3. **CORS**: Configurar orígenes específicos en lugar de `"*"`
4. **Rate Limiting**: Implementar límites de requests
5. **Autenticación**: Agregar JWT o OAuth2
6. **Base de datos**: Migrar de memoria a PostgreSQL/MongoDB
7. **Logging**: Implementar logging estructurado
8. **Backup**: Configurar backups automáticos de la BD

## 📝 Checklist de DevOps

- [ ] Código subido a GitHub
- [ ] GitHub Actions funcionando (badge verde)
- [ ] Dockerfile testeado localmente
- [ ] Variables de entorno configuradas
- [ ] Deployment en ambiente de staging
- [ ] Health checks configurados
- [ ] Monitoreo básico activo
- [ ] Backups configurados
- [ ] Documentación actualizada

## 🆘 Troubleshooting

### La API no inicia

```bash
# Verificar logs
docker logs ithaka-api

# Verificar puerto
lsof -i :8000
```

### Error de conexión a base de datos

```bash
# Verificar variable de entorno
echo $DATABASE_URL

# Probar conexión
psql $DATABASE_URL
```

### GitHub Actions falla

1. Revisa los logs en la pestaña Actions
2. Verifica que requirements.txt esté actualizado
3. Asegúrate de que el código funcione localmente primero

## 📞 Soporte

Para más información sobre el proyecto Ithaka, consulta el documento de definición del reto.
