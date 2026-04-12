---
name: storyboard-generator
description: "Habilidad para generar automáticamente storyboards para videos UGC con IA. Garantiza consistencia del personaje generando una sola hoja y luego recortando fotogramas individuales. Se activa con solicitudes como 'Crear un storyboard', 'Generar storyboard', 'Crear flujo de video UGC', etc."
triggers:
  - Crear un storyboard
  - Generar storyboard
  - Crear flujo de video UGC
  - Storyboard de video
  - Crear composición de escenas
  - storyboard-generator
  - storyboard
---

# Generador de Storyboard (Generación de Storyboard UGC)

Herramienta de creación de storyboards para producción de videos UGC con IA. **Genera todos los fotogramas como una sola imagen de hoja y luego los recorta** para garantizar la consistencia del personaje.

## Modos de Generación

### Modo Hoja (Predeterminado / Recomendado)
- Genera todos los fotogramas como **una sola hoja de storyboard**
- Una llamada API para todos los fotogramas -> **Excelente consistencia del personaje**
- La cuadrícula se recorta en fotogramas individuales después de la generación
- Superior en velocidad, costo y consistencia

### Modo Individual (Legado)
- Genera un fotograma a la vez
- Intenta mantener la consistencia mediante imágenes de referencia del personaje, pero tiene limitaciones
- Para uso de respaldo

## Funcionalidades

### 1. Diseño de Personaje
- Generar imágenes de referencia a partir de prompts detallados del personaje
- Usar imágenes existentes del personaje como referencia
- En modo hoja, las imágenes de referencia se pasan durante la generación para mejorar la consistencia

### 2. Generación de Storyboard
- Genera automáticamente descripciones de escenas de 4/8/16 paneles a partir de escenarios (Gemini Flash)
- Modo hoja: Genera como una sola imagen de cuadrícula, luego recorta automáticamente
- Modo individual: Genera un fotograma a la vez, luego compone en cuadrícula
- Redimensionamiento automático (ancho predeterminado 540px, compresión JPG)

### 3. Narración e Instrucciones de Superposición de Texto
- Genera automáticamente guiones de narración (japonés) para cada fotograma
- Especifica contenido, posición y estilo de la superposición de texto
- Produce campos narration y text_overlay en scenes.json

### 4. Detección Automática de Tipo de Movimiento (motion_type)
- **static**: Centrado en texto -> Mantener como imagen fija
- **ken_burns**: Paisaje/composición estática -> Zoom/pan es suficiente (sin necesidad de i2V)
- **motion_graphics**: Transiciones UI/animación de texto -> Remotion es suficiente (sin necesidad de i2V)
- **i2v**: Movimiento de personaje/expresiones faciales -> Requiere conversión i2V (ej., fal.ai wan-i2v)
- Optimización de costos: Solo las escenas que realmente necesitan i2V se designan como i2V

### 5. Integración de Generación de Video
- Seleccionar cualquier StartFrame/EndFrame del storyboard
- Generación de Image-to-Video mediante fal.ai (wan-i2v)
- Soporte para especificación de movimiento de cámara

## Uso

```bash
# Recomendado: Modo hoja (generar hoja única -> recortar)
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "Video UGC explicando cómo usar la aplicación" \
    --character "Mujer japonesa de 20 años, ropa casual, expresión alegre" \
    --aspect-ratio 9:16 \
    --num-frames 8 \
    --mode sheet \
    --session "app_promo"

# Modo individual (respaldo)
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "Video de reseña de producto" \
    --character "..." \
    --mode individual \
    --session "product_review"

# Usando imagen de personaje existente
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "..." \
    --character-image "path/to/character.png" \
    --mode sheet \
    --session "with_ref"

# Generación de video (desde storyboard existente)
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --storyboard-dir "output/storyboard/YYYYMMDD_session" \
    --start-frame 1 \
    --end-frame 8 \
    --video-duration 10
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| --scenario | Sí | - | Escenario/tema del video |
| --character | No* | - | Prompt detallado del personaje |
| --character-image | No* | - | Ruta a la imagen de referencia del personaje existente |
| --mode | No | sheet | Modo de generación: sheet / individual |
| --aspect-ratio | No | 9:16 | Relación de aspecto (9:16, 16:9, 1:1, 4:3, 3:4) |
| --num-frames | No | 16 | Número de fotogramas (4, 8, 16) |
| --output-width | No | 540 | Ancho máximo de imagen de salida en px (0 para ilimitado) |
| --layout | No | auto | Diseño de cuadrícula (solo modo individual) |
| --session | No | - | Nombre de sesión (nombre de carpeta de salida) |
| --style | No | modern_clean | Estilo visual |
| --start-frame | No | - | Número de fotograma de inicio para generación de video |
| --end-frame | No | - | Número de fotograma final para generación de video |
| --video-duration | No | 5 | Duración del video (segundos): 5 o 10 |
| --camera-motion | No | - | Movimiento de cámara |

*Se requiere --character o --character-image

## Estructura de Salida

```
output/storyboard/
+-- YYYYMMDD_HHMMSS_session/
    +-- character_reference.png    # Imagen de referencia del personaje
    +-- storyboard_sheet.png       # Hoja original (modo hoja)
    +-- storyboard_grid.jpg        # Cuadrícula redimensionada
    +-- frames/
    |   +-- frame_01.jpg           # Fotogramas recortados (compresión JPG)
    |   +-- frame_02.jpg
    |   +-- ...
    +-- scenes.json                # Información de escena (narration, text_overlay, motion_type)
    +-- video/                     # Al generar video
        +-- output.mp4
```

## Comparación de Rendimiento

| | Hoja (Recomendado) | Individual |
|---|---|---|
| Llamadas API | 3 | N+2 |
| Tiempo de generación (8 fotogramas) | ~1 min | ~5 min |
| Tamaño de archivo | ~325KB | ~800KB |
| Consistencia del personaje | Excelente | Regular |

## Estilos Visuales

- `modern_clean` - Moderno y limpio (predeterminado)
- `animal_crossing` - Estilo Animal Crossing
- `vibrant_ugc` - UGC vibrante
- `anime` - Estilo anime

## Requisitos

- `GEMINI_API_KEY`: Para Gemini Flash/Generación de Imágenes
- `FAL_KEY`: Para generación de video i2V (solo al generar video)
- Paquetes Python: google-genai, Pillow, python-dotenv

## Configuración del Entorno

```bash
export GEMINI_API_KEY="your-key"    # Mac/Linux
export PYTHONPATH="/path/to/.pip/local/local/lib/python3.11/dist-packages:$PYTHONPATH"    # Mac/Linux
# Windows (cmd): set GEMINI_API_KEY=your-key
#                set PYTHONPATH=C:\path\to\site-packages;%PYTHONPATH%
# Windows (PowerShell): $env:GEMINI_API_KEY = "your-key"
#                       $env:PYTHONPATH = "C:\path\to\site-packages;$env:PYTHONPATH"
```

## Frases de Activación

- "Crear un storyboard"
- "Generar storyboard"
- "Storyboard de video UGC"
- "Crear flujo de video"

## Descripción General

Habilidad para generar automáticamente storyboards para producción de videos UGC con IA. Garantiza consistencia del personaje generando todos los fotogramas como una sola imagen de hoja y luego recortando. También soporta guiones de narración y detección automática del tipo de movimiento.

## Solución de Problemas

| Error | Solución |
|-------|---------|
| API key not found | Configure `GEMINI_API_KEY` como variable de entorno |
| Problemas de consistencia del personaje | Use `--mode sheet` (recomendado). El modo individual tiene menor consistencia |
| FAL_KEY not set | Solo es necesario para generación de video (i2V). No se necesita solo para generación de storyboard |

## Criterios de Éxito

- [ ] Las imágenes de storyboard para el número especificado de fotogramas están generadas en `output/storyboard/`
- [ ] `scenes.json` contiene narration y motion_type
- [ ] La apariencia del personaje es consistente entre fotogramas
