# código nuevo edizon
"""validation.py — Revisa los datos de los cuerpos antes de calcular.

Por qué existe: la interfaz y el motor reciben números escritos a mano. Un campo
vacío, una masa negativa o una posición repetida producían errores confusos
(TypeError, IndexError, energía infinita). Aquí se revisan una sola vez y se
explica qué cuerpo y qué campo hay que corregir.

Qué contiene: `validate_bodies_data` para los diccionarios del panel,
`validate_body_objects` para los objetos del motor y `overlapping_pairs` para
detectar dos cuerpos en el mismo punto.

Cómo funciona: se recorre cada cuerpo, se convierte cada campo a número, se
comprueba que sea finito y que la masa sea positiva. Nada se convierte en cero
por su cuenta: un campo vacío es un error.

Cómo cambiarlo: añadir un campo nuevo a `BODY_NUMBER_FIELDS` con su nombre para
el mensaje; las dos validaciones lo usan sin tocar el resto.
"""

import math

import numpy as np

from src.physics.gravity import MIN_DISTANCE

# Campos numéricos de un cuerpo y el nombre que se muestra en los mensajes.
BODY_NUMBER_FIELDS = (
    ("mass", "masa"),
    ("x", "posición x"),
    ("y", "posición y"),
    ("z", "posición z"),
    ("vx", "velocidad x"),
    ("vy", "velocidad y"),
    ("vz", "velocidad z"),
)

def _number(value, body_label, field_label):
    """Convierte un campo a número y lo rechaza si está vacío o no es finito.

    Recibe:
        value       : valor tal como llega del panel o del motor.
        body_label  : texto que identifica al cuerpo en el mensaje.
        field_label : texto que identifica el campo en el mensaje.
    Devuelve:
        El número como `float`.
    Lanza:
        ValueError con el cuerpo y el campo que hay que corregir.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValueError(f"{body_label}: el campo {field_label} está vacío.")

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{body_label}: el campo {field_label} debe ser un número; llegó {value!r}."
        ) from None

    if not math.isfinite(number):
        raise ValueError(f"{body_label}: el campo {field_label} debe ser un número finito.")

    return number


def _body_label(index, name):
    """Texto para los mensajes: número de cuerpo y nombre si lo tiene."""
    if isinstance(name, str) and name.strip():
        return f"Cuerpo {index + 1} ('{name.strip()}')"
    return f"Cuerpo {index + 1}"


def validate_bodies_data(bodies):
    """Revisa los cuerpos del panel y devuelve una copia con números.

    Recibe:
        bodies : lista de diccionarios con name, mass, x, y, z, vx, vy, vz.
    Devuelve:
        Una lista nueva, con los mismos campos y todos los números como `float`.
    Lanza:
        ValueError con el cuerpo y el campo que no sirve.
    """
    if not bodies:
        raise ValueError("No hay cuerpos: agrega al menos uno.")

    normalized = []
    for index, data in enumerate(bodies):
        if not isinstance(data, dict):
            raise ValueError(f"Cuerpo {index + 1}: los datos no tienen el formato esperado.")

        name = data.get("name")
        label = _body_label(index, name)
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{label}: el nombre no puede estar vacío.")

        clean = {"name": name.strip()}
        for field, field_label in BODY_NUMBER_FIELDS:
            value = _number(data.get(field), label, field_label)
            if field == "mass" and value <= 0:
                raise ValueError(f"{label}: la masa debe ser mayor que cero (llegó {value:g} kg).")
            clean[field] = value
        normalized.append(clean)

    return normalized


def validate_body_objects(bodies):
    """Revisa cuerpos ya construidos, antes de integrarlos.

    Recibe:
        bodies : lista de objetos `Body` del motor.
    Devuelve:
        Nada; solo comprueba.
    Lanza:
        ValueError con el cuerpo y el campo que no sirve.
    """
    if not bodies:
        raise ValueError("No hay cuerpos: se necesitan al menos dos para simular.")
    if len(bodies) < 2:
        raise ValueError("Se necesitan al menos dos cuerpos para simular.")

    for index, body in enumerate(bodies):
        label = _body_label(index, getattr(body, "name", None))
        if not isinstance(getattr(body, "name", None), str) or not body.name.strip():
            raise ValueError(f"{label}: el nombre no puede estar vacío.")

        mass = _number(getattr(body, "mass", None), label, "masa")
        if mass <= 0:
            raise ValueError(f"{label}: la masa debe ser mayor que cero (llegó {mass:g} kg).")

        for vector, labels in (
            (getattr(body, "position", None), ("posición x", "posición y", "posición z")),
            (getattr(body, "velocity", None), ("velocidad x", "velocidad y", "velocidad z")),
        ):
            if not isinstance(vector, np.ndarray) or vector.shape != (3,):
                raise ValueError(f"{label}: el vector debe tener tres componentes.")
            for component, field_label in zip(vector, labels):
                _number(component, label, field_label)

    # Dos cuerpos en el mismo punto no se pueden integrar: el potencial sería
    # infinito. Se detiene antes de empezar y se nombra el par (tarea A05).
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            distance = float(np.linalg.norm(bodies[j].position - bodies[i].position))
            if distance < MIN_DISTANCE:
                raise ValueError(
                    f"Los cuerpos '{bodies[i].name}' y '{bodies[j].name}' están a "
                    f"{distance:.3g} m, menos que el mínimo de {MIN_DISTANCE:g} m. "
                    "Sepáralos antes de simular."
                )


def overlapping_pairs(bodies):
    """Pares de cuerpos más cerca que la distancia mínima.

    Recibe:
        bodies : lista de diccionarios normalizados (con mass, x, y, z).
    Devuelve:
        Lista de tuplas (nombre_a, nombre_b, distancia). Vacía si no hay problema.
    """
    problems = []
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            first, second = bodies[i], bodies[j]
            dx = second["x"] - first["x"]
            dy = second["y"] - first["y"]
            dz = second["z"] - first["z"]
            distance = math.sqrt(dx * dx + dy * dy + dz * dz)
            if distance < MIN_DISTANCE:
                problems.append((first["name"], second["name"], distance))
    return problems


def overlap_message(problems):
    """Mensaje que explica qué par de cuerpos hay que separar.

    Recibe:
        problems : lo que devuelve `overlapping_pairs`.
    Devuelve:
        El texto para el usuario, o una cadena vacía si no hay problemas.
    """
    if not problems:
        return ""

    detalles = "; ".join(
        f"'{first}' y '{second}' están a {distance:.3g} m"
        for first, second, distance in problems
    )
    return (
        f"Hay cuerpos superpuestos: {detalles}. "
        f"Sepáralos al menos {MIN_DISTANCE:g} m cambiando su posición inicial."
    )
