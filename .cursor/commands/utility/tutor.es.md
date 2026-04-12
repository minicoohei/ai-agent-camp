# Tutor - Generación de contenido de aprendizaje

Este comando utiliza `tools/tutor_generate.py` para generar automáticamente HTML de aprendizaje para principiantes a partir de diversas fuentes de entrada.

## Funcionalidades

- **Múltiples fuentes de entrada**: Tema / Archivo / Texto / SpecStory
- Genera automáticamente **HTML en formato tutorial** para principiantes
- **Muestra los archivos referenciados**
- **Muestra diagramas de flujo de procesamiento PlantUML**

## Pasos de ejecución

### Paso 1: Seleccionar fuente de entrada

Utilice la herramienta AskQuestion para que el usuario seleccione una fuente de entrada:

```json
{
  "title": "Seleccionar fuente de entrada del contenido de aprendizaje",
  "questions": [{
    "id": "input_source",
    "prompt": "¿Qué método desea utilizar para crear el tutorial?",
    "options": [
      {"id": "topic", "label": "Especificar tema - Generar un tutorial sobre cualquier tema"},
      {"id": "file", "label": "Especificar archivo - Generar un manual de uso para un archivo de código"},
      {"id": "text", "label": "Especificar texto - Generar una explicación del código/texto pegado"},
      {"id": "specstory", "label": "Análisis de SpecStory - Analizar brechas de aprendizaje del historial de conversaciones"}
    ]
  }]
}
```

### Paso 2: Procesar según la fuente de entrada

#### Para especificación de tema

Solicite al usuario que ingrese un tema y luego ejecute:

```bash
uv run python tools/tutor_generate.py --topic "nombre del tema"
```

Ejemplos:
```bash
uv run python tools/tutor_generate.py --topic "Conceptos básicos de Git"
uv run python tools/tutor_generate.py --topic "Introducción a GitHub Actions"
uv run python tools/tutor_generate.py --topic "Decoradores de Python"
```

#### Para especificación de archivo

Solicite al usuario que seleccione/ingrese un archivo y luego ejecute:

```bash
uv run python tools/tutor_generate.py --file "ruta_del_archivo"
```

Ejemplos:
```bash
uv run python tools/tutor_generate.py --file "src/auth.py"
uv run python tools/tutor_generate.py --file "tools/guide_action.py"
```

#### Para especificación de texto

Solicite al usuario que ingrese texto/código y luego ejecute:

```bash
uv run python tools/tutor_generate.py --text "texto de entrada"
```

#### Para análisis de SpecStory

1. Primero, obtenga la lista de archivos:
```bash
uv run python tools/tutor_generate.py --list --json
```

2. Muestre la interfaz de selección de archivos con AskQuestion:
```json
{
  "title": "Seleccionar archivos de SpecStory para analizar",
  "questions": [{
    "id": "specstory_files",
    "prompt": "Seleccione los archivos a analizar (selección múltiple permitida)",
    "options": [...],
    "allow_multiple": true
  }]
}
```

3. Ejecute con los archivos seleccionados:
```bash
uv run python tools/tutor_generate.py --names "file1.md,file2.md"
```

### Paso 3: Verificar resultados

- Confirme la ruta del archivo HTML generado e infórmelo al usuario.
- Proporcione instrucciones sobre cómo abrirlo con Live Server.

## Lista de opciones

| Opción | Descripción |
|--------|-------------|
| `--topic`, `-t` | Especificar un tema para generar un tutorial |
| `--file` | Especificar una ruta de archivo para generar un manual |
| `--text` | Especificar texto para generar una explicación |
| `--specstory` | Analizar brechas de aprendizaje del historial de SpecStory |
| `--list`, `-l` | Mostrar lista de archivos SpecStory |
| `--json`, `-j` | Salida en formato JSON (usar con --list) |
| `--names`, `-n` | Especificar por nombre de archivo (separados por coma) |
| `--select`, `-s` | Especificar por número (ej.: 1,2,3) |
| `--files`, `-f` | Número de archivos a analizar (por defecto: 1) |
| `--output`, `-o` | Ruta del archivo de salida |

## Contenido de la salida (formato tutorial)

- **Información de la fuente de entrada**: Desde qué fuente se generó el contenido
- **Diagrama de flujo de procesamiento**: Visualización del proceso con PlantUML
- **Descripción general**: Introducción al tema y su importancia para el aprendizaje
- **Conocimientos previos**: Conocimientos fundamentales requeridos
- **Secciones**: Explicaciones paso a paso
  - Descripciones detalladas
  - Ejemplos de código
  - Puntos clave y consejos
- **Errores comunes y precauciones**: Puntos donde los principiantes suelen tropezar
- **Resumen**: Revisión del contenido aprendido
- **Siguientes pasos**: Qué aprender a continuación

## Ejemplos de uso

### Generar tutorial a partir de un tema
```
/tutor
-> Seleccionar "Especificar tema"
-> Ingresar "Conceptos básicos de Docker"
```

### Generar manual a partir de un archivo
```
/tutor
-> Seleccionar "Especificar archivo"
-> Seleccionar o ingresar un archivo
```

### Analizar brechas de aprendizaje desde SpecStory
```
/tutor
-> Seleccionar "Análisis de SpecStory"
-> Seleccionar múltiples archivos para analizar
```
