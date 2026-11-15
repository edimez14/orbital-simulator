# código nuevo edizon
"""test_integrators.py — Pruebas de Euler-Cromer y Verlet.

¿Para qué sirve?
    Comprobar que los integradores avanzan el estado correctamente y comparar su
    estabilidad.

¿Por qué existe?
    Los integradores son el corazón del avance temporal. Se prueban por separado
    y luego se comparan con datos (no por suposición), según el PDF.

Datos usados
    Sol–Tierra: masa del Sol 1.989e30 kg, Tierra 5.972e24 kg a 1.496e11 m.

¿Qué comprobará?
    - Una órbita circular con Euler-Cromer: tras un periodo, vuelve cerca.
    - Un paso de Verlet: cambia el estado.
    - Verlet conserva la energía igual que Euler-Cromer (es el mismo método).

¿Cómo ejecutarlo?
    pytest tests/test_integrators.py

¿Cómo modificarlo?
    Añadir métodos nuevos como casos de prueba adicionales.
"""

import numpy as np

from src.integrators.euler_cromer import step
from src.integrators.verlet import step as verlet_step
from src.physics.bodies import Body
from src.physics.conservation import mechanical_energy, relative_error
from src.physics.gravity import G

MASA_SOL = 1.989e30     # kg.
MASA_TIERRA = 5.972e24  # kg.
DISTANCIA = 1.496e11    # m.
V_CIRCULAR = np.sqrt(G * MASA_SOL / DISTANCIA)  # m/s.
PERIODO = 2 * np.pi * DISTANCIA / V_CIRCULAR     # s.

PASOS_POR_PERIODO = 2000


def _sistema_tierra():
    """Crea el sistema Sol–Tierra con la Tierra en órbita circular."""
    sol = Body("Sol", MASA_SOL, np.zeros(3), np.zeros(3))
    tierra = Body(
        "Tierra", MASA_TIERRA, np.array([DISTANCIA, 0.0, 0.0]), np.array([0.0, V_CIRCULAR, 0.0])
    )
    return [sol, tierra]


def _error_maximo_de_energia(integrator, dt, pasos):
    """Mayor variación porcentual de la energía durante una órbita circular."""
    sistema = _sistema_tierra()
    inicial = mechanical_energy(sistema)

    maximo = 0.0
    for _ in range(pasos):
        integrator(sistema, dt)
        maximo = max(maximo, relative_error(mechanical_energy(sistema), inicial))
    return maximo


def test_orbita_circular_se_cierra():
    """Tras un periodo, la Tierra vuelve cerca de su punto de partida."""
    sistema = _sistema_tierra()
    dt = PERIODO / PASOS_POR_PERIODO

    for _ in range(PASOS_POR_PERIODO):
        step(sistema, dt)

    assert np.linalg.norm(sistema[1].position - np.array([DISTANCIA, 0.0, 0.0])) < 0.01 * DISTANCIA


def test_verlet_avanza_el_estado():
    """Un paso de Verlet cambia la posición y la velocidad de la Tierra."""
    sistema = _sistema_tierra()

    verlet_step(sistema, 60.0)

    assert not np.array_equal(sistema[1].position, np.array([DISTANCIA, 0.0, 0.0]))
    assert not np.array_equal(sistema[1].velocity, np.array([0.0, V_CIRCULAR, 0.0]))


def test_verlet_conserva_mejor_la_energia_que_euler_cromer():
    """Velocity-Verlet es un método distinto y conserva mejor la energía (A11)."""
    dt = PERIODO / 200
    pasos = 2000  # unas 10 órbitas.

    error_euler = _error_maximo_de_energia(step, dt, pasos)
    error_verlet = _error_maximo_de_energia(verlet_step, dt, pasos)

    assert error_euler < 1.0
    assert error_verlet < 1.0
    assert error_verlet < error_euler


def test_verlet_es_de_orden_dos():
    """Al reducir el paso a la mitad, el error de posición baja ~4 veces (A11)."""
    def error_tras_un_periodo(pasos):
        sistema = _sistema_tierra()
        dt = PERIODO / pasos
        for _ in range(pasos):
            verlet_step(sistema, dt)
        return np.linalg.norm(sistema[1].position - np.array([DISTANCIA, 0.0, 0.0]))

    grueso = error_tras_un_periodo(400)
    fino = error_tras_un_periodo(800)

    assert grueso / fino > 3.0
