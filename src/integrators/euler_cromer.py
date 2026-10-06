# código nuevo edizon
"""euler_cromer.py — Integrador de Euler-Cromer.

¿Para qué sirve?
    Avanzar el estado del sistema en el tiempo. Primero actualiza la velocidad
    usando la aceleracion actual y DESPUES actualiza la posicion usando la
    velocidad NUEVA. Ese orden es lo que lo hace mas estable que el Euler
    explicito para problemas orbitales.

    Velocidad nueva : v(t+dt) = v(t) + a(t) * dt
    Posicion nueva  : r(t+dt) = r(t) + v(t+dt) * dt

¿Por qué existe?
    Es el integrador mas simple de los dos y el primero que se implementa. Sirve
    de referencia para comparar luego con Verlet.

¿Qué contendrá? (aún sin implementar)
    - `step(bodies, dt)` : recibe el estado actual y `dt`, y devuelve (o modifica)
      el siguiente estado.

¿Cómo funciona paso a paso?
    1. Recibir la aceleracion actual de cada cuerpo (calculada en `gravity.py`).
    2. Actualizar la velocidad de cada cuerpo con esa aceleracion.
    3. Actualizar la posicion con la velocidad ya actualizada.
    4. Devolver el nuevo estado.

Validacion (PDF seccion 5.3, paso 3)
    Implementarlo primero y correr una orbita circular de 2 cuerpos. Confirmar
    —aunque sea con un print de coordenadas— que la orbita se cierra.

¿Cómo modificarlo?
    - Cambiar el orden de actualizacion: NO hacerlo; el orden es lo que define a
      Euler-Cromer. Para otro esquema, crear un archivo nuevo.
    - Cambiar a paso adaptativo: modificar el manejo de `dt` y documentarlo.
"""
