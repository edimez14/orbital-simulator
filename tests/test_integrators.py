# código nuevo edizon
"""test_integrators.py — Pruebas de Euler-Cromer y Verlet.

¿Para qué sirve?
    Comprobar que los integradores avanzan el estado correctamente y comparar su
    estabilidad.

¿Por qué existe?
    Los integradores son el corazon del avance temporal. Se prueban por separado
    y luego se comparan con datos (no por suposicion), segun el PDF.

¿Qué contendrá? (aún sin implementar)
    - Prueba de una orbita circular de 2 cuerpos: la orbita debe cerrarse.
    - Comparacion de conservacion de energia entre Euler-Cromer y Verlet.
    - Prueba del primer paso (arranque) de Verlet.

¿Cómo ejecutarlo? (cuando este implementado)
    pytest tests/test_integrators.py

¿Cómo modificarlo?
    Anadir metodos nuevos como casos de prueba adicionales.
"""
