---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~35 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "slides", "narration", "tts"]
nonInteractiveMode: deferred
---
# Lección 15-8: Video de Narración de Diapositivas

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 15-8: Video de Narración de Diapositivas**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar automáticamente un video donde un presentador narra materiales HTML o imagenes de diapositivas |
| Duración | ~35 min |
| Herramientas utilizadas | slide_narration_pipeline (Gemini + ElevenLabs + Fabric/Kling + FFmpeg) |
| Requisitos previos | FAL_KEY, GEMINI_API_KEY, ELEVEN_API_KEY configurados |
| Guía de costos | Revise la [Guía de Estrategia de Costos de IA de Video](https://ai-agent.camp/es/course/module-15) primero (recomendado) |
| Página del curso | Consulte [Module 15: Generación de Video](https://ai-agent.camp/es/course/module-15) en paralelo |

**Estimación de costos**: 5 segmentos x Fabric 720p aprox. **$12/video**; solo guion **$0.03**

**Flujo de la sesión:**
1. Verificar entorno y preparar materiales
2. Generar y revisar el guion automáticamente
3. Generar video del presentador
4. Componer diapositivas + presentador
5. Agregar música de fondo (opcional)
6. Revisar video completado

Al finalizar esta sesión, un video de narración de diapositivas estará guardado en `output/ugc/slide_narration/`.

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

## Paso 1: Verificar Entorno y Preparar Materiales

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Seleccionar materiales",
  "questions": [{
    "id": "source_choice",
    "prompt": "De que materiales desea crear un video de diapositivas?",
    "options": [
      {"id": "html", "label": "Desde materiales HTML (usar los materiales de este curso)"},
      {"id": "slides", "label": "Desde imagenes de diapositivas (especificar carpeta PNG/JPG)"},
      {"id": "script_only", "label": "Generar solo el guion primero para revisar"}
    ]
  }]
}
```

**Desde materiales HTML:**
```bash
cd ~/ai-agent-camp
python -m ugc.slide_narration_pipeline \
  --html https://ai-agent.camp/es/course/module-1 \
  --engine fabric --resolution 720p
```

**Solo guion:**
```bash
cd ~/ai-agent-camp
python -m ugc.slide_narration_pipeline \
  --html https://ai-agent.camp/es/course/module-1 \
  --script-only
```

---

## Paso 2: Revisar y Ajustar el Guion

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Revision del guion",
  "questions": [{
    "id": "step_action",
    "prompt": "Desea revisar el guion generado?",
    "options": [
      {"id": "check", "label": "Revisar y editar si es necesario"},
      {"id": "change_style", "label": "Regenerar con un estilo diferente"},
      {"id": "skip", "label": "Continuar tal cual"}
    ]
  }]
}
```

**Estilos de guion:**
- `friendly` - Tono conversacional amigable (predeterminado)
- `formal` - Estilo de presentación formal
- `casual` - Estilo de charla casual

---

## Paso 3: Generar Video del Presentador

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Seleccionar motor",
  "questions": [{
    "id": "engine_choice",
    "prompt": "Seleccione el motor de video del presentador",
    "options": [
      {"id": "fabric", "label": "Fabric 1.0 (con sincronizacion labial $2.50/30s)"},
      {"id": "kling", "label": "Kling 2.6 Pro (movimiento natural $2.80/30s)"},
      {"id": "skip_presenter", "label": "Sin presentador (solo diapositivas)"}
    ]
  }]
}
```

---

## Paso 4: Revisar Resultado de Composición

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 4: Resultado de composicion",
  "questions": [{
    "id": "step_action",
    "prompt": "Desea revisar el resultado de la composicion?",
    "options": [
      {"id": "check", "label": "Revisar el video"},
      {"id": "change_position", "label": "Cambiar posicion del presentador"},
      {"id": "skip", "label": "Continuar"}
    ]
  }]
}
```

**Opciones de posición del presentador:**
- `right` - Inferior derecha (predeterminado)
- `left` - Inferior izquierda
- `bottom` - Inferior centro

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
      {"id": "add_bgm", "label": "Agregar musica de fondo (especificar archivo, volumen 12% recomendado)"},
      {"id": "no_bgm", "label": "Completar sin musica de fondo"},
      {"id": "generate", "label": "Aprender generacion de musica de fondo en Leccion 15-7 (Video musical)"}
    ]
  }]
}
```

---

## Paso 6: Revisar Video Completado

**Contenido:**
```text
Revise summary.json en output/ugc/slide_narration/<timestamp>/.

Elementos a verificar:
- Ruta del video final
- Numero de segmentos
- Motor utilizado
- Costo de generacion

Consejos de optimizacion de costos:
- Usar 480p reduce el costo de Fabric a la mitad
- --script-only para revisar el guion primero ($0.03)
- Sin presentador, solo diapositivas Ken Burns + audio TTS ($0.05)
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
      {"id": "trouble_1", "label": "El analisis HTML no puede extraer secciones"},
      {"id": "trouble_2", "label": "El audio TTS suena poco natural"},
      {"id": "trouble_3", "label": "El video del presentador expiro"},
      {"id": "trouble_4", "label": "La composicion de superposicion esta desalineada"}
    ]
  }]
}
```

### Problema 1: "El análisis HTML no puede extraer secciones"
**Solución**: Use la opción --slides para especificar imagenes de diapositivas directamente

### Problema 2: "El audio TTS suena poco natural"
**Solución**: Use --script-only para generar el guion primero -> editar manualmente -> re-ejecutar

### Problema 3: "El video del presentador expiro"
**Solución**: Cambie de motor (fabric -> kling), acorte los segmentos

### Problema 4: "La composición de superposición esta desalineada"
**Solución**: La opción -shortest de FFmpeg se ajusta automáticamente (habilitada por defecto)

---

## Punto de Control
- [ ] Las claves API están correctamente configuradas
- [ ] El análisis HTML o las imagenes de diapositivas están preparados
- [ ] El guion fue generado con lenguaje hablado natural
- [ ] El video del presentador fue generado
- [ ] Las diapositivas y el presentador fueron compuestos
- [ ] El video final fue revisado

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
      {"id": "next_auto", "label": "Siguiente seccion (/start-15-9 Video de demostracion de producto)"},
      {"id": "retry", "label": "Regenerar con materiales diferentes"},
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

