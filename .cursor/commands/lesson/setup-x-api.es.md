---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Tener una cuenta de X", "Navegador disponible"]
level: "beginner"
tags: ["setup", "x", "twitter", "api"]
---

# Configuración de X (Twitter) API

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-x-api` para mostrar el progreso
2. Detectar automáticamente la clave API existente:
   - Ejecutar `uv run python tools/credential_manager.py status`
   - Si X_BEARER_TOKEN ya está configurado, solo ejecutar Step 4 (prueba de API) y marcar como completado
   - Si existe en texto plano en `.env`, sugerir migración al almacén de credenciales

**Mostrar advertencia importante al usuario:**

```text
ADVERTENCIA: La API de X (Twitter) requiere un plan de pago

- Nivel gratuito: La API de Recent Search NO está disponible
- Plan Basic: Se requiere $100/mes
- Esta configuración es opcional. Puede omitirla si no va a usar el skill x-research

Las demás lecciones de la capacitación (creación de banners, generación de gráficos,
análisis de datos, etc.) funcionan perfectamente sin la API de X.
```

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Obtener un Bearer Token del X Developer Portal, guardarlo en el Credential Store y habilitar las funciones de búsqueda en tiempo real y análisis de tendencias de X |
| Duración | ~15 minutos |
| Requisitos previos | Tener una cuenta de X, navegador disponible |
| Nivel de operación | Sin entrada de comandos CLI (todo lo ejecuta la IA automáticamente + solo operaciones GUI) |
| Precio | **Se requiere plan Basic ($100/mes) o superior**. El nivel gratuito no admite la API de Recent Search |
| Caso de uso | Búsqueda en tiempo real y análisis de tendencias de X (Twitter). Usado por el skill x-research |

**Flujo de la sesión:**
1. Abrir X Developer Portal en el navegador (la IA abre el navegador automáticamente)
2. Solicitar una cuenta de desarrollador, crear un proyecto y una app
3. Obtener el Bearer Token
4. Guardarlo de forma segura con credential_manager.py en un terminal separado
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
    "prompt": "La configuración de la API de X requiere el plan Basic ($100/mes). ¿Está listo?",
    "options": [
      {"id": "ready", "label": "Tengo un plan de pago / planeo suscribirme. Comencemos"},
      {"id": "chrome", "label": "Automatizar operaciones del navegador con /chrome"},
      {"id": "check_cost", "label": "Quiero saber más sobre los precios"},
      {"id": "skip", "label": "Omitir (no usaré la API de X)"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Después de abrir el navegador en Step 1, seguir la sección "Automatización con integración Chrome")
(check_cost -> Indicar: "Precios de la API de X: El nivel gratuito es solo para publicar (sin API de búsqueda). El plan Basic ($100/mes) habilita la API de Recent Search. El plan Pro ($5,000/mes) habilita Full-Archive Search, pero Basic es suficiente para la capacitación. Si el costo no lo justifica, recomendamos omitirlo")
(skip -> Indicar: "Configuración de la API de X omitida. Sin impacto en otras lecciones. Puede reiniciar con /setup-x-api más tarde" e ir a la finalización)
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Abrir X Developer Portal en el navegador

**Lo que hace la IA:**
1. Detectar automáticamente el sistema operativo (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://developer.x.com/en/portal/dashboard
# Windows:
start https://developer.x.com/en/portal/dashboard
# Linux:
xdg-open https://developer.x.com/en/portal/dashboard
```

**Una vez que se abra el navegador, mostrar el siguiente AskQuestion:**

```json
{
  "title": "Step 1: Acceder al X Developer Portal",
  "questions": [{
    "id": "portal_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para solicitar una cuenta de desarrollador:\n\n1. Inicie sesión con su cuenta de X\n2. Seleccione 'Sign up for Free Account' o 'Subscribe to Basic'\n   (Se requiere el plan Basic para usar la API de Recent Search)\n3. Complete el caso de uso (ej: 'Academic research and AI agent training')\n4. Acepte el acuerdo de desarrollador\n\n¿Apareció el panel del Developer Portal?",
    "options": [
      {"id": "dashboard_ready", "label": "¡El panel apareció!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "signup_issue", "label": "Tengo problemas con la solicitud de cuenta de desarrollador"},
      {"id": "already_have_account", "label": "Ya tengo una cuenta de desarrollador"}
    ]
  }]
}
```

(dashboard_ready -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://developer.x.com/en/portal/dashboard")
(signup_issue -> Indicar: "Las solicitudes del Developer Portal pueden requerir revisión. Complete el caso de uso de forma específica (ej: 'Building an AI-powered social media research tool for corporate training'). La revisión puede tomar algunos días. Vuelva a ejecutar esta configuración después de recibir el correo de aprobación")
(already_have_account -> Ir al Step 2)

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisitos previos:** La extensión "Claude in Chrome" (v1.0.36+) está instalada en Chrome, y se inició con `claude --chrome` o se ejecutó `/chrome` dentro de la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://developer.x.com/en/portal/dashboard en el navegador
2. Usar la integración Chrome para ejecutar secuencialmente:
   - Seleccionar "Subscribe to Basic" (Se requiere el plan Basic para la API de Recent Search. La cuenta gratuita no admite la API de búsqueda)
   - Dejar la entrada de información de pago al usuario (esperar la acción del usuario)
   - Ingresar "AI agent training and educational purposes" como caso de uso
   - Aceptar el Developer Agreement y enviar (esperar la acción del usuario)
   - Navegar a "Projects & Apps" en el Dashboard
   - Hacer clic en "+ Add Project" -> Ingresar "AIAgent Bootcamp" como nombre del proyecto, seleccionar "Exploring the API" como caso de uso
   - Hacer clic en "+ Add App" -> Ingresar "AIAgent Bootcamp" como nombre de la App, seleccionar "Development" como entorno
   - Abrir la pestaña "Keys and tokens"
   - Hacer clic en "Regenerate" junto al Bearer Token
   - Hacer clic en "Yes, regenerate" en el diálogo de confirmación
3. Una vez que se muestre el Bearer Token, indicar al usuario: "Copie el token. No se puede volver a mostrar una vez que salga de la página"
4. Ir al Step 3

**Nota:** No leer el valor del Bearer Token desde la pantalla del navegador. El usuario lo copia manualmente.

Si la integración Chrome no está disponible, siga los pasos manuales a continuación.

---

## Step 2: Crear proyecto y obtener Bearer Token

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Obtener Bearer Token",
  "questions": [{
    "id": "token_status",
    "prompt": "Siga estos pasos para obtener el Bearer Token:\n\n1. Verifique la sección Dashboard > 'Projects & Apps'\n2. Si no hay proyecto, haga clic en '+ Add Project'\n   - Ingrese un nombre de proyecto (ej: 'AIAgent Bootcamp')\n   - Seleccione un caso de uso (ej: 'Exploring the API')\n3. Haga clic en '+ Add App' dentro del proyecto\n   - Ingrese un nombre de App (ej: 'AIAgent Bootcamp')\n   - Seleccione 'Development' como entorno de App\n4. Abra la pestaña 'Keys and tokens'\n5. Haga clic en 'Regenerate' en la sección 'Bearer Token'\n6. Copie el Bearer Token mostrado\n\n¿Pudo copiar el Bearer Token?",
    "options": [
      {"id": "copied", "label": "¡Bearer Token copiado!"},
      {"id": "no_project", "label": "No sé cómo crear un proyecto"},
      {"id": "no_bearer", "label": "No encuentro el Bearer Token"},
      {"id": "plan_issue", "label": "Estoy en el nivel gratuito y quiero actualizar a Basic"}
    ]
  }]
}
```

(copied -> Ir al Step 3)
(no_project -> Indicar: "Seleccione 'Projects & Apps' en el menú izquierdo del Dashboard. Verá el botón '+ Add Project'. El nombre del proyecto puede ser cualquiera (ej: 'AIAgent Bootcamp'). Después de crearlo, haga clic en '+ Add App' dentro del proyecto para agregar una app")
(no_bearer -> Indicar: "Seleccione la App > abra la pestaña 'Keys and tokens'. La sección 'Bearer Token' está en el medio de la página. Haga clic en el botón 'Regenerate' para generar un nuevo token. Copie el token mostrado inmediatamente (no se puede volver a mostrar una vez que salga de la página)")
(plan_issue -> Indicar: "Seleccione 'Products' > 'Twitter API v2' en el menú izquierdo del Dashboard y haga clic en 'Subscribe' bajo el plan 'Basic'. Se requiere información de tarjeta de crédito. Después de completar la actualización, vuelva a las instrucciones del Step 2")

---

## Step 3: Guardar el Bearer Token de forma segura

**Nota importante de seguridad:**
No pegue el Bearer Token en este chat. Lo guardaremos de forma segura en una ventana de terminal separada.

**Lo que la IA ejecuta automáticamente:**
1. Verificar si el paquete `keyring` está instalado
   - Si no está instalado: Ejecutar automáticamente `pip install keyring`
2. Ejecutar `uv run python tools/credential_manager.py status` para verificar el estado actual

**Mensaje para mostrar al usuario:**

```text
Después de copiar el Bearer Token, siga estos pasos para guardarlo de forma segura:

┌─────────────────────────────────────────────────────────────┐
│ Ejecute el siguiente comando en una ventana de terminal     │
│ separada:                                                   │
│                                                             │
│ Cursor: Ctrl+` (acento grave) para abrir un nuevo terminal  │
│ Claude Code: Abrir una ventana de terminal separada         │
│                                                             │
│ uv run python tools/credential_manager.py store X_BEARER_TOKEN     │
│                                                             │
│ -> Aparecerá "Enter value for X_BEARER_TOKEN:"              │
│ -> Pegue el Bearer Token copiado y presione Enter           │
│   (El texto que escribe no se mostrará en pantalla.         │
│    Esto es normal)                                          │
│ -> "Stored X_BEARER_TOKEN" significa que se guardó           │
└─────────────────────────────────────────────────────────────┘

Una vez guardado, vuelva a este chat y dígame que "terminó".
```

**¿Por qué ejecutarlo en una ventana separada?**
Si maneja el Bearer Token en este chat de IA, el valor queda en el registro de la conversación.
Al ejecutar `credential_manager.py` en una ventana separada, el valor del token se guarda directamente
en el almacenamiento cifrado del sistema operativo (macOS Keychain / Windows Credential Locker / Linux SecretService),
y nunca aparece en archivos de texto plano ni en registros del chat.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Guardar el Bearer Token",
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
(terminal_help -> Indicar: "Para Cursor: Menú > Terminal > New Terminal, o presione Ctrl+` (Mac: Cmd+`). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra su terminal WSL (Ubuntu), o agregue una pestaña Ubuntu en Windows Terminal. Luego navegue con cd al directorio del proyecto")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `pip install keyring`)
(security_question -> Explicar: "Esta herramienta usa el almacenamiento cifrado integrado del sistema operativo. En macOS usa Keychain, en Windows usa Credential Locker y en Linux usa SecretService (GNOME Keyring, etc.). No se crean archivos de texto plano (.env). El almacenamiento también se bloquea cuando la pantalla está bloqueada, proporcionando protección contra el acceso físico")

---

## Step 4: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Primero ejecutar `credential_manager.py status` para verificar si `X_BEARER_TOKEN` está guardado en el Credential Store:
   - **Nota**: No mostrar el valor del Bearer Token en el chat. Solo mostrar salida enmascarada como "Se confirmó que el Bearer Token está configurado (primeros 4 caracteres: AAAA...)"
   - Comando de verificación de estado: `uv run python tools/credential_manager.py status`

2. Si pasa la verificación básica, enviar una solicitud de prueba real a la API de X:
   - Inyectar desde el Credential Store a variables de entorno y ejecutar la llamada API
   - Código de prueba:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     token = os.getenv("X_BEARER_TOKEN")
     if not token:
         print("Error: X_BEARER_TOKEN no está configurado.")
         sys.exit(1)
     resp = requests.get("https://api.x.com/2/tweets/search/recent",
         params={"query": "hello", "max_results": 10},
         headers={"Authorization": f"Bearer {token}"})
     if resp.status_code == 200:
         data = resp.json()
         count = data.get("meta", {}).get("result_count", 0)
         print(f"¡Conexión exitosa! Resultados de búsqueda: {count} elementos")
     elif resp.status_code == 403:
         print("Error: Acceso denegado. Se requiere plan Basic ($100/mes) o superior.")
     else:
         print(f"Error: {resp.status_code}")
         print("Verifique la re-autenticación, regeneración de clave API o configuración de permisos.")
     ```
   - Instalar automáticamente los paquetes faltantes (`requests`, `keyring`)

3. Mostrar AskQuestion según los resultados de la prueba:

**Al tener éxito en la prueba:**
```text
¡La configuración de la API de X está completa!

Resultado de la prueba: Se recibió respuesta exitosa de la API de Recent Search.
Ahora puede usar las funciones de búsqueda en tiempo real y análisis de tendencias de X (Twitter).
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
      {"id": "recheck_token", "label": "Volver a verificar el Bearer Token (volver al Step 1)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(recheck_token -> Volver al Step 1)
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
      {"id": "trouble_403", "label": "Error '403 Forbidden'"},
      {"id": "trouble_429", "label": "Error '429 Too Many Requests'"},
      {"id": "trouble_401", "label": "Error '401 Unauthorized'"},
      {"id": "trouble_approval", "label": "La solicitud del Developer Portal no se aprueba"},
      {"id": "trouble_package", "label": "Errores de paquetes de Python"},
      {"id": "trouble_cost", "label": "Me preocupa el precio"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error "403 Forbidden"
**Causa**: La API de Recent Search no está disponible en el nivel gratuito
**Indicación de la IA**: "La API de X en el nivel gratuito no admite la API de Recent Search (/2/tweets/search/recent). Se requiere una actualización al plan Basic ($100/mes) o superior. Vaya a Dashboard > Products > Twitter API v2 y suscríbase al plan Basic. Después de la actualización, no es necesario regenerar el Bearer Token (el mismo token funcionará)"

### Problema 2: Error "429 Too Many Requests"
**Causa**: Se alcanzó el límite de velocidad
**Indicación de la IA**: "La API de X tiene límites de velocidad. La API de Recent Search del plan Basic permite 60 solicitudes cada 15 minutos. Espere unos minutos e intente de nuevo. Evite enviar una gran cantidad de solicitudes en rápida sucesión"

### Problema 3: Error "401 Unauthorized"
**Causa**: El Bearer Token es inválido o no se copió correctamente
**Lo que hace la IA**:
1. Verificar el estado de almacenamiento de `X_BEARER_TOKEN` con `credential_manager.py status` (solo mostrar valor enmascarado)
2. Si no está guardado en el Credential Store, guiar el re-registro
3. Si está guardado, volver a ejecutar la prueba de API. Si falla, indicar: "Vaya a Developer Portal > App > Keys and tokens y regenere el Bearer Token"

### Problema 4: La solicitud del Developer Portal no se aprueba
**Indicación de la IA**: "Las solicitudes del Developer Portal pueden requerir revisión. Verifique lo siguiente: (1) Complete el caso de uso de forma específica y en inglés (2) Enfatice el propósito educativo, como 'Academic research and AI agent training for corporate education programs' (3) Indique claramente cómo se usarán los datos (ej: 'Analyzing public tweet trends for training purposes only'). La aprobación normalmente toma de 1 a 3 días hábiles. También es posible volver a solicitar"

### Problema 5: Errores de paquetes de Python
**Causa**: Los paquetes necesarios no están instalados
**Lo que hace la IA**: Instalar automáticamente los paquetes faltantes (`pip install requests keyring`)

### Problema 6: Preocupación por el precio
**Indicación de la IA**: "Los precios de la API de X son los siguientes: Gratuito ($0) = solo publicar, sin API de búsqueda. Basic ($100/mes) = API de Recent Search (últimos 7 días) disponible. Pro ($5,000/mes) = Full-Archive Search (todo el historial) disponible. Basic es suficiente para la capacitación. Las lecciones que no usan la API de X (creación de banners, generación de gráficos, etc.) no se ven afectadas. Si el costo no lo justifica, no dude en omitirlo"

### Problema 7: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa y guiar la solución

---

## Punto de verificación
- [ ] Solicitó una cuenta de desarrollador en X Developer Portal
- [ ] Creó un proyecto y una app
- [ ] Obtuvo el Bearer Token
- [ ] Guardó en el Credential Store con credential_manager.py store
- [ ] Confirmó el almacenamiento con credential_manager.py status
- [ ] La prueba de API fue exitosa (se recibió respuesta de la API de Recent Search)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de la API de X está completa! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_x_research", "label": "Probar la investigación de X (skill x-research)"},
      {"id": "try_marketing", "label": "Comenzar lecciones de marketing (/start-12-1)"},
      {"id": "setup_other", "label": "Configurar otras API (/start-0-1)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_x_research -> Guiar cómo usar el skill x-research
- try_marketing -> Guiar a /start-12-1
- setup_other -> Guiar a /start-0-1
- back_to_setup -> Guiar a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-x-api` para actualizar el progreso
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "Ahora puede usar la API de X con el skill x-research y las lecciones de marketing (/start-12-1)"
