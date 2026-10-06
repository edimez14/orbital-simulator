# código nuevo edizon
"""gravity.py — Calcula la fuerza y la aceleración gravitacional.

¿Para qué sirve?
    Aplicar la Ley de Gravitacion Universal entre varios cuerpos y devolver las
    fuerzas (o aceleraciones) que cada uno siente.

    Forma vectorial de la aceleracion del cuerpo i por el cuerpo j (PDF ec. 2):
        a_i = G * sum_{j != i} ( m_j * (r_j - r_i) / |r_j - r_i|^3 )

¿Por qué existe?
    Es el "motor" de la fisica. No sabe nada de integracion ni de graficos: solo
    recibe posiciones y masas, y devuelve fuerzas/aceleraciones. Asi se puede
    probar a mano con un caso simple (por ejemplo Tierra-Sol).

¿Qué contendrá? (aún sin implementar)
    - `G`            : constante de gravitacion en las unidades elegidas
                       (si se usan AU, masas solares y anos, G = 4*pi^2).
    - `compute_accelerations(bodies)` : aceleracion de cada cuerpo por el resto.
    - `compute_forces(bodies)`        : alternativa que devuelve fuerzas.

¿Cómo funciona paso a paso?
    1. Recorrer los pares de cuerpos (i, j) con i distinto de j.
    2. Calcular el vector de separacion (r_j - r_i) y su distancia.
    3. Sumar la contribucion a la aceleracion de i.
    4. Devolver el arreglo completo de aceleraciones.

Validacion (PDF seccion 5.3, paso 2)
    Antes de seguir, probar con 2 cuerpos fijos y verificar el resultado a mano
    con un caso simple.

¿Cómo modificarlo?
    - Cambiar de sistema de unidades: ajustar `G` y documentarlo.
    - Optimizar: usar NumPy para vectorizar el calculo entre todos los cuerpos.
    - Añadir otra fuerza: crear un archivo nuevo, no mezclarla aqui.
"""
