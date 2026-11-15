# código nuevo edizon
"""test_bodies.py — Pruebas de la clase `Body`.

¿Para qué sirve?
    Comprobar que un cuerpo guarda su masa, posición y velocidad iniciales.

¿Por qué existe?
    Sin esto, nadie sabría si la clase guarda lo que debe guardar. Es la prueba
    más sencilla de todas y la primera del proyecto.

¿Qué comprobará?
    Que al crear un cuerpo se conservan sus datos tal cual se recibieron.

¿Cómo ejecutarlo?
    pytest tests/test_bodies.py

¿Cómo modificarlo?
    No se necesita: este archivo cubre el punto pedido por el plan.
"""

import numpy as np

from src.physics.bodies import Body


def test_guarda_los_datos_iniciales():
    posicion = np.array([1.0, 0.0, 0.0])
    velocidad = np.array([0.0, 2.0, 0.0])

    cuerpo = Body(
        name="Tierra",
        mass=1.0,
        position=posicion,
        velocity=velocidad,
    )

    assert cuerpo.name == "Tierra"
    assert cuerpo.mass == 1.0
    assert np.array_equal(cuerpo.position, posicion)
    assert np.array_equal(cuerpo.velocity, velocidad)
