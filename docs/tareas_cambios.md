<!-- código nuevo edizon -->
# Tareas de cambios — una por una

Cambios pedidos para llevar el proyecto al diseño del pre-proyecto
(`docs/Pre-Proyecto Grupo 6.pdf`) y al boceto de interfaz.

Regla: **una tarea a la vez**. Cada una se propone, el usuario la aprueba y
recién ahí se coloca. Nada se hace por iniciativa propia.

## Progreso

- [x] Tarea 1 — Física en unidades SI
- [x] Tarea 2 — Datos reales de los cuerpos
- [x] Tarea 3 — Motor con opciones de simulación
- [x] Tarea 4 — Historial y resultados para la interfaz
- [x] Tarea 5 — Aplicación Dash: estructura y tema
- [x] Tarea 6 — Vista 3D con Plotly
- [x] Tarea 7 — Gráficas dentro de la interfaz
- [x] Tarea 8 — Editar cuerpos
- [x] Tarea 9 — Tipo de trayectoria y umbral de escape
- [x] Tarea 10 — Resultados y tabla de datos
- [x] Tarea 11 — Pruebas y documentación
- [ ] Tarea 12 — Empaquetado (en pausa: no se compila hasta que el usuario lo ordene)
- [x] Tarea 13 — Que se vea el modelo (WebGL)
- [x] Tarea 14 — Que el panel se adapte a la pantalla
- [x] Tarea 15 — Que el panel sea fácil de entender
- [x] Tarea 16 — Manual de usuario
- [x] Tarea 17 — Que se vea el movimiento (animación)
- [x] Tarea 18 — Que se vean los assets y no se vea tan simple
- [x] Tarea 19 — Que las gráficas queden al lado, no abajo
- [x] Tarea 20 — Poder girar, inclinar y acercar la vista
- [x] Tarea 21 — Pausar, continuar y reiniciar
- [x] Tarea 22 — Más tipos de órbita (y velocidad ajustable)
- [x] Tarea 23 — Que la órbita nunca se vea diminuta
- [x] Tarea 24 — Que los cuerpos se vean bien (esferas, no recuadros planos)
- [x] Tarea 25 — Que cambiar un valor no parezca reiniciar la página
- [x] Tarea 26 — Arreglar el desborde del panel de configuración
- [x] Tarea 27 — Animación dentro del navegador (no depende de la red)

---

## Tarea nueva (del 16 de octubre, quinta tanda)

### Tarea 27 — Animación dentro del navegador
- **Problema:** la animación le pedía un cuadro al servidor cada 60 milisegundos.
  En una red con intermediario (por ejemplo la universidad) se quedaba trabada.
- **Cambio:** la figura lleva todos los cuadros y sus botones de **Reproducir** y
  **Pausar**. La animación corre en el navegador y no le pide nada al servidor.
- **Criterio:** la animación funciona igual en cualquier red y el servidor no
  recibe peticiones mientras corre.

---

## Tareas nuevas (del 16 de octubre, cuarta tanda)

### Tarea 24 — Que los cuerpos se vean bien
- **Problema:** las texturas se pegan como recuadros planos y se ven feas.
- **Cambio:** dibujar cada cuerpo como una esfera con luz y halo (círculos de
  color), con el color propio de cada cuerpo. Se quitan las texturas pegadas.
- **Criterio:** en la vista se ven esferas redondas, no recuadros.

### Tarea 25 — Que cambiar un valor no parezca reiniciar la página
- **Problema:** al escribir un valor, el panel se vuelve a dibujar entero y parece
  que la página se refresca; además, el acercamiento de la vista se pierde.
- **Cambio:** los campos guardan su valor al salir de la casilla (no en cada
  tecla), y la vista mantiene el giro y el acercamiento entre cuadros.
- **Criterio:** se puede escribir un número sin que el panel se rearme, y el
  acercamiento se mantiene mientras corre la animación.

### Tarea 26 — Arreglar el desborde del panel de configuración
- **Problema:** en el panel izquierdo los botones de tipo de órbita se salen y la
  barra de velocidad queda cortada.
- **Cambio:** que los botones bajen de línea cuando no quepan y que la barra de
  velocidad se vea completa.
- **Criterio:** en la pantalla del usuario se ven los cuatro botones y la barra
  completa, sin nada cortado.

---

## Tareas nuevas (del 16 de octubre, tercera tanda)

### Tarea 20 — Poder girar, inclinar y acercar la vista
- **Problema:** la vista de la órbita está fija; no se puede girar, inclinar ni
  acercar.
- **Cambio:** controles de **giro**, **inclinación** y **acercamiento**, y ejes que
  se ajustan a lo que se pide.
- **Criterio:** mover los tres controles cambia la vista al instante.

### Tarea 21 — Pausar, continuar y reiniciar
- **Problema:** no hay forma de detener ni reiniciar la animación, y al cambiar un
  valor parece que la simulación arranca sola.
- **Cambio:** botones **Pausar/Continuar** y **Reiniciar**. Cambiar un valor no
  vuelve a arrancar nada: el resultado se ve cuando se pulse *Iniciar Simulación*.
- **Criterio:** la animación se detiene, sigue y se reinicia cuando se pulsa.

### Tarea 22 — Más tipos de órbita (y velocidad ajustable)
- **Problema:** solo hay tres tipos y no se puede pedir una órbita intermedia.
- **Cambio:** añadir **Parabólica** y un control de **velocidad** (en veces la
  velocidad circular) para conseguir cualquier órbita. El panel dice qué tipo
  resulta con la velocidad elegida.
- **Criterio:** cualquier velocidad entre 0,5 y 2,0 veces la circular da una órbita
  y el panel dice de qué tipo es.

### Tarea 23 — Que la órbita nunca se vea diminuta
- **Problema:** cuando el cuerpo se aleja mucho (caso hiperbólico), la vista se
  encoge tanto que el recorrido se ve como un punto.
- **Cambio:** el encuadre se ajusta a lo que se lleva recorrido y se abre a medida
  que el cuerpo se aleja.
- **Criterio:** el recorrido se ve con buen tamaño en cualquier tipo de órbita.

---

## Tareas nuevas (del 16 de octubre, segunda tanda)

### Tarea 17 — Que se vea el movimiento (animación)
- **Problema:** al iniciar la simulación se dibuja la órbita completa y nada se
  mueve; no se ve la trayectoria avanzar.
- **Cambio:** al pulsar *Iniciar Simulación*, el cuerpo avanza por la órbita: el
  recorrido se va dibujando y el cuerpo se mueve. Se puede ver en repetido.
- **Criterio:** al iniciar, el cuerpo se ve moverse por la órbita.

### Tarea 18 — Que se vean los assets y no se vea tan simple
- **Problema:** los cuerpos son puntos de color y la escena se ve vacía; las
  texturas de `assets/textures/` no se usan.
- **Cambio:** dibujar cada cuerpo con su textura (Sol, planetas y Luna) y poner un
  fondo de estrellas.
- **Criterio:** en la vista se reconocen los cuerpos por su imagen y el fondo se
  ve estrellado.

### Tarea 19 — Que las gráficas queden al lado, no abajo
- **Problema:** el punto de corte de la Tarea 14 movió la columna de gráficas
  abajo en una pantalla normal.
- **Cambio:** mantener las tres columnas hasta pantallas de unos 1150 píxeles;
  apilar solo por debajo de eso.
- **Criterio:** en una pantalla normal y en una ventana mediana, las gráficas
  siguen a la derecha.

---

## Tareas nuevas (del 16 de octubre)

### Tarea 13 — Que se vea el modelo
- **Problema:** la vista 3D usa WebGL (Plotly `scatter3d`) y el navegador del
  usuario no lo soporta; sale el aviso "WebGL is not supported by your browser".
- **Cambio:** dibujar la órbita con líneas y puntos normales (sin WebGL), con una
  vista inclinada que se vea en 3D.
- **Criterio:** en el navegador se ven el cuerpo central, la órbita y el cuerpo que
  gira, sin avisos.

### Tarea 14 — Que el panel se adapte a la pantalla
- **Problema:** el panel tiene columnas de ancho fijo y en pantallas medianas y
  pequeñas se corta (la columna de gráficas queda fuera).
- **Cambio:** que las tres zonas se acomoden solas y se apilen cuando no quepan.
- **Criterio:** en pantalla completa y en una ventana pequeña se ve todo sin
  cortarse ni salir barras de desplazamiento horizontales.

### Tarea 15 — Que el panel sea fácil de entender
- **Problema:** no se entiende qué hacer ni en qué orden.
- **Cambio:** ordenar el panel por pasos (1: cuerpo central, 2: cuerpo que orbita,
  3: cómo se mueve, 4: iniciar), con textos cortos que expliquen cada cosa y
  valores de ejemplo listos para usar.
- **Criterio:** alguien que no conoce el programa sabe qué hacer sin que se lo
  expliquen.

### Tarea 16 — Manual de usuario
- **Archivo:** `docs/manual_de_usuario.md`.
- **Contenido:** qué es el programa, cómo abrirlo y cada paso en orden, con lo que
  hay que escribir y qué significa cada resultado.
- **Forma:** paso a paso, sin lenguaje técnico y sin relleno.
- **Criterio:** seguir el manual de corrido alcanza para usar el programa.

---

## Decisión previa (confirmada)

1. **Unidades:** el texto del pre-proyecto recomienda AU / masas solares / años,
   pero el boceto de la interfaz usa SI (kg, m, m/s, días). Los bocetos mandan.
   Se propone: **SI en todo el proyecto**, con el tiempo mostrado en días.
2. **Interfaz:** el boceto es un panel tipo aplicación web. Eso se hace con
   **Plotly + Dash** (lo que el propio pre-proyecto propone para "verse
   profesional"). VPython no puede dibujar ese panel. Esto implica **retirar
   VPython** (`scene3d.py` y `controls.py` actuales).
3. **Librerías nuevas:** esto agrega `dash` y `plotly` a `requirements.txt`.

---

## Tareas

### Tarea 1 — Física en unidades SI
- `src/physics/gravity.py`: `G = 6.674e-11` (m³·kg⁻¹·s⁻²).
- `src/physics/conservation.py`: fórmulas con kg, m, s (energía en J, momento en
  kg·m²/s).
- Pruebas de gravedad y conservación en SI.
- **Criterio:** las pruebas actuales siguen pasando, ahora en SI.

### Tarea 2 — Datos reales de los cuerpos
- Presets con datos reales, en kg, m y m/s (por ejemplo Tierra–Luna, Sol–Tierra).
- Quitar el preset de juguete "sistema_solar_interno".
- **Criterio:** simular Tierra–Luna y que la órbita se mantenga dentro de la
  tolerancia.

### Tarea 3 — Motor con opciones de simulación
- Elegir método numérico (Euler-Cromer o Verlet), paso de tiempo y tiempo total.
- **Criterio:** el mismo escenario corre con los dos métodos y con distinto paso.

### Tarea 4 — Historial y resultados para la interfaz
- Historial con posición, velocidad, energía total / cinética / potencial y
  momento angular.
- **Criterio:** con esos datos se llenan las tarjetas y la tabla del boceto.

### Tarea 5 — Aplicación Dash: estructura y tema
- Panel izquierdo (configuración), centro (vista 3D, resultados, tabla), derecha
  (gráficas). Tema oscuro del boceto.
- **Criterio:** abre la app y se ve la estructura del boceto.

### Tarea 6 — Vista 3D con Plotly
- Órbita, cuerpo central, ejes y controles de rotar/zoom.
- Nota: las texturas reales son limitadas en Plotly; se evalúa mostrar imágenes
  de los cuerpos o esferas de color.
- **Criterio:** la órbita se ve en 3D y se puede rotar.

### Tarea 7 — Gráficas dentro de la interfaz
- Trayectoria 2D, energía (total, cinética, potencial), momento angular y
  verificación de Kepler (las pestañas del boceto).
- **Criterio:** salen las gráficas del boceto, con sus ejes y rótulos.

### Tarea 8 — Editar cuerpos
- Agregar cuerpo, editar masa / posición / velocidad, eliminar.
- **Criterio:** agregar la Luna como segundo cuerpo y verla orbitar.

### Tarea 9 — Tipo de trayectoria y umbral de escape
- Selector circular / elíptica / hiperbólica y velocidad de escape visible.
- **Criterio:** cada tipo de órbita sale con los datos del escenario.

### Tarea 10 — Resultados y tabla de datos
- Tarjetas (posición, velocidad, energía, momento angular) y tabla por tiempo.
- **Criterio:** los números de la tabla coinciden con las gráficas.

### Tarea 11 — Pruebas y documentación
- Pruebas del motor y de la interfaz; README y plan alineados con SI y Dash.
- **Criterio:** `pytest` corre completo y la documentación no contradice el
  boceto.

### Tarea 12 — Empaquetado
- Ejecutable que abra la interfaz sin tener Python instalado (Fase 12 del plan).
- **Criterio:** el ejecutable abre la simulación en otro computador.
