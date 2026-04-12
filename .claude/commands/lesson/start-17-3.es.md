---
description: "When the user says /start-17-3 — Module 17 Lesson 17-3: Redaccion publicitaria (Copywriting)"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~35 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "copywriting", "lp", "ab-test"]
---

# Lección 17-3: Redaccion Publicitaria (Copywriting)

## Lo Qué Hará en Esta Sesion

Bienvenido a **Lección 17-3: Redaccion Publicitaria**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear textos de Landing Page / página de funciones con la habilidad copywriting y generar variaciones para pruebas A/B |
| Duración | ~35 min |
| Habilidades utilizadas | copywriting, ab-test-setup |
| Requisitos previos | Clave API de Gemini configurada |
| Página del curso | Consulte [Module 17: Marketing](https://ai-agent.camp/es/course/module-17) en paralelo |

**Flujo de la sesion:**
1. Comprender la estructura efectiva de textos de Landing Page (hero, problema, solución, CTA)
2. Crear textos para una Landing Page de "Cursor Bootcamp"
3. Generar variaciones para pruebas A/B

Al finalizar está sesion, estarán completos 1 conjunto de textos de Landing Page y 2 patrones de variaciones.

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Verificación de Preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Está listo?",
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

## Paso 1: Comprender la Estructura de Textos de Landing Page

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Estructura de textos de Landing Page",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
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
Explique la estructura de textos para una Landing Page efectiva.
Para cada seccion, explique su funcion y consejos de escritura:
1. Seccion hero (titular + subtitular)
2. Planteamiento del problema (articular los puntos de dolor del usuario)
3. Solucion (propuesta de valor del producto)
4. Prueba social (resultados, testimonios)
5. Caracteristicas/beneficios (3-5 elementos)
6. CTA (llamada a la accion)
7. FAQ (preguntas frecuentes)
```

---

## Paso 2: Crear Textos de Landing Page para "Cursor Bootcamp"

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Crear textos de Landing Page",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
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
Use la habilidad copywriting para crear textos de Landing Page para "Cursor Bootcamp".

Informacion del producto:
- Nombre: Cursor Bootcamp
- Resumen: Capacitacion en agentes de IA (Claude Code / Cursor) para no ingenieros
- Objetivo: Profesionales de negocios, participantes de capacitacion corporativa
- Valor: Mejora dramatica de la eficiencia laboral con IA, sin programacion
- Trayectoria: 11 modulos, 85+ comandos, 21 habilidades incluidas
- Precio: Bajo consulta

Cree textos para las siguientes secciones:
1. Seccion hero (titular + subtitular)
2. Planteamiento del problema
3. Solucion
4. Caracteristicas (3 elementos)
5. CTA

Guarde los resultados en output/lp-copy-v1.md.
```

---

## Paso 3: Generar Variaciones para Pruebas A/B

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Generar variaciones para pruebas A/B",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
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
Basandose en los textos creados (output/lp-copy-v1.md),
cree 2 patrones de variaciones para pruebas A/B.

Variacion A (output/lp-copy-v2a.md):
- Cambiar el hero a tipo "apelacion al miedo" (Sigue haciendo trabajo manual?)
- Cambiar CTA a "Pruebelo ahora"

Variacion B (output/lp-copy-v2b.md):
- Cambiar el hero a tipo "apelacion a resultados" (El 95% de los participantes mejoro su eficiencia)
- Cambiar CTA a "Consulta gratuita"

Incluya la intencion de cada patron y las metricas para medir la efectividad.
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
      {"id": "trouble_1", "label": "Los textos son demasiado largos o redundantes"},
      {"id": "trouble_2", "label": "El tono no coincide con el objetivo"},
      {"id": "trouble_3", "label": "Las variaciones son demasiado similares"},
      {"id": "trouble_4", "label": "El archivo no se guarda"}
    ]
  }]
}
```

### Problema 1: "Textos demasiado largos"
**Solución**: Especifique longitudes objetivo por sección y regenere.

### Problema 2: "El tono no coincide"
**Solución**: Especifique el perfil objetivo más concretamente.

### Problema 3: "Las variaciones son muy similares"
**Solución**: Cambie el eje de apelacion (funcional vs emocional vs resultados) para crear diferencias mayores.

### Problema 4: "El archivo no se guarda"
**Solución**: `mkdir -p ~/ai-agent-camp/output`

---

## Punto de Control
- [ ] Comprendio la estructura de textos de Landing Page (hero/problema/solución/características/CTA)
- [ ] Creo 1 conjunto de textos de Landing Page para "Cursor Bootcamp" con la habilidad copywriting
- [ ] Genero 2 patrones de variaciones para pruebas A/B
- [ ] lp-copy-v1.md, lp-copy-v2a.md, lp-copy-v2b.md están guardados en la carpeta output

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-17-4)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```
