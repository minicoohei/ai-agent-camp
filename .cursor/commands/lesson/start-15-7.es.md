---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~45 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "music-video", "suno", "beat-sync"]
nonInteractiveMode: deferred
---
# Lección 15-7: Video Musical

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 15-7: Video Musical**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar una pista musical con IA, combinar videos de escenas sincronizados con el ritmo para crear un video musical |
| Duración | ~45 min |
| Herramientas utilizadas | mv_pipeline (Suno/fal.ai + librosa + Gemini + Kling + FFmpeg) |
| Requisitos previos | FAL_KEY, GEMINI_API_KEY configurados. uv add librosa recomendado |
| Guía de costos | Revise la [Guía de Estrategia de Costos de IA de Video](https://ai-agent.camp/es/course/module-15) primero (recomendado) |
| Página del curso | Consulte [Module 15: Generación de Video](https://ai-agent.camp/es/course/module-15) en paralelo |

**Estimación de costos**:
- I2V completo (Kling x8) + música IA: aprox. **$6-12**
- Optimizado en costos (A-roll x3 + B-roll x5): aprox. **$3-5**
- Música existente + solo Ken Burns: aprox. **$0.10** (solo generación de imagenes)

**Flujo de la sesión:**
1. Verificar entorno y preparar música
2. Generación de música con IA o cargar música existente
3. Análisis de ritmo y línea de tiempo de escenas
4. Generación de imagenes de escenas + clips de video
5. Union sincronizada con el ritmo y mezcla musical
6. Revisar video musical completado

Al finalizar esta sesión, un video musical estará guardado en `output/ugc/mv/`.

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Verificación de Preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "install_librosa", "label": "Quiero instalar librosa"},
      {"id": "cost_guide", "label": "Quiero ver la guia de costos primero"}
    ]
  }]
}
```

(install_librosa -> Ejecutar `uv add librosa`)

---

## Paso 1: Verificar Entorno y Preparar Música

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Preparar musica",
  "questions": [{
    "id": "music_source",
    "prompt": "Como desea preparar la musica?",
    "options": [
      {"id": "generate", "label": "Generar musica con IA (fal.ai Suno)"},
      {"id": "existing", "label": "Usar un archivo de musica existente"},
      {"id": "explain", "label": "Explicar como funciona la generacion de musica con IA"}
    ]
  }]
}
```

---

## Paso 2: Ejecutar Pipeline

**Generación de música con IA + creación de video musical:**
```bash
cd ~/ai-agent-camp
python -m ugc.mv_pipeline \
  --prompt "Bright pop song, positive lyrics, tempo 120BPM" \
  --style anime \
  --engine kling \
  --num-scenes 8 \
  --cost-optimize --aroll-count 3
```

**7 pasos que el pipeline ejecuta automáticamente:**
1. **Preparación de música** -> Generación con IA o copia de archivo existente
2. **Análisis de ritmo** (librosa) -> `beat_analysis.json`
3. **Generación de prompts de escena** (Gemini) -> `scenes.json`
4. **Generación de imagenes de fotogramas** (Gemini Image) -> 8 imagenes de escenas
5. **Generación de clips de video** (Kling I2V + Ken Burns) -> 8 clips
6. **Union sincronizada con el ritmo** (FFmpeg xfade) -> `joined.mp4`
7. **Mezcla musical** (FFmpeg) -> `final.mp4`

---

## Paso 3: Revisar Análisis de Ritmo

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Resultados del analisis de ritmo",
  "questions": [{
    "id": "step_action",
    "prompt": "Desea revisar los resultados del analisis de ritmo?",
    "options": [
      {"id": "check", "label": "Revisar resultados del analisis"},
      {"id": "explain_beat", "label": "Explicar la mecanica de sincronizacion de ritmo"},
      {"id": "skip", "label": "Continuar"}
    ]
  }]
}
```

**Mecánica de sincronización de ritmo:**
```text
Detectar posiciones de ritmo en la musica
    |
Dividir en downbeats (ritmos fuertes)
    |
Secciones de chorus -> A-roll (I2V dinamico)
Secciones de verse -> B-roll (metraje calmado Ken Burns)
    |
Transiciones de corte en posiciones de ritmo
```

---

## Paso 4: Revisar Imagenes de Escenas y Clips de Video

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 4: Revisar clips",
  "questions": [{
    "id": "step_action",
    "prompt": "Seleccione metodo de revision",
    "options": [
      {"id": "check_frames", "label": "Revisar imagenes de fotogramas"},
      {"id": "check_clips", "label": "Revisar clips de video"},
      {"id": "regenerate", "label": "Regenerar escenas especificas"},
      {"id": "skip", "label": "Continuar"}
    ]
  }]
}
```

**Estilos visuales disponibles:**
- `anime` - Estilo anime
- `cinematic_live` - Estilo cinematográfico de acción real
- `abstract` - Estilo abstracto/artistico
- `watercolor` - Estilo acuarela
- `pixel_art` - Estilo pixel art
- `vibrant_ugc` - Estilo vibrante para redes sociales

---

## Paso 5: Revisar Video Musical Completado y Resumen de Costos

**Contenido:**
```text
Revise summary.json en output/ugc/mv/.

Elementos a verificar:
- Ruta y duracion de la musica
- Estilo visual
- Numero de escenas (desglose A-roll / B-roll)
- Costo de generacion

Tecnicas de optimizacion de costos:
- Usar A-roll (I2V) solo para secciones de chorus para concentrar el impacto
- Usar B-roll Ken Burns para secciones de verse con metraje calmado
- Esto produce A-roll x3 + B-roll x5 = $2.10 + $0 = $2.10 (solo video)
```

---

## Problemas Comunes y Soluciones

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "La generacion de musica con IA falla"},
      {"id": "trouble_2", "label": "Error al instalar librosa"},
      {"id": "trouble_3", "label": "Los ritmos y las transiciones de escena estan desincronizados"},
      {"id": "trouble_4", "label": "El ambiente del video y la musica no coinciden"}
    ]
  }]
}
```

### Problema 1: "La generación de música con IA falla"
**Solución**: Use la opción --music con un archivo de música existente

### Problema 2: "Error al instalar librosa"
**Solución**:
```bash
uv add librosa soundfile
# Si eso no funciona:
uv add librosa --no-deps
uv add soundfile numba
```

### Problema 3: "Ritmos y transiciones desincronizados"
**Solución**: Reduzca `--num-scenes` (8 -> 6) para alinearse mejor con los ritmos

### Problema 4: "El ambiente del video y la música no coinciden"
**Solución**: Cambie el estilo para que coincida con el género musical
- Pop -> `anime` o `vibrant_ugc`
- Rock -> `cinematic_live`
- Electrónica -> `abstract`
- Clasica -> `watercolor`

---

## Punto de Control
- [ ] Las claves API están correctamente configuradas
- [ ] La música fue preparada (generada con IA o existente)
- [ ] El análisis de ritmo fue ejecutado
- [ ] Las imagenes de escenas fueron generadas
- [ ] Los clips de video A-roll / B-roll fueron generados
- [ ] El video musical fue completado con sincronización de ritmo
- [ ] La mezcla musical fue exitosa

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente accion",
    "options": [
      {"id": "next_auto", "label": "Siguiente seccion (/start-15-8 Video de narracion de diapositivas)"},
      {"id": "retry", "label": "Regenerar con musica/estilo diferente"},
      {"id": "review_all", "label": "Revisar Module 15"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

## Enlaces de referencia (sincronizado con las slides de Module 15)

Cinco recursos para buscar plantillas o inspiración.

- [Dribbble (motion design portfolios)](https://dribbble.com/)
- [Envato Elements — video templates / logo animation](https://elements.envato.com/video-templates/logo+animation)
- [Placeit — minimalist motion-graphics intro maker](https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988)
- [YouTube — After Effects templates project channel](https://www.youtube.com/@paftereffectstemplatesproj6705)
- [YouTube — motion-graphics templates playlist](https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj)

