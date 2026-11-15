# código nuevo edizon
"""gravity.py — Calcula la aceleración gravitacional.

¿Para qué sirve?
    Aplicar la Ley de Gravitación Universal entre varios cuerpos y devolver la
    aceleración que cada uno siente.

    Forma vectorial de la aceleración del cuerpo i por el cuerpo j (PDF ec. 2):
        a_i = G * sum_{j != i} ( m_j * (r_j - r_i) / |r_j - r_i|^3 )

¿Por qué existe?
    Es el "motor" de la física. No sabe nada de integración ni de gráficos: solo
    recibe posiciones y masas, y devuelve aceleraciones. Así se puede probar a
    mano con un caso simple (por ejemplo Sol-Tierra).

¿Qué contendrá?
    - `G` : constante de gravitación, 6.674e-11 m³·kg⁻¹·s⁻² en unidades SI.
    - `compute_accelerations(bodies)` : aceleración de cada cuerpo por el resto.

Unidades (SI)
    distancia : m
    masa      : kg
    tiempo    : s
    Con estas unidades, G = 6.674e-11 m³·kg⁻¹·s⁻².

¿Cómo funciona paso a paso?
    1. Recorrer los pares de cuerpos (i, j) con i distinto de j.
    2. Calcular el vector de separación (r_j - r_i) y su distancia.
    3. Sumar la contribución a la aceleración de i.
    4. Devolver el arreglo completo de aceleraciones.

Riesgo (PDF Fase 3)
    Si dos cuerpos quedan en el mismo punto, la distancia es cero y la división
    falla. Se usa una distancia mínima de seguridad.

¿Cómo modificarlo?
    No hay nada que cambiar todavía. Para otra fuerza, crear un archivo nuevo.
"""

import math

import numpy as np

# Constante de gravitación universal, en unidades SI (m³·kg⁻¹·s⁻²).
G = 6.674e-11

# Distancia mínima para no dividir por cero si dos cuerpos coinciden (en m).
MIN_DISTANCE = 1.0


def escape_velocity(mass, distance):
    """Velocidad de escape a una distancia del cuerpo central: sqrt(2·G·M/r).

    Recibe:
        mass     : masa del cuerpo central (kg).
        distance : distancia al centro (m).
    Devuelve:
        La velocidad de escape (m/s).
    """
    return float(np.sqrt(2 * G * mass / distance))


def compute_accelerations(bodies):
    """Calcula la aceleración de cada cuerpo por la atracción de los demás.

    Recibe:
        bodies : lista de cuerpos (cada uno con `mass` y `position`).

    Devuelve:
        Un arreglo con una aceleración (tres números) por cada cuerpo, en el
        mismo orden en que llegan.
    """
    # Se trabaja con números sueltos: para pocos cuerpos es más rápido que
    # crear arreglos en cada paso y el resultado es el mismo.
    count = len(bodies)
    accelerations = [[0.0, 0.0, 0.0] for _ in range(count)]

    for i in range(count):
        body_i = bodies[i]
        xi = float(body_i.position[0])
        yi = float(body_i.position[1])
        zi = float(body_i.position[2])
        for j in range(i + 1, count):
            body_j = bodies[j]
            dx = float(body_j.position[0]) - xi
            dy = float(body_j.position[1]) - yi
            dz = float(body_j.position[2]) - zi

            distance = math.sqrt(dx * dx + dy * dy + dz * dz)
            if distance < MIN_DISTANCE:
                distance = MIN_DISTANCE
            factor = G / (distance * distance * distance)

            # Cada cuerpo acelera hacia el otro, con la masa del otro.
            first = factor * float(body_j.mass)
            accelerations[i][0] += first * dx
            accelerations[i][1] += first * dy
            accelerations[i][2] += first * dz

            second = factor * float(body_i.mass)
            accelerations[j][0] -= second * dx
            accelerations[j][1] -= second * dy
            accelerations[j][2] -= second * dz

    return np.array(accelerations)
