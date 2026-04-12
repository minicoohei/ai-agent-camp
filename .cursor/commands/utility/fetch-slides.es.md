# Fetch Slides - Obtención de Google Slides

Obtenga el contenido de presentaciones de Google Slides en formato Markdown/JSON.

## Funcionalidades

- Extracción de texto de diapositivas
- Conversión de tablas a Markdown
- Obtención de notas del presentador
- Anotación de metadatos (fecha de creación, último editor, etc.)

## Pasos

### Paso 1: Extraer parámetros

Extraiga lo siguiente de la entrada del usuario:
- **URL/ID**: URL de Google Slides o ID de la presentación
- **Formato de salida**: markdown / json (predeterminado: markdown)
- **Destino de salida**: Ruta del archivo (se muestra en pantalla si se omite)

### Paso 2: Ejecutar la herramienta

Utilice la API de Google Slides para obtener el contenido. Después de configurar la autenticación con `/setup-google-api`, siga estos pasos:

```bash
# Verificar/configurar la autenticación de Google API
uv run python tools/api_setup_wizard.py guide google
```

Utilice las funciones interactivas de Claude Code / Cursor para especificar la URL o ID, obtener el contenido de las diapositivas y formatearlo.

### Paso 3: Mostrar resultados

Presente el Markdown o JSON de salida al usuario.

## Ejemplos de uso

### Obtener desde URL

```
/fetch-slides https://docs.google.com/presentation/d/1abc123xyz/edit
```

### Obtener desde ID

```
/fetch-slides 1abc123xyz
```

### Guardar en formato JSON

```
/fetch-slides 1abc123xyz --output slides.json --format json
```

### Guardar en archivo Markdown

```
/fetch-slides https://docs.google.com/presentation/d/1abc123xyz/edit -o output/slides.md
```

## Formatos de salida

### Markdown

```markdown
---
id: 1abc123xyz
title: Título de la presentación
created: 2026-01-15T10:00:00Z
modified: 2026-01-16T14:30:00Z
authors: user@example.com
total_slides: 10
---

# Título de la presentación

## Tabla de contenidos

1. [Introducción](#slide-1)
2. [Descripción general](#slide-2)
...

---

## Slide 1 {#slide-1}

Contenido de la diapositiva...

> **Notas del presentador:**
> Las notas del presentador se muestran aquí

---

## Slide 2 {#slide-2}

...
```

### JSON

```json
{
  "id": "1abc123xyz",
  "title": "Título de la presentación",
  "total_slides": 10,
  "slides": [
    {
      "number": 1,
      "content": ["Texto de la diapositiva..."],
      "speaker_notes": "Notas del presentador..."
    }
  ]
}
```

## Requisitos previos

Se requiere autenticación de Google API. Configure una de las siguientes opciones:

1. **Cuenta de servicio**: Variable de entorno `GCP_SA_KEY`
2. **OAuth**: Archivo `token.json`

Método de configuración:

```bash
uv run python tools/api_setup_wizard.py guide google
```

## Comandos relacionados

- `/api-setup-wizard` - Configuración de Google API
- `/generate-slide` - Generación de imágenes de diapositivas
