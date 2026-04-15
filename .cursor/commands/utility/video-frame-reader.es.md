# Video Frame Reader - Extracción de fotogramas clave de video

Este comando extrae fotogramas clave de videos, opcionalmente realiza análisis de fotogramas con Gemini Vision y genera los resultados en JSON.

## Requisitos previos
- `ffmpeg` instalado
- Python3 + `Pillow` + `numpy`
- Clave API de Gemini (si se realiza análisis)

## Pasos de ejecución

1. **Extracción de parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Ruta del archivo de video** (obligatorio)
   - **Directorio de salida** (opcional; por defecto `{nombre_video}_keyframes`)
   - **threshold** (opcional, por defecto: 0.85)
   - **quality** (opcional, por defecto: 30)
   - **scale** (opcional, por defecto: 0.3)
   - **intent** (opcional, perspectiva del análisis)
   - **max-frames** (opcional, fotogramas máximos para el análisis; por defecto: 12)

2. **Configuración inicial del venv** (si no se ha realizado):
   ```bash
   cd .cursor/skills/video-frame-reader
   python3 -m venv venv          
   source venv/bin/activate      # macOS/Linux/WSL
   pip install Pillow numpy --quiet
   ```

3. **Extracción + Análisis**:
   ```bash
   uv run python tools/video_frame_analyzer.py "{ruta_video}" -o "{directorio_salida}" -t {threshold} -q {quality} -s {scale} --intent "{intent}" --max-frames {max_frames}
   ```

4. **Verificar resultados**:
   - Confirme que la salida JSON contiene tanto `extraction` como `analysis`
   - Agregue `--no-analyze` para omitir el análisis
   - Muestre cualquier `error` tal como está

## Ejemplos de uso

### Básico
```
/video-frame-reader /path/to/video.mp4
```

### Reducción de tokens más agresiva
```
/video-frame-reader /path/to/video.mp4 -t 0.75 -q 20 -s 0.2
```

### Especificar perspectiva del análisis
```
/video-frame-reader /path/to/video.mp4 --intent "Verificar si las transiciones de pantalla después de los clics en botones se ven naturales"
```
