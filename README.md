# Orbital Simulator — Leyes de Kepler

Simulador computacional interactivo en **Python** que modela el movimiento orbital de
uno o varios cuerpos bajo **gravitación universal**. Permite identificar órbitas
circulares, elípticas e hiperbólicas y verifica cuantitativamente la conservación de
energía y momento angular, además de las tres leyes de Kepler.

Proyecto académico de Física Mecánica — Grupo 6 — Taller 19.
Basado en `docs/Pre-Proyecto Grupo 6.pdf` y en `docs/plan_de_desarrollo.md`.

## Objetivo

Construir un simulador que no solo se vea bien, sino que sea **físicamente
verificable**: debe conservar energía y momento angular dentro de una tolerancia
(1 %) y demostrar las leyes de Kepler con datos reproducibles.

## Tecnologías

| Componente           | Librería                                  |
|----------------------|-------------------------------------------|
| Cálculos numéricos   | NumPy                                     |
| Integración          | Código propio (Euler-Cromer y Verlet)     |
| Interfaz y gráficas  | Plotly + Dash (panel web)                 |
| Pruebas              | pytest                                    |
| Empaquetado          | PyInstaller                               |

## Unidades

Todo el proyecto usa el **Sistema Internacional**:

- distancia: metros (m)
- masa: kilogramos (kg)
- tiempo: segundos (s)

La interfaz muestra el tiempo en **días**. Con estas unidades,
`G = 6.674e-11 m³·kg⁻¹·s⁻²`.

## Punto crítico de diseño

El **loop de física corre independiente del renderizado** (`src/simulation.py`). La
física nunca se calcula dentro de la función que dibuja: la interfaz pide una corrida
y recibe el historial.

## Cómo ejecutar

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m src.main
```

Luego abre `http://127.0.0.1:8050` y pulsa **Iniciar Simulación**.

El uso paso a paso está en `docs/manual_de_usuario.md`.

## Qué se puede hacer en el panel

- **Elegir el tipo de trayectoria**: circular, elíptica o hiperbólica (ajusta la
  velocidad del cuerpo que orbita).
- **Editar los cuerpos**: nombre, masa, posición y velocidad; agregar y eliminar.
- **Elegir el método numérico**: Euler-Cromer o Verlet.
- **Ajustar** el paso de tiempo y el tiempo total.
- Ver la **velocidad circular y la de escape** mientras se edita.
- Ver la **vista 3D**, la trayectoria 2D, la energía (total, cinética y potencial),
  el momento angular y la verificación de Kepler.
- Leer las **tarjetas de resultados** y la **tabla de datos**.

## Pruebas

Un solo framework (**pytest**):

```bash
pytest                    # todas las pruebas
pytest tests/scenarios    # solo los escenarios (circular, elíptica, hiperbólica)
pytest --cov=src          # con cobertura
```

## Estructura de carpetas

```
orbital-simulator/
├── src/
│   ├── physics/       ¿cómo interactúan los cuerpos?
│   │   ├── bodies.py
│   │   ├── gravity.py
│   │   └── conservation.py
│   ├── integrators/   ¿cómo avanza el tiempo?
│   │   ├── euler_cromer.py
│   │   └── verlet.py
│   ├── kepler/        ¿se cumplen las leyes?
│   │   └── kepler_laws.py
│   ├── simulation.py  motor: corre el loop y arma el historial
│   ├── ui/            interfaz web
│   │   ├── app.py         panel (Dash)
│   │   ├── figures.py     figuras (Plotly)
│   │   └── controls.py    velocidad de escape (queda de la etapa VPython)
│   ├── render/        módulos de la etapa VPython (por retirar)
│   │   ├── plots.py
│   │   └── scene3d.py
│   └── main.py        lanzador de la interfaz
├── tests/             pruebas unitarias y de escenarios
├── data/presets.json  escenarios con datos reales
├── docs/              informe, guías, plan y tareas
├── assets/            estilo del panel y texturas
└── requirements.txt / requirements-dev.txt
```

## Datos iniciales

`data/presets.json` trae escenarios con datos reales (kg, m, m/s):

- `tierra_luna` — la Tierra como cuerpo primario y la Luna orbitando.
- `sol_tierra` — el Sol y la Tierra.
- `sol_sistema_interno` — el Sol y los cuatro planetas interiores.

## Estado actual

Hechas las tareas 1 a 10 de `docs/tareas_cambios.md` (física en SI, datos reales,
motor con métodos, historial, panel, vista 3D, gráficas, edición de cuerpos, tipos de
trayectoria y resultados). Quedan la documentación fina (tarea 11) y el empaquetado
(tarea 12).

Los módulos de la etapa VPython (`render/scene3d.py` y el `Controls` de
`ui/controls.py`) quedan por retirar; `ui/controls.py` todavía aporta
`escape_velocity`, que usa la interfaz.

## Cómo modificar el proyecto

- Añadir una ley o métrica → nuevo archivo en `kepler/` y su prueba en `tests/`.
- Cambiar el método numérico → nuevo archivo en `integrators/` y una línea en
  `simulation.py`.
- Cambiar la interfaz → `src/ui/app.py`; el estilo, en `assets/style.css`.
- Cambiar los escenarios → `data/presets.json`.

## Repositorio

```
git@github.com:edimez14/orbital-simulator.git
```
