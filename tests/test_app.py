# código nuevo edizon
"""test_app.py — Pruebas de la interfaz.

¿Para qué sirve?
    Comprobar el panel, las tarjetas, la tabla, el selector del cuerpo analizado,
    la clasificación física, la animación y el estado visible.

¿Por qué existe?
    La interfaz es la parte visible; si no arma o no muestra datos, el proyecto no
    sirve aunque la física esté bien. Cubre las tareas A02, A03, A14, A15, A16,
    A18, A19, A20, A23, A31, A33, A34 y A40 del plan de corrección.

¿Cómo ejecutarlo?
    pytest tests/test_app.py

¿Cómo modificarlo?
    Añadir comprobaciones nuevas si se agregan secciones al panel.
"""

import math

import numpy as np
import pytest

from src.physics.bodies import Body
from src.simulation import load_bodies, run_simulation
from src.ui.app import (
    analyzed_index,
    animation_from,
    apply_speed,
    body_options,
    build_layout,
    build_panel,
    circular_speed,
    initial_bodies,
    orbit_state,
    results_cards,
    table_rows,
    velocities_text,
)
from src.ui.figures import orbit_animation


def test_el_panel_trae_las_zonas_del_boceto():
    """El panel arma configuración, vista, resultados, tabla y gráficas."""
    texto = str(build_layout())

    assert "Configuración de la Simulación" in texto
    assert "Vista de la órbita" in texto
    assert "Resultados del cuerpo analizado" in texto
    assert "Datos del cuerpo analizado" in texto
    assert "Gráficas" in texto
    assert "Primera ley de Kepler" in texto


def test_el_panel_guiia_por_pasos():
    """El panel muestra los cuatro pasos y el botón de iniciar."""
    texto = str(build_layout())

    assert "1. Escenario de ejemplo" in texto
    assert "2. Tipo de órbita" in texto
    assert "3. Cuerpos" in texto
    assert "4. Cálculo" in texto
    assert "Iniciar Simulación" in texto


def test_los_escenarios_guardados_tienen_nombre():
    """El motor lista los escenarios guardados."""
    from src.simulation import preset_names

    nombres = preset_names()

    assert "tierra_luna" in nombres
    assert "sol_tierra" in nombres


def test_elegir_escenario_carga_sus_cuerpos():
    """Elegir otro escenario trae los cuerpos de ese preset."""
    from src.ui.app import body_to_dict

    cuerpos = [body_to_dict(body) for body in load_bodies("sol_tierra")]

    assert [cuerpo["name"] for cuerpo in cuerpos] == ["Sol", "Tierra"]


def test_las_tarjetas_y_la_tabla_se_llenan():
    """Con una corrida real, las tarjetas y la tabla traen datos."""
    history = run_simulation(load_bodies("tierra_luna"), 60, 100, "Verlet")

    tarjetas = results_cards(history, 1)
    filas = table_rows(history, 1)

    assert len(tarjetas) == 4
    assert filas
    assert "Tiempo (días)" in filas[0]
    assert filas[0]["E total (J)"] != 0.0


def test_la_vista_de_la_orbita_no_usa_webgl():
    """La vista se dibuja sin WebGL: no hay trazas 3D."""
    from plotly.graph_objects import Scatter3d

    from src.ui.figures import orbit_figure

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet")
    figura = orbit_figure(history, ["Tierra", "Luna"])

    assert all(not isinstance(trace, Scatter3d) for trace in figura.data)


def test_la_vista_trae_ejes_estrellas_orbita_y_cuerpos():
    """La vista trae ejes, estrellas, la órbita y los cuerpos como esferas."""
    from src.ui.figures import orbit_figure

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet")
    figura = orbit_figure(history, ["Tierra", "Luna"])
    nombres = [trace.name for trace in figura.data]

    assert "eje x" in nombres
    assert "eje y" in nombres
    assert "eje z" in nombres
    assert "estrellas" in nombres
    assert "Tierra" in nombres
    assert "Órbita: Luna" in nombres
    assert len(figura.layout.images) == 0


def test_el_brillo_queda_en_la_misma_posicion_que_el_cuerpo():
    """El brillo ya no se desplaza una fracción de la órbita (tarea A30)."""
    from src.ui.figures import _body_traces

    trazas = _body_traces("Luna", 12.0, 34.0, 100.0, "#ffffff")
    brillo = trazas[2]

    assert list(brillo.x) == [12.0]
    assert list(brillo.y) == [34.0]


def test_la_vista_mantiene_el_acercamiento_entre_cuadros():
    """La vista conserva el giro y el acercamiento del usuario."""
    from src.ui.figures import orbit_figure

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet")

    assert orbit_figure(history, ["Tierra", "Luna"]).layout.uirevision == "orbita"


def test_la_animacion_dibuja_solo_el_recorrido_recorrido():
    """El cuadro de la animación corta el recorrido en el punto actual."""
    from src.ui.figures import orbit_frame

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet", record_every=10)
    figura = orbit_frame(history, ["Tierra", "Luna"], 5)
    recorrido = [trace for trace in figura.data if trace.name == "Órbita: Luna"][0]

    assert len(recorrido.x) == 6


def test_la_animacion_trae_cuadros_y_tres_botones():
    """La vista animada trae cuadros y los botones de reproducir, pausar y reiniciar."""
    from plotly.graph_objects import Scatter3d

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet", record_every=10)
    figura = orbit_animation(history, ["Tierra", "Luna"], frames=10)

    assert len(figura.frames) >= 10
    assert figura.frames[-1].name == str(len(history["positions"]) - 1)
    assert [boton.label for boton in figura.layout.updatemenus[0].buttons] == [
        "Reproducir", "Pausar", "Reiniciar"
    ]
    assert figura.layout.uirevision == "orbita"
    assert all(not isinstance(trace, Scatter3d) for trace in figura.data)


def test_la_animacion_conserva_la_primera_y_la_ultima_muestra():
    """Para cualquier cantidad de registros, los extremos no se pierden (A31)."""
    for total in (100, 241, 1000, 2058):
        history = {
            "positions": [[[float(i), 0.0, 0.0]] for i in range(total)],
            "time": [float(i) for i in range(total)],
        }
        muestra = animation_from(history, ["Cuerpo"], count=240)

        assert muestra["positions"][0] == [[0.0, 0.0, 0.0]]
        assert muestra["positions"][-1] == [[float(total - 1), 0.0, 0.0]]
        assert muestra["times"][-1] == float(total - 1)


def test_las_graficas_del_analisis_se_construyen():
    """Las cuatro gráficas del boceto se construyen con el historial."""
    from src.ui.figures import energy_figure, kepler_figure, momentum_figure, trajectory_figure

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet", record_every=10)
    names = ["Tierra", "Luna"]

    assert len(trajectory_figure(history, names).data) == 3
    assert len(energy_figure(history).data) == 3
    assert len(momentum_figure(history).data) == 1
    assert kepler_figure(history, 1).data


def test_la_segunda_ley_no_falla_con_una_sola_muestra():
    """Una corrida de un solo paso muestra un aviso, no un IndexError (A04)."""
    from src.ui.figures import kepler_figure

    history = run_simulation(load_bodies("tierra_luna"), 60.0, 1)

    assert kepler_figure(history, 1).layout.annotations


def test_el_panel_permite_editar_y_agregar_cuerpos():
    """El panel trae el botón de agregar y los campos de cada cuerpo."""
    from src.ui.app import NEW_BODY, _body_card

    assert "Agregar cuerpo" in str(build_layout())

    tarjeta = str(_body_card(1, NEW_BODY))
    assert "Masa" in tarjeta
    assert "Velocidad inicial" in tarjeta
    assert "Eliminar" in tarjeta


def test_cada_campo_tiene_etiqueta_con_cuerpo_y_unidad():
    """La etiqueta accesible distingue cuerpo, magnitud y unidad (tarea A40)."""
    from src.ui.app import _body_card

    tarjeta = str(_body_card(1, {"name": "Luna", "mass": 1.0, "x": 2.0, "y": 3.0,
                                 "z": 4.0, "vx": 5.0, "vy": 6.0, "vz": 7.0}))

    assert "Luna, posición x en m" in tarjeta
    assert "Luna, velocidad x en m/s" in tarjeta
    assert "Nombre del cuerpo 1" in tarjeta


def test_los_cuerpos_del_panel_van_y_vuelven():
    """Un cuerpo se convierte a la forma del panel y regresa igual."""
    from src.ui.app import body_to_dict, dict_to_body

    original = Body("Cuerpo", 1.5e22, np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0]))
    copia = dict_to_body(body_to_dict(original))

    assert copia.name == original.name
    assert copia.mass == original.mass
    assert np.array_equal(copia.position, original.position)
    assert np.array_equal(copia.velocity, original.velocity)


def test_iniciar_usa_los_cuerpos_del_panel():
    """La simulación corre con los cuerpos y los parámetros del panel."""
    salidas = build_panel(initial_bodies(), "Verlet", 60, 2, 35, 25, 1.0, 1)

    assert len(salidas) == 10
    assert salidas[0]  # tarjetas.
    assert salidas[1]  # filas.
    assert salidas[6]  # vista animada.
    assert salidas[7]  # historial guardado.
    assert "Cálculo terminado" in salidas[8].children
    assert "elipse" in salidas[9] or "Elipse" in salidas[9] or "vuelta" in salidas[9]


def test_el_panel_rechaza_un_solo_cuerpo():
    """Sin secundario se explica el motivo y no se integra (tarea A03)."""
    with pytest.raises(ValueError, match="al menos dos"):
        build_panel(initial_bodies()[:1], "Verlet", 60, 1, 35, 25, 1)


def test_el_panel_rechaza_dt_invalido():
    """Un dt de cero no vacía el panel en silencio: se explica (tarea A34)."""
    with pytest.raises(ValueError, match="paso de tiempo"):
        build_panel(initial_bodies(), "Verlet", 0, 2, 35, 25, 1.0)


def test_el_panel_rechaza_masa_vacia_y_negativa():
    """La masa vacía o negativa se rechaza con el campo identificado (A02)."""
    from src.ui.app import set_body_field

    with pytest.raises(ValueError, match="masa está vacío"):
        build_panel(set_body_field(initial_bodies(), 1, "mass", None),
                    "Verlet", 60, 1, 35, 25, 1)

    with pytest.raises(ValueError, match="mayor que cero"):
        build_panel(set_body_field(initial_bodies(), 1, "mass", -5),
                    "Verlet", 60, 1, 35, 25, 1)


def test_el_panel_rechaza_cuerpos_superpuestos():
    """Dos cuerpos en el mismo punto se rechazan nombrando el par (A05)."""
    from src.ui.app import add_body_to, set_body_field

    superpuesto = set_body_field(add_body_to(initial_bodies()), 2, "x", 3.844e8)

    with pytest.raises(ValueError, match="Luna"):
        build_panel(superpuesto, "Verlet", 60, 1, 35, 25, 1)


def test_agregar_eliminar_y_editar_cuerpos():
    """Las tres operaciones del panel cambian la lista como se espera."""
    from src.ui.app import add_body_to, remove_body_at, set_body_field

    base = initial_bodies()
    assert len(base) == 2

    crecidos = add_body_to(base)
    assert len(crecidos) == 3
    assert len(base) == 2

    menos = remove_body_at(crecidos, 1)
    assert len(menos) == 2
    assert menos[0]["name"] == base[0]["name"]

    cambiados = set_body_field(base, 1, "mass", 1.0e23)
    assert cambiados[1]["mass"] == 1.0e23
    assert base[1]["mass"] != 1.0e23


def test_las_velocidades_por_tipo_de_trayectoria():
    """Cada tipo de trayectoria usa la velocidad que le toca, con las dos masas."""
    from src.physics.gravity import escape_velocity
    from src.ui.app import apply_trajectory, trajectory_speed

    masa = 5.972e24
    distancia = 3.844e8
    secundaria = 7.342e22
    v_circular = circular_speed(masa, distancia, secundaria)

    assert np.isclose(trajectory_speed("Circular", masa, distancia, secundaria), v_circular)
    assert np.isclose(trajectory_speed("Elíptica", masa, distancia, secundaria), 0.8 * v_circular)
    assert np.isclose(
        trajectory_speed("Parabólica", masa, distancia, secundaria), math.sqrt(2) * v_circular
    )
    assert np.isclose(
        trajectory_speed("Hiperbólica", masa, distancia, secundaria),
        1.2 * escape_velocity(masa + secundaria, distancia),
        rtol=1e-6,
    )

    cuerpo = apply_trajectory(initial_bodies(), "Circular")[1]
    rapidez = (cuerpo["vx"] ** 2 + cuerpo["vy"] ** 2 + cuerpo["vz"] ** 2) ** 0.5
    assert np.isclose(rapidez, v_circular, rtol=1e-6)


def test_la_velocidad_circular_usa_las_dos_masas():
    """Con masas iguales, mu = G·(M+m) duplica la velocidad circular (A13)."""
    sola = circular_speed(1e24, 1e8)
    doble = circular_speed(1e24, 1e8, 1e24)

    assert np.isclose(doble, sola * math.sqrt(2))


def test_el_tipo_de_orbita_sale_de_la_velocidad():
    """La aproximación por rapidez sigue disponible."""
    from src.ui.app import orbit_kind

    assert orbit_kind(1.0) == "Circular"
    assert orbit_kind(0.8) == "Elíptica"
    assert orbit_kind(1.2) == "Elíptica"
    assert orbit_kind(1.4142) == "Parabólica"
    assert orbit_kind(1.8) == "Hiperbólica"


def test_la_clasificacion_usa_energia_y_excentricidad():
    """Circular, elíptica, parabólica e hiperbólica se distinguen por el estado."""
    base = initial_bodies()
    tipos = {}

    for kind, factor in (("Circular", 1.0), ("Elíptica", 0.8), ("Parabólica", math.sqrt(2)),
                         ("Hiperbólica", 1.6)):
        ajustados = apply_speed(base, factor, 1)
        tipos[kind] = orbit_state(ajustados, 1)["kind"]

    assert tipos == {"Circular": "Circular", "Elíptica": "Elíptica",
                     "Parabólica": "Parabólica", "Hiperbólica": "Hiperbólica"}


def test_una_velocidad_radial_no_se_llama_circular():
    """Una velocidad radial con la rapidez circular no es una órbita circular (A15)."""
    base = initial_bodies()
    radial = base[:]
    radial[1] = dict(radial[1])
    radial[1]["vx"] = circular_speed(base[0]["mass"], 3.844e8, base[1]["mass"])
    radial[1]["vy"] = 0.0

    estado = orbit_state(radial, 1)

    assert estado["radial"] is True
    assert estado["kind"] != "Circular"


def test_las_velocidades_usan_las_tres_dimensiones():
    """Un cuerpo sobre el eje z recibe una velocidad tangente válida (A14)."""
    base = initial_bodies()
    sobre_z = [base[0], dict(base[1], x=0.0, y=0.0, z=3.844e8, vx=0.0, vy=0.0, vz=0.0)]

    ajustado = apply_speed(sobre_z, 1.0, 1)
    estado = orbit_state(ajustado, 1)

    assert math.isfinite(estado["speed"])
    assert np.isclose(estado["speed"], circular_speed(base[0]["mass"], 3.844e8, base[1]["mass"]))
    assert estado["radial"] is False


def test_el_texto_muestra_distancia_velocidad_y_clasificacion():
    """El texto del panel explica el estado actual con sus unidades."""
    texto = velocities_text(initial_bodies(), 1)

    assert "Distancia 3D" in texto
    assert "v circular" in texto
    assert "v escape" in texto
    assert "× la circular" in texto
    assert "Circular" in texto


def test_el_selector_de_cuerpo_usa_identidad_estable():
    """Dos cuerpos con el mismo nombre se distinguen por su número (A18)."""
    bodies = [{"name": "Tierra"}, {"name": "Igual"}, {"name": "Igual"}]
    opciones = body_options(bodies)

    assert [opcion["label"] for opcion in opciones] == ["0 · Tierra", "1 · Igual", "2 · Igual"]
    assert analyzed_index(bodies, 2) == 2
    assert analyzed_index(bodies, 99) == 1
    assert analyzed_index([], None) == 0


def test_las_vistas_de_detalle_usan_el_mismo_cuerpo():
    """Tarjetas y tabla muestran el cuerpo elegido, no el último (A18)."""
    bodies = load_bodies("sol_sistema_interno")
    history = run_simulation(bodies, 600.0, 50, "Verlet", record_every=10)

    tarjetas = str(results_cards(history, 2))
    fila = table_rows(history, 2)[-1]

    assert f"{float(history['positions'][-1][2][0]):.4g}" in tarjetas
    assert fila["x (m)"] == float(history["positions"][-1][2][0])


def test_la_tabla_respeta_el_maximo_y_los_extremos():
    """La tabla nunca pasa de 40 filas e incluye el último instante (A33)."""
    history = run_simulation(load_bodies("tierra_luna"), 60.0, 200, "Verlet")

    for limite in (1, 39, 40, 41):
        filas = table_rows(history, 1, max_rows=limite)
        assert len(filas) <= limite

    filas = table_rows(history, 1)
    assert len(filas) <= 40
    assert filas[0]["Tiempo (días)"] == 0.0
    assert filas[-1]["Tiempo (días)"] == pytest.approx(history["time"][-1] / 86400)
    assert filas[-1]["E total (J)"] == history["energy"][-1]


def test_la_tabla_no_confunde_instantes_por_redondeo():
    """Los tiempos se guardan sin redondear; dos instantes distintos siguen distintos."""
    history = run_simulation(load_bodies("tierra_luna"), 1.0, 100, "Verlet")
    filas = table_rows(history, 1, max_rows=40)

    tiempos = [fila["Tiempo (días)"] for fila in filas]
    assert len(set(tiempos)) == len(tiempos)


def test_el_estilo_se_adapta_a_pantallas_pequenas():
    """El estilo trae reglas para pantallas medianas y pequeñas (Tarea 14)."""
    from src.config import project_root

    estilo = (project_root() / "assets" / "style.css").read_text(encoding="utf-8")

    assert "@media" in estilo
    assert "grid-template-columns: 1fr" in estilo


def test_las_tarjetas_y_la_tabla_coinciden_con_las_graficas():
    """Todo sale del mismo historial: los números tienen que coincidir."""
    from src.ui.figures import energy_figure, momentum_figure

    history = run_simulation(load_bodies("tierra_luna"), 60, 200, "Verlet", record_every=10)

    filas = table_rows(history, 1)
    energia = energy_figure(history)
    momento = momentum_figure(history)

    assert filas[0]["Tiempo (días)"] == 0.0
    assert filas[0]["E total (J)"] == history["energy"][0]
    assert energia.data[0].y[0] == history["energy"][0]
    assert energia.data[1].y[0] == history["energy_kinetic"][0]
    assert energia.data[2].y[0] == history["energy_potential"][0]
    assert momento.data[0].y[0] == history["momentum"][0]

    tarjetas = str(results_cards(history, 1))
    assert f"{history['energy'][-1]:.4g}" in tarjetas
    assert f"{float(history['positions'][-1][1][0]):.4g}" in tarjetas
