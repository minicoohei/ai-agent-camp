---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "30 min"
prerequisites: ["start-16-1", "start-16-2", "start-16-3"]
level: "advanced"
tags: ["email", "gmail", "gogcli", "github-actions", "automation"]
nonInteractiveMode: deferred
---
# Lección 16-5: Flujo de Trabajo de Automatización de Correo

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-5: Flujo de Trabajo de Automatización de Correo**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Automatizar el envío periódico de correos con GitHub Actions y configurar notificaciones a Slack |
| Duración | ~30 min |
| Herramientas utilizadas | gogcli (gog), check-inbox, GitHub Actions |
| Requisitos previos | Lecciones 16-1 a 16-3 completadas |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

**Flujo de la sesión:**
1. Disenar la visión general de la automatización de correo
2. Crear el flujo de trabajo de GitHub Actions
3. Configurar notificaciones a Slack
4. Ejercicio integral (integración de todas las habilidades)

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Paso 1: Visión General de la Automatización de Correo

Pipeline de automatización construido con GitHub Actions + gogcli:

```text
+-------------------------------------------+
|         GitHub Actions (cron)             |
|  +-------------+  +-----------------+    |
|  | google-sync  |->|  check-inbox    |    |
|  | Sincronizar  |  |  Extraer tareas |    |
|  +-------------+  +--------+--------+    |
|                             |              |
|  +-------------+  +--------v--------+    |
|  | gog send    |<-|  Borrador de     |    |
|  | Enviar correo|  |  respuesta      |    |
|  +------+------+  +-----------------+    |
|         |                                 |
|  +------v---------------------------+    |
|  | Notificacion a Slack (resumen)    |    |
|  +-----------------------------------+    |
+-------------------------------------------+
```

---

## Paso 2: Disenar el Flujo de Trabajo de GitHub Actions

**Disenar un ejemplo de flujo de trabajo:**
```text
Disene un flujo de trabajo de GitHub Actions con los siguientes requisitos:

1. Disparador: Ejecutar cada manana a las 9:00 (hora local)
2. Pasos:
   a. Sincronizar correos con google-sync
   b. Extraer tareas con check-inbox
   c. Producir resumen como salida
   d. Notificar a Slack
3. Variables de entorno: GOOGLE_CREDENTIALS (Secret)
```

---

## Paso 3: Configurar Notificaciones a Slack

**Configuración de Slack Webhook:**
1. Configurar Incoming Webhook de la aplicación Slack
2. Guardar la URL del Webhook en GitHub Secrets
3. Enviar la notificación con `curl` dentro del flujo de trabajo

---

## Paso 4: Ejercicio Integral

Ejercicio que integra todas las habilidades aprendidas en el Module 16.

**Tarea del ejercicio:**
```text
Construya el siguiente pipeline de automatizacion de correo:

1. Obtener correos recibidos con gogcli
2. Extraer tareas y determinar prioridad con check-inbox
3. Generar borradores de respuesta para correos de alta prioridad
4. Verificar el contenido del envio
5. Enviar respuestas con gogcli
6. Notificar los resultados del procesamiento a Slack
```

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| Error de credenciales en GitHub Actions | Verifique que los valores correctos esten configurados en Secrets |
| El cron no se ejecuta | Verifique la sintaxis cron (atención UTC: 9:00 JST = 0:00 UTC) |
| Las notificaciones de Slack no llegan | Verifique que la URL del Webhook sea correcta |
| gogcli no funciona en entorno CI | Verifique que el binario `gog` este en el PATH |

---

## Punto de Control

- [ ] Diseño el flujo de trabajo de automatización de correo
- [ ] Se creó el archivo YAML de GitHub Actions
- [ ] Comprendio el mecanismo de notificaciones a Slack
- [ ] Uso todas las habilidades de forma integrada en el ejercicio integral

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Todas las lecciones del Module 16 completadas!",
  "questions": [{
    "id": "next_action",
    "prompt": "Felicitaciones! Que desea hacer a continuacion?",
    "options": [
      {"id": "next_module", "label": "Ir al Module 14 -> Creacion de articulos"},
      {"id": "review_all", "label": "Quiero revisar el Module 16"},
      {"id": "home", "label": "Volver al inicio"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
