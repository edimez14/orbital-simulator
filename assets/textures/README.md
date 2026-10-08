<!-- código nuevo edizon -->
# Carpeta `assets/textures/`

Aquí están las **texturas** que usan los cuerpos celestes y el fondo. La guía
completa (fuentes, licencias, nombres y tamaños) está en
`docs/recursos_visuales.md`.

## Contenido actual

| Carpeta | Archivos |
|---------|----------|
| `planets/` | `mercurio.jpg`, `venus.jpg`, `tierra.jpg`, `marte.jpg`, `jupiter.jpg`, `saturno.jpg`, `saturno_anillo.png`, `urano.jpg`, `neptuno.jpg` |
| `moons/` | `luna.jpg` |
| `stars/` | `sol.jpg` |
| `background/` | `fondo_estelar.jpg` |

Todas son de **Solar System Scope**, licencia **CC BY 4.0** (ver créditos en la
guía).

## Reglas rápidas

- Nombres en minúsculas, sin espacios ni tildes.
- Mapas de planetas en proporción **2:1** y dimensiones **potencia de 2**
  (2048×1024).
- `.jpg` para color; `.png` solo si necesitas transparencia.

## Cómo se usan en el código

Se referencian desde `src/render/scene3d.py` con el argumento `texture=`, por
ejemplo `texture="assets/textures/planets/tierra.jpg"`.

Si falta una textura, el simulador funciona igual: usa solo el `color` de cada
cuerpo.

## Volver a descargarlas

```bash
bash scripts/descargar_texturas.sh
```
