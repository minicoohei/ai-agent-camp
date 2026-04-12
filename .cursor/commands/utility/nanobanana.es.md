# Nano Banana Pro - Generación y edición de imágenes

Este comando utiliza `tools/nanobanana.py` para generar y editar imágenes con Nano Banana Pro (Gemini 3 Pro Image).

## Funcionalidades

1. **Texto a imagen (text-to-image)**: Generar nuevas imágenes solo con un prompt
2. **Edición de imágenes**: Editar imágenes existentes con instrucciones

## Pasos de ejecución

1. **Extracción de parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Prompt**: Instrucciones de generación/edición (obligatorio) ej.: "Un paisaje del Monte Fuji", "Desenfocar el fondo"
   - **Ruta de imagen de entrada**: Solo al editar (opcional)
   - **Relación de aspecto**: Válida solo para generación. `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9` (por defecto: `16:9`)
   - **Nombre de sesión**: Inferir del título del chat actual/nombre del proyecto (obligatorio)
   - **Ruta de salida**: Se genera automáticamente si se omite (se guarda en la carpeta `docs/generated/fecha_nombreSesión/` cuando se especifica `--session`)

2. **Ejecución de la herramienta**:

   **Generación de texto a imagen:**
   ```bash
   uv run python tools/nanobanana.py "{prompt}" --session "{nombre_sesión}" --aspect-ratio "{relación_aspecto}"
   ```

   **Edición de imagen:**
   ```bash
   uv run python tools/nanobanana.py "{prompt}" --input "{ruta_imagen_entrada}" --session "{nombre_sesión}"
   ```

## Acerca de los nombres de sesión

Para el argumento `--session`, infiera un nombre apropiado del título o contexto del chat actual.
- Ejemplo: Título del chat "Creación de banner para Cursor Bootcamp" -> `--session "cursor_bootcamp_banner"`
- Ejemplo: Solicitud "Crear un paisaje del Monte Fuji" -> `--session "monte_fuji_paisaje"`

Esto organiza las imágenes en carpetas específicas por sesión como `docs/generated/20251223_cursor_bootcamp_banner/`.
