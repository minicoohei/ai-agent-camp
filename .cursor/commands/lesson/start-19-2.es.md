---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module19-outlook-windows"
duration: "Aprox. 35 min"
prerequisites: ["start-19-1"]
level: "intermediate"
tags: ["outlook", "microsoft365", "rules", "folders", "categories"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 19-2: Carpetas, reglas y categorías

## 📍 Qué harás en esta sesión

¡Bienvenido a **Lesson 19-2: Carpetas, reglas y categorías**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Automatizar la organización del correo usando carpetas, reglas y categorías de Outlook |
| Duración | Aprox. 35 min |
| Habilidades | Configuración de reglas de Outlook, gestión de categorías, m365 CLI |
| Requisitos previos | Lesson 19-1 completada (autenticación de m365 CLI configurada) |
| Página del curso | Consulta [Módulo 19: Outlook](https://ai-agent.camp/es/course/module-19) en paralelo |

> **💡 Info de herramientas**: Esta lección usa m365 CLI. Funciona con Cursor IDE y Claude Code (CLI/Escritorio). En algunos entornos como Codex CLI, puede aparecer el error `request_user_input is not supported`. En ese caso, consulta la sección "Flujo de trabajo alternativo".

**Flujo de la sesión:**
1. Aprender diseño de carpetas que mantiene la bandeja de entrada ligera
2. Configurar condiciones y acciones de reglas (mover, asignar categorías, etc.)
3. Comprender el etiquetado transversal con categorías
4. Después de aplicar las reglas de organización, automatizar listado y envío de correos con m365 CLI
5. Registrar y guardar resultados de configuración en output/outlook/

Al final de esta sesión, podrás organizar tu bandeja de entrada usando carpetas, reglas y categorías de Outlook, y automatizar tareas con m365 CLI.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad, escribe "continúa" o "sigue" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificación de preparación

Primero confirmemos que todo está configurado.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Estás listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Empecemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la página del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar requisitos previos)
(view_html → Mostrar ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Step 1: Diseño de carpetas — No dejes que la bandeja desborde

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Fundamentos del diseño de carpetas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Por favor, explica las mejores prácticas para el diseño de carpetas en Outlook. Cubre lo siguiente:

1. Principios básicos del diseño de carpetas:
   - Apuntar a Inbox Zero
   - Mantener la jerarquía en máximo 2 niveles (demasiado profundo es inmanejable)
   - Organización basada en acciones vs. basada en proyectos

2. Ejemplo de estructura de carpetas recomendada:
   - 📁 01_Acción requerida (correos que necesitan respuesta)
   - 📁 02_Esperando (esperando respuesta/aprobación)
   - 📁 03_Referencia (solo lectura/informativo)
   - 📁 04_Proyectos/ (subcarpetas por proyecto)
   - 📁 05_Archivo/ (mensual/anual)

3. Listar carpetas con m365 CLI:
   m365 outlook mail folder list
```

**Resultado esperado**: Comprendes los principios de diseño de carpetas y has revisado tu estructura actual.

---

## 🚀 Step 2: Condiciones y acciones de reglas (Mover, Categorizar)

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Condiciones y acciones de reglas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Por favor, explica cómo configurar reglas en Outlook. Cubre lo siguiente:

1. Estructura básica de una regla:
   - Condición: Cuándo se activa la regla
   - Acción: Qué sucede cuando se cumplen las condiciones
   - Excepción: Cuándo no aplicar la regla

2. Condiciones comunes:
   - Filtrar por remitente (from)
   - El asunto contiene una palabra clave
   - Destinatario (to/cc) — cuando estás en CC
   - Por dominio (@empresa.com, etc.)

3. Acciones comunes:
   - Mover a carpeta específica
   - Asignar categoría
   - Cambiar nivel de importancia
   - Agregar bandera
   - Mostrar notificación

4. Práctica: Crear las siguientes reglas en Outlook
   - Regla 1: Correos internos (@tu-dominio) → Asignar categoría "Interno"
   - Regla 2: Boletines → Mover a carpeta "03_Referencia"
   - Regla 3: Correos de tu jefe → Establecer importancia "Alta"

5. Registrar la configuración en output/outlook/rules-config.json
```

**Resultado esperado**: Se crean tres reglas en Outlook con clasificación automática basada en condiciones.

---

## 🚀 Step 3: Etiquetado transversal con categorías

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Etiquetado transversal con categorías",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Configura el etiquetado transversal usando la función de categorías de Outlook.

Pasos:
1. Conceptos básicos de categorías:
   - Carpetas = un correo solo puede estar en una carpeta
   - Categorías = un correo puede tener múltiples etiquetas
   - Usa carpetas para "ubicación", categorías para "naturaleza"

2. Ejemplo de diseño de categorías:
   - 🔴 Urgente (Rojo): Necesita acción hoy
   - 🟡 Esta semana (Amarillo): Necesita acción esta semana
   - 🟢 Info (Verde): Solo lectura
   - 🔵 Proyecto A (Azul): Relacionado con Proyecto A
   - 🟣 Proyecto B (Púrpura): Relacionado con Proyecto B

3. Verificar categorías con m365 CLI:
   m365 outlook mail list --top 10 --query "categories/any(c:c eq 'Urgente')"

4. Diseñar reglas combinadas para categorías y carpetas
5. Registrar la configuración en output/outlook/categories-config.json
```

**Resultado esperado**: Las categorías están configuradas y combinadas con carpetas para una gestión eficiente del correo.

---

## 🚀 Step 4: Automatización de listado y envío de correos con m365 CLI

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Automatización con m365 CLI",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Usa m365 CLI para automatizar el listado y envío de correos después de la organización.

Pasos:
1. mkdir -p output/outlook

2. Obtener listas de correo por carpeta:
   # Lista de correos de la bandeja de entrada
   m365 outlook mail list --top 20 --output json > output/outlook/inbox-list.json

   # Listar carpetas de correo
   m365 outlook mail folder list --output json

3. Obtención con filtros:
   # Solo correos no leídos
   m365 outlook mail list --filter "isRead eq false" --output json

   # Correos con categoría específica
   m365 outlook mail list --filter "categories/any(c:c eq 'Urgente')" --output json

4. Automatizar envío de correo:
   m365 outlook mail send \
     --to "colega@ejemplo.com" \
     --subject "Informe semanal" \
     --bodyContents "Adjunto el informe de esta semana." \
     --bodyContentType Text

5. Guardar resultados en output/outlook/automation-result.json
```

**Resultado esperado**: El listado y envío de correos se automatizan con m365 CLI, los resultados se guardan en output/outlook/.

---

## 🚀 Step 5: Verificación de configuración y registro

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificación de configuración y registro",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Verifica los resultados de configuración y crea un resumen.

Pasos:
1. Mostrar la estructura de carpetas que creaste
2. Revisar la lista de reglas con condiciones y acciones de cada una
3. Revisar el diseño de categorías y las reglas operativas
4. Crear un resumen en output/outlook/summary.md que cubra:
   - Estructura de carpetas
   - Configuración de reglas (condición → acción)
   - Diseño de categorías
   - Lista de comandos de automatización m365 CLI
5. Sugerir 3 puntos de mejora para operaciones futuras
```

**Resultado esperado**: Se guarda un resumen de configuración de carpetas, reglas y categorías en output/outlook/.

---

## ⚠️ Solución de problemas comunes

AskUserQuestion (AskQuestion) te permite seleccionar el problema para recibir orientación.

**Configuración de AskQuestion:**
```json
{
  "title": "Selecciona tu problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Selecciona el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "La autenticación de m365 CLI expiró"},
      {"id": "trouble_2", "label": "Las reglas no funcionan como se esperaba"},
      {"id": "trouble_3", "label": "Las categorías no aparecen"},
      {"id": "trouble_4", "label": "Error al enviar correo"}
    ]
  }]
}
```


### Problema 1: "La autenticación de m365 CLI expiró"
**Causa**: El token de acceso ha expirado
**Prompt de solución**:
```
Re-autentícate con el comando m365 login.
Usa m365 status para verificar el estado actual de autenticación.
Si el token ha expirado, se requiere re-autenticación por navegador.
```

### Problema 2: "Las reglas no funcionan como se esperaba"
**Causa**: Condiciones de regla incorrectas o problemas de prioridad
**Prompt de solución**:
```
Revisa las condiciones y acciones en la configuración de reglas de Outlook.
Las reglas se aplican de arriba hacia abajo, así que verifica su orden de prioridad.
Verifica si la opción "Detener el procesamiento de más reglas" está habilitada.
```

### Problema 3: "Las categorías no aparecen"
**Causa**: Categorías no creadas o consulta de filtro incorrecta
**Prompt de solución**:
```
Verifica si las categorías están creadas en Configuración de Outlook → Gestión de categorías.
Verifica que la sintaxis del filtro de m365 CLI sea correcta.
Los nombres de categorías deben especificarse como coincidencia exacta.
```

### Problema 4: "Error al enviar correo"
**Causa**: Permisos insuficientes o parámetros de envío inválidos
**Prompt de solución**:
```
Verifica que el permiso Mail.Send esté otorgado a m365 CLI.
Verifica que se especifique una dirección de correo válida en el parámetro --to.
--bodyContentType puede ser Text o HTML.
```

---

## ✅ Punto de control
- [ ] Comprendidos los principios de diseño de carpetas y revisada la estructura
- [ ] Configuradas las condiciones y acciones de reglas para clasificación automática
- [ ] Comprendido el etiquetado transversal con categorías
- [ ] Automatizado el listado y envío de correos con m365 CLI
- [ ] Resultados de configuración guardados en output/outlook/


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 output/outlook/
├── inbox-list.json            ← Lista de correos de la bandeja
├── rules-config.json          ← Registro de configuración de reglas
├── categories-config.json     ← Registro de configuración de categorías
├── automation-result.json     ← Resultados de automatización m365 CLI
└── summary.md                 ← Resumen de configuración
```
> Formato: JSON / Markdown

### Comandos de verificación
```bash
# Verificar archivos de salida
ls -lh output/outlook/

# Verificar lista de correos
cat output/outlook/inbox-list.json | jq '.[:3]'

# Verificar resumen
cat output/outlook/summary.md
```

> 💡 **Claude Code**: `Read output/outlook/summary.md` para vista previa en chat
> 💡 **Cursor**: Haz clic en el archivo en el explorador de archivos para previsualizar

---

## ✅ Verificación de finalización
Pega lo siguiente en el chat de Cursor para verificar el estado de finalización:

```
# Verificación de finalización: Verifica que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de completado/incompleto y los elementos faltantes.

---

## ➡️ Próximos pasos

AskUserQuestion (AskQuestion) te permite elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elige el próximo paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elige tu próxima acción",
    "options": [
      {"id": "next_module", "label": "Avanzar al Módulo 20 (/start-20-1)"},
      {"id": "review_module", "label": "Revisar Módulo 19"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Guía después de la selección:**
- next_module → /start-20-1 para el Módulo 20
- review_module → Revisar cada lección del Módulo 19
- finish → Finalizar sesión
