---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "35 min"
prerequisites: ["start-16-1"]
level: "intermediate"
tags: ["email", "gmail", "gogcli", "send"]
---

# Lección 16-3: Envió de Correo con gogcli

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-3: Envió de Correo con gogcli**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Practicar la creación, envió, respuesta en hilo y adjuntos con `gog gmail send` |
| Duración | ~35 min |
| Herramientas utilizadas | gogcli (gog) |
| Requisitos previos | Lección 16-1 completada (gogcli autenticado) |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

> **Importante**: El envío de correo es una operación irreversible. Verifique bien el contenido antes de enviar.
> **Nota**: En v0.9.0, el flag `--dry-run` fue eliminado. La verificación previa al envío debe realizarse visualmente.

---

## Paso 1: Verificación de Versión y Preparación

```bash
gog --version
```

Confirme que es v0.9.0 o superior. Todos los comandos `gog gmail` requieren `--account <su-email@gmail.com>`.

---

## Paso 2: Enviar Correo de Prueba

**Envie siempre a su propia dirección de correo.**

```bash
gog gmail send \
  --account <su-email@gmail.com> \
  --to <su-email@gmail.com> \
  --subject "Prueba de envio con gogcli" \
  --body "Este es un correo de prueba enviado desde gogcli (gog gmail send)."
```

---

## Paso 3: Respuesta en Hilo

**Obtener el ID del hilo:**
```bash
gog gmail search "subject:Prueba de envio con gogcli" --account <su-email@gmail.com> --max 1
```

**Responder al hilo:**
```bash
gog gmail send \
  --account <su-email@gmail.com> \
  --thread-id <thread-id> \
  --subject "Re: Prueba de envio con gogcli" \
  --body "Esta es una prueba de respuesta en hilo desde gogcli."
```

> **Nota**: En v0.9.0, `--subject` es obligatorio. No se puede omitir al responder.

---

## Paso 4: Envió con Archivo Adjunto

**Crear archivo de prueba:**
```bash
echo "Contenido del archivo adjunto de prueba." > /tmp/test-attachment.txt
```

**Enviar correo con adjunto:**
```bash
gog gmail send \
  --account <su-email@gmail.com> \
  --to <su-email@gmail.com> \
  --subject "Prueba de archivo adjunto" \
  --body "Prueba de correo con archivo adjunto." \
  --attach /tmp/test-attachment.txt
```

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| `insufficient permission` | `gog auth remove <email>` -> `gog auth add <email>` para re-autenticar |
| Enviado pero no recibido | Verifique la carpeta de correo no deseado |
| `thread not found` | Verifique que el ID del hilo sea correcto con `gog gmail search` |
| Error de archivo adjunto | Verifique que la ruta del archivo sea correcta (se recomienda ruta absoluta) |

---

## Punto de Control

- [ ] Verificó `gog --version` es v0.9.0 o superior
- [ ] Envió un correo de prueba a sí mismo y confirmó la recepción
- [ ] Realizó una respuesta en hilo con `--thread-id`
- [ ] Envió un archivo adjunto con `--attach`

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-3 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_lesson", "label": "Ir a 16-4 -> Diseno de secuencia de correos"},
      {"id": "practice", "label": "Quiero practicar mas envios"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
