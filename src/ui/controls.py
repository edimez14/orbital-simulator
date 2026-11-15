# código nuevo edizon
"""controls.py — Controles de entrada del usuario.

¿Para qué sirve?
    Ofrecer deslizadores y botones para ajustar la masa del cuerpo central y la
    velocidad inicial del cuerpo que orbita, y entregar esos valores a `main.py`.

¿Por qué existe?
    Permite explorar cómo cambia el tipo de órbita (circular, elíptica o
    hiperbólica) al mover la velocidad inicial.

¿Qué contendrá?
    - `escape_velocity(mass, distance)` : el umbral de escape.
    - `Controls` : los deslizadores, los botones y los valores elegidos.

Umbral físico importante (PDF sección 5.4)
    La trayectoria hiperbólica necesita velocidad inicial MAYOR que la velocidad
    de escape. La interfaz muestra ese valor para que el usuario no ingrese
    números sin sentido físico.

Riesgo (PDF Fase 10)
    No confundir la interfaz con la física: los controles solo cambian valores;
    no calculan nada más que el umbral que muestran.

¿Cómo modificarlo?
    - Añadir otro parámetro (por ejemplo dt o el integrador): agregar un control
      y pasarlo a `main.py`.
    - Cambiar de librería de interfaz: reescribir solo este archivo.
"""

from vpython import button, slider, wtext

from src.physics.gravity import escape_velocity


class Controls:
    """Los controles de la interfaz: deslizadores, botones y valores elegidos.

    Solo guarda lo que el usuario elige. No calcula física ni toca el estado de
    los cuerpos.
    """

    def __init__(self, mass, velocity, distance):
        """Crea los deslizadores y los botones.

        Recibe:
            mass     : masa inicial del cuerpo central (masas solares).
            velocity : velocidad inicial del cuerpo que orbita (AU/año).
            distance : distancia inicial al cuerpo central (AU).
        """
        self.mass = mass
        self.velocity = velocity
        self.distance = distance
        self.running = False
        self.restart_requested = False

        self._mass_slider = slider(
            min=0.1, max=3.0, value=mass, step=0.1,
            text="Masa del cuerpo central (masas solares)",
            bind=self._read_sliders,
        )
        self._velocity_slider = slider(
            min=0.0, max=15.0, value=velocity, step=0.1,
            text="Velocidad inicial (AU/año)",
            bind=self._read_sliders,
        )
        self._escape_text = wtext(text="")
        self._update_escape_text()

        button(text="Iniciar", bind=self._start)
        button(text="Pausar", bind=self._pause)
        button(text="Reiniciar", bind=self._restart)

    def _read_sliders(self, _):
        """Lee los deslizadores y actualiza el umbral de escape."""
        self.mass = self._mass_slider.value
        self.velocity = self._velocity_slider.value
        self._update_escape_text()

    def _update_escape_text(self):
        """Muestra la velocidad de escape con los valores actuales."""
        escape = escape_velocity(self.mass, self.distance)
        self._escape_text.text = (
            f"Velocidad de escape: {escape:.2f} AU/año "
            "(por encima, la órbita es abierta)"
        )

    def _start(self, _):
        """Botón Iniciar: la simulación avanza."""
        self.running = True

    def _pause(self, _):
        """Botón Pausar: la simulación se detiene."""
        self.running = False

    def _restart(self, _):
        """Botón Reiniciar: se vuelve al estado inicial con los valores actuales."""
        self.restart_requested = True
        self.running = False
