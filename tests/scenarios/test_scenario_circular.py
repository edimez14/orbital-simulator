# código nuevo edizon
"""Escenario de prueba: órbita circular.

¿Para qué sirve?
    Comprobar que con una velocidad tangencial igual a la velocidad circular el
    cuerpo describe una órbita aproximadamente circular.

¿Por qué existe?
    Es el escenario más simple y el primero del checklist de casos de prueba
    (PDF sección 5.3, paso 10). Si este funciona, la gravedad y el integrador
    están bien conectados.

Velocidad circular (PDF sección 3.6)
    v_c = sqrt(G * M / r)

¿Qué contendrá? (aún sin implementar)
    - Un caso con masa central M, radio r y velocidad exactamente v_c.
    - La simulacion de varios periodos.
    - Una comprobacion de que el radio se mantiene casi constante y que la
      orbita se cierra.

Criterio de aceptación
    La variacion relativa del radio debe quedar dentro de la tolerancia
    (por ejemplo 1 %).

¿Cómo ejecutarlo? (cuando esté implementado)
    pytest tests/scenarios/test_scenario_circular.py

¿Cómo modificarlo?
    Cambiar M, r o la tolerancia en un solo bloque al inicio del archivo.
"""
