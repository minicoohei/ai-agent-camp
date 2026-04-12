---
name: viral-short-video
description: "Habilidad de generación de guiones y storyboards para videos virales de TikTok/YouTube Shorts. Incorpora automáticamente técnicas virales investigadas (gancho de 3 segundos, estructura modular, puente de loop, texto flash, pantalla dividida, etc.) en la creación de guiones y storyboards. Se activa con 'Guión de video TikTok', 'Quiero hacer un video viral', 'Guión de video corto', etc."
triggers:
  - Quiero hacer un video viral
  - Guión de video TikTok
  - Guión de video corto
  - Quiero hacer un video que se viralice
  - Plan de video para Reels
  - viral-short-video
  - TikTok Shorts
---

# Video Corto Viral - Guión y Storyboard de Video Corto Viral

Pipeline de producción de videos virales para TikTok / YouTube Shorts.
Incorpora automáticamente técnicas virales basadas en investigación en los guiones,
integrándose con `storyboard-generator` / `video-editor` existentes para la producción de video.

## Vista General del Pipeline Completo

```
[Tema/Producto/Objetivo]
  |
[generate_viral_script.py]  <- Núcleo de esta habilidad
  +-- viral_script.json       (Guión estructurado viral)
  +-- scenes.json             (Compatible con storyboard-generator)
  +-- hook_variants.json      (Variaciones de gancho x3)
  +-- hook_analysis.json      (--analyze-video: análisis de gancho pico)
  |
[storyboard-generator]       <- Habilidad existente
  +-- frames/                 (Imágenes de storyboard)
  +-- scenes.json             (Mejorado)
  |
[video-editor]               <- Habilidad existente (mejorada)
  +-- Incrustación de subtítulos
  +-- Inserción de texto flash
  +-- Composición de pantalla dividida (método de superposición de fondo)
  +-- Video final.mp4
```

## Recursos Incluidos

### Recursos de Fondo de Gameplay (`assets/gameplay/`)

| Nombre de Preset | Juego | Duración | Notas |
|-----------------|-------|----------|-------|
| subway_surfers | Subway Surfers | 26 min | Vertical HD, Sin Copyright |
| minecraft | Minecraft Parkour | 5 min | Vertical 2K 60fps, Sin Copyright |

### Recursos de Compilación de Ganchos (`assets/hooks/`)

| Nombre de Preset | Contenido | Caso de Uso |
|-----------------|-----------|-------------|
| hook_viral_10 | 10 TikTok Hooks You Can Use To Go Viral | Ejemplos de ganchos: 10 patrones |
| hook_trifecta | This HOOK Combo Will Get You Viral on TikTok | Estrategia de tríada de ganchos + ejemplos |
| hook_600k_gmv | This Hook Made $600K GMV on TikTok Shop | Desglose de gancho de $600K en ingresos |

Configuración inicial: `bash skills/viral-short-video/scripts/download_assets.sh`

## Uso

```bash
# Básico: Generar guión viral desde tema
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "Cómo usar una billetera cripto de forma segura" \
  --duration 30 \
  --target "Principiantes en cripto de 20-30 años" \
  --session "crypto_wallet_tips"

# Generar guión con nombre de producto
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "Reducir comisiones de transferencia un 90% con esta app" \
  --product "Mi Producto" \
  --duration 15 \
  --tone casual \
  --session "product_fees"

# De principio a fin con generación de storyboard
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "Cómo hacer videos con IA" \
  --duration 60 \
  --generate-storyboard \
  --character "Mujer japonesa de 20 años, ropa casual" \
  --session "ai_video_tutorial"

# Dry-run (solo guión, sin generación de imágenes)
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "3 errores de inversión" \
  --duration 30 \
  --dry-run

# Extracción de gancho pico: Analizar video de compilación de ganchos incluido
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video hook_viral_10 \
  --topic "Billetera cripto" --duration 30

# Extracción de gancho pico: Analizar video personalizado
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video path/to/any_viral_video.mp4 \
  --topic "Introducción de app" --duration 15

# Extracción de gancho pico: Dry-run (solo mostrar resultados de análisis)
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video hook_trifecta \
  --topic "Trabajo extra" --dry-run
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| --topic | Sí | - | Tema/tópico del video |
| --product | No | - | Nombre del producto/servicio |
| --duration | No | 30 | Duración del video (segundos): 15, 30, 60 |
| --target | No | - | Descripción de la audiencia objetivo |
| --tone | No | casual | Tono: casual, professional, energetic, storytelling |
| --hook-style | No | auto | Estilo de gancho: curiosity, fomo, social_proof, pattern_interrupt, contrarian |
| --split-screen | No | false | Incluir instrucciones de pantalla dividida |
| --flash-text | No | true | Incluir texto flash (activador de re-visualización) |
| --loop | No | true | Incluir puente de loop (retorno al inicio) |
| --variants | No | 3 | Número de variaciones de gancho |
| --generate-storyboard | No | false | Llamar a storyboard-generator después de generar scenes.json |
| --character | No | - | Descripción del personaje para storyboard |
| --session | No | - | Nombre de sesión (nombre de carpeta de salida) |
| --dry-run | No | false | Generar solo guión (llamadas API mínimas) |
| --lang | No | ja | Idioma del guión: ja, en |
| --analyze-video | No | - | Extracción de gancho pico. Nombre de preset (hook_viral_10, hook_trifecta, hook_600k_gmv) o ruta de archivo |

## Estructura de Salida

```
output/viral-scripts/
+-- YYYYMMDD_HHMMSS_session/
    +-- viral_script.json      # Guión principal (estructura viral)
    +-- scenes.json            # Formato compatible con storyboard-generator
    +-- hook_variants.json     # Variaciones de gancho
    +-- hook_analysis.json     # Resultados de análisis de gancho pico (solo --analyze-video)
    +-- storyboard/            # Solo --generate-storyboard
        +-- frames/
        +-- storyboard_sheet.png
        +-- scenes.json
```

## Formato de viral_script.json

```json
{
  "meta": {
    "topic": "Tema",
    "product": "Nombre del producto",
    "duration": 30,
    "target": "Audiencia objetivo",
    "tone": "casual"
  },
  "hook": {
    "text": "Honestamente no quería compartir esto pero...",
    "duration": 3,
    "trigger_type": "curiosity_gap",
    "visual_note": "Ojos bien abiertos, hablando a cámara",
    "emotion": "surprise"
  },
  "body": [
    {
      "text": "En realidad, solo usando esta app, las comisiones de transferencia...",
      "duration": 5,
      "visual_note": "Mostrando pantalla del smartphone mientras explica",
      "motion_type": "i2v"
    }
  ],
  "cta": {
    "text": "Enlace en el perfil. Revísalo ahora",
    "duration": 3,
    "visual_note": "Señalando la parte inferior de la pantalla",
    "emotion": "friendly"
  },
  "loop_bridge": {
    "enabled": true,
    "end_text": "Eso que mencioné antes...",
    "connects_to": "hook",
    "visual_note": "Regresar al mismo ángulo de cámara de la apertura"
  },
  "flash_text": {
    "enabled": true,
    "text": "¿Viste hasta el final? Míralo de nuevo",
    "color": "red",
    "duration_frames": 3,
    "position": "center"
  },
  "viral_techniques": {
    "split_screen": false,
    "captions": true,
    "lofi_aesthetic": true,
    "fast_pace": true,
    "speech_speed": 1.2
  },
  "hook_variants": [
    {
      "text": "El 99% de las personas no sabe esto...",
      "trigger_type": "curiosity_gap"
    },
    {
      "text": "Si te pierdes esto te vas a arrepentir en serio",
      "trigger_type": "fomo"
    },
    {
      "text": "1 millón de personas lo usan pero nadie habla de esto",
      "trigger_type": "social_proof"
    }
  ]
}
```

---

## Hoja de Referencia de Técnicas Virales

### 1. Gancho de 3 Segundos Inicial (Lo Más Importante)

**Datos**: Retención de 3 segundos mayor al 65% -> 4-7x impresiones / engagement +340%

**7 Activadores Psicológicos** (usados en 84.3% de videos virales):

| # | Activador | Ejemplo de Gancho |
|---|-----------|-------------------|
| 1 | Interrupción de Patrón | "Espera, mira esto" |
| 2 | Brecha de Curiosidad | "Nadie te dice esto sobre..." |
| 3 | FOMO | "Te estás perdiendo de..." |
| 4 | Prueba Social | "1 millón de personas ya lo usan" |
| 5 | Activación Emocional | "No puedo creer que funcione" |
| 6 | Sorpresa | (ojos bien abiertos + pausa de 1s) |
| 7 | Relevancia Personal | "Si eres [objetivo], mira esto" |

### 2. Estructura Modular

```text
[Gancho: 0-3s] -> [Cuerpo: 3-15s] -> [CTA: 15s+]
```

- Efecto: Costo de producción -40%, velocidad de prueba 2x
- Intercambiar solo la parte del Gancho para pruebas A/B

### 3. Puente de Loop

- Efecto: Re-visualización = impulso de algoritmo +84%
- 70% tasa de completado -> promoción del algoritmo
- 92% tasa de completado -> 3x alcance (certificación de Contenido Pegajoso)
- Patrón: Al final del video "Sobre lo que mencioné antes..." -> regresa al inicio

### 4. Texto Flash (Activador de Re-visualización)

- Mostrar texto rojo/negro durante 2-3 fotogramas (menos de 0.1 segundos) al final
- Velocidad demasiado rápida para leer conscientemente -> "¿Acabo de ver algo?" -> Re-visualización
- Ejemplos de texto: "Míralo de nuevo", "Mensaje oculto", "¿Lo notaste?"
- Color: Rojo (urgencia/visibilidad) o texto blanco sobre fondo negro (misterioso)

### 5. Gameplay de Fondo (Método de Superposición)

- Fondo en pantalla completa: Minecraft/Subway Surfers -> superponer contenido principal encima
- Estilo TikTok: Gameplay en pantalla completa (1080x1920), contenido principal en mitad superior (1080x960)
- Efecto: Tiempo promedio de visualización +40%, comentarios/compartidos 2x
- Especialmente efectivo para 67% de Gen Z (18-24)
- Recursos de preset incluidos: `subway_surfers`, `minecraft`
- Nota: Puede dañar la imagen de marca -> recomendado para publicaciones orgánicas

### 6. Extracción de Gancho Pico

- Identificar automáticamente los momentos de gancho más fuertes de videos virales
- Puntuación vía video-frame-reader + Gemini Flash Vision
- Generar automáticamente propuestas de guión reestructurado a partir de patrones de gancho extraídos
- 3 recursos de compilación de ganchos incluidos disponibles para análisis inmediato

### 7. Subtítulos

- 85% miran en silencio -> subtítulos aumentan retención +31%, engagement +38%
- Zona segura TikTok: Posición Y 55-65% (evitar 15% superior, 20% inferior)
- Japonés: 5-8 caracteres por línea, máximo 2 líneas, negrita blanca + trazo negro 3px

### 8. Sensación Lo-fi (Estilo UGC)

- Estilo UGC vs calidad profesional: CTR 4x, tasa de conversión +29%
- Ambiente casual tipo grabación con iPhone
- Fondo: Ambientes naturales tipo hogar, café

### 9. Ritmo de Audio

- Velocidad de habla 1.1-1.3x -> previene abandono
- Reducir pausas para aumentar densidad de información

---

## Habilidades Relacionadas

| Habilidad | Rol | Método de Integración |
|-----------|-----|----------------------|
| `storyboard-generator` | scenes.json -> imágenes de storyboard | Integración automática con `--generate-storyboard` |
| `video-editor` | Composición de video final (subtítulos/flash/superposición de fondo) | `compose_video.py --flash-text --split-screen subway_surfers` |
| `video-frame-reader` | Extracción de fotogramas clave de video | Integración automática con `--analyze-video` |
| `banner-creator` | Generación de miniaturas | Ejecutar por separado |
| `social-content` | Generación de texto de publicación y hashtags | Ejecutar por separado |

## Requisitos

- `GEMINI_API_KEY`: Para Gemini Flash (generación de guiones)
- Paquetes Python: google-genai, python-dotenv
- Dependencias de `storyboard-generator` (solo generación de storyboard)
- `ffmpeg` (solo composición de video)

## Frases de Activación

- "Crear un guión de video TikTok"
- "Quiero hacer un video viral"
- "Guión de video corto"
- "Generar un guión para TikTok"
- "Quiero hacer un video que se viralice"
- "Plan de video para Reels"
