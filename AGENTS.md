<!-- código nuevo edizon -->
# Reglas para agentes del proyecto

**Proyecto:** Simulador orbital (Leyes de Kepler).
**Quién usa este archivo:** yo mismo, y cualquier agente que trabaje en el
proyecto. Se lee antes de escribir o cambiar algo.

Estas reglas ordenan cómo trabajo. Si una regla y lo pedido por el usuario
disponen, lo pedido manda sobre esta lista.

## Regla 1 — No romper lo que ya funciona
Todo lo que ya existe y funciona se conserva tal cual, salvo lo que el usuario
pida explícitamente cambiar. Si algo parece mal hecho, se lo señalo antes de
tocarlo.

## Regla 2 — Todo pasa por la revisión del usuario
Ningún cambio se guarda en el proyecto sin la aprobación del usuario. Yo presento
lo que he hecho o propuesto; el usuario decide; si no lo acepta, no se coloca.
Ni un detalle pequeño se aplica por mi cuenta.

## Regla 3 — Sigue el plan, fase por fase
El desarrollo está ordenado en fases en `docs/plan_de_desarrollo.md`. Se hace fase
por fase, en el orden en que están escritas. Se termina la fase actual antes de
empezar la siguiente. No se salta una fase ni se empieza la siguiente mientras la
actual sigue abierta.

## Regla 4 — Documenta todo, como se documenta aquí
Cada archivo empieza con un texto que explica para qué sirve. Cada función tiene
su comentario: qué hace, qué recibe y qué devuelve, y cómo se usa. Sin relleno y
sin rodeos. Si algo no necesita explicación, no se comenta.

## Regla 5 — Solo lo que pide el plan
No se añaden funciones, carpetas ni ideas que no estén en el plan. Si veo algo
que parece necesario pero el plan no lo pide, lo propongo al usuario y espero su
decisión. No lo implemento por iniciativa propia.

## Regla 6 — No cambies las convenciones existentes
Las unidades (distancia en AU, masa en masas solares, tiempo en años), los nombres
de funciones y la organización de carpetas son del proyecto. Si algo está mal
planteado, se lo señalo y espero una decisión del usuario. No los arreglo yo solo.

## Regla 7 — No añadas librerías nuevas
Solo se usa lo que ya está en `requirements.txt`. Pedir una librería nueva se
hace al usuario, y se decide antes de escribir una sola línea.

## Regla 8 — Estructura de carpetas
Cada carpeta responde a una sola pregunta. Un archivo nuevo solo entra si el plan
lo pide. Dentro de un archivo, una función por pregunta. No se mezclan temas.

## Regla 9 — Presenta cada cambio de forma clara
Cuando empiezo un cambio, se dice qué hice, por qué y qué queda pendiente. Todo
en español, sin tecnicismos innecesarios. El usuario debe poder revisarlo sin
abrir el código.

## Regla 10 — Detente si algo falla o duda
Si un paso no funciona o no estoy seguro, lo detengo y pregunto al usuario en
lugar de improvisar. No se prueba una solución a ciegas.

## Regla 11 — Sin trabajo extra
No se hace ninguna mejora que no pida el plan: no se optimiza lo que funciona, no
se reordena lo existente y no se pulen detalles. Lo pedido al usuario es lo único
que se hace.

## Regla 12 — El usuario decide
El usuario es el dueño del proyecto. Yo decido nada por mí mismo, ni siquiera
para arreglar pequeños detalles. Siempre se pregunta antes de actuar.

## Regla 13 — Ritmo de trabajo
Al terminar cada fase se resume: lo hecho, lo siguiente y lo que necesita una
decisión del usuario. Se pasa al siguiente punto solo cuando la fase actual está
terminada y aprobada.

## Regla 14 — Trabajo en grupo
El proyecto lo hace un grupo, no una sola persona. Cada quien trabaja en cosas
diferentes, nunca en las mismas. El trabajo de una persona no debe dañar el de
las demás. Cuando se junta el trabajo de todos, todo debe funcionar en conjunto.
Si un cambio mío puede afectar lo que otro está haciendo, se lo aviso al usuario
antes de tocarlo.
