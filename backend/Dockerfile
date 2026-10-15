FROM python:3.11-slim

# Evita archivos .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para compilar librerías de ChromaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python primero (aprovecha caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios de persistencia local para documentos y ChromaDB
RUN mkdir -p /app/data/docs /app/data/chroma_db

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]