---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
duration: "~25 min"
prerequisites: ["start-9-2"]
level: "intermediate"
tags: ["slack", "api", "message", "reply", "post"]
---

# 🎓 Lesson 9-3: Envio de respuestas

## 📍 Lo que hara en esta sesion

**Lesson 9-3: Slack API — Envio de mensajes y obtencion de informacion de usuarios**!

| Elemento | Contenido |
|------|------|
| Objetivo | Enviar mensajes y respuestas en hilos con chat.postMessage, y obtener informacion de usuarios con users.list / users.info |
| Duracion | ~25 min |
| Habilidades utilizadas | curl, Slack Web API, generacion de texto con IA |
| Requisitos previos | Lesson 9-2 completada (capacidad de obtener mensajes e hilos) |
| Pagina del curso | [Module 9: Slack](https://ai-agent.camp/es/course/module-9) como referencia paralela |

**Flujo de la sesion:**
1. Enviar un mensaje al canal con `chat.postMessage` (flujo de confirmacion dry-run)
2. Enviar una respuesta en hilo especificando `thread_ts`
3. Enviar un mensaje con mencion
4. Obtener informacion de usuarios con `users.list` / `users.info` (resolucion de ID para menciones)
5. Ejercicio practico: Crear y enviar un resumen de un hilo como respuesta

Al final de esta sesion, podra enviar mensajes y respuestas en hilos con la API de Slack, y tambien obtener informacion de usuarios.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

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
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Establecer el token como variable de entorno e ir al Step 1)
(check_prereq → Ejecutar `auth.test` para verificar la conexion. Tambien verificar el scope `chat:write`. Si falla, dirigir a Lesson 9-1)
(view_html → Mostrar la ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

**Contenido que la IA ejecuta automaticamente al iniciar la sesion:**
```bash
export SLACK_USER_TOKEN=$(uv run python tools/credential_manager.py get SLACK_USER_TOKEN)
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Conexion OK: {d[\"team\"]} / {d[\"user\"]} (user_id: {d[\"user_id\"]})')" 2>/dev/null || echo "Conexion fallida: Complete primero la Lesson 9-1"
```

---

## 🚀 Step 1: Enviar mensaje con chat.postMessage (flujo de confirmacion dry-run)

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Envio de mensaje (con dry-run)",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Si elige practice — Contenido que la IA ejecuta:**

**Importante**: El envio de mensajes es una operacion irreversible, por lo que siempre se realiza un dry-run (vista previa).

1. Verificar el canal de destino:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=20" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    print(f'{ch[\"id\"]} : #{ch[\"name\"]}')"
```

2. **dry-run**: Confirmar el contenido del envio con el usuario:
```text
Se enviara el siguiente contenido. Si no hay problemas, escriba "OK para enviar".

Destino: #nombre-del-canal (CHANNEL_ID)
Mensaje: Publicacion de prueba (aprendiendo Slack API)
```

3. Enviar despues de la confirmacion del usuario:
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"Publicacion de prueba (aprendiendo Slack API)"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Resultado esperado**:
```json
{
    "ok": true,
    "channel": "C0XXXXXXX",
    "ts": "1713075000.123456",
    "message": {
        "text": "Publicacion de prueba (aprendiendo Slack API)",
        "user": "U0XXXXXXX",
        "ts": "1713075000.123456"
    }
}
```

**Scope de OAuth requerido**: `chat:write`

---

## 🚀 Step 2: Enviar respuesta en hilo especificando thread_ts

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Envio de respuesta en hilo",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Si elige practice — Contenido que la IA ejecuta:**

1. Verificar el hilo de destino (usar el ts del mensaje publicado en Step 1):
```bash
# Obtener mensajes existentes con hilos
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=5" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    has_thread = '(tiene hilo)' if msg.get('reply_count', 0) > 0 else ''
    print(f'ts={msg[\"ts\"]} {has_thread}: {msg.get(\"text\", \"\")[:60]}')"
```

2. **dry-run** → Enviar respuesta en hilo despues de la confirmacion del usuario:
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"Prueba de respuesta en hilo","thread_ts":"PARENT_TS"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Puntos clave**:
- Especificar el `ts` del mensaje padre en `thread_ts` convierte el mensaje en una respuesta en hilo
- Agregar `reply_broadcast: true` muestra la respuesta del hilo tambien en el canal (equivalente a "Publicar tambien en el canal")

---

## 🚀 Step 3: Envio de mensaje con mencion

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Envio de mensaje con mencion",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Si elige practice — Contenido que la IA ejecuta:**

Las menciones se insertan con el ID de usuario en formato `<@USER_ID>`:
```bash
# Verificar su propio ID de usuario
MY_USER_ID=$(curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['user_id'])")
echo "Mi ID de usuario: $MY_USER_ID"
```

```bash
# Envio de mensaje con mencion (a uno mismo — para pruebas)
# Ejecutar despues de la confirmacion dry-run
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"CHANNEL_ID\",\"text\":\"<@${MY_USER_ID}> Prueba de mencion\"}" \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Sintaxis de menciones:**
| Sintaxis | Destino |
|------|------|
| `<@U0XXXXXXX>` | Usuario especifico |
| `<!channel>` | Todos en el canal |
| `<!here>` | Todos los miembros en linea |
| `<!subteam^S0XXXXXXX>` | Grupo de usuarios |

**Nota**: `<!channel>` y `<!here>` envian notificaciones a muchas personas, por lo que no deben usarse con fines de prueba.

---

## 🚀 Step 4: Obtener informacion de usuarios con users.list / users.info

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Obtencion de informacion de usuarios",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Si elige practice — Contenido que la IA ejecuta:**

1. Obtener la lista de usuarios del workspace con `users.list`:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.list?limit=50" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('members', []):
    if u.get('deleted') or u.get('is_bot'):
        continue
    print(f'{u[\"id\"]} : {u.get(\"real_name\", \"Desconocido\")} (@{u[\"name\"]}')"
```

2. Obtener detalles de un usuario especifico con `users.info`:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.info?user=U0XXXXXXX" \
  | python3 -c "
import sys, json
u = json.load(sys.stdin)['user']
print(f'Nombre: {u.get(\"real_name\", \"Desconocido\")}')
print(f'Nombre para mostrar: {u.get(\"profile\", {}).get(\"display_name\", \"No configurado\")}')
print(f'Correo: {u.get(\"profile\", {}).get(\"email\", \"No publico\")}')
print(f'Estado: {u.get(\"profile\", {}).get(\"status_text\", \"Ninguno\")}')
print(f'Zona horaria: {u.get(\"tz\", \"Desconocida\")}')"
```

**Campos principales:**
| Campo | Descripcion |
|-----------|------|
| `id` | ID de usuario (usado para menciones) |
| `name` | Nombre de usuario (el nombre despues de @) |
| `real_name` | Nombre real |
| `profile.display_name` | Nombre para mostrar |
| `profile.email` | Correo electronico (requiere scope `users:read.email`) |
| `tz` | Zona horaria |
| `is_bot` | Si es un bot o no |

**Scope de OAuth requerido**: `users:read`

---

## 🚀 Step 5: Ejercicio practico — Enviar un resumen del hilo como respuesta

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Ejercicio practico — Responder con resumen del hilo",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Si elige practice — Se ejecuta el siguiente flujo de trabajo:**

En este ejercicio se combinan la obtencion de mensajes aprendida en Lesson 9-2 con el envio de esta leccion.

1. **Obtener el hilo**: Obtener el hilo con `conversations.replies`
2. **Resolver IDs de usuario**: Convertir a nombres de usuario con `users.info`
3. **Resumen con IA**: Hacer que la IA resuma el contenido del hilo obtenido
4. **dry-run**: Mostrar el texto del resumen y confirmar con el usuario
5. **Respuesta en hilo**: Enviar el resumen como respuesta con `chat.postMessage`

```bash
# 1. Obtener el hilo y guardar en archivo
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.replies?channel=CHANNEL_ID&ts=THREAD_TS" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    ts = datetime.datetime.fromtimestamp(float(msg['ts']))
    print(f'[{ts.strftime(\"%m/%d %H:%M\")}] {msg.get(\"user\",\"?\")} : {msg.get(\"text\",\"\")}')" \
  > ~/ai-agent-camp/data/slack_thread_for_summary.txt
```

```text
# 2. Solicitar resumen a la IA
Lea ~/ai-agent-camp/data/slack_thread_for_summary.txt y
resuma el contenido de este hilo en 3-5 lineas.
El resumen debe comenzar con "Resumen de este hilo:".
```

```bash
# 3. Despues de la confirmacion dry-run, enviar el resumen como respuesta en hilo
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"Resumen de este hilo:\n(texto del resumen generado por IA)","thread_ts":"THREAD_TS"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Resultado esperado**: El resumen se publica como respuesta en el hilo.

---

## ⚠️ Problemas comunes y soluciones

**Configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "not_authed / missing_scope en chat.postMessage"},
      {"id": "trouble_2", "label": "El mensaje se envio pero no se muestra"},
      {"id": "trouble_3", "label": "La mencion no funciona (se muestra como texto)"},
      {"id": "trouble_4", "label": "Los mensajes en japones se muestran con caracteres incorrectos"}
    ]
  }]
}
```

### Problema 1: "not_authed / missing_scope"
**Causa**: El scope `chat:write` no esta configurado
**Solucion**:
1. Abrir la aplicacion en https://api.slack.com/apps
2. En OAuth & Permissions → User Token Scopes, agregar `chat:write`
3. Reinstalar en el workspace
4. Guardar el nuevo token con `credential_manager.py store SLACK_USER_TOKEN`

### Problema 2: "El mensaje se envio pero no se muestra"
**Causa**: Se envio a otro canal, o se publico dentro de un hilo
**Solucion**:
```bash
# Verificar el channel y ts de la respuesta
# Comprobar si channel coincide con lo esperado
# Verificar si thread_ts esta incluido (si se convirtio en respuesta de hilo sin intencion)
```

### Problema 3: "La mencion se muestra como texto"
**Causa**: Se escribio como texto `@username`
**Solucion**: Las menciones deben usar el formato `<@U0XXXXXXX>` con el ID de usuario. `@nombre` no funciona como mencion.
```bash
# Buscar ID de usuario
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.list?limit=100" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('members', []):
    if not u.get('deleted') and not u.get('is_bot'):
        print(f'<@{u[\"id\"]}> → {u.get(\"real_name\", u[\"name\"])}')"
```

### Problema 4: "Los mensajes en japones se muestran con caracteres incorrectos"
**Causa**: Problema de codificacion JSON
**Solucion**: Especificar `Content-Type: application/json; charset=utf-8` y enviar con cuerpo JSON. Con `application/x-www-form-urlencoded` es necesario codificar los caracteres en URL.

---

## ✅ Punto de control
- [ ] Se envio un mensaje al canal con `chat.postMessage`
- [ ] Se envio una respuesta en hilo especificando `thread_ts`
- [ ] Se envio un mensaje con mencion
- [ ] Se obtuvo informacion de usuarios con `users.list` / `users.info`
- [ ] Se creo un resumen del hilo y se envio como respuesta

---

## 📋 Vista previa de entregables

Los entregables de esta leccion son la salida del terminal y las publicaciones en Slack.

### Salida esperada
```text
# Resultado de chat.postMessage
ok: true
channel: C0XXXXXXX
ts: 1713075000.123456

# Resultado de users.list
U0ABC1234 : Juan Garcia (@juan.garcia)
U0DEF5678 : Maria Lopez (@maria.lopez)
U0GHI9012 : Carlos Rodriguez (@carlos.rodriguez)

# Visualizacion en Slack
Se publica "Publicacion de prueba (aprendiendo Slack API)" en #general
Se publica el resumen como respuesta en el hilo
```

---

## ➡️ Siguientes pasos

Se han completado todas las operaciones basicas de la API de Slack (obtencion de canales, obtencion de mensajes, envio de mensajes, obtencion de informacion de usuarios). Avancemos al siguiente modulo.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-10-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-10-1
- finish → Finalizar
