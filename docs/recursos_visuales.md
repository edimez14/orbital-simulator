<!-- código nuevo edizon -->
# Recursos visuales y texturas

Guía única para conseguir y colocar **todo lo que se ve en el simulador**:
planetas, Sol, estrellas de fondo, lunas y demás cuerpos celestes.

---

## 1. Regla de oro: VPython NO carga modelos 3D

VPython solo trabaja con **primitivas** (formas básicas). **No** puede importar
archivos OBJ, GLTF, FBX ni STL.

Consecuencia práctica: **no pierdas tiempo buscando modelos 3D** en Sketchfab,
Blender o packs de mallas. Aquí no funcionan. La forma rápida, óptima y que se ve
bien es **primitivas + texturas gratis**.

Si algún día se quisiera usar modelos 3D reales, habría que cambiar de motor
(Panda3D, Ursina, Godot). Eso está fuera del alcance actual del proyecto.

---

## 2. Qué primitiva usar para cada cosa

| Lo que quieres | Primitiva de VPython |
|----------------|----------------------|
| Planetas, Luna, Sol | `sphere` + `color` + `texture` |
| Sol y estrellas que brillan | `sphere(emissive=True)` |
| Cielo estrellado | `points` (procedural, sin archivos) o esfera gigante con textura |
| Trayectoria orbital | `curve` |
| Ejes y rejilla | `box` o `curve` |
| Nombre del cuerpo | `label` |
| Anillos (Saturno) | `ring` |
| Vector velocidad / fuerza | `arrow` |
| Nave o sonda | `compound` (varias primitivas unidas) |

---

## 3. Dónde guardar las texturas

Todas las texturas van dentro de la carpeta **`assets/textures/`**, cada tipo en
su subcarpeta. **Ya están descargadas y ordenadas:**

```
assets/
└── textures/
    ├── planets/
    │   ├── mercurio.jpg
    │   ├── venus.jpg
    │   ├── tierra.jpg
    │   ├── marte.jpg
    │   ├── jupiter.jpg
    │   ├── saturno.jpg
    │   ├── saturno_anillo.png
    │   ├── urano.jpg
    │   └── neptuno.jpg
    ├── moons/
    │   └── luna.jpg
    ├── stars/
    │   └── sol.jpg
    └── background/
        └── fondo_estelar.jpg
```

### Convenciones de nombre

- Todo en minúsculas, **sin espacios ni tildes**: `tierra.jpg`, `marte.jpg`.
- Color del planeta: `planets/<nombre>.jpg`.
- Anillos (con transparencia): `planets/saturno_anillo.png`.
- Fondo: `background/fondo_estelar.jpg`.

### Formato y tamaño

- Los mapas de planetas son **equirectangulares, proporción 2:1** (2048×1024).
  Así se envuelven bien en una esfera.
- Dimensiones en **potencias de 2** (1024, 2048, 4096).
- `.jpg` para color. `.png` solo cuando hace falta transparencia (el anillo de
  Saturno).
- Tamaño actual: cada mapa pesa ~450 KB; el total de la carpeta es ~5.9 MB.
- Evita 8K: pesa mucho y no se nota.

---

## 4. De dónde sacarlas (gratis y legales)

| Fuente | Qué trae | Licencia |
|--------|----------|----------|
| **Solar System Scope** — https://www.solarsystemscope.com/textures/ | Todos los planetas en 2K/4K/8K, anillo de Saturno, fondo estelar | CC BY 4.0 (dar crédito) |
| **NASA Visible Earth** — https://visibleearth.nasa.gov/ | Tierra, nubes, mapas reales | Dominio público |
| **NASA Image Library** — https://images.nasa.gov/ | Sol, planetas, naves | Dominio público |
| **ESO Milky Way panorama** — https://www.eso.org/public/images/eso0932a/ | Foto de la Vía Láctea para el fondo | CC BY 4.0 |
| **Wikimedia Commons** — https://commons.wikimedia.org/ | Variado (planetas, lunas, cometas) | Revisar cada archivo |

### Cómo leer las licencias

- **Dominio público**: libre, sin condiciones.
- **CC BY 4.0**: libre, pero hay que **dar crédito** (ver sección 9).
- **Cualquier otra**: revisar antes de usar. Si no dice nada claro, no la uses.

**Fuente más rápida: Solar System Scope.** Es la que se usó para descargar todo.

---

## 5. Cómo descargarlas (o volver a descargarlas)

Las texturas **ya están en el proyecto**. Para bajarlas de nuevo o en otro
computador, se usa el script, que las deja renombradas en español:

```bash
bash scripts/descargar_texturas.sh
```

El script (en `scripts/descargar_texturas.sh`) salta los archivos que ya existen,
así que se puede correr sin miedo. Para agregar o quitar texturas, se edita la
lista `ARCHIVOS` dentro del script.

---

## 6. Cómo usarlas en el código

- La textura se pasa con el argumento `texture=`.
- Si el archivo está en `assets/textures/planets/tierra.jpg`, se usa esa ruta.
- Espera a que carguen con `scene.waitfor("textures")` para que no aparezcan a
  medias.
- **Diseño a prueba de fallos**: si la textura no existe, usa solo el `color`.
  Así el simulador se ve bien aunque falte algún archivo.

```python
# código nuevo edizon
from vpython import sphere, vector, color

# Con textura si existe; si no, solo color.
tierra = sphere(
    pos=vector(5, 0, 0),
    radius=0.15,
    color=color.blue,          # respaldo si falta la textura
    texture="assets/textures/planets/tierra.jpg",
)
```

### Empaquetado (PyInstaller)

Cuando el programa se empaquete en un ejecutable, las texturas deben ir dentro.
Hay que agregar `assets/textures` a `datas` en `orbital_simulator.spec` y resolver
la ruta con `sys._MEIPASS` cuando el programa está congelado. Se deja anotado aquí
para cuando toque compilar.

---

## 7. Escala visual (importante para la física)

En el sistema solar real los planetas son invisibles frente a las distancias. No
se puede usar escala real. Se usa un **factor de escala de dibujo** (por ejemplo,
tamaños comprimidos con logaritmo).

**Regla del proyecto**: el tamaño en pantalla NO es el físico. Esto debe quedar
claro para no confundir el análisis. La posición sí respeta la física; el tamaño
visible es solo para poder verlo.

---

## 8. Rendimiento

- Crea cada objeto UNA vez y solo actualiza su `pos`. Nunca crees objetos dentro
  del bucle de dibujo.
- Las trayectorias (`curve`) con demasiados puntos se vuelven lentas: guarda cada
  N pasos (submuestreo).
- El fondo estelado con `points` es casi gratis; úsalo en vez de muchas esferas.
- Texturas de 2K: suficiente. Evita 8K.

---

## 9. Créditos y licencias

Todas las texturas descargadas provienen de **Solar System Scope** y están bajo
licencia **CC BY 4.0**. Se debe dar crédito así:

> Texturas planetarias: [Solar System Scope](https://www.solarsystemscope.com/textures/),
> licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

| Archivo | Fuente | Licencia |
|---------|--------|----------|
| `planets/mercurio.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/venus.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/tierra.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/marte.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/jupiter.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/saturno.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/saturno_anillo.png` | Solar System Scope | CC BY 4.0 |
| `planets/urano.jpg` | Solar System Scope | CC BY 4.0 |
| `planets/neptuno.jpg` | Solar System Scope | CC BY 4.0 |
| `moons/luna.jpg` | Solar System Scope | CC BY 4.0 |
| `stars/sol.jpg` | Solar System Scope | CC BY 4.0 |
| `background/fondo_estelar.jpg` | Solar System Scope | CC BY 4.0 |

---

## 10. Sonido e interface (UI): lo que VPython NO puede

Importante para no descargar cosas que no se pueden usar:

- **Sonido**: VPython **no reproduce audio**. Para usar sonidos habría que añadir
  otra librería (por ejemplo `pygame.mixer`) que el proyecto todavía no tiene y
  que no aporta a la verificación de las leyes de Kepler.
- **UI/UX**: la interface de VPython son **controles nativos hechos con código**
  (sliders, botones, menús, casillas), no imágenes. No hay iconos ni fondos de
  aplicación que descargar.

Por eso no se descargaron sonidos ni imágenes de interface.

---

## 11. Prioridad (lo dice el PDF)

La sección 5.3 deja el 3D casi al final (**paso 8**): "no inviertas tiempo en 3D
bonito antes de tener conservación de energía funcionando". Primero la física;
la estética después.
