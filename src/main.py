# código nuevo edizon
"""main.py — Lanzador de la interfaz.

¿Para qué sirve?
    Arrancar la aplicación web del simulador (el panel del boceto).

¿Por qué existe?
    Es el único punto de entrada (`python -m src.main`). Toda la lógica vive en
    los módulos; aquí solo se lanza la interfaz.

¿Cómo ejecutarlo?
    python -m src.main    (desde la raíz del proyecto)

¿Cómo modificarlo?
    - Cambiar el puerto: pasar `port` a `app.run`.
    - Mostrar la página de errores de Dash: poner `debug=True`.
"""

from src.ui.app import app


def main():
    """Arranca la interfaz web."""
    app.run(debug=False)


if __name__ == "__main__":
    main()
