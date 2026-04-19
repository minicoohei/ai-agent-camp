---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "gmail"]
---

# 🎓 Lesson 4-2: Busqueda y navegacion de Gmail

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-2: Busqueda y navegacion de Gmail**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Buscar, visualizar y analizar correos de Gmail usando gogcli |
| Duracion | ~25 min |
| Skills utilizados | gogcli gmail |
| Requisitos previos | Configuracion de autenticacion de gogcli completada (start-4-1 finalizado) |

**Flujo de la sesion:**
1. Aprender la sintaxis de consulta de busqueda de Gmail
2. Ver detalles del hilo de correo
3. Analizar y resumir resultados de busqueda con IA

Al finalizar esta sesion, podra buscar y analizar libremente correos de Gmail usando gogcli.

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
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → `gog auth list`  para verificar estado de autenticacion)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Aprender sintaxis de consulta de busqueda de Gmail

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Aprender la sintaxis de consulta de busqueda de Gmail",
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

Probemos la sintaxis de consulta principal disponible en la busqueda de Gmail de gogcli:

```bash
# Buscar correos no leidos
gog gmail search "is:unread" --account your-email@gmail.com

# Buscar correos de un remitente especifico
gog gmail search "from:example@company.com" --account your-email@gmail.com

# Buscar correos de los ultimos 7 dias
gog gmail search "newer_than:7d" --account your-email@gmail.com

# Buscar correos con palabras clave en el asunto
gog gmail search "subject:reunion" --account your-email@gmail.com

# Buscar correos con archivos adjuntos
gog gmail search "has:attachment newer_than:30d" --account your-email@gmail.com

# Condiciones compuestas: no leidos y dentro de los ultimos 3 dias
gog gmail search "is:unread newer_than:3d" --account your-email@gmail.com
```

**Operadores de busqueda principales:**

| Operador | Descripcion | Ejemplo |
|--------|------|-----|
| `is:unread` | Correos no leidos | `is:unread` |
| `from:` | Especificar remitente | `from:boss@company.com` |
| `to:` | Especificar destinatario | `to:team@company.com` |
| `subject:` | Busqueda por asunto | `subject:acta-de-reunion` |
| `newer_than:` | Especificacion de periodo | `newer_than:7d` / `newer_than:1m` |
| `has:attachment` | Tiene adjunto | `has:attachment` |
| `label:` | Especificacion de etiqueta | `label:important` |
| `in:` | Especificacion de carpeta | `in:inbox` / `in:sent` |

**Resultado esperado**: Se muestra una lista de correos que coinciden con cada consulta (ID de correo, asunto, remitente, fecha/hora).

---

## 🚀 Step 2: Navegar detalles de hilos de correo

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Ver detalles del hilo de correo",
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

Utilice los IDs de hilo obtenidos en el Step 1 para verificar los detalles:

```bash
# Obtener ID del hilo mediante busqueda de correo
gog gmail search "newer_than:1d" --account your-email@gmail.com

# Obtener detalles del hilo (usar el ID mostrado arriba)
gog gmail thread get <ID-del-hilo> --account your-email@gmail.com

# Obtener cuerpo del mensaje
gog gmail message get <ID-del-mensaje> --account your-email@gmail.com
```

**Pasos:**
1. `gog gmail search` para buscar correos y anotar el ID del hilo de los correos de interes
2. `gog gmail thread get` para ver el hilo completo (incluyendo respuestas)
3. `gog gmail message get` para obtener el cuerpo de los mensajes individuales

**Resultado esperado**: Se muestran el asunto, remitente, fecha/hora y cuerpo del correo. La vista de hilo tambien muestra la cadena de respuestas.

---

## 🚀 Step 3: Analizar y resumir resultados de busqueda con IA

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Analizar y resumir resultados de busqueda con IA",
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

Haga que la IA analice los correos obtenidos con gogcli:

```bash
# Obtener correos no leidos de la ultima semana
gog gmail search "is:unread newer_than:7d" --account your-email@gmail.com
```

Pegue la lista de correos obtenida en el chat de Cursor y solicite el analisis con un prompt como el siguiente:

```text
Analice la lista de correos anterior y resuma desde las siguientes perspectivas:
1. Correos que requieren respuesta (prioridad: Alta/Media/Baja)
2. Correos solo informativos (FYI)
3. Correos que contienen tareas
4. Resumen de una linea para cada correo
```

**Ejemplo avanzado:**
```bash
# Resumir las interacciones con una persona especifica cronologicamente
gog gmail search "from:boss@company.com newer_than:30d" --account your-email@gmail.com

# -> Solicitar a la IA: "Resuma los correos anteriores cronologicamente y extraiga las solicitudes pendientes"
```

**Resultado esperado**: La IA clasifica los correos y genera una lista de tareas priorizada y un resumen.

---

## ⚠️ Problemas comunes y soluciones

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "La busqueda devuelve 0 resultados"},
      {"id": "trouble_2", "label": "El cuerpo del correo tiene caracteres ilegibles"},
      {"id": "trouble_3", "label": "Se produce un error de autenticacion"},
      {"id": "trouble_4", "label": "Error por olvidar --account"}
    ]
  }]
}
```

### Problema 1: "Los resultados de busqueda devuelven 0 elementos"
**Causa**: Error de sintaxis en la consulta, o no existen correos coincidentes
**Prompt de solucion**:
```text
Intente una consulta mas amplia. Primero verifique si hay correos de los ultimos 30 dias con "newer_than:30d".
Si la busqueda por asunto no funciona bien, intente filtrar por remitente o fecha.
```

### Problema 2: "El cuerpo del correo tiene problemas de codificacion"
**Causa**: Problema de codificacion
**Prompt de solucion**:
```text
Intente redirigir la salida de gogcli a un archivo:
gog gmail message get <id> --account <email> > /tmp/mail.txt
Verifique la codificacion del archivo: file /tmp/mail.txt
```

### Problema 3: "Ocurre un error de autenticacion"
**Causa**: El token ha expirado
**Prompt de solucion**:
```text
Elimine la autenticacion con gog auth remove your-email@gmail.com,
luego vuelva a autenticarse con gog auth add your-email@gmail.com.
```

### Problema 4: "Error por olvidar --account"
**Causa**: gogcli requiere --account para todos los comandos
**Prompt de solucion**:
```text
En gogcli, --account <direccion-de-correo> es obligatorio para todos los comandos.
Configurar un alias es conveniente:
alias gogg="gog --account your-email@gmail.com"
```

---

## ✅ Punto de control
- [ ] Comprendio la sintaxis de consulta de busqueda de Gmail (is:unread, from:, newer_than:, etc.)
- [ ] Pudo ver los detalles del hilo de correo
- [ ] Pudo hacer que la IA analice los resultados de busqueda y genere resumenes
- [ ] Pudo buscar con condiciones compuestas


---

## 📋 Vista previa de resultados

El entregable de esta leccion es la salida de la terminal.

### Salida esperada
```text
┌─────────────────────────────────────┐
│  Resultado de ejecución del comando    │
│  Estado: ✅ Éxito                       │
│  Elementos procesados: N               │
└─────────────────────────────────────┘
```

> Consejo: Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Codex para verificar la finalizacion:

```text
Ejecute los siguientes comandos de gogcli para verificar que la busqueda y visualizacion de Gmail funcionen correctamente:
1. gog gmail search "is:unread newer_than:7d" --account <su-correo>
2. Seleccione un resultado y muestre los detalles del hilo con gog gmail thread get
Verifique que todos los comandos funcionen correctamente.
```

**Resultado esperado**: Los resultados de busqueda y detalles del hilo se muestran sin errores.

---

## 🎉 Siguientes pasos

La busqueda y visualizacion de Gmail esta completa! En la siguiente leccion, aprendera operaciones de Google Calendar.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/start-4-3)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-3)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /start-4-3（Operaciones de Google Calendar)
- next_window → Abrir nueva ventana con /start-4-3
- finish → Finalizar
