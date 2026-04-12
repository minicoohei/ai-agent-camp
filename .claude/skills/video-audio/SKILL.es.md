---
name: video-audio
description: "Habilidad de generación de audio para video. Genera archivos de audio a partir de narraciones en scenes.json usando la API TTS de ElevenLabs, produciendo un formato sincronizable con video. Se activa con 'Generar narración', 'TTS', 'Agregar audio', etc."
triggers:
  - Generar narración
  - Generar audio
  - Lectura TTS
  - Agregar audio al video
  - Elegir una voz
  - video-audio
  - ElevenLabs
---

# Audio de Video (TTS)

Genera audio a partir de los campos de narración de scenes.json usando ElevenLabs TTS.

## Inicio Rápido

```bash
# Generar un solo archivo combinado para todas las narraciones
python skills/video-audio/scripts/generate_audio.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --voice akari \
  --output output/narration.mp3

# Generar archivos individuales por fotograma
python skills/video-audio/scripts/generate_audio.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --voice akari \
  --per-scene
```

## Lista de Voces Japonesas

| ID | Nombre | Características | Alias |
|----|--------|-----------------|-------|
| EkK6wL8GaH8IgBZTTDGJ | Akari | Femenina brillante y natural | `akari` |
| EnLxjGl88dNO1Jv6AZk2 | Miyu | Confiable con profundidad | `miyu` |
| G3EZ8O36A0x9lmeOtr0f | Kaori | Amigable y accesible | `kaori` |
| PmgfHCGeS5b7sH90BOOJ | Fumi | Femenina tranquila | `fumi` |
| StTDrGrPSyfaHGmzwXbj | Masa | Masculina japonesa | `masa` |
| gARvXPexe5VF3cKZBian | Mitsuki | Neutral | `mitsuki` |
| YOUR_VOICE_ID | Voz Personalizada | Voz personalizada | `custom` |

## Opciones

| Opción | Predeterminado | Descripción |
|--------|----------------|-------------|
| `--voice` | `akari` | Nombre de voz o ID |
| `--model` | `eleven_multilingual_v2` | Modelo TTS |
| `--stability` | `0.5` | Estabilidad (0-1) |
| `--similarity` | `0.75` | Impulso de similitud (0-1) |
| `--speed` | `1.0` | Velocidad de reproducción |
| `--per-scene` | false | Producir archivo individual por fotograma |
| `--silence-gap` | `0.3` | Silencio entre escenas (segundos) |
| `--output` | auto | Ruta del archivo de salida |

## Salida

### Modo Combinado (Predeterminado)
```
{storyboard_dir}/audio/narration.mp3    # Todas las narraciones combinadas
{storyboard_dir}/audio/narration.json   # Información de marcas de tiempo
```

### Modo Por Escena
```
{storyboard_dir}/audio/frame_01.mp3
{storyboard_dir}/audio/frame_02.mp3
...
{storyboard_dir}/audio/timestamps.json  # Tiempos de inicio/fin de cada fotograma
```

## Formato de timestamps.json
```json
{
  "total_duration": 18.5,
  "scenes": [
    {
      "frame_number": 1,
      "start": 0.0,
      "end": 2.8,
      "duration": 2.8,
      "text": "Guión de narración"
    }
  ]
}
```

## Integración con Video

Pase a compose_video.py mediante la opción `--audio`:
```bash
python skills/video-editor/scripts/compose_video.py \
  --storyboard-dir output/storyboard/session \
  --audio output/storyboard/session/audio/narration.mp3
```

Para Remotion, coloque en `public/audio/narration.mp3` y referencie con el componente `<Audio>`.

## Variables de Entorno
- `ELEVEN_API_KEY` -- Clave API de ElevenLabs (requerida)

## Dependencias
- Python 3.11+
- curl (llamadas API de ElevenLabs)
- ffmpeg (concatenación de audio, `.bin/ffmpeg`)
