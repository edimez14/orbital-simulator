#!/usr/bin/env python3
# código nuevo edizon
# ---------------------------------------------------------------------------
# generar_pdf.py
#
# ¿Para qué sirve?
#   Convierte un archivo Markdown (.md) a PDF manteniendo títulos, listas y
#   tablas.
#
# ¿Por qué existe?
#   El informe y el plan se escriben en Markdown (fácil de leer y de versionar)
#   pero a veces hace falta una versión en PDF para entregar o imprimir.
#
# ¿Cómo se usa?
#   Primero instalar las librerías:   pip install fpdf2 markdown
#   Luego, desde la raíz del proyecto:
#       python scripts/generar_pdf.py docs/plan_de_desarrollo.md
#   Si no se indica un archivo, convierte el plan por defecto. Si no se indica
#   salida, deja el PDF al lado del .md (mismo nombre, extensión .pdf).
#
# ¿Cómo funciona paso a paso?
#   1. Lee el archivo Markdown.
#   2. Le quita los comentarios HTML (no se imprimen).
#   3. Convierte el texto a HTML.
#   4. Arma el PDF con una fuente que sí soporta tildes y símbolos.
#   5. Guarda el PDF.
#
# ¿Cómo modificarlo?
#   - Cambiar la fuente: editar la carpeta FONT_DIRS (busca una que exista).
#   - Cambiar el formato de página: editar format="A4".
# ---------------------------------------------------------------------------
import re
import sys
import warnings
from pathlib import Path

import markdown
from fpdf import FPDF

# fpdf2 avisa que algunos parámetros del HTML cambiarán de nombre en el futuro.
# Aquí se silencia ese aviso para que la salida quede limpia.
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Carpetas donde suelen estar las fuentes DejaVu (soporta tildes y símbolos).
FONT_DIRS = [
    Path("/usr/share/fonts/TTF"),
    Path("/usr/share/fonts/truetype/dejavu"),
]
ARCHIVO_POR_DEFECTO = Path("docs/plan_de_desarrollo.md")


def encontrar_fuente(nombre: str) -> Path:
    """Devuelve la ruta de una fuente buscando en las carpetas conocidas.

    Se recorre FONT_DIRS y se devuelve la primera coincidencia. Si no se
    encuentra, se avisa y se detiene, porque el PDF sin tildes no sirve.
    """
    for carpeta in FONT_DIRS:
        ruta = carpeta / nombre
        if ruta.exists():
            return ruta
    raise FileNotFoundError(
        f"No se encontró la fuente {nombre}. Instala las fuentes DejaVu."
    )


def limpiar_celdas(html: str) -> str:
    """Quita las etiquetas de formato dentro de las celdas de tabla.

    El motor de PDF no acepta etiquetas como `<code>` o `<b>` dentro de una celda
    (falla al leer la tabla). Como el formato en las celdas es solo estético, se
    deja el texto plano para que la tabla siempre se pueda imprimir.
    """
    def limpiar(match: "re.Match[str]") -> str:
        etiqueta, contenido = match.group(1), match.group(2)
        contenido = re.sub(r"</?[^>]+>", "", contenido)
        return f"<{etiqueta}>{contenido}</{etiqueta}>"

    return re.sub(r"<(td|th)>(.*?)</\1>", limpiar, html, flags=re.DOTALL)


def convertir_markdown_a_pdf(origen: Path, destino: Path) -> None:
    """Convierte el archivo Markdown `origen` en el PDF `destino`."""
    print(f"[leyendo]  {origen}")
    texto = origen.read_text(encoding="utf-8")

    # Los comentarios HTML (por ejemplo el marcador de código nuevo) no se
    # imprimen; se quitan antes de convertir.
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)

    html = markdown.markdown(
        texto,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    html = limpiar_celdas(html)

    pdf = FPDF(format="A4")
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_font("DejaVu", "", str(encontrar_fuente("DejaVuSans.ttf")))
    pdf.add_font("DejaVu", "B", str(encontrar_fuente("DejaVuSans-Bold.ttf")))
    pdf.add_font("DejaVu", "I", str(encontrar_fuente("DejaVuSans-Oblique.ttf")))
    pdf.set_font("DejaVu", size=11)
    pdf.add_page()
    # font_family y pre_code_font usan DejaVu para que las tildes, los símbolos
    # y los caracteres de árbol (├, └) se impriman bien.
    pdf.write_html(
        html,
        font_family="DejaVu",
        pre_code_font="DejaVu",
        table_line_separators=True,
        heading_sizes={"h1": 19, "h2": 15, "h3": 13, "h4": 12},
    )
    pdf.output(str(destino))
    print(f"[listo]    PDF en {destino}")


def main() -> None:
    origen = Path(sys.argv[1]) if len(sys.argv) > 1 else ARCHIVO_POR_DEFECTO
    destino = Path(sys.argv[2]) if len(sys.argv) > 2 else origen.with_suffix(".pdf")

    if not origen.exists():
        print(f"[error]    No existe el archivo {origen}")
        sys.exit(1)

    convertir_markdown_a_pdf(origen, destino)


if __name__ == "__main__":
    main()
