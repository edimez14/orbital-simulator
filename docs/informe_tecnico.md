<!-- código nuevo edizon -->
# Informe Técnico — Simulador Orbital y Leyes de Kepler

Documento donde se documentan los resultados del proyecto. Se completa a medida
que avanza la implementación.

## 1. Introducción

Planteamiento del problema: predecir el movimiento orbital partiendo de
condiciones iniciales, relacionando una ley física continua con un procedimiento
numérico paso a paso.

## 2. Marco teórico

- Ley de Gravitación Universal.
- Segunda Ley de Newton.
- Energía mecánica y su conservación.
- Momento angular y su conservación.
- Integración numérica: Euler-Cromer y Verlet.
- Leyes de Kepler.

## 3. Metodología

- Variables medidas (t, m, r, v, a, E, L, T, A).
- Escenarios de prueba: circular, elíptico, hiperbólico.
- Unidades internas: AU, masas solares, años.
- Tolerancia objetivo inicial: 1 %.

## 4. Resultados

Pendiente de llenar con las gráficas y tablas generadas por el simulador
(energía relativa, momento angular relativo, área barrida, T² vs a³).

## 5. Análisis de error

Se reporta el error relativo de una magnitud X como:

    Error = |X_sim - X_ref| / X_ref × 100 %

Para conservación se usa la variación respecto al valor inicial:

    ΔX(t) = |X(t) - X(0)| / X(0) × 100 %

## 6. Conclusiones

Pendiente. Debe indicar si el modelo reproduce las órbitas esperadas y si las
magnitudes de conservación y las relaciones de Kepler cumplen la tolerancia.

## 7. Referencias

Ver sección 10 de `docs/Pre-Proyecto Grupo 6.pdf`.
