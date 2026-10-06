# código nuevo edizon
"""main.py — Orquestador del simulador orbital.

¿Para qué sirve?
    Une todas las piezas del proyecto. Es el unico archivo que conoce todos los
    modulos: crea los cuerpos iniciales, corre el loop de simulacion y llama al
    renderizado. Es el punto de entrada (`python src/main.py`).

¿Por qué existe este archivo?
    Para que ningun otro modulo dependa de todos los demas. Si la fisica no sabe
    que existe el render (y viceversa), cada parte se puede probar por separado.

¿Qué contendrá? (aún sin implementar)
    - Construccion de los cuerpos iniciales desde un preset o desde la interfaz.
    - El loop de simulacion: pedir aceleraciones a `physics/gravity.py`, avanzar
      el estado con un integrador de `integrators/`, y registrar energia y momento
      angular con `physics/conservation.py` en un historial.
    - Cada N pasos, entregar el historial a `render/scene3d.py` para dibujar.
    - Al final (o en tiempo real), llamar a `render/plots.py` y a
      `kepler/kepler_laws.py` para analizar el historial completo.

¿Cómo funciona paso a paso?
    1. Se cargan los parametros (masas, posiciones, velocidades, dt, integrador).
    2. Se repite: calcular aceleracion -> avanzar estado con dt -> guardar estado.
    3. El render lee el estado guardado; nunca calcula fisica.

Punto critico (PDF seccion 4.1)
    El loop de fisica corre independiente del renderizado. No calcular fisica
    dentro de la funcion que dibuja. Si se acoplan, la simulacion se vuelve tan
    lenta como el framerate y no se pueden correr miles de pasos para verificar
    Kepler con precision.

¿Cómo modificarlo?
    - Cambiar el integrador: escoger otro archivo de `integrators/` en la linea
      donde se avanza el estado.
    - Cambiar la frecuencia de dibujo: ajustar el valor de "cada N pasos".
    - Anadir otra metrica: registrarla en el historial y pasarla al analisis.

Orden recomendado de construccion (PDF seccion 5.3)
    Este archivo se completa despues de tener `bodies`, `gravity`,
    `euler_cromer`, `conservation` y `verlet` funcionando.
"""
