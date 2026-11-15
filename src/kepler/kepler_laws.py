# código nuevo edizon
"""kepler_laws.py — Verifica las tres leyes de Kepler.

¿Para qué sirve?
    Tomar las posiciones generadas por la simulación y comprobar las tres leyes
    de Kepler con datos medidos, no con una fórmula aplicada a un tramo corto.

    Primera ley : las órbitas ligadas son elipses con el cuerpo central en uno
                  de sus focos.
    Segunda ley : el radio vector barre áreas iguales en tiempos iguales.
    Tercera ley : para órbitas alrededor del mismo cuerpo central, T² es
                  proporcional a a³.

¿Por qué existe?
    Es la prueba de que el simulador reproduce la mecánica clásica. Sin este
    archivo, solo existiría una animación, no una verificación física.

¿Qué contiene?
    - `swept_area(r1, r2)`                  : área barrida entre dos posiciones.
    - `check_first_law(relative_positions)` : ajuste de elipse con cobertura.
    - `check_second_law(positions, times)`  : velocidad areal por intervalo.
    - `measure_period(positions, times)`    : periodo medido por cruce de vuelta.
    - `check_third_law(orbits, mass)`       : comparación con la teoría.

Política de honestidad
    Si el arco es corto, la órbita es abierta o faltan datos, se devuelve un
    estado "insuficiente" en vez de una conclusión falsa.

¿Cómo modificarlo?
    - Cambiar tolerancias: constantes al inicio.
    - Añadir otra métrica: nueva función en este archivo.
"""

import math

import numpy as np

# Cobertura angular mínima para aceptar una elipse (casi una vuelta completa).
MIN_COVERAGE_DEG = 330.0

# Residuo máximo del ajuste de elipse, en fracción del semieje mayor.
MAX_RESIDUAL = 0.02

# Variación máxima de la velocidad areal para aceptar la segunda ley.
MAX_AREAL_VARIATION_PERCENT = 1.0

# Tolerancia al comparar T²/a³ con la teoría (meta del proyecto: 1 %).
THIRD_LAW_TOLERANCE_PERCENT = 1.0

# Puntos mínimos para intentar un ajuste.
MIN_POINTS = 5


def swept_area(r1, r2):
    """Área barrida por el radio vector entre dos posiciones consecutivas.

    Recibe:
        r1, r2 : posiciones relativas al cuerpo central.
    Devuelve:
        El área del triángulo que forman (m²).
    """
    return 0.5 * float(np.linalg.norm(np.cross(r1, r2)))


def _orbit_plane(positions):
    """Plano de la órbita y posiciones proyectadas en ese plano.

    Recibe:
        positions : posiciones relativas (N, 3).
    Devuelve:
        (eje1, eje2, normal, proyectadas) o None si no se puede definir el plano.
    """
    points = np.asarray(positions, dtype=float)
    if len(points) < 3:
        return None

    # Normal aproximada con el producto de dos radios no paralelos.
    normal = None
    for i in range(1, len(points) - 1):
        candidate = np.cross(points[i] - points[0], points[i + 1] - points[0])
        if np.linalg.norm(candidate) > 0:
            normal = candidate
            break
    if normal is None:
        return None

    normal = normal / np.linalg.norm(normal)
    first = points[0] - np.dot(points[0], normal) * normal
    if np.linalg.norm(first) == 0:
        return None

    axis1 = first / np.linalg.norm(first)
    axis2 = np.cross(normal, axis1)
    projected = np.column_stack((points @ axis1, points @ axis2))
    return axis1, axis2, normal, projected


def check_first_law(relative_positions):
    """Ajusta una elipse con foco en el origen y comprueba la cobertura.

    El ajuste usa 1/r = A + B·cos(θ) + C·sin(θ) sobre el plano de la órbita.
    De ahí salen el semieje mayor y la excentricidad. Si el arco no cubre casi
    una vuelta, no se certifica la elipse (tarea A22).

    Recibe:
        relative_positions : posiciones relativas al cuerpo central.
    Devuelve:
        Un diccionario con estado, semieje mayor, excentricidad, cobertura,
        residuo y mensaje.
    """
    points = np.asarray(relative_positions, dtype=float)
    base = {
        "status": "insuficiente",
        "semi_major_axis": None,
        "eccentricity": None,
        "periastro": None,
        "apoastro": None,
        "coverage_deg": 0.0,
        "residual": None,
        "points": int(len(points)),
        "message": "",
    }

    if len(points) < MIN_POINTS:
        base["message"] = "Hacen falta más muestras para medir la primera ley."
        return base

    plane = _orbit_plane(points)
    if plane is None:
        base["message"] = "La trayectoria no define un plano orbital."
        return base

    _, _, _, projected = plane
    distances = np.linalg.norm(points, axis=1)
    if np.any(distances == 0):
        base["message"] = "La trayectoria pasa por el cuerpo central."
        return base

    angles = np.unwrap(np.arctan2(projected[:, 1], projected[:, 0]))
    coverage = math.degrees(abs(angles[-1] - angles[0]))
    base["coverage_deg"] = coverage

    if coverage < MIN_COVERAGE_DEG:
        base["message"] = (
            f"El arco cubre {coverage:.0f}° y hacen falta al menos "
            f"{MIN_COVERAGE_DEG:.0f}° para comprobar la elipse."
        )
        return base

    # Ajuste lineal de 1/r frente a cos(θ) y sin(θ).
    design = np.column_stack((np.ones_like(angles), np.cos(angles), np.sin(angles)))
    coefficients, *_ = np.linalg.lstsq(design, 1.0 / distances, rcond=None)
    a_coef, b_coef, c_coef = coefficients

    if a_coef <= 0:
        base["status"] = "no_elipse"
        base["message"] = "El ajuste no corresponde a una órbita cerrada."
        return base

    eccentricity = math.hypot(b_coef, c_coef) / a_coef
    parameter = 1.0 / a_coef
    if eccentricity >= 1:
        base["eccentricity"] = eccentricity
        base["status"] = "no_elipse"
        base["message"] = f"La excentricidad medida es {eccentricity:.3f}: la órbita es abierta."
        return base

    semi_major = parameter / (1 - eccentricity**2)
    periastro = parameter / (1 + eccentricity)
    apoastro = parameter / (1 - eccentricity)

    # El ajuste ya incluye la orientación de la elipse (B·cos θ + C·sin θ).
    fitted = 1.0 / (a_coef + b_coef * np.cos(angles) + c_coef * np.sin(angles))
    residual = float(np.max(np.abs(fitted - distances)) / semi_major)

    base.update(
        {
            "semi_major_axis": float(semi_major),
            "eccentricity": float(eccentricity),
            "periastro": float(periastro),
            "apoastro": float(apoastro),
            "residual": residual,
        }
    )

    if residual > MAX_RESIDUAL:
        base["status"] = "no_elipse"
        base["message"] = f"El residuo del ajuste ({residual * 100:.2f} %) es demasiado alto."
        return base

    base["status"] = "ok"
    base["message"] = (
        f"Elipse con a = {semi_major:,.0f} m, e = {eccentricity:.4f}, "
        f"cobertura {coverage:.0f}° y residuo {residual * 100:.2f} %."
    )
    return base


def check_second_law(relative_positions, times):
    """Velocidad areal en cada intervalo, con los tiempos reales.

    No se supone que todos los intervalos duren lo mismo: cada área se divide
    entre su propio tiempo. Así el muestreo de la pantalla no altera el
    diagnóstico (tarea A24).

    Recibe:
        relative_positions : posiciones relativas al cuerpo central.
        times              : tiempos de cada posición (s). También acepta un
                             número, para intervalos iguales.
    Devuelve:
        Un diccionario con tiempos, áreas, velocidades areales, variación y
        estado.
    """
    positions = list(relative_positions)
    count = len(positions)
    if np.isscalar(times):
        times = [i * float(times) for i in range(count)]
    times = [float(value) for value in times]

    if count < 3 or len(times) != count:
        return {
            "status": "insuficiente",
            "times": [],
            "areas": [],
            "areal_velocities": [],
            "max_variation": None,
            "mean_areal": None,
            "message": "Hacen falta al menos tres muestras con sus tiempos.",
        }

    results = []
    for i in range(count - 1):
        delta = times[i + 1] - times[i]
        if delta <= 0:
            continue
        area = swept_area(positions[i], positions[i + 1])
        results.append((times[i + 1], area, area / delta))

    if len(results) < 2:
        return {
            "status": "insuficiente",
            "times": [],
            "areas": [],
            "areal_velocities": [],
            "max_variation": None,
            "mean_areal": None,
            "message": "Los tiempos no permiten comparar intervalos.",
        }

    areal = np.array([value for _, _, value in results])
    mean_areal = float(np.mean(areal))

    if mean_areal == 0:
        return {
            "status": "insuficiente",
            "times": [],
            "areas": [],
            "areal_velocities": [],
            "max_variation": None,
            "mean_areal": 0.0,
            "message": "La velocidad areal media es cero: el movimiento es radial.",
        }

    variation = float(np.max(np.abs(areal - mean_areal)) / abs(mean_areal) * 100.0)
    status = "ok" if variation <= MAX_AREAL_VARIATION_PERCENT else "revisar"

    return {
        "status": status,
        "times": [time for time, _, _ in results],
        "areas": [area for _, area, _ in results],
        "areal_velocities": [value for _, _, value in results],
        "max_variation": variation,
        "mean_areal": mean_areal,
        "message": (
            f"Velocidad areal media {mean_areal:,.4g} m²/s; "
            f"variación máxima {variation:.3f} % (meta {MAX_AREAL_VARIATION_PERCENT:g} %)."
        ),
    }


def measure_period(relative_positions, times):
    """Mide el periodo con el primer cruce de una vuelta completa.

    Recibe:
        relative_positions : posiciones relativas al cuerpo central.
        times              : tiempos de cada posición (s).
    Devuelve:
        Un diccionario con "period" (o None), "status", "turns" y "message".
        No devuelve el periodo teórico: si no se mide, se dice.
    """
    points = np.asarray(relative_positions, dtype=float)
    times = [float(value) for value in times]

    if len(points) < MIN_POINTS or len(times) != len(points):
        return {"period": None, "status": "insuficiente", "turns": 0.0,
                "message": "Hacen falta más muestras para medir el periodo."}

    plane = _orbit_plane(points)
    if plane is None:
        return {"period": None, "status": "insuficiente", "turns": 0.0,
                "message": "La trayectoria no define un plano orbital."}

    _, _, _, projected = plane
    angles = np.unwrap(np.arctan2(projected[:, 1], projected[:, 0]))
    swept = float(abs(angles[-1] - angles[0]))
    turns = swept / (2 * math.pi)

    if swept < 2 * math.pi:
        return {
            "period": None,
            "status": "insuficiente",
            "turns": turns,
            "message": (
                f"La trayectoria da {turns:.2f} vueltas; hace falta al menos una "
                "vuelta completa (órbita cerrada)."
            ),
        }

    direction = 1.0 if angles[-1] >= angles[0] else -1.0
    cumulative = np.abs(angles - angles[0])

    for i in range(1, len(cumulative)):
        if cumulative[i] >= 2 * math.pi:
            previous_angle = cumulative[i - 1]
            fraction = (2 * math.pi - previous_angle) / (cumulative[i] - previous_angle)
            period = times[i - 1] + fraction * (times[i] - times[i - 1])
            return {
                "period": float(period),
                "status": "ok",
                "turns": turns,
                "direction": direction,
                "message": f"Periodo medido: {period:,.0f} s ({period / 86400:.2f} días).",
            }

    return {"period": None, "status": "insuficiente", "turns": turns,
            "message": "No se encontró el cruce de una vuelta completa."}


def check_third_law(orbits, central_mass=None):
    """Compara T²/a³ de varias órbitas con la teoría.

    Recibe:
        orbits       : lista de diccionarios con "semi_major_axis" y "period".
                       Opcionalmente "secondary_mass" para afinar la teoría.
        central_mass : masa del cuerpo central (kg).
    Devuelve:
        Un diccionario con estado, constantes, valor teórico, error máximo y
        mensaje. Hacen falta al menos tres órbitas válidas.
    """
    valid = [
        orbit for orbit in orbits
        if orbit.get("semi_major_axis") and orbit.get("period")
        and orbit["semi_major_axis"] > 0 and orbit["period"] > 0
    ]

    if len(valid) < 3:
        return {
            "status": "insuficiente",
            "constants": [],
            "theoretical": None,
            "max_error_percent": None,
            "message": "Hacen falta al menos tres órbitas medidas y válidas.",
        }

    constants = [
        orbit["period"] ** 2 / orbit["semi_major_axis"] ** 3 for orbit in valid
    ]

    theoretical = None
    if central_mass:
        from src.physics.gravity import G

        theoretical = 4 * math.pi**2 / (G * central_mass)

    if theoretical is not None:
        error = max(abs(value - theoretical) / theoretical * 100 for value in constants)
        status = "ok" if error <= THIRD_LAW_TOLERANCE_PERCENT else "revisar"
        message = (
            f"{len(valid)} órbitas medidas; error máximo frente a 4π²/[G·(M+m)]: "
            f"{error:.3f} % (meta {THIRD_LAW_TOLERANCE_PERCENT:g} %)."
        )
    else:
        error = max(abs(value - np.mean(constants)) / abs(np.mean(constants)) * 100
                    for value in constants)
        status = "ok" if error <= THIRD_LAW_TOLERANCE_PERCENT else "revisar"
        message = (
            f"{len(valid)} órbitas medidas; dispersión de T²/a³: {error:.3f} %."
        )

    return {
        "status": status,
        "constants": constants,
        "theoretical": theoretical,
        "max_error_percent": float(error),
        "message": message,
    }
