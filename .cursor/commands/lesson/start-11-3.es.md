---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "~25 min"
prerequisites: ["start-11-2"]
level: "intermediate"
tags: ["github-actions", "news", "email", "slack", "webhook", "cron"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-3: Flujo de trabajo de obtencion de noticias y distribucion por correo/Slack

## 📍 Lo que hara en esta sesion

**Leccion 11-3: Obtencion de noticias y distribucion por correo/Slack**!

| Elemento | Contenido |
|------|------|
| Objetivo | Construir un flujo de trabajo en GitHub Actions que obtiene noticias automaticamente y las distribuye por correo electronico y Slack |
| Duracion | ~25 min |
| Habilidades utilizadas | GitHub Actions, Python (requests), Slack Webhook, smtplib |
| Requisitos previos | Leccion 11-2 completada (comprension de la configuracion de Secrets) |

**Flujo de la sesion:**
1. Creacion del script de obtencion de noticias
2. Implementacion del envio por correo electronico
3. Configuracion de notificaciones via Slack Webhook
4. Creacion del flujo de trabajo de GitHub Actions
5. Configuracion de Secrets y pruebas de funcionamiento

Al final de esta sesion, tendra un pipeline que recopila noticias periodicamente y las distribuye automaticamente por correo electronico y Slack.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar.

---

## 🎯 Verificacion de preparacion

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar que la Leccion 11-2 esta completada. Verificar la existencia del directorio `.github/workflows/`)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Creacion del script de obtencion de noticias

```json
{
  "title": "🚀 Step 1: Script de obtencion de noticias",
  "questions": [{
    "id": "step_action",
    "prompt": "Crearemos un script en Python que obtiene noticias desde feeds RSS o la News API.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar el funcionamiento de RSS/API"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `tools/fetch_news.py`:

```python
#!/usr/bin/env python3
"""Script de obtencion de noticias — Recopila noticias desde feeds RSS"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

# URLs de feeds RSS (ejemplo: Hacker News, TechCrunch)
RSS_FEEDS = [
    {"name": "Hacker News", "url": "https://hnrss.org/newest?count=5"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
]

def fetch_rss(url, max_items=5):
    """Obtener noticias desde un feed RSS"""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    items = []
    for item in root.iter("item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        items.append({"title": title, "link": link, "pubDate": pub_date})
        if len(items) >= max_items:
            break
    return items

def main():
    all_news = []
    for feed in RSS_FEEDS:
        try:
            items = fetch_rss(feed["url"])
            all_news.append({"source": feed["name"], "items": items})
        except Exception as e:
            print(f"[WARN] {feed['name']}: {e}")
    
    # Salida JSON
    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "feeds": all_news
    }
    with open("output/news_digest.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Obtencion completada: {sum(len(f['items']) for f in all_news)} noticias")
    return output

if __name__ == "__main__":
    main()
```

```bash
mkdir -p output && python tools/fetch_news.py
```

**Resultado esperado**: Los datos de noticias se guardan en `output/news_digest.json`.

---

## 🚀 Step 2: Implementacion del envio por correo electronico

```json
{
  "title": "🚀 Step 2: Envio por correo",
  "questions": [{
    "id": "step_action",
    "prompt": "Agregaremos el proceso de envio de las noticias obtenidas por correo electronico.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar el uso de smtplib"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Agregar la funcion de envio a `tools/fetch_news.py`:

```python
import smtplib
from email.mime.text import MIMEText
import os

def send_email(news_data):
    """Enviar resumen de noticias por correo electronico"""
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    to_email = os.environ.get("NOTIFY_EMAIL", smtp_user)
    
    if not smtp_user or not smtp_pass:
        print("[SKIP] Envio de correo omitido: credenciales SMTP no configuradas")
        return

    # Crear cuerpo del correo
    body_lines = [f"# Resumen de noticias ({news_data['generated_at'][:10]})\n"]
    for feed in news_data["feeds"]:
        body_lines.append(f"\n## {feed['source']}")
        for item in feed["items"]:
            body_lines.append(f"- [{item['title']}]({item['link']})")
    
    body = "\n".join(body_lines)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"Resumen de noticias {news_data['generated_at'][:10]}"
    msg["From"] = smtp_user
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    print(f"Correo enviado correctamente a: {to_email}")
```

**Punto clave**: Si usa Gmail, necesitara una contrasena de aplicacion. Configure `SMTP_USER` y `SMTP_PASS` en Secrets.

**Resultado esperado**: El resumen de noticias se envia por correo electronico.

---

## 🚀 Step 3: Configuracion de notificaciones via Slack Webhook

```json
{
  "title": "🚀 Step 3: Notificacion a Slack",
  "questions": [{
    "id": "step_action",
    "prompt": "Enviaremos notificaciones de noticias usando Slack Incoming Webhook.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar como crear un Slack Webhook"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

```python
def send_slack(news_data):
    """Enviar notificacion de noticias via Slack Webhook"""
    webhook_url = os.environ.get("SLACK_WEBHOOK", "")
    if not webhook_url:
        print("[SKIP] Notificacion a Slack omitida: SLACK_WEBHOOK no configurado")
        return

    # Construir mensaje de Slack
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "📰 Resumen de noticias"}}]
    for feed in news_data["feeds"]:
        items_text = "\n".join(f"• <{i['link']}|{i['title']}>" for i in feed["items"])
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{feed['source']}*\n{items_text}"}
        })

    payload = {"blocks": blocks}
    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    print("Notificacion a Slack enviada correctamente")
```

**Pasos para crear la Webhook URL:**
1. Activar "Incoming Webhooks" en la Slack App
2. Seleccionar el canal de destino con "Add New Webhook to Workspace"
3. Configurar la URL generada en GitHub Secrets como `SLACK_WEBHOOK`

**Resultado esperado**: El resumen de noticias se publica en el canal especificado.

---

## 🚀 Step 4: Creacion del flujo de trabajo de GitHub Actions

```json
{
  "title": "🚀 Step 4: Creacion del flujo de trabajo",
  "questions": [{
    "id": "step_action",
    "prompt": "Crearemos un flujo de trabajo que obtiene y distribuye noticias con un horario cron.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar la sintaxis de expresiones cron"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/news-digest.yml`:

```yaml
name: News Digest
on:
  schedule:
    - cron: '0 0 * * *'  # UTC 0:00 = JST 9:00
  workflow_dispatch:
    inputs:
      skip_email:
        description: 'Omitir envio de correo'
        type: boolean
        default: false

jobs:
  news-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: uv add requests

      - name: Fetch news
        run: |
          mkdir -p output
          python tools/fetch_news.py

      - name: Send email notification
        if: ${{ !inputs.skip_email }}
        env:
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          NOTIFY_EMAIL: ${{ secrets.NOTIFY_EMAIL }}
        run: python -c "from tools.fetch_news import *; send_email(main())"

      - name: Send Slack notification
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        run: python -c "from tools.fetch_news import *; send_slack(main())"

      - uses: actions/upload-artifact@v4
        with:
          name: news-digest-${{ github.run_number }}
          path: output/news_digest.json
          retention-days: 7
```

**Resultado esperado**: El archivo de flujo de trabajo se crea y aparece en `gh workflow list`.

---

## 🚀 Step 5: Configuracion de Secrets y pruebas de funcionamiento

```json
{
  "title": "🚀 Step 5: Ejecucion de prueba",
  "questions": [{
    "id": "step_action",
    "prompt": "Configuraremos los Secrets y ejecutaremos el flujo de trabajo manualmente para probarlo.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar como configurar Secrets"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

1. **Configuracion de Secrets** (GitHub Web UI: Settings → Secrets and variables → Actions):
   - `SLACK_WEBHOOK`: URL del Slack Incoming Webhook
   - `SMTP_USER`: Direccion de Gmail (si se envia correo)
   - `SMTP_PASS`: Contrasena de aplicacion de Gmail (si se envia correo)
   - `NOTIFY_EMAIL`: Direccion de correo del destinatario

2. **Prueba de ejecucion manual**:
```bash
# Ejecutar el flujo de trabajo manualmente
gh workflow run "News Digest"

# Verificar resultados de ejecucion
gh run list --limit 3
```

3. **Verificacion de logs**:
```bash
gh run view <run_id> --log
```

**Resultado esperado**: El flujo de trabajo se completa correctamente y llegan las notificaciones de Slack (y correo si esta configurado).

---

## ⚠️ Problemas comunes y soluciones

```json
{
  "title": "⚠️ Solucion de problemas",
  "questions": [{
    "id": "trouble",
    "prompt": "Ha encontrado algun problema?",
    "options": [
      {"id": "trouble_1", "label": "Fallo en la obtencion del feed RSS"},
      {"id": "trouble_2", "label": "Error en el Slack Webhook"},
      {"id": "trouble_3", "label": "Fallo en el envio de correo"},
      {"id": "trouble_4", "label": "El horario cron no funciona"}
    ]
  }]
}
```

### Problema 1: "Fallo en la obtencion del feed RSS"
**Causa**: La URL del feed ha cambiado o fue descontinuada, o se produce un timeout.
**Solucion**:
```text
Abra las URLs de RSS_FEEDS en el navegador y verifique que devuelven XML. Si hay timeout, aumente el valor de timeout a 60.
```

### Problema 2: "Error en el Slack Webhook"
**Causa**: La URL del Webhook es invalida o el Secret no esta configurado correctamente.
**Solucion**:
```text
Pruebe directamente desde local con: curl -X POST -H "Content-Type: application/json" -d '{"text":"prueba"}' $SLACK_WEBHOOK. Si obtiene 404, vuelva a crear el Webhook.
```

### Problema 3: "Fallo en el envio de correo"
**Causa**: La contrasena de aplicacion de Gmail no esta configurada o la verificacion en dos pasos esta desactivada.
**Solucion**:
```text
Genere una contrasena de aplicacion en Gmail (Cuenta de Google → Seguridad → Contrasenas de aplicacion). La verificacion en dos pasos debe estar activada.
```

### Problema 4: "El horario cron no funciona"
**Causa**: Los cron de GitHub Actions solo funcionan en la rama por defecto. Ademas, se desactivan si el repositorio no tiene actividad durante mas de 60 dias.
**Solucion**:
```text
Verifique que el archivo de flujo de trabajo esta fusionado en la rama main. Primero confirme que la ejecucion manual con workflow_dispatch funciona correctamente.
```

---

## ✅ Punto de control

- [ ] `tools/fetch_news.py` obtiene noticias correctamente
- [ ] Los datos se guardan en `output/news_digest.json`
- [ ] Se pueden enviar notificaciones via Slack Webhook (si esta configurado)
- [ ] `.github/workflows/news-digest.yml` esta creado
- [ ] `gh workflow run` ejecuta correctamente de forma manual

---

## 📋 Vista previa de entregables

**Archivos creados:**
```text
tools/
└── fetch_news.py          # Script de obtencion y distribucion de noticias

.github/workflows/
└── news-digest.yml        # Flujo de trabajo de distribucion periodica

output/
└── news_digest.json       # Datos de noticias (generados en ejecucion)
```

---

## ➡️ Siguientes pasos

```json
{
  "title": "➡️ Siguientes pasos",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_auto", "label": "Avanzar a la Leccion 11-4 (Llamar a AI CLI desde GitHub Actions) → /start-11-4"},
      {"id": "review_module", "label": "Revisar los entregables de esta leccion"},
      {"id": "finish", "label": "Terminar por hoy"}
    ]
  }]
}
```
