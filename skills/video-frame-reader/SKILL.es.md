---
name: video-frame-reader
description: "Habilidad para extraer fotogramas clave de archivos de video, deduplicarlos y optimizarlos, y luego analizar su contenido. Se activa con 'Muéstrame el contenido del video', 'Extraer fotogramas clave', 'Analizar este video', etc."
triggers:
  - Muéstrame el contenido del video
  - Extraer fotogramas clave
  - Analizar este video
  - Verificar el video
  - Ver grabación de pantalla
  - video-frame-reader
  - extracción de fotogramas clave
---

# Lector de Fotogramas de Video

Extrae fotogramas clave del video, presenta el costo en tokens y luego analiza.

## Requisitos

- ffmpeg (para extracción de fotogramas)
- Python 3 + Pillow + numpy

## Flujo de Trabajo

### 1. Capturar la Intención del Usuario

Comprender claramente por qué el usuario quiere que se analice el video:
- Ejemplo: "El comportamiento de transición de pantalla parece incorrecto"
- Ejemplo: "Quiero verificar la respuesta después de hacer clic en el botón"
- Ejemplo: "Ayúdeme a identificar problemas de rendimiento"

Esta intención se convierte en contexto importante para el análisis.

### 2. Crear venv (Solo la Primera Vez)

```bash
python3 -m venv skills/video-frame-reader/scripts/venv
source skills/video-frame-reader/scripts/venv/bin/activate    # Mac/Linux/WSL
pip install Pillow numpy --quiet
```

### 3. Extraer Fotogramas Clave

```bash
source skills/video-frame-reader/scripts/venv/bin/activate    # Mac/Linux/WSL
python3 skills/video-frame-reader/scripts/extract_keyframes.py "<ruta_video>"
```

Ejemplo de salida (JSON):
```json
{
  "keyframe_count": 52,
  "image_size": "266x576",
  "total_tokens": 10400,
  "cost_usd_opus": 0.156,
  "cost_usd_sonnet": 0.031,
  "cost_usd_haiku": 0.0104,
  "files": ["/.../key_0001.jpg", ...]
}
```

### 4. Presentar Costo

Después de la extracción, presente lo siguiente al usuario:

```
Extracción de fotogramas clave completada:
- Fotogramas extraídos: {keyframe_count}
- Tamaño de imagen: {image_size}
- Tokens estimados: {total_tokens}
- Estimación de costo: Haiku ${cost_usd_haiku} / Sonnet ${cost_usd_sonnet} / Opus ${cost_usd_opus}

¿Proceder con el análisis de fotogramas?
```

### 5. Invocar Subagente Después de la Aprobación

Después de la aprobación del usuario, invocar subagente usando la herramienta Task:

```
Task(
  subagent_type="general-purpose",
  model="haiku",
  description="Análisis de fotogramas",
  prompt="""
[Intención del Usuario]
{Intención capturada en el Paso 1}

[Archivos de Imagen de Fotogramas]
{Lista de rutas del array files}

Analice las imágenes de fotogramas anteriores e identifique problemas/comportamientos según la intención del usuario.
"""
)
```

Beneficios de este enfoque:
- La intención del usuario se incluye en el contexto de análisis
- El subagente puede enfocarse en análisis eficiente específico a la intención
- Procesado en contexto independiente para mejor eficiencia de tokens

## Opciones

| Opción | Predeterminado | Descripción |
|--------|----------------|-------------|
| `-t, --threshold` | 0.85 | Umbral de similitud (mayor = más fotogramas conservados) |
| `-q, --quality` | 30 | Calidad JPEG (1-100) |
| `-s, --scale` | 0.3 | Escala de redimensionamiento |
| `-o, --output` | `<nombre_video>_keyframes/` | Directorio de salida |

### Ejemplo de Reducción de Tokens

```bash
# Reducción más agresiva (umbral, calidad y tamaño más bajos)
python3 extract_keyframes.py video.mp4 -t 0.75 -q 20 -s 0.2
```

## Descripción General

Habilidad para extraer automáticamente fotogramas clave de archivos de video, deduplicarlos y optimizarlos, y luego analizar su contenido. Presenta el costo en tokens por adelantado y ejecuta el análisis mediante subagente después de la aprobación del usuario.

## Solución de Problemas

| Error | Solución |
|-------|---------|
| ffmpeg not found | `brew install ffmpeg` (Mac) o `apt install ffmpeg` (Linux) para instalar |
| No keyframes extracted | Bajar `--threshold` (ej., 0.75) para extraer más fotogramas |

## Criterios de Éxito

- [ ] Las imágenes de fotogramas clave están guardadas en el directorio de salida
- [ ] La estimación de costo en tokens se muestra en formato JSON
- [ ] Se devuelven resultados alineados con la intención de análisis del usuario

## Uso

Consulte la sección "Flujo de Trabajo" anterior. Ejemplos básicos:

```bash
# Extraer fotogramas clave
python3 skills/video-frame-reader/scripts/extract_keyframes.py "video.mp4"

# Con opciones de reducción de tokens
python3 skills/video-frame-reader/scripts/extract_keyframes.py "video.mp4" -t 0.75 -q 20 -s 0.2
```
