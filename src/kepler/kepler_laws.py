# código nuevo edizon
"""kepler_laws.py — Verifica las tres leyes de Kepler.

¿Para qué sirve?
    Tomar el historial de posiciones generado por la simulacion y comprobar las
    tres leyes de Kepler contra la teoria.

    Primera ley : las orbitas ligadas son elipses con el cuerpo central en uno
                  de sus focos.
    Segunda ley : el radio vector barre areas iguales en tiempos iguales.
    Tercera ley : para orbitas alrededor del mismo cuerpo central, T^2 es
                  proporcional a a^3.

¿Por qué existe?
    Es la prueba de que el simulador reproduce la mecanica clasica. Sin este
    archivo, solo existiria una animacion, no una verificacion fisica.

¿Qué contendrá? (aún sin implementar)
    - `check_first_law(positions)`       : ajustar/inspeccionar la elipse y
                                           localizar el foco.
    - `check_second_law(positions, dt)`  : calcular areas barridas A(dt) en
                                           intervalos de tiempo iguales.
    - `check_third_law(orbits)`          : comparar T^2 con a^3 (relacion lineal).
    - `swept_area(...)`                  : area entre dos radios vectores.

¿Cómo funciona paso a paso?
    1. Recibir el historial completo (o una lista de orbitas).
    2. Calcular la magnitud pedida en cada ley.
    3. Compararla con el resultado teorico y reportar la desviacion.

Criterio de exito (PDF seccion 6.2)
    Demostrar con pruebas reproducibles que las orbitas y las relaciones de
    Kepler cumplen una tolerancia cuantitativa razonable (por ejemplo 1 %).

¿Cómo modificarlo?
    - Anadir otra ley o una nueva metrica: nueva funcion en este archivo.
    - Cambiar la tolerancia: definirla en un solo lugar y usarla en las tres.
"""
