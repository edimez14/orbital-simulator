# código nuevo edizon
"""hook-vpython.py — Hook de PyInstaller para VPython.

¿Para qué sirve?
    Indicarle a PyInstaller qué archivos y submodulos de VPython hay que incluir
    en el ejecutable. Sin esto, la escena 3D no encuentra sus archivos.

¿Por qué existe?
    VPython guarda plantillas y librerias JavaScript/WebGL que no se detectan
    solas al analizar los `import`. Este hook las recoge.

¿Cómo funciona paso a paso?
    1. `collect_data_files('vpython')` reúne los archivos de datos (plantillas,
       scripts JS, etc.).
    2. `collect_submodules('vpython')` incluye todos los submodulos para evitar
       que falte alguno.

¿Cómo se activa?
    PyInstaller lo carga solo, porque la receta `orbital_simulator.spec` declara
    esta carpeta en `hookspath`. El nombre DEBE empezar por `hook-` y terminar en
    el nombre del modulo (`vpython`).

¿Cómo modificarlo?
    - Si falta una libreria relacionada (por ejemplo `glowscript`), agregar otra
      llamada a `collect_data_files` con su nombre.
    - No poner logica de la simulacion aqui; es solo empaquetado.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Archivos de datos (plantillas y librerias web de VPython).
datas = collect_data_files("vpython")

# Todos los submodulos, para no depender de que el analisis los vea.
hiddenimports = collect_submodules("vpython")
