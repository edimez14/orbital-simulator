# código nuevo edizon
"""config.py — Rutas y parámetros generales del proyecto.

¿Para qué sirve?
    Dar la carpeta base del proyecto tanto si el programa corre suelto (desde el
    repositorio) como si corre empaquetado con PyInstaller.

¿Por qué existe?
    Empaquetado, los archivos no quedan en la misma ruta que en el repositorio.
    Sin esto, el ejecutable no encontraría `assets/` ni `data/`.

¿Qué contendrá?
    - `project_root()` : la carpeta base del proyecto.

¿Cómo modificarlo?
    - Añadir aquí las rutas nuevas (por ejemplo una carpeta de resultados).
"""

import sys
from pathlib import Path


def project_root():
    """Carpeta base del proyecto.

    Empaquetado con PyInstaller los archivos van a la carpeta temporal
    `sys._MEIPASS`; suelto, es la carpeta del repositorio.

    Devuelve:
        La ruta base, como `Path`.
    """
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent.parent
