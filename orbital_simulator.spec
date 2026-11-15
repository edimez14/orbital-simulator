# código nuevo edizon
# -*- mode: python ; coding: utf-8 -*-
"""orbital_simulator.spec — Receta de PyInstaller para el instalador.

¿Para qué sirve?
    Le dice a PyInstaller cómo empaquetar el simulador en un ejecutable que
    funcione SIN tener Python instalado.

¿Por qué existe?
    PyInstaller no adivina todo. Este archivo declara el punto de entrada y los
    datos que hay que incluir: la interfaz (Dash y Plotly), la carpeta `assets/`
    (estilo del panel) y `data/` (escenarios).

¿Cómo se usa?
    Desde la raíz del proyecto:
        pyinstaller orbital_simulator.spec
    El resultado queda en dist/orbital-simulator/.

¿Cómo funciona paso a paso?
    1. Analysis   : lee src/main.py y descubre los módulos y datos necesarios.
    2. PYZ        : empaqueta el bytecode de Python.
    3. EXE        : construye el ejecutable.
    4. COLLECT    : junta el ejecutable con sus archivos en una carpeta.

¿Cómo modificarlo?
    - Cambiar el icono: reemplazar `icon=` por la ruta de un .ico/.icns.
    - Pasar a un solo archivo: usar EXE con `a.binaries` y `a.datas` incluidos
      y quitar el COLLECT (más portable, pero más lento al abrir).
"""

from PyInstaller.utils.hooks import collect_all

# Dash y Plotly traen archivos web (JavaScript y plantillas) que no se detectan
# solos al analizar los `import`.
dash_datas, dash_binaries, dash_hiddenimports = collect_all("dash")
plotly_datas, plotly_binaries, plotly_hiddenimports = collect_all("plotly")

# 1. Análisis: punto de entrada y qué incluir.
a = Analysis(
    ["src/main.py"],
    pathex=[],
    binaries=dash_binaries + plotly_binaries,
    datas=dash_datas + plotly_datas + [("assets", "assets"), ("data", "data")],
    hiddenimports=dash_hiddenimports + plotly_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # VPython y Matplotlib quedaron de etapas anteriores; no los usa la interfaz.
    excludes=["vpython", "matplotlib", "tkinter", "IPython", "jupyter", "pytest"],
    noarchive=False,
)

# 2. Empaquetado del bytecode.
pyz = PYZ(a.pure)

# 3. Ejecutable.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="orbital-simulator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # se mantiene la consola para ver registros y errores
)

# 4. Carpeta final con el ejecutable y sus archivos.
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="orbital-simulator",
)
