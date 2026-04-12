---
description: "When the user says /start-7-4 — Module 7 Lesson 7-4: 5 patrones de diseño (Diseño avanzado de skills)"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-3"]
duration: "~20 min"
level: "advanced"
tags: ["agent", "design-patterns", "architecture"]
---

# 🎓 Lesson 7-4: 5 patrones de diseño

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-4: 5 patrones de diseño**!

| Elemento | Contenido |
|------|------|
| Objetivo | Aprender 5 patrones de diseño de skills y aplicar el patrón Iterative Refinement al skill de actas de reunion |
| Duración | ~20 min |
| Habilidades utilizadas | meeting-notes-summarizer (creado y mejorado en Lessons 7-2, 7-3) |
| Requisitos previos | Lesson 7-3 completada (skill probado y mejorado) |
| Página del curso | Consulte [Module 7: Skill/Commands](https://ai-agent.camp/es/course/module-7) junto con está lección |

**Flujo de la sesion:**
1. Patrón Sequential Workflow
2. Patrón Multi-MCP Coordination
3. Patrón Iterative Refinement
4. Patrón Context-aware Tool Selection
5. Patrón Domain-specific Intelligence
6. Aplicar Iterative Refinement al skill de actas de reunion (ejercicio práctico)

Al final de está sesion, comprenderá los 5 patrones de diseño y habrá aplicado el patrón Iterative Refinement al skill de actas de reunion.

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
(check_prereq → Ejecutar verificación de requisitos previos: Confirmar que Lesson 7-3 está completada y que meeting-notes-summarizer existe en `skills/meeting-notes-summarizer/`)
(view_html → Mostrar URL de la página del curso https://ai-agent.camp/es/course/module-7)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Patrón Sequential Workflow

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Patron Sequential Workflow",
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

**Concepto**: Un patrón que ejecuta tareas en un orden definido, dónde la salida de cada paso se convierte en la entrada del siguiente. Cómo el procesamiento es lineal y predecible, es facil de depurar y cada paso puede probarse independientemente.

**Aplicación en el skill de actas de reunion:**
Recibir texto → Extraer asistentes → Identificar agenda → Organizar decisiones → Extraer elementos de accion → Salida Markdown

Entrada:
```
Disene el flujo de procesamiento al aplicar el patron Sequential Workflow al skill de actas de reunion.

Defina claramente la entrada/salida de cada paso, mostrando como la salida del paso anterior se convierte en la entrada del siguiente:
1. Recibir y preprocesar texto
2. Extraer asistentes
3. Identificar agenda/temas
4. Organizar decisiones
5. Extraer elementos de accion (con responsables y fechas limite)
6. Generar actas de reunion en Markdown
```

**Resultado esperado**: Se disena un flujo de procesamiento de 6 pasos con entrada/salida claramente definida para cada paso.

---

## 🚀 Step 2: Patrón Multi-MCP Coordination

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Patron Multi-MCP Coordination",
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

**Concepto**: Un patrón que coordina múltiples herramientas y skills para lograr tareas complejas que no se pueden realizar con una sola herramienta. Es importante aprovechar las fortalezas de cada herramienta y disenar el paso de datos y el manejo de errores.

**Aplicación en el skill de actas de reunion:**
Obtener registros de reunion de un canal via Slack search → Estructurar con el skill de actas → Guardar en Notion DB

Entrada:
```
Disene una integracion de los siguientes 3 skills usando el patron Multi-MCP Coordination:

1. slack-search (Busqueda en Slack) → Obtener registros de reunion de un canal especifico
2. meeting-notes-summarizer (Generador de actas) → Convertir registros en actas estructuradas
3. notion-db (Integracion con Notion) → Guardar actas en una base de datos de Notion

Disene el metodo de paso de datos entre skills y el manejo de fallback ante errores.
```

**Resultado esperado**: Se disena el flujo de integración de 3 skills, con formatos de datos claros, metodos de paso y lógica de fallback ante errores.

---

## 🚀 Step 3: Patrón Iterative Refinement

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Patron Iterative Refinement",
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

**Concepto**: Un patrón que mejora la calidad a través de un ciclo de generación de borrador → revisión → mejora → re-revisión. En lugar de buscar la perfeccion en una sola generación, adopta un enfoque iterativo para mejorar la calidad.

**Aplicación en el skill de actas de reunion:**
Generación del borrador inicial → Auto-revisión (verificación de brechas) → Generación de version mejorada → Confirmacion final

Entrada:
```
Disene como incorporar el patron Iterative Refinement en el skill de actas de reunion:

1. Borrador inicial: Generar actas a partir del texto de entrada
2. Auto-revision: Auto-verificacion desde estas perspectivas
   - Estan incluidos todos los asistentes?
   - Los elementos de accion tienen responsables y fechas limite?
   - Las decisiones son claras?
3. Version mejorada: Revisar las actas basandose en los resultados de la revision
4. Confirmacion final: Mostrar el diff entre antes y despues de la mejora

Muestre la estructura especifica de prompts para describir este mecanismo en SKILL.md.
```

**Resultado esperado**: Se disenan los 4 pasos de Iterative Refinement con notacion clara para SKILL.md y estructura específica de prompts.

---

## 🚀 Step 4: Patrón Context-aware Tool Selection

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Patron Context-aware Tool Selection",
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

**Concepto**: Un patrón que selecciona diferentes rutas de procesamiento según el contexto de la entrada. Determina automáticamente el tipo de entrada y la enruta al handler optimo.

**Aplicación en el skill de actas de reunion:**
Auto-deteccion del formato de entrada → Enrutamiento al handler apropiado

Entrada:
```
Aplique el patron Context-aware Tool Selection al skill de actas de reunion.

Disene la ramificacion segun el formato de entrada:
- Entrada de texto → Convertir directamente a actas
- Texto de transcripcion de audio → Eliminar ruido → Convertir a actas
- Formato de registro de chat → Organizar por orador → Convertir a actas
- Memo con puntos → Estimar estructura → Convertir a actas

Disene los criterios de determinacion para cada rama y las diferencias en el procesamiento.
```

**Resultado esperado**: Se definen criterios de determinacion para 4 formatos de entrada con flujos de preprocesamiento apropiados para cada formato.

---

## 🚀 Step 5: Patrón Domain-specific Intelligence

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Patron Domain-specific Intelligence",
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

**Concepto**: Un patrón que incorpora conocimiento experto específico del dominio en los skills para lograr precision y calidad que la IA generica no puede alcanzar. Incorpora conocimiento del dominio de reuniones (tipos de reunion, plantillas, terminologia) en el skill.

**Aplicación en el skill de actas de reunion:**
Auto-deteccion del tipo de reunion → Selección de plantilla por tipo → Interpretacion de terminologia de la industria → Recomendacion de acciones de seguimiento

Entrada:
```
Disene como incorporar conocimiento experto del dominio de reuniones en el skill de actas de reunion usando el patron Domain-specific Intelligence:

1. Auto-deteccion del tipo de reunion (reunion regular/lluvia de ideas/revision/reunion de toma de decisiones)
2. Seleccion de plantilla de actas apropiada para cada tipo
3. Reglas para interpretar terminologia y abreviaturas de la industria
4. Patrones recomendados de acciones de seguimiento

Muestre la estructura especifica de archivos para ubicar esto en el directorio references/ de SKILL.md.
```

**Resultado esperado**: El conocimiento experto del dominio de reuniones está estructurado y el diseño de ubicacion en el directorio references/ está completó.

---

## 🚀 Step 6: Ejercicio práctico — Aplicar Iterative Refinement

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 6: Ejercicio practico — Aplicar Iterative Refinement",
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

Incorpore el patrón Iterative Refinement diseñado en Step 3 en el SKILL.md real de meeting-notes-summarizer. Este es un ejercicio práctico para traducir el diseño en implementación.

Entrada:
```
Modifique el SKILL.md de meeting-notes-summarizer creado en Lesson 7-2 para incorporar el patron Iterative Refinement.

Cambios especificos:
1. Agregar un paso de "Auto-revision" al flujo de trabajo
2. Agregar un checklist de revision (5+ elementos)
3. Definir las condiciones del ciclo de mejora (cuando dejar de mejorar)
4. Mostrar el diff antes y despues para confirmar los cambios

Despues de la modificacion, verifique el funcionamiento con datos de ejemplo.
```

**Resultado esperado**: El patrón Iterative Refinement se incorpora en el SKILL.md de meeting-notes-summarizer, y se confirma que la auto-revisión y el ciclo de mejora funcionan.

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
      {"id": "trouble_1", "label": "No puedo distinguir los patrones"},
      {"id": "trouble_2", "label": "No se como combinar multiples patrones"},
      {"id": "trouble_3", "label": "El skill se rompio al modificar SKILL.md"},
      {"id": "trouble_4", "label": "Iterative Refinement crea un bucle infinito"}
    ]
  }]
}
```

### Problema 1: No puedo distinguir los patrones
**Causa**: Los 5 patrones parecen conceptualmente similares
**Prompt de solución**:
```
Cree una tabla comparativa resumiendo cada patron en una linea:

| Patron | En pocas palabras | Ejemplo en skill de actas |
|--------|-------------------|--------------------------|
| Sequential Workflow | Procesar en orden | Texto → Extraer → Organizar → Salida |
| Multi-MCP Coordination | Coordinar multiples herramientas | Slack → Actas → Notion |
| Iterative Refinement | Mejorar iterativamente | Borrador → Revision → Correccion |
| Context-aware Tool Selection | Ramificar segun la entrada | Deteccion de formato → Procesamiento apropiado |
| Domain-specific Intelligence | Incorporar conocimiento del dominio | Plantillas por tipo de reunion |
```

### Problema 2: No se cómo combinar múltiples patrones
**Causa**: No está claro cómo combinar patrones
**Prompt de solución**:
```
Muestre un ejemplo combinando Sequential Workflow + Iterative Refinement.

Ejemplo: Aplicar Iterative Refinement dentro de cada paso del Sequential Workflow
1. Recibir y preprocesar texto
2. Extraer asistentes → Auto-revision → Mejorar
3. Identificar agenda → Auto-revision → Mejorar
4. Organizar decisiones → Auto-revision → Mejorar
5. Extraer elementos de accion → Auto-revision → Mejorar
6. Salida Markdown

Explique los puntos de mejora en cada paso en detalle.
```

### Problema 3: El skill se rompio al modificar SKILL.md
**Causa**: Error de sintaxis o secciones requeridas faltantes en SKILL.md
**Prompt de solución**:
```
Siga estos pasos para recuperar:
1. Verifique los cambios con git diff
   git diff skills/meeting-notes-summarizer/SKILL.md
2. Si hay problemas, revierta los cambios
   cp skills/meeting-notes-summarizer/SKILL.md.backup skills/meeting-notes-summarizer/SKILL.md
3. Vuelva a aplicar las modificaciones cuidadosamente
```

### Problema 4: Iterative Refinement crea un bucle infinito
**Causa**: No se definio condicion de terminación para el ciclo de mejora
**Prompt de solución**:
```
Limite el ciclo de mejora a un maximo de 2 iteraciones. Agregue lo siguiente a SKILL.md:

## Limites del ciclo de mejora
- Maximo de iteraciones de mejora: 2
- Condiciones de terminacion: Cuando se cumpla alguna de las siguientes
  1. Todos los elementos del checklist de revision estan OK
  2. El conteo de mejoras llega a 2
  3. No hay cambios respecto a la mejora anterior
- Si quedan problemas despues de 2 mejoras, agregarlos como lista de problemas pendientes en la salida
```

---

## ✅ Punto de control
- [ ] Comprendio el flujo de procesamiento del patrón Sequential Workflow
- [ ] Diseño la integración Multi-MCP Coordination
- [ ] Comprendio el ciclo de revisión/mejora de Iterative Refinement
- [ ] Diseño la ramificacion de Context-aware Tool Selection
- [ ] Comprendio la incorporacion de conocimiento experto de Domain-specific Intelligence
- [ ] Aplico el patrón Iterative Refinement al skill de actas de reunion
- [ ] Confirmo que el skill modificado funciona correctamente


---

## 📋 Vista previa de entregables

### Salida esperada
```
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

```
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Determinacion de aprobado/no aprobado con los elementos faltantes listados.

---

## ➡️ Siguientes pasos

Esta es la última lección de la serie de Dominio de Skills. Felicitaciones!

Use AskQuestion para elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "back_to_module", "label": "Volver a otras lecciones del Module 7"},
      {"id": "course_top", "label": "Volver al inicio (abrir pagina principal del curso)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- back_to_module → Mostrar lista de lecciones del Module 7 (/start-7-1 a /start-7-8)
- course_top → Abrir https://ai-agent.camp/es/course en el navegador
- finish → Finalizar
