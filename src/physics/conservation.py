# código nuevo edizon
"""conservation.py — Calcula energía mecánica y momento angular.

¿Para qué sirve?
    En cada instante, calcular magnitudes que en un sistema ideal deben
    permanecer constantes. Sirven como indicador de error del integrador: si se
    disparan o derivan, el método numérico está mal o el dt es demasiado grande.

    Energía mecánica total (PDF ec. 3):
        E = K + U = (1/2) · m · v² - G · M · m / r
    Momento angular respecto al origen (PDF ec. 4):
        L = r × (m · v)

Unidades (SI)
    energía : J (julios)
    momento : kg·m²/s

¿Por qué existe?
    Un gráfico bonito no demuestra que la física esté bien. Estas magnitudes son
    el criterio objetivo para validar el integrador, independiente del render.

¿Qué contendrá?
    - `kinetic_energy(body)`                : energía cinética de un cuerpo.
    - `potential_energy(bodies)`            : energía potencial del sistema.
    - `mechanical_energy(bodies)`           : suma de K + U.
    - `angular_momentum(body)`              : momento angular respecto al origen.
    - `relative_error(current, initial)`    : variación porcentual (PDF ec. 6).

Interpretación
    La variación relativa de E y L (respecto al valor inicial) es el indicador.
    Meta preliminar de tolerancia: ≤ 1 % (PDF sección 5.5).

¿Cómo modificarlo?
    - Añadir otra magnitud conservada: nueva función y usarla en el historial.
    - Cambiar la tolerancia: ajustar la constante en un solo lugar.
"""

import numpy as np

from src.physics.gravity import G, MIN_DISTANCE

# Tolerancia de la meta de conservación (PDF sección 5.5): 1 %.
CONSERVATION_TARGET_PERCENT = 1.0


def kinetic_energy(body):
    """Energía cinética de un cuerpo: K = ½ · m · v².

    Recibe:
        body : un cuerpo (usa su masa y su velocidad).
    Devuelve:
        La energía cinética, en las unidades del proyecto.
    """
    return 0.5 * body.mass * float(np.dot(body.velocity, body.velocity))


def potential_energy(bodies):
    """Energía potencial gravitacional del sistema: U = -G · Σ m_i·m_j / r_ij.

    Recibe:
        bodies : lista de cuerpos (usa masa y posición de cada uno).
    Devuelve:
        La energía potencial total, que siempre es negativa.
    """
    total = 0.0
    for i, body_i in enumerate(bodies):
        for j in range(i + 1, len(bodies)):
            body_j = bodies[j]
            distance = float(np.linalg.norm(body_j.position - body_i.position))
            if distance < MIN_DISTANCE:
                raise ValueError(
                    f"Los cuerpos '{body_i.name}' y '{body_j.name}' están a "
                    f"{distance:.3g} m, menos que el mínimo de {MIN_DISTANCE:.3g} m."
                )
            total -= G * body_i.mass * body_j.mass / distance
    return total


def mechanical_energy(bodies):
    """Energía mecánica total del sistema: suma de las cinéticas más la potencial.

    Recibe:
        bodies : lista de cuerpos.
    Devuelve:
        La energía mecánica E = K + U.
    """
    total = 0.0
    for body in bodies:
        total += kinetic_energy(body)
    return total + potential_energy(bodies)


def angular_momentum(body):
    """Momento angular de un cuerpo respecto al origen: L = r × (m · v).

    Recibe:
        body : un cuerpo (usa su masa, posición y velocidad).
    Devuelve:
        El vector de momento angular.
    """
    return np.cross(body.position, body.mass * body.velocity)


def relative_error(current, initial):
    """Variación porcentual respecto al valor inicial.

    Se divide entre el valor absoluto del inicial para que funcione igual con
    energías negativas. Si la referencia es cero, el porcentaje no tiene sentido
    (por ejemplo una energía casi cero cerca del escape): se devuelve `None` y
    quien lo use debe mostrar "no evaluable" (tarea A12).

    Recibe:
        current : valor actual.
        initial : valor al inicio (el de referencia).
    Devuelve:
        La variación en porcentaje, o `None` si `initial` es cero.
    """
    if initial == 0:
        return None
    return abs(current - initial) / abs(initial) * 100.0


def error_report(current, initial):
    """Error de una magnitud conservada: porcentaje y valor absoluto.

    El error absoluto siempre se puede dar, aunque la referencia sea cero. El
    porcentaje solo se da cuando la referencia permite comparar (tarea A12).

    Recibe:
        current : valor actual.
        initial : valor al inicio (el de referencia).
    Devuelve:
        Un diccionario con "percentage" (o None), "absolute" y "reference_zero".
    """
    return {
        "percentage": relative_error(current, initial),
        "absolute": abs(current - initial),
        "reference_zero": initial == 0,
    }
