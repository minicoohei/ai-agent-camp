---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Navegador disponible", "Tener correo electrónico o cuenta de Google/GitHub"]
level: "beginner"
tags: ["setup", "elevenlabs", "api", "tts", "voice"]
nonInteractiveMode: deferred
---
# Configuración de la API de ElevenLabs

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-elevenlabs` para mostrar el progreso
2. Detectar automáticamente la clave de API existente:
   - Ejecutar `uv run python tools/credential_manager.py status`
   - Si ELEVENLABS_API_KEY (o ELEVEN_API_KEY) ya está configurada, puede ejecutar solo el Step 4 (prueba de API) y marcarlo como completado
   - Si existe una clave en texto plano en `.env`, sugerir la migración al almacén de credenciales

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Obtener una clave de API de ElevenLabs y guardarla en el Almacén de credenciales para poder usar las funciones de texto a voz (TTS) y síntesis de voz |
| Duración | ~10 minutos |
| Requisitos previos | Una dirección de correo electrónico o cuenta de Google/GitHub, y un navegador disponible |
| Nivel de operación | No se necesitan comandos CLI (todo lo ejecuta automáticamente la IA + solo operaciones de GUI) |

**Casos de uso:**
ElevenLabs es un servicio de síntesis de voz con IA (TTS). Admite texto a voz, clonación de voz y síntesis de voz multilingüe, utilizado para generar narraciones de video y más.

**Sobre los costos:**
El plan gratuito permite hasta 10.000 caracteres al mes. Esto es más que suficiente para el uso a nivel de curso.

**Flujo de la sesión:**
1. Abrir ElevenLabs en el navegador (la IA abre el navegador automáticamente)
2. Crear una cuenta / iniciar sesión (registrarse mediante autenticación de Google/GitHub)
3. Obtener su clave de API (solo copiarla desde la página de configuración)
4. Guardar en el Almacén de credenciales (ejecutar un comando en una terminal separada)
5. Prueba de funcionalidad (la IA lo ejecuta automáticamente)

> **Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación antes de la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está preparado/a?",
    "options": [
      {"id": "ready", "label": "¡Preparado/a! Comencemos"},
      {"id": "chrome", "label": "Automatizar operaciones del navegador con /chrome"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Después de abrir el navegador en el Step 1, seguir la sección "Automatización con integración Chrome" para la ejecución automática)
(check_prereq -> Indicar: "Está listo/a si tiene una dirección de correo electrónico o una cuenta de Google/GitHub. El plan gratuito permite hasta 10.000 caracteres al mes.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Abrir ElevenLabs en el navegador

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://elevenlabs.io
# Windows:
start https://elevenlabs.io
# Linux:
xdg-open https://elevenlabs.io
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 1: Registrarse / Iniciar sesión en ElevenLabs",
  "questions": [{
    "id": "signup_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para crear su cuenta:\n\n1. Haga clic en 'Sign up' en la parte superior derecha (o 'Log in' si ya tiene cuenta)\n2. Regístrese con autenticación de Google / GitHub, o con su dirección de correo electrónico\n3. Una vez que haya iniciado sesión, continúe con el siguiente paso\n\n¿Ha iniciado sesión?",
    "options": [
      {"id": "logged_in", "label": "¡He iniciado sesión!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "signup_issue", "label": "Tengo problemas para registrarme"},
      {"id": "already_have_key", "label": "Ya tengo una clave de API"}
    ]
  }]
}
```

(logged_in -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://elevenlabs.io")
(signup_issue -> Indicar: "La autenticación de Google es la más fácil. Haga clic en Sign up en la parte superior derecha -> Continue with Google. Si no funciona, intente registrarse con su dirección de correo electrónico.")
(already_have_key -> Saltar al Step 3)

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisito previo:** La extensión "Claude in Chrome" (v1.0.36+) debe estar instalada en Chrome, y debe haber iniciado con `claude --chrome` o ejecutado `/chrome` en la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://elevenlabs.io en el navegador
2. Usar la integración Chrome para realizar las siguientes operaciones en orden:
   - Hacer clic en "Sign up" o "Log in"
   - Autenticarse con Google, GitHub o correo electrónico (esperar la acción del usuario)
   - Después de iniciar sesión, navegar a https://elevenlabs.io/app/settings/api-keys
   - Si hay una clave existente, dejarla como está; de lo contrario hacer clic en "Create API Key"
3. Una vez que se muestre la clave de API, indicar al usuario "Haga clic en el botón de copiar junto a la clave de API para copiarla"
4. Ir al Step 3

**Nota:** No leer el valor de la clave de API desde la pantalla del navegador. El usuario la copia manualmente.

Si la integración Chrome no está disponible, siga los pasos a continuación manualmente.

---

## Step 2: Obtener su clave de API

**Lo que hace la IA:**
1. Abrir la página de claves de API en el navegador:

```bash
# Mac:
open https://elevenlabs.io/app/settings/api-keys
# Windows:
start https://elevenlabs.io/app/settings/api-keys
# Linux:
xdg-open https://elevenlabs.io/app/settings/api-keys
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 2: Obtener su clave de API",
  "questions": [{
    "id": "key_status",
    "prompt": "¿Se abrió la página de configuración de claves de API? Siga estos pasos para obtener su clave de API:\n\n1. Confirme que se muestra la página de API Keys\n2. Si hay una clave existente, haga clic en el icono de copiar\n3. Si no, haga clic en 'Create API Key' para crear una nueva\n4. Copie la clave de API mostrada\n\n¿Copió la clave de API?",
    "options": [
      {"id": "copied", "label": "¡Copié la clave de API!"},
      {"id": "page_not_found", "label": "No encuentro la página de configuración"},
      {"id": "no_create_button", "label": "No encuentro el botón 'Create API Key'"},
      {"id": "need_help", "label": "Necesito otra ayuda"}
    ]
  }]
}
```

(copied -> Ir al Step 3)
(page_not_found -> Indicar: "Después de iniciar sesión, haga clic en el icono de perfil en la parte inferior izquierda -> Profile + API key. O abra esta URL directamente: https://elevenlabs.io/app/settings/api-keys")
(no_create_button -> Indicar: "Espere a que la página se cargue completamente. Si se muestran claves existentes en la sección de API Keys, haga clic en el icono de copiar junto a la clave.")
(need_help -> Recopilar detalles del error y asistir individualmente)

---

## Step 3: Guardar la clave de API de forma segura

**Nota importante de seguridad:**
No pegue la clave de API en este chat. La guardaremos de forma segura en una ventana de terminal separada.

**Lo que la IA ejecuta automáticamente:**
1. Verificar si el paquete `keyring` está instalado
   - Si no está instalado: ejecutar automáticamente `uv add keyring`
2. Ejecutar `uv run python tools/credential_manager.py status` para verificar el estado actual

**Mensaje para mostrar al usuario:**

```text
Una vez que haya copiado la clave de API, siga estos pasos para guardarla de forma segura:

┌──────────────────────────────────────────────────────────────────┐
│ Ejecute los siguientes comandos en una ventana de terminal       │
│ separada:                                                        │
│                                                                  │
│ Cursor: Ctrl+` (acento grave) para abrir una nueva terminal      │
│ Claude Code: Abra una ventana de terminal separada               │
│                                                                  │
│ (1) Guardar con el nombre de clave principal:                    │
│ uv run python tools/credential_manager.py store ELEVENLABS_API_KEY      │
│                                                                  │
│ → Se mostrará "Enter value for ELEVENLABS_API_KEY:"              │
│ → Pegue la clave de API copiada y presione Enter                 │
│   (Los caracteres que escriba no se mostrarán en pantalla.       │
│    Esto es normal.)                                              │
│ → "Stored ELEVENLABS_API_KEY" significa que se guardó            │
│   exitosamente                                                   │
│                                                                  │
│ (2) También guardar con el alias (algún código usa este nombre): │
│ uv run python tools/credential_manager.py store ELEVEN_API_KEY          │
│                                                                  │
│ → Pegue la misma clave de API y presione Enter                   │
│ → "Stored ELEVEN_API_KEY" significa que está listo               │
└──────────────────────────────────────────────────────────────────┘

Una vez que ambos guardados estén completos, regrese a este chat y diga "listo".
```

**Por qué ejecutar en una ventana separada:**
Si maneja claves de API en el chat de IA, los valores quedarán en el registro de la conversación.
Al ejecutar `credential_manager.py` en una ventana separada, los valores de las claves se almacenan directamente
en el almacenamiento cifrado del SO (macOS Keychain / Windows Credential Locker / Linux SecretService),
y nunca se almacenan en archivos de texto plano ni en registros de chat.

**Por qué guardar con dos nombres de clave:**
El SDK oficial de ElevenLabs y el código de ejemplo a veces usan `ELEVEN_API_KEY`.
Al guardar el mismo valor bajo `ELEVENLABS_API_KEY` y `ELEVEN_API_KEY`,
cualquier código que haga referencia a cualquiera de los nombres funcionará correctamente.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Guardar la clave de API",
  "questions": [{
    "id": "store_status",
    "prompt": "¿Ejecutó ambos comandos en una terminal separada?",
    "options": [
      {"id": "done", "label": "¡Guardé ambos!"},
      {"id": "one_done", "label": "Solo guardé el primero"},
      {"id": "terminal_help", "label": "No sé cómo abrir una terminal"},
      {"id": "command_error", "label": "Obtuve un error con el comando"},
      {"id": "security_question", "label": "Tengo una pregunta sobre seguridad"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(one_done -> Indicar: "Ejecute también el segundo: `uv run python tools/credential_manager.py store ELEVEN_API_KEY` -> Pegue la misma clave de API.")
(terminal_help -> Indicar: "Para Cursor: Menú en la parte superior > Terminal > New Terminal, o presione Ctrl+acento grave (Cmd+acento grave en Mac). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra su terminal WSL (Ubuntu), o agregue una pestaña Ubuntu en Windows Terminal. Luego navegue con cd al directorio del proyecto.")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `uv add keyring`)
(security_question -> Explicar: "Esta herramienta usa el almacenamiento cifrado estándar del SO. En macOS usa Keychain, en Windows usa Credential Locker y en Linux usa SecretService (GNOME Keyring, etc.). No se crean archivos de texto plano (.env). El almacenamiento también se bloquea cuando la pantalla está bloqueada, proporcionando protección contra acceso físico.")

---

## Step 4: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Primero, ejecutar `credential_manager.py status` para verificar si `ELEVENLABS_API_KEY` está guardada en el Almacén de credenciales:
   - **Nota**: No mostrar el valor de la clave de API en absoluto. Solo mostrar "Se confirmó que la clave de API está configurada."
   - Comando de verificación de estado: `uv run python tools/credential_manager.py status`

2. Si la verificación básica pasa, enviar una solicitud de prueba a la API de ElevenLabs:
   - Inyectar variables de entorno desde el Almacén de credenciales y realizar la llamada a la API
   - Ejemplo de código de prueba:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")
     if not key:
         print("Error: ELEVENLABS_API_KEY no está configurada.")
         sys.exit(1)
     resp = requests.get("https://api.elevenlabs.io/v1/models",
         headers={"xi-api-key": key})
     if resp.status_code == 200:
         models = resp.json()
         print(f"¡Conexión exitosa! Modelos disponibles: {len(models)}")
         for m in models[:3]:
             print(f"  - {m.get('name', 'N/A')}")
     else:
         print(f"Error: {resp.status_code}")
         print("Verifique la re-autenticación, regeneración de clave de API o configuración de permisos.")
     ```
   - Instalar automáticamente los paquetes necesarios (`requests`, `keyring`) si no están instalados

3. Mostrar una AskQuestion según el resultado de la prueba:

**En caso de éxito:**
```text
¡La configuración de la API de ElevenLabs se completó!

Resultado de la prueba: Se obtuvo exitosamente la lista de modelos de la API.
Ahora puede usar texto a voz (TTS), síntesis de voz, generación de narración y más.
```

**En caso de fallo — AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de la API. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Ejecutar la prueba de nuevo"},
      {"id": "recheck_key", "label": "Verificar la clave de API de nuevo (volver al Step 2)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(recheck_key -> Volver al Step 2)
(show_error -> Mostrar el mensaje de error e indicar la causa y la solución)
(skip_test -> Indicar: "Se omitió la prueba de la API. Puede verificarla más tarde con /check-setup.")

---

## Problemas comunes y soluciones

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el tipo de problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda a su situación",
    "options": [
      {"id": "trouble_invalid", "label": "Obtengo un error 'Invalid API key'"},
      {"id": "trouble_quota", "label": "Obtengo un error 'Quota exceeded'"},
      {"id": "trouble_package", "label": "Obtengo un error de paquete de Python"},
      {"id": "trouble_voice", "label": "No sé cómo elegir una voz en japonés"},
      {"id": "trouble_cost", "label": "Me preocupan los costos"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error "Invalid API key"
**Causa**: La clave de API no se copió correctamente, o la clave es inválida
**Lo que hace la IA**:
1. Verificar el estado de guardado de `ELEVENLABS_API_KEY` con `credential_manager.py status` (solo mostrar valor enmascarado)
2. Si no está guardada en el Almacén de credenciales, indicar que se vuelva a registrar
3. Si está guardada, volver a ejecutar la prueba de API. Si falla, indicar: "Vuelva a crear la clave en la página de configuración de ElevenLabs: https://elevenlabs.io/app/settings/api-keys"

### Problema 2: Error "Quota exceeded"
**Causa**: Se alcanzó el límite mensual de caracteres del plan gratuito (10.000 caracteres)
**Indicación de la IA**: "El plan gratuito de ElevenLabs permite hasta 10.000 caracteres al mes. Se reinicia al inicio de cada mes, por lo que puede esperar hasta el próximo mes o considerar actualizar a un plan de pago (Starter: $5/mes, 30.000 caracteres). Puede verificar el uso actual en https://elevenlabs.io/app/subscription."

### Problema 3: Error de paquete de Python
**Causa**: Los paquetes necesarios no están instalados
**Lo que hace la IA**: Instalar automáticamente los paquetes faltantes (`uv add requests keyring`)

### Problema 4: Elegir voces en japonés
**Indicación de la IA**: "ElevenLabs ofrece voces multilingües. Para encontrar voces que admitan japonés, filtre por 'Japanese' en https://elevenlabs.io/app/voice-library. Usando el modelo Multilingual v2, la mayoría de las voces pueden leer texto en japonés de forma natural."

### Problema 5: Preocupación por los costos
**Indicación de la IA**: "ElevenLabs tiene un plan gratuito que permite hasta 10.000 caracteres al mes. Para el uso a nivel de curso (unas pocas generaciones de prueba), el nivel gratuito es más que suficiente. Puede verificar su uso en https://elevenlabs.io/app/subscription en cualquier momento. No hay actualización automática a un plan de pago, por lo que no se le cobrará inesperadamente."

### Problema 6: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar al usuario la solución

---

## Punto de control
- [ ] Creó una cuenta de ElevenLabs (o inició sesión)
- [ ] Obtuvo y copió la clave de API desde la página de configuración de claves de API
- [ ] Guardó en el Almacén de credenciales con credential_manager.py store ELEVENLABS_API_KEY
- [ ] También guardó el alias con credential_manager.py store ELEVEN_API_KEY
- [ ] Confirmó el guardado con credential_manager.py status
- [ ] La prueba de API fue exitosa (se obtuvo la lista de modelos)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de la API de ElevenLabs se completó! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_video_narration", "label": "Probar a crear un video de presentación de producto (/start-13-3)"},
      {"id": "try_slide_video", "label": "Probar a crear un video de narración de diapositivas (/start-13-5)"},
      {"id": "setup_other", "label": "Configurar otra API (/start-0-1)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_video_narration -> Dirigir a /start-13-3
- try_slide_video -> Dirigir a /start-13-5
- setup_other -> Dirigir a /start-0-1
- back_to_setup -> Dirigir a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-elevenlabs` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "La configuración de la API de ElevenLabs se completó. Puede proceder a crear un video de presentación de producto con `/start-13-3` o un video de narración de diapositivas con `/start-13-5`."

## Enlaces de referencia (sincronizado con las slides de Module 15)

Cinco recursos para buscar plantillas o inspiración.

- [Dribbble (motion design portfolios)](https://dribbble.com/)
- [Envato Elements — video templates / logo animation](https://elements.envato.com/video-templates/logo+animation)
- [Placeit — minimalist motion-graphics intro maker](https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988)
- [YouTube — After Effects templates project channel](https://www.youtube.com/@paftereffectstemplatesproj6705)
- [YouTube — motion-graphics templates playlist](https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj)

