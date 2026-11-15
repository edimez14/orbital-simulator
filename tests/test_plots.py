# código nuevo edizon
"""test_plots.py — Pruebas de las gráficas de análisis.

¿Para qué sirve?
    Comprobar que las cuatro gráficas se generan con sus ejes y rótulos y que se
    guardan cuando se les indica una ruta.

¿Por qué existe?
    Una gráfica sin ejes no se puede leer. Aquí se verifica que cada figura sale
    con su información (PDF sección 6.2, paso 3 de la Fase 7).

¿Qué comprobará?
    - Que cada gráfica se guarda como archivo.
    - Que cada gráfica tiene rótulos en los dos ejes.

¿Cómo ejecutarlo?
    pytest tests/test_plots.py

¿Cómo modificarlo?
    Añadir una prueba por cada gráfica nueva.
"""

import matplotlib.pyplot as plt

from src.render.plots import (
    plot_angular_momentum,
    plot_energy,
    plot_swept_area,
    plot_third_law,
)

HISTORIAL = {
    "time": [0.0, 0.5, 1.0],
    "energy": [-10.0, -10.05, -10.0],
    "momentum": [1.0, 1.0001, 1.0],
}


def _revisar(figure, output_path):
    """Comprueba que el archivo existe y que los dos ejes tienen rótulo."""
    assert output_path.exists()
    assert figure.axes[0].get_xlabel()
    assert figure.axes[0].get_ylabel()
    plt.close(figure)


def test_grafica_de_energia(tmp_path):
    """La gráfica de energía se guarda y tiene rótulos."""
    output_path = tmp_path / "energia.png"

    _revisar(plot_energy(HISTORIAL, output_path), output_path)


def test_grafica_de_momento_angular(tmp_path):
    """La gráfica de momento angular se guarda y tiene rótulos."""
    output_path = tmp_path / "momento.png"

    _revisar(plot_angular_momentum(HISTORIAL, output_path), output_path)


def test_grafica_de_area_barrida(tmp_path):
    """La gráfica de área barrida se guarda y tiene rótulos."""
    output_path = tmp_path / "area.png"

    _revisar(plot_swept_area([0.0, 0.5, 1.0], [0.0, 1.5, 3.0], output_path), output_path)


def test_grafica_de_tercera_ley(tmp_path):
    """La gráfica de T² contra a³ se guarda y tiene rótulos."""
    output_path = tmp_path / "tercera_ley.png"

    _revisar(plot_third_law([1.0, 1.52], [1.0, 1.88], output_path), output_path)
