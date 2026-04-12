---
name: video-audio
description: "Video audio generation skill. Generates audio files from scenes.json narrations using ElevenLabs TTS API, outputting in a format that can be synced with video. Triggered by 'Generate narration', 'TTS', 'Add audio', etc."
triggers:
  - Generate narration
  - Generate audio
  - TTS read aloud
  - Add audio to video
  - Choose a voice
  - video-audio
  - ElevenLabs
---

# Video Audio (TTS)

Generates audio from scenes.json narration fields using ElevenLabs TTS.

## Quick Start

```bash
# Generate a single combined file for all narrations
python skills/video-audio/scripts/generate_audio.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --voice akari \
  --output output/narration.mp3

# Generate individual files per frame
python skills/video-audio/scripts/generate_audio.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --voice akari \
  --per-scene
```

## Japanese Voice List

| ID | Name | Characteristics | Alias |
|----|------|-----------------|-------|
| EkK6wL8GaH8IgBZTTDGJ | Akari | Bright, natural female | `akari` |
| EnLxjGl88dNO1Jv6AZk2 | Miyu | Trustworthy with depth | `miyu` |
| G3EZ8O36A0x9lmeOtr0f | Kaori | Friendly and approachable | `kaori` |
| PmgfHCGeS5b7sH90BOOJ | Fumi | Calm female | `fumi` |
| StTDrGrPSyfaHGmzwXbj | Masa | Japanese male | `masa` |
| gARvXPexe5VF3cKZBian | Mitsuki | Neutral | `mitsuki` |
| YOUR_VOICE_ID | Custom Voice | Custom voice | `custom` |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--voice` | `akari` | Voice name or ID |
| `--model` | `eleven_multilingual_v2` | TTS model |
| `--stability` | `0.5` | Stability (0-1) |
| `--similarity` | `0.75` | Similarity boost (0-1) |
| `--speed` | `1.0` | Playback speed |
| `--per-scene` | false | Output individual file per frame |
| `--silence-gap` | `0.3` | Silence between scenes (seconds) |
| `--output` | auto | Output file path |

## Output

### Combined Mode (Default)
```
{storyboard_dir}/audio/narration.mp3    # All narrations combined
{storyboard_dir}/audio/narration.json   # Timestamp information
```

### Per-scene Mode
```
{storyboard_dir}/audio/frame_01.mp3
{storyboard_dir}/audio/frame_02.mp3
...
{storyboard_dir}/audio/timestamps.json  # Start/end times for each frame
```

## timestamps.json Format
```json
{
  "total_duration": 18.5,
  "scenes": [
    {
      "frame_number": 1,
      "start": 0.0,
      "end": 2.8,
      "duration": 2.8,
      "text": "Narration script"
    }
  ]
}
```

## Integration with Video

Pass to compose_video.py via the `--audio` option:
```bash
python skills/video-editor/scripts/compose_video.py \
  --storyboard-dir output/storyboard/session \
  --audio output/storyboard/session/audio/narration.mp3
```

For Remotion, place at `public/audio/narration.mp3` and reference with the `<Audio>` component.

## Environment Variables
- `ELEVEN_API_KEY` -- ElevenLabs API key (required)

## Dependencies
- Python 3.11+
- curl (ElevenLabs API calls)
- ffmpeg (audio concatenation, `.bin/ffmpeg`)
