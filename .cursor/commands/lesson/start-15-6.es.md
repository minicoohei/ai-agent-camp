---
description: "When the user says /start-15-6 — Module 15 Lesson 15-6: Generar video anime desde storyboard (Gemini Image + Kling/Veo I2V + FFmpeg)"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~40 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "storyboard", "anime", "kling"]
---

# 15-6: Video Anime con Storyboard

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 15-6: Video Anime con Storyboard**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar imagenes de storyboard a partir de un escenario de texto, convertirlas en video con motores de IA y combinarlas en una obra única |
| Duración | ~40 min |
| Herramientas utilizadas | storyboard_anime_pipeline (Gemini + Kling/Veo + FFmpeg) |
| Requisitos previos | FAL_KEY, GEMINI_API_KEY configurados |
| Guía de costos | Revise la [Guía de Estrategia de Costos de IA de Video](https://ai-agent.camp/es/course/module-15) primero (recomendado) |
| Página del curso | Consulte [Module 15: Generación de Video](https://ai-agent.camp/es/course/module-15) en paralelo |

**Estimación de costos**:
- I2V completo (Kling x8): aprox. **$5.60**
- Modo optimizado en costos (A-roll x4 + B-roll x4): aprox. **$2.80**
- Solo B-roll Ken Burns (para pruebas): **$0** (procesamiento local)

**Flujo de la sesión:**
1. Verificar entorno y preparar escenario
2. Descomposición de escenas y generación de imagenes de fotogramas
3. Clasificación A-roll / B-roll y conversión a video
4. Union con crossfade y transiciones
5. Agregar música de fondo (opcional)
6. Revisar video completado y resumen de costos

Al finalizar esta sesión, un video anime con storyboard estará guardado en `output/ugc/storyboard_anime/`.

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
      {"id": "cost_guide", "label": "Quiero ver la guia de costos primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra leccion"}
    ]
  }]
}
```

---

## Paso 1: Verificar Entorno y Preparar Escenario

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
1. Las claves API requeridas estan configuradas
   - echo $FAL_KEY
   - echo $GEMINI_API_KEY
2. FFmpeg esta instalado
   - ffmpeg -version
3. Tenga un escenario (historia) en mente
   - Ejemplo: "Una historia de aventuras sobre una chica que encuentra criaturas misteriosas en un bosque magico"
   - Ejemplo: "Un dia cotidiano en una cafeteria"
   - Ejemplo: "Un astronauta explorando un planeta desconocido"
```

---

## Paso 2: Ejecución Automatizada Completa del Pipeline

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Seleccionar modo de ejecucion",
  "questions": [{
    "id": "mode_choice",
    "prompt": "Que modo desea ejecutar?",
    "options": [
      {"id": "cost_optimize", "label": "Modo optimizado en costos (A-roll x4 + B-roll Ken Burns, ~$2.80)"},
      {"id": "full_i2v", "label": "Modo I2V completo (todas las escenas como video, ~$5.60)"},
      {"id": "broll_only", "label": "Solo Ken Burns (para pruebas, $0)"},
      {"id": "explain", "label": "Explicar la diferencia entre A-roll / B-roll"}
    ]
  }]
}
```

**Modo optimizado en costos:**
```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "(escenario especificado por el usuario)" \
  --style anime --engine kling --num-scenes 8 \
  --cost-optimize --aroll-count 4
```

**5 pasos que el pipeline ejecuta automáticamente:**
1. **Descomposición de escenas** (Gemini Flash) -> `scenes.json`
2. **Generación de imagenes de fotogramas** (Gemini Image) -> `frames/frame_000.png` ~ `frame_007.png`
3. **Generación de clips de video** (Kling I2V o Ken Burns) -> `clips/clip_000.mp4` ~
4. **Union con crossfade** (FFmpeg xfade) -> `joined.mp4`
5. **Salida final** -> `final.mp4`

---

## Paso 3: Revisar Imagenes de Fotogramas

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Revisar imagenes de fotogramas",
  "questions": [{
    "id": "step_action",
    "prompt": "Desea revisar las imagenes de fotogramas generadas?",
    "options": [
      {"id": "check", "label": "Revisar imagenes de fotogramas"},
      {"id": "regenerate", "label": "Regenerar fotogramas especificos"},
      {"id": "change_style", "label": "Regenerar con un estilo diferente"},
      {"id": "skip", "label": "Continuar"}
    ]
  }]
}
```

**Estilos disponibles:**
- `anime` - Estilo anime (predeterminado)
- `modern_clean` - Moderno y limpio
- `vibrant_ugc` - Estilo UGC vibrante
- `animal_crossing` - Estilo Animal Crossing
- `watercolor` - Estilo acuarela
- `pixel_art` - Estilo pixel art
- `cinematic_live` - Estilo cinematográfico de acción real

---

## Paso 4: Revisar A-roll / B-roll y Clips de Video

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 4: Revisar clips de video",
  "questions": [{
    "id": "step_action",
    "prompt": "Seleccione como revisar los clips de video",
    "options": [
      {"id": "check_all", "label": "Revisar todos los clips"},
      {"id": "check_aroll", "label": "Revisar solo clips A-roll"},
      {"id": "explain_aroll", "label": "Explicar la mecanica de A-roll / B-roll"},
      {"id": "skip", "label": "Continuar"}
    ]
  }]
}
```

**Explicación de A-roll / B-roll:**
```text
[A-roll (metraje principal)]
- Convertido a video por motor I2V (Image-to-Video)
- Movimiento de personajes, escenas de accion importantes
- Costo: Kling $0.70/clip, Veo $8/clip

[B-roll (metraje complementario)]
- Pseudo-video usando efecto Ken Burns (FFmpeg zoompan)
- Paisajes, fondos, transiciones
- Costo: $0 (procesamiento local)

[Tipos de efectos (Ken Burns)]
zoom_in, zoom_out, pan_left, pan_right, slow_zoom, pan_down, pan_up
```

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
      {"id": "generate", "label": "Generar musica de fondo con Suno AI (cubierto en una leccion posterior)"}
    ]
  }]
}
```

---

## Paso 6: Revisar Video Completado y Resumen de Costos

**Contenido:**
```text
Lea summary.json en output/ugc/storyboard_anime/ y revise los resultados.

Elementos a verificar:
- Ruta del video final
- Numero de escenas (desglose A-roll / B-roll)
- Costo de generacion ($)
- Exito/fallo de cada paso

Consejos de optimizacion de costos:
- Limitar a 4 clips A-roll es 1/4 del costo normal
- Los efectos Ken Burns son $0, asi que el B-roll se puede agregar libremente
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
      {"id": "trouble_2", "label": "Los estilos de las imagenes de fotogramas son inconsistentes"},
      {"id": "trouble_3", "label": "La conversion de video I2V expiro"},
      {"id": "trouble_4", "label": "La union con crossfade fallo"}
    ]
  }]
}
```

### Problema 1: "Error de clave API"
**Causa**: Las variables de entorno no están configuradas
**Solución**:
```bash
cat .env | grep -E "FAL_KEY|GEMINI"
```

### Problema 2: "Los estilos de las imagenes son inconsistentes"
**Causa**: Variación en la generación de imagenes de Gemini
**Solución**: Fije la descripción del personaje con la opción `--character`

### Problema 3: "La conversión de video I2V expiro"
**Causa**: El procesamiento de fal.ai es lento
**Solución**: Reduzca el conteo I2V con `--cost-optimize`, o cambie Kling -> Veo

### Problema 4: "La union con crossfade falló"
**Causa**: Incompatibilidad de formato de video
**Solución**: El pipeline recurre automáticamente a concatenación simple

---

## Punto de Control
- [ ] Las claves API están correctamente configuradas
- [ ] La descomposición de escenas del escenario se completó
- [ ] Las imagenes de fotogramas fueron generadas
- [ ] Comprendio la diferencia A-roll / B-roll
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
      {"id": "next_auto", "label": "Siguiente seccion (/start-15-7 Video musical)"},
      {"id": "retry", "label": "Regenerar con un escenario/estilo diferente"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```
