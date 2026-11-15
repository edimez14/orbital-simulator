# código nuevo edizon
# Imagen de la interfaz web para plataformas gratuitas con Docker.
# Escucha en el puerto que entregue la plataforma (PORT) o en 7860, que es el
# que usa Hugging Face Spaces por defecto.

FROM python:3.12-slim

# Salida sin búfer para que los registros lleguen a la plataforma.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

# Primero las dependencias: si el código cambia, esta capa se reutiliza.
COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Solo lo que la aplicación necesita en ejecución.
COPY src ./src
COPY assets ./assets
COPY data ./data

EXPOSE 7860

# Un solo proceso con varios hilos: el cálculo usa CPU y el estado de cada
# usuario vive en su navegador (dcc.Store), no en el servidor.
CMD ["sh", "-c", "gunicorn src.wsgi:server --bind 0.0.0.0:${PORT:-7860} --workers 1 --threads 4 --timeout 120 --access-logfile -"]
