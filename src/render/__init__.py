# código nuevo edizon
"""Paquete `render/` — responde: ¿qué ve el usuario?

Contiene la representacion visual del sistema. SOLO LEE el estado generado por
la fisica; nunca lo modifica ni calcula fisica.

¿Qué contiene?
    - scene3d.py : escena 3D interactiva (VPython).
    - plots.py   : graficas 2D de analisis (Matplotlib).

¿Por qué separado?
    Para poder correr miles de pasos de integracion sin quedar limitado por el
    framerate de los graficos. La fisica no depende de esta carpeta.

¿Cómo modificarlo?
    Cambiar de libreria 3D solo afecta a `scene3d.py` y `ui/controls.py`.
"""
