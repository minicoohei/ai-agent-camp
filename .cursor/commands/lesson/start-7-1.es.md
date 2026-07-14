---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-6-2"]
duration: "~20 min"
level: "intermediate"
tags: ["agent", "skill-design", "best-practices"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 7-1: Fundamentos del diseño de skills

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-1: Fundamentos del diseño de skills**!

| Elemento | Contenido |
|------|------|
| Objetivo | Comprender las mejores practicas de diseño de skills de Anthropic y crear una especificación de caso de uso para un skill de actas de reunion |
| Duración | ~20 min |
| Habilidades utilizadas | Ninguna (lección de diseño y conceptos) |
| Requisitos previos | Se recomienda completar Lesson 6-2 (conocimientos básicos de Skills) |
| Página del curso | Consulte [Module 7: Skill/Commands](https://ai-agent.camp/es/course/module-7) junto con está lección |

**Flujo de la sesion:**
1. Comprender las 3 categorias de skills
2. Aprender Progressive Disclosure (revelación gradual de información)
3. Definir el caso de uso del skill de actas de reunion
4. Establecer criterios de exito

Al final de está sesion, habrá completado una especificación de caso de uso para el skill de actas de reunion (meeting-notes-summarizer).

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificación de preparación

Primero verifiquemos que todo esté listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Está listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar ruta de la página del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Comprender las 3 categorias de skills

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Comprender las 3 categorias de skills",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**

La guía de skills de Anthropic define 3 categorias:

1. **Document Creation** — Generación y edición de documentos (ej: actas de reunion, informes, contratos)
2. **Workflow Automation** — Automatización de tareas repetitivas (ej: revisión de código, despliegue, pruebas)
3. **MCP Enhancement** — Extensión de servidores MCP (ej: integración de API, obtencion de datos, integración de servicios externos)

Entrada:
```text
Explique las 3 categorias de skills (Document Creation / Workflow Automation / MCP Enhancement),
incluyendo sus caracteristicas y ejemplos concretos.
A cual categoria pertenece nuestro "skill de actas de reunion"?
```

**Resultado esperado**: Comprension de las 3 categorias y confirmacion de que el skill de actas de reunion pertenece a "Document Creation".

---

## 🚀 Step 2: Aprender Progressive Disclosure

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Aprender Progressive Disclosure",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**

Los skills revelan información en 3 etapas:

1. **Metadatos** (name + description) — Siempre en contexto (~100 palabras)
2. **Cuerpo de SKILL.md** — Se carga al activarse (recomendado menos de 5,000 palabras)
3. **Recursos incluidos** (scripts/, references/) — Se cargan solo cuando es necesario

Entrada:
```text
Explique las 3 etapas de Progressive Disclosure usando el skill de actas de reunion como ejemplo:

- Etapa 1 (Metadatos): Que name y description configurar
- Etapa 2 (Cuerpo de SKILL.md): Que procedimientos y directrices describir
- Etapa 3 (Recursos incluidos): Que colocar en scripts/ y references/

Disene cada etapa de forma concisa, teniendo en cuenta el costo de tokens.
```

**Resultado esperado**: Diseño concreto del contenido para las 3 etapas y comprension de su impacto en la ventana de contexto.

---

## 🚀 Step 3: Definir el caso de uso del skill de actas de reunion

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Definir el caso de uso del skill de actas de reunion",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**

La especificación del caso de uso debe incluir:
- Nombre del skill y categoria
- Frases de activación (cuando debe activarse)
- Entrada y salida
- Diferenciacion de skills existentes

Entrada:
```text
Cree una especificacion de caso de uso para el skill "meeting-notes-summarizer".

Incluya los siguientes elementos:

## Especificacion de caso de uso

| Elemento | Contenido |
|------|------|
| Nombre del skill | meeting-notes-summarizer |
| Categoria | Document Creation |
| Proposito | Generar automaticamente actas de reunion estructuradas a partir de texto/notas de reuniones |

### Frases de activacion (cuando activar)
- Frases que deben activar: 5 o mas
- Frases que NO deben activar: 3 o mas

### Especificacion de entrada
- Formato de entrada (texto, archivo, etc.)
- Informacion obligatoria y opcional

### Especificacion de salida
- Formato de salida (Markdown)
- Secciones obligatorias (Asistentes, Agenda, Decisiones, Elementos de accion, Proxima reunion)

### Diferenciacion de skills existentes
- Diferencias con check-inbox, slack-search y document-processor
```

**Resultado esperado**: Especificación de caso de uso completada con una vision general clara del skill.

---

## 🚀 Step 4: Establecer criterios de exito

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Establecer criterios de exito",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**

Establezca criterios de exito desde perspectivas cuantitativas y cualitativas.

Entrada:
```text
Defina criterios de exito para el skill meeting-notes-summarizer.

### Metricas cuantitativas
- Precision de activacion (tasa de activacion correcta / tasa de evitar falsos positivos)
- Completitud de salida (tasa de cobertura de secciones obligatorias)
- Velocidad de procesamiento (tiempo de respuesta)

### Metricas cualitativas
- Legibilidad de la salida
- Especificidad de los elementos de accion
- Identificacion precisa de asistentes

### Casos de prueba
- Prueba minima: Notas de una reunion corta (5 min) con 3 personas
- Prueba estandar: Actas de una reunion regular (60 min) con 10 personas
- Prueba maxima: Notas de un taller largo con mezcla de ingles y japones
```

**Resultado esperado**: Criterios de exito cuantitativos y cualitativos y casos de prueba definidos.

---

## ⚠️ Problemas comunes y soluciones

Use AskQuestion para seleccionar el problema y siga la guía.

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No entiendo la clasificacion de categorias"},
      {"id": "trouble_2", "label": "No se me ocurren frases de activacion"},
      {"id": "trouble_3", "label": "La diferencia con skills existentes no esta clara"},
      {"id": "trouble_4", "label": "Los criterios de exito son demasiado abstractos"}
    ]
  }]
}
```

### Problema 1: No entiendo la clasificación de categorias
**Causa**: El skill abarca múltiples categorias
**Prompt de solución**:
```text
Cual es el proposito principal de este skill? Elija una categoria basada en la funcion mas importante.
Si hay elementos de multiples categorias, elija una categoria principal y anote las demas como subcategorias.
```

### Problema 2: No se me ocurren frases de activación
**Causa**: Los escenarios de uso del usuario no están claros
**Prompt de solución**:
```text
Imagine 5 escenarios donde querria usar este skill.
Lo primero que el usuario diria a la IA en cada escenario es una frase de activacion.
```

### Problema 3: La diferencia con skills existentes no está clara
**Causa**: El alcance de la superposicion de funciones es ambiguo
**Prompt de solución**:
```text
Lea el SKILL.md de los skills existentes (check-inbox, slack-search, document-processor)
y compare su "Proposito" y "Formato de salida".
```

### Problema 4: Los criterios de exito son demasiado abstractos
**Causa**: No hay objetivos numericos específicos
**Prompt de solución**:
```text
Si tuviera que calificar unas "buenas actas de reunion" sobre 10 puntos, como asignaria los puntos a cada elemento?
Esa asignacion de puntos se convierte en la prioridad de sus criterios de exito.
```

---

## ✅ Punto de control
- [ ] Comprendio las 3 categorias de skills (Document Creation / Workflow Automation / MCP Enhancement)
- [ ] Comprendio las 3 etapas de Progressive Disclosure
- [ ] Creo la especificación de caso de uso del skill de actas de reunion
- [ ] Definio frases de activación (correctas e incorrectas)
- [ ] Establecio criterios de exito cuantitativos y cualitativos
- [ ] Definio 3 tipos de casos de prueba


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 skills/{skill_name}/
├── SKILL.md  (definicion del skill)
├── scripts/    (scripts de ejecucion)
└── tests/      (archivos de prueba)
```

### Comandos de verificación
```bash
# Verificar la estructura del directorio del skill
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Verificar el inicio de SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat de Cursor para verificar la finalización:

```text
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Determinacion de aprobado/no aprobado con los elementos faltantes listados.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar una nueva sección.

Use AskQuestion para elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-7-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-7-2
- finish → Finalizar
