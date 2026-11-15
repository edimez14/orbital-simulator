# código nuevo edizon
"""scene3d.py — Dibuja el sistema en 3D.

¿Para qué sirve?
    Mostrar la escena tridimensional: las posiciones de los cuerpos, sus
    trayectorias, los ejes de referencia y un fondo estelar, usando VPython.

¿Por qué existe?
    Es la parte visible del proyecto, pero NO la más importante. Dibuja el estado
    que ya calculó la física; no calcula nada por su cuenta.

¿Qué contendrá?
    - `create_scene(bodies)`     : crea esferas, trayectorias, ejes y fondo.
    - `update(objects, bodies)`  : mueve las esferas y alarga las trayectorias.

Escala visual (importante)
    `SCALE` convierte AU a unidades de pantalla, así que las DISTANCIAS sí
    respetan la escala. El TAMAÑO de las esferas es decorativo: NO es el tamaño
    físico (si fuera real, los planetas serían invisibles).

REGLA DE ORO (PDF sección 4.1 y 4.3)
    Este archivo SOLO LEE el estado. Nunca lo modifica y nunca calcula física.

¿Cómo modificarlo?
    - Cambiar el estilo (tamaño, color, fondo): solo en las constantes de arriba.
    - Cambiar de librería 3D: reescribir solo este archivo.
"""

from pathlib import Path

import numpy as np
from vpython import arrow, color, curve, points, scene, sphere, vector

ASSETS = Path(__file__).resolve().parents[2] / "assets" / "textures"

# Así pide el navegador las texturas: ruta relativa a la raíz del proyecto.
# VPython sirve los archivos desde la carpeta donde se ejecuta el programa, así
# que hay que correrlo desde la raíz del proyecto (ver docstring).
TEXTURE_PREFIX = "assets/textures"

# Unidades de pantalla por AU. Las distancias se multiplican por este valor.
SCALE = 100.0

# Tamaño en pantalla de cada cuerpo (decorativo, NO es el tamaño físico).
RADII = {"Sol": 10.0}
DEFAULT_RADIUS = 3.0

# Color de cada cuerpo, que se usa si no hay textura.
COLORS = {
    "Sol": color.yellow,
    "Mercurio": color.gray(0.6),
    "Venus": color.orange,
    "Tierra": color.blue,
    "Marte": color.red,
}
DEFAULT_COLOR = color.white

# Archivo de textura de cada cuerpo (si no existe, queda el color).
TEXTURES = {
    "Sol": "stars/sol.jpg",
    "Mercurio": "planets/mercurio.jpg",
    "Venus": "planets/venus.jpg",
    "Tierra": "planets/tierra.jpg",
    "Marte": "planets/marte.jpg",
}


def create_scene(bodies):
    """Crea la escena 3D con esferas, trayectorias, ejes y fondo estelar.

    Recibe:
        bodies : lista de cuerpos a dibujar.
    Devuelve:
        Un diccionario: nombre del cuerpo -> {"sphere": esfera, "trail": curva}.
    """
    scene.title = "Simulador orbital — Leyes de Kepler"
    scene.background = color.black

    _draw_stars()
    _draw_axes()

    objects = {}
    for body in bodies:
        objects[body.name] = {
            "sphere": _create_sphere(body),
            "trail": curve(color=COLORS.get(body.name, DEFAULT_COLOR)),
        }

    # Esperar a que carguen las texturas antes de animar (paso 6 de la Fase 9).
    scene.waitfor("textures")
    return objects


def update(objects, bodies):
    """Mueve las esferas a la posición actual y alarga las trayectorias.

    Recibe:
        objects : lo que devolvió `create_scene`.
        bodies  : lista de cuerpos, en el mismo orden que en `create_scene`.
    """
    for body in bodies:
        screen_position = body.position * SCALE
        point = vector(
            float(screen_position[0]),
            float(screen_position[1]),
            float(screen_position[2]),
        )
        objects[body.name]["sphere"].pos = point
        objects[body.name]["trail"].append(point)


def _create_sphere(body):
    """Crea la esfera de un cuerpo con su tamaño, color y textura.

    Recibe:
        body : un cuerpo (usa su nombre y su posición inicial).
    Devuelve:
        La esfera de VPython.
    """
    texture_file = TEXTURES.get(body.name)
    texture = None
    if texture_file and (ASSETS / texture_file).exists():
        texture = f"{TEXTURE_PREFIX}/{texture_file}"

    return sphere(
        pos=vector(
            float(body.position[0]) * SCALE,
            float(body.position[1]) * SCALE,
            float(body.position[2]) * SCALE,
        ),
        radius=RADII.get(body.name, DEFAULT_RADIUS),
        color=COLORS.get(body.name, DEFAULT_COLOR),
        texture=texture,
        emissive=(body.name == "Sol"),
    )


def _draw_axes(length=200.0):
    """Dibuja los tres ejes de referencia: x rojo, y verde, z azul.

    Recibe:
        length : largo de cada eje, en unidades de pantalla.
    """
    arrow(axis=vector(length, 0, 0), color=color.red)
    arrow(axis=vector(0, length, 0), color=color.green)
    arrow(axis=vector(0, 0, length), color=color.blue)


def _draw_stars(number=200, distance=800.0):
    """Dibuja el fondo estelar como puntos repartidos en una esfera lejana.

    Recibe:
        number   : cuántas estrellas dibujar.
        distance : distancia de las estrellas al centro, en unidades de pantalla.
    """
    positions = np.random.uniform(-1.0, 1.0, (number, 3))
    positions = positions / np.linalg.norm(positions, axis=1, keepdims=True) * distance

    points(pos=[vector(float(x), float(y), float(z)) for x, y, z in positions], color=color.white)
