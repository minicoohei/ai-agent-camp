---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
duration: "~30 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["agent", "command", "cursor"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 6-1: Fundamentos de creacion de comandos personalizados

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 6-1: Fundamentos de creacion de comandos personalizados**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear comandos personalizados (.cursor/commands/) en Cursor para reutilizacion del equipo |
| Duracion | ~30 min |
| Skills utilizados | Cursor Commands, Markdown（YAML frontmatter） |
| Requisitos previos | Usando Cursor, ai-agent-camp esta abierto |
| Pagina del curso | [Module 6: Desarrollo de agentes](https://ai-agent.camp/es/course/module-6) en paralelo |

**Flujo de la sesion:**
1. Verificar la estructura del directorio de comandos
2. Crear comandos simples (project-info, env-check, run-tests)
3. Verificar el funcionamiento

Al finalizar esta sesion, podra usar comandos para usted y su equipo.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de iniciar la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo/a?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver primero la página del curso"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Verificar estructura del directorio de comandos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verificar la estructura del directorio de comandos",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```text
Verifique la estructura del directorio de comandos del proyecto ai-agent-camp.

Verifique que existan los siguientes directorios:
- .cursor/commands/
- .cursor/commands/lesson/
- .cursor/commands/utility/

Créelos si no existen.
```

**Resultado esperado**: Se confirma y crea la estructura del directorio de comandos.

---

## 🚀 Step 2: Crear comandos simples

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear comandos simples",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
````text
Cree el archivo .cursor/commands/project-info.md con el siguiente contenido:

---
description: "Mostrar informacion del proyecto"
---

# Informacion del Proyecto

## Descripcion general
Este proyecto es una plataforma base para el desarrollo de agentes de IA.

## Estructura de directorios
```
ai-agent-camp/
├── .claude/         # Configuracion de Claude Code
│   └── skills/      # Skills reutilizables
├── .cursor/         # Configuracion de Cursor IDE
│   └── commands/    # Comandos personalizados
│   └── commands/    # Comandos personalizados para Cursor
├── skills/          # Copia maestra de skills comunes
├── course/          # Materiales del curso HTML
└── tools/           # Scripts de Python
```

## Stack tecnologico
- AI Framework: Claude 3.5 Sonnet
- Protocolo: MCP (Model Context Protocol)
- IDE: Cursor / Claude Code
````

**Resultado esperado**: `/project-info` se crea el comando.

---

## 🚀 Step 3: Comando de verificacion de entorno

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Comando de verificación de entorno",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
````text
Cree el archivo .cursor/commands/env-check.md con el siguiente contenido:

---
description: "Verificar el estado del entorno de desarrollo"
---

# Verificacion del entorno

Un comando para verificar el estado de su entorno de desarrollo.

## Lista de verificacion

Ejecute los siguientes comandos para verificar su entorno:

### 1. Verificar version de Node.js
```bash
node --version
```
Valor esperado: v18.x o superior

### 2. Verificar version de Python
```bash
python3 --version    # En Windows, python --version
```
Valor esperado: Python 3.9 o superior

### 3. Verificar configuracion de Git
```bash
git config user.name
git config user.email
```

### 4. Verificar paquetes npm
```bash
npm list -g --depth=0
```

### 5. Verificar paquetes uv
```bash
uv pip list | head -20
```

## Solucion de problemas
Si encuentra algun problema, verifique su configuracion con `/start-0-1`.
````

**Resultado esperado**: `/env-check` se crea el comando.

---

## 🚀 Step 4: Comando de ejecucion de pruebas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Comando de ejecución de pruebas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
````text
Cree el archivo .cursor/commands/run-tests.md con el siguiente contenido:

---
description: "Ejecutar las pruebas del proyecto"
---

# Ejecucion de pruebas

Un comando para ejecutar las pruebas del proyecto.

## Pruebas de Python

### Ejecutar todas las pruebas
```bash
pytest tests/ -v
```

### Pruebas con cobertura
```bash
pytest tests/ -v --cov=src/ --cov-report=term-missing
```

### Ejecutar archivo de prueba especifico
```bash
pytest tests/test_specific.py -v
```

## Pruebas de JavaScript (Node.js)

### Pruebas npm
```bash
npm test
```

### Archivo de prueba especifico
```bash
npx jest tests/specific.test.js
```

## Interpretacion de resultados

- ✅ PASSED: Prueba exitosa
- ❌ FAILED: Prueba fallida (verifique los detalles del error)
- ⚠️ SKIPPED: Prueba omitida
- 📊 Coverage: Tasa de cobertura (objetivo: 80% o mas)
````

**Resultado esperado**: `/run-tests` se crea el comando.

---

## 🚀 Step 5: Verificar operacion de comandos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificar el funcionamiento del comando",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```text
Verifique la lista y el funcionamiento de los comandos creados:

1. Liste los archivos en el directorio .cursor/commands/
2. Extraiga la descripción de cada archivo de comando
3. Verifique que la convención de nombres sea consistente

Comandos creados:
- /project-info
- /env-check
- /run-tests

Verifique que cada comando sea reconocido por Cursor.
```

**Resultado esperado**: Puede confirmar que los comandos creados se reconocen correctamente.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "El comando no se reconoce"},
      {"id": "trouble_2", "label": "La descripción no se muestra"},
      {"id": "trouble_3", "label": "El código dentro del comando no se ejecuta"},
      {"id": "trouble_4", "label": "El texto en japonés tiene problemas de codificación"}
    ]
  }]
}
```


### Problema 1: "El comando no se reconoce"
**Causa**: La ruta del archivo es incorrecta, o el formato Markdown es invalido
**Prompt de solucion**:
```text
Verifique lo siguiente:
1. ¿El archivo está en el directorio .cursor/commands/?
2. ¿La extensión del archivo es .md?
3. ¿El formato del frontmatter (sección encerrada entre ---) es correcto?
```

### Problema 2: "La descripcion no se muestra"
**Causa**: Error de sintaxis del frontmatter YAML
**Prompt de solucion**:
```text
Verifique el formato del frontmatter:
---
description: "texto de descripción"
---

Nota: Se requiere un espacio después de los dos puntos.
```

### Problema 3: "El codigo dentro del comando no se ejecuta"
**Causa**: Los comandos son instrucciones y no se ejecutan automaticamente
**Prompt de solucion**:
```text
Los comandos de Cursor funcionan como "plantillas".
Los bloques de código dentro de los comandos deben ser copiados y pegados por el usuario,
o debe instruir a la IA con "ejecute este comando".
```

### Problema 4: "El texto en japones tiene problemas de codificacion"
**Causa**: La codificacion del archivo no es UTF-8
**Prompt de solucion**:
```text
Verifique que el archivo esté guardado en UTF-8.
Configure la codificación predeterminada a UTF-8 en la configuración de Cursor.
```

---

## ✅ Punto de control
- [ ] El directorio .cursor/commands/ existe
- [ ] project-info.md esta creado
- [ ] env-check.md esta creado
- [ ] run-tests.md esta creado
- [ ] Los comandos se reconocen en Cursor


---

## 📋 Vista previa de resultados

### Salida esperada
```text
📁 output/
└── {nombre-del-proyecto}/  (artefactos de agente/código)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/{nombre-del-proyecto}/

# Verificar el inicio (primeras 30 lineas)
head -30 output/{nombre-del-proyecto}/
```

> 💡 Ver texto completo: `cat output/{nombre-del-proyecto}/` para mostrar el texto completo

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Cursor para verificar la finalizacion:

```text
# Verificación de finalización: Verifique que se hayan generado los archivos de salida esperados en la carpeta output/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-6-2)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-6-2
- finish → Finalizar
