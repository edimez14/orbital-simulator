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
su subcarpeta:

```
assets/
├── README.md
└── textures/
    ├── README.md
    ├── planets/       # mapas de planetas (2:1)
    ├── moons/         # lunas
    ├── stars/         # Sol y estrellas
    └── background/    # fondo estelar / Vía Láctea
```

### Convenciones de nombre

- Todo en minúsculas, sin espacios ni tildes: `earth.jpg`, `mars.jpg`.
- Color del planeta: `planets/<nombre>.jpg`.
- Anillos (con transparencia): `planets/saturn_ring.png`.
- Fondo: `background/milkyway.jpg`.

### Formato y tamaño

- **Mapas de planetas = equirectangulares, proporción 2:1** (por ejemplo
  2048×1024). Así se envuelven bien en una esfera.
- Dimensiones en **potencias de 2** (1024, 2048, 4096). Si no lo son, VPython
  estira la imagen.
- Usa `.jpg` para color (pesa menos). Usa `.png` solo cuando necesites
  transparencia (anillos, nubes).
- Evita 8K: pesa mucho y no se nota. **2048×1024 es suficiente**.

---

## 4. De dónde sacarlas (gratis y legales)

| Fuente | Qué trae | Licencia |
|--------|----------|----------|
| **Solar System Scope** — https://www.solarsystemscope.com/textures/ | Todos los planetas en 2K/4K/8K, anillos de Saturno, fondo estelar | CC BY 4.0 (dar crédito) |
| **NASA Visible Earth** — https://visibleearth.nasa.gov/ | Tierra, nubes, mapas reales | Dominio público |
| **NASA Image Library** — https://images.nasa.gov/ | Sol, planetas, naves | Dominio público |
| **ESO Milky Way panorama** — https://www.eso.org/public/images/eso0932a/ | Foto de la Vía Láctea para el fondo | CC BY 4.0 |
| **Wikimedia Commons** — https://commons.wikimedia.org/ | Variado (planetas, lunas, cometas) | Revisar cada archivo |
| **Planet Pixel Emporium** — http://planetpixelemporium.com/planets.html | Texturas de planetas | Revisar licencia en el sitio |

### Cómo leer las licencias

- **Dominio público**: libre, sin condiciones.
- **CC BY 4.0**: libre, pero hay que **dar crédito** (anótalo en la sección 9).
- **Cualquier otra**: revisar antes de usar. Si no dice nada claro, no la uses.

Recuerda: **Solar System Scope es la fuente más rápida**. Trae casi todo lo que
necesitas en un solo lugar.

---

## 5. Cómo descargarlas (paso a paso)

1. Entra a **Solar System Scope** (`solarsystemscope.com/textures`).
2. Descarga la versión de **2K** de cada planeta que vayas a usar.
3. Descarga el **fondo estelar** y, si usas Saturno, su **anillo**.
4. Renombra cada archivo según la sección 3 (`earth.jpg`, `mars.jpg`, etc.).
5. Guárdalos en la subcarpeta que corresponde dentro de `assets/textures/`.
6. Si una imagen no es potencia de 2, redimensiónala (con GIMP, o en línea).

No necesitas todos los planetas de una. Empieza con **Sol, Tierra y uno o dos
más**; agrega el resto después.

---

## 6. Cómo usarlas en el código

- La textura se pasa con el argumento `texture=`.
- Si el archivo está en `assets/textures/planets/earth.jpg`, se usa esa ruta.
- Espera a que carguen con `scene.waitfor("textures")` para que no aparezcan a
  medias.
- **Diseño a prueba de fallos**: si la textura no existe, usa solo el `color`.
  Así el simulador se ve bien aunque todavía no hayas descargado nada.

```python
# código nuevo edizon
from vpython import sphere, vector, color

# Con textura si existe; si no, solo color.
earth = sphere(
    pos=vector(5, 0, 0),
    radius=0.15,
    color=color.blue,          # respaldo si falta la textura
    texture="assets/textures/planets/earth.jpg",
)
```

### Empaquetado (PyInstaller)

Cuando el programa se empaquete en un ejecutable, las texturas deben ir dentro.
Hay que agregar la carpeta a `datas` en `orbital_simulator.spec` y resolver la
ruta con `sys._MEIPASS` cuando el programa está congelado. Se deja anotado aquí
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
- El fondo estrellado con `points` es casi gratis; úsalo en vez de muchas esferas.
- Texturas de 2K: suficiente. Evita 8K.

---

## 9. Créditos y licencias (llenar al descargar)

| Archivo | Fuente | Licencia | Autor / crédito |
|---------|--------|----------|-----------------|
| (ej.) `planets/earth.jpg` | Solar System Scope | CC BY 4.0 | Solar System Scope |
|  |  |  |  |
|  |  |  |  |

Completar esta tabla es la forma de cumplir CC BY. Sirve también para el informe.

---

## 10. Prioridad (lo dice el PDF)

La sección 5.3 deja el 3D casi al final (**paso 8**): "no inviertas tiempo en 3D
bonito antes de tener conservación de energía funcionando". Primero la física;
la estética después.
