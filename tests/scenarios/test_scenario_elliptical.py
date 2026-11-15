# código nuevo edizon
"""Escenario de prueba: órbita elíptica.

¿Para qué sirve?
    Comprobar que con una velocidad tangencial menor que la circular (y menor
    que la de escape) el cuerpo describe una órbita elíptica.

¿Por qué existe?
    Es el segundo escenario del checklist (PDF sección 5.3, paso 10). Es la base
    para verificar la Primera Ley de Kepler (el cuerpo central en un foco).

Condiciones
    0 < v_inicial < v_circular   y   v_inicial < v_escape
    donde v_escape = sqrt(2 * G * M / r)

Fórmulas usadas (para comprobar)
    a = r / (2 - f²)     y     e = 1 - f², con f = v_inicial / v_circular.

Datos usados
    Sol: 1.989e30 kg. Cuerpo: 5.972e24 kg a 1.496e11 m.

¿Cómo ejecutarlo?
    pytest tests/scenarios/test_scenario_elliptical.py

¿Cómo modificarlo?
    Cambiar M, r, la fracción de v_c o la tolerancia en este bloque de arriba.
"""

import numpy as np

from src.integrators.euler_cromer import step
from src.physics.bodies import Body
from src.physics.gravity import G

MASA_CENTRAL = 1.989e30  # kg.
MASA_CUERPO = 5.972e24   # kg.
RADIO = 1.496e11         # m.
FRACCION_VELOCIDAD = 0.8  # fracción de la velocidad circular.
PASOS_POR_PERIODO = 6000


def test_orbita_eliptica():
    """Con v = 0.8·v_c: a = 1.1e11 m y e = 0.36 (dentro del 1 %)."""
    v_c = np.sqrt(G * MASA_CENTRAL / RADIO)
    a_teorico = RADIO / (2 - FRACCION_VELOCIDAD**2)
    e_teorico = 1 - FRACCION_VELOCIDAD**2
    periodo = 2 * np.pi * np.sqrt(a_teorico**3 / (G * MASA_CENTRAL))
    dt = periodo / PASOS_POR_PERIODO

    centro = Body("Centro", MASA_CENTRAL, np.zeros(3), np.zeros(3))
    cuerpo = Body(
        "Cuerpo",
        MASA_CUERPO,
        np.array([RADIO, 0.0, 0.0]),
        np.array([0.0, FRACCION_VELOCIDAD * v_c, 0.0]),
    )
    inicio = np.array([RADIO, 0.0, 0.0])

    distancias = []
    for _ in range(int(periodo / dt)):  # un periodo
        distancias.append(np.linalg.norm(cuerpo.position - centro.position))
        step([centro, cuerpo], dt)

    a_medido = (min(distancias) + max(distancias)) / 2
    e_medido = (max(distancias) - min(distancias)) / (max(distancias) + min(distancias))

    assert np.isclose(a_medido, a_teorico, rtol=0.01)
    assert abs(e_medido - e_teorico) < 0.01
    assert max(distancias) / min(distancias) > 1.5
    assert np.linalg.norm(cuerpo.position - inicio) < 0.01 * RADIO
