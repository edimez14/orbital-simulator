# código nuevo edizon
"""Escenario de prueba: órbita elíptica.

¿Para qué sirve?
    Comprobar que con una velocidad tangencial menor que la velocidad circular
    (pero menor que la de escape) el cuerpo describe una órbita elíptica.

¿Por qué existe?
    Es el segundo escenario del checklist (PDF sección 5.3, paso 10). Es la base
    para verificar la Primera Ley de Kepler (el cuerpo central en un foco).

Condiciones (PDF sección 6.1)
    v_circular > v_inicial > 0  y  v_inicial < v_escape
    donde v_escape = sqrt(2 * G * M / r)

¿Qué contendrá? (aún sin implementar)
    - Un caso con velocidad entre 0 y v_c.
    - La simulacion de al menos una orbita completa.
    - La comprobacion de que la distancia al foco varia (periastro y apoastro)
      y de que la orbita es cerrada.

Criterio de aceptación
    El semieje mayor y la excentricidad deben coincidir con la teoria dentro de
    la tolerancia definida.

¿Cómo ejecutarlo? (cuando esté implementado)
    pytest tests/scenarios/test_scenario_elliptical.py

¿Cómo modificarlo?
    Cambiar la masa, el radio o la fraccion de v_c en un solo bloque al inicio.
"""
