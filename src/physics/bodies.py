# código nuevo edizon
"""bodies.py — Define qué es un cuerpo celeste.

¿Para qué sirve?
    Representar un cuerpo mediante su masa, posición, velocidad y nombre. Es una
    ESTRUCTURA DE DATOS, no lógica: aquí no se calcula nada, solo se guarda el
    estado del cuerpo.

¿Por qué existe?
    Todos los demás módulos necesitan una forma común de leer y escribir el estado
    (posición y velocidad). Si cada módulo inventa su propio formato, se vuelven
    incompatibles.

¿Qué contendrá?
    La clase `Body`, con su masa, posición y velocidad.

    - `name`         : nombre del cuerpo (por ejemplo "Sol", "Tierra").
    - `mass`         : masa (en kg).
    - `position`     : vector (x, y, z) en m.
    - `velocity`     : vector (vx, vy, vz) en m/s.
    - `acceleration` : vector de aceleración (m/s²), lo rellena el integrador.
    - `previous_position` : posición del paso anterior, la usa Verlet.

Unidades (SI)
    Todo el proyecto usa el Sistema Internacional; la interfaz muestra el tiempo
    en días.
        - distancia : m
        - masa      : kg
        - tiempo    : s

¿Cómo funciona paso a paso?
    1. Se crea un `Body` con su masa, posición y velocidad iniciales.
    2. Los integradores actualizan `position`, `velocity` y `acceleration`.
    3. Los demás módulos solo leen esos valores.

¿Cómo modificarlo?
    No hay nada que cambiar todavía. Si se añade un valor fijo (por ejemplo el
    tamaño del cuerpo para dibujarlo), se agrega aquí sin tocar otros archivos.
"""

import numpy as np


class Body:
    """Un cuerpo celeste: su masa, posición y velocidad actuales."""

    def __init__(self, name, mass, position, velocity):
        """Guarda los datos iniciales de un cuerpo.

        Recibe:
            name     : nombre del cuerpo, por ejemplo "Sol".
            mass      : masa en kg.
            position  : posición inicial, tres números en m.
            velocity  : velocidad inicial, tres números en m/s.

        `previous_position` empieza vacío; lo usa el integrador de Verlet.
        """
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(3)
        self.previous_position = None
