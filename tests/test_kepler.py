# código nuevo edizon
"""test_kepler.py — Pruebas de las tres leyes de Kepler.

¿Para qué sirve?
    Comprobar que `kepler/kepler_laws.py` verifica correctamente las tres leyes
    sobre orbitas generadas por la simulacion.

¿Por qué existe?
    Es la demostracion final del proyecto: que el simulador reproduce la
    mecanica clasica con pruebas reproducibles.

¿Qué contendrá? (aún sin implementar)
    - Primera ley: la orbita es cerrada y el cuerpo central esta en un foco.
    - Segunda ley: las areas barridas en tiempos iguales son aproximadamente
      iguales.
    - Tercera ley: T^2 / a^3 se mantiene aproximadamente constante.

Casos a cubrir (PDF seccion 5.3, paso 10)
    Orbita circular, eliptica e hiperbolica, en ese orden de complejidad.

¿Cómo ejecutarlo? (cuando este implementado)
    pytest tests/test_kepler.py

¿Cómo modificarlo?
    Anadir orbitas de prueba adicionales manteniendo cada caso aislado.
"""
