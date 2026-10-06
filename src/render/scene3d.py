# código nuevo edizon
"""scene3d.py — Dibuja el sistema en 3D.

¿Para qué sirve?
    Mostrar la escena tridimensional del sistema: posiciones actuales de los
    cuerpos, sus trayectorias y los ejes de referencia, usando VPython.

¿Por qué existe?
    Es la parte visible del proyecto, pero NO la mas importante. Dibuja el estado
    que ya calculo la fisica; no calcula nada por su cuenta.

¿Qué contendrá? (aún sin implementar)
    - Creacion de esferas para cada cuerpo (tamano y color proporcionales).
    - Trazado de la trayectoria recorrida.
    - Ejes de referencia.
    - Una funcion `update(history_slice)` que posiciona los objetos segun el
      estado guardado.

REGLA DE ORO (PDF seccion 4.1 y 4.3)
    Este archivo SOLO LEE el estado. Nunca lo modifica y nunca calcula fisica.
    No calcular fisica dentro de la funcion que dibuja.

¿Cómo funciona paso a paso?
    1. Al inicio, crear los objetos visuales (esferas, curvas, ejes).
    2. En cada actualizacion, recibir un fragmento del historial.
    3. Mover las esferas a las posiciones correspondientes.

¿Cómo modificarlo?
    - Cambiar el estilo (tamano, color, fondo): solo en la funcion de creacion.
    - Cambiar de libreria 3D: reescribir solo este archivo.
"""
