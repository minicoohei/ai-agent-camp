---
description: "When the user says /start-17-2 — Module 17 Lesson 17-2: Auditoria SEO y estrategia de palabras clave"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~40 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "seo", "keyword", "audit"]
---

# Lección 17-2: Auditoria SEO y Estrategia de Palabras Clave

## Lo Qué Hará en Esta Sesion

Bienvenido a **Lección 17-2: Auditoria SEO y Estrategia de Palabras Clave**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Realizar una auditoria SEO y desarrollar una estrategia de palabras clave con las habilidades seo-audit + programmatic-seo |
| Duración | ~40 min |
| Habilidades utilizadas | seo-audit, programmatic-seo |
| Requisitos previos | Clave API de Gemini configurada |
| Página del curso | Consulte [Module 17: Marketing](https://ai-agent.camp/es/course/module-17) en paralelo |

**Flujo de la sesion:**
1. Comprender los fundamentos de la auditoria SEO
2. Diagnosticar problemas SEO de un sitio objetivo con la habilidad seo-audit
3. Disenar estrategia de palabras clave y plantillas de paginas con programmatic-seo

Al finalizar está sesion, estarán completos un informe de auditoria SEO y una lista de palabras clave.

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

## Paso 1: Comprender los Fundamentos de la Auditoria SEO

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Fundamentos de la auditoria SEO",
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
Explique los elementos fundamentales a verificar en una auditoria SEO.
Organizelos en las siguientes categorias:
- SEO tecnico (velocidad del sitio, rastreo, indexacion)
- SEO en pagina (titulo, meta descripcion, estructura de encabezados)
- SEO de contenido (densidad de palabras clave, enlaces internos, calidad del contenido)
- SEO fuera de pagina (backlinks, autoridad de dominio)
```

---

## Paso 2: Diagnosticar Problemas SEO con seo-audit

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Diagnosticar problemas SEO con seo-audit",
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
Use la habilidad seo-audit para diagnosticar problemas SEO del siguiente sitio:
URL: https://example.com (su propio sitio o un sitio de practica)

Enfoquese en los siguientes elementos:
- Optimizacion de meta tags (titulo, descripcion)
- Estructura de encabezados (H1-H3)
- Atributos alt de imagenes
- Estructura de enlaces internos
- Compatibilidad movil

Guarde los resultados como informe en output/seo-audit-report.md.
```

---

## Paso 3: Disenar Estrategia de Palabras Clave con programmatic-seo

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Disenar estrategia de palabras clave y plantillas de paginas",
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
Use la habilidad programmatic-seo para disenar una estrategia de palabras clave sobre el tema "Utilizacion de Agentes de IA".

Incluya lo siguiente:
1. Palabras clave principales (5) y palabras clave de cola larga (15)
2. Clasificacion de intencion de busqueda (informacional/comparacion/transaccional)
3. Propuestas de plantillas de pagina para cada palabra clave
4. Estructura de cluster tematico (pagina pilar + articulos satelite)

Guarde los resultados en output/keyword-strategy.md.
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
      {"id": "trouble_1", "label": "Los resultados de la auditoria SEO no se muestran"},
      {"id": "trouble_2", "label": "Error de acceso a la URL"},
      {"id": "trouble_3", "label": "La lista de palabras clave es demasiado pequena"},
      {"id": "trouble_4", "label": "El archivo del informe no se guarda"}
    ]
  }]
}
```

### Problema 1: "Los resultados no se muestran"
**Solución**: Verifique el contenido de la habilidad seo-audit. Lea el archivo de habilidad primero: skills/seo-audit/SKILL.md

### Problema 2: "Error de acceso a la URL"
**Solución**: Verifique que la URL sea accesible. Para practicar, use https://ai-agent.camp/es/course cómo objetivo.

### Problema 3: "Lista de palabras clave pequeña"
**Solución**: Amplice el tema e incluya múltiples conceptos relacionados.

### Problema 4: "El archivo no se guarda"
**Solución**: `mkdir -p ~/ai-agent-camp/output`

---

## Punto de Control
- [ ] Comprendio los fundamentos de la auditoria SEO (técnico/en página/contenido/fuera de página)
- [ ] Diagnóstico problemas SEO con la habilidad seo-audit
- [ ] El informe de auditoria SEO está guardado en la carpeta output
- [ ] La lista de palabras clave (5 principales + 15 de cola larga) está completa
- [ ] La estructura de cluster tematico está diseñada

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-17-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```
