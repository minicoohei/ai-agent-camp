---
name: gslides-parser
description: "Habilidad para analizar la estructura de Google Slides a través de GAS y generar mapeo YAML. Se activa con solicitudes como 'analiza las diapositivas,' 'analiza la estructura de diapositivas,' 'crea mapeo YAML,' etc. Realiza análisis semántico compatible con pptx-converter + asignación de marcadores de posición."
triggers:
  - gslides-parser
  - スライドパース
  - スライド構造解析
  - YAMLマッピング
  - Google Slides解析
  - gslides
---

# /gslides-parser - Analizador de Google Slides

Analice la estructura de una presentación de Google Slides a través de GAS y genere YAML de mapeo compatible con pptx-converter.

## Prerrequisitos

```bash
# clasp se ejecuta via npx (no requiere instalación)
# Iniciar sesión con cuenta de Google
npx -y @google/clasp login

# Habilitar la API de Google Apps Script
# https://script.google.com/home/usersettings
```

## Inicio Rápido

```bash
# 1. Configuración inicial del proyecto GAS (solo primera vez)
python skills/gslides-parser/scripts/gslides_parser.py setup

# 2. Ejecutar manualmente una vez en el editor de GAS para conceder permisos
npx @google/clasp open --cwd skills/gslides-parser/gas/

# 3. Ejecutar análisis
python skills/gslides-parser/scripts/gslides_parser.py analyze \
  1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ \
  -o output/slides/mapping.yaml
```

## Subcomandos

| Comando | Descripción |
|---------|-------------|
| `setup` | Configuración inicial del proyecto GAS (clasp create + push) |
| `analyze <id>` | Analizar presentación -> Salida YAML |
| `json <id>` | Solo generar JSON del resultado del análisis GAS |

## Opciones

### analyze

| Opción | Descripción | Predeterminado |
|--------|-------------|----------------|
| `-o, --output` | Ruta del YAML de salida | `output/slides/gslides_<id>_<timestamp>.yaml` |
| `--no-gemini` | Deshabilitar análisis semántico de Gemini | false |
| `--skip-push` | Omitir clasp push | false |

### json

| Opción | Descripción | Predeterminado |
|--------|-------------|----------------|
| `-o, --output` | Ruta del JSON de salida | stdout |
| `--skip-push` | Omitir clasp push | false |

## Esquema YAML de Salida (compatible con pptx-converter)

```yaml
source: "Google Slides: Nombre de la Presentación"
presentation_id: "1ZVAI8..."
presentation_url: "https://docs.google.com/presentation/d/1ZVAI8.../edit"
generated_at: "2026-02-10T12:00:00"
slide_width_pt: 720
slide_height_pt: 405

slides:
  - slide_number: 1
    object_id: "p6"
    layout: "TITLE"
    elements:
      - id: "g1234abcd"
        type: text
        role: title
        hint: "Título principal."
        position: { left: 36, top: 150, width: 648, height: 80 }
        style: { font: "Noto Sans JP", size: 36, bold: true, color: "333333" }
        value: "Texto del Título"
        placeholder: "{{slide_1_title}}"

placeholders:
  - key: "{{slide_1_title}}"
    type: text
    role: title
    current: "Texto del Título"
```

## Flujo de Procesamiento

```
[Usuario] -> python gslides_parser.py analyze <id>
                    |
        +-----------+-----------+
        |  1. clasp push        |  Enviar código GAS
        |     (gas/ -> GAS)     |
        +-----------+-----------+
                    |
        +-----------+-----------+
        |  2. clasp run         |  Ejecutar parsePresentation()
        |     parsePresentation |  -> Devuelve estructura JSON
        +-----------+-----------+
                    |
        +-----------+-----------+
        |  3. gas_to_yaml.py    |  Análisis semántico
        |     JSON -> YAML      |  + asignación de marcadores
        +-----------+-----------+
                    |
        +-----------+-----------+
        |  4. Salida YAML       |  Compatible con pptx-converter
        +-----------+
```

## Elementos Analizados por el Parser GAS

| Tipo de Elemento | Información Extraída |
|-----------------|---------------------|
| **Shape (Texto)** | Texto, estilo (font/size/bold/color), detección de marcadores, color de relleno |
| **Imagen** | URL de origen, URL de contenido, enlace |
| **Tabla** | Texto de todas las celdas, conteo de filas/columnas, detección de encabezado, estilo de celda |
| **Grupo** | Análisis recursivo de elementos hijos |
| **SheetsChart** | ID de hoja de cálculo, ID de gráfico |
| **Línea** | Tipo de línea, grosor, color |
| **WordArt** | Texto renderizado |
| **Video** | Fuente, URL, ID de video |

## Análisis Semántico

Las heurísticas detectan automáticamente los siguientes roles:

- **Texto**: title, subtitle, heading, body, caption, label, footnote, page_number, bullet_list
- **Imagen**: hero_image, logo, icon, photo, decorative, background
- **Tabla**: data_table, comparison_table, schedule_table
- **Gráfico**: revenue_chart, trend_chart, comparison_chart
- **Forma**: accent_decoration, callout, divider, background_shape
- **Grupo**: process_flow, feature_cards, step_diagram

## Solución de Problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `Not logged in` | clasp sin sesión iniciada | `npx @google/clasp login` |
| `Script API disabled` | API de GAS deshabilitada | Habilite en [configuración de API GAS](https://script.google.com/home/usersettings) |
| `PERMISSION_DENIED` | Alcance OAuth no aprobado | Ejecute manualmente una vez en el editor de GAS para conceder permisos |
| `Function not found` | Push no completado | `npx @google/clasp push --force` |
| Timeout | Presentación grande | Ejecute directamente desde el editor de GAS |

## Habilidades Relacionadas

- **gslides-creator**: Crear nuevas diapositivas a partir de plantillas usando el YAML analizado
- **pptx-converter**: Funcionalidad equivalente para archivos PPTX (extract -> build -> convert)
- **gas-clasp-ops**: Gestión de proyectos clasp
