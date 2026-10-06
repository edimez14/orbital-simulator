<!-- código nuevo edizon -->
# Distribución — Usar el simulador en cualquier parte

Objetivo: que cualquier persona pueda abrir el simulador **sin instalar Python**
ni librerías. Se logra con un **ejecutable creado por PyInstaller**.

## Por qué un ejecutable y no Docker

VPython 7 no abre una ventana nativa: corre un **servidor local** y muestra la
escena 3D en el **navegador**. Un ejecutable de escritorio encaja directo con eso
(el usuario hace doble clic y se abre el navegador). Docker obligaría al usuario a
tenerlo instalado y a manejar el puerto del servidor a mano.

## Archivos que intervienen

| Archivo | Para qué sirve |
|---------|----------------|
| `orbital_simulator.spec` | Receta de PyInstaller (punto de entrada + qué incluir). |
| `build_hooks/hook-vpython.py` | Incluye los archivos internos de VPython. |
| `requirements-dev.txt` | Incluye `pyinstaller` para poder compilar. |
| `.github/workflows/build-installers.yml` | Compila para Windows, macOS y Linux. |

## Cómo compilar en tu máquina

```bash
pip install -r requirements-dev.txt
pyinstaller orbital_simulator.spec
```

El resultado queda en `dist/orbital-simulator/`. Esa carpeta se copia a otra
máquina y se ejecuta `orbital-simulator` (Linux/macOS) o
`orbital-simulator.exe` (Windows).

## Cómo se generan los tres sistemas

PyInstaller **no compila cruzado**: el `.exe` de Windows solo se crea en Windows.
Por eso el workflow `.github/workflows/build-installers.yml` corre en los tres
sistemas y publica un paquete por cada uno.

Para lanzarlo:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Luego, en GitHub → pestaña **Actions**, se descarga cada paquete.

## Un solo archivo vs carpeta

La receta actual genera una **carpeta** (más confiable y rápida al abrir). Si se
prefiere un **único archivo**, se ajusta la receta `orbital_simulator.spec`
(ver los comentarios dentro del archivo).

## Nota importante

VPython usa el navegador para mostrar la escena 3D. El ejecutable necesita que la
máquina tenga un navegador (cualquiera tiene uno). No requiere pantalla especial
ni dependencias de sistema.

## Estado

Andamiaje listo. La compilación real se prueba cuando `src/main.py` tenga código
funcional.
