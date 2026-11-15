# código nuevo edizon
"""test_simulation.py — Pruebas del motor de simulación.

¿Para qué sirve?
    Comprobar el contrato de entrada, la política de duración, el historial, el
    límite de registros y la conservación medida en cada paso.

¿Por qué existe?
    Es el puente entre la física y la interfaz: si el motor falla, la interfaz no
    tiene nada que mostrar. Las pruebas cubren las tareas A04, A06, A07, A09, A10
    y A21 del plan de corrección.

Datos usados
    Sol–Tierra: masa del Sol 1.989e30 kg, Tierra 5.972e24 kg a 1.496e11 m.

¿Cómo ejecutarlo?
    pytest tests/test_simulation.py

¿Cómo modificarlo?
    Añadir casos nuevos si se agregan más métodos o más magnitudes.
"""

import numpy as np
import pytest

from src.physics.bodies import Body
from src.physics.gravity import G
from src.simulation import (
    INTEGRATORS,
    run_simulation,
    sample_indices,
    step_plan,
    total_steps,
)

MASA_SOL = 1.989e30     # kg.
MASA_TIERRA = 5.972e24  # kg.
DISTANCIA = 1.496e11    # m.
V_CIRCULAR = np.sqrt(G * MASA_SOL / DISTANCIA)  # m/s.
PERIODO = 2 * np.pi * DISTANCIA / V_CIRCULAR     # s.


def _sistema():
    """Crea el sistema Sol–Tierra con la Tierra en órbita circular."""
    sol = Body("Sol", MASA_SOL, np.zeros(3), np.zeros(3))
    tierra = Body(
        "Tierra", MASA_TIERRA, np.array([DISTANCIA, 0.0, 0.0]), np.array([0.0, V_CIRCULAR, 0.0])
    )
    return [sol, tierra]


def _variacion_maxima(history):
    """Mayor variación porcentual de la energía durante la corrida."""
    inicial = history["energy"][0]
    return max(abs(energia - inicial) / abs(inicial) * 100 for energia in history["energy"])


def test_total_steps():
    """365 días con paso de 1 día son 365 pasos."""
    assert total_steps(365 * 86400, 86400) == 365


def test_duracion_no_divisible_usa_un_ultimo_paso_mas_corto():
    """100 s con paso de 60 s son dos pasos: 60 s y 40 s (tarea A04)."""
    steps, last = step_plan(100.0, 60.0)

    assert steps == 2
    assert last == pytest.approx(40.0)


def test_paso_mayor_que_la_duracion_integra_la_duracion_completa():
    """Un paso de 200000 s para un día integra exactamente 86400 s."""
    steps, last = step_plan(86400.0, 200000.0)

    assert steps == 1
    assert last == pytest.approx(86400.0)


def test_los_dos_metodos_estan_disponibles():
    """El motor ofrece Euler-Cromer y Verlet."""
    assert "Euler-Cromer" in INTEGRATORS
    assert "Verlet" in INTEGRATORS


def test_el_historial_guarda_tiempo_energia_momento_y_posiciones():
    """El historial trae las listas que pide la interfaz, con inicio y final."""
    history = run_simulation(_sistema(), PERIODO / 1000, 100)

    assert len(history["time"]) == 101
    for key in ("energy", "energy_kinetic", "energy_potential", "momentum",
                "positions", "velocities"):
        assert len(history[key]) == 101
    assert history["time"][0] == 0.0
    assert history["time"][-1] == pytest.approx(history["final_time"])


def test_el_ultimo_registro_coincide_con_el_estado_final():
    """El último registro es el estado que devuelve la integración (tarea A09)."""
    bodies = _sistema()
    history = run_simulation(bodies, 60.0, 100, "Verlet", record_every=30)

    assert history["time"] == [0.0, 1800.0, 3600.0, 5400.0, 6000.0]
    assert np.allclose(history["positions"][-1][1], bodies[1].position)
    assert np.allclose(history["velocities"][-1][1], bodies[1].velocity)


def test_duracion_no_divisible_termina_en_el_tiempo_pedido():
    """100 pasos de 60 s más un último paso corto suman la duración pedida."""
    history = run_simulation(_sistema(), 60.0, 2, last_step=40.0)

    assert history["time"][-1] == pytest.approx(100.0)


def test_la_energia_total_es_cinetica_mas_potencial():
    """En cada fila del historial, E total = cinética + potencial."""
    history = run_simulation(_sistema(), PERIODO / 1000, 50)

    for total, cinetica, potencial in zip(
        history["energy"], history["energy_kinetic"], history["energy_potential"]
    ):
        assert np.isclose(total, cinetica + potencial)


def test_la_energia_se_conserva_con_los_dos_metodos():
    """Con el mismo escenario, los dos métodos conservan E dentro del 1 %."""
    for method in INTEGRATORS:
        history = run_simulation(_sistema(), PERIODO / 2000, 2000, method)
        assert _variacion_maxima(history) < 1.0


def test_distinto_paso_cambia_el_resultado():
    """Con paso más grueso el error de energía es mayor."""
    fino = run_simulation(_sistema(), PERIODO / 4000, 4000)
    grueso = run_simulation(_sistema(), PERIODO / 500, 500)

    assert _variacion_maxima(grueso) > _variacion_maxima(fino)


def test_guardar_cada_ciertos_pasos_reduce_el_historial():
    """Con `record_every` el historial trae menos filas, pero la física es igual."""
    completo = run_simulation(_sistema(), PERIODO / 1000, 1000)
    reducido = run_simulation(_sistema(), PERIODO / 1000, 1000, record_every=100)

    assert len(completo["time"]) == 1001
    assert len(reducido["time"]) == 11
    assert np.isclose(reducido["energy"][0], completo["energy"][0])
    assert reducido["time"][-1] == completo["time"][-1]


def test_el_presupuesto_de_registros_incluye_los_extremos():
    """Con `max_records` el historial no pasa del límite y conserva inicio y fin."""
    history = run_simulation(_sistema(), PERIODO / 4000, 4000, max_records=37)

    assert len(history["time"]) <= 37
    assert history["time"][0] == 0.0
    assert history["time"][-1] == pytest.approx(history["final_time"])


@pytest.mark.parametrize("total,maximo", [(1, 40), (39, 40), (40, 40), (41, 40), (100, 40), (2058, 40)])
def test_sample_indices_respeta_el_maximo_y_los_extremos(total, maximo):
    """Los índices son únicos, ordenados y siempre incluyen primero y último."""
    indices = sample_indices(total, maximo)

    assert indices[0] == 0
    assert indices[-1] == total - 1
    assert len(indices) <= maximo
    assert indices == sorted(set(indices))


def test_la_conservacion_se_mide_en_cada_paso_no_solo_en_los_guardados():
    """Cambiar cuánto se guarda no cambia el peor error medido (tarea A21)."""
    completo = run_simulation(_sistema(), PERIODO / 500, 500)
    reducido = run_simulation(_sistema(), PERIODO / 500, 500, max_records=10)

    assert completo["conservation"]["energy"]["max_percent"] == pytest.approx(
        reducido["conservation"]["energy"]["max_percent"], rel=1e-9
    )


def test_una_referencia_cero_se_informa_como_no_evaluable():
    """Si la energía inicial es cero, no se inventa un porcentaje (tarea A12)."""
    sol = Body("A", 1.0, np.zeros(3), np.zeros(3))
    cuerpo = Body("B", 1.0, np.array([1.0, 0.0, 0.0]), np.array([np.sqrt(2 * G), 0.0, 0.0]))

    from src.physics.conservation import error_report

    reporte = error_report(0.0, 0.0)
    assert reporte["reference_zero"] is True
    assert reporte["percentage"] is None

    history = run_simulation([sol, cuerpo], 1e-4, 2)
    assert "max_absolute" in history["conservation"]["energy"]


def test_un_encuentro_cercano_detiene_la_corrida():
    """Dos cuerpos que llegan al mínimo detienen la corrida con causa (A06)."""
    primero = Body("A", 1e24, np.zeros(3), np.zeros(3))
    segundo = Body("B", 1e24, np.array([2.0, 0.0, 0.0]), np.zeros(3))

    history = run_simulation([primero, segundo], 3e-7, 10, "Verlet")

    assert history["stopped"] is not None
    assert "se detuvo" in history["stopped"]["reason"]
    assert history["stopped"]["time"] > 0
    assert "A" in history["stopped"]["pair"]


def test_el_motor_rechaza_dos_cuerpos_superpuestos():
    """Dos cuerpos en el mismo punto se rechazan antes de integrar (A05)."""
    primero = Body("A", 1e24, np.zeros(3), np.zeros(3))
    segundo = Body("B", 1e24, np.zeros(3), np.zeros(3))

    with pytest.raises(ValueError, match="superpuestos|menos que el mínimo"):
        run_simulation([primero, segundo], 1.0, 1)


@pytest.mark.parametrize(
    "cambio,mensaje",
    [
        ({"dt": 0}, "paso de tiempo"),
        ({"dt": float("inf")}, "paso de tiempo"),
        ({"steps": 0}, "pasos"),
        ({"steps": 1.5}, "entero"),
        ({"record_every": 0}, "intervalo"),
        ({"method": "RK4"}, "método"),
    ],
)
def test_el_contrato_rechaza_parametros_invalidos(cambio, mensaje):
    """Cada entrada inválida da un ValueError con su causa (tarea A07)."""
    parametros = {"dt": 1.0, "steps": 10, "method": "Verlet"}
    parametros.update(cambio)

    with pytest.raises(ValueError, match=mensaje):
        run_simulation(_sistema(), **parametros)


def test_el_presupuesto_de_trabajo_rechaza_antes_de_integrar():
    """Una solicitud enorme se rechaza con el costo calculado (tarea A08)."""
    with pytest.raises(ValueError, match="Reduce la duración"):
        run_simulation(_sistema(), 1.0, 3_000_000)


def test_el_motor_rechaza_un_solo_cuerpo():
    """La entrada pública del motor exige al menos dos cuerpos (tarea A02)."""
    with pytest.raises(ValueError, match="al menos dos"):
        run_simulation([Body("Solo", 1.0, np.zeros(3), np.zeros(3))], 1.0, 1)
