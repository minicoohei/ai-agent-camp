# PowerPoint Operations - Operaciones PPTX

Lectura, escritura y análisis de archivos PowerPoint utilizando python-pptx.

## Funcionalidades

- Lectura de diapositivas y conversión a Markdown
- Análisis de la estructura de presentaciones
- Extracción de plantillas
- Creación de nuevos archivos PPTX

## Pasos de ejecución

### Paso 1: Extracción de parámetros

Extraiga lo siguiente de la entrada del usuario:
- **Comando**: read / to-markdown / analyze / extract-template / create
- **Ruta del archivo**: Ruta del archivo PPTX
- **Número de diapositiva**: Cuando se especifica una diapositiva particular
- **Destino de salida**: Ruta del archivo (se muestra en pantalla si se omite)

### Paso 2: Ejecución de la herramienta

```bash
# Lectura
uv run python tools/pptx_ops.py read <archivo.pptx>

# Conversión a Markdown
uv run python tools/pptx_ops.py to-markdown <archivo.pptx>

# Análisis de estructura
uv run python tools/pptx_ops.py analyze <archivo.pptx>

# Extracción de plantilla
uv run python tools/pptx_ops.py extract-template <archivo.pptx> --output template.json

# Creación
uv run python tools/pptx_ops.py create template.json --output new.pptx
```

### Paso 3: Mostrar resultados

Presente los datos de salida al usuario.

## Opciones

### Comando read

| Opción | Descripción |
|--------|-------------|
| `--slide INT` / `-s` | Número de diapositiva específico (indexado desde 1) |
| `--format TEXT` / `-f` | Formato de salida: text / json |

### Comando to-markdown

| Opción | Descripción |
|--------|-------------|
| `--output PATH` / `-o` | Ruta del archivo de salida |

### Comando extract-template

| Opción | Descripción |
|--------|-------------|
| `--output PATH` / `-o` | Ruta del archivo JSON de salida |

### Comando create

| Opción | Descripción |
|--------|-------------|
| `--output PATH` / `-o` | Ruta del archivo PPTX de salida (obligatorio) |

## Ejemplos de uso

### Leer un archivo

```
/pptx-ops read presentation.pptx
```

### Leer una diapositiva específica

```
/pptx-ops read presentation.pptx --slide 3
```

### Convertir a Markdown

```
/pptx-ops to-markdown presentation.pptx -o slides.md
```

### Analizar una presentación

```
/pptx-ops analyze presentation.pptx --format json
```

### Extraer una plantilla

```
/pptx-ops extract-template template.pptx --output my_template.json
```

### Crear desde una plantilla

```
/pptx-ops create my_template.json --output new_presentation.pptx
```

## Formato de salida

### read (formato texto)

```
=== Slide 1 ===
Shapes: 5

Text content:
  - Título de la presentación
  - Subtítulo
  - Autor: Taro Tanaka

Notes: Las notas del orador aparecen aquí...
```

### to-markdown

```markdown
# presentation.pptx

**Slides**: 10

---

## Tabla de contenido

1. [Título de la presentación](#slide-1)
2. [Resumen](#slide-2)
...

---

## Slide 1 {#slide-1}

### Título de la presentación

Subtítulo

> **Notas del orador:**
> Las notas del orador aparecen aquí
```

### analyze

```
📊 Informe de análisis: presentation.pptx
==================================================
Slides: 10
Total text length: 2500 characters
Layouts used: ['Title Slide', 'Title and Content', 'Blank']

Shape types:
  MSO_SHAPE_TYPE.PLACEHOLDER (14): 28
  MSO_SHAPE_TYPE.TEXT_BOX (17): 5
  MSO_SHAPE_TYPE.PICTURE (13): 3

Slides overview:
  1. Title Slide (3 shapes)
  2. Title and Content (5 shapes)
  3. Title and Content (4 shapes)
```

### extract-template

```json
{
  "source_file": "presentation.pptx",
  "slide_width": 9144000,
  "slide_height": 6858000,
  "layouts": [
    {
      "name": "Title Slide",
      "placeholders": [...]
    }
  ],
  "slides": [
    {
      "index": 1,
      "layout_name": "Title Slide",
      "content_structure": [...]
    }
  ]
}
```

## Formato JSON de plantilla (para create)

```json
{
  "slides": [
    {
      "title": "Título de la diapositiva",
      "content": [
        "Punto 1",
        "Punto 2",
        "Punto 3"
      ],
      "notes": "Notas del orador"
    }
  ]
}
```

## Requisitos previos

Se requiere la biblioteca python-pptx:

```bash
pip install python-pptx
```

## Comandos relacionados

- `/excel-ops` - Operaciones con Excel
- `/fetch-slides` - Obtener Google Slides
- `/generate-slide` - Generar imágenes de diapositivas
