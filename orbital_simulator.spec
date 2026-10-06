# código nuevo edizon
# -*- mode: python ; coding: utf-8 -*-
"""orbital_simulator.spec — Receta de PyInstaller para el instalador.

¿Para qué sirve?
    Le dice a PyInstaller cómo empaquetar el simulador en un ejecutable que
    funcione SIN tener Python instalado. Es la receta del "instalador".

¿Por qué existe?
    PyInstaller no adivina todo. Este archivo declara el punto de entrada, los
    hooks y los datos que hay que incluir (sobre todo los de VPython).

¿Cómo se usa?
    Desde la raiz del proyecto:
        pyinstaller orbital_simulator.spec
    El resultado queda en dist/orbital-simulator/.

¿Cómo funciona paso a paso?
    1. Analysis   : lee src/main.py y descubre los modulos y datos necesarios.
    2. PYZ        : empaqueta el bytecode de Python.
    3. EXE        : construye el ejecutable.
    4. COLLECT    : junta el ejecutable con sus archivos en una carpeta.

Nota sobre VPython (importante)
    VPython 7 corre un servidor local y manda la escena 3D a un navegador. Sus
    archivos internos (JavaScript/WebGL) hay que incluirlos aparte; por eso se usa
    el hook en build_hooks/hook-vpython.py.

¿Cómo modificarlo?
    - Cambiar el icono: reemplazar `icon=` por la ruta de un .ico/.icns.
    - Pasar a un solo archivo: usar EXE con `a.binaries` y `a.datas` incluidos
      y quitar el COLLECT (mas portable, pero mas lento al abrir).
    - Anadir datos (por ejemplo data/presets.json): agregarlos a `datas`.

ESTADO: andamiaje. Se completa y prueba cuando main.py tenga codigo funcional.
"""

import os

# Carpeta con los hooks personalizados (por ejemplo el de VPython).
# SPECPATH es una variable que PyInstaller inyecta al leer este archivo.
hook_dir = os.path.join(SPECPATH, "build_hooks")

# 1. Analisis: punto de entrada y que incluir.
a = Analysis(
    ["src/main.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[hook_dir],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
