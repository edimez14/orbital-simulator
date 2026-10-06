# código nuevo edizon
"""plots.py — Gráficas 2D de análisis.

¿Para qué sirve?
    Producir las graficas que sustentan el analisis del informe, usando
    Matplotlib.

    Graficas previstas (PDF seccion 6.2):
        - Energia relativa  : t  vs  dE/E0   -> estabilidad del integrador.
        - Momento angular   : t  vs  dL/L0   -> conservacion.
        - Area barrida      : t  vs  A(dt)   -> segunda ley de Kepler.
        - T^2 vs a^3        : a^3 vs T^2     -> tercera ley (relacion lineal).

¿Por qué existe?
    Estas graficas NO son decoracion: son la evidencia objetiva de que el metodo
    numerico conserva las magnitudes fisicas.

¿Qué contendrá? (aún sin implementar)
    - `plot_energy(history)`        : energia vs tiempo.
    - `plot_angular_momentum(...)`  : momento angular vs tiempo.
    - `plot_swept_area(...)`        : areas barridas en tiempos iguales.
    - `plot_third_law(orbits)`      : T^2 contra a^3.

¿Cómo funciona paso a paso?
    1. Recibir el historial (listas de tiempo y magnitudes).
    2. Construir cada figura con su eje X, eje Y y rotulos.
    3. Guardar o mostrar la figura.

¿Cómo modificarlo?
    - Anadir una grafica: nueva funcion aqui, reutilizando el historial.
    - Cambiar el estilo: un solo bloque de configuracion al inicio del archivo.
"""
