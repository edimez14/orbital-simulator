# código nuevo edizon
"""Escenario de prueba: trayectoria hiperbólica.

¿Para qué sirve?
    Comprobar que con una velocidad inicial mayor que la velocidad de escape el
    cuerpo escapa y describe una trayectoria hiperbólica abierta.

¿Por qué existe?
    Es el tercer escenario del checklist (PDF sección 5.3, paso 10). Verifica que
    el simulador distingue órbitas ligadas de trayectorias abiertas.

Velocidad de escape (PDF sección 5.4)
    v_escape = sqrt(2 * G * M / r)
    Se requiere v_inicial > v_escape.

Umbral en la interfaz (PDF sección 5.4)
    El simulador debe calcular y mostrar esta velocidad de escape; si no, los
    valores ingresados producen resultados sin sentido físico.

¿Qué contendrá? (aún sin implementar)
    - Un caso con velocidad claramente mayor que v_escape.
    - La simulacion hasta que el cuerpo se aleje mucho del centro.
    - La comprobacion de que la distancia crece sin retorno (orbita abierta).

Criterio de aceptación
    La energia mecanica total debe ser mayor o igual a cero (sistema no ligado).

¿Cómo ejecutarlo? (cuando esté implementado)
    pytest tests/scenarios/test_scenario_hyperbolic.py

¿Cómo modificarlo?
    Cambiar el factor de velocidad sobre v_escape en un solo bloque al inicio.
"""
