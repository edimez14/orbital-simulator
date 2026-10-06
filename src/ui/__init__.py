# código nuevo edizon
"""Paquete `ui/` — entradas del usuario.

Contiene la interfaz de controles que traduce la interaccion del usuario en
cambios del estado inicial (masas y velocidades).

¿Qué contiene?
    - controls.py : sliders/campos de entrada (controles nativos de VPython).

¿Por qué separado?
    Traducir la interaccion es una responsabilidad distinta de calcular fisica o
    dibujar. `controls.py` no hace fisica ni renderizado.

¿Cómo modificarlo?
    Anadir un control nuevo aqui; conectarlo con `main.py`.
"""
