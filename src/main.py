# código nuevo edizon
"""main.py — Lanzador de la interfaz.

¿Para qué sirve?
    Arrancar la aplicación web del simulador (el panel del boceto).

¿Por qué existe?
    Es el único punto de entrada (`python -m src.main`). Toda la lógica vive en
    los módulos; aquí solo se lanza la interfaz.

¿Cómo funciona con un servicio en la nube?
    Las plataformas gratuitas entregan el puerto en la variable `PORT` y esperan
    que la aplicación escuche en `0.0.0.0`. En local, sin `PORT`, se mantiene
    `127.0.0.1:8050` para no exponer el panel a la red.

¿Cómo ejecutarlo?
    python -m src.main          (local: http://127.0.0.1:8050)
    PORT=8080 python -m src.main (servicio: http://0.0.0.0:8080)

¿Cómo modificarlo?
    - Cambiar el puerto local: variable `PORT`.
    - Mostrar la página de errores de Dash: poner `debug=True`.
"""

import os

from src.ui.app import app


def main():
    """Arranca la interfaz web en el puerto que indique el entorno."""
    port = int(os.environ.get("PORT", "8050"))
    # En producción (PORT definido) se acepta tráfico de la plataforma; en local
    # solo se escucha en la propia máquina.
    host = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")

    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
