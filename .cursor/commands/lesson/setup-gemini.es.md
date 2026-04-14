---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Tener una cuenta de Google", "Navegador disponible"]
level: "beginner"
tags: ["setup", "gemini", "api"]
---

# Configuración de la API de Gemini

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-gemini` para mostrar el progreso
2. Detectar automáticamente la clave de API existente:
   - Ejecutar `uv run python tools/credential_manager.py status`
   - Si GEMINI_API_KEY ya está configurada, puede ejecutar solo el Step 3 (prueba de API) y marcarlo como completado
   - Si existe una clave en texto plano en `.env`, sugerir la migración al almacén de credenciales

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Obtener una clave de API de Gemini desde Google AI Studio y guardarla en el Almacén de credenciales para poder usar funciones de IA como generación de imágenes |
| Duración | ~10 minutos |
| Requisitos previos | Tener una cuenta de Google y un navegador disponible |
| Nivel de operación | No se necesitan comandos CLI (todo lo ejecuta automáticamente la IA + solo operaciones de GUI) |

**Flujo de la sesión:**
1. Abrir Google AI Studio en el navegador (la IA abre el navegador automáticamente)
2. Obtener la clave de API (solo hacer clic en botones en pantalla)
3. Guardar la clave de API de forma segura (la IA crea el archivo automáticamente)
4. Ingresar la clave de API (abrir el archivo y pegar)
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
(check_prereq -> Indicar: "Está listo/a si puede iniciar sesión en un navegador con una cuenta de Google.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Abrir Google AI Studio en el navegador

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://aistudio.google.com/apikey
# Windows:
start https://aistudio.google.com/apikey
# Linux:
xdg-open https://aistudio.google.com/apikey
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 1: Obtener la clave de API en el navegador",
  "questions": [{
    "id": "browser_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para obtener su clave de API:\n\n1. Inicie sesión con su cuenta de Google\n2. Haga clic en el botón 'Get API key'\n3. Haga clic en 'Create API key'\n4. Haga clic en el botón 'Copiar' junto a la clave de API mostrada\n\n¿Copió la clave de API?",
    "options": [
      {"id": "copied", "label": "¡Copié la clave de API!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "no_button", "label": "No encuentro el botón 'Get API key'"},
      {"id": "login_issue", "label": "No puedo iniciar sesión en mi cuenta de Google"}
    ]
  }]
}
```

(copied -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://aistudio.google.com/apikey")
(no_button -> Indicar: "Espere a que la página se cargue completamente. Si aún no aparece, haga clic en la pestaña 'Get API key' en la parte superior de la página.")
(login_issue -> Indicar: "Google AI Studio requiere una cuenta de gmail.com o Google Workspace. Intente iniciar sesión con su cuenta de empresa.")

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisito previo:** La extensión "Claude in Chrome" (v1.0.36+) debe estar instalada en Chrome, y debe haber iniciado con `claude --chrome` o ejecutado `/chrome` en la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://aistudio.google.com/apikey en el navegador
2. Usar la integración Chrome para realizar las siguientes operaciones en orden:
   - Si se necesita iniciar sesión en la cuenta de Google, esperar la acción del usuario
   - Hacer clic en el botón "Get API key" o "Obtener clave de API"
   - Hacer clic en el botón "Create API key" o "Crear clave de API"
   - Si aparece una pantalla de selección de proyecto, seleccionar el proyecto predeterminado y hacer clic en "Create API key in existing project"
3. Una vez que la clave de API aparezca en pantalla, indicar al usuario "Haga clic en el botón de copiar para copiar la clave de API"
4. Ir al Step 2

**Nota:** No leer el valor de la clave de API desde la pantalla del navegador. El usuario la copia manualmente.

Si la integración Chrome no está disponible, siga las instrucciones del Step 1 manualmente.

---

## Step 2: Guardar la clave de API de forma segura

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
│ uv run python tools/credential_manager.py store GEMINI_API_KEY     │
│                                                             │
│ → Se mostrará "Enter value for GEMINI_API_KEY:"             │
│ → Pegue la clave de API copiada y presione Enter            │
│   (Los caracteres que escriba no se mostrarán en pantalla.  │
│    Esto es normal.)                                         │
│ → "Stored GEMINI_API_KEY" significa que se guardó           │
│   exitosamente                                              │
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
  "title": "Step 2: Guardar la clave de API",
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

(done -> Ir al Step 3)
(terminal_help -> Indicar: "Para Cursor: Menú en la parte superior > Terminal > New Terminal, o presione Ctrl+` (Cmd+` en Mac). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra PowerShell o Windows Terminal desde el menú Inicio, o presione Ctrl+Shift+T para una nueva pestaña. Luego navegue al directorio del proyecto con cd.")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `pip install keyring`)
(security_question -> Explicar: "Esta herramienta usa el almacenamiento cifrado estándar del SO. En macOS usa Keychain, en Windows usa Credential Locker y en Linux usa SecretService (GNOME Keyring, etc.). No se crean archivos de texto plano (.env). El almacenamiento también se bloquea cuando la pantalla está bloqueada, proporcionando protección contra acceso físico.")

---

## Step 3: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Primero, ejecutar `credential_manager.py status` para verificar si `GEMINI_API_KEY` está guardada en el Almacén de credenciales:
   - **Nota**: No mostrar el valor de la clave de API en el chat. Solo mostrar salida enmascarada como "La clave de API está configurada (primeros 4 caracteres: AIza...)"
   - Comando de verificación de estado: `uv run python tools/credential_manager.py status`

2. Si la verificación básica pasa, enviar una solicitud de prueba a la API de Gemini:
   - Inyectar variables de entorno desde el Almacén de credenciales y realizar la llamada a la API
   - Ejemplo de código de prueba:
     ```python
     import os
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     from dotenv import load_dotenv
     load_dotenv()
     from google import genai
     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
     response = client.models.generate_content(
         model="gemini-2.5-flash",
         contents="¡Hola! Por favor, salude en una sola línea."
     )
     print("Respuesta de la API:", response.text)
     ```
   - Instalar automáticamente los paquetes necesarios (`google-genai`, `keyring`) si no están instalados

3. Mostrar una AskQuestion según el resultado de la prueba:

**En caso de éxito:**
```text
¡La configuración de la API de Gemini se completó!

Resultado de la prueba: Se recibió exitosamente una respuesta de la API.
Ahora puede usar funciones de IA como generación de imágenes (/banner), creación de diagramas (/diagram) y más.
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
      {"id": "recheck_key", "label": "Verificar la clave de API de nuevo (volver al Step 1)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(recheck_key -> Volver al Step 1)
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
      {"id": "trouble_cost", "label": "Me preocupan los costos"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error "Invalid API key"
**Causa**: La clave de API no se copió correctamente, o la clave es inválida
**Lo que hace la IA**:
1. Verificar el estado de guardado de `GEMINI_API_KEY` con `credential_manager.py status` (solo mostrar valor enmascarado)
2. Si no está guardada en el Almacén de credenciales, indicar que se vuelva a registrar
3. Si está guardada, volver a ejecutar la prueba de API. Si falla, indicar: "Vuelva a crear la clave en Google AI Studio."

### Problema 2: Error "Quota exceeded"
**Causa**: Se alcanzó el límite del nivel gratuito
**Indicación de la IA**: "El nivel gratuito de la API de Gemini permite 15 solicitudes por minuto y 1.500 solicitudes por día. Espere unos minutos e intente de nuevo. El nivel gratuito es más que suficiente para el uso en el curso."

### Problema 3: Error de paquete de Python
**Causa**: Los paquetes necesarios no están instalados
**Lo que hace la IA**: Instalar automáticamente los paquetes faltantes (`pip install google-genai python-dotenv`)

### Problema 4: Preocupación por los costos
**Indicación de la IA**: "La API de Gemini tiene un nivel gratuito. No hay costos dentro de los límites del nivel gratuito. Para el uso a nivel de curso (unas pocas docenas de generaciones al día), el nivel gratuito es más que suficiente. Google le notificará antes de que se apliquen cargos."

### Problema 5: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar al usuario la solución

---

## Punto de control
- [ ] Obtuvo una clave de API de Google AI Studio
- [ ] Guardó en el Almacén de credenciales con credential_manager.py store
- [ ] Confirmó el guardado con credential_manager.py status
- [ ] La prueba de API fue exitosa (se recibió una respuesta de la API de Gemini)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de la API de Gemini se completó! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "setup_slack", "label": "Configurar también la API de Slack (/setup-slack)"},
      {"id": "try_banner", "label": "Probar a crear un banner ahora mismo (/start-1-1)"},
      {"id": "try_diagram", "label": "Probar a crear un diagrama (/start-2-1)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- setup_slack -> Dirigir a /setup-slack
- try_banner -> Dirigir a /start-1-1
- try_diagram -> Dirigir a /start-2-1
- back_to_setup -> Dirigir a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-gemini` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, configure la API de Slack con `/setup-slack` (se puede omitir)"
