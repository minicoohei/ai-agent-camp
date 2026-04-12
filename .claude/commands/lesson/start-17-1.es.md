---
description: "When the user says /start-17-1 — Module 17 Lesson 17-1: Publicación en X y creación de banners"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~30 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "x-post", "banner", "sns"]
---

# Lección 17-1: Publicación en X y Creación de Banners

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 17-1: Publicación en X y Creación de Banners**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear texto de publicación en X y un banner usando las habilidades social-content + banner-creator |
| Duración | ~30 min |
| Habilidades utilizadas | social-content, banner-creator (Gemini Image Generation API) |
| Requisitos previos | Clave API de Gemini configurada |
| Página del curso | Consulte [Module 17: Marketing](https://ai-agent.camp/es/course/module-17) en paralelo |

**Flujo de la sesión:**
1. Comprender las mejores prácticas de publicación en X (horarios, hashtags, límites de caracteres)
2. Crear 3 patrones de texto de publicación en X con la habilidad social-content
3. Crear un banner para publicación en X con banner-creator (1200x675px)

Al finalizar esta sesión, estaran completos 3 patrones de texto y 1 imagen de banner.

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
      {"id": "view_html", "label": "Quiero ver la pagina del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra leccion"}
    ]
  }]
}
```

---

## Paso 1: Comprender las Mejores Prácticas de Publicación en X

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Mejores practicas de publicacion en X",
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
```
Explique las mejores practicas para publicaciones en X (Twitter).
Cubra los siguientes puntos:
- Horarios optimos de publicacion
- Uso efectivo de hashtags (cantidad, seleccion)
- Limites de caracteres (140 vs 280 caracteres) y longitud ideal
- Tecnicas para aumentar el engagement
```

**Resultado esperado**: Se explican los horarios optimos, estrategias de hashtags y mejores prácticas de caracteres para publicaciones en X.

---

## Paso 2: Crear 3 Patrones de Texto con social-content

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Crear 3 patrones de texto para X",
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
```
Use la habilidad social-content para crear 3 patrones de texto de publicacion en X:
Tema: "Cursor Bootcamp - Capacitacion en Agentes de IA"
Objetivo: Profesionales de negocios, no ingenieros
Tono: Amigable y atractivo

Patron 1: Tipo pregunta ("Sigue haciendo...?")
Patron 2: Tipo resultados/numeros ("X% de mejora en eficiencia")
Patron 3: Tipo historia (estilo testimonial)

Incluya hashtags para cada patron.
```

**Resultado esperado**: Se generan 3 patrones de texto, cada uno con un enfoque diferente.

---

## Paso 3: Crear un Banner con banner-creator

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Crear un banner para X",
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
```
Use banner-creator para crear un banner para publicaciones en X.
Tema: "Cursor Bootcamp - Multiplique su productividad por 10 con IA"
Plataforma: x_post (1200x675px)
Estilo: Moderno, tecnologico, orientado a negocios
Salida: ~/ai-agent-camp/outputs/marketing-12-1-banner.png
```

**Resultado esperado**: Se genera una imagen de banner de 1200x675px en la carpeta outputs.

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
      {"id": "trouble_1", "label": "Ocurre un error de API"},
      {"id": "trouble_2", "label": "El texto es demasiado largo"},
      {"id": "trouble_3", "label": "El tamano del banner es incorrecto"},
      {"id": "trouble_4", "label": "La imagen no se genera"}
    ]
  }]
}
```

### Problema 1: "Ocurre un error de API"
**Causa**: La clave API de Gemini no está configurada o esta limitada por tasa
**Solución**: Verifique la variable de entorno GEMINI_API_KEY. Si hay límite de tasa, espere 30 segundos y reintente.

### Problema 2: "El texto es demasiado largo"
**Causa**: Supera el límite de 280 caracteres de X
**Solución**: Acorte el texto a 280 caracteres. Los hashtags cuentan como caracteres.

### Problema 3: "El tamaño del banner es incorrecto"
**Causa**: Especificación de plataforma incorrecta
**Solución**: Especifique --platform como "x_post" en banner-creator para generar automáticamente a 1200x675px (16:9).

### Problema 4: "La imagen no se genera"
**Causa**: El directorio outputs no existe o problema de permisos
**Solución**: `mkdir -p ~/ai-agent-camp/outputs`

---

## Punto de Control
- [ ] Comprendio las mejores prácticas de X (horarios, hashtags, caracteres)
- [ ] Creó 3 patrones de texto con la habilidad social-content
- [ ] Género 1 banner para X (1200x675px) con banner-creator
- [ ] El archivo de imagen esta guardado en la carpeta outputs

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
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-17-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```
