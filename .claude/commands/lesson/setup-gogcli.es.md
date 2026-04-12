---
description: "Configuración de gogcli (Google Workspace CLI) (Guía completa)"
duration: "~15 min"
prerequisites: ["Tener una cuenta de Google", "Navegador disponible"]
level: "beginner"
tags: ["setup", "gogcli", "google", "gmail", "calendar", "oauth"]
---

# Configuración de gogcli (Google Workspace CLI)

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-gogcli` para mostrar el progreso
2. Detectar automáticamente la instalación y autenticación existentes:
   - Ejecutar `which gog` o `gog --version`
   - Si gogcli ya está instalado, verificar el estado de autenticación con `gog auth list`
   - Si ya está instalado y autenticado, saltar al Step 4 (prueba de funcionalidad)

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar gogcli y completar la autenticación Google OAuth para poder acceder a Gmail/Calendar/Drive/Sheets desde la CLI |
| Duración | ~15 minutos |
| Requisitos previos | Tener una cuenta de Google y un navegador disponible |
| Nivel de operación | No se necesitan comandos CLI (todo lo ejecuta automáticamente la IA + solo autenticación OAuth en el navegador) |

**Flujo de la sesión:**
1. Instalar gogcli (la IA detecta automáticamente el SO e instala)
2. Realizar la autenticación Google OAuth (la IA ejecuta el comando, usted inicia sesión en el navegador)
3. Verificar la cuenta autenticada (la IA lo ejecuta automáticamente)
4. Prueba de funcionalidad de Gmail/Calendar (la IA lo ejecuta automáticamente)

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
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(check_prereq -> Indicar: "Está listo/a si puede iniciar sesión en un navegador con una cuenta de Google. gogcli es gratuito y funciona dentro de los límites del nivel gratuito de la API de Google Workspace.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Instalar gogcli

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Linux)
2. Verificar si ya está instalado: `which gog`
3. Si no está instalado, ejecutar los siguientes comandos:

```bash
# Mac (Homebrew recomendado):
brew install nicholasgasior/tools/gog

# Mac alternativa (si Go está instalado):
go install github.com/nicholasgasior/gog@latest

# Linux (se requiere Go):
go install github.com/nicholasgasior/gog@latest
```

4. Después de la instalación, verificar con `gog --version`

**Lógica de decisión del método de instalación:**
- `which brew` tiene éxito -> Instalar vía Homebrew
- `which go` tiene éxito -> Instalar vía `go install`
- Ninguno disponible -> Guiar la instalación de Homebrew primero

**Configuración de AskQuestion:**
```json
{
  "title": "Step 1: Instalar gogcli",
  "questions": [{
    "id": "install_status",
    "prompt": "Se ejecutó la instalación de gogcli. Por favor verifique el resultado.",
    "options": [
      {"id": "installed", "label": "¡Se instaló correctamente!"},
      {"id": "brew_error", "label": "Obtuve un error con brew install"},
      {"id": "go_error", "label": "Obtuve un error con go install"},
      {"id": "no_brew_no_go", "label": "No tengo instalado ni Homebrew ni Go"},
      {"id": "command_not_found", "label": "No se encuentra el comando gog"}
    ]
  }]
}
```

(installed -> Ir al Step 2)
(brew_error -> Ejecutar `brew update && brew tap nicholasgasior/tools` y reintentar. Si sigue fallando, guiar hacia `go install`)
(go_error -> Verificar la versión de Go con `go version`. Se requiere Go 1.21 o superior. Si no está instalado, guiar hacia `brew install go`)
(no_brew_no_go -> Indicar: "Primero instalemos Homebrew. Abra https://brew.sh en su navegador y copie/ejecute el comando de instalación.")
(command_not_found -> Guiar para agregar `export PATH=$PATH:$(go env GOPATH)/bin` a la configuración del shell. Para Homebrew, ejecutar `brew link gog`)

---

## Step 2: Autenticación Google OAuth

**Lo que hace la IA:**
1. Ejecutar `gog auth add`
2. El navegador se abrirá automáticamente y mostrará la pantalla de autenticación Google OAuth

**Mensaje para mostrar al usuario:**

```text
Iniciando la autenticación Google OAuth.

┌─────────────────────────────────────────────────────────────┐
│ El navegador se abrirá automáticamente. Siga estos pasos    │
│ para autenticarse:                                          │
│                                                             │
│ 1. Seleccione su cuenta de Google en el navegador           │
│    (o inicie sesión)                                        │
│ 2. En la pantalla "¿Permitir esta aplicación?",             │
│    haga clic en "Permitir"                                  │
│ 3. Cuando aparezca "Authorization successful",              │
│    la autenticación está completa                           │
│ 4. Regrese a la terminal                                    │
│                                                             │
│ * Las credenciales se almacenan de forma segura en          │
│   ~/.config/gogcli/                                         │
│ * No es necesario ingresar claves de API manualmente        │
│   (se gestiona automáticamente vía OAuth)                   │
└─────────────────────────────────────────────────────────────┘
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Autenticación Google OAuth",
  "questions": [{
    "id": "auth_status",
    "prompt": "Por favor autentique su cuenta de Google en el navegador. ¿Pudo autenticarse?",
    "options": [
      {"id": "authenticated", "label": "¡Autenticado/a!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "auth_error", "label": "Obtuve un error de autenticación"},
      {"id": "account_help", "label": "No sé qué cuenta de Google elegir"},
      {"id": "access_denied", "label": "Aparece 'access denied'"}
    ]
  }]
}
```

(authenticated -> Ir al Step 3)
(browser_not_open -> Indicar: "Copie la URL que aparece en la terminal y péguela manualmente en su navegador.")
(auth_error -> Volver a ejecutar `gog auth add`. Verificar el mensaje de error para identificar la causa)
(account_help -> Indicar: "Seleccione la cuenta de Google que usa normalmente con Gmail. Puede ser una cuenta de Google Workspace de su empresa o una cuenta personal de Gmail. Puede agregar otra cuenta más adelante.")
(access_denied -> Indicar: "Es posible que el Google Workspace de su organización restrinja el acceso a aplicaciones externas. Consulte con su administrador de TI, o pruebe con una cuenta personal de Gmail.")

---

## Step 3: Verificación de cuenta

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `gog auth list` para mostrar la lista de cuentas autenticadas
2. Verificar que se muestre la cuenta de Google correcta

**AskQuestion de verificación:**
```json
{
  "title": "Step 3: Verificación de cuenta",
  "questions": [{
    "id": "account_check",
    "prompt": "Se muestra la cuenta autenticada. ¿Es la cuenta correcta?",
    "options": [
      {"id": "correct", "label": "¡Es la cuenta correcta!"},
      {"id": "wrong_account", "label": "Quiero usar una cuenta diferente"},
      {"id": "no_account", "label": "No se muestra ninguna cuenta"}
    ]
  }]
}
```

(correct -> Ir al Step 4)
(wrong_account -> Guiar para agregar una cuenta diferente con `gog auth add`)
(no_account -> Volver al Step 2 y repetir la autenticación OAuth)

---

## Step 4: Prueba de funcionalidad

**Lo que la IA ejecuta automáticamente:**

1. Obtener la dirección de correo electrónico de la cuenta autenticada con `gog auth list`
2. Ejecutar la prueba de búsqueda de Gmail:
   ```bash
   gog gmail search "newer_than:1d" --account <email>
   ```
3. Ejecutar la prueba de obtención de Calendar:
   ```bash
   gog calendar list --account <email> --days 1
   ```

**En caso de éxito:**
```text
¡La configuración de gogcli se completó!

Resultados de la prueba:
- Búsqueda de Gmail: Funcionando correctamente
- Obtención de Calendar: Funcionando correctamente

Ahora puede acceder a Gmail/Calendar/Drive/Sheets desde la CLI.
```

**En caso de fallo - AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de funcionalidad. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Ejecutar la prueba de nuevo"},
      {"id": "reauth", "label": "Repetir la autenticación OAuth (volver al Step 2)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(reauth -> Volver al Step 2)
(show_error -> Mostrar el mensaje de error e indicar la causa y la solución)
(skip_test -> Indicar: "Se omitió la prueba de funcionalidad. Puede verificarla más tarde con /check-setup.")

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
      {"id": "trouble_brew", "label": "Obtengo un error con brew install"},
      {"id": "trouble_auth", "label": "La autenticación OAuth falla"},
      {"id": "trouble_org", "label": "La cuenta de Google de mi organización tiene restricciones"},
      {"id": "trouble_access", "label": "Obtengo un error 'access denied'"},
      {"id": "trouble_not_found", "label": "No se encuentra el comando gog"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error con brew install
**Causa**: El tap de Homebrew no está registrado, o Homebrew está desactualizado
**Lo que hace la IA**:
1. Ejecutar `brew update`
2. Ejecutar `brew tap nicholasgasior/tools`
3. Reintentar `brew install nicholasgasior/tools/gog`
4. Si sigue fallando, guiar hacia la alternativa con `go install`

### Problema 2: La autenticación OAuth falla
**Causa**: Bloqueador de ventanas emergentes del navegador, o problemas de red
**Lo que hace la IA**:
1. Guiar para pegar manualmente la URL que aparece en la terminal en el navegador
2. Volver a ejecutar `gog auth add`
3. Guiar para verificar la configuración del bloqueador de ventanas emergentes del navegador

### Problema 3: La cuenta de Google de la organización tiene restricciones
**Causa**: El administrador de Google Workspace ha restringido el acceso a aplicaciones externas
**Indicación de la IA**: "Consulte con el administrador de TI de su organización sobre el permiso para usar gogcli. Si eso no es posible, pruebe autenticarse con una cuenta personal de Gmail (@gmail.com). Puede agregar otra cuenta con `gog auth add`."

### Problema 4: Error "access denied"
**Causa**: Permisos de alcance OAuth insuficientes, o configuración de seguridad de la cuenta
**Lo que hace la IA**:
1. Verificar el estado de autenticación con `gog auth list`
2. Guiar para eliminar y volver a autenticar: `gog auth remove <email>` y luego `gog auth add`
3. Guiar para verificar la configuración de seguridad de la cuenta de Google (https://myaccount.google.com/security)

### Problema 5: No se encuentra el comando gog
**Causa**: El PATH no está configurado
**Lo que hace la IA**:
1. Si se instaló con Homebrew: ejecutar `brew link gog`
2. Si se instaló con `go install`: guiar para agregar `export PATH=$PATH:$(go env GOPATH)/bin` a `.zshrc` / `.bashrc`
3. Guiar para ejecutar `source ~/.zshrc` o abrir una nueva terminal

### Problema 6: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar la solución

---

## Punto de control
- [ ] gogcli está instalado
- [ ] La autenticación Google OAuth está completa
- [ ] `gog auth list` muestra la cuenta
- [ ] La prueba de búsqueda de Gmail fue exitosa
- [ ] La prueba de obtención de Calendar fue exitosa

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de gogcli se completó! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_gmail", "label": "Probar búsqueda y lectura de Gmail (/start-15-1)"},
      {"id": "try_calendar", "label": "Probar operaciones de Google Calendar"},
      {"id": "try_article", "label": "Comenzar a escribir un artículo (/start-16-1)"},
      {"id": "back_to_setup", "label": "Volver a la lista de configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_gmail -> Dirigir a /start-15-1
- try_calendar -> Guiar sobre cómo usar las operaciones de Google Calendar
- try_article -> Dirigir a /start-16-1
- back_to_setup -> Dirigir a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-gogcli` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, pruebe la búsqueda y lectura de Gmail con `/start-15-1`"
