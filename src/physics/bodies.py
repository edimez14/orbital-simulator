# código nuevo edizon
"""bodies.py — Define qué es un cuerpo celeste.

¿Para qué sirve?
    Representar un cuerpo mediante su masa, posicion, velocidad y nombre. Es una
    ESTRUCTURA DE DATOS, no logica: aqui no se calcula nada, solo se guarda el
    estado del cuerpo.

¿Por qué existe?
    Todos los demas modulos necesitan una forma comun de leer y escribir el estado
    (posicion y velocidad). Si cada modulo inventa su propio formato, se vuelven
    incompatibles.

¿Qué contendrá? (aún sin implementar)
    - Clase `Body` con:
        * `name`      : nombre del cuerpo (por ejemplo "Sol", "Tierra").
        * `mass`      : masa (en masas solares).
        * `position`  : vector (x, y, z) en AU.
        * `velocity`  : vector (vx, vy, vz) en AU/ano.
        * `acceleration`: vector de aceleracion, usado por los integradores.
    - Metodos de apoyo para leer/actualizar el estado de forma clara.

Unidades (PDF seccion 3.6)
    Usar unidades astronomicas normalizadas para evitar numeros gigantes:
        - distancia : AU
        - masa      : masas solares
        - tiempo    : anos
    Mantener una sola convencion interna; no mezclar SI con AU.

¿Cómo funciona paso a paso?
    1. Se crea un `Body` con su masa, posicion y velocidad iniciales.
    2. Los integradores actualizan `position`, `velocity` y `acceleration`.
    3. `gravity.py` y `conservation.py` solo LEEN esos valores.

¿Cómo modificarlo?
    - Añadir un atributo fijo (por ejemplo `color` o `radius` para la escena):
      agregarlo en la clase `Body`.
    - Cambiar la convencion de unidades: actualizar el docstring y los valores
      por defecto, nunca mezclar dos convenciones a la vez.
"""
