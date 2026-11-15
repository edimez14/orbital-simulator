# código nuevo edizon
"""verlet.py — Integrador de velocity-Verlet.

¿Para qué sirve?
    Avanzar el estado del sistema con un método de orden dos: la posición usa la
    posición, la velocidad y la aceleración del instante actual; la velocidad usa
    la aceleración actual y la del instante nuevo.

    r(t+dt) = r(t) + v(t)·dt + ½·a(t)·dt²
    v(t+dt) = v(t) + ½·(a(t) + a(t+dt))·dt

¿Por qué existe?
    Antes el archivo usaba la forma de posición de Verlet y estimaba la velocidad
    con una diferencia hacia atrás: eso reproducía Euler-Cromer y no mejoraba la
    energía. Esta variante sí es un método distinto y de orden dos (tarea A11).

¿Qué contiene?
    `step(bodies, dt)` : avanza todos los cuerpos un paso.

¿Cómo funciona paso a paso?
    1. Calcular las aceleraciones en el instante actual.
    2. Mover todas las posiciones con la fórmula de arriba.
    3. Recalcular las aceleraciones con las posiciones nuevas.
    4. Actualizar las velocidades con el promedio de las dos aceleraciones.

¿Cómo modificarlo?
    - Cambiar el método: crear otro archivo en `integrators/`, no tocar este.
    - Añadir otra magnitud: no hace falta; el motor la guarda desde fuera.
"""

from src.physics.gravity import compute_accelerations


def step(bodies, dt):
    """Avanza el estado del sistema un paso `dt` con velocity-Verlet.

    Recibe:
        bodies : lista de cuerpos (masa, posición y velocidad actuales).
        dt     : cuánto avanza el tiempo en este paso, en segundos.
    Devuelve:
        Nada; actualiza posición, velocidad, aceleración y posición anterior.
    """
    # Aceleración del instante actual, antes de mover nada.
    current_accelerations = compute_accelerations(bodies)
    previous_positions = [body.position.copy() for body in bodies]

    # Primero se mueven TODAS las posiciones...
    for body, acceleration in zip(bodies, current_accelerations):
        body.position = body.position + body.velocity * dt + 0.5 * acceleration * dt**2

    # ...y solo entonces se recalculan las aceleraciones con las posiciones nuevas.
    new_accelerations = compute_accelerations(bodies)

    # La velocidad combina la aceleración vieja y la nueva: así el método es de
    # orden dos y conserva mejor la energía.
    for body, acceleration, new_acceleration, previous in zip(
        bodies, current_accelerations, new_accelerations, previous_positions
    ):
        body.velocity = body.velocity + 0.5 * (acceleration + new_acceleration) * dt
        body.acceleration = new_acceleration
        body.previous_position = previous
