#!/usr/bin/env bash
# código nuevo edizon
# ---------------------------------------------------------------------------
# descargar_texturas.sh
#
# ¿Para qué sirve?
#   Descarga las texturas de los cuerpos celestes y el fondo, y las guarda ya
#   renombradas en español dentro de assets/textures/.
#
# ¿Por qué existe?
#   Para no bajarlas una por una a mano y dejar registrado de dónde sale cada
#   archivo. Fuente: Solar System Scope (https://www.solarsystemscope.com/textures/),
#   licencia CC BY 4.0 (se debe dar crédito; ver docs/recursos_visuales.md).
#
# ¿Cómo se usa?
#   Desde la raíz del proyecto:
#       bash scripts/descargar_texturas.sh
#   Si un archivo ya existe, se salta y no lo vuelve a bajar.
#
# ¿Cómo modificarlo?
#   Agregar o quitar líneas en el arreglo ARCHIVOS con el formato
#   "nombre_origen|ruta_destino".
# ---------------------------------------------------------------------------
set -euo pipefail

BASE="https://www.solarsystemscope.com/textures/download"
DEST="assets/textures"

ARCHIVOS=(
  "2k_sun.jpg|stars/sol.jpg"
  "2k_mercury.jpg|planets/mercurio.jpg"
  "2k_venus_surface.jpg|planets/venus.jpg"
  "2k_earth_daymap.jpg|planets/tierra.jpg"
  "2k_moon.jpg|moons/luna.jpg"
  "2k_mars.jpg|planets/marte.jpg"
  "2k_jupiter.jpg|planets/jupiter.jpg"
  "2k_saturn.jpg|planets/saturno.jpg"
  "2k_saturn_ring_alpha.png|planets/saturno_anillo.png"
  "2k_uranus.jpg|planets/urano.jpg"
  "2k_neptune.jpg|planets/neptuno.jpg"
  "2k_stars_milky_way.jpg|background/fondo_estelar.jpg"
)

for item in "${ARCHIVOS[@]}"; do
  origen="${item%%|*}"
  destino="${item##*|}"
  ruta="${DEST}/${destino}"
  mkdir -p "$(dirname "$ruta")"

  if [ -f "$ruta" ]; then
    echo "[existe]  $ruta"
    continue
  fi

  echo "[bajando] $destino"
  curl -sL --max-time 120 "${BASE}/${origen}" -o "$ruta"
  echo "[listo]   $ruta"
done

echo "Terminado. Texturas en $DEST"
