# código nuevo edizon
"""euler_cromer.py — Integrador de Euler-Cromer.

¿Para qué sirve?
    Avanzar el estado del sistema en el tiempo. Primero actualiza la velocidad
    usando la aceleración actual y DESPUÉS actualiza la posición usando la
    velocidad NUEVA. Ese orden es lo que lo hace más estable que el Euler
    explícito para problemas orbitales.

    Velocidad nueva : v(t+dt) = v(t) + a(t) * dt
    Posición nueva  : r(t+dt) = r(t) + v(t+dt) * dt

¿Por qué existe?
    Es el integrador más simple de los dos y el primero que se implementa. Sirve
    de referencia para comparar luego con Verlet.

¿Qué contendrá?
    `step(bodies, dt)` : recibe el estado actual y `dt`, y lo avanza un paso.

¿Cómo funciona paso a paso?
    1. Pedir la aceleración actual de cada cuerpo a `gravity.py`.
    2. Actualizar la velocidad de cada cuerpo con esa aceleración.
    3. Actualizar la posición con la velocidad ya actualizada.

¿Cómo modificarlo?
    - Cambiar el orden de actualización: NO hacerlo; el orden es lo que define a
      Euler-Cromer. Para otro esquema, crear un archivo nuevo.
"""

from src.physics.gravity import compute_accelerations


def step(bodies, dt):
    """Avanza el estado del sistema un paso `dt` con Euler-Cromer.

    Recibe:
        bodies : lista de cuerpos (masa, posición y velocidad actuales).
        dt     : cuánto avanza el tiempo en este paso, en años.
    """
    accelerations = compute_accelerations(bodies)

    # Primero las velocidades, con la aceleración del instante actual.
    for body, acceleration in zip(bodies, accelerations):
        body.acceleration = acceleration
        body.velocity = body.velocity + acceleration * dt

    # Después las posiciones, con la velocidad ya actualizada.
    for body in bodies:
        body.position = body.position + body.velocity * dt
