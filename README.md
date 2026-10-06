<!-- código nuevo edizon -->
# Orbital Simulator — Leyes de Kepler

Simulador computacional interactivo en **Python** que modela el movimiento orbital de
uno o varios cuerpos bajo **gravitación universal**. Permite identificar órbitas
circulares, elípticas e hiperbólicas y verifica cuantitativamente la conservación de
energía y momento angular, además de las tres leyes de Kepler.

Proyecto académico de Física Mecánica — Grupo 6 — Taller 19.
Basado en `docs/Pre-Proyecto Grupo 6.pdf`.

## Objetivo

Construir un simulador que no solo se vea bien, sino que sea **físicamente
verificable**: debe conservar energía y momento angular dentro de una tolerancia
(por ejemplo 1 %) y demostrar las leyes de Kepler con datos reproducibles.

## Tecnologías

| Componente        | Librería            |
|-------------------|---------------------|
| Cálculos numéricos| NumPy               |
| Integración       | Código propio (Euler-Cromer y Verlet) |
| Visualización 3D  | VPython             |
| Gráficas de análisis | Matplotlib       |
| Interfaz de controles | Controles nativos de VPython |

## Unidades

Se usan **unidades astronómicas normalizadas** (AU, masas solares, años) para evitar
números gigantes y errores de precisión de punto flotante. El código debe mantener una
**sola convención interna** y no mezclar SI con unidades astronómicas sin conversión
explícita.

## Estructura de carpetas

```
orbital-simulator/
├── src/
│   ├── physics/       # ¿cómo interactúan los cuerpos?
│   │   ├── bodies.py
│   │   ├── gravity.py
│   │   └── conservation.py
│   ├── integrators/   # ¿cómo avanza el tiempo?
│   │   ├── euler_cromer.py
│   │   └── verlet.py
│   ├── kepler/        # ¿se cumplen las leyes?
│   │   └── kepler_laws.py
│   ├── render/        # ¿qué ve el usuario?
│   │   ├── scene3d.py
│   │   └── plots.py
│   ├── ui/            # entradas del usuario
│   │   └── controls.py
│   └── main.py        # orquestador del loop de simulación
├── tests/
│   ├── test_gravity.py        # pruebas unitarias
│   ├── test_integrators.py
│   ├── test_conservation.py
│   ├── test_kepler.py
│   └── scenarios/             # pruebas de escenarios físicos
│       ├── test_scenario_circular.py
│       ├── test_scenario_elliptical.py
│       └── test_scenario_hyperbolic.py
├── data/
│   └── presets.json
├── docs/
│   ├── informe_tecnico.md
│   ├── distribucion.md
│   └── recursos_visuales.md
├── build_hooks/                    # hooks de PyInstaller (VPython)
│   └── hook-vpython.py
├── .github/workflows/              # compila instaladores en CI
│   └── build-installers.yml
├── assets/                         # recursos visuales (opcional)
│   └── textures/                   # planetas, lunas, estrellas, fondo
├── orbital_simulator.spec          # receta del instalador
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

Cada carpeta responde a **una sola pregunta**. No mezclar física con renderizado: si se
acoplan, cualquier error gráfico hace dudar de los cálculos, y el framerate de la
interfaz limita la cantidad de pasos de integración.

## Punto crítico de diseño

El **loop de física corre independiente del renderizado**. La física nunca se calcula
dentro de la función que dibuja. El renderizado lee el estado del historial cada N pasos.
Esto permite correr miles de pasos para verificar Kepler con precisión.

## Cómo ejecutar (cuando esté implementado)

```bash
pip install -r requirements.txt
python src/main.py
```

## Pruebas y control de versiones

Dos tipos de prueba, con un solo framework (**pytest**):

- **Unitarias** (`tests/test_*.py`): verifican una pieza aislada.
- **Escenarios** (`tests/scenarios/`): verifican el sistema completo (circular,
  elíptica, hiperbólica).

```bash
pip install -r requirements-dev.txt
pytest                        # todas las pruebas
pytest tests/scenarios        # solo los escenarios
pytest --cov=src              # con cobertura
```

Para el ignore, el proyecto usa su propio `.gitignore`, que cubre lo universal de
Python y lo propio del simulador. Ese archivo se puede copiar a cualquier otro
proyecto Python como plantilla.

## Repositorio

```
git@github.com:edimez14/orbital-simulator.git
```

```bash
git clone git@github.com:edimez14/orbital-simulator.git
```

## Distribución (usar en cualquier parte)

El objetivo es un **instalador/ejecutable** que funcione sin tener Python
instalado. Se genera con PyInstaller a partir de la receta `orbital_simulator.spec`.

```bash
pip install -r requirements-dev.txt
pyinstaller orbital_simulator.spec
# resultado en dist/orbital-simulator/
```

Como PyInstaller no compila entre sistemas operativos, el workflow
`.github/workflows/build-installers.yml` genera el ejecutable de Windows, macOS y
Linux automáticamente. Detalles y decisiones en `docs/distribucion.md`.

## Recursos visuales

Los cuerpos se dibujan con primitivas de VPython (esferas, curvas, puntos); VPython
no carga modelos 3D externos. Las texturas gratuitas, sus licencias y dónde
guardarlas están en `docs/recursos_visuales.md`.

## Estado actual

Esqueleto del proyecto: los archivos contienen **únicamente documentación**. La lógica
se implementa siguiendo el orden del checklist del PDF (sección 5.3):

1. `bodies.py`
2. `gravity.py`
3. `euler_cromer.py`
4. `conservation.py`
5. `verlet.py`
6. `plots.py`
7. `kepler_laws.py`
8. `scene3d.py`
9. `controls.py`
10. Casos de prueba: circular, elíptica, hiperbólica.

## Cómo modificar el proyecto

- Añadir una nueva ley o métrica → nuevo archivo en `kepler/` y su test en `tests/`.
- Cambiar el método numérico → nuevo archivo en `integrators/` sin tocar `gravity.py`.
- Cambiar la librería 3D → solo se reescribe `render/scene3d.py` y `ui/controls.py`.
- Cambiar presets → solo `data/presets.json`.
