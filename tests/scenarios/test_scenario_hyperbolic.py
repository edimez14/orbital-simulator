# código nuevo edizon
"""Escenario de prueba: trayectoria hiperbólica.

¿Para qué sirve?
    Comprobar que con una velocidad inicial mayor que la velocidad de escape el
    cuerpo escapa y describe una trayectoria abierta.

¿Por qué existe?
    Es el tercer escenario del checklist (PDF sección 5.3, paso 10). Verifica que
    el simulador distingue órbitas ligadas de trayectorias abiertas.

Velocidad de escape (PDF sección 5.4)
    v_escape = sqrt(2 * G * M / r)
    Se requiere v_inicial > v_escape.

Datos usados
    Sol: 1.989e30 kg. Cuerpo: 5.972e24 kg a 1.496e11 m.

Criterio de aceptación
    La energía total debe ser mayor o igual a cero (sistema no ligado).

¿Cómo ejecutarlo?
    pytest tests/scenarios/test_scenario_hyperbolic.py

¿Cómo modificarlo?
    Cambiar M, r, el factor sobre v_escape o la tolerancia en este bloque.
"""

import numpy as np

from src.integrators.euler_cromer import step
from src.physics.bodies import Body
from src.physics.conservation import mechanical_energy
from src.physics.gravity import G

MASA_CENTRAL = 1.989e30  # kg.
MASA_CUERPO = 5.972e24   # kg.
RADIO = 1.496e11         # m.
FACTOR_ESCAPE = 1.2      # cuánto supera la velocidad de escape.
PASOS = 20000            # pasos a simular.


def test_trayectoria_hiperbolica_escapa():
    """Con v = 1.2·v_escape la distancia crece sin volver y E ≥ 0."""
    v_escape = np.sqrt(2 * G * MASA_CENTRAL / RADIO)
    periodo_circular = 2 * np.pi * RADIO / np.sqrt(G * MASA_CENTRAL / RADIO)
    dt = periodo_circular / 2000  # unos 10 años en total.

    centro = Body("Centro", MASA_CENTRAL, np.zeros(3), np.zeros(3))
    cuerpo = Body(
        "Cuerpo",
        MASA_CUERPO,
        np.array([RADIO, 0.0, 0.0]),
        np.array([0.0, FACTOR_ESCAPE * v_escape, 0.0]),
    )

    distancias = []
    for _ in range(PASOS):
        distancias.append(np.linalg.norm(cuerpo.position - centro.position))
        step([centro, cuerpo], dt)

    mitad = len(distancias) // 2

    assert mechanical_energy([centro, cuerpo]) >= 0.0
    assert distancias[-1] > 10 * RADIO
    assert distancias[-1] > distancias[mitad]
    assert min(distancias[mitad:]) > 2 * RADIO
