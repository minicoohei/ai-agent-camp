---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "25 min"
prerequisites: []
level: "beginner"
tags: ["email", "gmail", "gogcli", "setup"]
---

# Lección 16-1: Configuración de Gmail - Autenticación y Sincronización de Correo con gogcli

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-1: Configuración de Gmail**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Autenticarse en Gmail con gogcli y preparar la búsqueda y lectura de correos |
| Duración | ~25 min |
| Herramientas utilizadas | gogcli (gog) |
| Requisitos previos | Cuenta de Google (Gmail) |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

**Flujo de la sesión:**
1. Verificar la instalación de gogcli
2. Configurar la autenticación de Gmail con `gog auth add`
3. Probar la búsqueda de correos con `gog gmail search`
4. Verificar la sincronización de correo con google-sync

Al finalizar esta sesión, podrá acceder a Gmail con gogcli y buscar/leer correos.

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Verificación de Preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo?",
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

## Paso 1: Verificar la Instalación de gogcli

**Comando a ejecutar:**
```bash
gog --version
```

**Resultado esperado:**
- Si se muestra el número de versión, está correcto (se recomienda v0.9.0 o superior)
- Si el comando no se encuentra, instale con `brew install gogcli` (o ejecute `/setup-gogcli`)

> **Nota**: En los comandos siguientes, todas las llamadas a la API de Gmail requieren `--account <su-email@gmail.com>`. Especifiquelo explicitamente si tiene varias cuentas registradas.

---

## Paso 2: Configurar la Autenticación de Gmail

**Comando a ejecutar:**
```bash
gog auth add <su-email@gmail.com>
```

Se abrirá el navegador mostrando la pantalla de autenticación OAuth de Google.
Después de conceder acceso, el token se guardará localmente.

**Verificar autenticación:**
```bash
gog auth list
```

**Verificar los scopes:**
```bash
gog auth services
```

Confirme que el scope de envío de Gmail (`gmail.send`) está incluido.

---

## Paso 3: Prueba de Búsqueda de Correos

**Buscar correos no leidos:**
```bash
gog gmail search "is:unread" --account <su-email@gmail.com> --max 5
```

**Buscar correos de un remitente específico:**
```bash
gog gmail search "from:noreply@github.com" --account <su-email@gmail.com> --max 5
```

---

## Paso 4: Sincronización de Correo con google-sync (Opcional)

La habilidad check-inbox lee archivos Markdown locales.
Sincronice los correos localmente con google-sync para que 13-2 funcione sin problemas.

**Verificar sincronización:**
```bash
ls data/google-sync/data/*/gmail/ 2>/dev/null || echo "No hay datos de sincronizacion"
```

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| Comando `gog` no encontrado | Ejecute `brew install gogcli` (o `/setup-gogcli`) |
| El navegador no se abre en la autenticación | Use `gog auth add --no-browser <email>` para copiar la URL manualmente |
| Scope de OAuth insuficiente | `gog auth remove <email>` -> vuelva a ejecutar `gog auth add <email>` |
| La búsqueda devuelve resultados vacios | Cambie la consulta a `is:inbox` y reintente |

---

## Punto de Control

- [ ] `gog --version` muestra el número de versión
- [ ] `gog auth list` muestra la cuenta
- [ ] `gog gmail search "is:inbox" --account <su-email@gmail.com> --max 3` recupera correos

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-1 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_lesson", "label": "Ir a 16-2 -> Analisis de correos recibidos y extraccion de tareas"},
      {"id": "practice", "label": "Quiero practicar mas busquedas"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
