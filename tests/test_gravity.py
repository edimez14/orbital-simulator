# código nuevo edizon
"""test_gravity.py — Pruebas del cálculo gravitacional.

¿Para qué sirve?
    Comprobar que `physics/gravity.py` calcula la fuerza y la aceleracion
    correctamente, comparando contra un caso resuelto a mano.

¿Por qué existe?
    Un error en la gravedad invalida todo el simulador. Se prueba de forma
    aislada antes de continuar con los integradores (PDF seccion 5.3, paso 2).

¿Qué contendrá? (aún sin implementar)
    - Prueba con 2 cuerpos fijos y un caso simple (por ejemplo Tierra-Sol).
    - Verificacion de la direccion de la fuerza (atraccion, no repulsion).
    - Verificacion de la magnitud contra el valor calculado a mano.

¿Cómo ejecutarlo? (cuando este implementado)
    pytest tests/test_gravity.py

¿Cómo modificarlo?
    Anadir mas casos de prueba aqui, manteniendo cada prueba independiente.
"""
