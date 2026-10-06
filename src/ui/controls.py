# código nuevo edizon
"""controls.py — Controles de entrada del usuario.

¿Para qué sirve?
    Ofrecer sliders y campos para ajustar la masa y la velocidad inicial, y
    traducir esa interaccion en cambios del estado inicial de la simulacion.

¿Por qué existe?
    Permite explorar como una pequena modificacion de la velocidad inicial
    cambia el tipo de orbita (circular, eliptica o hiperbolica).

¿Qué contendrá? (aún sin implementar)
    - Controles nativos de VPython para masa y velocidad inicial.
    - Botones de iniciar/pausar/reiniciar la simulacion.
    - Lectura de valores y entrega del estado inicial a `main.py`.

Umbral fisico importante (PDF seccion 5.4)
    La trayectoria hiperbolica requiere velocidad inicial MAYOR a la velocidad de
    escape. Debemos calcular y mostrar ese umbral en la interfaz; si no, los
    inputs producen resultados sin sentido fisico.

¿Cómo funciona paso a paso?
    1. Crear los controles con sus valores iniciales y rangos.
    2. Al mover un control, actualizar los parametros de entrada.
    3. Entregar el estado inicial a `main.py` cuando el usuario lo pida.

¿Cómo modificarlo?
    - Anadir otro parametro (por ejemplo dt o el integrador): agregar un control
      y pasarlo a `main.py`.
    - Cambiar de libreria de UI: reescribir solo este archivo.

Este archivo es la ultima pieza del checklist (PDF seccion 5.3, paso 9): se
conecta cuando el motor de fisica ya es confiable.
"""
