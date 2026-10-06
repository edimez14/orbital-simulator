<!-- código nuevo edizon -->
# Carpeta `assets/textures/`

Aquí van todas las **texturas** que usan los cuerpos celestes y el fondo. La guía
completa (fuentes, licencias, nombres y tamaños) está en
`docs/recursos_visuales.md`.

## Subcarpetas

| Carpeta | Qué guardar | Ejemplo |
|---------|-------------|---------|
| `planets/` | Mapas de planetas (2:1) y anillos | `earth.jpg`, `mars.jpg`, `saturn_ring.png` |
| `moons/` | Lunas | `moon.jpg` |
| `stars/` | Sol y estrellas | `sun.jpg` |
| `background/` | Fondo estelar / Vía Láctea | `milkyway.jpg` |

## Reglas rápidas

- Nombres en minúsculas, sin espacios ni tildes.
- Mapas de planetas en proporción **2:1** y dimensiones **potencia de 2**
  (2048×1024 es ideal).
- `.jpg` para color; `.png` solo si necesitas transparencia.

## Cómo se usan en el código

Se referencian desde `src/render/scene3d.py` con el argumento `texture=`, por
ejemplo `texture="assets/textures/planets/earth.jpg"`.

Mientras no haya texturas, el simulador funciona igual: usa solo el `color` de
cada cuerpo.
