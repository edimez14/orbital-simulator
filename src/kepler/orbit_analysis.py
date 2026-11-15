# código nuevo edizon
"""orbit_analysis.py — Compara varias órbitas para la tercera ley.

¿Para qué sirve?
    Medir el periodo y el semieje mayor de tres órbitas circulares alrededor del
    mismo cuerpo central y comprobar T²/a³. Es el flujo explícito que pide la
    tarea A27: no se corre al mover la cámara, solo cuando el usuario lo pide.

¿Por qué existe?
    La tercera ley no se puede comprobar con una sola órbita: hacen falta varias
    alrededor del mismo centro. Estas corridas son cortas y no tocan la simulación
    que el usuario está viendo.

¿Qué contiene?
    `third_law_analysis(primary, secondary, radii, method)` : corre, mide y
    devuelve los puntos junto con el diagnóstico.

¿Cómo funciona paso a paso?
    1. Para cada radio, coloca el secundario en órbita circular con
       mu = G·(M+m).
    2. Corre poco más de una vuelta y mide el periodo con las posiciones.
    3. Ajusta el semieje mayor con la primera ley.
    4. Compara las tres parejas con `check_third_law`.

¿Cómo modificarlo?
    - Cambiar los radios o el número de puntos por órbita: parámetros.
    - Cambiar el método: se pasa como argumento.
"""

import math

import numpy as np

from src.kepler.kepler_laws import check_first_law, check_third_law, measure_period
from src.physics.bodies import Body
from src.physics.gravity import G
from src.simulation import run_simulation

# Radios de comparación, en veces el radio del cuerpo analizado.
RADII_FACTORS = (0.6, 1.0, 1.5)

# Muestras por órbita al medir.
STEPS_PER_ORBIT = 600


def _circular_state(primary_mass, secondary_mass, radius):
    """Crea los dos cuerpos en una órbita circular alrededor del centro de masa.

    Recibe:
        primary_mass   : masa del primario (kg).
        secondary_mass : masa del secundario (kg).
        radius         : distancia entre los dos (m).
    Devuelve:
        La lista [primario, secundario] con la velocidad relativa correcta.
    """
    mu = G * (primary_mass + secondary_mass)
    speed = math.sqrt(mu / radius)

    primary = Body("Primario", primary_mass, np.zeros(3), np.zeros(3))
    secondary = Body(
        "Secundario",
        secondary_mass,
        np.array([radius, 0.0, 0.0]),
        np.array([0.0, speed, 0.0]),
    )
    return [primary, secondary]


def third_law_analysis(primary_mass, secondary_mass, base_radius, method="Verlet",
                       radii_factors=RADII_FACTORS):
    """Mide tres órbitas circulares y comprueba la tercera ley.

    Recibe:
        primary_mass   : masa del cuerpo central (kg).
        secondary_mass : masa del cuerpo que orbita (kg).
        base_radius    : distancia de referencia (m).
        method         : método numérico.
        radii_factors  : cuántos radios se prueban, en veces `base_radius`.
    Devuelve:
        Un diccionario con "orbits" (puntos medidos), "check" (diagnóstico) y
        "message".
    """
    mu = G * (primary_mass + secondary_mass)
    measured = []

    for factor in radii_factors:
        radius = base_radius * factor
        period_theory = 2 * math.pi * math.sqrt(radius**3 / mu)
        dt = period_theory / STEPS_PER_ORBIT
        steps = int(math.ceil(1.05 * period_theory / dt))

        bodies = _circular_state(primary_mass, secondary_mass, radius)
        history = run_simulation(bodies, dt, steps, method)

        relatives = [np.subtract(step[1], step[0]) for step in history["positions"]]
        period = measure_period(relatives, history["time"])
        ellipse = check_first_law(relatives)

        if period["status"] != "ok" or ellipse["status"] != "ok":
            continue

        measured.append(
            {
                "label": f"{factor:g}×",
                "radius": float(radius),
                "semi_major_axis": ellipse["semi_major_axis"],
                "period": period["period"],
                "mu": float(mu),
            }
        )

    check = check_third_law(measured, central_mass=primary_mass + secondary_mass)
    return {
        "orbits": measured,
        "check": check,
        "message": check["message"],
    }
