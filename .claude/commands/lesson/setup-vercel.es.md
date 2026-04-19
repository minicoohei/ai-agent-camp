---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Node.js 18 o superior instalado", "Navegador disponible"]
level: "beginner"
tags: ["setup", "vercel", "deploy", "hosting"]
---

# Configuración de Vercel CLI

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-vercel` para mostrar el progreso
2. Detectar automáticamente el estado de instalación existente:
   - Ejecutar `vercel --version` para verificar si el CLI está instalado
   - Ejecutar `vercel whoami` para verificar si ya inició sesión
   - Si ambos tienen éxito, saltar al Step 4 (prueba)
3. **Esta configuración es opcional.** Vercel CLI se usa en la Lección 15-5 (Producción de LP - Deploy en Vercel). Puede omitirla si no la necesita de inmediato.

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar Vercel CLI, iniciar sesión y estar listo para desplegar y publicar sitios web |
| Duración | ~10 minutos |
| Requisitos previos | Node.js 18 o superior instalado, navegador disponible |
| Nivel de operación | Se requiere entrada de comandos CLI (la instalación la ejecuta la IA automáticamente + autenticación del navegador) |
| Precio | Plan gratuito (Hobby) con proyectos personales ilimitados. El nivel gratuito es suficiente para la capacitación |

**Flujo de la sesión:**
1. Crear una cuenta de Vercel (registro en el navegador)
2. Instalar Vercel CLI (la IA lo ejecuta automáticamente)
3. Iniciar sesión en Vercel (autenticación del navegador o autenticación con token)
4. Prueba de operación (la IA la ejecuta automáticamente)

> **Consejo**: Si la IA deja de responder a mitad del proceso, escriba "por favor continúa" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo? (Esta configuración es opcional. Se usa en la Lección 15-5)",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "chrome", "label": "Automatizar operaciones del navegador con /chrome"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "skip", "label": "No lo necesito ahora, omitir"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Después de abrir el navegador en Step 1, seguir la sección "Automatización con integración Chrome")
(check_prereq -> Indicar: "Se requiere Node.js 18 o superior. Puede verificarlo con `node --version`")
(skip -> Indicar: "Omitido. Puede configurarlo nuevamente más tarde con `/setup-vercel` cuando sea necesario" y finalizar)
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Crear cuenta de Vercel

**Lo que hace la IA:**
1. Detectar automáticamente el sistema operativo (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://vercel.com/signup
# Windows:
start https://vercel.com/signup
# Linux:
xdg-open https://vercel.com/signup
```

**Una vez que se abra el navegador, mostrar el siguiente AskQuestion:**

```json
{
  "title": "Step 1: Crear cuenta de Vercel",
  "questions": [{
    "id": "account_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para crear una cuenta:\n\n1. Haga clic en 'Continue with GitHub' (recomendado)\n   - Puede registrarse directamente con su cuenta de GitHub\n   - O elija 'Continue with GitLab' o 'Continue with Email'\n2. Complete la autenticación / verificación de correo\n3. La creación de cuenta está completa\n\nIndíqueme el estado de su cuenta:",
    "options": [
      {"id": "created", "label": "¡Cuenta creada!"},
      {"id": "already_have", "label": "Ya tengo una cuenta"},
      {"id": "no_github", "label": "No tengo cuenta de GitHub"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"}
    ]
  }]
}
```

(created -> Ir al Step 2)
(already_have -> Ir al Step 2)
(no_github -> Indicar: "También puede registrarse con Email. Seleccione 'Continue with Email' en la página de registro. O también puede primero crear una cuenta de GitHub con `/setup-github`")
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://vercel.com/signup")

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisitos previos:** La extensión "Claude in Chrome" (v1.0.36+) está instalada en Chrome, y se inició con `claude --chrome` o se ejecutó `/chrome` dentro de la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://vercel.com/signup en el navegador
2. Usar la integración Chrome para ejecutar:
   - Hacer clic en "Continue with GitHub"
   - Si aparece la pantalla de autenticación de GitHub, solicitar al usuario que apruebe
3. Una vez confirmado el registro, ir al Step 2

Si la integración Chrome no está disponible, siga los pasos manuales del Step 1.

---

## Step 2: Instalar Vercel CLI

**Lo que la IA ejecuta automáticamente:**
1. Verificar la versión de Node.js:
   ```bash
   node --version
   ```
   - Si es inferior a Node.js 18: Indicar "Se requiere Node.js 18 o superior. Configure con `/start-0-1`" y detener
2. Instalar Vercel CLI:
   ```bash
   npm i -g vercel
   ```
   - En caso de error de permisos (`EACCES`): Indicar `sudo npm i -g vercel`
3. Verificar la instalación:
   ```bash
   vercel --version
   ```

**Al tener éxito en la instalación:**
```text
¡Vercel CLI ha sido instalado! (Versión: XX.X.X)
A continuación, iniciaremos sesión en su cuenta de Vercel.
```

**AskQuestion en caso de fallo en la instalación:**
```json
{
  "title": "Ocurrió un error de instalación",
  "questions": [{
    "id": "install_error",
    "prompt": "Ocurrió un error al instalar Vercel CLI.",
    "options": [
      {"id": "retry", "label": "Intentar de nuevo"},
      {"id": "sudo", "label": "Intentar con privilegios de administrador (sudo)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip", "label": "Omitir e intentar más tarde"}
    ]
  }]
}
```

(retry -> Volver a ejecutar `npm i -g vercel`)
(sudo -> Ejecutar `sudo npm i -g vercel`)
(show_error -> Mostrar mensaje de error con causa y solución)
(skip -> Indicar: "Omitido. Puede configurarlo nuevamente más tarde con `/setup-vercel`")

---

## Step 3: Inicio de sesión en Vercel

**Indicar que hay dos métodos: Método A (entorno interactivo, recomendado) y Método B (entorno no interactivo, autenticación con token).**

**Lo que hace la IA:**
1. Primero intentar el Método A: Ejecutar `vercel login`
2. El navegador se abre automáticamente y se autentica con la cuenta de Vercel
3. Si aparece "Congratulations!" en el terminal, el inicio de sesión está completo

**Mensaje para mostrar al usuario:**

```text
Iniciaremos sesión en Vercel.

┌─────────────────────────────────────────────────────────────┐
│ Método A (recomendado): Autenticación del navegador         │
│                                                             │
│ Al ejecutar `vercel login` se abrirá su navegador.          │
│ Autentíquese con su cuenta de Vercel para completar.        │
│                                                             │
│ Método B (entornos no interactivos): Autenticación con      │
│ token                                                       │
│                                                             │
│ Para CI/CD o cuando no hay navegador disponible:            │
│ 1. Cree un token en https://vercel.com/account/tokens       │
│ 2. En un terminal separado, ejecute:                        │
│    uv run python tools/credential_manager.py store VERCEL_TOKEN    │
│ 3. Use la opción --token al desplegar                       │
└─────────────────────────────────────────────────────────────┘
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Inicio de sesión en Vercel",
  "questions": [{
    "id": "login_status",
    "prompt": "Se ejecutó `vercel login`. ¿Cuál es el resultado?",
    "options": [
      {"id": "done", "label": "Sesión iniciada (apareció Congratulations!)"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "non_interactive", "label": "Estoy en un entorno no interactivo (quiero autenticación con token)"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(browser_not_open -> Indicar: "Si el navegador no se abre, copie la URL mostrada en el terminal y péguela en su navegador manualmente. Si eso tampoco funciona, pruebe el Método B (autenticación con token)")
(non_interactive -> Guiar el flujo de autenticación con token a continuación)

### Método B: Autenticación con token (para entornos no interactivos)

**Lo que hace la IA:**
1. Abrir la página de creación de tokens en el navegador:
   ```bash
   # Mac:
   open https://vercel.com/account/tokens
   # Windows:
   start https://vercel.com/account/tokens
   # Linux:
   xdg-open https://vercel.com/account/tokens
   ```

**Mensaje para mostrar al usuario:**

```text
Configuraremos con autenticación con token.

┌─────────────────────────────────────────────────────────────┐
│ Siga estos pasos en una ventana de terminal separada:       │
│                                                             │
│ 1. Abra https://vercel.com/account/tokens en el navegador   │
│ 2. Haga clic en el botón "Create" para crear un token       │
│ 3. Copie el token                                           │
│ 4. En un terminal separado, ejecute:                        │
│                                                             │
│    uv run python tools/credential_manager.py store VERCEL_TOKEN    │
│                                                             │
│ -> Aparecerá "Enter value for VERCEL_TOKEN:"                │
│ -> Pegue el token copiado y presione Enter                  │
│   (El texto que escribe no se mostrará en pantalla.         │
│    Esto es normal)                                          │
│ -> "Stored VERCEL_TOKEN" significa que se guardó             │
└─────────────────────────────────────────────────────────────┘

Una vez guardado, vuelva a este chat y dígame que "terminó".
```

**AskQuestion para almacenamiento de token:**
```json
{
  "title": "Autenticación con token",
  "questions": [{
    "id": "token_status",
    "prompt": "¿Pudo guardar el token en un terminal separado?",
    "options": [
      {"id": "done", "label": "¡Guardado!"},
      {"id": "terminal_help", "label": "No sé cómo abrir un terminal"},
      {"id": "command_error", "label": "El comando dio un error"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(terminal_help -> Indicar: "Para Cursor: Menú > Terminal > New Terminal, o presione Ctrl+` (Mac: Cmd+`). Para Claude Code: Abra una ventana/pestaña de terminal separada. Mac: Cmd+T (nueva pestaña) o Cmd+N (nueva ventana). Windows: Abra su terminal WSL (Ubuntu), o agregue una pestaña Ubuntu en Windows Terminal. Luego navegue con cd al directorio del proyecto")
(command_error -> La IA ejecuta `uv run python tools/credential_manager.py status` para verificar la situación e identificar la causa. Si keyring no está instalado, ejecutar automáticamente `uv add keyring`)

---

## Step 4: Prueba

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar pruebas según el método de inicio de sesión:
   - **Método A (autenticación del navegador)**: Ejecutar `vercel whoami` -- éxito si aparece el nombre de usuario
   - **Método B (autenticación con token)**: Primero verificar si `VERCEL_TOKEN` está guardado con `uv run python tools/credential_manager.py status`, luego obtener el token del credential_manager y verificar con `vercel whoami --token <TOKEN>`

**Al tener éxito en la prueba:**
```text
¡La configuración de Vercel CLI está completa!

Resultado de la prueba: Se confirmó el nombre de usuario "xxxxx".
Ahora puede desplegar y publicar sitios web.
```

**AskQuestion en caso de fallo en la prueba:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error con `vercel whoami`. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Intentar la prueba de nuevo"},
      {"id": "relogin", "label": "Iniciar sesión de nuevo (volver al Step 3)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(relogin -> Volver al Step 3)
(show_error -> Mostrar mensaje de error con causa y solución)
(skip_test -> Indicar: "Prueba omitida. Puede verificar más tarde con `/check-setup`")

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
      {"id": "trouble_permission", "label": "Error de permisos de npm (EACCES)"},
      {"id": "trouble_notfound", "label": "'vercel: command not found'"},
      {"id": "trouble_browser", "label": "La autenticación del navegador falla"},
      {"id": "trouble_node", "label": "La versión de Node.js es muy antigua"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error de permisos de npm (EACCES)
**Causa**: Se necesitan privilegios de administrador para la instalación global
**Lo que hace la IA**:
1. Indicar `sudo npm i -g vercel`
2. Si eso no funciona, guiar para cambiar el directorio de instalación con `npm config set prefix ~/.npm-global` y agregar `~/.npm-global/bin` al PATH

### Problema 2: "vercel: command not found"
**Causa**: PATH no configurado, o instalación incompleta
**Lo que hace la IA**:
1. Verificar la ubicación de instalación con `which vercel` o `npm list -g vercel`
2. Si necesita agregar al PATH, guiar para agregar al archivo de configuración del shell (`.zshrc` / `.bashrc`)
3. Reiniciar el terminal o ejecutar `source ~/.zshrc`

### Problema 3: La autenticación del navegador falla
**Causa**: Error de comunicación entre el navegador y el CLI, o firewall
**Indicación de la IA**: "Intente ejecutar `vercel login` de nuevo. Si el navegador no se abre, copie la URL mostrada en el terminal y péguela en su navegador manualmente. Si eso tampoco funciona, pruebe el Método B (autenticación con token)"

### Problema 4: La versión de Node.js es muy antigua
**Causa**: Se instaló una versión de Node.js inferior a 18
**Lo que hace la IA**:
1. Verificar la versión actual con `node --version`
2. Guiar la actualización a Node.js 18 o superior (`nvm install 18` o descargar desde el sitio oficial)

### Problema 5: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa y guiar la solución

---

## Punto de verificación
- [ ] Creó una cuenta de Vercel
- [ ] Vercel CLI está instalado (vercel --version)
- [ ] Inició sesión en Vercel (vercel whoami)
- [ ] La prueba fue exitosa (se mostró el nombre de usuario)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de Vercel CLI está completa! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_deploy", "label": "Probar producción de LP y deploy (/start-15-5)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_deploy -> Guiar a /start-15-5
- back_to_setup -> Guiar a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-vercel` para actualizar el progreso
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "A continuación, probemos la producción de LP y el deploy en Vercel con `/start-15-5`"
