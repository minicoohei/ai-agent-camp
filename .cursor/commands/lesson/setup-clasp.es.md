---
description: "Configuración de Google Apps Script CLI (clasp) (Guía completa)"
duration: "~10 min"
prerequisites: ["Node.js 18 o superior instalado", "Tener una cuenta de Google", "Navegador disponible"]
level: "beginner"
tags: ["setup", "gas", "clasp", "google"]
---

# Configuración de Google Apps Script CLI (clasp)

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-clasp` para mostrar el progreso
2. Detectar automáticamente el estado de instalación existente:
   - Ejecutar `clasp --version`
   - Si clasp ya está instalado y `clasp list` funciona, puede ejecutar solo el Step 5 (prueba) y marcarlo como completado
   - Si no está instalado, comenzar desde el Step 1

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar clasp (Google Apps Script CLI), completar la autenticación OAuth y poder crear, editar y desplegar proyectos GAS desde su máquina local |
| Duración | ~10 minutos |
| Requisitos previos | Node.js 18+ instalado, una cuenta de Google y un navegador disponible |
| Nivel de operación | Requiere entrada de comandos CLI (npm install + clasp login) |
| Costo | Gratuito |

**Flujo de la sesión:**
1. Verificar la versión de Node.js
2. Instalar clasp globalmente vía npm (la IA lo ejecuta automáticamente)
3. Habilitar la API de Apps Script en el navegador (la IA abre el navegador automáticamente)
4. Realizar la autenticación OAuth con clasp login
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
(chrome -> Después de abrir el navegador en el Step 3, seguir la sección "Automatización con integración Chrome" para la ejecución automática)
(check_prereq -> Indicar: "Está listo/a si tiene Node.js 18+ instalado y puede iniciar sesión en un navegador con una cuenta de Google. La verificación de Node.js se hará en el siguiente paso.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Verificar Node.js

**Lo que hace la IA:**
1. Ejecutar `node --version` para verificar la versión de Node.js
2. Verificar que la versión sea 18 o superior

**Si Node.js es 18 o superior:**
Mostrar "Confirmado Node.js v{versión}. Pasando al Step 2." e ir al Step 2

**Si Node.js no está instalado o es inferior a 18 — AskQuestion:**

```json
{
  "title": "Step 1: Se requiere la instalación de Node.js",
  "questions": [{
    "id": "node_status",
    "prompt": "clasp requiere Node.js 18 o superior. Por favor instálelo desde la siguiente URL:\n\nhttps://nodejs.org/\n\nHaga clic en el botón de descarga de la versión 'LTS' y siga las instrucciones del instalador.\n\nDespués de la instalación, reinicie su terminal.",
    "options": [
      {"id": "installed", "label": "Instalé Node.js"},
      {"id": "help", "label": "No sé cómo instalarlo"},
      {"id": "skip", "label": "Configurar más tarde (omitir)"}
    ]
  }]
}
```

(installed -> Volver a ejecutar `node --version` para verificar. Si es 18+, ir al Step 2)
(help -> Indicar: "Vaya a https://nodejs.org/ y haga clic en el botón verde 'LTS' para descargar. Abra el archivo descargado y siga las instrucciones en pantalla para completar la instalación.")
(skip -> Indicar: "La configuración de clasp requiere Node.js. Vuelva a ejecutar /setup-clasp más tarde." y finalizar)

---

## Step 2: Instalar clasp

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `npm install -g @google/clasp` para instalar clasp globalmente
2. Verificar el resultado de la instalación

**Si la instalación es exitosa:**
Mostrar "La instalación de clasp se completó. Pasando al Step 3." e ir al Step 3

**Si ocurre un error de permisos (EACCES) — AskQuestion:**

```json
{
  "title": "Step 2: Error de permisos de npm",
  "questions": [{
    "id": "npm_permission",
    "prompt": "Ocurrió un error de permisos durante la instalación global de npm. Puede resolverlo con uno de estos métodos:\n\n[Método 1] Usar sudo (Mac/Linux):\nsudo npm install -g @google/clasp\n→ Se le pedirá su contraseña\n\n[Método 2] Usar npx como alternativa (sin instalación):\nnpx @google/clasp login\n→ Necesita agregar npx cada vez, pero evita el problema de permisos",
    "options": [
      {"id": "sudo", "label": "Reintentar con sudo"},
      {"id": "npx", "label": "Usar npx como alternativa"},
      {"id": "help", "label": "Quiero conocer otros métodos"}
    ]
  }]
}
```

(sudo -> Ejecutar `sudo npm install -g @google/clasp`. Si es exitoso, ir al Step 3)
(npx -> Indicar: "En los siguientes pasos, use `npx @google/clasp` en lugar de `clasp`." e ir al Step 3)
(help -> Indicar: "Puede cambiar los permisos del directorio predeterminado de npm: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally")

---

## Step 3: Habilitar la API de Apps Script

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://script.google.com/home/usersettings
# Windows:
start https://script.google.com/home/usersettings
# Linux:
xdg-open https://script.google.com/home/usersettings
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 3: Habilitar la API de Apps Script",
  "questions": [{
    "id": "api_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para habilitar la API de Apps Script:\n\n1. Inicie sesión con su cuenta de Google\n2. Busque el interruptor de 'Google Apps Script API'\n3. Active el interruptor\n\n* Si ya está activado, déjelo como está.\n\n¿Completado?",
    "options": [
      {"id": "done", "label": "¡Habilité la API! (o ya estaba activada)"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "no_toggle", "label": "No encuentro el interruptor"},
      {"id": "org_restriction", "label": "Dice que está restringido por el administrador de mi organización"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://script.google.com/home/usersettings")
(no_toggle -> Indicar: "Cerca del centro de la página, debería haber un elemento 'Google Apps Script API' con un interruptor de activación/desactivación. Intente desplazarse hacia abajo. Si no lo encuentra, asegúrese de haber iniciado sesión con su cuenta de Google.")
(org_restriction -> Indicar: "Es posible que el administrador de su organización de Google Workspace haya deshabilitado la API de Apps Script. Intente iniciar sesión con una cuenta personal de Gmail (xxx@gmail.com). Si necesita usar una cuenta de organización, solicite a su administrador de TI que habilite la API de Apps Script.")

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisito previo:** La extensión "Claude in Chrome" (v1.0.36+) debe estar instalada en Chrome, y debe haber iniciado con `claude --chrome` o ejecutado `/chrome` en la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://script.google.com/home/usersettings en el navegador
2. Usar la integración Chrome para realizar lo siguiente:
   - Encontrar el interruptor de "Google Apps Script API"
   - Si el interruptor está desactivado, hacer clic para activarlo
3. Confirmar que el interruptor está activado, luego ir al Step 4

Si la integración Chrome no está disponible, siga las instrucciones del Step 3 manualmente.

---

## Step 4: clasp login (Autenticación OAuth)

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `clasp login`
2. El navegador se abre automáticamente mostrando la pantalla de autenticación de la cuenta de Google

**Configuración de AskQuestion:**

```json
{
  "title": "Step 4: Autenticarse con la cuenta de Google",
  "questions": [{
    "id": "login_status",
    "prompt": "Se ejecutó clasp login. La pantalla de autenticación de la cuenta de Google aparecerá en el navegador:\n\n1. Seleccione la cuenta de Google que desea usar\n2. Haga clic en 'Permitir' para otorgar permisos de acceso a clasp\n3. Cuando aparezca 'Authorization successful.' en la terminal, habrá terminado\n\n¿Se completó la autenticación?",
    "options": [
      {"id": "done", "label": "¡Se mostró 'Authorization successful.'!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "permission_denied", "label": "Se muestra 'Esta aplicación está bloqueada'"},
      {"id": "timeout", "label": "Apareció la pantalla de autenticación pero la terminal no responde"}
    ]
  }]
}
```

(done -> Ir al Step 5)
(browser_not_open -> Indicar: "Si se muestra una URL en la terminal, cópiela y péguela en su navegador. Si está en un entorno remoto como SSH, intente `clasp login --no-localhost`.")
(permission_denied -> Indicar: "La política de su organización de Google Workspace puede estar bloqueando aplicaciones de terceros. Intente iniciar sesión con una cuenta personal de Gmail (xxx@gmail.com).")
(timeout -> Indicar: "Si 'Logged in!' se muestra en el navegador después de la autenticación, regrese a la terminal y verifique. Si no hay respuesta, presione Ctrl+C para cancelar y vuelva a ejecutar `clasp login`.")

---

## Step 5: Prueba de configuración

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar `clasp --version` para verificar la versión
2. Ejecutar `clasp list` para obtener la lista de proyectos
   - En el primer uso, "No script files found." o una lista vacía está bien. Si no hay errores, la autenticación fue exitosa

3. Mostrar una AskQuestion según el resultado de la prueba:

**En caso de éxito:**
```text
¡La configuración de clasp se completó!

Resultados de la prueba:
- Versión de clasp: {versión}
- Autenticación OAuth: Exitosa
- Obtención de lista de proyectos: Exitosa ({cantidad} proyectos)

Ahora puede crear, editar y desplegar proyectos de Google Apps Script desde su máquina local.
Esto se puede usar para automatizar Google Sheets, Forms y Docs.
```

**En caso de fallo — AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de clasp. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Ejecutar la prueba de nuevo"},
      {"id": "relogin", "label": "Rehacer clasp login (volver al Step 4)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(relogin -> Volver al Step 4)
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
      {"id": "trouble_npm", "label": "Obtengo un error de permisos (EACCES) con npm install"},
      {"id": "trouble_api_disabled", "label": "Obtengo un error 'Apps Script API has not been used'"},
      {"id": "trouble_browser", "label": "El navegador no se abre con clasp login"},
      {"id": "trouble_org", "label": "Estoy restringido con una cuenta de Google de organización"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error de permisos (EACCES) con npm install
**Causa**: No tiene permisos de escritura en el directorio de instalación global
**Lo que hace la IA**:
1. Sugerir reintentar con `sudo npm install -g @google/clasp`
2. Si aún no se resuelve, dirigir al cambio del directorio predeterminado de npm: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally

### Problema 2: Error "Apps Script API has not been used"
**Causa**: La API de Apps Script no está habilitada
**Lo que hace la IA**:
1. Abrir https://script.google.com/home/usersettings en el navegador
2. Indicar al usuario que verifique si el interruptor de "Google Apps Script API" está activado
3. Después de activarlo, volver a ejecutar `clasp list` para verificar

### Problema 3: El navegador no se abre con clasp login
**Causa**: Entorno remoto, conexión SSH, WSL, etc. donde no se puede abrir un navegador
**Indicación de la IA**: "Intente `clasp login --no-localhost`. Copie la URL que aparece en la terminal y péguela en su navegador manualmente para autenticarse."

### Problema 4: Restringido con cuenta de Google de organización
**Causa**: El administrador de Google Workspace ha restringido aplicaciones de terceros o la API de Apps Script
**Indicación de la IA**: "Intente `clasp login` con una cuenta personal de Gmail (xxx@gmail.com). Si necesita usar una cuenta de organización, solicite a su administrador de TI: (1) Habilitar la API de Apps Script, (2) Permitir clasp (cliente OAuth)."

### Problema 5: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar al usuario la solución

---

## Punto de control
- [ ] Node.js 18 o superior está instalado
- [ ] clasp fue instalado con `npm install -g @google/clasp`
- [ ] La API de Apps Script fue habilitada (https://script.google.com/home/usersettings)
- [ ] La autenticación OAuth se completó con `clasp login` (se mostró "Authorization successful.")
- [ ] `clasp --version` muestra la versión
- [ ] `clasp list` se ejecuta sin errores

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de clasp se completó! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "start_gas", "label": "Aprender los fundamentos de GAS (/start-10-1)"},
      {"id": "setup_other", "label": "Ir a otra configuración (/start-0-1)"},
      {"id": "check_setup", "label": "Verificar todo el entorno (/check-setup)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- start_gas -> Dirigir a /start-10-1 (Fundamentos de Clasp / gestión de proyectos GAS)
- setup_other -> Dirigir a /start-0-1
- check_setup -> Dirigir a /check-setup
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-clasp` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, aprenda los fundamentos de GAS con `/start-10-1` (Fundamentos de Clasp / gestión de proyectos GAS)"
