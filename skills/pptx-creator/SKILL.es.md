---
name: pptx-creator
description: "Habilidad que genera automáticamente archivos .pptx manteniendo el diseño de la plantilla, simplemente ingresando un tema. Se activa con solicitudes como 'Crear una presentación', 'Generar diapositivas', 'Crear PPTX', 'Crear un documento de propuesta'."
triggers:
  - Crear una presentación
  - Generar diapositivas
  - Crear PPTX
  - Crear un documento de propuesta
  - pptx-creator
  - Crear PowerPoint
  - Hacer una presentación
---

# /pptx-creator — Generación automática de presentaciones PPTX v2

Genera automáticamente archivos .pptx editables que mantienen el diseño de la plantilla, simplemente ingresando un tema.
Después de la generación, está disponible la exportación de imágenes + verificación de calidad con Gemini Vision.

## Activadores

Se activa con solicitudes como:
- "Crear presentación", "Generar diapositivas", "Crear PPTX", "Generar presentación"
- "Crear una presentación sobre ~"
- "Crear un documento de propuesta", "Generar diapositivas de informe"

## Cómo funciona

1. **Gemini Flash** genera un esquema estructurado (YAML) a partir del tema
2. Mantiene el diseño de la plantilla PPTX (maestro/tema/fuentes)
3. Enfoque híbrido de **inyección de PH de diseño** + **generación de código de elementos enriquecidos** para generación de diapositivas de alta calidad
4. **Exportación de imágenes** + **revisión de calidad con Gemini Vision** (`--verify`)

## Plantillas

| Plantilla | Tamaño | Fuente | Características |
|-----------|--------|--------|-----------------|
| `simple` | 13.333" x 7.5" | Yu Gothic | Simple, versátil, método de inyección PH |
| `standard` | 20.0" x 11.25" | Noto Sans JP + Futura | Diseño profesional, método code_gen |

## Tipos de diapositiva (11 tipos)

| Tipo | Descripción |
|------|-------------|
| `title` | Diapositiva de portada (título centrado + subtítulo + línea de acento) |
| `section` | Divisor de sección (número + título + barra de acento) |
| `content` | Contenido con viñetas (barra de título + puntos) |
| `key_message` | Un mensaje clave mostrado grande y centrado |
| `two_column` | Diseño de dos columnas (contenido izquierdo/derecho en tarjetas redondeadas) |
| `comparison` | Comparación izquierda/derecha (barra de encabezado + viñetas) |
| `agenda` | Agenda numerada (números circulares + líneas divisorias) |
| `closing` | Diapositiva de cierre (Gracias + línea de acento) |
| `kpi_dashboard` | Visualización de KPI (3-4 tarjetas, tarjetas redondeadas + tasa de cambio) |
| `process_flow` | Flujo de proceso (círculos numerados + flechas + descripciones) |
| `table` | Visualización de tabla (acento en fila de encabezado + fondos alternados) |

## Uso

### Generar PPTX a partir de un tema

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "Propuesta de utilización de IA" \
  --template simple \
  -o output/slides/proposal.pptx
```

### Generar + Verificación de calidad (Recomendado)

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "Informe de rendimiento Q1" \
  --template standard \
  --slides 10 \
  --verify \
  -o output/slides/q1_report.pptx
```

### Generar solo esquema (ejecución en seco)

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "Plan de nuevo negocio" \
  --dry-run \
  --save-outline /tmp/outline.yaml
```

### Solo exportación de imágenes

```bash
python skills/pptx-creator/scripts/export_to_images.py \
  output/slides/proposal.pptx \
  -o output/slides/proposal_images/
```

### Solo revisión de calidad

```bash
python skills/pptx-creator/scripts/quality_reviewer.py \
  output/slides/proposal_images/ \
  --threshold 7.0
```

## Parámetros

| Parámetro | Requerido | Por defecto | Descripción |
|-----------|-----------|-------------|-------------|
| `--topic` | *1 | - | Tema de la presentación |
| `--outline` | *1 | - | Ruta del YAML de esquema existente |
| `--template` | No | simple | Nombre de plantilla (simple/standard) |
| `--output` / `-o` | No | auto-generado | Ruta de salida del PPTX |
| `--slides` / `-n` | No | 8 | Número de diapositivas |
| `--audience` | No | business | Público objetivo |
| `--language` / `-l` | No | ja | Idioma de salida (ja/en) |
| `--save-outline` | No | - | Destino de guardado del YAML del esquema |
| `--dry-run` | No | false | Solo generar esquema |
| `--verify` | No | false | Exportación de imágenes + verificación de calidad después de la generación |
| `--verify-threshold` | No | 7.0 | Umbral de puntuación de aprobación de verificación de calidad |

*1: `--topic` y `--outline` son parámetros mutuamente excluyentes requeridos

## Ubicación de plantillas

```text
skills/pptx-creator/templates/
├── simple/template.pptx      ← Plantilla simple Yu Gothic
└── standard/template.pptx    ← Plantilla básica estándar
```

## Dependencias

- Python 3.8+
- `python-pptx` — Manipulación de PPTX
- `google-genai` — API de Gemini
- `pyyaml` — Procesamiento de YAML
- `python-dotenv` — Variables de entorno
- `libreoffice` — Exportación de imágenes (al usar --verify)
- `poppler-utils` — Conversión de PDF a PNG (al usar --verify)
- Variables de entorno: `GEMINI_API_KEY` o `GOOGLE_API_KEY`

## Pasos de ejecución para agentes

Cuando un usuario solicita "Crear una presentación" o similar:

1. Recopilar tema y requisitos
2. Ejecutar el siguiente comando:

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "<tema del usuario>" \
  --template simple \
  --slides <cantidad> \
  --verify \
  -o output/slides/<nombre_archivo>.pptx
```

3. Verificar los resultados de la comprobación de calidad
4. Si falla, modificar el esquema y regenerar
5. Comunicar la ruta del archivo de salida al usuario

## Descripción general

Habilidad que genera automáticamente archivos .pptx editables manteniendo el diseño de la plantilla, simplemente ingresando un tema. Genera esquemas (YAML) con Gemini Flash, compatible con 11 tipos de diapositivas.

## Solución de problemas

| Error | Solución |
|-------|----------|
| API key not found | Establezca `GEMINI_API_KEY` o `GOOGLE_API_KEY` como variable de entorno |
| Template not found | Verifique que los archivos de plantilla estén ubicados en `skills/pptx-creator/templates/` |
| LibreOffice not found | Se requiere la instalación de `libreoffice` al usar `--verify` |

## Criterios de éxito

- [ ] Se ha generado un archivo .pptx con el número especificado de diapositivas
- [ ] Cuando se especifica `--verify`, la puntuación de calidad está por encima del umbral
- [ ] Se mantienen las fuentes y el esquema de colores de la plantilla

## Uso

Consulte la sección "Uso" anterior. Ejemplo básico:

```bash
python skills/pptx-creator/scripts/pptx_creator.py --topic "Propuesta de utilización de IA" --template simple --verify -o output/slides/proposal.pptx
```
