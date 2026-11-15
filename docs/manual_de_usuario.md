<!-- código nuevo edizon -->
# Manual de usuario — Simulador Orbital

Este manual explica cómo usar el programa, paso a paso.

---

## Qué es el programa

Sirve para ver cómo se mueven dos o más cuerpos en el espacio (por ejemplo, la Luna
alrededor de la Tierra) y para comprobar que las cuentas están bien.

El programa se usa desde el navegador.

---

## Antes de empezar

Necesitas:

- Una computadora con navegador.
- El programa instalado y funcionando.

Si aún no está instalado, pídele a quien te entregó el proyecto que lo deje listo.

---

## Paso 1. Abrir el programa

1. Abre la terminal en la carpeta del proyecto.
2. Escribe esto y pulsa Enter:

   ```
   python -m src.main
   ```

3. Espera a que aparezca un mensaje parecido a:

   ```
   Dash is running on http://127.0.0.1:8050/
   ```

4. Abre el navegador y escribe esta dirección:

   ```
   http://127.0.0.1:8050
   ```

5. Verás el panel con el título **Simulador Orbital**.

No cierres la terminal mientras usas el programa.

---

## Paso 2. Elegir el escenario (grupo 1 del panel)

En **1. Escenario de ejemplo** elige uno:

- **Tierra y Luna**: la Tierra queda en el centro y la Luna gira a su alrededor.
- **Sol y Tierra**: el Sol queda en el centro y la Tierra gira alrededor.
- **Sistema solar interno**: el Sol en el centro y cuatro planetas alrededor.

Al elegirlo, los cuerpos del panel cambian solos. No tienes que escribir nada.

---

## Paso 3. Elegir el tipo de órbita (grupo 2 del panel)

En **2. Tipo de órbita** elige uno de los cuatro botones:

- **Circular**: el cuerpo gira siempre a la misma distancia.
- **Elíptica**: el cuerpo se acerca y se aleja, dibujando un óvalo.
- **Parabólica**: el caso justo en el límite; se va y apenas vuelve.
- **Hiperbólica**: el cuerpo se va y no vuelve.

Al elegir uno, el programa ajusta la velocidad para que salga ese tipo de órbita y
mueve el control de **Velocidad**.

También puedes mover **Velocidad (× la circular)** a mano: el número indica cuántas
veces la velocidad circular se está usando. Menos de 1,41 son órbitas que vuelven;
más de 1,41 el cuerpo se escapa.

Debajo aparece una línea con tres velocidades:

- **v circular**: la velocidad que hace una órbita redonda.
- **v escape**: la velocidad a la que el cuerpo ya no vuelve.
- **ahora**: la velocidad que está puesta, cuántas veces la circular es y qué tipo
  de órbita resulta.

---

## Paso 4. Revisar o cambiar los cuerpos (grupo 3 del panel)

Cada cuerpo tiene estos datos:

| Dato | Qué significa |
|------|----------------|
| Nombre | Cómo se llama el cuerpo (por ejemplo "Tierra"). |
| Masa (kg) | Cuánto pesa el cuerpo, en kilogramos. |
| Posición inicial (m) | Dónde está al empezar, en metros (x, y, z). |
| Velocidad inicial (m/s) | Con qué velocidad se mueve al empezar (x, y, z). |

Cosas que puedes hacer:

- **Cambiar un dato**: escribe otro número en su casilla. El cambio se usa cuando
  pulses *Iniciar Simulación*.
- **Agregar un cuerpo**: pulsa *+ Agregar cuerpo*. Aparece uno nuevo con datos de
  ejemplo.
- **Eliminar un cuerpo**: pulsa *Eliminar*. El primer cuerpo no se puede eliminar
  porque es el centro.

El primer cuerpo es el centro. Si le dejas la velocidad en cero, se queda quieto en
el medio y los demás giran a su alrededor.

---

## Paso 5. Elegir el cálculo (grupo 4 del panel)

- **Método**: hay dos, *Euler-Cromer* y *Verlet*. Los dos dan resultados parecidos;
  sirven para comparar. Si no sabes cuál elegir, deja *Verlet*.
- **Paso de tiempo (s)**: cuánto tiempo avanza el programa en cada cálculo. Un
  número más pequeño da resultados más exactos, pero tarda más.
- **Duración (días)**: cuánto tiempo se simula.

---

## Paso 6. Iniciar y leer los resultados

Pulsa **Iniciar Simulación**. Después de un momento verás:

**En el centro:**

- **Vista de la órbita**: se ve el cuerpo central y el recorrido del cuerpo que
  gira. Debajo de la vista están los controles:
  - **Giro**: gira la vista alrededor del centro.
  - **Inclinación**: mira la órbita desde arriba o desde el lado.
  - **Acercamiento**: agranda o reduce la vista.
  - **Reproducir / Pausar**: botones que están dentro de la gráfica; con ellos se
    ve cómo se mueve el cuerpo.
  - **Barra de progreso**: al lado de esos botones; se puede arrastrar para ir a
    cualquier punto de la órbita.
- **Resultados del cuerpo que gira**: su posición, su velocidad, su energía y su
  momento angular en el último instante.
- **Datos del cuerpo que gira**: una tabla con esos mismos valores, cada cierto
  tiempo.

**A la derecha:**

- **Trayectoria**: el recorrido visto desde arriba, en forma de dibujo.
- **Energía Mecánica**: tres líneas con la energía total, la de movimiento y la de
  atracción. Si el cálculo está bien, la línea de la total queda casi plana.
- **Momento Angular**: otra línea que también debe quedar casi plana.
- **Ley de Kepler**: el área que va barriendo el cuerpo. Si el cálculo está bien,
  el área es parecida en todos los tramos.

---

## Qué significa cada número

| Número | Qué es |
|--------|--------|
| Masa (kg) | Cuánto pesa el cuerpo. |
| Posición (m) | Dónde está. |
| Velocidad (m/s) | A qué velocidad se mueve y hacia dónde. |
| Energía mecánica (J) | Suma de la energía de movimiento y la de atracción. |
| Momento angular (kg·m²/s) | Cuánto gira alrededor del centro. |

Si el cálculo está bien, la energía y el momento angular se mantienen casi iguales
durante toda la simulación. Por eso se ven como líneas planas.

---

## Si algo no se ve bien

- **La página no abre**: revisa que la terminal siga abierta y que la dirección sea
  `http://127.0.0.1:8050`.
- **El cuerpo se escapa y no vuelve**: su velocidad es mayor que *v escape*. Baja la
  velocidad o elige *Circular*.
- **La órbita se ve rara o "explotada"**: usa un paso de tiempo más pequeño.
- **Tarda mucho**: usa un paso de tiempo más grande o baja la duración.
- **Al pulsar Iniciar no aparece nada**: revisa que la masa y las distancias no sean
  cero.

---

## Cómo cerrar el programa

1. Cierra la pestaña del navegador.
2. En la terminal, pulsa `Ctrl` + `C`.
