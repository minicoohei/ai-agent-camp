---
name: pptx-converter
description: "Conversión de plantillas PPTX y generación de presentaciones desde cero. Reescribe el contenido preservando temas, animaciones y SmartArt. Se activa con solicitudes como 'Convertir PPTX', 'Crear diapositivas', 'Reescribir PowerPoint', 'Generar presentación'."
triggers:
  - Convertir PPTX
  - Crear diapositivas
  - Reescribir PowerPoint
  - Generar presentación
  - pptx-converter
  - Conversión de PowerPoint
  - Crear diapositivas usando plantilla
version: 1.0.0
author: CursorBootcamp
dependencies:
  - python: 3.8+
  - packages: ["python-pptx", "pyyaml", "lxml", "google-generativeai", "python-dotenv", "Pillow"]
---

## Palabras clave de activación
"Convertir PPTX", "Crear diapositivas", "Reescribir PowerPoint", "Generar presentación", "PowerPoint"

# PPTX Converter

Herramienta para conversión de plantillas de PowerPoint y generación de presentaciones desde cero.

## Funcionalidades

### 1. convert - Conversión de plantilla (un solo comando)
Copia el PPTX fuente, analiza semánticamente todos los elementos con Gemini y reescribe automáticamente el contenido para un nuevo tema.

```bash
python skills/pptx-converter/scripts/pptx_converter.py convert \
    source.pptx \
    --topic "Informe de ventas Q1 2026" \
    -o output/slides/q1_report.pptx
```

**Se preserva:** Maestros de diapositivas, colores del tema, definiciones de fuentes, animaciones, transiciones, estructura SmartArt, posicionamiento del diseño

### 2. extract - Generar YAML de mapeo
Extrae y analiza semánticamente todos los elementos del PPTX fuente, generando un YAML de mapeo coordenadas-elementos para revisión y edición manual.

```bash
python skills/pptx-converter/scripts/pptx_converter.py extract \
    source.pptx \
    -o mapping.yaml
```

### 3. build - Mapeo + Datos → PPTX
Reescribe elementos usando un YAML de datos editado manualmente.

```bash
python skills/pptx-converter/scripts/pptx_converter.py build \
    source.pptx \
    mapping.yaml \
    --data data.yaml \
    -o output.pptx
```

### 4. deck - Generar presentación desde cero
Genera un esquema con Gemini a partir de un tema → crea automáticamente el PPTX.

```bash
python skills/pptx-converter/scripts/pptx_converter.py deck \
    --topic "Propuesta de utilización de agentes de IA" \
    --type proposal \
    --style corporate \
    -o output/slides/proposal.pptx
```

**Opciones de deck:**
- `--type`: auto / presentation / proposal / report / educational / pitch
- `--style`: corporate / creative / minimal / academic
- `--slides N`: Número de diapositivas (0=la IA decide)
- `--audience`: Público objetivo
- `--outline-only`: Solo generar YAML del esquema

## Tipos de elementos compatibles

| Tipo | Extraer | Reescribir | Notas |
|------|:-------:|:----------:|-------|
| Texto | o | o | Preservación completa de estilos (fuente, color, negrita, etc.) |
| Gráfico | o | o | Solo reemplazo de datos vía chart.replace_data() |
| Tabla | o | o | Estilo de celdas preservado, solo se reemplaza el contenido |
| Imagen | o | o | Preservada por defecto, reemplazo individual disponible |
| Forma | o | o | Se reemplaza el texto dentro de las formas |
| Grupo | o | o | Elementos hijos procesados recursivamente (hasta profundidad 3) |
| SmartArt | o | parcial | Solo nodos de texto, reemplazados por manipulación directa de XML |

## Estructura del YAML de mapeo

```yaml
source: "source.pptx"
generated_at: "2026-02-09T15:30:00"
slide_width: 12192000
slide_height: 6858000

slides:
  - slide_number: 1
    layout: "Title Slide"
    elements:
      - id: 2
        name: "Title 1"
        type: text
        role: title
        hint: "Título principal. 15-25 caracteres."
        position: { left: 457200, top: 274638, width: 8229600, height: 1143000 }
        style: { font: "Meiryo UI", size: 36, bold: true, color: "2563EB" }
        value: "Estrategia de ventas 2025"
        placeholder: "{{slide_1_title}}"

placeholders:
  - key: "{{slide_1_title}}"
    type: text
    role: title
    current: "Estrategia de ventas 2025"
```

## Decisión de flujo de trabajo

- **Tiene un PPTX de plantilla** → `convert` (un solo comando)
- **Quiere revisar el mapeo manualmente** → `extract` → editar YAML → `build`
- **Crear desde cero** → `deck`

## Variables de entorno

- `GEMINI_API_KEY` o `GOOGLE_API_KEY`: Clave de API de Gemini (requerida)
- `GEMINI_FLASH_MODEL`: Modelo de procesamiento de texto (por defecto: gemini-2.5-flash)
