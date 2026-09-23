# -*- coding: utf-8 -*-
"""Convierte el .md del informe a HTML listo para imprimir a PDF (Edge headless)."""
import markdown
import pathlib

SRC = "Arquitectura para sistemas IA.md"
OUT = "EP1_Equipo1_informe.html"

md_text = pathlib.Path(SRC).read_text(encoding="utf-8")
body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])

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

pathlib.Path(OUT).write_text(html, encoding="utf-8")
print("HTML generado:", OUT)
