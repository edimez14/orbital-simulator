# código nuevo edizon
"""Paquete `integrators/` — responde: ¿cómo avanza el tiempo?

Contiene los metodos numericos que, a partir del estado actual (posicion,
velocidad, aceleracion) y un paso de tiempo `dt`, calculan el siguiente estado.

¿Qué contiene?
    - euler_cromer.py : integrador simple y estable para orbitas.
    - verlet.py       : segundo metodo, para comparar precision.

¿Por qué separado?
    Cada integrador responde a la pregunta "¿como avanza el tiempo?" sin saber
    como se calcula la gravedad ni como se dibuja. Implementar los dos permite
    comparar conservacion de energia en el informe.

¿Cómo modificarlo?
    Anadir un metodo nuevo (por ejemplo Runge-Kutta) como un archivo mas aqui.
"""
