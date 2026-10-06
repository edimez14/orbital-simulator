# código nuevo edizon
"""Paquete `kepler/` — responde: ¿se cumplen las leyes?

Contiene el analisis que toma los datos de posicion generados por la simulacion
y los contrasta contra las leyes de Kepler.

¿Qué contiene?
    - kepler_laws.py : verificacion de las tres leyes.

¿Por qué separado de `physics/`?
    La fisica genera el estado; este paquete lo INTERPRETA. Separarlos permite
    cambiar el analisis sin tocar el motor de gravedad.

¿Cómo modificarlo?
    Anadir otra verificacion (por ejemplo energia por unidad de masa) aqui.
"""
