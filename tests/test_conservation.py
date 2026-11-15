# código nuevo edizon
"""test_conservation.py — Pruebas de conservación de energía y momento angular.

¿Para qué sirve?
    Verificar que `physics/conservation.py` calcula bien la energía mecánica y el
    momento angular, y que el integrador los conserva dentro de la tolerancia.

¿Por qué existe?
    Es el criterio objetivo para validar el método numérico. Si energía o momento
    angular se disparan, el integrador o la gravedad están mal.

Datos usados (Sol–Tierra)
    Masa del Sol      : 1.989e30 kg
    Masa de la Tierra : 5.972e24 kg
    Distancia         : 1.496e11 m

¿Qué comprobará?
    - Energía cinética, potencial y momento angular en casos conocidos.
    - La variación relativa (≤ 1 %) en una órbita circular.

¿Cómo ejecutarlo?
    pytest tests/test_conservation.py

¿Cómo modificarlo?
    Cambiar la tolerancia en un solo lugar y documentar por qué.
"""

import numpy as np

from src.integrators.euler_cromer import step
from src.physics.bodies import Body
from src.physics.conservation import (
    angular_momentum,
    kinetic_energy,
    mechanical_energy,
    potential_energy,
    relative_error,
)
from src.physics.gravity import G

MASA_SOL = 1.989e30     # kg.
MASA_TIERRA = 5.972e24  # kg.
DISTANCIA = 1.496e11    # m.
V_CIRCULAR = np.sqrt(G * MASA_SOL / DISTANCIA)  # m/s.

PASOS_POR_PERIODO = 2000


def test_energia_cinetica():
    """Masa 2 kg con velocidad (3, 0, 0) m/s: K = 9 J."""
    cuerpo = Body("Prueba", 2.0, np.zeros(3), np.array([3.0, 0.0, 0.0]))

    assert kinetic_energy(cuerpo) == 9.0


def test_energia_potencial():
    """Dos masas de 1 kg separadas 1 m: U = -G julios."""
    primero = Body("A", 1.0, np.zeros(3), np.zeros(3))
    segundo = Body("B", 1.0, np.array([1.0, 0.0, 0.0]), np.zeros(3))

    assert np.isclose(potential_energy([primero, segundo]), -G)


def test_momento_angular():
    """La Tierra en órbita: L_z = m · r · v."""
    tierra = Body(
        "Tierra", MASA_TIERRA, np.array([DISTANCIA, 0.0, 0.0]), np.array([0.0, V_CIRCULAR, 0.0])
    )

    momento = angular_momentum(tierra)

    assert np.isclose(momento[2], MASA_TIERRA * DISTANCIA * V_CIRCULAR)
    assert np.isclose(momento[0], 0.0)
    assert np.isclose(momento[1], 0.0)


def test_variacion_relativa():
    """De 100 a 101 hay 1 %."""
    assert relative_error(101.0, 100.0) == 1.0


def test_orbita_circular_conserva_energia_y_momento():
    """En una órbita circular, E y L varían menos del 1 % tras un periodo."""
    sol = Body("Sol", MASA_SOL, np.zeros(3), np.zeros(3))
    tierra = Body(
        "Tierra", MASA_TIERRA, np.array([DISTANCIA, 0.0, 0.0]), np.array([0.0, V_CIRCULAR, 0.0])
    )
    sistema = [sol, tierra]

    energia_inicial = mechanical_energy(sistema)
    momento_inicial = np.linalg.norm(angular_momentum(sol) + angular_momentum(tierra))

    periodo = 2 * np.pi * DISTANCIA / V_CIRCULAR
    dt = periodo / PASOS_POR_PERIODO
    for _ in range(PASOS_POR_PERIODO):
        step(sistema, dt)

    energia_final = mechanical_energy(sistema)
    momento_final = np.linalg.norm(angular_momentum(sol) + angular_momentum(tierra))

    assert relative_error(energia_final, energia_inicial) < 1.0
    assert relative_error(momento_final, momento_inicial) < 1.0
