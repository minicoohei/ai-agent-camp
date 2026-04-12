---
description: "Configuración de Typefully API (con guía completa)"
duration: "~10 min"
prerequisites: ["Tener cuenta de X (Twitter)", "Navegador disponible"]
level: "beginner"
tags: ["setup", "typefully", "api", "sns"]
---

# Configuración de Typefully API

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-typefully` para mostrar el progreso
2. Detectar automáticamente la clave API existente:
   - Ejecutar `uv run python tools/credential_manager.py status`
   - Si TYPEFULLY_API_KEY ya está configurada, solo ejecutar Step 4 (prueba de API) y marcar como completado
   - Si existe en texto plano en `.env`, sugerir migración al almacén de credenciales

> **Esta configuración es opcional.** La API de Typefully se usa en lecciones de marketing (Módulo 12) para programar publicaciones en redes sociales. Puede omitirla si no va a tomar las lecciones de marketing.

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Obtener una clave API de Typefully, guardarla en el Credential Store y habilitar las funciones de programación y gestión de publicaciones en redes sociales |
| Duración | ~10 minutos |
| Requisitos previos | Tener una cuenta de X (Twitter), navegador disponible |
| Nivel de operación | La mayor parte lo ejecuta la IA automáticamente (solo un comando manual en un terminal separado para guardar la clave API) |

**¿Qué es Typefully?**
Typefully es un servicio para programar y gestionar publicaciones en redes sociales como X (Twitter), LinkedIn y más. Puede publicar contenido generado por IA directamente. Tiene plan gratuito. Los planes de pago comienzan desde $12.5/mes.

**Flujo de la sesión:**
1. Abrir Typefully en el navegador (la IA abre el navegador automáticamente)
2. Registrarse / iniciar sesión con cuenta de X (Twitter)
3. Obtener la clave API (solo copiar desde la página de configuración)
4. Guardar la clave API de forma segura con credential_manager.py (ejecutar en terminal separado)
5. Prueba de operación (la IA la ejecuta automáticamente)

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
      {"id": "skip", "label": "Quiero omitir esta configuración"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Después de abrir el navegador en Step 1, seguir la sección "Automatización con integración Chrome")
(check_prereq -> Indicar: "Está listo si puede iniciar sesión con su cuenta de X (Twitter) en un navegador. Typefully tiene un plan gratuito, por lo que no tiene costo")
(skip -> Indicar: "Configuración de Typefully API omitida. Puede configurarla más tarde con /setup-typefully cuando sea necesario" y finalizar)
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Abrir Typefully en el navegador

**Lo que hace la IA:**
1. Detectar automáticamente el sistema operativo (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://typefully.com
# Windows:
start https://typefully.com
# Linux:
xdg-open https://typefully.com
```

**Una vez que se abra el navegador, mostrar el siguiente AskQuestion:**

```json
{
  "title": "Step 1: Registrarse / iniciar sesión en Typefully",
  "questions": [{
    "id": "browser_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para registrarse:\n\n1. Haga clic en 'Get started free' en la página principal de Typefully\n2. Seleccione 'Sign up with X (Twitter)' para autenticarse con su cuenta de X\n3. Una vez que aparezca el panel de Typefully, el registro está completo\n\n¿Pudo registrarse?",
    "options": [
      {"id": "signed_up", "label": "¡Registrado / sesión iniciada!"},
      {"id": "already_account", "label": "Ya tengo una cuenta"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "x_auth_issue", "label": "La autenticación con la cuenta de X no funciona"}
    ]
  }]
}
```

(signed_up -> Ir al Step 2)
(already_account -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://typefully.com")
(x_auth_issue -> Indicar: "Si la autenticación con su cuenta de X está bloqueada, habilite el acceso de aplicaciones de terceros en la configuración de privacidad de X. Vaya a X -> Configuración -> Seguridad y acceso a la cuenta -> Aplicaciones y sesiones para verificar")

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisitos previos:** La extensión "Claude in Chrome" (v1.0.36+) está instalada en Chrome, y se inició con `claude --chrome` o se ejecutó `/chrome` dentro de la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://typefully.com en el navegador
2. Usar la integración Chrome para ejecutar secuencialmente:
   - Hacer clic en "Get started free"
   - Autenticar con "Sign up with X (Twitter)" (esperar la acción del usuario)
   - Después de iniciar sesión, navegar a https://typefully.com/settings/api
   - Hacer clic en "Generate API Key" o "Create API Key"
3. Una vez que se muestre la clave API, indicar al usuario: "Copie la clave API"
4. Ir al Step 3

**Nota:** No leer el valor de la clave API desde la pantalla del navegador. El usuario la copia manualmente.

Si la integración Chrome no está disponible, siga los pasos manuales a continuación.

---

## Step 2: Obtener la clave API

**Lo que hace la IA:**
1. Ejecutar el siguiente comando para abrir la página de configuración de API en el navegador:

```bash
# Mac:
open https://typefully.com/settings/api
# Windows:
start https://typefully.com/settings/api
# Linux:
xdg-open https://typefully.com/settings/api
```

**Una vez que se abra el navegador, mostrar el siguiente AskQuestion:**

```json
{
  "title": "Step 2: Obtener clave API",
  "questions": [{
    "id": "api_key_status",
    "prompt": "¿Se abrió la página de configuración de API? Siga estos pasos para obtener la clave API:\n\n1. Vaya a la página Settings > API de Typefully\n2. Si se muestra una clave API, cópiela tal como está\n3. Si necesita crear una nueva, haga clic en 'Generate API Key'\n4. Copie la clave API mostrada\n\n¿Pudo copiar la clave API?",
    "options": [
      {"id": "copied", "label": "¡Clave API copiada!"},
      {"id": "page_not_found", "label": "No encuentro la página de configuración de API"},
      {"id": "no_api_key", "label": "No se muestra ninguna clave API"},
      {"id": "paid_plan_required", "label": "Dice que se requiere un plan de pago"}
    ]
  }]
}
```

(copied -> Ir al Step 3)
(page_not_found -> Indicar: "Abra esta URL directamente en su navegador: https://typefully.com/settings/api -- La página de configuración aparecerá si ha iniciado sesión")
(no_api_key -> Indicar: "Verifique si hay un botón 'Generate API Key' o 'Create API Key' en la página. Si no lo encuentra, intente recargar la página")
(paid_plan_required -> Indicar: "Es posible que se necesite un plan de pago para acceder a la API. Si el plan gratuito no admite acceso a la API, puede omitir esta configuración sin problemas")

---

## Step 3: Guardar la clave API de forma segura

**Nota importante de seguridad:**
No pegue la clave API en este chat. La guardaremos de forma segura en una ventana de terminal separada.

**Lo que la IA ejecuta automáticamente:**
1. Verificar si el paquete `keyring` está instalado
   - Si no está instalado: Ejecutar automáticamente `pip install keyring`
2. Ejecutar `uv run python tools/credential_manager.py status` para verificar el estado actual

**Mensaje para mostrar al usuario:**

```text
Después de copiar la clave API, siga estos pasos para guardarla de forma segura:

┌─────────────────────────────────────────────────────────────┐
│ Ejecute el siguiente comando en una ventana de terminal     │
│ separada:                                                   │
│                                                             │
│ Cursor: Ctrl+` (acento grave) para abrir un nuevo terminal  │
│ Claude Code: Abrir una ventana de terminal separada         │
│                                                             │
│ uv run python tools/credential_manager.py store TYPEFULLY_API_KEY  │
│                                                             │
│ -> Aparecerá "Enter value for TYPEFULLY_API_KEY:"           │
│ -> Pegue la clave API copiada y presione Enter              │
│   (El texto que escribe no se mostrará en pantalla.         │
│    Esto es normal)                                          │
│ -> "Stored TYPEFULLY_API_KEY" significa que se guardó        │
└─────────────────────────────────────────────────────────────┘

Una vez guardado, vuelva a este chat y dígame que "terminó".
```

**¿Por qué ejecutarlo en una ventana separada?**
Si maneja la clave API en este chat de IA, el valor queda en el registro de la conversación.
Al ejecutar `credential_manager.py` en una ventana separada, el valor de la clave se guarda directamente
en el almacenamiento cifrado del sistema operativo (macOS Keychain / Windows Credential Locker / Linux SecretService),
y nunca aparece en archivos de texto plano ni en registros del chat.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Guardar la clave API",
  "questions": [{
    "id": "store_status",
    "prompt": "¿Pudo ejecutar el comando en un terminal separado?",
    "options": [
      {"id": "done", "label": "¡Guardado!"},
      {"id": "terminal_help", "label": "No sé cómo abrir un terminal"},
      {"id": "command_error", "label": "El comando dio un error"},
      {"id": "security_question", "label": "Tengo una pregunta sobre seguridad"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(terminal_help -> Indicar: "Para Cursor: Menú > Terminal > New Terminal, o presione Ctrl+` (Mac: Cmd+`). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra PowerShell o Windows Terminal desde el menú Inicio, o Ctrl+Shift+T para una nueva pestaña. Luego navegue con cd al directorio del proyecto")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `pip install keyring`)
(security_question -> Explicar: "Esta herramienta usa el almacenamiento cifrado integrado del sistema operativo. En macOS usa Keychain, en Windows usa Credential Locker y en Linux usa SecretService (GNOME Keyring, etc.). No se crean archivos de texto plano (.env). El almacenamiento también se bloquea cuando la pantalla está bloqueada, proporcionando protección contra el acceso físico")

---

## Step 4: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Primero ejecutar `credential_manager.py status` para verificar si `TYPEFULLY_API_KEY` está guardada en el Credential Store:
   - **Nota**: No mostrar el valor de la clave API en el chat. Solo mostrar salida enmascarada como "Se confirmó que la clave API está configurada (primeros 4 caracteres: xxxx...)"
   - Comando de verificación de estado: `uv run python tools/credential_manager.py status`

2. Si pasa la verificación básica, enviar una solicitud de prueba real a la API de Typefully:
   - Inyectar desde el Credential Store a variables de entorno y ejecutar la llamada API
   - Ejemplo de código de prueba:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("TYPEFULLY_API_KEY")
     if not key:
         print("Error: TYPEFULLY_API_KEY no está configurada.")
         sys.exit(1)
     resp = requests.get("https://api.typefully.com/v1/drafts/recently-created",
         headers={"X-API-KEY": key})
     if resp.status_code == 200:
         print("¡Conexión exitosa! Se puede acceder a la API de Typefully.")
     else:
         print(f"Error: {resp.status_code}")
         print("Verifique la re-autenticación, regeneración de clave API o configuración de permisos.")
     ```
   - Instalar automáticamente los paquetes faltantes (`requests`, `keyring`)

3. Mostrar AskQuestion según los resultados de la prueba:

**Al tener éxito en la prueba:**
```text
¡La configuración de la API de Typefully está completa!

Resultado de la prueba: Se recibió respuesta exitosa de la API.
Ahora puede usar las funciones de programación y gestión de publicaciones en redes sociales.
```

**AskQuestion en caso de fallo en la prueba:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de API. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Intentar la prueba de nuevo"},
      {"id": "recheck_key", "label": "Volver a verificar la clave API (volver al Step 2)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(recheck_key -> Volver al Step 2)
(show_error -> Mostrar mensaje de error con causa y solución)
(skip_test -> Indicar: "Prueba de API omitida. Puede verificar más tarde con /check-setup")

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
      {"id": "trouble_x_auth", "label": "La autenticación con cuenta de X no funciona"},
      {"id": "trouble_invalid", "label": "Error 'Invalid API key' o 'Unauthorized'"},
      {"id": "trouble_not_found", "label": "No encuentro la página de clave API"},
      {"id": "trouble_cost", "label": "Me preocupa el precio"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: La autenticación con cuenta de X no funciona
**Causa**: El acceso de aplicaciones de terceros está bloqueado en la configuración de privacidad de X
**Lo que hace la IA**:
1. Indicar: "Vaya a X (Twitter) -> Configuración -> Seguridad y acceso a la cuenta -> Aplicaciones y sesiones para habilitar el acceso de aplicaciones de terceros"
2. Si eso no ayuda: "Intente limpiar las cookies del navegador e intente de nuevo"
3. Verificar si la cuenta de X está suspendida o restringida

### Problema 2: Error "Invalid API key" o "Unauthorized"
**Causa**: La clave API no se copió correctamente o la clave es inválida
**Lo que hace la IA**:
1. Verificar el estado de almacenamiento de `TYPEFULLY_API_KEY` con `credential_manager.py status` (solo mostrar valor enmascarado)
2. Si no está guardada en el Credential Store, guiar el re-registro
3. Si está guardada, volver a ejecutar la prueba de API. Si falla, indicar: "Recree la clave en la página de configuración de Typefully (https://typefully.com/settings/api)"

### Problema 3: No se encuentra la página de clave API
**Causa**: No ha iniciado sesión, o la URL ha cambiado
**Indicación de la IA**: "Primero inicie sesión en Typefully y luego acceda a https://typefully.com/settings/api. Si no encuentra la página, navegue desde el ícono en la esquina superior derecha del panel -> Settings -> API"

### Problema 4: Preocupación por el precio
**Indicación de la IA**: "Typefully tiene un plan gratuito. El acceso básico a la API está disponible en el plan gratuito. Los planes de pago comienzan desde $12.5/mes con más funciones (programación, análisis, etc.). El plan gratuito es suficiente para uso a nivel de capacitación"

### Problema 5: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa y guiar la solución

---

## Punto de verificación
- [ ] Se registró en Typefully con su cuenta de X (Twitter)
- [ ] Obtuvo la clave API desde la página de configuración de API (Settings > API)
- [ ] Guardó en el Credential Store con credential_manager.py store
- [ ] Confirmó el almacenamiento con credential_manager.py status
- [ ] La prueba de API fue exitosa (se recibió respuesta de la API de Typefully)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de la API de Typefully está completa! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_marketing", "label": "Comenzar lecciones de marketing (/start-12-1)"},
      {"id": "setup_other", "label": "Configurar otras API (/start-0-1)"},
      {"id": "try_banner", "label": "Intentar crear un banner (/start-1-1)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_marketing -> Guiar a /start-12-1
- setup_other -> Guiar a /start-0-1
- try_banner -> Guiar a /start-1-1
- back_to_setup -> Guiar a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-typefully` para actualizar el progreso
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "Ahora puede crear y programar publicaciones en redes sociales en las lecciones de marketing (/start-12-1)"
