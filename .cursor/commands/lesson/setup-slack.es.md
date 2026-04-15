---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Acceso de administrador a un espacio de trabajo de Slack"]
level: "beginner"
tags: ["setup", "slack", "api"]
---

# Configuración de Slack API

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-slack` para mostrar el progreso
2. **Este paso es opcional.** Puede omitirlo si no va a usar la integración con Slack
3. Detectar automáticamente el token existente:
   - Verificar si `SLACK_USER_TOKEN` existe en `.env` o en el almacén de credenciales
   - Si existe, verificar su validez con `auth.test` de la API de Slack. Si es válido, preguntar "La configuración de Slack ya está completa. ¿Desea omitirla?"
4. Si omite: Ejecutar `uv run python tools/setup_progress.py skip setup-slack --reason 'Usuario omitió'`

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Crear una Slack App, obtener un User Token, guardarlo de forma segura y habilitar las funciones de búsqueda y obtención de mensajes de Slack |
| Duración | ~15 minutos |
| Requisitos previos | Acceso de administrador al espacio de trabajo de Slack (o permiso para agregar Apps), navegador disponible |
| Nivel de operación | Sin entrada de comandos CLI (todo lo ejecuta la IA automáticamente + solo operaciones GUI) |

**Flujo de la sesión:**
1. Abrir la página de administración de Slack App (la IA abre el navegador automáticamente)
2. Crear una nueva Slack App (hacer clic en botones en pantalla)
3. Configurar User Token Scopes (agregar los permisos necesarios)
4. Instalar en el espacio de trabajo (hacer clic en el botón de permitir)
5. Guardar el User Token de forma segura (usando credential_manager)
6. Prueba de operación (la IA la ejecuta automáticamente)

> **Consejo**: Si la IA deja de responder a mitad del proceso, escriba "por favor continúa" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "chrome", "label": "Automatizar operaciones del navegador con /chrome"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "no_slack", "label": "No tengo un espacio de trabajo de Slack"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Después de abrir el navegador en Step 1, seguir la sección "Automatización con integración Chrome")
(check_prereq -> Indicar: "Está listo si ha iniciado sesión en un espacio de trabajo de Slack y tiene permiso para agregar Apps. Si no tiene permiso, consulte con el administrador del espacio de trabajo")
(no_slack -> Indicar: "Puede crear un espacio de trabajo de Slack de forma gratuita. Cree un espacio de trabajo de prueba en https://slack.com/create y luego reinicie esta configuración")
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Abrir la página de administración de Slack App

**Lo que hace la IA:**
1. Detectar automáticamente el sistema operativo (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://api.slack.com/apps
# Windows:
start https://api.slack.com/apps
# Linux:
xdg-open https://api.slack.com/apps
```

**Una vez que se abra el navegador, mostrar el siguiente AskQuestion:**

```json
{
  "title": "Step 1: Crear una Slack App",
  "questions": [{
    "id": "app_create",
    "prompt": "La página de administración de Slack App se abrió en su navegador. Siga estos pasos para crear una nueva App:\n\n1. Haga clic en el botón 'Create New App' en la esquina superior derecha\n2. Seleccione 'From scratch'\n3. Ingrese 'AIAgent Bootcamp' como nombre de la App\n4. Seleccione su espacio de trabajo en 'Pick a workspace'\n5. Haga clic en el botón 'Create App'\n\n¿Pudo crear la App?",
    "options": [
      {"id": "created", "label": "¡App creada!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "no_create_button", "label": "No encuentro el botón 'Create New App'"},
      {"id": "no_workspace", "label": "Mi espacio de trabajo no aparece"},
      {"id": "permission_error", "label": "Obtuve un error de permisos"}
    ]
  }]
}
```

(created -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://api.slack.com/apps")
(no_create_button -> Indicar: "Es posible que no haya iniciado sesión en Slack. Primero, haga clic en 'Sign in' en la esquina superior derecha para iniciar sesión con su cuenta de Slack")
(no_workspace -> Indicar: "Recargue la página mientras está conectado a su espacio de trabajo. Si aún no aparece, es posible que necesite crear un nuevo espacio de trabajo")
(permission_error -> Indicar: "El administrador del espacio de trabajo puede haber restringido la adición de Apps. Pida al administrador que permita agregar una Slack App llamada 'AIAgent Bootcamp'. Alternativamente, cree un espacio de trabajo de prueba gratuito en https://slack.com/create")

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisitos previos:** La extensión "Claude in Chrome" (v1.0.36+) está instalada en Chrome, y se inició con `claude --chrome` o se ejecutó `/chrome` dentro de la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://api.slack.com/apps en el navegador
2. Usar la integración Chrome para ejecutar secuencialmente:
   - Hacer clic en "Create New App"
   - Seleccionar "From scratch"
   - Ingresar "AIAgent Bootcamp" como nombre de la App
   - Seleccionar un espacio de trabajo en "Pick a workspace"
   - Hacer clic en "Create App"
   - Hacer clic en "OAuth & Permissions" en el menú izquierdo
   - En la sección "User Token Scopes", hacer clic en "Add an OAuth Scope" y agregar estos 4 scopes uno por uno: channels:history, channels:read, chat:write, users:read
   - Hacer clic en "Install to Workspace" en la parte superior de la página
   - Hacer clic en "Allow" en la pantalla de confirmación de permisos
3. Una vez que aparezca el User OAuth Token (xoxp-...), indicar al usuario: "Haga clic en el botón Copy junto al token para copiarlo"
4. Ir al Step 4

**Nota:** No leer el valor del token desde la pantalla del navegador. El usuario lo copia manualmente.

Si la integración Chrome no está disponible, siga los pasos manuales en los Steps 2-3 a continuación.

---

## Step 2: Configurar User Token Scopes

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Configurar User Token Scopes",
  "questions": [{
    "id": "scope_setup",
    "prompt": "La página de configuración de la App está visible. Siga estos pasos para configurar los User Token Scopes:\n\n1. Haga clic en 'OAuth & Permissions' en el menú izquierdo\n2. Desplácese hacia abajo para encontrar la sección 'Scopes'\n3. Haga clic en 'Add an OAuth Scope' bajo 'User Token Scopes'\n4. Agregue los siguientes 4 scopes uno por uno:\n\n   - channels:history (leer mensajes del canal)\n   - channels:read (leer información del canal)\n   - chat:write (enviar mensajes)\n   - users:read (leer información de usuarios)\n\n¿Agregó los 4 scopes?",
    "options": [
      {"id": "scopes_added", "label": "¡Agregué los 4 scopes!"},
      {"id": "cant_find_oauth", "label": "No encuentro 'OAuth & Permissions'"},
      {"id": "cant_find_scopes", "label": "No encuentro 'User Token Scopes'"},
      {"id": "scope_not_found", "label": "El scope que quiero agregar no aparece como opción"},
      {"id": "what_are_scopes", "label": "¿Qué son los scopes?"}
    ]
  }]
}
```

(scopes_added -> Ir al Step 3)
(cant_find_oauth -> Indicar: "Revise el menú lateral izquierdo. 'OAuth & Permissions' está bajo la sección 'Features'. Si no puede ver la barra lateral, intente ampliar la ventana del navegador")
(cant_find_scopes -> Indicar: "Desplácese hacia abajo en la página. La sección 'Scopes' está debajo de la sección 'OAuth Tokens for Your Workspace'. Busque 'User Token Scopes' dentro de ella. Nota: NO es 'Bot Token Scopes'")
(scope_not_found -> Indicar: "Ingrese el nombre del scope exactamente. Escribir en el campo de entrada filtra las sugerencias. Por ejemplo, escribir 'channels' mostrará channels:history y channels:read como opciones")
(what_are_scopes -> Explicar: "Los scopes definen el rango de operaciones que su App tiene permitido realizar. Los 4 que estamos agregando son:\n- channels:history = Permiso para leer mensajes pasados en canales\n- channels:read = Permiso para ver la lista de canales\n- chat:write = Permiso para publicar mensajes como la App\n- users:read = Permiso para ver información de miembros del espacio de trabajo\nEstos son los permisos mínimos necesarios para las funciones de búsqueda y gestión de tareas de Slack")

---

## Step 3: Instalar en el espacio de trabajo

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Instalar en el espacio de trabajo",
  "questions": [{
    "id": "install_app",
    "prompt": "Una vez completada la configuración de scopes, instale la App en su espacio de trabajo:\n\n1. Desplácese hacia arriba para encontrar la sección 'OAuth Tokens for Your Workspace'\n2. Haga clic en el botón 'Install to Workspace'\n   (También está bien si el botón dice 'Reinstall to Workspace')\n3. Haga clic en 'Allow' en la pantalla de confirmación de permisos\n4. Aparecerá el 'User OAuth Token' (una cadena que comienza con xoxp-)\n5. Haga clic en el botón 'Copy' a la derecha del token\n\n¿Pudo copiar el User OAuth Token?",
    "options": [
      {"id": "token_copied", "label": "¡Token copiado!"},
      {"id": "no_install_button", "label": "No hay botón 'Install to Workspace'"},
      {"id": "allow_denied", "label": "Fue rechazado en la pantalla de 'Allow'"},
      {"id": "no_token", "label": "No se muestra ningún token"}
    ]
  }]
}
```

(token_copied -> Ir al Step 4)
(no_install_button -> Indicar: "El botón de instalación no aparecerá si no se han agregado User Token Scopes. Vuelva al Step 2 y agregue al menos un scope")
(allow_denied -> Indicar: "El administrador del espacio de trabajo puede haber restringido la adición de Apps. Pida aprobación al administrador o cree un espacio de trabajo de prueba propio")
(no_token -> Indicar: "Si la instalación se completó correctamente, el 'User OAuth Token' debería aparecer en la parte superior de la página 'OAuth & Permissions'. Recargue la página y verifique la sección superior")

---

## Step 4: Guardar el token de forma segura

**Nota importante de seguridad:**
No pegue el token en este chat. Lo guardaremos de forma segura en una ventana de terminal separada.

**Lo que la IA ejecuta automáticamente:**
1. Verificar si el paquete `keyring` está instalado
   - Si no está instalado: Ejecutar automáticamente `pip install keyring`
2. Ejecutar `uv run python tools/credential_manager.py status` para verificar el estado actual

**Mensaje para mostrar al usuario:**

```text
Después de copiar el token, siga estos pasos para guardarlo de forma segura:

┌─────────────────────────────────────────────────────────────┐
│ Ejecute el siguiente comando en una ventana de terminal     │
│ separada:                                                   │
│                                                             │
│ Cursor: Ctrl+` (acento grave) para abrir un nuevo terminal  │
│ Claude Code: Abrir una ventana de terminal separada         │
│                                                             │
│ uv run python tools/credential_manager.py store SLACK_USER_TOKEN    │
│                                                             │
│ -> Aparecerá "Enter value for SLACK_USER_TOKEN:"             │
│ -> Pegue el User Token copiado y presione Enter              │
│   (El texto que escribe no se mostrará en pantalla.         │
│    Esto es normal)                                          │
│ -> "Stored SLACK_USER_TOKEN" significa que se guardó          │
└─────────────────────────────────────────────────────────────┘

Una vez guardado, vuelva a este chat y dígame que "terminó".
```

**¿Por qué ejecutarlo en una ventana separada?**
Si maneja el token en este chat de IA, el valor queda en el registro de la conversación.
Al ejecutar `credential_manager.py` en una ventana separada, el valor del token se guarda directamente
en el almacenamiento cifrado del sistema operativo (macOS Keychain / Windows Credential Locker / Linux SecretService),
y nunca aparece en archivos de texto plano ni en registros del chat.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 4: Guardar el token",
  "questions": [{
    "id": "store_status",
    "prompt": "¿Pudo ejecutar el comando en un terminal separado?",
    "options": [
      {"id": "done", "label": "¡Guardado!"},
      {"id": "terminal_help", "label": "No sé cómo abrir un terminal"},
      {"id": "command_error", "label": "El comando dio un error"},
      {"id": "credential_store_unavailable", "label": "El Credential Store no está disponible (respaldo)"},
      {"id": "security_question", "label": "Tengo una pregunta sobre seguridad"}
    ]
  }]
}
```

(done -> Ir al Step 5)
(terminal_help -> Indicar: "Para Cursor: Menú > Terminal > New Terminal, o presione Ctrl+` (Mac: Cmd+`). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra su terminal WSL (Ubuntu), o agregue una pestaña Ubuntu en Windows Terminal. Luego navegue con cd al directorio del proyecto")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `pip install keyring`)
(credential_store_unavailable -> Indicar: "Primero, verifiquemos el estado del almacén con `uv run python tools/credential_manager.py status`". Si realmente no está disponible, proporcionar el respaldo con .env como excepción: guiar para ingresar el token directamente en el archivo .env en un terminal separado, con la nota: "Asegúrese de que .env esté incluido en .gitignore. Cuando el Credential Store esté disponible, migre con `uv run python tools/credential_manager.py migrate` y limpie con `uv run python tools/credential_manager.py cleanup` para eliminar el token en texto plano de .env")
(security_question -> Explicar: "Esta herramienta usa el almacenamiento cifrado integrado del sistema operativo. En macOS usa Keychain, en Windows usa Credential Locker y en Linux usa SecretService (GNOME Keyring, etc.). No se crean archivos de texto plano (.env). El almacenamiento también se bloquea cuando la pantalla está bloqueada, proporcionando protección contra el acceso físico")

---

## Step 5: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Primero ejecutar `credential_manager.py status` para verificar si `SLACK_USER_TOKEN` está guardado en el Credential Store:
   - **Nota**: No mostrar el valor del token en el chat. Solo mostrar salida enmascarada como "Se confirmó que el token está configurado (xoxp-****...)"
   - Comando de verificación de estado: `uv run python tools/credential_manager.py status`

2. Si pasa la verificación básica, enviar una solicitud de prueba real a la API de Slack:
   - Inyectar desde el Credential Store a variables de entorno y ejecutar la llamada API
   - Ejemplo de código de prueba:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     token = os.getenv("SLACK_USER_TOKEN")
     if not token or token == "xoxp-your-user-token":
         print("Error: SLACK_USER_TOKEN no está configurado.")
         sys.exit(1)
     resp = requests.post(
         "https://slack.com/api/auth.test",
         headers={"Authorization": f"Bearer {token}"}
     ).json()
     if resp.get("ok"):
         print(f"¡Conexión exitosa! Espacio de trabajo: {resp['team']} / Nombre del bot: {resp['user']}")
     else:
         print(f"Error: {resp.get('error', 'Error desconocido')}")
     ```
   - Instalar automáticamente los paquetes faltantes (`requests`, `keyring`)

3. Mostrar mensajes según los resultados de la prueba:

**Al tener éxito en la prueba:**
```text
¡La configuración de la API de Slack está completa!

Resultados de la prueba:
  Espacio de trabajo: [nombre del espacio de trabajo]
  Nombre del bot: [nombre del bot]
  Conexión: Normal

Ahora puede usar la búsqueda de Slack (/start-9-1) y la gestión de tareas de Slack (/start-9-2).
```

**AskQuestion en caso de fallo en la prueba:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de la API de Slack. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Intentar la prueba de nuevo"},
      {"id": "recheck_token", "label": "Volver a verificar el token (volver al Step 3)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(recheck_token -> Volver al Step 3)
(show_error -> Mostrar el mensaje de error con causa y solución. Errores comunes: `invalid_auth` = token inválido, `token_revoked` = token revocado, `not_authed` = token no configurado)
(skip_test -> Indicar: "Prueba de API omitida. Puede verificar más tarde con /check-setup")

---

## Complemento: Invitar al bot a un canal

**Después de una prueba exitosa, la IA proporciona la siguiente guía:**

Para que la Slack App lea mensajes, el bot debe ser invitado al canal objetivo.

**Pasos (realizados en la aplicación de Slack):**
1. Abrir la aplicación de Slack
2. Navegar al canal donde desea leer mensajes
3. Hacer clic en el nombre del canal para abrir la configuración
4. Hacer clic en la pestaña "Integraciones"
5. Hacer clic en "Agregar una aplicación"
6. Seleccionar "AIAgent Bootcamp" y agregarla

Alternativamente, también puede enviar el mensaje `/invite @AIAgent Bootcamp` en el canal.

---

## Solución de problemas comunes

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda",
    "options": [
      {"id": "trouble_invalid", "label": "Error 'invalid_auth'"},
      {"id": "trouble_missing_scope", "label": "Error 'missing_scope'"},
      {"id": "trouble_not_in_channel", "label": "Error 'not_in_channel'"},
      {"id": "trouble_admin", "label": "Se requiere aprobación del administrador"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error "invalid_auth"
**Causa**: El User Token no se copió correctamente o es inválido
**Lo que hace la IA**:
1. Verificar el estado del Credential Store con `uv run python tools/credential_manager.py status` (solo informar si comienza con `xoxp-`, no mostrar el valor)
2. Verificar automáticamente si hay espacios extra, saltos de línea o comillas
3. Si se encuentra un problema, sugerir volver a guardar. Si no, indicar: "Regenere el token desde la página de configuración de Slack App"

### Problema 2: Error "missing_scope"
**Causa**: No se ha agregado el User Token Scope requerido
**Indicación de la IA**: "En la página de configuración de Slack App, vaya a 'OAuth & Permissions' -> 'User Token Scopes' y verifique que todos estos scopes estén agregados: channels:history, channels:read, chat:write, users:read. Después de agregar scopes, necesita hacer clic en 'Reinstall to Workspace' para reinstalar"

### Problema 3: Error "not_in_channel"
**Causa**: El bot no ha sido invitado al canal objetivo
**Indicación de la IA**: "Abra el canal objetivo en la aplicación de Slack, haga clic en el nombre del canal -> 'Integraciones' -> 'Agregar una aplicación' y agregue 'AIAgent Bootcamp'"

### Problema 4: Se requiere aprobación del administrador
**Causa**: La configuración del espacio de trabajo restringe la adición de Apps
**Indicación de la IA**: "Pida al administrador del espacio de trabajo que apruebe la adición de la Slack App. Si lo necesita urgentemente, puede crear un espacio de trabajo de prueba gratuito en https://slack.com/create para practicar"

### Problema 5: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error y compararlo con los códigos de error de la API de Slack para proporcionar la causa y la solución

---

## Punto de verificación
- [ ] Creó la Slack App "AIAgent Bootcamp"
- [ ] Agregó 4 scopes a User Token Scopes (channels:history, channels:read, chat:write, users:read)
- [ ] Instaló la App en el espacio de trabajo
- [ ] SLACK_USER_TOKEN está guardado en el Credential Store (verificar con `uv run python tools/credential_manager.py status`)
- [ ] La prueba de API fue exitosa (se mostró el nombre del espacio de trabajo y el nombre del bot)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de la API de Slack está completa! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "setup_gemini", "label": "Configurar también la API de Gemini (/setup-gemini)"},
      {"id": "try_slack_search", "label": "Probar la búsqueda de Slack (/start-9-1)"},
      {"id": "try_slack_task", "label": "Probar la gestión de tareas de Slack (/start-9-2)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- setup_gemini -> Guiar a /setup-gemini
- try_slack_search -> Guiar a /start-9-1
- try_slack_task -> Guiar a /start-9-2
- back_to_setup -> Mostrar lista de lecciones de configuración
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-slack` para actualizar el progreso
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "A continuación, instalemos extensiones con `/setup-extensions`"
