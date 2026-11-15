# código nuevo edizon
"""wsgi.py — Punto de entrada para servidores de producción.

¿Para qué sirve?
    Entregar el servidor Flask que hay dentro de la aplicación Dash a Gunicorn
    (o a cualquier servidor WSGI). Es lo que usan las plataformas en la nube.

¿Por qué existe?
    `python -m src.main` arranca el servidor de desarrollo de Flask, que no está
    pensado para recibir visitas. Gunicorn necesita una variable llamada
    `server` y este archivo la expone.

¿Cómo se usa?
    gunicorn src.wsgi:server --bind 0.0.0.0:$PORT --workers 1 --threads 4

¿Cómo modificarlo?
    Si el objeto de la aplicación cambia de nombre, ajustar solo la última línea.
"""

from src.ui.app import app

# Gunicorn busca este nombre exacto.
server = app.server
