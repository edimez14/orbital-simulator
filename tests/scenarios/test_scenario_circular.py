# código nuevo edizon
"""Escenario de prueba: órbita circular.

¿Para qué sirve?
    Comprobar que con una velocidad tangencial igual a la velocidad circular el
    cuerpo describe una órbita aproximadamente circular.

¿Por qué existe?
    Es el escenario más simple y el primero del checklist de casos de prueba
    (PDF sección 5.3, paso 10). Si este funciona, la gravedad y el integrador
    están bien conectados.

Velocidad circular
    v_c = sqrt(G * M / r)

Datos usados
    Sol: 1.989e30 kg. Cuerpo: 5.972e24 kg a 1.496e11 m.

Criterio de aceptación
    La variación relativa del radio debe quedar por debajo del 1 %.

¿Cómo ejecutarlo?
    pytest tests/scenarios/test_scenario_circular.py

¿Cómo modificarlo?
    Cambiar M, r, los periodos o la tolerancia en este bloque de arriba.
"""

import numpy as np

from src.integrators.euler_cromer import step
from src.physics.bodies import Body
from src.physics.gravity import G

MASA_CENTRAL = 1.989e30  # kg.
MASA_CUERPO = 5.972e24   # kg.
RADIO = 1.496e11         # m.
PERIODOS = 3             # cuántos periodos simular.
PASOS_POR_PERIODO = 4000


def test_radio_casi_constante_y_orbita_cerrada():
    """Con v = v_c el radio varía menos del 1 % y la órbita se cierra."""
    v_c = np.sqrt(G * MASA_CENTRAL / RADIO)
    periodo = 2 * np.pi * RADIO / v_c
    dt = periodo / PASOS_POR_PERIODO

    centro = Body("Centro", MASA_CENTRAL, np.zeros(3), np.zeros(3))
    cuerpo = Body("Cuerpo", MASA_CUERPO, np.array([RADIO, 0.0, 0.0]), np.array([0.0, v_c, 0.0]))
    inicio = np.array([RADIO, 0.0, 0.0])

    distancias = []
    for _ in range(PERIODOS * PASOS_POR_PERIODO):
        distancias.append(np.linalg.norm(cuerpo.position - centro.position))
        step([centro, cuerpo], dt)

    variacion = (max(distancias) - min(distancias)) / RADIO * 100
    assert variacion < 1.0
    assert np.linalg.norm(cuerpo.position - inicio) < 0.01 * RADIO
