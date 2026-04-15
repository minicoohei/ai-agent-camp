---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Navegador disponible", "Tener cuenta de GitHub o Google"]
level: "beginner"
tags: ["setup", "fal", "api", "video", "image"]
---

# Configuración de la API de fal.ai

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-fal` para mostrar el progreso
2. Detectar automáticamente la clave de API existente:
   - Ejecutar `uv run python tools/credential_manager.py status`
   - Si FAL_KEY ya está configurada, puede ejecutar solo el Step 4 (prueba) y marcarlo como completado
   - Si existe una clave en texto plano en `.env`, sugerir la migración al almacén de credenciales

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Obtener una clave de API de fal.ai y guardarla en el Almacén de credenciales para poder usar funciones de IA como generación de video e imagen |
| Duración | ~10 minutos |
| Requisitos previos | Una cuenta de GitHub o Google, y un navegador disponible |
| Nivel de operación | Principalmente ejecución automática por la IA (solo un comando manual en terminal separada para almacenar la clave de API) |

**¿Qué es fal.ai?**
Una plataforma que proporciona acceso unificado a motores de IA para generación de video (Kling, Veo, etc.), generación de imágenes, sincronización labial (Fabric), generación de música (Suno) y más. Una sola clave de API le da acceso a múltiples modelos de IA.

**Flujo de la sesión:**
1. Abrir fal.ai en el navegador (la IA abre el navegador automáticamente)
2. Crear una cuenta y obtener la clave de API (solo hacer clic en botones en pantalla)
3. Guardar la clave de API de forma segura en el Almacén de credenciales (ejecutar un comando en terminal separada)
4. Prueba de funcionalidad (la IA lo ejecuta automáticamente)

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
(check_prereq -> Indicar: "Puede registrarse con una cuenta de GitHub o Google. Si puede iniciar sesión en el navegador, está listo/a.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Abrir fal.ai en el navegador y crear una cuenta

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://fal.ai
# Windows:
start https://fal.ai
# Linux:
xdg-open https://fal.ai
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 1: Crear una cuenta de fal.ai",
  "questions": [{
    "id": "account_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para crear su cuenta:\n\n1. Haga clic en 'Sign Up' o 'Login' en la parte superior derecha\n2. Autentíquese con su cuenta de GitHub o Google\n3. Cuando se muestre el panel de control, habrá terminado\n\n¿Ha iniciado sesión?",
    "options": [
      {"id": "logged_in", "label": "¡He iniciado sesión!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "signup_issue", "label": "No puedo registrarme"},
      {"id": "already_have_account", "label": "Ya tengo una cuenta"}
    ]
  }]
}
```

(logged_in -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://fal.ai")
(signup_issue -> Indicar: "Intente autenticarse con su cuenta de GitHub. Si falla, intente con su cuenta de Google.")
(already_have_account -> Ir al Step 2)

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisito previo:** La extensión "Claude in Chrome" (v1.0.36+) debe estar instalada en Chrome, y debe haber iniciado con `claude --chrome` o ejecutado `/chrome` en la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://fal.ai en el navegador
2. Usar la integración Chrome para realizar las siguientes operaciones en orden:
   - Hacer clic en el botón "Sign Up" o "Login"
   - Autenticarse con cuenta de GitHub o Google (esperar la acción del usuario)
   - Después de iniciar sesión, navegar a https://fal.ai/dashboard/keys
   - Hacer clic en el botón "Create Key" o "Add Key"
3. Una vez que se muestre la clave de API, indicar al usuario "Copie la clave de API"
4. Ir al Step 3

**Nota:** No leer el valor de la clave de API desde la pantalla del navegador. El usuario la copia manualmente.

Si la integración Chrome no está disponible, siga los pasos a continuación manualmente.

---

## Step 2: Obtener su clave de API

**Lo que hace la IA:**
1. Abrir la página de administración de claves de API en el navegador:

```bash
# Mac:
open https://fal.ai/dashboard/keys
# Windows:
start https://fal.ai/dashboard/keys
# Linux:
xdg-open https://fal.ai/dashboard/keys
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 2: Obtener su clave de API",
  "questions": [{
    "id": "key_status",
    "prompt": "¿Se abrió la página de administración de claves de API? Siga estos pasos para obtener su clave de API:\n\n1. Haga clic en el botón 'Create Key' o 'Add Key'\n2. Copie la clave de API mostrada\n   (La clave puede mostrarse solo una vez. Asegúrese de copiarla.)\n\n¿Copió la clave de API?",
    "options": [
      {"id": "copied", "label": "¡Copié la clave de API!"},
      {"id": "page_not_found", "label": "No encuentro la página de administración de claves"},
      {"id": "no_create_button", "label": "No encuentro el botón 'Create Key'"},
      {"id": "key_already_exists", "label": "Ya tengo una clave existente"}
    ]
  }]
}
```

(copied -> Ir al Step 3)
(page_not_found -> Indicar: "Abra esta URL directamente en su navegador: https://fal.ai/dashboard/keys Asegúrese de haber iniciado sesión.")
(no_create_button -> Indicar: "Espere a que la página se cargue completamente. Busque 'Keys' o 'API Keys' en el menú lateral izquierdo del panel de control.")
(key_already_exists -> Indicar: "También puede usar una clave existente. Si puede copiar el valor de la clave, continúe al Step 3. También puede crear una nueva clave si lo prefiere." e ir al Step 3)

---

## Step 3: Guardar la clave de API de forma segura

**Nota importante de seguridad:**
No pegue la clave de API en este chat. La guardaremos de forma segura en una ventana de terminal separada.

**Lo que la IA ejecuta automáticamente:**
1. Verificar si el paquete `keyring` está instalado
   - Si no está instalado: ejecutar automáticamente `pip install keyring`
2. Ejecutar `uv run python tools/credential_manager.py status` para verificar el estado actual

**Mensaje para mostrar al usuario:**

```text
Una vez que haya copiado la clave de API, siga estos pasos para guardarla de forma segura:

┌─────────────────────────────────────────────────────────────┐
│ Ejecute el siguiente comando en una ventana de terminal     │
│ separada:                                                   │
│                                                             │
│ Cursor: Ctrl+` (acento grave) para abrir una nueva terminal │
│ Claude Code: Abra una ventana de terminal separada          │
│                                                             │
│ uv run python tools/credential_manager.py store FAL_KEY            │
│                                                             │
│ → Se mostrará "Enter value for FAL_KEY:"                    │
│ → Pegue la clave de API copiada y presione Enter            │
│   (Los caracteres que escriba no se mostrarán en pantalla.  │
│    Esto es normal.)                                         │
│ → "Stored FAL_KEY" significa que se guardó exitosamente     │
└─────────────────────────────────────────────────────────────┘

Una vez guardada, regrese a este chat y diga "listo".
```

**Por qué ejecutar en una ventana separada:**
Si maneja claves de API en el chat de IA, los valores quedarán en el registro de la conversación.
Al ejecutar `credential_manager.py` en una ventana separada, los valores de las claves se almacenan directamente
en el almacenamiento cifrado del SO (macOS Keychain / Windows Credential Locker / Linux SecretService),
y nunca se almacenan en archivos de texto plano ni en registros de chat.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Guardar la clave de API",
  "questions": [{
    "id": "store_status",
    "prompt": "¿Ejecutó el comando en una terminal separada?",
    "options": [
      {"id": "done", "label": "¡Guardado!"},
      {"id": "terminal_help", "label": "No sé cómo abrir una terminal"},
      {"id": "command_error", "label": "Obtuve un error con el comando"},
      {"id": "security_question", "label": "Tengo una pregunta sobre seguridad"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(terminal_help -> Indicar: "Para Cursor: Menú en la parte superior > Terminal > New Terminal, o presione Ctrl+` (Cmd+` en Mac). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra su terminal WSL (Ubuntu), o agregue una pestaña Ubuntu en Windows Terminal. Luego navegue con cd al directorio del proyecto.")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `pip install keyring`)
(security_question -> Explicar: "Esta herramienta usa el almacenamiento cifrado estándar del SO. En macOS usa Keychain, en Windows usa Credential Locker y en Linux usa SecretService (GNOME Keyring, etc.). No se crean archivos de texto plano (.env). El almacenamiento también se bloquea cuando la pantalla está bloqueada, proporcionando protección contra acceso físico.")

---

## Step 4: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Primero, ejecutar `credential_manager.py status` para verificar si `FAL_KEY` está guardada en el Almacén de credenciales:
   - **Nota**: No mostrar el valor de la clave de API en el chat. Solo mostrar salida enmascarada como "La clave de API está configurada (primeros 8 caracteres: xxxxxxxx...)"
   - Comando de verificación de estado: `uv run python tools/credential_manager.py status`

2. Verificar si el paquete `fal-client` está instalado:
   - Si no está instalado: ejecutar automáticamente `pip install fal-client`

3. Ejecutar una prueba de importación del paquete y verificación de configuración de FAL_KEY:
   - **Nota**: Las llamadas reales a la API de fal.ai tienen costo, por lo que solo se verifica la importación del paquete y la configuración de la clave
   - Código de prueba:
     ```python
     import os
     import sys
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("FAL_KEY")
     if not key:
         print("Error: FAL_KEY no está configurada.")
         sys.exit(1)
     try:
         import fal_client
         print(f"fal-client instalado: {fal_client.__version__ if hasattr(fal_client, '__version__') else 'OK'}")
         print(f"FAL_KEY configurada (primeros 8 caracteres: {key[:8]}...)")
         print("¡La configuración de la API de fal.ai se completó!")
     except ImportError:
         print("fal-client no está instalado. Ejecute pip install fal-client.")
     ```

4. Mostrar una AskQuestion según el resultado de la prueba:

**En caso de éxito:**
```text
¡La configuración de la API de fal.ai se completó!

Resultado de la prueba: Se confirmó la importación del paquete fal-client y la configuración de FAL_KEY.
Ahora puede usar motores de IA para generación de video (Kling, Veo, etc.), generación de imágenes,
sincronización labial (Fabric), generación de música (Suno) y más.
```

**En caso de fallo — AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba. Verifiquemos las posibles causas.",
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
(skip_test -> Indicar: "Se omitió la prueba. Puede verificarla más tarde con /check-setup.")

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
      {"id": "trouble_signup", "label": "No puedo crear cuenta / iniciar sesión"},
      {"id": "trouble_invalid", "label": "La clave de API es inválida (error de autenticación)"},
      {"id": "trouble_package", "label": "Obtengo un error al instalar fal-client"},
      {"id": "trouble_python", "label": "Tengo un problema con la versión de Python"},
      {"id": "trouble_cost", "label": "Me preocupan los costos"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: No puedo crear cuenta / iniciar sesión
**Causa**: Problemas con el proveedor de autenticación (GitHub/Google)
**Lo que hace la IA**:
1. Indicar: "Intente un método de autenticación diferente. Si GitHub falló, intente con una cuenta de Google, o viceversa."
2. Indicar: "Intente acceder a https://fal.ai de nuevo en el modo incógnito/navegación privada de su navegador."
3. Si aún no se resuelve: "Contacte al soporte de fal.ai (https://fal.ai)."

### Problema 2: Clave de API inválida (error de autenticación)
**Causa**: La clave de API no se copió correctamente, o la clave es inválida
**Lo que hace la IA**:
1. Verificar el estado de guardado de `FAL_KEY` con `credential_manager.py status` (solo mostrar valor enmascarado)
2. Si no está guardada en el Almacén de credenciales, indicar que se vuelva a registrar
3. Si está guardada: "Verifique en el panel de control de fal.ai (https://fal.ai/dashboard/keys) que la clave sea válida. Cree una nueva clave si es necesario."

### Problema 3: Error al instalar fal-client
**Causa**: Problemas con pip o conflictos de dependencias
**Lo que hace la IA**:
1. Volver a ejecutar `pip install fal-client`
2. Si los errores persisten, ejecutar `pip install --upgrade pip` y reintentar
3. Si el venv está dañado, recrearlo con `bash tools/scripts/setup.sh`

### Problema 4: Problema con la versión de Python
**Causa**: fal-client requiere Python 3.10 o superior
**Lo que hace la IA**:
1. Verificar la versión actual con `python --version`
2. Si es inferior a 3.10: "fal-client requiere Python 3.10 o superior. Actualice Python."
3. Si pyenv está instalado, indicar `pyenv install 3.10`

### Problema 5: Preocupación por los costos
**Indicación de la IA**: "fal.ai utiliza un modelo de precios de pago por uso. Para el uso a nivel de curso (algunas pruebas de generación de imágenes/video), los costos son de unos pocos dólares. Puede verificar el uso y el saldo en el panel de control (https://fal.ai/dashboard) en cualquier momento. También puede establecer un límite de facturación."

### Problema 6: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar al usuario la solución

---

## Punto de control
- [ ] Creó una cuenta de fal.ai
- [ ] Obtuvo una clave de API del panel de control de fal.ai
- [ ] Guardó FAL_KEY en el Almacén de credenciales con credential_manager.py store
- [ ] Confirmó el guardado con credential_manager.py status
- [ ] El paquete fal-client está instalado
- [ ] La prueba fue exitosa (se confirmó la importación de fal-client y la configuración de FAL_KEY)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de la API de fal.ai se completó! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "video_overview", "label": "Aprender sobre motores de IA de video (/start-13-2)"},
      {"id": "setup_elevenlabs", "label": "Configurar también la API de ElevenLabs (/setup-elevenlabs)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- video_overview -> Dirigir a /start-13-2
- setup_elevenlabs -> Dirigir a /setup-elevenlabs
- back_to_setup -> Dirigir a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-fal` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, aprenda sobre motores de IA de video con `/start-13-2`. O configure la API de ElevenLabs con `/setup-elevenlabs`."
