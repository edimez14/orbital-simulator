# código nuevo edizon
"""Paquete `physics/` — responde: ¿cómo interactúan los cuerpos?

Contiene la representacion de los cuerpos, el calculo de la fuerza/aceleracion
gravitacional y las magnitudes conservadas (energia y momento angular).

¿Qué contiene?
    - bodies.py        : estructura de datos de un cuerpo celeste.
    - gravity.py       : Ley de Gravitacion Universal.
    - conservation.py  : energia mecanica y momento angular.

¿Por qué separado del render?
    Para que un error de graficos no haga dudar de los calculos. La fisica no
    importa nada de `render/` ni de `ui/`.

¿Cómo modificarlo?
    Anadir un nuevo calculo fisico creando otro archivo dentro de esta carpeta.
"""
