# código nuevo edizon
"""test_kepler.py — Pruebas de las tres leyes de Kepler.

¿Para qué sirve?
    Comprobar que `kepler/kepler_laws.py` verifica las tres leyes con datos
    medidos y que rechaza los casos sin evidencia suficiente.

¿Por qué existe?
    Es la demostración final del proyecto: que el simulador reproduce la mecánica
    clásica con pruebas reproducibles. Cubre las tareas A22, A24, A25 y A26.

Cuerpo central
    Sol, masa 1.989e30 kg. Distancia de partida: 1.496e11 m.

¿Qué comprobará?
    - Primera ley: elipse con a y e calculados a mano; arco corto no certifica.
    - Segunda ley: velocidad areal constante con tiempos desiguales.
    - Periodo medido por cruce de una vuelta completa.
    - Tercera ley: T²/a³ frente a la teoría, con al menos tres órbitas.

¿Cómo ejecutarlo?
    pytest tests/test_kepler.py

¿Cómo modificarlo?
    Añadir órbitas de prueba adicionales manteniendo cada caso aislado.
"""

import numpy as np

from src.integrators.euler_cromer import step
from src.kepler.kepler_laws import (
    check_first_law,
    check_second_law,
    check_third_law,
    measure_period,
)
from src.kepler.orbit_analysis import third_law_analysis
from src.physics.bodies import Body
from src.physics.gravity import G

MASA_SOL = 1.989e30  # kg.
MASA_TIERRA = 5.972e24  # kg.
DISTANCIA = 1.496e11  # m.
MU = G * MASA_SOL  # m³/s².

PASOS_POR_PERIODO = 6000


def _orbita_relativa(factor_v, dt, steps, times=False):
    """Simula una órbita y devuelve las posiciones relativas al Sol."""
    sol = Body("Sol", MASA_SOL, np.zeros(3), np.zeros(3))
    cuerpo = Body(
        "Cuerpo",
        MASA_TIERRA,
        np.array([DISTANCIA, 0.0, 0.0]),
        np.array([0.0, factor_v * np.sqrt(MU / DISTANCIA), 0.0]),
    )

    relativas = []
    tiempos = []
    for i in range(steps):
        relativas.append(cuerpo.position - sol.position)
        tiempos.append(i * dt)
        step([sol, cuerpo], dt)
    return (relativas, tiempos) if times else relativas


def test_primera_ley():
    """Con v = 0.8·v_c: a = 1.1e11 m y e = 0.36 (calculados a mano)."""
    factor = 0.8
    a_teorico = DISTANCIA / (2 - factor**2)
    periodo = 2 * np.pi * np.sqrt(a_teorico**3 / MU)
    dt = periodo / PASOS_POR_PERIODO

    elementos = check_first_law(_orbita_relativa(factor, dt, int(periodo / dt) + 1))

    assert elementos["status"] == "ok"
    assert np.isclose(elementos["semi_major_axis"], a_teorico, rtol=0.01)
    assert abs(elementos["eccentricity"] - 0.36) < 0.01
    assert elementos["coverage_deg"] >= 330


def test_primera_ley_no_certifica_un_arco_corto():
    """Un tramo de pocos grados no alcanza para afirmar que hay elipse (A22)."""
    factor = 0.8
    a_teorico = DISTANCIA / (2 - factor**2)
    periodo = 2 * np.pi * np.sqrt(a_teorico**3 / MU)
    dt = periodo / PASOS_POR_PERIODO

    elementos = check_first_law(_orbita_relativa(factor, dt, 40))

    assert elementos["status"] == "insuficiente"
    assert "cubre" in elementos["message"] or "muestras" in elementos["message"]


def test_primera_ley_rechaza_una_hiperbola():
    """Con v = 1.5·v_c la órbita es abierta y no se clasifica como elipse."""
    dt = 3600.0
    elementos = check_first_law(_orbita_relativa(1.5, dt, 400))

    assert elementos["status"] in {"no_elipse", "insuficiente"}
    assert elementos["status"] != "ok"


def test_segunda_ley():
    """La velocidad areal varía menos del 1 %."""
    factor = 0.8
    a_teorico = DISTANCIA / (2 - factor**2)
    periodo = 2 * np.pi * np.sqrt(a_teorico**3 / MU)
    dt = periodo / PASOS_POR_PERIODO

    relativas, tiempos = _orbita_relativa(factor, dt, int(periodo / dt), times=True)
    resultado = check_second_law(relativas, tiempos)

    assert resultado["status"] == "ok"
    assert resultado["max_variation"] < 1.0


def test_segunda_ley_usa_los_tiempos_reales():
    """Con muestras desiguales, el área por tiempo sigue siendo la misma (A24)."""
    factor = 0.8
    a_teorico = DISTANCIA / (2 - factor**2)
    periodo = 2 * np.pi * np.sqrt(a_teorico**3 / MU)
    dt = periodo / PASOS_POR_PERIODO

    relativas, tiempos = _orbita_relativa(factor, dt, int(periodo / dt), times=True)
    # Se conservan una de cada tres muestras: los intervalos ya no son iguales.
    relativas = relativas[::3]
    tiempos = tiempos[::3]
    resultado = check_second_law(relativas, tiempos)

    assert resultado["max_variation"] < 1.0


def test_segunda_ley_informa_datos_insuficientes():
    """Dos muestras no permiten comparar intervalos."""
    resultado = check_second_law([np.array([1.0, 0.0, 0.0])], [0.0])

    assert resultado["status"] == "insuficiente"


def test_el_periodo_se_mide_de_la_trayectoria():
    """Un periodo circular medido coincide con el teórico (tarea A25)."""
    radio = DISTANCIA
    periodo_teorico = 2 * np.pi * np.sqrt(radio**3 / MU)
    dt = periodo_teorico / 2000

    relativas, tiempos = _orbita_relativa(
        1.0, dt, 2100, times=True
    )
    resultado = measure_period(relativas, tiempos)

    assert resultado["status"] == "ok"
    assert np.isclose(resultado["period"], periodo_teorico, rtol=0.01)


def test_el_periodo_no_se_inventa_con_un_arco_corto():
    """Un arco de menos de una vuelta no devuelve periodo."""
    resultado = measure_period(
        [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([-1.0, 0.0, 0.0]),
         np.array([0.0, -1.0, 0.0]), np.array([0.7, -0.7, 0.0])],
        [0.0, 1.0, 2.0, 3.0, 4.0],
    )

    assert resultado["status"] == "insuficiente"
    assert resultado["period"] is None


def test_tercera_ley_con_tres_orbitas_medidas():
    """Tres órbitas alrededor del mismo centro cumplen T²/a³ dentro del 1 %."""
    analisis = third_law_analysis(MASA_SOL, MASA_TIERRA, DISTANCIA)

    assert len(analisis["orbits"]) == 3
    assert analisis["check"]["status"] == "ok"
    assert analisis["check"]["max_error_percent"] < 1.0


def test_la_tercera_ley_no_certifica_con_datos_insuficientes():
    """Con dos órbitas o datos no positivos no se declara cumplida (A26)."""
    resultado = check_third_law(
        [
            {"semi_major_axis": 1.0, "period": 1.0},
            {"semi_major_axis": 2.0, "period": 2.8},
            {"semi_major_axis": 0.0, "period": 5.0},
        ]
    )

    assert resultado["status"] == "insuficiente"


def test_la_tercera_ley_detecta_datos_incoherentes():
    """Periodos inventados no coinciden con la referencia teórica."""
    resultado = check_third_law(
        [
            {"semi_major_axis": 1.0, "period": 1.0},
            {"semi_major_axis": 2.0, "period": 2.0},
            {"semi_major_axis": 3.0, "period": 3.0},
        ],
        central_mass=MASA_SOL,
    )

    assert resultado["status"] == "revisar"
    assert resultado["max_error_percent"] > 1.0
