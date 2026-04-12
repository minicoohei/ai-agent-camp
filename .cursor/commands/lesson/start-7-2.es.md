---
description: "When the user says /start-7-2 — Module 7 Lesson 7-2: Implementación de SKILL.md (Desarrollo del skill de actas de reunion)"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-1"]
duration: "~30 min"
level: "intermediate"
tags: ["agent", "skill-md", "implementation"]
---

# 🎓 Lesson 7-2: Implementación de SKILL.md

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-2: Implementación de SKILL.md**!

| Elemento | Contenido |
|------|------|
| Objetivo | Crear el SKILL.md de meeting-notes-summarizer desde cero y verificar su funcionamiento |
| Duración | ~30 min |
| Habilidades utilizadas | Claude Code Skills, SKILL.md |
| Requisitos previos | Lesson 7-1 completada (especificación de caso de uso disponible) |

**Flujo de la sesion:**
1. Optimizar el frontmatter YAML
2. Crear la estructura de directorios
3. Escribir el cuerpo de SKILL.md
4. Crear la plantilla de salida
5. Verificar el funcionamiento

Al final de está sesion, el SKILL.md de meeting-notes-summarizer estará completó y habrá confirmado que se activa correctamente con las frases de activación.

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
(view_html → Mostrar URL de la página del curso https://ai-agent.camp/es/course/module-7)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Optimizar el frontmatter YAML

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Optimizar el frontmatter YAML",
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
Entrada:
```
Cree el frontmatter YAML para meeting-notes-summarizer.

La description debe incluir tanto "que hace el skill" como "cuando usarlo (frases de activacion)".
Use solo los campos name y description.

Puntos clave:
- name debe ser conciso en kebab-case
- description debe incluir la explicacion funcional del skill + frases de activacion en lenguaje natural
- Encierre las frases de activacion entre comillas, incluyendo multiples patrones
- Condense a aproximadamente 100 palabras

Ejemplo:
---
name: meeting-notes-summarizer
description: Skill que genera automaticamente actas de reunion estructuradas (asistentes, agenda, decisiones, elementos de accion) a partir de texto o notas de reuniones. Usar cuando se solicite "resumir las actas de la reunion", "organizar las notas de la reunion", "extraer elementos de accion" o "compilar las notas de la reunion".
---
```

**Resultado esperado**: Se crea el frontmatter YAML con una description que incluye frases de activación.

---

## 🚀 Step 2: Crear la estructura de directorios

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear la estructura de directorios",
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
Entrada:
```
Cree la estructura de directorios para el skill meeting-notes-summarizer.

Ejecute los siguientes comandos:

mkdir -p skills/meeting-notes-summarizer/scripts
mkdir -p skills/meeting-notes-summarizer/references
touch skills/meeting-notes-summarizer/SKILL.md

Despues de la creacion, verifique la estructura de directorios.

Estructura de directorios esperada:
skills/meeting-notes-summarizer/
├── SKILL.md
├── scripts/
└── references/

Puntos clave:
- scripts/ contiene los scripts Python utilizados por el skill
- references/ contiene plantillas de salida y archivos de ejemplo
- SKILL.md es el punto de entrada del skill
```

**Resultado esperado**: Se crea la estructura de directorios del skill meeting-notes-summarizer.

---

## 🚀 Step 3: Escribir el cuerpo de SKILL.md

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Escribir el cuerpo de SKILL.md",
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
Entrada:
```
Escriba el cuerpo de skills/meeting-notes-summarizer/SKILL.md con la siguiente estructura.

Estructura de SKILL.md:

1. Frontmatter YAML (creado en Step 1)
2. Nombre y titulo del skill
3. Seccion "Cuando usar"
4. Seccion "Flujo de trabajo"
5. Seccion "Especificacion del formato de salida"
6. Seccion "Casos limite"

---
name: meeting-notes-summarizer
description: Skill que genera automaticamente actas de reunion estructuradas (asistentes, agenda, decisiones, elementos de accion) a partir de texto o notas de reuniones. Usar cuando se solicite "resumir las actas de la reunion", "organizar las notas de la reunion", "extraer elementos de accion" o "compilar las notas de la reunion".
---

# meeting-notes-summarizer - Generador automatico de actas de reunion

## Cuando usar

Use este skill al recibir solicitudes como:

- Crear actas a partir de texto o notas de reuniones
- Extraer elementos de accion o decisiones
- Estructurar y organizar notas de reuniones
- Formatear notas de reuniones

Frases de activacion de ejemplo:
- "Resume las actas de la reunion"
- "Organiza las notas de la reunion"
- "Extrae los elementos de accion"
- "Compila las notas de la reunion"
- "Organiza los puntos clave de esta reunion"
- "Lista las decisiones"

## Flujo de trabajo

Este skill procesa en los siguientes pasos:

### Step 1: Recibir texto de entrada
- Recibir texto de reunion, notas, transcripciones de audio, etc. del usuario
- Determinar el formato del texto (puntos, formato libre, registro de chat, etc.)

### Step 2: Extraer asistentes
- Identificar nombres de asistentes/oradores del texto
- Estandarizar variaciones de nombre (nombre completo, apodo, con/sin titulo)
- Si no se especifican asistentes, indicar "Asistentes desconocidos"

### Step 3: Identificar puntos de agenda
- Identificar los temas principales de la reunion en orden cronologico
- Resumir la discusion de cada tema
- Organizar las relaciones entre temas

### Step 4: Extraer decisiones
- Extraer decisiones usando palabras clave como "decidido", "acordado", "aprobado", etc.
- Anotar brevemente el contexto/razonamiento de cada decision
- Si no se tomaron decisiones, indicar explicitamente "Sin decisiones"

### Step 5: Extraer elementos de accion
- Extraer elementos de accion usando palabras clave como "hare", "me encargo", "verificar", "para la proxima reunion", etc.
- Asociar cada elemento de accion con un responsable y fecha limite
- Si el responsable es desconocido, indicar "Por confirmar"
- Si la fecha limite es desconocida, indicar "Fecha limite pendiente"

### Step 6: Formatear salida
- Formatear la salida segun la plantilla de references/output-template.md
- Generar actas de reunion estructuradas en formato Markdown
- Guardar la salida en el directorio output/

## Formato de salida

La salida sigue la plantilla definida en references/output-template.md.
Secciones principales:
- Informacion basica (fecha/hora, asistentes, ubicacion/metodo)
- Lista de agenda
- Decisiones
- Elementos de accion (formato de tabla con responsable, tarea, fecha limite)
- Proxima reunion

## Casos limite

### Sin elementos de accion
- Indicar "No hay elementos de accion para esta reunion" en la seccion "Elementos de accion"
- Algunas reuniones solo tienen decisiones, asi que esto no es un error

### Asistentes desconocidos
- Si se puede inferir del contenido, anotar con "(estimado)"
- Si es completamente desconocido, indicar "Asistentes: Desconocidos (no especificados en el texto)"

### Idiomas mixtos
- Producir salida en el idioma principal del texto de entrada
- Preservar nombres propios y terminos tecnicos en su idioma original
- Si se mezclan japones e ingles, priorizar el japones

### Texto de entrada demasiado corto
- Crear actas con informacion minima (solo agenda y decisiones)
- Indicar explicitamente "No especificado" para informacion faltante

### Formato de registro de chat
- Analizar marcas de tiempo y oradores
- Filtrar conversaciones casuales y ruido, extrayendo la esencia de la discusion
- Para formatos con hilos, clasificar temas por hilo

Mantenga dentro de 500 lineas y 5,000 palabras.
```

**Resultado esperado**: El SKILL.md se completa con los pasos del flujo de trabajo, especificación de salida y manejo de casos limite.

---

## 🚀 Step 4: Crear la plantilla de salida

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Crear la plantilla de salida",
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
Entrada:
```
Cree skills/meeting-notes-summarizer/references/output-template.md.

Escriba el siguiente formato estandar de actas de reunion como plantilla:

# Actas de reunion: {Nombre de la reunion}

## Informacion basica
- **Fecha/Hora**: {Fecha/Hora}
- **Asistentes**: {Lista de asistentes}
- **Ubicacion/Metodo**: {Ubicacion u Online}
- **Registrador**: {Nombre del registrador o Generado automaticamente por IA}

## Agenda

### 1. {Punto de agenda 1}
{Resumen de la discusion del punto de agenda 1}

### 2. {Punto de agenda 2}
{Resumen de la discusion del punto de agenda 2}

## Decisiones
- {Decision 1}
  - Contexto: {Razonamiento detras de la decision}
- {Decision 2}
  - Contexto: {Razonamiento detras de la decision}

## Elementos de accion

| Responsable | Tarea | Fecha limite | Prioridad |
|-------------|-------|--------------|-----------|
| {Nombre} | {Descripcion de la tarea} | {Fecha limite} | {Alta/Media/Baja} |
| {Nombre} | {Descripcion de la tarea} | {Fecha limite} | {Alta/Media/Baja} |

## Notas de discusion
{Discusion detallada e informacion complementaria}

## Proxima reunion
- **Proxima fecha/hora**: {Fecha/hora de la proxima reunion}
- **Agenda prevista**: {Agenda prevista para la proxima reunion}
- **Preparacion**: {Lo que debe prepararse antes de la proxima reunion}

---

Esta plantilla es referenciada desde SKILL.md.
Los marcadores de posicion (encerrados en {}) seran reemplazados con el contenido real de la reunion.
```

**Resultado esperado**: La plantilla estandar de actas de reunion se crea en references/output-template.md.

---

## 🚀 Step 5: Verificar el funcionamiento

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificar el funcionamiento",
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
Entrada:
```
Verifique el skill meeting-notes-summarizer.

Verificacion 1: Verificacion de la estructura de directorios
Ejecute los siguientes comandos para verificar que la estructura es correcta:
ls -la skills/meeting-notes-summarizer/
ls -la skills/meeting-notes-summarizer/scripts/
ls -la skills/meeting-notes-summarizer/references/

Verificacion 2: Verificacion del contenido de SKILL.md
Verifique el inicio de SKILL.md para confirmar que el frontmatter YAML está correctamente escrito:
head -5 skills/meeting-notes-summarizer/SKILL.md

Verificacion 3: Prueba de frases de activacion
Pruebe si el skill se activa correctamente con el siguiente memo de reunion de ejemplo:

---Memo de reunion de ejemplo---
15 de enero de 2024 14:00-15:00 Reunion regular
Asistentes: Tanaka, Sato, Suzuki

Tanaka: Informo sobre el progreso del nuevo proyecto. La Fase 1 está completa y estamos en transicion a la Fase 2.
Sato: Cuando se completara la revision de diseno?
Tanaka: Deberia estar lista para este viernes.
Suzuki: Comenzare a construir el entorno de pruebas el proximo lunes.
Sato: Aprobado. Procedamos con el presupuesto segun la estimacion original.

Decisiones:
- Completar la revision de diseno de la Fase 2 para este viernes
- El presupuesto procede segun la estimacion original

Proxima reunion: 22 de enero a las 14:00
---Fin del ejemplo---

De la instruccion "Resume este memo de reunion en actas de reunion" y verifique que se generan actas de reunion estructuradas siguiendo la plantilla de salida.

Verificacion 4: Verificacion de la salida
Verifique que las actas generadas incluyen:
- Informacion basica (fecha/hora, asistentes, ubicacion) correctamente extraida
- Puntos de agenda identificados
- Decisiones correctamente listadas
- Elementos de accion vinculados a responsables y fechas limite
- Salida en formato Markdown
```

**Resultado esperado**: El skill se activa correctamente para el memo de reunion de ejemplo y produce actas de reunion estructuradas.

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
      {"id": "trouble_1", "label": "SKILL.md no se activa"},
      {"id": "trouble_2", "label": "El formato de salida es inconsistente"},
      {"id": "trouble_3", "label": "El directorio no se reconoce"},
      {"id": "trouble_4", "label": "La description es demasiado larga (error)"}
    ]
  }]
}
```

### Problema 1: SKILL.md no se activa
**Causa**: Faltan frases de activación en la description
**Prompt de solución**:
```
Verifique la description en el frontmatter YAML de SKILL.md.

Verifique lo siguiente:
1. La description incluye frases de activacion?
   ej: "resumir las actas de la reunion", "organizar las notas de la reunion"
2. El campo name esta en kebab-case correcto?
3. Hay errores de sintaxis YAML (indentacion, comillas)?

Ejemplo de correccion:
description: Skill que genera automaticamente actas de reunion estructuradas (asistentes, agenda, decisiones, elementos de accion) a partir de texto o notas de reuniones. Usar cuando se solicite "resumir las actas", "organizar las notas" o "extraer elementos de accion".
```

### Problema 2: El formato de salida es inconsistente
**Causa**: Falta referencia a la plantilla de salida
**Prompt de solución**:
```
Verifique la seccion "Formato de salida" de SKILL.md.

Verifique lo siguiente:
1. Existe references/output-template.md?
2. La ruta de referencia al archivo de plantilla es correcta en SKILL.md?
3. Los marcadores de posicion de la plantilla son consistentes?

Verificar el archivo de plantilla:
cat skills/meeting-notes-summarizer/references/output-template.md
```

### Problema 3: El directorio no se reconoce
**Causa**: No está colocado correctamente bajo skills/
**Prompt de solución**:
```
Verifique la ubicacion del directorio.

Ubicacion correcta:
skills/meeting-notes-summarizer/SKILL.md

Verifique con el siguiente comando:
ls -la skills/meeting-notes-summarizer/

Errores comunes:
- .claude/skill/ (usando "skill" en lugar de "skills")
- skills/meeting-notes-summarizer/ (ruta correcta, con guiones)
- SKILL.md colocado en un directorio diferente
```

### Problema 4: La description es demasiado larga (error)
**Causa**: La description se ha vuelto demasiado extensa
**Prompt de solución**:
```
Condense la description a aproximadamente 100 palabras.

Puntos clave:
1. Explique la funcion del skill en una oracion
2. Limite las frases de activacion a 3-4 representativas
3. Mueva las explicaciones detalladas al cuerpo de SKILL.md

Antes de condensar (mal ejemplo):
description: Este skill toma datos de texto de reuniones, notas, texto de transcripcion de audio, etc. como entrada, realiza identificacion de asistentes, organizacion de agenda, extraccion de decisiones, enumeracion de elementos de accion, y produce como salida actas altamente estructuradas en formato Markdown a traves de procesamiento avanzado de texto.

Despues de condensar (buen ejemplo):
description: Skill que genera automaticamente actas de reunion estructuradas (asistentes, agenda, decisiones, elementos de accion) a partir de texto o notas de reuniones. Usar cuando se solicite "resumir las actas", "organizar las notas" o "extraer elementos de accion".
```

---

## ✅ Punto de control
- [ ] El frontmatter YAML (name + description) está optimizado
- [ ] La estructura de directorios está correctamente creada
- [ ] El cuerpo de SKILL.md contiene los pasos del flujo de trabajo
- [ ] La plantilla de salida está ubicada en references/
- [ ] Confirmo la activación correcta con frases de activación
- [ ] Confirmo que la salida está en formato Markdown estructurado


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-7-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-7-3
- finish → Finalizar
