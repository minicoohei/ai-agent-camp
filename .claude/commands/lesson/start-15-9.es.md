---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~30 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "product-demo", "avatar", "kling"]
nonInteractiveMode: deferred
---
# 15-9: Video de Demostración de Producto

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 15-9: Video de Demostración de Producto**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar un video donde un avatar con pantalla verde presenta una aplicación en la pantalla de un telefono |
| Duración | ~30 min |
| Herramientas utilizadas | product_demo_pipeline (Gemini + ElevenLabs + Fabric/Kling + FFmpeg) |
| Requisitos previos | FAL_KEY, GEMINI_API_KEY, ELEVEN_API_KEY configurados |
| Guía de costos | Revise la [Guía de Estrategia de Costos de IA de Video](https://ai-agent.camp/es/course/module-15) primero (recomendado) |
| Página del curso | Consulte [Module 15: Generación de Video](https://ai-agent.camp/es/course/module-15) en paralelo |

**Estimación de costos**: Motor Fabric 480p aprox. **$2.50/video**, Kling aprox. **$2.80/video**

**Flujo de la sesión:**
1. Verificar entorno y preparar capturas de pantalla
2. Seleccionar motor y ejecutar pipeline
3. Revisar y ajustar el guion
4. Revisar la composición con pantalla verde
5. Agregar música de fondo (opcional)
6. Revisar video completado y resumen de costos

Al finalizar esta sesión, un video de demostración de producto estará guardado en `output/ugc/product_demo/`.

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Verificación de Preparación

Primero, confirme que todo está listo.

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
      {"id": "cost_guide", "label": "Quiero ver la guia de costos primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra leccion"}
    ]
  }]
}
```

(ready -> Ir al Paso 1)
(check_prereq -> Ejecutar verificación de FAL_KEY / GEMINI_API_KEY / ELEVEN_API_KEY)
(cost_guide -> Guiar a https://ai-agent.camp/es/course/module-15)
(different_lesson -> Mostrar lista de modulos)

---

## Paso 1: Verificar Entorno y Preparar Capturas

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Verificar entorno",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Contenido:**
```text
Verifique lo siguiente:
1. Las claves API requeridas estan configuradas como variables de entorno
   - echo $FAL_KEY
   - echo $GEMINI_API_KEY
   - echo $ELEVEN_API_KEY (o $ELEVENLABS_API_KEY)
2. FFmpeg esta instalado
   - ffmpeg -version
3. Prepare una captura de pantalla de la aplicacion/servicio que desea presentar
   - Tamano de pantalla de telefono (vertical) recomendado
   - Si no tiene una disponible, se creara una muestra
```

**Resultado esperado**: Las claves API están confirmadas y las capturas de pantalla están listas.

---

## Paso 2: Ejecución Automatizada Completa del Pipeline

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Seleccionar motor de generacion de video",
  "questions": [{
    "id": "engine_choice",
    "prompt": "Que motor desea usar?",
    "options": [
      {"id": "fabric", "label": "Fabric 1.0 (buena relacion calidad-precio $2.50, con lip sync)"},
      {"id": "kling", "label": "Kling 2.6 Pro (movimiento natural $2.80, estilo UGC)"},
      {"id": "veo", "label": "Veo 3.1 (maxima calidad $15+, cuidado con el costo)"},
      {"id": "longcat", "label": "LongCat (animacion de cuerpo completo $3.00)"}
    ]
  }]
}
```

**Ejecución posterior a la selección:**

```bash
cd ~/ai-agent-camp
python -m ugc.product_demo_pipeline \
  --product "(nombre del producto especificado por el usuario)" \
  --screenshot ./(captura del usuario) \
  --engine fabric \
  --platform tiktok \
  --resolution 480p
```

**6 pasos que el pipeline ejecuta automáticamente:**
1. **Generación de guion** (Gemini Flash) -> `script.txt`
2. **Generación de imagen de avatar** (Gemini Image) -> `avatar.png` (persona sosteniendo telefono en pantalla verde)
3. **Generación de audio TTS** (ElevenLabs) -> `speech.mp3`
4. **Generación de video** (Fabric/Kling/Veo) -> `raw_video.mp4`
5. **Composición con pantalla verde** (FFmpeg) -> `composited.mp4` (captura compuesta en pantalla del telefono)
6. **Salida final** -> `final.mp4`

**Resultado esperado**: Un video se genera en `output/ugc/product_demo/`.

---

## Paso 3: Revisar y Ajustar el Guion Generado

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Revision del guion",
  "questions": [{
    "id": "step_action",
    "prompt": "Desea revisar el guion generado?",
    "options": [
      {"id": "check", "label": "Revisar y editar si es necesario"},
      {"id": "regenerate", "label": "Regenerar un guion diferente"},
      {"id": "skip", "label": "Continuar tal cual"}
    ]
  }]
}
```

**Contenido:**
```text
Lea script.txt en output/ugc/product_demo/ y revise el contenido.

Puntos a verificar:
- El gancho (primeros 2 segundos) capta la atencion?
- Transmite el atractivo del producto?
- Suena natural como lenguaje hablado?
- Es demasiado largo (30 segundos = aprox. 90 caracteres objetivo)?
```

---

## Paso 4: Revisar la Composición con Pantalla Verde

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 4: Revisar resultado de composicion",
  "questions": [{
    "id": "step_action",
    "prompt": "Desea revisar el resultado de la composicion?",
    "options": [
      {"id": "check", "label": "Revisar el video"},
      {"id": "retry_opencv", "label": "Recomponer con backend OpenCV"},
      {"id": "skip", "label": "Continuar"}
    ]
  }]
}
```

**Puntos a verificar:**
- La captura de pantalla está correctamente compuesta en la pantalla del telefono?
- Hay algún residuo verde?
- El balance entre el avatar y la captura es bueno?

---

## Paso 5: Agregar Música de Fondo (Opcional)

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 5: Agregar musica de fondo",
  "questions": [{
    "id": "bgm_choice",
    "prompt": "Desea agregar musica de fondo?",
    "options": [
      {"id": "add_bgm", "label": "Agregar musica de fondo (especificar archivo)"},
      {"id": "no_bgm", "label": "Completar sin musica de fondo"},
      {"id": "generate", "label": "Generar musica de fondo con Suno AI (fal.ai, cubierto en una leccion posterior)"}
    ]
  }]
}
```

**Agregar música de fondo:**
```python
from tools.ugc.audio_post import mix_bgm
mix_bgm(
    video_path="output/ugc/product_demo/.../composited.mp4",
    bgm_path="./my_bgm.mp3",
    output_path="output/ugc/product_demo/.../final_with_bgm.mp4",
    bgm_volume=0.15,
)
```

---

## Paso 6: Revisar Video Completado y Resumen de Costos

**Contenido:**
```text
Lea summary.json en output/ugc/product_demo/ y revise los resultados.

Elementos a verificar:
- Ruta del video final
- Motor utilizado
- Costo de generacion ($)
- Exito/fallo de cada paso

Consejos de optimizacion de costos:
- Usar 480p reduce el costo de Fabric a la mitad
- Reutilizar la imagen del avatar ahorra $0.02 cada vez
- Para generacion masiva, considere servicios de tarifa plana como GenSpark
  -> Detalles: https://ai-agent.camp/es/course/module-15
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
      {"id": "trouble_1", "label": "Error de clave API"},
      {"id": "trouble_2", "label": "La composicion con pantalla verde fallo"},
      {"id": "trouble_3", "label": "La generacion de video expiro"},
      {"id": "trouble_4", "label": "El audio y el movimiento de labios estan desincronizados"}
    ]
  }]
}
```

### Problema 1: "Error de clave API"
**Causa**: Las variables de entorno no están configuradas
**Solución**:
```bash
cat .env | grep -E "FAL_KEY|GEMINI|ELEVEN"    # Mac/Linux/WSL
```

### Problema 2: "La composición con pantalla verde falló"
**Causa**: Dificultad para detectar el verde en la imagen
**Solución**: Pruebe el backend OpenCV
```python
from ugc import composite_video
composite_video(video, screenshot, output, backend="opencv")
```

### Problema 3: "La generación de video expiro"
**Causa**: El procesamiento de fal.ai es lento
**Solución**: Cambie a Fabric o reintente

### Problema 4: "El audio y el movimiento de labios están desincronizados"
**Solución**: Aplique corrección de sincronización labial con MuseTalk
```python
from ugc.audio_post import apply_musetalk
apply_musetalk(video, audio, output)
```

---

## Punto de Control
- [ ] Las claves API están correctamente configuradas
- [ ] Las capturas de pantalla fueron preparadas
- [ ] El pipeline se completó correctamente
- [ ] La composición con pantalla verde fue exitosa
- [ ] El video final fue revisado
- [ ] Comprendio la guía de estrategia de costos

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
      {"id": "next_auto", "label": "Siguiente modulo (/start-16-1)"},
      {"id": "retry", "label": "Regenerar el mismo video con un motor diferente"},
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

