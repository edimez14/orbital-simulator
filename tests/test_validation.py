# código nuevo edizon
"""test_validation.py — Pruebas de la revisión de datos de los cuerpos.

¿Para qué sirve?
    Comprobar que un campo vacío, una masa no positiva o un número no finito se
    rechazan con un mensaje que identifica cuerpo y campo.

¿Por qué existe?
    Antes un campo vacío llegaba al motor y producía TypeError o energía
    infinita. Estas pruebas fijan el contrato de la tarea A02 y la detección de
    superposición de A05.

¿Qué comprobará?
    - Nombre vacío, masa vacía, cero y negativa.
    - Componentes no finitos.
    - Cuerpos superpuestos.
    - Datos válidos conservan su valor.

¿Cómo ejecutarlo?
    pytest tests/test_validation.py

¿Cómo modificarlo?
    Añadir un caso por cada campo nuevo de un cuerpo.
"""

import numpy as np
import pytest

from src.physics.bodies import Body
from src.physics.validation import (
    overlap_message,
    overlapping_pairs,
    validate_bodies_data,
    validate_body_objects,
)

VALIDO = {
    "name": "Luna",
    "mass": 7.342e22,
    "x": 3.844e8,
    "y": 0.0,
    "z": 0.0,
    "vx": 0.0,
    "vy": 1022.0,
    "vz": 0.0,
}


def test_los_datos_validos_se_conservan():
    """Un cuerpo correcto sale con los mismos valores, como números."""
    limpio = validate_bodies_data([VALIDO])

    assert limpio[0]["name"] == "Luna"
    assert limpio[0]["mass"] == 7.342e22
    assert limpio[0]["x"] == 3.844e8
    assert limpio[0]["vy"] == 1022.0


@pytest.mark.parametrize(
    "campo,valor,mensaje",
    [
        ("name", "", "nombre"),
        ("name", "   ", "nombre"),
        ("mass", None, "masa está vacío"),
        ("mass", "", "masa está vacío"),
        ("mass", 0, "mayor que cero"),
        ("mass", -1.0, "mayor que cero"),
        ("mass", float("nan"), "finito"),
        ("x", float("inf"), "finito"),
        ("vy", "no es un número", "número"),
    ],
)
def test_los_campos_invalidos_se_rechazan(campo, valor, mensaje):
    """Cada campo inválido produce un error con su nombre."""
    datos = dict(VALIDO)
    datos[campo] = valor

    with pytest.raises(ValueError, match=mensaje):
        validate_bodies_data([datos])


def test_el_mensaje_identifica_el_cuerpo():
    """El mensaje dice qué cuerpo hay que corregir."""
    datos = dict(VALIDO, mass=0)

    with pytest.raises(ValueError, match="Cuerpo 1"):
        validate_bodies_data([datos])


def test_un_campo_vacio_no_se_convierte_en_cero():
    """Un campo vacío es un error, no un cero silencioso (tarea A02)."""
    with pytest.raises(ValueError):
        validate_bodies_data([dict(VALIDO, vz=None)])


def test_dos_cuerpos_superpuestos_se_detectan():
    """Se informa el par exacto que está demasiado cerca (tarea A05)."""
    primero = dict(VALIDO, name="Tierra", x=0.0, y=0.0, z=0.0, mass=5.972e24)
    segundo = dict(VALIDO, name="Luna", x=0.0, y=0.0, z=0.0)

    problemas = overlapping_pairs([primero, segundo])
    mensaje = overlap_message(problemas)

    assert len(problemas) == 1
    assert "Tierra" in mensaje and "Luna" in mensaje
    assert "Sepáralos" in mensaje


def test_dos_cuerpos_separados_no_producen_mensaje():
    """Sin superposición, el mensaje queda vacío."""
    primero = dict(VALIDO, name="Tierra", mass=5.972e24, x=0.0)
    segundo = dict(VALIDO, name="Luna")

    assert overlapping_pairs([primero, segundo]) == []
    assert overlap_message([]) == ""


def test_el_motor_rechaza_un_cuerpo_con_masa_negativa():
    """La entrada pública del motor también valida la masa (tarea A02)."""
    cuerpo = Body("Malo", -1.0, np.zeros(3), np.zeros(3))
    otro = Body("Bueno", 1.0, np.array([10.0, 0.0, 0.0]), np.zeros(3))

    with pytest.raises(ValueError, match="mayor que cero"):
        validate_body_objects([cuerpo, otro])


def test_el_motor_rechaza_un_vector_de_dos_componentes():
    """Un vector que no tiene tres componentes se rechaza con claridad."""
    cuerpo = Body("Malo", 1.0, np.array([0.0, 0.0]), np.zeros(3))
    otro = Body("Bueno", 1.0, np.array([10.0, 0.0, 0.0]), np.zeros(3))

    with pytest.raises(ValueError, match="tres componentes"):
        validate_body_objects([cuerpo, otro])
