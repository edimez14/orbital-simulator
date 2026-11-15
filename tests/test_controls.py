# código nuevo edizon
"""test_controls.py — Pruebas de los controles de la interfaz.

¿Para qué sirve?
    Comprobar el umbral de velocidad de escape que muestra la interfaz
    (Fase 10, paso 2).

¿Por qué existe?
    El resto de los controles son botones y deslizadores (solo cambian valores);
    lo único con cálculo es la velocidad de escape.

¿Qué comprobará?
    - El valor de escape en un caso conocido: superficie de la Tierra ≈ 11186 m/s.
    - Que más masa implica más velocidad de escape.

¿Cómo ejecutarlo?
    pytest tests/test_controls.py

¿Cómo modificarlo?
    Añadir casos nuevos si se agregan más umbrales.
"""

import numpy as np

from src.ui.controls import escape_velocity


MASA_TIERRA = 5.972e24  # kg.
RADIO_TIERRA = 6.371e6  # m.


def test_velocidad_de_escape_conocida():
    """En la superficie de la Tierra: v_escape ≈ 11186 m/s."""
    assert np.isclose(escape_velocity(MASA_TIERRA, RADIO_TIERRA), 11186.0, rtol=1e-3)


def test_mas_masa_mayor_escape():
    """Más masa central exige más velocidad para escapar."""
    assert escape_velocity(2 * MASA_TIERRA, RADIO_TIERRA) > escape_velocity(MASA_TIERRA, RADIO_TIERRA)
