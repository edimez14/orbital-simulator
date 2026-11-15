# código nuevo edizon
"""plots.py — Gráficas 2D de análisis.

¿Para qué sirve?
    Producir las gráficas que sustentan el análisis del informe, usando
    Matplotlib.

    Gráficas previstas (PDF sección 6.2):
        - Energía relativa : t  vs  dE/E0  -> estabilidad del integrador.
        - Momento angular  : t  vs  dL/L0  -> conservación.
        - Área barrida     : t  vs  A(dt)  -> segunda ley de Kepler.
        - T² vs a³         : a³ vs T²      -> tercera ley (relación lineal).

¿Por qué existe?
    Estas gráficas NO son decoración: son la evidencia objetiva de que el método
    numérico conserva las magnitudes físicas.

¿Qué contendrá?
    - `plot_energy(history, output_path)`          : energía vs tiempo.
    - `plot_angular_momentum(history, output_path)`: momento angular vs tiempo.
    - `plot_swept_area(times, areas, ...)`         : áreas barridas.
    - `plot_third_law(a3, t2, ...)`                : T² contra a³.

    Cada función devuelve la figura y, si se le da una ruta, la guarda. Las dos
    últimas necesitan los datos que calcula `kepler.py` (Fase 8).

¿Cómo modificarlo?
    - Añadir una gráfica: nueva función aquí, reutilizando el historial.
    - Cambiar el estilo: un solo bloque de configuración al inicio del archivo.
"""

import matplotlib.pyplot as plt

from src.physics.conservation import relative_error


def _save(figure, output_path):
    """Guarda la figura si se indicó una ruta.

    Recibe:
        figure      : figura de Matplotlib.
        output_path : ruta del archivo, o None para no guardar.
    """
    if output_path is not None:
        figure.savefig(output_path)


def plot_energy(history, output_path=None):
    """Gráfica de la variación relativa de la energía contra el tiempo.

    Recibe:
        history     : historial con las listas "time" y "energy".
        output_path : ruta donde guardar la figura (opcional).
    Devuelve:
        La figura de Matplotlib.
    """
    energies = history["energy"]
    variation = [relative_error(value, energies[0]) for value in energies]

    figure, axes = plt.subplots()
    axes.plot(history["time"], variation)
    axes.set_xlabel("Tiempo (años)")
    axes.set_ylabel("Variación de energía (%)")
    axes.set_title("Conservación de la energía")
    _save(figure, output_path)
    return figure


def plot_angular_momentum(history, output_path=None):
    """Gráfica de la variación relativa del momento angular contra el tiempo.

    Recibe:
        history     : historial con las listas "time" y "momentum".
        output_path : ruta donde guardar la figura (opcional).
    Devuelve:
        La figura de Matplotlib.
    """
    momenta = history["momentum"]
    variation = [relative_error(value, momenta[0]) for value in momenta]

    figure, axes = plt.subplots()
    axes.plot(history["time"], variation)
    axes.set_xlabel("Tiempo (años)")
    axes.set_ylabel("Variación de momento angular (%)")
    axes.set_title("Conservación del momento angular")
    _save(figure, output_path)
    return figure


def plot_swept_area(times, areas, output_path=None):
    """Gráfica del área barrida por el radio vector contra el tiempo.

    Recibe:
        times       : tiempos medidos (en años).
        areas       : áreas barridas en cada intervalo (en AU²).
        output_path : ruta donde guardar la figura (opcional).
    Devuelve:
        La figura de Matplotlib.
    """
    figure, axes = plt.subplots()
    axes.plot(times, areas)
    axes.set_xlabel("Tiempo (años)")
    axes.set_ylabel("Área barrida (AU²)")
    axes.set_title("Segunda ley de Kepler")
    _save(figure, output_path)
    return figure


def plot_third_law(semi_major_axes, periods, output_path=None):
    """Gráfica de T² contra a³ para varias órbitas alrededor del mismo cuerpo.

    Recibe:
        semi_major_axes : semiejes mayores (en AU).
        periods         : periodos correspondientes (en años).
        output_path     : ruta donde guardar la figura (opcional).
    Devuelve:
        La figura de Matplotlib.
    """
    figure, axes = plt.subplots()
    axes.plot([a**3 for a in semi_major_axes], [t**2 for t in periods], "o")
    axes.set_xlabel("a³ (AU³)")
    axes.set_ylabel("T² (años²)")
    axes.set_title("Tercera ley de Kepler")
    _save(figure, output_path)
    return figure
