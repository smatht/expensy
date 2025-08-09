# Multi-stage build para optimizar el tamaño de la imagen
FROM python:3.11-slim as builder

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock ./

# instalar poetry y expotar dependencias a requirements.txt
RUN pip install poetry==1.8.5 && \
    poetry config virtualenvs.create false && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

# Stage de producción
FROM python:3.11-slim

# Instalar dependencias del sistema para producción
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements.txt desde el builder
COPY --from=builder /app/requirements.txt .

# instalar de pendencias de python
RUN pip install -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Instalar Gunicorn
RUN pip install gunicorn

# Crear directorio para archivos estáticos
RUN mkdir -p /app/static

# Configurar variables de entorno para Django
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=data.settings
ENV DEBUG=False
ENV STATIC_ROOT=/app/static

# Recolectar archivos estáticos
RUN cd data && python manage.py collectstatic --clear

# Cambiar permisos y propietario
RUN chown -R appuser:appuser /app
USER appuser

# Puerto para Cloud Run
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 data.wsgi:application 