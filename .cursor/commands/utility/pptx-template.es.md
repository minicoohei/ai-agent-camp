# Operaciones de plantillas PPTX

Una herramienta que extrae el formato de archivos PowerPoint en plantillas YAML y genera nuevas diapositivas reemplazando solo el texto.

## Descripción general

Esta herramienta consta de dos scripts:

1. **pptx_ops.py extract-template** - Extraer una plantilla de un PPTX
2. **pptx_ops.py create** - Generar un nuevo PPTX a partir de una plantilla

## Flujo de trabajo

```text
[PPTX Original] -> [Extractor] -> [template.yaml] + [screenshots/]
                                       |
                                  [data.yaml]
                                       |
[template.yaml] + [data.yaml] -> [Generador] -> [Nuevo PPTX]
```

## Uso

### 1. Extraer plantilla

Extraer información de formato de un archivo PPTX existente.

```bash
# Extracción básica de plantilla
uv run python tools/pptx_ops.py extract-template sample.pptx --output template.yaml

# Extraer solo diapositivas específicas
uv run python tools/pptx_ops.py extract-template sample.pptx --slide 1 --output slide1_template.yaml

# Generar capturas de pantalla también (requiere LibreOffice)
uv run python tools/pptx_ops.py extract-template sample.pptx \
    --output template.yaml \
    --screenshot-dir ./screenshots

# Omitir la conversión a marcadores de posición (mantener el texto original)
uv run python tools/pptx_ops.py extract-template sample.pptx \
    --output template.yaml \
    --no-placeholder
```

### 2. Verificar información del archivo

Inspeccionar la estructura de un archivo PPTX.

```bash
uv run python tools/pptx_ops.py analyze sample.pptx
```

### 3. Listar marcadores de posición

Ver los marcadores de posición (variables reemplazables) en una plantilla.

```bash
uv run python tools/pptx_ops.py placeholders template.yaml
```

### 4. Crear plantilla de datos

Generar un archivo de datos vacío correspondiente a la plantilla.

```bash
uv run python tools/pptx_ops.py create-data template.yaml --output data.yaml
```

### 5. Generar nuevo PPTX

Generar un nuevo PPTX a partir de una plantilla y datos.

```bash
uv run python tools/pptx_ops.py generate template.yaml data.yaml --output output.pptx
```

## Estructura del YAML de plantilla

```yaml
source_file: sample.pptx
slide_width: 12192000  # EMU (914400 EMU = 1 pulgada)
slide_height: 6858000
slides:
  - index: 1
    layout_name: Blank
    screenshot: slide_1.png
    shapes:
      - id: shape_1
        name: "Title 1"
        type: text_box
        position:
          left: 457200
          top: 274638
          width: 8229600
          height: 1143000
        content:
          word_wrap: true
          paragraphs:
            - text: "{{title}}"
              original_text: "Título original"
              style:
                font_name: "Meiryo UI"
                font_size: 44
                font_bold: true
                font_color: "000000"
                alignment: center
        fill:
          type: solid
          color: "FFFFFF"
```

## Ejemplo de YAML de datos

```yaml
# Defina valores correspondientes a {{placeholder}} en template.yaml
title: "Nuevo título"
subtitle: "Subtítulo"
image_path: "./images/new_image.png"
cell_0_1: "Valor de celda de tabla"
```

## Tipos de formas soportados

| Tipo | Descripción | Información extraída |
|------|-------------|---------------------|
| text_box | Cuadro de texto | Posición, tamaño, texto, estilo de fuente, alineación |
| picture | Imagen | Posición, tamaño, ruta de imagen (convertida a marcador de posición) |
| table | Tabla | Posición, tamaño, número de filas/columnas, contenido de celdas, estilo de celdas |
| auto_shape | Forma | Posición, tamaño, color de relleno, color de línea, texto |
| placeholder | Marcador de posición | Posición, tamaño, tipo, texto |
| group | Grupo | Extracción recursiva de formas secundarias |

## Generación de capturas de pantalla

Se requiere lo siguiente para la generación automática de capturas de pantalla:

```bash
# macOS
brew install poppler
pip install pdf2image
brew install --cask libreoffice

# Windows
# poppler: Descargue de https://github.com/oschwartz10612/poppler-windows y agréguelo al PATH
pip install pdf2image
# LibreOffice: winget install --id TheDocumentFoundation.LibreOffice
```

Utilice la opción `--no-generate-screenshot` para usar capturas de pantalla existentes.

## Ejemplo: Producción masiva de diapositivas con formato

1. Prepare un PPTX con formato como fuente

2. Extraiga la plantilla
   ```bash
   uv run python tools/pptx_ops.py extract-template format_sample.pptx \
       --output my_template.yaml
   ```

3. Verifique los marcadores de posición
   ```bash
   uv run python tools/pptx_ops.py placeholders my_template.yaml
   ```

4. Cree un archivo de datos
   ```bash
   uv run python tools/pptx_ops.py create-data my_template.yaml \
       --output my_data.yaml
   ```

5. Edite los datos e ingrese los valores
   ```yaml
   # my_data.yaml
   title: "Informe del primer trimestre de 2026"
   author: "Departamento de ventas"
   date: "2026-01-16"
   ```

6. Genere un nuevo PPTX
   ```bash
   uv run python tools/pptx_ops.py generate my_template.yaml my_data.yaml \
       --output Q1_report.pptx
   ```

## Requisitos previos

- Python 3.8 o superior
- Bibliotecas requeridas: `python-pptx`, `pyyaml`
- Opcional: `pdf2image`, `Pillow` (para generación de capturas de pantalla)
- Opcional: LibreOffice (para conversión a PDF)

```bash
pip install python-pptx pyyaml pdf2image Pillow
```

## Notas

- EMU (English Metric Units): 914,400 EMU = 1 pulgada
- Los colores de tema no se pueden convertir directamente a RGB y se muestran como `theme:XXX`
- Las formas agrupadas se extraen individualmente como formas secundarias
- Las animaciones complejas y los efectos de transición no se conservan
