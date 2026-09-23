# EP1 · Sistema de Recomendación de Productos para E-commerce (ShopFast)

Informe técnico de la **Evaluación Parcial N°1** de la asignatura
**Arquitectura de Sistemas de Inteligencia Artificial (ITY1102)** — Duoc UC.

| | |
|---|---|
| **Plantilla** | arc42 simplificada — secciones **1.1 → 1.4** |
| **Equipo 1** | Martin Higuera · Gabriel Durán · Francisco Salazar |
| **Docente** | Ricardo Aravena Videla |
| **Entrega** | Semana 7 — 24/09/2026 |
| **Caso** | Caso 1 — ShopFast ([insumos/](insumos/)) |

## 📦 Entregables

| Archivo | Notas |
|---|---|
| [`entregables/EP1_Equipo1_HigueraDuranSalazar.pdf`](entregables/EP1_Equipo1_HigueraDuranSalazar.pdf) | **10/10 páginas** (límite de la pauta) |
| [`entregables/EP1_Equipo1_HigueraDuranSalazar.docx`](entregables/EP1_Equipo1_HigueraDuranSalazar.docx) | Versión Word con ajustes de formato hechos a mano |

## 📁 Estructura

```
entregables/        PDF y DOCX que se suben a AVA
trabajo/            fuentes editables del informe
  ├ Arquitectura para sistemas IA.md      ← fuente única de verdad
  ├ arquitectura parcial 1.drawio.png     diagrama embebido en 1.4.4
  └ DiagramaShopPipeline_v2.drawio        diagrama editable (draw.io)
herramientas/       scripts que regeneran los entregables
  ├ generar_pdf.py                        md → HTML → Edge → PDF
  ├ generar_docx.py                       md → DOCX
  └ EP1_Equipo1_informe.html              intermedio regenerable (no se entrega)
insumos/            pauta del parcial y caso ShopFast del docente (md + pdf)
versiones_antiguas/ primeras versiones de docx, jpg y drawio (histórico, no usar)
opencode.json       comando /informe de automatización (ver abajo)
```

## 🔁 Regenerar los entregables

```sh
pip install markdown pypdf python-docx   # dependencias (una vez)
python herramientas/generar_pdf.py       # valida solo: corta con error si >10 páginas
python herramientas/generar_docx.py      # valida: 5 tablas, 1 imagen
```

Requiere Microsoft Edge (incluido en Windows) para imprimir el PDF. Los scripts
resuelven rutas desde su ubicación, así que funcionan desde cualquier carpeta.

> ⚠️ **Los dos scripts generan desde `trabajo/Arquitectura para sistemas IA.md`.**
> El DOCX tiene formato aplicado a mano (espaciado, títulos 18pt); el PDF también
> lleva ajustes de layout. **No los regeneres** salvo que quieras perder esos
> cambios — primero llevar los cambios al `.md`.

## ✅ Checklist de la pauta (`insumos/EP1_ITY1102_Estudiante.*`)

- [x] Secciones **1.1–1.4** con índice sincronizado
- [x] **11 requisitos funcionales (R.F.)** y **14 no funcionales (R.N.F.)**
- [x] **5 tablas** (R.F./R.N.F., comparativa de 3 ejes, decisiones, MLOps…)
- [x] Diagrama de arquitectura en **1.4.4** (PNG exportado desde draw.io)
- [x] **≥ 2 referencias APA** con `[cite:]` resueltos
- [x] **Declaración de uso de IA generativa** (OpenCode Zen)
- [x] **PDF ≤ 10 páginas** → 10/10

## 🤖 Automatización (OpenCode)

- **`/informe`** (definido en [`opencode.json`](opencode.json)): valida la
  estructura, comprime el texto si supera 4.600 palabras, regenera PDF y DOCX,
  y hace commit + push.
- MCP **context7** conectado para consultar documentación de librerías al día.
- El historial de git cuenta toda la evolución: del primer borrador → correcciones
  de estructura → diagrama v2 → compresión → PDF 10 págs. → organización en carpetas.
