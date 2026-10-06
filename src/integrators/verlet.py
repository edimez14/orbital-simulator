# código nuevo edizon
"""verlet.py — Integrador de Verlet.

¿Para qué sirve?
    Ser el segundo metodo numerico del proyecto, para comparar su precision y su
    capacidad de conservar energia contra Euler-Cromer.

    Forma de posicion de Verlet:
        r(t+dt) = 2*r(t) - r(t-dt) + a(t) * dt^2
    (la velocidad se obtiene de la diferencia de posiciones).

¿Por qué existe?
    Recorrer paso a paso la demostracion exige comparar dos integradores con
    datos, no por suposicion. Verlet suele conservar mejor la energia para un dt
    adecuado.

¿Qué contendrá? (aún sin implementar)
    - `step(bodies, dt)` : avanza el estado usando Verlet.
    - Manejo del estado anterior `r(t-dt)` (el primer paso necesita un arranque).

¿Cómo funciona paso a paso?
    1. Guardar la posicion anterior de cada cuerpo.
    2. Calcular la nueva posicion con la formula de Verlet.
    3. Estimar la velocidad a partir del cambio de posicion.
    4. Devolver el nuevo estado.

Validacion (PDF seccion 5.3, paso 5)
    Implementarlo DESPUES de confirmar que Euler-Cromer funciona. Comparar ambos:
    Verlet debe conservar la energia igual o mejor.

¿Cómo modificarlo?
    - Cambiar el arranque del primer paso: revisar solo esa parte.
    - Probar la variante "velocity Verlet": crear un archivo nuevo si se quiere
      mantener ambos metodos disponibles.
"""
