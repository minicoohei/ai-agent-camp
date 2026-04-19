# Screenshot Analyzer - Herramienta integrada de análisis de capturas de pantalla

Este comando utiliza `tools/screenshot_analyzer.py` para analizar capturas de pantalla, realizar diagnósticos de errores y generar tutoriales de operación.

## Funcionalidades

- **Modo Analyze**: Detecta errores en imágenes y presenta causas y soluciones (NextStep).
- **Modo Tutorial**: Analiza los pasos de operación en imágenes y genera tutoriales paso a paso con anotaciones.
- **Adición de anotaciones**: Agrega automáticamente anotaciones como bordes rojos y flechas en las ubicaciones de errores o pasos de operación.

## Pasos de ejecución

1. **Extracción de parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Ruta de la imagen de entrada**: La captura de pantalla a analizar (obligatorio)
   - **Modo**: `analyze` (análisis de errores) o `tutorial` (pasos de operación) (opcional, por defecto: `analyze`)
   - **Ruta de salida**: Por defecto `docs/bootcamp/screenshots/{mode}_{timestamp}.html` si se omite

2. **Ejecución de la herramienta**:
   Ejecute el comando en el siguiente formato.

   ```bash
   # Modo de análisis de errores (por defecto)
   uv run python tools/screenshot_analyzer.py "{ruta_imagen_entrada}" --mode analyze

   # Modo de tutorial de operación
   uv run python tools/screenshot_analyzer.py "{ruta_imagen_entrada}" --mode tutorial
   ```

3. **Verificación de resultados**:
   - Confirme la ruta del archivo HTML generado e infórmelo al usuario.
   - Proporcione instrucciones sobre cómo abrirlo con Live Server.
   - Muestre los mensajes de error si ocurre algún problema.

## Ejemplos de uso

### Análisis de errores (modo Analyze)
```
/screenshot-analyzer error.png
```
o
```
/screenshot-analyzer error.png --mode analyze
```

### Generación de tutorial de operación (modo Tutorial)
```
/screenshot-analyzer menu.png --mode tutorial
```

### Ejecutar sin anotaciones
```
/screenshot-analyzer error.png --no-annotate
```

### Especificar destino de salida
```
/screenshot-analyzer error.png --output docs/report/error_analysis.html
```

## Notas

- Requiere `GEMINI_API_KEY` o `GOOGLE_API_KEY` para ejecutarse.
- En el modo Tutorial, se generan imágenes anotadas para cada paso, por lo que el procesamiento puede tardar.
- El archivo de imagen original no se modifica (las imágenes anotadas se guardan como archivos separados).
