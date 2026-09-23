# -*- coding: utf-8 -*-
"""Pipeline md -> HTML -> PDF (Edge headless).

Rutas resueltas desde la ubicacion de este script (cwd-independiente):
  trabajo/Arquitectura para sistemas IA.md  ->  herramientas/*.html  ->  entregables/*.pdf
Uso:  python herramientas/generar_pdf.py
"""
import re
import sys
import time
import shutil
import tempfile
import subprocess
import pathlib

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "trabajo" / "Arquitectura para sistemas IA.md"
HTML_OUT = ROOT / "herramientas" / "EP1_Equipo1_informe.html"
PDF_OUT = ROOT / "entregables" / "EP1_Equipo1_HigueraDuranSalazar.pdf"
IMG_DIR = "trabajo"  # relativo al HTML (que vive en herramientas/)

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

md_text = SRC.read_text(encoding="utf-8")
body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])

# La imagen vive en trabajo/ pero el HTML se escribe en herramientas/
body = re.sub(
    r'src="([^"]+)"',
    lambda m: m.group(0)
    if m.group(1).startswith(("http", "file:", "..", "/"))
    else f'src="../{IMG_DIR}/{m.group(1)}"',
    body,
)

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>EP1 Equipo 1 - Arquitectura de Sistemas IA</title>
<style>
  @page {{ size: A4; margin: 1.1cm 1.55cm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: Georgia, "Times New Roman", serif; font-size: 10pt;
          line-height: 1.23; color: #111; margin: 0; }}
  h1 {{ font-size: 18pt; text-align: center; margin: 0.5em 0 0.25em; }}
  h2 {{ font-size: 13pt; margin-top: 0.9em; margin-bottom: 0.3em; border-bottom: 1px solid #999;
        padding-bottom: 2px; break-after: avoid; page-break-after: avoid; }}
  h3 {{ font-size: 11.5pt; margin-top: 0.8em; margin-bottom: 0.2em; break-after: avoid; page-break-after: avoid; }}
  h4 {{ font-size: 10.5pt; margin-top: 0.8em; margin-bottom: 0.2em; break-after: avoid; page-break-after: avoid; }}
  p  {{ margin: 0.25em 0; text-align: justify; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0.4em 0; font-size: 8.8pt; }}
  th, td {{ border: 1px solid #666; padding: 2.5px 5px; vertical-align: top; }}
  th {{ background: #eef2f7; text-align: left; }}
  thead {{ display: table-header-group; }}
  tr {{ break-inside: avoid; page-break-inside: avoid; }}
  img {{ max-width: 100%; max-height: 14.5cm; width: auto; height: auto;
         display: block; margin: 0.4em auto; }}
  ul, ol {{ margin: 0.3em 0 0.3em 1.3em; padding-left: 0.3em; }}
  li {{ margin: 0.08em 0; }}
  code {{ font-family: Consolas, monospace; font-size: 9.5pt; background: #f4f4f4; padding: 0 2px; }}
  hr {{ border: none; border-top: 1px solid #aaa; margin: 1em 0; }}
  div[style*="page-break"] {{ break-after: page; page-break-after: always; height: 0; }}
  em {{ font-style: italic; }}
  strong {{ font-weight: bold; }}
</style>
</head>
<body>
{body}
</body>
</html>"""

HTML_OUT.write_text(html, encoding="utf-8")
print("HTML:", HTML_OUT.relative_to(ROOT))

# ---- Imprimir a PDF con Edge headless ----
edge = next((p for p in EDGE_CANDIDATES if pathlib.Path(p).exists()), shutil.which("msedge"))
if not edge:
    sys.exit("ERROR: no se encontro Microsoft Edge")

if PDF_OUT.exists():
    PDF_OUT.unlink()  # asegurar que el conteo no lea un PDF viejo
profile = tempfile.mkdtemp(prefix="edge-pdf-")
try:
    proc = subprocess.run(
        [
            edge,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={PDF_OUT}",
            HTML_OUT.as_uri(),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    for _ in range(40):  # Edge puede tardar un pelin en cerrar el archivo
        if PDF_OUT.exists() and PDF_OUT.stat().st_size > 0:
            break
        time.sleep(0.5)
    if not PDF_OUT.exists() or PDF_OUT.stat().st_size == 0:
        sys.exit(f"ERROR: Edge no genero el PDF (exit={proc.returncode})\n{proc.stderr[-500:]}")
finally:
    shutil.rmtree(profile, ignore_errors=True)

# ---- Verificacion de paginas ----
from pypdf import PdfReader  # noqa: E402

n = len(PdfReader(str(PDF_OUT)).pages)
rel = PDF_OUT.relative_to(ROOT)
if n > 10:
    print(f"PDF: {rel} -> {n} PAGINAS  (¡LIMITE 10 EXCEDIDO!)")
    sys.exit(1)
print(f"PDF: {rel} -> {n} paginas OK (limite 10)")
