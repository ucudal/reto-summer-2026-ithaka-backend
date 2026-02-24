# ==============================================================================
# Dockerfile - Ithaka Backoffice API
# Optimizado para Kubernetes
# ==============================================================================

# --- Stage 1: Builder ---
    FROM python:3.11-slim AS builder

    WORKDIR /build
    
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    # --- Stage 2: Runtime ---
    FROM python:3.11-slim
    
    # Metadata
    LABEL maintainer="UCU Centro de Emprendimiento"
    LABEL description="Ithaka Backoffice API"
    LABEL version="1.0.0"
    
    # Crear usuario no-root (seguridad)
    RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser
    
    WORKDIR /app
    
    # Copiar dependencias del builder
    COPY --from=builder /install /usr/local
    
    # Copiar código fuente
    COPY . .
    
    # Cambiar a usuario no-root
    USER appuser
    
    # Puerto de la API
    EXPOSE 8000
    
    # Health check (usado por K8s como fallback)
    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
      CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
    
    # Comando de inicio
    # --workers: ajustar según los CPU limits del pod
    # --host 0.0.0.0: necesario para que K8s pueda hacer probes
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
    