# código nuevo edizon
"""figures.py — Figuras de la interfaz (Plotly).

¿Para qué sirve?
    Construir las figuras que muestra el panel: la vista de la órbita (animada),
    la trayectoria en 2D, la energía, el momento angular y la verificación de
    Kepler.

¿Por qué existe?
    Separa el dibujo del panel. `app.py` arma la pantalla; aquí se arma cada
    figura a partir del historial.

¿Qué contendrá?
    - `orbit_animation(history, names, ...)` : vista de la órbita animada.
    - `orbit_figure(history, names)`         : vista completa, sin animación.
    - `orbit_frame(history, names, index)`   : la órbita hasta un punto.
    - `trajectory_figure(history, names)`    : la órbita en 2D (plano x–y).
    - `energy_figure(history)`               : energía total, cinética y potencial.
    - `momentum_figure(history)`             : momento angular.
    - `kepler_figure(history)`               : áreas barridas (segunda ley).

Sobre la vista de la órbita (Tarea 13)
    Plotly dibuja el 3D con WebGL y hay navegadores que no lo soportan. Aquí la
    órbita se dibuja con líneas y puntos normales, aplicando una proyección: los
    tres ejes se ven inclinados y dan la sensación de profundidad, sin WebGL.

Sobre la animación (Tarea 27)
    La animación va en cuadros dentro de la misma figura, con su botón de
    reproducir y pausar. Así corre en el navegador y no depende de la red.

Sobre los cuerpos (Tarea 24)
    Cada cuerpo se dibuja como una esfera: un círculo del color del cuerpo, un halo
    suave alrededor y un brillo.

Unidades
    Distancias en metros, energía en julios, momento en kg·m²/s; el tiempo de las
    gráficas va en días. Las posiciones se dibujan respecto al cuerpo primario,
    que queda en el centro.

¿Cómo modificarlo?
    - Cambiar colores o tamaños: en `_BODY_COLORS` y las constantes de arriba.
    - Cambiar el ángulo de la vista: en `_AZIMUTH` y `_ELEVATION`.
    - Añadir otra figura: nueva función aquí.
"""

import math

import numpy as np
import plotly.graph_objects as go

from src.kepler.kepler_laws import check_second_law
from src.simulation import sample_indices

# Colores de los cuerpos que no están en la lista de abajo.
_COLORS = ["#2b7fff", "#ef4444", "#22c55e", "#eab308", "#a855f7"]

# Color propio de cada cuerpo.
_BODY_COLORS = {
    "Sol": "#f5c542",
    "Mercurio": "#9aa4b2",
    "Venus": "#e0a35b",
    "Tierra": "#2b7fff",
    "Marte": "#d1603d",
    "Luna": "#c8ccd4",
    "Júpiter": "#d8a273",
    "Saturno": "#e3d3a3",
    "Urano": "#8fd3e8",
    "Neptuno": "#5b7ff0",
}

# Ángulos de la vista de la órbita, en grados.
_AZIMUTH = 35.0
_ELEVATION = 25.0

# Largo de los ejes de referencia (en relación con la órbita).
_AXIS_FACTOR = 1.2

# Estrellas del fondo.
_STAR_COUNT = 160

# Cuadros y velocidad de la animación.
_FRAMES = 150
_FRAME_MS = 40

_SEGUNDOS_POR_DIA = 86400


def _base_layout(figure, height=200):
    """Aplica el estilo oscuro común a una figura.

    Recibe:
        figure : figura de Plotly.
        height : alto en píxeles.
    Devuelve:
        La misma figura, ya con el estilo.
    """
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1626",
        plot_bgcolor="#0e1626",
        height=height,
        margin={"l": 55, "r": 20, "t": 20, "b": 40},
        legend={"font": {"color": "#c9d6e8"}},
        font={"color": "#8fa3bf"},
    )
    return figure


def _relative_positions(steps, index):
    """Posiciones del cuerpo `index` respecto al primario (índice 0)."""
    return [np.subtract(step[index], step[0]) for step in steps]


def _body_color(name, index):
    """Color del cuerpo: el suyo si es conocido, o uno de la lista."""
    return _BODY_COLORS.get(name, _COLORS[(index - 1) % len(_COLORS)])


def _stars(extent):
    """Fondo de estrellas, para que la escena no se vea vacía.

    Recibe:
        extent : tamaño de la vista en unidades de pantalla.
    Devuelve:
        La traza con los puntos de las estrellas.
    """
    rng = np.random.default_rng(7)
    xs = rng.uniform(-2.0, 2.0, _STAR_COUNT) * extent
    ys = rng.uniform(-2.0, 2.0, _STAR_COUNT) * extent

    return go.Scatter(
        x=xs,
        y=ys,
        mode="markers",
        marker={"size": 3, "color": "#6b7c94"},
        name="estrellas",
        hoverinfo="skip",
        showlegend=False,
    )


def _project(points, azimuth=_AZIMUTH, elevation=_ELEVATION):
    """Pasa puntos (x, y, z) a coordenadas de pantalla (x, y).

    Usa dos ángulos: azimut (giro) y elevación (altura). Así la órbita se ve
    inclinada, sin necesidad de WebGL.

    Recibe:
        points    : lista de puntos (x, y, z).
        azimuth   : giro, en grados.
        elevation : altura, en grados.
    Devuelve:
        Dos listas: coordenada horizontal y coordenada vertical.
    """
    az = math.radians(azimuth)
    el = math.radians(elevation)

    horizontales, verticales = [], []
    for point in points:
        x, y, z = float(point[0]), float(point[1]), float(point[2])
        horizontales.append(-x * math.sin(az) + y * math.cos(az))
        verticales.append(-(x * math.cos(az) + y * math.sin(az)) * math.sin(el) + z * math.cos(el))
    return horizontales, verticales


def _extent(names, steps, index=None, zoom=1.0):
    """Mitad del encuadre de la vista.

    Se calcula con lo que se lleva recorrido, para que el trazo no se vea
    diminuto cuando el cuerpo se aleja mucho (Tarea 23).
    """
    hasta = len(steps) if index is None else min(index + 1, len(steps))

    extent = 0.0
    for i in range(1, len(names)):
        for punto in _relative_positions(steps, i)[:hasta]:
            extent = max(extent, abs(float(punto[0])), abs(float(punto[1])), abs(float(punto[2])))

    return (extent * _AXIS_FACTOR / max(zoom, 0.1)) or 1.0


def _body_traces(name, x, y, extent, color, central=False):
    """Las tres trazas de un cuerpo: halo, cuerpo y brillo.

    El brillo se dibuja en la MISMA posición que el cuerpo. Antes se desplazaba
    una fracción del tamaño de la órbita y con el zoom quedaba como un punto
    separado (tarea A30).

    Recibe:
        name    : nombre del cuerpo.
        x, y    : posición ya proyectada.
        extent  : tamaño de la vista (se conserva por compatibilidad).
        color   : color del cuerpo.
        central : True para el cuerpo central (más grande).
    Devuelve:
        La lista de trazas.
    """
    size = 26 if central else 15

    return [
        go.Scatter(
            x=[x], y=[y], mode="markers",
            marker={"size": size * 2.1, "color": color, "opacity": 0.16},
            showlegend=False, hoverinfo="skip",
        ),
        go.Scatter(
            x=[x], y=[y], mode="markers",
            marker={"size": size, "color": color, "line": {"width": 0}},
            name=name, hoverinfo="skip",
        ),
        go.Scatter(
            x=[x], y=[y], mode="markers",
            marker={"size": max(4, size * 0.34), "color": "#ffffff", "opacity": 0.45},
            showlegend=False, hoverinfo="skip",
        ),
    ]


def _add_body(figure, name, x, y, extent, color, central=False):
    """Dibuja un cuerpo como una esfera: halo, círculo y brillo."""
    for trace in _body_traces(name, x, y, extent, color, central):
        figure.add_trace(trace)


def _orbit_view(names, steps, index=None, azimuth=_AZIMUTH, elevation=_ELEVATION, zoom=1.0):
    """Vista de la órbita: estrellas, ejes, recorrido y cuerpos.

    Recibe:
        names     : nombres de los cuerpos.
        steps     : posiciones por paso (cada paso: una posición por cuerpo).
        index     : hasta qué paso dibujar el recorrido (None = todo).
        azimuth   : giro de la vista, en grados.
        elevation : inclinación de la vista, en grados.
        zoom      : acercamiento (1 = normal).
    Devuelve:
        La figura de Plotly.
    """
    relative = {i: _relative_positions(steps, i) for i in range(1, len(names))}
    extent = _extent(names, steps, index, zoom)

    figure = go.Figure()
    figure.add_trace(_stars(extent))

    # Ejes de referencia, para dar la sensación de profundidad.
    for nombre, color, extremo in (
        ("x", "#ef4444", (extent, 0.0, 0.0)),
        ("y", "#22c55e", (0.0, extent, 0.0)),
        ("z", "#3b82f6", (0.0, 0.0, extent)),
    ):
        xs, ys = _project([(0.0, 0.0, 0.0), extremo], azimuth, elevation)
        figure.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line={"color": color, "width": 1}, name=f"eje {nombre}"))

    # Recorrido de cada cuerpo que orbita.
    for i in range(1, len(names)):
        color = _body_color(names[i], i)
        xs, ys = _project(relative[i], azimuth, elevation)

        if index is None:
            figure.add_trace(
                go.Scatter(x=xs, y=ys, mode="lines", line={"color": color, "width": 2}, name=f"Órbita: {names[i]}")
            )
        else:
            figure.add_trace(
                go.Scatter(
                    x=xs, y=ys, mode="lines", opacity=0.30, hoverinfo="skip", showlegend=False,
                    line={"color": color, "width": 1, "dash": "dot"},
                )
            )
            figure.add_trace(
                go.Scatter(
                    x=xs[: index + 1], y=ys[: index + 1],
                    mode="lines", line={"color": color, "width": 3}, name=f"Órbita: {names[i]}",
                )
            )

    # Los cuerpos, en su posición actual.
    _add_body(figure, names[0], 0.0, 0.0, extent, _body_color(names[0], 0), central=True)
    for i, name in enumerate(names):
        if i == 0:
            continue
        punto = relative[i][-1 if index is None else index]
        xs, ys = _project([punto], azimuth, elevation)
        _add_body(figure, name, xs[0], ys[0], extent, _body_color(name, i))

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0a1120",
        plot_bgcolor="#0a1120",
        height=360,
        margin={"l": 10, "r": 10, "t": 10, "b": 60},
        # Mantiene el giro y el acercamiento que haga el usuario.
        uirevision="orbita",
        legend={"font": {"color": "#c9d6e8"}, "orientation": "h", "y": -0.05, "x": 0.0},
        xaxis={"range": [-extent, extent], "visible": False, "scaleanchor": "y", "scaleratio": 1},
        yaxis={"range": [-extent, extent], "visible": False},
    )
    return figure


def orbit_figure(history, names):
    """Vista completa de la órbita (sin animación).

    Recibe:
        history : historial con la lista "positions".
        names   : nombres de los cuerpos, en el mismo orden del historial.
    Devuelve:
        La figura de Plotly.
    """
    return _orbit_view(names, history["positions"])


def orbit_frame(history, names, index, azimuth=_AZIMUTH, elevation=_ELEVATION, zoom=1.0):
    """Vista de la órbita hasta un punto.

    Recibe:
        history   : historial con la lista "positions".
        names     : nombres de los cuerpos.
        index     : hasta qué paso se dibuja el recorrido.
        azimuth   : giro de la vista, en grados.
        elevation : inclinación de la vista, en grados.
        zoom      : acercamiento (1 = normal).
    Devuelve:
        La figura de Plotly.
    """
    total = len(history["positions"])
    return _orbit_view(
        names,
        history["positions"],
        max(0, min(index, total - 1)),
        azimuth=azimuth,
        elevation=elevation,
        zoom=zoom,
    )


def orbit_animation(history, names, azimuth=_AZIMUTH, elevation=_ELEVATION, zoom=1.0, frames=_FRAMES):
    """Vista de la órbita animada dentro del navegador (Tarea 27).

    La figura trae todos los cuadros y dos botones: reproducir y pausar. La
    animación corre en el navegador, así que no le pide nada al servidor.

    Recibe:
        history   : historial con la lista "positions".
        names     : nombres de los cuerpos.
        azimuth   : giro de la vista, en grados.
        elevation : inclinación de la vista, en grados.
        zoom      : acercamiento (1 = normal).
        frames    : cuántos cuadros guardar, como máximo.
    Devuelve:
        La figura de Plotly, lista para reproducir.
    """
    steps = history["positions"]
    total = len(steps)
    # Índices únicos repartidos, con el primero y el último (tarea A31).
    indices = sample_indices(total, frames)
    if not indices:
        indices = [0]

    # La órbita se dibuja completa; los cuadros solo mueven los cuerpos. Así la
    # animación pesa poco (Tarea 27).
    figure = _orbit_view(names, steps, index=None, azimuth=azimuth, elevation=elevation, zoom=zoom)

    relative = {i: _relative_positions(steps, i) for i in range(1, len(names))}

    # Orden de las trazas de `_orbit_view` con la órbita completa: estrellas, tres
    # ejes, una línea por cada cuerpo que orbita y, después, los cuerpos (halo,
    # cuerpo y brillo), primero el central.
    primero_cuerpo = 4 + (len(names) - 1) + 3

    cuadros = []
    pasos_del_cursor = []

    for indice in indices:
        alcance = _extent(names, steps, indice, zoom)
        datos = []
        trazas = []

        for i in range(1, len(names)):
            base = primero_cuerpo + 3 * (i - 1)
            punto = relative[i][indice]
            bx, by = _project([punto], azimuth, elevation)
            trazas.extend([base, base + 1, base + 2])
            datos.extend(_body_traces(names[i], bx[0], by[0], alcance, _body_color(names[i], i)))

        cuadros.append(
            go.Frame(
                name=str(indice),
                data=datos,
                traces=trazas,
                layout={"xaxis": {"range": [-alcance, alcance]}, "yaxis": {"range": [-alcance, alcance]}},
            )
        )
        pasos_del_cursor.append(
            {
                "method": "animate",
                "label": "",
                "args": [
                    [str(indice)],
                    {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}},
                ],
            }
        )

    figure.frames = cuadros
    figure.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 0.0, "y": -0.16, "xanchor": "left", "yanchor": "top",
                "bgcolor": "#16233a", "font": {"color": "#e6edf7"},
                "buttons": [
                    {
                        "label": "Reproducir",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": _FRAME_MS, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "Pausar",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                    {
                        # Reiniciar vuelve al primer cuadro sin recalcular la
                        # física: la figura ya trae todos los cuadros (A32).
                        "label": "Reiniciar",
                        "method": "animate",
                        "args": [
                            [str(indices[0])],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                ],
            }
        ],
        sliders=[{"active": 0, "steps": pasos_del_cursor, "x": 0.25, "len": 0.75, "y": -0.12}],
    )
    return figure


def trajectory_figure(history, names):
    """Órbita en 2D (plano x–y) del cuerpo que orbita respecto al primario.

    Recibe:
        history : historial con la lista "positions".
        names   : nombres de los cuerpos, en el mismo orden del historial.
    Devuelve:
        La figura de Plotly.
    """
    steps = history["positions"]

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(x=[0.0], y=[0.0], mode="markers", marker={"size": 11, "color": _body_color(names[0], 0)}, name=names[0])
    )

    for index in range(1, len(names)):
        relativas = _relative_positions(steps, index)
        xs = [float(p[0]) for p in relativas]
        ys = [float(p[1]) for p in relativas]
        color = _body_color(names[index], index)

        figure.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line={"color": color}, name=f"Órbita: {names[index]}"))
        figure.add_trace(
            go.Scatter(x=[xs[-1]], y=[ys[-1]], mode="markers", marker={"size": 8, "color": color}, name=names[index])
        )

    _base_layout(figure)
    figure.update_layout(
        xaxis={"title": "x (m)", "gridcolor": "#1c2a44", "scaleanchor": "y", "scaleratio": 1},
        yaxis={"title": "y (m)", "gridcolor": "#1c2a44"},
    )
    return figure


def energy_figure(history):
    """Energía mecánica contra el tiempo: total, cinética y potencial.

    Recibe:
        history : historial con "time", "energy", "energy_kinetic" y
                  "energy_potential".
    Devuelve:
        La figura de Plotly.
    """
    dias = [time / _SEGUNDOS_POR_DIA for time in history["time"]]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=dias, y=history["energy"], mode="lines", name="Total", line={"color": "#2b7fff"}))
    figure.add_trace(go.Scatter(x=dias, y=history["energy_kinetic"], mode="lines", name="Cinética", line={"color": "#22c55e"}))
    figure.add_trace(go.Scatter(x=dias, y=history["energy_potential"], mode="lines", name="Potencial", line={"color": "#eab308"}))

    _base_layout(figure)
    figure.update_layout(
        xaxis={"title": "Tiempo (días)", "gridcolor": "#1c2a44"},
        yaxis={"title": "Energía (J)", "gridcolor": "#1c2a44"},
    )
    return figure


def momentum_figure(history):
    """Momento angular contra el tiempo.

    Recibe:
        history : historial con "time" y "momentum".
    Devuelve:
        La figura de Plotly.
    """
    dias = [time / _SEGUNDOS_POR_DIA for time in history["time"]]

    figure = go.Figure(
        go.Scatter(x=dias, y=history["momentum"], mode="lines", name="L", line={"color": "#a855f7"})
    )

    _base_layout(figure)
    figure.update_layout(
        xaxis={"title": "Tiempo (días)", "gridcolor": "#1c2a44"},
        yaxis={"title": "L (kg·m²/s)", "gridcolor": "#1c2a44"},
    )
    return figure


def kepler_figure(history, index=1):
    """Velocidad areal del cuerpo analizado (segunda ley de Kepler).

    Usa los tiempos reales del historial, no un dt supuesto, y compara la
    velocidad areal (área / tiempo) para que un muestreo desigual no falsee el
    resultado (tarea A24).

    Recibe:
        history : historial con "time" y "positions".
        index   : posición del cuerpo analizado dentro de cada muestra.
    Devuelve:
        La figura de Plotly.
    """
    positions = history.get("positions", [])
    times = history.get("time", [])
    if len(positions) < 3 or index >= len(positions[0]):
        figure = go.Figure()
        _base_layout(figure)
        figure.add_annotation(
            text="Hacen falta al menos tres muestras para comprobar la segunda ley.",
            showarrow=False, font={"color": "#8fa3bf"},
        )
        return figure

    relativas = _relative_positions(positions, index)
    resultado = check_second_law(relativas, times)

    dias = [time / _SEGUNDOS_POR_DIA for time in resultado["times"]]
    figure = go.Figure(
        go.Scatter(
            x=dias,
            y=resultado["areal_velocities"],
            mode="lines+markers",
            name="Velocidad areal",
            line={"color": "#f97316"},
        )
    )

    _base_layout(figure)
    figure.update_layout(
        xaxis={"title": "Tiempo (días)", "gridcolor": "#1c2a44"},
        yaxis={"title": "Área / tiempo (m²/s)", "gridcolor": "#1c2a44"},
        annotations=[
            {
                "text": resultado["message"],
                "xref": "paper",
                "yref": "paper",
                "x": 0.0,
                "y": 1.12,
                "showarrow": False,
                "font": {"color": "#8fa3bf", "size": 10},
            }
        ],
    )
    return figure


def third_law_figure(orbits):
    """Puntos medidos de T² frente a a³, con la referencia teórica.

    Recibe:
        orbits : lista de diccionarios con "semi_major_axis" y "period".
    Devuelve:
        La figura de Plotly. Si no hay datos, lo dice en el gráfico.
    """
    valid = [
        orbit for orbit in orbits
        if orbit.get("semi_major_axis", 0) > 0 and orbit.get("period", 0) > 0
    ]

    figure = go.Figure()
    _base_layout(figure)

    if len(valid) < 2:
        figure.add_annotation(
            text="Hacen falta al menos dos órbitas medidas.",
            showarrow=False, font={"color": "#8fa3bf"},
        )
        return figure

    a3 = [orbit["semi_major_axis"] ** 3 for orbit in valid]
    t2 = [orbit["period"] ** 2 for orbit in valid]

    figure.add_trace(
        go.Scatter(x=a3, y=t2, mode="markers+text", text=[o.get("label", "") for o in valid],
                   textposition="top center", name="Medido", marker={"size": 10, "color": "#2b7fff"})
    )

    # Referencia teórica: T² = (4π² / mu) · a³.
    if valid[0].get("mu"):
        factor = 4 * math.pi**2 / valid[0]["mu"]
        xs = [0.0, max(a3) * 1.1]
        figure.add_trace(
            go.Scatter(x=xs, y=[factor * x for x in xs], mode="lines",
                       name="Teoría", line={"color": "#22c55e", "dash": "dot"})
        )

    figure.update_layout(
        xaxis={"title": "a³ (m³)", "gridcolor": "#1c2a44"},
        yaxis={"title": "T² (s²)", "gridcolor": "#1c2a44"},
    )
    return figure
