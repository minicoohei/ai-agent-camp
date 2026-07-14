---
nonInteractiveMode: deferred
---

# Guide - Sugerir próximas acciones

Este comando utiliza `tools/guide_action.py` para analizar la situación actual a partir del historial de SpecStory y presentar el contexto de fondo y las próximas acciones.

## Funcionalidades

- Analizar la situación actual a partir del historial de SpecStory
- Proporcionar **explicaciones de fondo y contexto**
- Presentar claramente las **próximas acciones**
- Generar **ejemplos de prompts para usar con el siguiente Agente**
- **Listar explícitamente los archivos referenciados**

## Pasos

### Paso 1: Obtener la lista de archivos de SpecStory

Primero, obtenga la lista de archivos en formato JSON con el siguiente comando:

```bash
uv run python tools/guide_action.py --list --json
```

### Paso 2: Mostrar la interfaz de selección de archivos

Basándose en el JSON obtenido, utilice la herramienta AskQuestion para mostrar una interfaz de selección de archivos al usuario.

**Configuración de AskQuestion:**
- `title`: "Seleccione archivos de SpecStory para analizar"
- `questions`: Presente cada archivo del JSON obtenido como una opción de selección
- `allow_multiple`: true (permitir selección múltiple)

Ejemplo:
```json
{
  "title": "Seleccione archivos de SpecStory para analizar",
  "questions": [{
    "id": "specstory_files",
    "prompt": "Seleccione los archivos para analizar (se permite selección múltiple)",
    "options": [
      {"id": "2025-12-18_10-00Z-example.md", "label": "2025-12-18 10:00Z - Example Title"},
      ...
    ],
    "allow_multiple": true
  }]
}
```

### Paso 3: Ejecutar análisis con los archivos seleccionados

Usando los nombres de archivo seleccionados por el usuario, ejecute el siguiente comando:

```bash
uv run python tools/guide_action.py --names "{nombres_archivo_seleccionados_separados_por_comas}" --output "{ruta_salida}"
```

Ejemplo:
```bash
uv run python tools/guide_action.py --names "2025-12-18_10-00Z-example.md,2025-12-17_09-30Z-another.md"
```

### Paso 4: Verificar resultados

- Verifique la ruta del archivo HTML generado e informe al usuario.
- Guíe al usuario sobre cómo abrirlo con Live Server.

## Opciones

| Opción | Descripción |
|--------|-------------|
| `--list`, `-l` | Mostrar lista de archivos de SpecStory |
| `--json`, `-j` | Salida en formato JSON (usar con --list) |
| `--names`, `-n` | Especificar por nombre de archivo (separados por comas) |
| `--select`, `-s` | Especificar por número (ej.: 1,2,3) |
| `--files`, `-f` | Analizar los N archivos más recientes (predeterminado: 3) |
| `--output`, `-o` | Ruta del archivo de salida |

## Contenido de salida

- **Lista de archivos de SpecStory referenciados**: Qué archivos fueron analizados
- **Resumen de la situación actual**: En qué se está trabajando actualmente
- **Explicación de fondo**: Por qué este trabajo es necesario
- **Próximas acciones**: Cosas específicas por hacer
- **Ejemplos de prompts**: Prompts para ingresar en un nuevo Agente
- **Resultados esperados**: Qué se logrará
