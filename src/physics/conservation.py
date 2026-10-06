# código nuevo edizon
"""conservation.py — Calcula energía mecánica y momento angular.

¿Para qué sirve?
    En cada instante, calcular magnitudes que en un sistema ideal deben
    permanecer constantes. Sirven como indicador de error del integrador: si se
    disparan o derivan, el metodo numerico esta mal implementado o el dt es
    demasiado grande.

    Energia mecanica total (PDF ec. 3):
        E = K + U = (1/2) * m * v^2 - G * M * m / r
    Momento angular respecto al origen (PDF ec. 4):
        L = r x (m * v)

¿Por qué existe?
    Un grafico bonito no demuestra que la fisica este bien. Estas magnitudes son
    el criterio OBJETIVO para validar el integrador, independiente del render.

¿Qué contendrá? (aún sin implementar)
    - `kinetic_energy(body)`        : energia cinetica de un cuerpo.
    - `potential_energy(bodies)`    : energia potencial gravitacional del sistema.
    - `mechanical_energy(bodies)`   : suma de K + U.
    - `angular_momentum(body)`      : momento angular respecto al origen.
    - `relative_error(current, initial)` : variacion porcentual (PDF ec. 6).

¿Cómo funciona paso a paso?
    1. Recibir el estado actual de los cuerpos.
    2. Calcular E y L con las formulas de arriba.
    3. Devolver los valores para que `main.py` los guarde en el historial.

Interpretacion
    - Variacion relativa de E y L (respecto al valor inicial) como indicador.
    - Meta preliminar de tolerancia: <= 1 % (PDF seccion 5.5). Confirmar el valor
      despues de experimentar con dt y con ambos integradores.

¿Cómo modificarlo?
    - Añadir otra magnitud conservada: nueva funcion y usarla en el historial.
    - Cambiar la tolerancia: ajustar la constante en un solo lugar.
"""
