---
name: gslides-creator
description: "Habilidad para crear Google Slides a partir de plantillas. Se activa con solicitudes como 'crea Google Slides,' 'genera diapositivas,' 'crea una presentación,' etc. Usa GAS + clasp CLI para copiar plantillas, reescribir contenido y generar presentaciones desde cero."
triggers:
  - gslides-creator
  - Google Slides作成
  - スライド生成
  - プレゼン作成
  - テンプレートからスライド
  - gslides
---

# /gslides-creator - Creador de Google Slides

Cree Google Slides a partir de plantillas, o genere presentaciones desde cero.

## Prerrequisitos

```bash
# clasp con sesión iniciada
clasp login

# API de GAS habilitada
# https://script.google.com/home/usersettings

# gslides-parser configurado (usado por el comando convert)
python skills/gslides-parser/scripts/gslides_parser.py setup
```

## Inicio Rápido

```bash
# 1. Configuración inicial del proyecto GAS (solo primera vez)
python skills/gslides-creator/scripts/gslides_creator.py setup

# 2. Crear desde plantilla con nuevo tema
python skills/gslides-creator/scripts/gslides_creator.py convert \
  1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ \
  --topic "Curso Práctico de Claude Code para Ingenieros" \
  --title "Curso Práctico de Claude Code"

# 3. Generar presentación desde cero
python skills/gslides-creator/scripts/gslides_creator.py deck \
  --topic "Reporte de Ventas Q1 2026" --slides 10 --style corporate
```

## Subcomandos

| Comando | Descripción |
|---------|-------------|
| `setup` | Configuración inicial del proyecto GAS |
| `convert <template_id> --topic "..."` | Copia de plantilla -> Reescritura con Gemini |
| `build <template_id> --data data.yaml` | Copia de plantilla -> Reescritura precisa con datos YAML |
| `deck --topic "..."` | Generar presentación desde cero (esquema de Gemini) |

## convert - Reescritura de Plantilla

Copie una plantilla y genere contenido adaptado a un nuevo tema usando Gemini, luego reemplace por lotes con `replaceAllText`.

```bash
python gslides_creator.py convert TEMPLATE_ID \
  --topic "Nuevo tema" \
  --title "Nuevo título"
```

Flujo de procesamiento:
1. Analizar la estructura de la plantilla con gslides-parser
2. Generar nuevo contenido para marcadores de posición con Gemini Flash
3. Copiar plantilla + replaceAllText con GAS `convertPresentation()`
4. Generar nueva URL de Google Slides

## build - Reescritura Precisa

Reescribir texto, estilo y posición por elemento basándose en un YAML de mapeo.

```bash
# 1. Obtener mapeo con gslides-parser
python gslides_parser.py analyze TEMPLATE_ID -o mapping.yaml

# 2. Crear YAML de datos (manual o Gemini)
# 3. Construir
python gslides_creator.py build TEMPLATE_ID \
  --data data.yaml --title "Nueva Presentación"
```

Formato YAML de datos:
```yaml
slides:
  - slide_number: 1
    elements:
      - id: "g123abc"
        value: "Nuevo texto de título"
        style:
          font: "Noto Sans JP"
          size: 36
          bold: true
      - id: "g456def"
        value: "Nuevo texto del cuerpo"
```

## deck - Generar Presentación desde Cero

Genere un esquema con Gemini y construya diapositivas con GAS.

```bash
python gslides_creator.py deck \
  --topic "Propuesta de Utilización de IA" \
  --slides 10 \
  --style corporate \
  --save-outline outline.yaml

# Para heredar el tema de una plantilla
python gslides_creator.py deck \
  --topic "Reporte Q1" \
  --template TEMPLATE_ID \
  --style minimal
```

### Estilos

| Estilo | Descripción |
|--------|-------------|
| `corporate` | Tonos azules empresariales (predeterminado) |
| `minimal` | Monocromo + acento rojo |

### Tipos de Diapositiva (Selección automática)

| Tipo | Descripción |
|------|-------------|
| title | Diapositiva de título |
| section | Divisor de sección |
| content | Viñetas |
| key_message | Mensaje clave |
| two_column | Diseño de dos columnas |
| comparison | Comparación (izquierda/derecha) |
| agenda | Agenda |
| closing | Diapositiva de cierre |
| kpi_dashboard | Tarjetas de KPI |
| process_flow | Flujo de proceso |
| table | Tabla |

## Lista de Funciones GAS

| Función | Archivo | Descripción |
|---------|---------|-------------|
| `convertPresentation()` | convertSlides.js | Copia de plantilla + replaceAllText |
| `listPlaceholders()` | convertSlides.js | Obtener lista de marcadores de posición |
| `buildPresentation()` | buildSlides.js | Reescritura detallada a nivel de elemento |
| `createDeck()` | deckSlides.js | Generar presentación desde cero |
| `createDeckFromTemplate()` | deckSlides.js | Generación de presentación basada en plantilla |

## Habilidades Relacionadas

- **gslides-parser**: Analizar la estructura de Google Slides y generar YAML de mapeo
- **pptx-creator**: Versión PPTX de funcionalidad equivalente (Gemini -> YAML -> PPTX)
- **pptx-converter**: Conversión de plantillas PPTX
- **gas-clasp-ops**: Gestión de proyectos clasp
