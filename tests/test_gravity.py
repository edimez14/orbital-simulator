# código nuevo edizon
"""test_gravity.py — Pruebas del cálculo gravitacional.

¿Para qué sirve?
    Comprobar que `physics/gravity.py` calcula la aceleración correctamente,
    comparando contra valores calculados a mano en unidades SI.

¿Por qué existe?
    Un error en la gravedad invalida todo el simulador. Se prueba de forma
    aislada antes de continuar con los integradores (PDF sección 5.3, paso 2).

Datos usados (Sol–Tierra)
    Masa del Sol      : 1.989e30 kg
    Masa de la Tierra : 5.972e24 kg
    Distancia         : 1.496e11 m

¿Qué comprobará?
    - La magnitud y la dirección de la aceleración contra un valor a mano.
    - Que la fuerza atrae (no empuja).

¿Cómo ejecutarlo?
    pytest tests/test_gravity.py

¿Cómo modificarlo?
    Añadir más casos aquí, manteniendo cada prueba independiente.
"""

import numpy as np

from src.physics.bodies import Body
from src.physics.gravity import G, compute_accelerations

MASA_SOL = 1.989e30     # kg.
MASA_TIERRA = 5.972e24  # kg.
DISTANCIA = 1.496e11    # m.


def _sol_y_tierra():
    """Crea el Sol en el origen y la Tierra sobre el eje x."""
    sol = Body("Sol", MASA_SOL, np.zeros(3), np.zeros(3))
    tierra = Body("Tierra", MASA_TIERRA, np.array([DISTANCIA, 0.0, 0.0]), np.zeros(3))
    return sol, tierra


def test_aceleracion_coincide_con_el_calculo_a_mano():
    """La Tierra cae hacia el Sol con a = G·M/r² ≈ 5.931e-3 m/s²."""
    sol, tierra = _sol_y_tierra()

    aceleraciones = compute_accelerations([sol, tierra])

    assert np.isclose(aceleraciones[1][0], -5.931e-3, rtol=1e-3)
    assert np.isclose(aceleraciones[1][1], 0.0)
    assert np.isclose(aceleraciones[1][2], 0.0)


def test_la_fuerza_atrae():
    """La Tierra está a la derecha del Sol, así que acelera hacia la izquierda."""
    sol, tierra = _sol_y_tierra()

    aceleraciones = compute_accelerations([sol, tierra])

    assert aceleraciones[1][0] < 0.0
