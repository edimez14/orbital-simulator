# código nuevo edizon
"""app.py — Interfaz web (Dash) del simulador.

¿Para qué sirve?
    Montar el panel del boceto: a la izquierda la configuración, en el centro la
    vista, los resultados y la tabla, y a la derecha las gráficas.

¿Por qué existe?
    VPython no puede dibujar este panel. Dash permite el diseño del boceto y deja
    la física en Python, separada de lo visual.

¿Qué contiene?
    - La estructura y el tema oscuro del boceto.
    - Edición de cuerpos: nombre, masa, posición y velocidad; agregar y eliminar.
    - Tipos de órbita y control de velocidad, con clasificación física real.
    - Selector del cuerpo analizado, para que tarjetas, tabla y leyes hablen del
      mismo cuerpo.
    - Estado visible de la corrida: validación, errores y conservación medida.
    - Primera ley en pantalla y análisis explícito de la tercera ley.

Unidades
    Todo en SI. La tabla y las gráficas muestran el tiempo en días.

¿Cómo modificarlo?
    - Cambiar los cuerpos iniciales: ajustar `DEFAULT_PRESET`.
    - Cambiar el tema: `assets/style.css`.
    - Cada sección de la página es una función `_..._panel()`.
"""

import copy
import logging
import math

import numpy as np
import plotly.graph_objects as go
from dash import (
    ALL,
    Dash,
    Input,
    Output,
    State,
    callback_context,
    dash_table,
    dcc,
    html,
    no_update,
)

from src.config import project_root
from src.kepler.kepler_laws import check_first_law
from src.kepler.orbit_analysis import third_law_analysis
from src.physics.bodies import Body
from src.physics.gravity import G
from src.physics.validation import (
    overlap_message,
    overlapping_pairs,
    validate_bodies_data,
)
from src.simulation import (
    INTEGRATORS,
    load_bodies,
    parse_positive,
    preset_names,
    run_simulation,
    sample_indices,
    step_plan,
)
from src.ui import figures

ROOT = project_root()

SEGUNDOS_POR_DIA = 86400

# Escenario inicial (el del boceto: Tierra y Luna).
DEFAULT_PRESET = "tierra_luna"
DEFAULT_METHOD = "Verlet"
DEFAULT_DT = 60        # segundos.
DEFAULT_TOTAL_DAYS = 30

# Máximo de puntos que se guardan para las gráficas y la tabla. Guardar todos
# los pasos hace lenta la interfaz; la física sí corre en cada paso.
MAX_RECORDS = 2000

# Puntos que usa la animación de la órbita (menos puntos = más fluido).
ANIMATION_POINTS = 240

# Valores de un cuerpo nuevo (por defecto, separado de la Luna).
NEW_BODY = {
    "name": "Cuerpo",
    "mass": 7.342e22,
    "x": -3.844e8,
    "y": 0.0,
    "z": 0.0,
    "vx": 0.0,
    "vy": -1022.0,
    "vz": 0.0,
}

CAMPOS_POSICION = ("x", "y", "z")
CAMPOS_VELOCIDAD = ("vx", "vy", "vz")

# Tipos de trayectoria que ofrece el panel.
TRAJECTORY_TYPES = ("Circular", "Elíptica", "Parabólica", "Hiperbólica")

# Velocidad de cada tipo, en veces la velocidad circular.
# (la velocidad de escape es sqrt(2) veces la circular)
SPEED_FACTORS = {
    "Circular": 1.0,
    "Elíptica": 0.8,
    "Parabólica": math.sqrt(2),
    "Hiperbólica": 1.2 * math.sqrt(2),
}

# Límites del control de velocidad (en veces la velocidad circular).
SPEED_MIN = 0.5
SPEED_MAX = 2.0
SPEED_STEP = 0.05

# Excentricidad por debajo de la cual la órbita se presenta como circular.
# 0,02 es el umbral en que la elipse se ve redonda en la vista (justificación
# de la tarea A15: no es una igualdad física, es una etiqueta visual).
CIRCULAR_ECCENTRICITY = 0.02

# Energía específica relativa considerada cero para separar la parábola.
PARABOLIC_TOLERANCE = 1e-6

# Nombres que se muestran para cada escenario guardado.
SCENARIO_LABELS = {
    "tierra_luna": "Tierra y Luna",
    "sol_tierra": "Sol y Tierra",
    "sol_sistema_interno": "Sistema solar interno",
}

# Columnas de la tabla. Se muestran las tres componentes para representar el
# estado 3D completo (tarea A33).
TABLE_COLUMNS = [
    "Tiempo (días)", "x (m)", "y (m)", "z (m)",
    "vx (m/s)", "vy (m/s)", "vz (m/s)",
    "E total (J)", "L total (kg·m²/s)",
]

# Máximo de filas que se muestran en la tabla.
MAX_TABLE_ROWS = 40


def _short(value):
    """Da formato corto a un número grande (por ejemplo 5.972e+24)."""
    return f"{value:.4g}"


def _short_vector(vector):
    """Da formato corto a un vector de tres números."""
    return ", ".join(_short(componente) for componente in vector)


def _empty_figure(text, height=220):
    """Figura vacía con un mensaje, para los huecos del panel."""
    figure = go.Figure()
    figure.add_annotation(text=text, showarrow=False, font={"color": "#8fa3bf"})
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1626",
        plot_bgcolor="#0e1626",
        margin={"l": 40, "r": 20, "t": 30, "b": 30},
        height=height,
        xaxis={"visible": False},
        yaxis={"visible": False},
    )
    return figure


def _card(title, value):
    """Una tarjeta de resultado (título y valor)."""
    return html.Div(
        [html.Div(title, className="card-title"), html.Div(value, className="card-value")],
        className="card",
    )


def _status(message, kind="info"):
    """Área de estado visible y anunciada por lectores de pantalla (A34)."""
    return html.Div(message, className=f"status {kind}", role="status", **{"aria-live": "polite"})


def body_to_dict(body):
    """Convierte un cuerpo a un diccionario editable para el panel."""
    return {
        "name": body.name,
        "mass": body.mass,
        "x": float(body.position[0]),
        "y": float(body.position[1]),
        "z": float(body.position[2]),
        "vx": float(body.velocity[0]),
        "vy": float(body.velocity[1]),
        "vz": float(body.velocity[2]),
    }


def dict_to_body(data):
    """Crea un cuerpo a partir de los valores del panel."""
    return Body(
        data["name"],
        data["mass"],
        np.array([data["x"], data["y"], data["z"]], dtype=float),
        np.array([data["vx"], data["vy"], data["vz"]], dtype=float),
    )


def initial_bodies():
    """Cuerpos del escenario inicial, en la forma que usa el panel."""
    return [body_to_dict(body) for body in load_bodies(DEFAULT_PRESET)]


def add_body_to(bodies):
    """Devuelve la lista con un cuerpo nuevo al final."""
    return bodies + [copy.deepcopy(NEW_BODY)]


def remove_body_at(bodies, index):
    """Devuelve la lista sin el cuerpo de esa posición."""
    return [data for i, data in enumerate(bodies) if i != index]


def set_body_field(bodies, index, field, value):
    """Devuelve la lista con un campo de un cuerpo cambiado."""
    actualizados = copy.deepcopy(bodies)
    actualizados[index][field] = value
    return actualizados


def body_options(bodies):
    """Opciones del selector de cuerpo analizado.

    El número delante del nombre es la identidad estable: si dos cuerpos se
    llaman igual, el usuario sigue distinguiéndolos (tarea A18).
    """
    return [
        {"label": f"{index} · {data.get('name', 'Cuerpo')}", "value": index}
        for index, data in enumerate(bodies)
    ]


def analyzed_index(bodies, value):
    """Índice válido del cuerpo analizado dentro de la lista."""
    if not bodies:
        return 0
    if isinstance(value, int) and 0 <= value < len(bodies):
        return value
    return min(1, len(bodies) - 1)


def circular_speed(mass, distance, secondary_mass=0.0):
    """Velocidad circular con las dos masas: sqrt(G·(M+m)/r).

    Recibe:
        mass           : masa del cuerpo central (kg).
        distance       : distancia entre los dos (m).
        secondary_mass : masa del cuerpo que orbita (kg).
    Devuelve:
        La rapidez circular (m/s).
    """
    return float(np.sqrt(G * (mass + secondary_mass) / distance))


def trajectory_speed(kind, mass, distance, secondary_mass=0.0):
    """Velocidad del cuerpo que orbita según el tipo de trayectoria elegido.

    Recibe:
        kind           : "Circular", "Elíptica", "Parabólica" o "Hiperbólica".
        mass           : masa del cuerpo central (kg).
        distance       : distancia entre los dos cuerpos (m).
        secondary_mass : masa del cuerpo que orbita (kg).
    Devuelve:
        La rapidez inicial (m/s).
    """
    return SPEED_FACTORS.get(kind, 1.0) * circular_speed(mass, distance, secondary_mass)


def orbit_kind(factor):
    """Tipo de órbita según la rapidez, en veces la velocidad circular.

    Es una aproximación de la interfaz. La clasificación física se hace con
    `orbit_state`, que usa energía y excentricidad (tarea A15).
    """
    raiz_de_dos = math.sqrt(2)
    if abs(factor - 1.0) < 0.02:
        return "Circular"
    if factor < raiz_de_dos - 0.02:
        return "Elíptica"
    if abs(factor - raiz_de_dos) <= 0.02:
        return "Parabólica"
    return "Hiperbólica"


def _relative_state(primary, body):
    """Distancia, rapidez y dirección relativa entre dos cuerpos del panel."""
    r = np.array(
        [body["x"] - primary["x"], body["y"] - primary["y"], body["z"] - primary["z"]],
        dtype=float,
    )
    v = np.array(
        [body["vx"] - primary["vx"], body["vy"] - primary["vy"], body["vz"] - primary["vz"]],
        dtype=float,
    )
    return r, v


def orbit_state(bodies, index=1):
    """Clasifica la órbita del cuerpo `index` a partir del estado físico.

    Usa la energía específica del movimiento relativo y el vector de
    excentricidad e = (v × (r × v))/mu - r/|r|. No usa solo la rapidez.

    Recibe:
        bodies : lista de cuerpos del panel.
        index  : cuerpo analizado.
    Devuelve:
        Un diccionario con "kind", "eccentricity", "relative_energy",
        "distance", "speed", "factor" y "radial"; o None si no se puede medir.
    """
    if len(bodies) < 2 or index <= 0 or index >= len(bodies):
        return None

    primary, body = bodies[0], bodies[index]
    r, v = _relative_state(primary, body)
    distance = float(np.linalg.norm(r))
    speed = float(np.linalg.norm(v))
    if distance == 0:
        return None

    mu = G * (float(primary["mass"]) + float(body["mass"]))
    if mu <= 0:
        return None

    specific_energy = 0.5 * speed**2 - mu / distance
    scale = mu / distance
    relative_energy = specific_energy / scale if scale else 0.0

    h = np.cross(r, v)
    angular = float(np.linalg.norm(h))
    radial = angular < 1e-9 * max(distance * speed, 1.0)
    eccentricity = float(np.linalg.norm(np.cross(v, h) / mu - r / distance))

    if relative_energy < -PARABOLIC_TOLERANCE:
        kind = "Circular" if eccentricity < CIRCULAR_ECCENTRICITY else "Elíptica"
    elif relative_energy > PARABOLIC_TOLERANCE:
        kind = "Hiperbólica"
    else:
        kind = "Parabólica"

    return {
        "kind": kind,
        "eccentricity": eccentricity,
        "relative_energy": relative_energy,
        "distance": distance,
        "speed": speed,
        "factor": speed / circular_speed(primary["mass"], distance, body["mass"]),
        "radial": radial,
        "mu": mu,
    }


def _tangent_direction(r, velocity):
    """Dirección tangente a la posición relativa, estable en 3D.

    Si la velocidad actual ya tiene parte tangente, se conserva esa dirección
    (así una edición manual no cambia el sentido de giro). Si el movimiento es
    radial, se usa un eje auxiliar no paralelo a r.
    """
    distance = float(np.linalg.norm(r))
    if distance == 0:
        return None

    radius = r / distance
    tangent = velocity - np.dot(velocity, radius) * radius
    norm = float(np.linalg.norm(tangent))
    if norm > 0:
        return tangent / norm

    axis = np.array([0.0, 0.0, 1.0]) if abs(radius[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    candidate = np.cross(axis, radius)
    norm = float(np.linalg.norm(candidate))
    if norm == 0:
        return None
    return candidate / norm


def apply_speed(bodies, factor, index=1):
    """Pone la velocidad del cuerpo analizado en `factor` veces la circular.

    La velocidad queda perpendicular a la línea que une los dos cuerpos, en el
    plano que ya tenía el movimiento. Usa las tres dimensiones (tarea A14).

    Recibe:
        bodies : lista de cuerpos del panel.
        factor : velocidad, en veces la velocidad circular.
        index  : cuerpo que se ajusta (por defecto el primero que orbita).
    Devuelve:
        La lista de cuerpos, con la velocidad del cuerpo ajustada.
    """
    if len(bodies) < 2 or index <= 0 or index >= len(bodies):
        return bodies

    actualizados = copy.deepcopy(bodies)
    primario, cuerpo = actualizados[0], actualizados[index]
    r, v = _relative_state(primario, cuerpo)
    distance = float(np.linalg.norm(r))
    if distance == 0 or primario["mass"] <= 0:
        return bodies

    direction = _tangent_direction(r, v)
    if direction is None:
        return bodies

    rapidez = factor * circular_speed(primario["mass"], distance, cuerpo["mass"])
    cuerpo["vx"] = primario["vx"] + rapidez * float(direction[0])
    cuerpo["vy"] = primario["vy"] + rapidez * float(direction[1])
    cuerpo["vz"] = primario["vz"] + rapidez * float(direction[2])
    return actualizados


def apply_trajectory(bodies, kind, index=1):
    """Devuelve la lista con la velocidad del cuerpo según el tipo elegido."""
    return apply_speed(bodies, SPEED_FACTORS.get(kind, 1.0), index)


def velocities_text(bodies, index=1):
    """Texto con la velocidad circular, la de escape, la puesta y la clasificación.

    Recibe:
        bodies : lista de cuerpos del panel.
        index  : cuerpo analizado.
    Devuelve:
        El texto que explica el estado actual, en 3D.
    """
    if len(bodies) < 2:
        return "Agrega un cuerpo que orbite para ver las velocidades."

    state = orbit_state(bodies, index)
    if state is None:
        return "La distancia y la masa deben ser mayores que cero."

    primary = bodies[0]
    circular = circular_speed(primary["mass"], state["distance"], bodies[index]["mass"])
    escape = math.sqrt(2) * circular
    note = " Clasificación aproximada del par." if len(bodies) > 2 else ""
    radial = " Movimiento radial: no hay órbita circular." if state["radial"] else ""

    return (
        f"Distancia 3D: {state['distance']:,.0f} m · "
        f"v circular: {circular:,.0f} m/s · v escape: {escape:,.0f} m/s · "
        f"ahora: {state['speed']:,.0f} m/s ({state['factor']:.2f} × la circular, "
        f"{state['kind']}, e = {state['eccentricity']:.4f}).{radial}{note}"
    )


def _body_field(index, field, label, value, body_name, unit="", accessible=None):
    """Un campo editable de un cuerpo, con su etiqueta accesible.

    La etiqueta envuelve al campo: así el lector de pantalla lee el cuerpo, la
    magnitud y la unidad (tarea A40).

    Recibe:
        index     : número del cuerpo.
        field     : nombre interno del campo (x, y, z, vx, ...).
        label     : nombre visible de la magnitud (x, y, masa...).
        value     : valor actual.
        body_name : nombre del cuerpo, para la etiqueta accesible.
        unit      : unidad que se muestra (m, m/s, kg).
        accessible: nombre largo para el lector de pantalla (por ejemplo
                    "velocidad x"); si no se da, se usa `label`.
    """
    nombre_accesible = accessible or label
    accessible = f"{body_name}, {nombre_accesible}" + (f" en {unit}" if unit else "")
    return html.Label(
        [
            html.Span(accessible, className="sr-only"),
            html.Span(label + (f" ({unit})" if unit else ""), className="field-label"),
            dcc.Input(
                id={"type": "body-field", "index": index, "field": field},
                type="number",
                value=value,
                debounce=True,
                className="field-input",
            ),
        ],
        className="field",
    )


def _body_card(index, data):
    """Tarjeta editable de un cuerpo: nombre, masa, posición y velocidad."""
    encabezado = [
        html.Label(
            [
                html.Span(f"Nombre del cuerpo {index}", className="sr-only"),
                dcc.Input(
                    id={"type": "body-field", "index": index, "field": "name"},
                    type="text",
                    value=data["name"],
                    debounce=True,
                    className="name-input",
                ),
            ],
            className="name-label",
        ),
        html.Span("(Primario)" if index == 0 else "(Secundario)", className="body-role"),
    ]
    if index > 0:
        encabezado.append(
            html.Button(
                "Eliminar",
                id={"type": "remove-body", "index": index},
                className="remove",
                **{"aria-label": f"Eliminar el cuerpo {data['name']}"},
            )
        )

    return html.Div(
        [
            html.Div(encabezado, className="body-head"),
            _body_field(index, "mass", "Masa", data["mass"], data["name"], "kg"),
            html.Div("Posición inicial", className="group-title"),
            html.Div(
                [
                    _body_field(index, campo, campo, data[campo], data["name"], "m",
                                accessible=f"posición {campo}")
                    for campo in CAMPOS_POSICION
                ],
                className="triple",
            ),
            html.Div("Velocidad inicial", className="group-title"),
            html.Div(
                [
                    _body_field(index, campo, campo, data[campo], data["name"], "m/s",
                                accessible=f"velocidad {campo[1]}")
                    for campo in CAMPOS_VELOCIDAD
                ],
                className="triple",
            ),
        ],
        className="body-card",
    )


def _header():
    """Encabezado del panel."""
    return html.Div(
        [
            html.Div(
                [
                    html.H1("Simulador Orbital"),
                    html.P("Leyes de Kepler • Gravitación Universal"),
                ],
                className="titles",
            )
        ],
        className="header",
    )


def _config_panel():
    """Panel izquierdo: los pasos para configurar y correr la simulación."""
    return html.Div(
        [
            html.H2("Configuración de la Simulación"),
            html.Div(
                "Elige un escenario, revisa los cuerpos, elige el cálculo y pulsa "
                "Iniciar Simulación. Los resultados salen en el centro y a la derecha.",
                className="help",
            ),
            html.H3("1. Escenario de ejemplo"),
            html.Label("Escenario", htmlFor="scenario"),
            dcc.Dropdown(
                id="scenario",
                options=[
                    {"label": SCENARIO_LABELS.get(name, name), "value": name}
                    for name in preset_names()
                ],
                value=DEFAULT_PRESET,
                clearable=False,
                className="dropdown",
            ),
            html.H3("2. Tipo de órbita"),
            dcc.RadioItems(
                id="trajectory-type",
                options=[{"label": name, "value": name} for name in TRAJECTORY_TYPES],
                value=TRAJECTORY_TYPES[0],
                className="chips",
            ),
            html.Label("Velocidad (× la circular)", htmlFor="speed"),
            dcc.Slider(
                id="speed",
                min=SPEED_MIN,
                max=SPEED_MAX,
                step=SPEED_STEP,
                value=1.0,
                marks={SPEED_MIN: "0,5", 1.0: "1", round(math.sqrt(2), 2): "escape", SPEED_MAX: "2"},
            ),
            html.Div(id="velocities-text", className="hint"),
            html.H3("3. Cuerpos"),
            html.Div(
                "El primero es el centro. Puedes cambiar la masa, dónde está cada uno "
                "y con qué velocidad se mueve.",
                className="hint",
            ),
            html.Label("Cuerpo analizado", htmlFor="analyzed-body"),
            dcc.Dropdown(
                id="analyzed-body",
                options=body_options(initial_bodies()),
                value=1,
                clearable=False,
                className="dropdown",
            ),
            html.Button("+ Agregar cuerpo", id="add-body", className="ghost"),
            html.Div(id="bodies-list"),
            html.H3("4. Cálculo"),
            html.Label("Método", htmlFor="method"),
            dcc.Dropdown(
                id="method",
                options=[{"label": name, "value": name} for name in INTEGRATORS],
                value=DEFAULT_METHOD,
                clearable=False,
                className="dropdown",
            ),
            html.Label("Paso de tiempo (s)", htmlFor="dt"),
            dcc.Input(id="dt", type="number", value=DEFAULT_DT, min=1, className="wide"),
            html.Label("Duración (días)", htmlFor="total-days"),
            dcc.Input(id="total-days", type="number", value=DEFAULT_TOTAL_DAYS, min=1, className="wide"),
            html.Div("Un paso más pequeño es más preciso, pero tarda más.", className="hint"),
            html.Button("Iniciar Simulación", id="start", className="primary"),
        ],
        className="panel",
    )


def _center_panel():
    """Centro: estado, controles de la vista, vista, resultados, tabla y 1.ª ley."""
    return html.Div(
        [
            html.H2("Vista de la órbita"),
            html.Div(
                "Pulsa Iniciar Simulación y usa los botones de la gráfica para ver el "
                "movimiento. Mueve los controles para girar, inclinar o acercar.",
                className="hint",
            ),
            dcc.Graph(id="view3d", figure=_empty_figure("Pulsa Iniciar Simulación", height=360)),
            html.Div(
                [
                    html.Div(
                        [html.Label("Giro", htmlFor="azimuth"),
                         dcc.Slider(id="azimuth", min=0, max=360, step=5, value=35, updatemode="mouseup")],
                        className="control",
                    ),
                    html.Div(
                        [html.Label("Inclinación", htmlFor="elevation"),
                         dcc.Slider(id="elevation", min=-85, max=85, step=5, value=25, updatemode="mouseup")],
                        className="control",
                    ),
                    html.Div(
                        [html.Label("Acercamiento", htmlFor="zoom"),
                         dcc.Slider(id="zoom", min=0.5, max=3, step=0.1, value=1, updatemode="mouseup")],
                        className="control",
                    ),
                ],
                className="controls",
            ),
            html.Div(id="status"),
            html.H2("Resultados del cuerpo analizado"),
            html.Div(
                "Coordenadas absolutas del sistema (origen en 0,0,0). La trayectoria de "
                "la vista es relativa al primario.",
                className="hint",
            ),
            html.Div(id="results", className="cards"),
            html.H2("Datos del cuerpo analizado"),
            html.Div(
                "Una fila por intervalo de tiempo; tiempo y magnitudes en el sistema absoluto.",
                className="hint",
            ),
            dash_table.DataTable(
                id="table",
                columns=[{"name": columna, "id": columna} for columna in TABLE_COLUMNS],
                data=[],
                page_size=8,
                style_as_list_view=True,
                style_table={"overflowX": "auto"},
                style_header={"backgroundColor": "#16233a", "color": "#e6edf7", "fontWeight": "bold"},
                style_cell={"backgroundColor": "#0e1626", "color": "#c9d6e8", "border": "1px solid #1c2a44"},
                style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#111d31"}],
            ),
            html.H2("Primera ley de Kepler"),
            html.Div(id="first-law", className="hint"),
        ],
        className="panel center",
    )


def _plots_panel():
    """Derecha: las gráficas del análisis y la tercera ley explícita."""
    mensaje = "Pulsa Iniciar Simulación"
    return html.Div(
        [
            html.H2("Gráficas"),
            html.H3("Trayectoria"),
            dcc.Graph(id="plot-trajectory", figure=_empty_figure(mensaje)),
            html.H3("Energía Mecánica"),
            dcc.Graph(id="plot-energy", figure=_empty_figure(mensaje)),
            html.H3("Momento Angular"),
            dcc.Graph(id="plot-momentum", figure=_empty_figure(mensaje)),
            html.H3("Segunda ley (velocidad areal)"),
            dcc.Graph(id="plot-kepler", figure=_empty_figure(mensaje)),
            html.H3("Tercera ley"),
            html.Button("Analizar 3 órbitas", id="third-law", className="ghost"),
            html.Div(
                "Corre tres órbitas cortas alrededor del cuerpo central. No cambia la "
                "simulación que estás viendo.",
                className="hint",
            ),
            dcc.Graph(id="plot-third-law", figure=_empty_figure("Pulsa Analizar 3 órbitas")),
            html.Div(id="third-law-text", className="hint"),
        ],
        className="panel",
    )


def build_layout():
    """Arma el panel completo: izquierda, centro y derecha."""
    return html.Div(
        [
            dcc.Store(id="bodies-store", data=initial_bodies()),
            dcc.Store(id="history-store"),
            _header(),
            html.Div([_config_panel(), _center_panel(), _plots_panel()], className="grid"),
        ],
        className="app",
    )


def animation_from(history, names, count=ANIMATION_POINTS):
    """Toma una muestra del historial, para animar la órbita con pocos puntos.

    Recibe:
        history : historial completo de la corrida.
        names   : nombres de los cuerpos.
        count   : cuántos puntos quiere la animación.
    Devuelve:
        Un diccionario con "names", "positions" y "times", listo para el
        navegador. La primera y la última muestra siempre se conservan.
    """
    total = len(history["positions"])
    indices = sample_indices(total, count)

    return {
        "names": names,
        "positions": [
            [[float(c) for c in punto] for punto in history["positions"][i]] for i in indices
        ],
        "times": [float(history["time"][i]) for i in indices] if history.get("time") else [],
    }


def _history_for_store(history, names):
    """Versión del historial que se guarda en el navegador (solo listas)."""
    stored = {
        key: history[key]
        for key in ("time", "energy", "energy_kinetic", "energy_potential", "momentum")
    }
    stored["positions"] = [[[float(c) for c in punto] for punto in step] for step in history["positions"]]
    stored["velocities"] = [[[float(c) for c in punto] for punto in step] for step in history["velocities"]]
    stored["names"] = names
    stored["conservation"] = history["conservation"]
    stored["final_time"] = history["final_time"]
    stored["stopped"] = history["stopped"]
    return stored


def _index_from_history(history, value):
    """Índice válido del cuerpo analizado dentro de un historial guardado."""
    count = len(history["positions"][0]) if history.get("positions") else 0
    if isinstance(value, int) and 0 <= value < count:
        return value
    return min(1, count - 1) if count else 0


def results_cards(history, index=1):
    """Tarjetas de resultados del último instante del cuerpo analizado.

    Recibe:
        history : historial que devuelve `run_simulation`.
        index   : cuerpo analizado.
    Devuelve:
        Las cuatro tarjetas. E y L son totales del sistema (tarea A20).
    """
    index = _index_from_history(history, index)
    posicion = history["positions"][-1][index]
    velocidad = history["velocities"][-1][index]

    return [
        _card("Posición absoluta (m)", _short_vector(posicion)),
        _card("Velocidad absoluta (m/s)", _short_vector(velocidad)),
        _card("Energía mecánica total del sistema (J)", _short(history["energy"][-1])),
        _card("Momento angular total del sistema (kg·m²/s)", _short(history["momentum"][-1])),
    ]


def table_rows(history, index=1, max_rows=MAX_TABLE_ROWS):
    """Filas de la tabla, repartidas a lo largo de la corrida.

    Muestra como máximo `max_rows` filas y siempre incluye el primer y el último
    instante. El tiempo se guarda sin redondear (tarea A33).

    Recibe:
        history  : historial que devuelve `run_simulation`.
        index    : cuerpo analizado.
        max_rows : cuántas filas mostrar como máximo.
    Devuelve:
        La lista de filas para la tabla.
    """
    index = _index_from_history(history, index)
    total = len(history["time"])
    filas = []

    for i in sample_indices(total, max_rows):
        posicion = history["positions"][i][index]
        velocidad = history["velocities"][i][index]
        filas.append(
            {
                "Tiempo (días)": float(history["time"][i] / SEGUNDOS_POR_DIA),
                "x (m)": float(posicion[0]),
                "y (m)": float(posicion[1]),
                "z (m)": float(posicion[2]),
                "vx (m/s)": float(velocidad[0]),
                "vy (m/s)": float(velocidad[1]),
                "vz (m/s)": float(velocidad[2]),
                "E total (J)": float(history["energy"][i]),
                "L total (kg·m²/s)": float(history["momentum"][i]),
            }
        )
    return filas


def conservation_summary(history):
    """Texto con la peor variación de E y L durante toda la corrida (A21).

    Recibe:
        history : historial con "conservation".
    Devuelve:
        El texto para el área de estado.
    """
    conservation = history.get("conservation")
    if not conservation:
        return ""

    target = conservation["target_percent"]
    parts = []
    for name, data, unit in (
        ("Energía", conservation["energy"], "J"),
        ("Momento angular", conservation["momentum"], "kg·m²/s"),
    ):
        if data["max_percent"] is None:
            parts.append(
                f"{name}: no evaluable (referencia cero); error absoluto máximo "
                f"{data['max_absolute']:.4g} {unit}."
            )
        else:
            verdict = "cumple" if data["max_percent"] <= target else "no cumple"
            parts.append(
                f"{name}: variación máxima {data['max_percent']:.6g} % "
                f"(meta {target:g} %: {verdict})."
            )
    return " · ".join(parts)


def first_law_summary(history, index=1):
    """Texto de la primera ley para el cuerpo analizado (tarea A23)."""
    index = _index_from_history(history, index)
    if len(history["positions"]) < 5 or index == 0:
        return "Hacen falta más muestras y un cuerpo que orbite para comprobar la primera ley."

    relatives = [
        np.subtract(step[index], step[0]) for step in history["positions"]
    ]
    result = check_first_law(relatives)
    return result["message"]


def draw_panel(history, names, index, azimuth, elevation, zoom):
    """Arma las ocho salidas visuales a partir de un historial ya calculado."""
    return (
        results_cards(history, index),
        table_rows(history, index),
        figures.trajectory_figure(history, names),
        figures.energy_figure(history),
        figures.momentum_figure(history),
        figures.kepler_figure(history, index),
        figures.orbit_animation(history, names, azimuth=azimuth, elevation=elevation, zoom=zoom),
        _history_for_store(history, names),
        _status(
            "Cálculo terminado. " + conservation_summary(history)
            + (f" {history['stopped']['reason']}" if history.get("stopped") else ""),
            "warning" if history.get("stopped") else "ok",
        ),
        first_law_summary(history, index),
    )


def _empty_panel(message, kind="error"):
    """Salidas vacías con un estado que explica el motivo (tarea A34)."""
    vacio = _empty_figure("Corrige los datos y vuelve a iniciar")
    return (
        [], [],
        vacio, vacio, vacio, vacio,
        _empty_figure("Corrige los datos y vuelve a iniciar", height=360),
        None,
        _status(message, kind),
        "Sin datos: corrige la entrada y vuelve a iniciar.",
    )


def build_panel(stored_bodies, method, dt, total_days, azimuth, elevation, zoom, index=1):
    """Valida, corre la simulación y arma todo lo que se muestra en el panel.

    Recibe:
        stored_bodies : cuerpos del panel.
        method        : método numérico elegido.
        dt            : paso de tiempo (s).
        total_days    : duración (días).
        azimuth       : giro de la vista, en grados.
        elevation     : inclinación de la vista, en grados.
        zoom          : acercamiento de la vista.
        index         : cuerpo analizado.
    Devuelve:
        Las nueve salidas del panel. Si algo no sirve, devuelve salidas vacías y
        un estado con el motivo.
    Lanza:
        ValueError con el motivo cuando la entrada no es válida.
    """
    bodies_data = validate_bodies_data(stored_bodies)

    if len(bodies_data) < 2:
        raise ValueError(
            "Se necesitan al menos dos cuerpos para simular. "
            "Agrega un cuerpo que orbite alrededor del primario."
        )

    problems = overlapping_pairs(bodies_data)
    if problems:
        raise ValueError(overlap_message(problems))

    total_time = parse_positive(total_days, "La duración") * SEGUNDOS_POR_DIA
    step = parse_positive(dt, "El paso de tiempo")
    steps, last_step = step_plan(total_time, step)

    bodies = [dict_to_body(data) for data in bodies_data]
    names = [body.name for body in bodies]
    index = analyzed_index(bodies_data, index)

    # El motor corre con el último paso ya acortado, si hace falta, para que el
    # tiempo final sea exactamente la duración pedida.
    history = run_simulation(
        bodies, step, steps, method, max_records=MAX_RECORDS, last_step=last_step
    )

    return draw_panel(history, names, index, azimuth, elevation, zoom)


def _panel_error(exc):
    """Convierte un error en salidas vacías con explicación."""
    return _empty_panel(str(exc))


app = Dash(__name__, assets_folder=str(ROOT / "assets"))
app.title = "Simulador Orbital"
# Las tarjetas de los cuerpos las crea un callback, así que sus campos no están
# en el layout inicial.
app.config.suppress_callback_exceptions = True
app.layout = build_layout()


@app.server.after_request
def _sin_copias(response):
    """Pide al navegador que no guarde copias de las respuestas."""
    response.headers["Cache-Control"] = "no-store"
    return response


@app.callback(Output("bodies-list", "children"), Input("bodies-store", "data"))
def render_bodies(bodies):
    """Dibuja una tarjeta editable por cada cuerpo."""
    return [_body_card(index, data) for index, data in enumerate(bodies)]


@app.callback(
    Output("bodies-store", "data"),
    Input("add-body", "n_clicks"),
    Input({"type": "remove-body", "index": ALL}, "n_clicks"),
    Input({"type": "body-field", "index": ALL, "field": ALL}, "value"),
    Input("speed", "value"),
    Input("scenario", "value"),
    Input("trajectory-type", "value"),
    State("bodies-store", "data"),
    State("analyzed-body", "value"),
    prevent_initial_call=True,
)
def update_bodies(add_clicks, remove_clicks, field_values, speed, scenario, kind,
                  bodies, selected):
    """Mantiene la lista de cuerpos: escenario, tipo, velocidad, agregar o cambiar.

    Es la única fuente de verdad: de aquí salen los cuerpos que usan los demás
    controles y la simulación.
    """
    triggered = callback_context.triggered_id

    if triggered == "add-body":
        return add_body_to(bodies)

    if triggered == "scenario":
        return [body_to_dict(body) for body in load_bodies(scenario)]

    index = analyzed_index(bodies, selected)

    if triggered == "trajectory-type":
        # Si la lista ya está en ese tipo, no se toca: evita que la
        # sincronización de los controles vuelva a escribir una velocidad
        # manual (tareas A16 y A17).
        state = orbit_state(bodies, index)
        if state is not None and state["kind"] == kind:
            return no_update
        return apply_trajectory(bodies, kind, index)

    if triggered == "speed" and speed is not None:
        state = orbit_state(bodies, index)
        if state is not None and abs(state["factor"] - speed) <= 1e-6:
            return no_update
        return apply_speed(bodies, speed, index)

    if isinstance(triggered, dict) and triggered.get("type") == "remove-body":
        return remove_body_at(bodies, triggered["index"])

    if isinstance(triggered, dict) and triggered.get("type") == "body-field":
        index = triggered["index"]
        field = triggered["field"]
        valor = callback_context.triggered[0]["value"]
        if bodies[index][field] == valor:
            return no_update
        return set_body_field(bodies, index, field, valor)

    return no_update


@app.callback(
    Output("trajectory-type", "value"),
    Input("bodies-store", "data"),
    State("trajectory-type", "value"),
)
def sync_type(bodies, current):
    """Muestra el tipo que resulta de las velocidades reales.

    Es una lectura, no una orden: solo cambia la etiqueta marcada.
    """
    state = orbit_state(bodies, analyzed_index(bodies, 1))
    if state is None or state["kind"] == current:
        return no_update
    return state["kind"]


@app.callback(
    Output("speed", "value"),
    Input("bodies-store", "data"),
    State("speed", "value"),
)
def sync_speed(bodies, current):
    """Muestra la rapidez real del cuerpo como veces la circular.

    No reescribe velocidades: si el valor ya coincide, no hace nada.
    """
    state = orbit_state(bodies, analyzed_index(bodies, 1))
    if state is None:
        return no_update
    factor = min(SPEED_MAX, max(SPEED_MIN, state["factor"]))
    if current is not None and abs(current - factor) <= 1e-6:
        return no_update
    return factor


@app.callback(
    Output("analyzed-body", "options"),
    Output("analyzed-body", "value"),
    Input("bodies-store", "data"),
    State("analyzed-body", "value"),
)
def sync_analyzed_body(bodies, current):
    """Mantiene el selector de cuerpo con una identidad estable (A18)."""
    return body_options(bodies), analyzed_index(bodies, current)


@app.callback(
    Output("velocities-text", "children"),
    Input("bodies-store", "data"),
    Input("analyzed-body", "value"),
)
def show_velocities(bodies, index):
    """Muestra las velocidades y la clasificación del cuerpo analizado."""
    return velocities_text(bodies, analyzed_index(bodies, index))


@app.callback(
    Output("results", "children"),
    Output("table", "data"),
    Output("plot-trajectory", "figure"),
    Output("plot-energy", "figure"),
    Output("plot-momentum", "figure"),
    Output("plot-kepler", "figure"),
    Output("view3d", "figure"),
    Output("history-store", "data"),
    Output("status", "children"),
    Output("first-law", "children"),
    Input("start", "n_clicks"),
    Input("azimuth", "value"),
    Input("elevation", "value"),
    Input("zoom", "value"),
    Input("analyzed-body", "value"),
    State("method", "value"),
    State("dt", "value"),
    State("total-days", "value"),
    State("bodies-store", "data"),
    State("history-store", "data"),
    prevent_initial_call=True,
    running=[(Output("start", "disabled"), True, False)],
)
def update_panel(start_clicks, azimuth, elevation, zoom, selected, method, dt,
                 total_days, stored_bodies, stored_history):
    """Corre la simulación, o solo rehace la vista si se movió un control."""
    vista_giro = azimuth if azimuth is not None else 35.0
    vista_inclinacion = elevation if elevation is not None else 25.0
    vista_zoom = zoom if zoom is not None else 1.0
    triggered = callback_context.triggered_id

    if triggered != "start":
        if not stored_history:
            return (no_update,) * 10

        if triggered == "analyzed-body":
            index = _index_from_history(stored_history, selected)
            return (
                results_cards(stored_history, index),
                table_rows(stored_history, index),
                no_update,
                no_update,
                no_update,
                figures.kepler_figure(stored_history, index),
                no_update,
                no_update,
                _status(
                    "Cálculo terminado. " + conservation_summary(stored_history)
                    + (f" {stored_history['stopped']['reason']}" if stored_history.get("stopped") else ""),
                    "warning" if stored_history.get("stopped") else "ok",
                ),
                first_law_summary(stored_history, index),
            )

        figura = figures.orbit_animation(
            {"positions": stored_history["positions"], "time": stored_history["time"]},
            stored_history["names"],
            azimuth=vista_giro,
            elevation=vista_inclinacion,
            zoom=vista_zoom,
        )
        return (no_update,) * 6 + (figura,) + (no_update,) * 3

    try:
        return build_panel(stored_bodies, method, dt, total_days, vista_giro,
                           vista_inclinacion, vista_zoom, selected)
    except ValueError as exc:
        logging.warning("Entrada rechazada: %s", exc)
        return _panel_error(str(exc))
    except Exception:
        logging.exception("Fallo inesperado al calcular el panel")
        return _panel_error(
            "Ocurrió un error inesperado al calcular. Revisa los datos y vuelve a "
            "iniciar; el detalle técnico quedó en el registro del servidor."
        )


@app.callback(
    Output("plot-third-law", "figure"),
    Output("third-law-text", "children"),
    Input("third-law", "n_clicks"),
    State("bodies-store", "data"),
    State("analyzed-body", "value"),
    prevent_initial_call=True,
)
def analyze_third_law(clicks, bodies, index):
    """Corre tres órbitas cortas y muestra T² frente a a³ (tarea A27)."""
    if not clicks:
        return no_update, no_update

    try:
        data = validate_bodies_data(bodies)
        position = analyzed_index(data, index)
        if position == 0:
            raise ValueError("Elige un cuerpo que orbite: el primario no sirve para medir órbitas.")

        primary = data[0]
        secondary = data[position]
        r, v = _relative_state(primary, secondary)
        distance = float(np.linalg.norm(r))
        if distance == 0:
            raise ValueError("El cuerpo analizado está en el centro: sepáralo para medir órbitas.")

        result = third_law_analysis(
            float(primary["mass"]), float(secondary["mass"]), distance
        )
    except ValueError as exc:
        return _empty_figure(str(exc)), str(exc)
    except Exception:
        logging.exception("Fallo al analizar la tercera ley")
        return (
            _empty_figure("No se pudo completar el análisis"),
            "Ocurrió un error inesperado; el detalle quedó en el registro del servidor.",
        )

    return figures.third_law_figure(result["orbits"]), result["message"]


if __name__ == "__main__":
    app.run(debug=False)
