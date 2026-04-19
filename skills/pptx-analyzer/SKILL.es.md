---
name: pptx-analyzer
description: "Habilidad que analiza la estructura de archivos PowerPoint (.pptx), generando información sobre diapositivas, formas y texto. Se activa con solicitudes como 'Analizar PPTX', 'Verificar estructura de plantilla', 'Inspeccionar elementos de diapositiva'."
triggers:
  - Analizar PPTX
  - Verificar estructura de plantilla
  - Inspeccionar elementos de diapositiva
  - pptx-analyzer
  - Análisis de PowerPoint
  - Mostrar el contenido del PowerPoint
---

# PPTX Analyzer

Habilidad para analizar la estructura de archivos PowerPoint.

## Funcionalidades

1. **Extracción de estructura**: Extrae diapositivas, formas, marcadores de posición y texto
2. **Generación de imágenes**: Convierte diapositivas a imágenes PNG (opcional)
3. **Análisis semántico**: Determina roles de diapositivas y propósitos de elementos usando Gemini (opcional)

## Uso

```bash
# Análisis básico (salida JSON + TXT)
python scripts/analyze_pptx.py template.pptx

# Análisis con imágenes
python scripts/analyze_pptx.py template.pptx --with-images

# Con análisis semántico de Gemini
python scripts/analyze_pptx.py template.pptx --with-gemini

# Especificar directorio de salida
python scripts/analyze_pptx.py template.pptx --output-dir ./output
```

## Formatos de salida

### JSON (`{filename}_structure.json`)

```json
{
  "source_file": "template",
  "total_slides": 5,
  "slides": [
    {
      "slide_index": 0,
      "layout_name": "Diapositiva de título",
      "shapes": [
        {
          "shape_id": 2,
          "name": "Title 1",
          "shape_type": "Shape",
          "left": 838200,
          "top": 2130425,
          "width": 10515600,
          "height": 1325563,
          "text": "Título de la presentación",
          "has_text_frame": true,
          "is_placeholder": true,
          "placeholder_type": "TITLE (1)"
        }
      ]
    }
  ]
}
```

### Texto (`{filename}_structure.txt`)

```
=== Slide 1 (Layout: Diapositiva de título) ===
  [2] Title 1
      Type: Shape, Pos: (0.9", 2.3"), Size: 11.5" x 1.5"
      Placeholder: TITLE (1)
      Text: "Título de la presentación"
```

## Dependencias

- `python-pptx`: Requerido
- `Pillow`: Procesamiento de imágenes (al usar `--with-images`)
- `pdf2image` + LibreOffice: Conversión de imágenes vía PDF
- `google-generativeai`: Análisis con Gemini (al usar `--with-gemini`)

## Casos de uso

1. **Análisis de plantillas**: Comprender la estructura de plantillas antes de la generación automática de diapositivas
2. **Identificación de marcadores de posición**: Identificar cuadros de texto y posiciones de gráficos para reemplazo
3. **Verificación de diseño**: Comprobar tipos de diseño y posicionamiento de elementos en cada diapositiva
