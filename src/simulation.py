# código nuevo edizon
"""simulation.py — Motor de la simulación.

¿Para qué sirve?
    Correr el loop de física: avanzar el estado con el integrador elegido y
    guardar el historial (tiempo, energía, momento angular y posiciones).

¿Por qué existe?
    Separa el motor de la interfaz. La interfaz solo pide una corrida y recibe el
    historial; no sabe de integradores ni de ecuaciones. Aquí también se revisan
    los parámetros de entrada y se mide la conservación en cada paso (tareas A07,
    A09, A10 y A21).

¿Qué contiene?
    - `preset_names()` : los nombres de los escenarios guardados.
    - `load_bodies(preset_name)` : construye los cuerpos desde un preset.
    - `INTEGRATORS` : los métodos numéricos disponibles, por nombre.
    - `total_steps(total_time, dt)` : cuántos pasos caben en un tiempo total.
    - `step_plan(total_time, dt)` : pasos y tamaño del último paso.
    - `sample_indices(total, max_count)` : índices repartidos, con extremos.
    - `run_simulation(bodies, dt, steps, method)` : corre y devuelve el historial.

Política de duración
    Si la duración no es múltiplo de `dt`, el último paso se acorta para que el
    tiempo final sea exactamente el pedido. Nunca se redondea en silencio.

Límite de trabajo
    Una solicitud que pida demasiados pasos o demasiados pares se rechaza antes
    de empezar, con el costo calculado y alternativas.

¿Cómo modificarlo?
    - Añadir un método numérico: nuevo archivo en `integrators/` y una línea en
      `INTEGRATORS`.
    - Cambiar el presupuesto: `MAX_WORK` y `MAX_STEPS`.
"""

import json
import math

import numpy as np

from src.config import project_root
from src.integrators.euler_cromer import step as euler_cromer_step
from src.integrators.verlet import step as verlet_step
from src.physics.bodies import Body
from src.physics.conservation import CONSERVATION_TARGET_PERCENT
from src.physics.gravity import G, MIN_DISTANCE
from src.physics.validation import validate_body_objects

# Archivo con los escenarios guardados.
PRESETS_FILE = project_root() / "data" / "presets.json"

# Métodos numéricos disponibles, por nombre.
INTEGRATORS = {
    "Euler-Cromer": euler_cromer_step,
    "Verlet": verlet_step,
}

# Presupuesto de trabajo por solicitud: pasos × pares de cuerpos.
MAX_WORK = 20_000_000

# Tope absoluto de pasos, aunque haya un solo par.
MAX_STEPS = 2_000_000


def preset_names(presets_file=PRESETS_FILE):
    """Nombres de los escenarios guardados en `presets.json`.

    Recibe:
        presets_file : ruta del archivo de presets.
    Devuelve:
        La lista de nombres, en el orden del archivo.
    """
    with open(presets_file, encoding="utf-8") as file:
        data = json.load(file)

    return [preset["nombre"] for preset in data["presets"]]


def load_bodies(preset_name, presets_file=PRESETS_FILE):
    """Crea la lista de cuerpos a partir de un preset.

    Recibe:
        preset_name  : nombre del preset dentro de `presets.json`.
        presets_file : ruta del archivo de presets.
    Devuelve:
        La lista de cuerpos, con posición y velocidad como arreglos de NumPy.
    """
    with open(presets_file, encoding="utf-8") as file:
        data = json.load(file)

    preset = next(p for p in data["presets"] if p["nombre"] == preset_name)

    return [
        Body(
            body["name"],
            body["mass"],
            np.array(body["position"], dtype=float),
            np.array(body["velocity"], dtype=float),
        )
        for body in preset["cuerpos"]
    ]


def parse_positive(value, name):
    """Convierte un valor a número finito y mayor que cero.

    Recibe:
        value : valor tal como llega (texto, None o número).
        name  : nombre del parámetro para el mensaje.
    Devuelve:
        El número como `float`.
    Lanza:
        ValueError si no es un número finito y positivo.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValueError(f"{name} está vacío.")

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} debe ser un número; llegó {value!r}.") from None

    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} debe ser un número finito y mayor que cero.")

    return number


def total_steps(total_time, dt):
    """Cuántos pasos hacen falta para cubrir `total_time`.

    Si la duración no es múltiplo de `dt`, se usa un último paso más corto, así
    que el número de pasos se redondea hacia arriba (tarea A04).

    Recibe:
        total_time : duración total (s).
        dt         : paso de tiempo (s).
    Devuelve:
        El número de pasos (entero, al menos 1).
    """
    total = parse_positive(total_time, "La duración")
    step = parse_positive(dt, "El paso de tiempo")

    return max(1, int(math.ceil(total / step)))


def step_plan(total_time, dt):
    """Pasos y tamaño del último paso para integrar exactamente la duración.

    Recibe:
        total_time : duración total (s).
        dt         : paso de tiempo (s).
    Devuelve:
        Una tupla (steps, last_dt). `last_dt` es `dt` cuando la duración es
        múltiplo exacto; si no, es el resto, siempre mayor que cero.
    """
    total = parse_positive(total_time, "La duración")
    step = parse_positive(dt, "El paso de tiempo")
    steps = total_steps(total, step)

    if steps == 1:
        return 1, total

    last = total - (steps - 1) * step
    if last <= 0 or math.isclose(last, 0.0, abs_tol=1e-9 * max(total, step)):
        return steps, step
    return steps, last


def sample_indices(total, max_count):
    """Índices repartidos que siempre incluyen el primero y el último.

    Recibe:
        total     : cuántos elementos hay (estados o registros).
        max_count : cuántos índices se quieren como máximo.
    Devuelve:
        Lista de índices únicos y ordenados. Si `max_count` es None o mayor que
        `total`, devuelve todos.
    """
    if total <= 0:
        return []
    if max_count is None or max_count >= total:
        return list(range(total))
    if max_count <= 1:
        return [0]

    repartidos = np.linspace(0, total - 1, num=max_count)
    return sorted({int(round(value)) for value in repartidos} | {total - 1})


def _pairs(bodies):
    """Cuántos pares de cuerpos hay."""
    return len(bodies) * (len(bodies) - 1) // 2


def _check_budget(steps, bodies):
    """Rechaza una solicitud que cueste más que el presupuesto.

    Recibe:
        steps  : pasos que se quieren dar.
        bodies : cuerpos de la corrida.
    Lanza:
        ValueError con el costo calculado y qué cambiar.
    """
    work = steps * max(1, _pairs(bodies))
    if steps > MAX_STEPS or work > MAX_WORK:
        raise ValueError(
            f"La solicitud pide {steps:,} pasos × {_pairs(bodies)} pares "
            f"({work:,} operaciones) y el máximo es {MAX_WORK:,}. "
            "Reduce la duración, aumenta el paso de tiempo o quita cuerpos."
        )


def _check_steps(steps):
    """Revisa que `steps` sea un entero mayor que cero."""
    if isinstance(steps, bool) or not isinstance(steps, (int, np.integer)):
        raise ValueError("Los pasos deben ser un número entero.")
    if steps < 1:
        raise ValueError("Los pasos deben ser mayores que cero.")


def _check_record_every(record_every):
    """Revisa que `record_every` sea un entero mayor o igual que uno."""
    if isinstance(record_every, bool) or not isinstance(record_every, (int, np.integer)):
        raise ValueError("El intervalo de guardado debe ser un número entero.")
    if record_every < 1:
        raise ValueError("El intervalo de guardado debe ser mayor o igual que 1.")


def _min_pair(bodies):
    """Distancia del par de cuerpos más cercano.

    Recibe:
        bodies : lista de cuerpos.
    Devuelve:
        Una tupla (distancia, nombre_a, nombre_b). Con un solo cuerpo devuelve
        (inf, "", "").
    """
    best = (math.inf, "", "")
    for i in range(len(bodies)):
        first = bodies[i]
        for j in range(i + 1, len(bodies)):
            second = bodies[j]
            dx = float(second.position[0]) - float(first.position[0])
            dy = float(second.position[1]) - float(first.position[1])
            dz = float(second.position[2]) - float(first.position[2])
            distance = math.sqrt(dx * dx + dy * dy + dz * dz)
            if distance < best[0]:
                best = (distance, first.name, second.name)
    return best


def _measures(bodies):
    """Energía y momento angular del sistema, calculados sin NumPy.

    Se usa en cada paso del motor, así que conviene que sea rápido: para dos a
    cinco cuerpos, operar con números sueltos evita el costo de crear arreglos.

    Recibe:
        bodies : lista de cuerpos.
    Devuelve:
        Una tupla (cinética, potencial, total, momento_angular) donde el momento
        es un vector (Lx, Ly, Lz).
    """
    kinetic = 0.0
    potential = 0.0
    lx = ly = lz = 0.0

    for body in bodies:
        mass = float(body.mass)
        x = float(body.position[0])
        y = float(body.position[1])
        z = float(body.position[2])
        vx = float(body.velocity[0])
        vy = float(body.velocity[1])
        vz = float(body.velocity[2])

        kinetic += 0.5 * mass * (vx * vx + vy * vy + vz * vz)
        lx += mass * (y * vz - z * vy)
        ly += mass * (z * vx - x * vz)
        lz += mass * (x * vy - y * vx)

    for i in range(len(bodies)):
        first = bodies[i]
        for j in range(i + 1, len(bodies)):
            second = bodies[j]
            dx = float(second.position[0]) - float(first.position[0])
            dy = float(second.position[1]) - float(first.position[1])
            dz = float(second.position[2]) - float(first.position[2])
            distance = math.sqrt(dx * dx + dy * dy + dz * dz)
            if distance < MIN_DISTANCE:
                raise ValueError(
                    f"Los cuerpos '{first.name}' y '{second.name}' están a "
                    f"{distance:.3g} m, menos que el mínimo de {MIN_DISTANCE:g} m."
                )
            potential -= G * float(first.mass) * float(second.mass) / distance

    return kinetic, potential, kinetic + potential, (lx, ly, lz)


def _update_max(error_state, current, initial):
    """Actualiza el máximo error guardado con el valor de este paso."""
    if initial == 0:
        error_state["reference_zero"] = True
        error_state["max_absolute"] = max(error_state["max_absolute"], abs(current - initial))
        return

    percentage = abs(current - initial) / abs(initial) * 100.0
    error_state["max_percent"] = max(error_state["max_percent"] or 0.0, percentage)
    error_state["max_absolute"] = max(error_state["max_absolute"], abs(current - initial))


def run_simulation(bodies, dt, steps, method="Euler-Cromer", record_every=1,
                   max_records=None, last_step=None):
    """Corre el loop de física y devuelve el historial.

    Recibe:
        bodies       : lista de cuerpos con su estado inicial.
        dt           : paso de tiempo (s).
        steps        : cuántos pasos dar.
        method       : nombre del método dentro de `INTEGRATORS`.
        record_every : guarda el historial cada tantos pasos (1 = todos). La
                       física siempre avanza en cada paso; esto solo decide cada
                       cuánto se guarda.
        max_records  : si se indica, limita el historial a ese número de filas,
                       conservando siempre el primer y el último estado.
        last_step    : tamaño del último paso (s). Si es None se usa `dt`. Sirve
                       para que una duración no divisible se integre completa.
    Devuelve:
        Un diccionario con las listas "time", "energy" (total), "energy_kinetic",
        "energy_potential", "momentum", "positions" y "velocities", más el
        diagnóstico "conservation", el tiempo final y si la corrida se detuvo.
    Lanza:
        ValueError si los cuerpos o los parámetros no sirven.
    """
    step = parse_positive(dt, "El paso de tiempo")
    final_step = parse_positive(last_step, "El último paso") if last_step is not None else step
    _check_steps(steps)
    _check_record_every(record_every)

    if method not in INTEGRATORS:
        raise ValueError(
            f"El método '{method}' no existe; usa uno de: {', '.join(INTEGRATORS)}."
        )

    validate_body_objects(bodies)
    _check_budget(steps, bodies)

    integrator = INTEGRATORS[method]

    # Estados que se guardan: el inicial, los del intervalo y siempre el final.
    if max_records is None:
        saved = {k for k in range(1, steps + 1) if k % record_every == 0} | {steps}
    else:
        saved = set(sample_indices(steps + 1, max_records)) - {0}

    history = {
        "time": [],
        "energy": [],
        "energy_kinetic": [],
        "energy_potential": [],
        "momentum": [],
        "positions": [],
        "velocities": [],
    }

    initial_kinetic, initial_potential, initial_energy, initial_momentum = _measures(bodies)
    initial_momentum_norm = math.sqrt(sum(component * component for component in initial_momentum))

    energy_error = {"max_percent": None, "max_absolute": 0.0, "reference_zero": False}
    momentum_error = {"max_percent": None, "max_absolute": 0.0, "reference_zero": False}

    # El momento angular se compara como vector: norma y dirección.
    momentum_scale = initial_momentum_norm if initial_momentum_norm > 0 else 0.0
    if momentum_scale == 0:
        momentum_error["reference_zero"] = True

    def save_state(at_time, measures):
        """Guarda el estado actual en el historial, con sus magnitudes ya calculadas."""
        kinetic, potential, energy, momentum = measures
        history["time"].append(float(at_time))
        history["energy"].append(float(energy))
        history["energy_kinetic"].append(float(kinetic))
        history["energy_potential"].append(float(potential))
        history["momentum"].append(float(math.sqrt(sum(c * c for c in momentum))))
        history["positions"].append([body.position.copy() for body in bodies])
        history["velocities"].append([body.velocity.copy() for body in bodies])

    save_state(
        0.0, (initial_kinetic, initial_potential, initial_energy, initial_momentum)
    )

    time = 0.0
    steps_done = 0
    stopped = None

    for step_number in range(1, steps + 1):
        current_step = final_step if step_number == steps else step
        integrator(bodies, current_step)
        time += current_step
        steps_done = step_number

        # Primero se comprueba el acercamiento: si el estado ya no es válido, no
        # se calcula su energía (daría infinito) ni se guarda como resultado.
        distance, first, second = _min_pair(bodies)
        if distance < MIN_DISTANCE:
            stopped = {
                "reason": (
                    f"La corrida se detuvo en t = {time:.6g} s: '{first}' y '{second}' "
                    f"están a {distance:.3g} m, menos que el mínimo de {MIN_DISTANCE:g} m."
                ),
                "time": float(time),
                "pair": [first, second],
                "distance": float(distance),
            }
            break

        # Conservación medida en cada paso, no solo en los guardados (A21).
        measures = _measures(bodies)
        _update_max(energy_error, measures[2], initial_energy)

        if momentum_scale > 0:
            momentum = measures[3]
            difference = math.sqrt(
                sum((momentum[i] - initial_momentum[i]) ** 2 for i in range(3))
            )
            percentage = difference / momentum_scale * 100.0
            momentum_error["max_percent"] = max(momentum_error["max_percent"] or 0.0, percentage)
            momentum_error["max_absolute"] = max(momentum_error["max_absolute"], difference)

        if step_number in saved:
            save_state(time, measures)

    history["conservation"] = {
        "target_percent": CONSERVATION_TARGET_PERCENT,
        "energy": energy_error,
        "momentum": momentum_error,
    }
    history["final_time"] = float(history["time"][-1])
    history["steps"] = int(steps)
    history["steps_done"] = int(steps_done)
    history["method"] = method
    history["dt"] = step
    history["stopped"] = stopped
    return history
