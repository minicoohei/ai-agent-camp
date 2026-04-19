---
name: video-editor
description: "Habilidad de edición de video para TikTok/YouTube. Incrusta subtítulos con ffmpeg, aplica efectos Ken Burns, combina escenas y sintetiza audio. Lee instrucciones de edición de scenes.json y produce el video final. También incluye componentes Remotion (para entornos locales). Se activa con 'Editar video', 'Agregar subtítulos', 'Crear video con subtítulos', etc."
triggers:
  - Editar video
  - Agregar subtítulos
  - Crear video con subtítulos
  - Combinar escenas
  - Exportar video
  - video-editor
  - edición ffmpeg
---

# Editor de Video

Genera el video final a partir de scenes.json + imágenes de fotogramas/clips de video.

## Dos Modos de Ejecución

### Modo ffmpeg (Compatible con sandbox / Recomendado)
No requiere Chromium. Funciona en entornos sandbox.

```bash
python skills/video-editor/scripts/compose_video.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --captions \
  --output output/final_tiktok.mp4
```

### Modo Remotion (Entorno local)
Requiere Chromium + Node.js. Animaciones más avanzadas.

```bash
npx remotion render TikTokVideo --output=out/tiktok_video.mp4 --root=remotion-editor/src/Root.tsx
```

## Pipeline ffmpeg

### 1. Preparación de Recursos
```
scenes.json -> Verificar motion_type de cada fotograma
  i2v        -> Usar video/{frame}_i2v.mp4
  ken_burns  -> Filtro zoompan de ffmpeg: imagen -> video
  static     -> Loop de ffmpeg: imagen -> video
  motion_graphics -> ffmpeg: imagen -> video (soporte futuro de animación de texto)
```

### 2. Normalización
Normalizar todos los clips a especificaciones unificadas:
- Resolución: 1080x1920 (9:16) o 1920x1080 (16:9)
- FPS: 30
- Códec: h264 / yuv420p
- Video i2V horizontal -> Convertir a vertical con fondo difuminado

### 3. Incrustación de Subtítulos (drawtext)
```bash
ffmpeg -i clip.mp4 -vf "drawtext=text='Texto':fontfile=/path/to/NotoSansJP-Bold.otf:\
  fontsize=64:fontcolor=white:borderw=3:bordercolor=black:\
  x=(w-text_w)/2:y=h*0.58" output.mp4
```

Especificaciones de subtítulos:
| Elemento | Recomendado para TikTok |
|----------|------------------------|
| Tamaño de fuente | 54-76px (5-7% del ancho de pantalla) |
| Caracteres/línea | Japonés 5-8 caracteres / Inglés 2-3 palabras |
| Líneas máximas | 2 |
| Fuente | Noto Sans JP Bold |
| Color | Blanco + trazo negro (3px) + sombra |
| Posición | Y: 55-65% (dentro de la zona segura de TikTok) |

### 4. Concatenación
```bash
ffmpeg -f concat -safe 0 -i concat.txt -c:v libx264 -pix_fmt yuv420p final.mp4
```

### 5. Síntesis de Audio (Opcional)
```bash
ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -shortest final_with_audio.mp4
```

## Zona Segura de TikTok
```
+---------------------+
|  Evitar 15% sup.    | <- Nombre de usuario/Botón seguir
+---------------------+
|   Contenido princ.  |
|  +---------------+  |
|  | Subtítulos    |  | <- Y: 55-65%
|  +---------------+  |
+---------------------+
|  Evitar 20% inf.    | <- Me gusta/Comentar/Compartir
+---------------------+
```

## Formato de scenes.json
```json
{
  "title": "Título del video",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:02",
      "motion_type": "i2v | ken_burns | static | motion_graphics",
      "narration": "Guión de narración",
      "text_overlay": {
        "main_text": "Subtítulo principal",
        "sub_text": "Subtítulo secundario",
        "position": "top | center | bottom",
        "style": "bold | subtitle | minimal"
      }
    }
  ]
}
```

## Dependencias
- ffmpeg (binario estático: `.bin/ffmpeg`)
- Python 3.11+ (compose_video.py)
- Fuente Noto Sans JP (para subtítulos)

## Componentes Remotion (Uso Local)
```
remotion-editor/src/
  components/
    Caption.tsx    # Subtítulos optimizados para TikTok (saltos de línea en japonés, animación pop-in)
    KenBurns.tsx   # Efectos de zoom/pan Ken Burns
  compositions/
    TikTokVideo.tsx # Composición principal 9:16
  Root.tsx         # Punto de entrada
```

## Habilidades Relacionadas
- `storyboard-generator` -- Recursos de entrada (fotogramas + scenes.json)
- `content-creator` -- Planificación de contenido
- `post-publisher` -- Publicación y distribución
