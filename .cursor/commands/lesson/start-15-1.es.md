---
description: "When the user says /start-15-1 — Module 15 Lesson 15-1: Extraer y analizar fotogramas clave de video"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~30 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["video", "keyframe", "analysis", "ffmpeg"]
---

# Lección 15-1: Análisis de Fotogramas de Video

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 15-1: Análisis de Fotogramas de Video**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Extraer fotogramas clave de un video, analizar el contenido y crear un informe resumen |
| Duración | ~30 min |
| Habilidades utilizadas | video-frame-reader (FFmpeg, Gemini Visión API) |
| Requisitos previos | FFmpeg, Python 3.9+, y clave API de Gemini configurada |
| Página del curso | Consulte [Module 15: Generación de Video](https://ai-agent.camp/es/course/module-15) en paralelo |

**Flujo de la sesión:**
1. Verificar el entorno
2. Preparar el video de muestra
3. Extraer y analizar fotogramas clave
4. Crear un informe resumen del video

Al finalizar esta sesión, los fotogramas clave y el resumen estaran guardados en los outputs.

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
      {"id": "view_html", "label": "Quiero ver la pagina del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra leccion"}
    ]
  }]
}
```

(ready -> Ir al Paso 1)
(check_prereq -> Ejecutar verificación de requisitos previos)
(view_html -> Mostrar la ruta de la página del curso)
(different_lesson -> Mostrar lista de modulos)

---

## Paso 0: Preparar un Video de Prueba

Use el video de muestra incluido primero. Solo agregue un video de práctica con FFmpeg si no tiene uno.

```bash
# Crear el directorio data bajo lesson (si es necesario)
mkdir -p courses/aiagent/lesson03-core/module15-video/practice/data/videos

# Generar un video de prueba con FFmpeg (10 segundos, 640x480, 30fps):
ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -pix_fmt yuv420p courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4
```

> **Nota**: Si FFmpeg no está instalado, la verificación del entorno en el Paso 1 le guiará.

---

## Paso 1: Verificar el Entorno

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Verificar el entorno",
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

**Instrucciones (ejemplo)**:
Entrada:
```
Verifique el entorno necesario para la extraccion de fotogramas de video:
- Esta instalado FFmpeg?
- Esta instalado Python 3.9+?
- Esta disponible la habilidad video-frame-reader?

Si falta algo, muestre los pasos de instalacion.
```

**Resultado esperado**: Se verifica el entorno requerido y se muestran los pasos de instalación si falta algo.

---

## Paso 2: Preparar Video de Muestra

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Preparar video de muestra",
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

**Instrucciones (ejemplo)**:
Entrada:
```
Para las pruebas de extraccion de fotogramas, verifique lo siguiente:
1. Existe la carpeta `courses/aiagent/lesson03-core/module15-video/practice/data/videos/`
2. Se puede usar el ejemplo oficial `data/videos/module7-lesson1-frame-lab-sample.mp4` o `courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4`

Si desea probar con otro video, puede colocar un MP4 de 30 segundos o menos en `courses/aiagent/lesson03-core/module15-video/practice/data/videos/`.
```

**Resultado esperado**: Los videos de prueba están listos y las rutas confirmadas.

---

## Paso 3: Extraer Fotogramas Clave

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Extraer fotogramas clave",
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

**Instrucciones (ejemplo)**:
Entrada:
```
Extraiga fotogramas clave de data/videos/module7-lesson1-frame-lab-sample.mp4 o
courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4
(usando extract_keyframes.py de video-frame-reader).

Configuracion:
- Intervalo de extraccion: cada 5 segundos (o valor predeterminado de la habilidad)
- Formato de salida: segun la habilidad (PNG, etc.)
- Ruta de salida: data/frames/ u otra ruta clara

Despues de la extraccion, muestre la lista de imagenes de fotogramas generadas.
```

**Resultado esperado**: Los fotogramas clave se guardan como PNG en el intervalo especificado.

---

## Paso 4: Analizar los Fotogramas Extraidos

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 4: Analizar los fotogramas extraidos",
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

**Instrucciones (ejemplo)**:
Entrada:
```
Analice las imagenes de fotogramas extraidas:

Para cada imagen en data/frames/, proporcione:
- Descripcion del contenido de la escena
- Objetos detectados
- Resultados de OCR si hay texto presente
- Diferencias con el fotograma anterior
```

**Resultado esperado**: Se describe el contenido de cada fotograma.

---

## Paso 5: Crear Informe Resumen del Video

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 5: Crear informe resumen del video",
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

**Instrucciones (ejemplo)**:
Entrada:
```
Basandose en los resultados del analisis de fotogramas, cree un informe resumen del video.

Contenido del informe:
- Resumen del video (1-2 oraciones)
- Lista de escenas principales
- Descripcion del contenido en formato de linea de tiempo
- Puntos destacados

Salida: output/video_summary.md
```

**Resultado esperado**: El contenido del video se resume en formato Markdown.

---

## Paso 6: Detectar Cambios de Escena

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 6: Detectar cambios de escena",
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

**Instrucciones (ejemplo)**:
Entrada:
```
Detecte automaticamente los cambios de escena en el video.

Metodo de deteccion:
- Analizar cambios en la distribucion de colores entre fotogramas
- Registrar puntos con grandes cambios como limites de escena
- Identificar tiempos de inicio y fin de cada escena

Guarde los resultados en formato JSON:
Salida: output/scene_detection.json
```

> **Nota**: La detección de cambios de escena es una extensión futura. Actualmente solo se admite la extracción de fotogramas clave.
> En este paso, puede usar el filtro `select='gt(scene,0.3)'` de FFmpeg o la comparación manual de diferencias entre fotogramas como alternativas.

**Resultado esperado**: Las marcas de tiempo de los cambios de escena se guardan en formato JSON.

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
      {"id": "trouble_1", "label": "FFmpeg no encontrado"},
      {"id": "trouble_2", "label": "No se puede cargar el video"},
      {"id": "trouble_3", "label": "Error de memoria insuficiente"},
      {"id": "trouble_4", "label": "Las imagenes de fotogramas estan todas negras"}
    ]
  }]
}
```

### Problema 1: "FFmpeg no encontrado"
**Causa**: FFmpeg no está instalado
**Solución**:
```
Instale FFmpeg.
macOS: brew install ffmpeg
Windows: winget install ffmpeg o descargue de https://ffmpeg.org/download.html
Despues de la instalacion, verifique con ffmpeg -version.
```

### Problema 2: "No se puede cargar el video"
**Causa**: El formato de video no es compatible o hay un problema de codec
**Solución**:
```
Verifique el formato del archivo de video.
Use ffprobe para obtener informacion del codec, y
muestre como convertir a un formato compatible (MP4/H.264).
```

### Problema 3: "Error de memoria insuficiente"
**Causa**: El video es largo o la resolución es alta
**Solución**:
```
Muestre como resolver el error de memoria insuficiente:
- Aumentar el intervalo de extraccion (por ejemplo, cada 30 segundos)
- Reducir la resolucion del video
- Procesar en lotes usando procesamiento dividido
```

### Problema 4: "Las imagenes de fotogramas están todas negras"
**Causa**: El video comienza con un fundido de entrada o hay un problema de codec
**Solución**:
```
Los fotogramas extraidos son imagenes negras.
- Desplazar la posicion de inicio unos segundos
- Probar un metodo diferente de extraccion de fotogramas
Muestre como solucionarlo.
```

---

## Punto de Control
- [ ] FFmpeg se instaló correctamente
- [ ] Se preparo un video de prueba
- [ ] Se extrajeron los fotogramas clave
- [ ] Las imagenes extraidas se guardaron correctamente
- [ ] Se analizo el contenido de los fotogramas
- [ ] Se creó un informe resumen del video

---

## Vista Previa de Entregables

### Salida esperada
```
output/ugc/
  *.mp4           (archivos de video)
  metadata.json   (metadatos)
  thumbnails/     (miniaturas)
```

### Comandos de verificación
```bash
# Lista y tamano de archivos de salida
ls -lh output/ugc/

# Verificar metadatos
cat output/ugc/*metadata*.json 2>/dev/null | head -20

# Reproducir video (macOS: open / Linux: xdg-open)
open output/ugc/*.mp4
```

---

## Verificación de Finalización
Pegue lo siguiente en el chat de Cursor para verificar la finalización:

```
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de finalización/incompleto y los elementos faltantes.

---

## Siguientes Pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar.

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente accion",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-15-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Guía posterior a la selección (ejemplo)**:
- next_auto -> /next_lesson
- next_window -> Abrir /start-15-2 en una nueva ventana
- finish -> Fin
