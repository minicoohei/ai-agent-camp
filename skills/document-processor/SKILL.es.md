---
name: document-processor
description: "Sub-agente para leer, editar y analizar archivos PDF/PPTX/Excel. Separa el procesamiento de documentos grandes del contexto principal para optimizar el consumo de contexto. Se activa con solicitudes como 'analiza el PDF,' 'lee el contenido del PPTX,' 'analiza el Excel,' 'edita las diapositivas,' etc."
triggers:
  - PDFを分析
  - PDFを編集
  - PPTXを分析
  - PPTXを読んで
  - スライドの内容
  - Excelを分析
  - Excelを読んで
  - ドキュメントを処理
---

# Sub-Agente de Procesamiento de Documentos

Un sub-agente para leer, editar y analizar archivos PDF/PPTX/Excel en un contexto dedicado.

## Propósito

Separar el procesamiento de documentos grandes del contexto del agente principal para:
- Reducir el consumo de contexto (efecto de reducción de 2000-10000 tokens)
- Devolver solo resúmenes de resultados de procesamiento
- Permitir el procesamiento paralelo de múltiples archivos

## Formatos Soportados

| Formato | Lectura | Edición | Análisis |
|---------|:-------:|:-------:|:--------:|
| PDF (.pdf) | Sí | Sí | Sí |
| PowerPoint (.pptx) | Sí | Sí | Sí |
| Excel (.xlsx) | Sí | Sí | Sí |

## Scripts Disponibles

### 1. Operaciones de PowerPoint (`tools/pptx_ops.py`)

```bash
# Lectura
uv run python tools/pptx_ops.py read <archivo.pptx>

# Conversión a Markdown
uv run python tools/pptx_ops.py to-markdown <archivo.pptx>

# Análisis de estructura
uv run python tools/pptx_ops.py analyze <archivo.pptx>

# Extracción de plantilla
uv run python tools/pptx_ops.py extract-template <archivo.pptx> --output template.json

# Crear nuevo
uv run python tools/pptx_ops.py create <template.json> --output nuevo.pptx
```

### 2. Operaciones de Excel (`tools/excel_ops.py`)

```bash
# Lectura
uv run python tools/excel_ops.py read <archivo.xlsx>

# Lectura de hoja específica
uv run python tools/excel_ops.py read <archivo.xlsx> --sheet "Hoja1"

# Conversión a Markdown
uv run python tools/excel_ops.py to-markdown <archivo.xlsx>

# Reporte de análisis
uv run python tools/excel_ops.py analyze <archivo.xlsx>

# Escritura
uv run python tools/excel_ops.py write <archivo.xlsx> --data '{"sheet": "Hoja1", "cell": "A1", "value": "Hola"}'
```

### 3. Operaciones de PDF (`tools/pdf_page_editor.py`)

```bash
# Extracción de texto y análisis
uv run python tools/pdf_page_editor.py analyze <archivo.pdf>

# Edición de página
uv run python tools/pdf_page_editor.py edit <archivo.pdf> --page 1 --changes <changes.yaml>

# Compresión
uv run python tools/pdf_page_editor.py compress <archivo.pdf> --output comprimido.pdf
```

## Patrón de Invocación del Sub-Agente

El agente principal invoca este sub-agente usando el siguiente patrón:

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Document analysis",
    prompt="""
    Lea y ejecute esta habilidad: skills/document-processor/SKILL.md
    
    Tarea: {instrucciones del usuario}
    Archivo objetivo: {ruta del archivo}
    
    Devuelva el resultado en formato de resumen.
    """
)
```

## Formato de Retorno

Los resultados de procesamiento se devuelven en el siguiente formato de resumen:

```yaml
status: success
file: ejemplo.pptx
summary:
  total_slides: 10
  key_content:
    - slide_1: "Diapositiva de título - Resumen del proyecto"
    - slide_2: "Tabla de contenidos - 5 elementos"
  findings:
    - "La plantilla tiene relación de aspecto 16:9"
    - "Esquema de colores: azul/blanco/negro"
output_files:
  - example_structure.json
  - example_structure.txt
```

## Dependencias

```txt
python-pptx>=0.6.21
openpyxl>=3.1.0
pdf2image>=1.16.0
Pillow>=9.0.0
PyMuPDF>=1.21.0
google-generativeai>=0.3.0
```

## Casos de Uso

1. **Análisis de PPTX**: Comprensión de estructura de plantillas, identificación de marcadores de posición
2. **Análisis de Excel**: Comprensión de estructura de datos, relaciones entre hojas
3. **Edición de PDF**: Corrección de texto, reconstrucción de páginas
4. **Procesamiento por lotes**: Procesamiento masivo de múltiples documentos

## Notas

- Los archivos grandes (>50MB) pueden tardar en procesarse
- La edición de PDF no modifica el archivo original; genera un archivo nuevo
- Los archivos PPTX con muchas imágenes pueden tener las imágenes extraídas con la opción `--with-images`

## Descripción General

Una habilidad de sub-agente que lee, edita y analiza archivos PDF/PPTX/Excel en un contexto dedicado. Separa el procesamiento de documentos grandes del contexto principal y devuelve solo resúmenes de resultados de procesamiento.

## Solución de Problemas

| Error | Solución |
|-------|----------|
| python-pptx no instalado | Instale con `uv add python-pptx` |
| Error de análisis de PDF | Verifique que PyMuPDF esté instalado: `uv add PyMuPDF` |
| Archivo demasiado grande (>50MB) | El procesamiento puede tardar. Considere pre-comprimir con la habilidad de compresión de PDF |

## Criterios de Éxito

- [ ] El contenido del documento se ha devuelto en formato de resumen (YAML)
- [ ] Durante las operaciones de edición, el archivo original no se modifica y se genera un archivo nuevo
- [ ] Completado sin errores

## Uso

Consulte la sección "Scripts Disponibles" anterior. Ejemplos básicos:

```bash
# Leer PPTX
uv run python tools/pptx_ops.py read presentacion.pptx

# Analizar Excel
uv run python tools/excel_ops.py analyze datos.xlsx

# Analizar PDF
uv run python tools/pdf_page_editor.py analyze documento.pdf
```
