---
description: "Configuración de cuenta de GitHub y creación de repositorio"
duration: "~10 min"
prerequisites: ["/setup-start completado"]
level: "beginner"
tags: ["setup", "github"]
---

# Configuración de cuenta de GitHub y creación de repositorio

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-github` para mostrar el progreso
2. Verificar si ya está conectado con `gh auth status`. Si está conectado, mostrar "La autenticación de GitHub está completada."
3. Verificar si ya existe un repositorio personal con `git remote -v`. Si existe, confirmar "El repositorio también está configurado. ¿Desea omitir?"

## Lo que hará en esta sesión

**¡Bienvenido/a a la configuración de cuenta de GitHub!**

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Iniciar sesión en GitHub y crear su propio repositorio privado |
| Duración | ~10 minutos (15 minutos si necesita crear una cuenta) |
| Habilidades utilizadas | Ninguna (la IA se encarga de todo automáticamente) |
| Requisitos previos | `/setup-start` completado (Python / Node.js / Git / GitHub CLI están instalados) |
| Siguiente comando | `/start-0-1` (Verificación de configuración del entorno) |

**Flujo de la sesión:**
1. Verificar su cuenta de GitHub
2. Autenticación de GitHub (solo presionar "Permitir" en el navegador)
3. Crear su repositorio personal

> **Importante**: No necesita escribir ningún comando en la terminal. La IA se encarga de todo internamente. Cuando se abra el navegador, solo siga las instrucciones en pantalla.
> **Nota de seguridad**: No pegue contraseñas ni tokens en el chat. Toda la autenticación se realiza de forma segura a través del navegador.
> **Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.
>
> **Nota para Codex**: En Codex, en lugar de ejecutar `/setup-github` directamente, siga los pasos de verificación en este documento y proceda a través de `gh auth` secuencialmente. Solo el inicio de sesión en el navegador y los clics en botones de autorización son realizados por el usuario.

---

## Confirmación antes de la sesión

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
      {"id": "check_prereq", "label": "Aún no he realizado /setup-start"},
      {"id": "what_is_github", "label": "¿Qué es GitHub?"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Cuando se necesite crear una cuenta en el Step 1, después de abrir el navegador, seguir la sección "Automatización con integración Chrome" para la ejecución automática)
(check_prereq -> Indicar: "Ejecute /setup-start primero. Verificará que el software necesario esté instalado.")
(what_is_github -> Indicar: "GitHub es un servicio en la nube para almacenar y gestionar programas y archivos de forma segura. Piense en él como la versión para programadores de Google Drive. En este curso, lo usaremos para guardar su trabajo. Es gratuito." -> Ir al Step 1)

---

## Step 1: Verificar su cuenta de GitHub

**Configuración de AskQuestion:**
```json
{
  "title": "Step 1: Verificación de cuenta de GitHub",
  "questions": [{
    "id": "has_account",
    "prompt": "¿Tiene una cuenta de GitHub?",
    "options": [
      {"id": "yes", "label": "Sí, tengo una"},
      {"id": "no", "label": "No (quiero crear una)"},
      {"id": "not_sure", "label": "No estoy seguro/a"}
    ]
  }]
}
```

### Si tiene una cuenta (yes)

-> Ir al Step 2

### Si no tiene una cuenta (no)

**Lo que la IA ejecuta automáticamente:**
Primero, ejecutar `uname -s` para detectar el SO (si ya se detectó en el Step 1, usar ese resultado).

Mostrar:
```text
Vamos a crear una cuenta de GitHub.
La IA abrirá el navegador automáticamente. Espere un momento...
```

```bash
# La IA ejecuta:
# Mac:
open https://github.com/signup
# Windows:
start https://github.com/signup
```

**Instrucciones para la creación de cuenta:**
```text
Una vez que se abra el navegador, siga estos pasos:

1. Ingrese su dirección de correo electrónico y haga clic en "Continue"
2. Establezca una contraseña y haga clic en "Continue"
   (Use una contraseña de 8+ caracteres, incluyendo números o símbolos)
3. Elija un nombre de usuario y haga clic en "Continue"
   (Solo caracteres alfanuméricos y guiones. Ejemplo: taro-yamada)
4. Elija su preferencia de notificaciones por correo y haga clic en "Continue"
5. Resuelva la verificación de puzzle y haga clic en "Create account"
6. Se enviará un código de confirmación a su correo registrado
7. Ingrese el código de 6 dígitos del correo

Cuando la creación de la cuenta esté completa, escriba "listo" aquí.
```

### Automatización con integración Chrome (modo `/chrome`, solo para creación de cuenta nueva)

**Requisito previo:** La extensión "Claude in Chrome" (v1.0.36+) debe estar instalada en Chrome, y debe haber iniciado con `claude --chrome` o ejecutado `/chrome` en la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://github.com/signup en el navegador
2. Usar la integración Chrome para realizar las siguientes operaciones en orden:
   - Enfocar el campo de correo electrónico y solicitar al usuario que lo ingrese
   - Hacer clic en "Continue"
   - Hacer clic en "Continue" después de ingresar la contraseña
   - Hacer clic en "Continue" después de ingresar el nombre de usuario
   - Hacer clic en "Continue" después de la configuración de notificaciones
   - Dejar la verificación de puzzle al usuario
   - Hacer clic en "Create account"
3. La entrada del código de confirmación por correo la realiza el usuario manualmente
4. Después de completar la creación de la cuenta, ir al Step 2

**Nota:** No leer valores de contraseña o correo electrónico desde la pantalla del navegador.

Si la integración Chrome no está disponible, siga los pasos anteriores manualmente.

**Configuración de AskQuestion (verificación de finalización):**
```json
{
  "title": "Confirmación de creación de cuenta",
  "questions": [{
    "id": "account_created",
    "prompt": "¿Se completó la creación de la cuenta de GitHub?",
    "options": [
      {"id": "done", "label": "¡Completado!"},
      {"id": "stuck", "label": "Me quedé atascado/a a mitad de camino"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"}
    ]
  }]
}
```

(done -> Ir al Step 2)
(stuck -> "¿En qué pantalla está? Dígame qué se muestra en su pantalla." y asistir)
(browser_not_open -> Indicar: "Abra su navegador y escriba https://github.com/signup en la barra de direcciones.")

### Si no está seguro/a (not_sure)

Mostrar:
```text
Vamos a verificar. ¿Le resulta familiar alguna de las siguientes?
- Recibió un correo de confirmación de registro de GitHub
- Puede iniciar sesión en https://github.com

Si no está seguro/a, no hay problema en crear una cuenta nueva.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Verificación de cuenta",
  "questions": [{
    "id": "account_check",
    "prompt": "¿Qué desea hacer?",
    "options": [
      {"id": "try_login", "label": "Intentar iniciar sesión (abrir navegador)"},
      {"id": "create_new", "label": "Crear una nueva"}
    ]
  }]
}
```

(try_login -> La IA ejecuta `open https://github.com/login` / `start https://github.com/login` para abrir el navegador -> Si el inicio de sesión es exitoso, ir al Step 2; si no, ir al flujo de creación de cuenta nueva)
(create_new -> Ir al flujo de "Si no tiene una cuenta" anterior)

---

## Step 2: Autenticación de GitHub

**Lo que la IA ejecuta automáticamente:**

### 2-1. Verificar autenticación existente

Primero, ejecutar `gh auth status` para verificar si ya está conectado.

**Si ya está conectado:**
```text
Está conectado a GitHub como {nombre_de_usuario}.
```
-> Ir al Step 3

**Si no está conectado:**

### 2-2. Iniciar autenticación por navegador

Mostrar:
```text
Iniciando sesión en GitHub.
La IA abrirá el navegador automáticamente. Siga estos pasos:
```

```bash
La IA ejecuta: gh auth login --web -p https
```

Este comando tiene dos resultados posibles:

**Patrón A: El navegador se abre automáticamente**
```text
El navegador se abrió automáticamente.
Haga clic en el botón verde "Authorize GitHub CLI" en la pantalla.
El resultado aparecerá automáticamente en este chat cuando termine.
```

**Patrón B: Se muestra un código de 8 dígitos**

Leer el código de 8 dígitos (por ejemplo, `XXXX-XXXX`) de la salida del comando e indicar:
```text
Se ha abierto una página de autenticación en el navegador.
Ingrese el siguiente código en la pantalla:

    XXXX-XXXX

(Ingrese este código exactamente como se muestra)

Pasos:
1. Se muestra un campo de entrada de 8 dígitos en el navegador
2. Ingrese el código anterior y haga clic en "Continue"
3. Haga clic en el botón verde "Authorize GitHub CLI"
4. El resultado aparecerá automáticamente en este chat cuando termine
```

Si el navegador no se abre:
```text
Si el navegador no se abrió, abra la siguiente URL en su navegador:
https://github.com/login/device

Luego ingrese el código anterior.
```

### 2-3. Verificar resultado de la autenticación

La IA ejecuta `gh auth status` para verificar el resultado.

**Si la autenticación fue exitosa:**
```text
¡Autenticación exitosa! Ahora está conectado a GitHub como {nombre_de_usuario}.
```
-> Ir al Step 3

**Si la autenticación falló:**

**Configuración de AskQuestion:**
```json
{
  "title": "Ocurrió un problema de autenticación",
  "questions": [{
    "id": "auth_trouble",
    "prompt": "Parece que la autenticación no funcionó. Cuénteme su situación.",
    "options": [
      {"id": "retry", "label": "Intentar de nuevo"},
      {"id": "browser_issue", "label": "El navegador no se abrió"},
      {"id": "code_expired", "label": "La pantalla de entrada del código desapareció"},
      {"id": "other_error", "label": "Se mostró un mensaje de error"}
    ]
  }]
}
```

(retry -> Volver a ejecutar `gh auth login --web -p https`)
(browser_issue -> Indicar: "Abra su navegador y vaya a https://github.com/login/device" y volver a mostrar el código)
(code_expired -> "El código puede haber expirado. Ejecutándolo de nuevo." -> Volver a ejecutar `gh auth login --web -p https`)
(other_error -> "Dígame el mensaje de error que se muestra." y asistir)

---

## Step 3: Crear su repositorio personal

**Lo que la IA ejecuta automáticamente:**

### 3-1. Verificar estado actual

La IA ejecuta lo siguiente en orden:
1. Obtener el nombre de usuario de `gh auth status`
2. Verificar la configuración remota actual con `git remote -v`

### 3-2. Acciones según el estado

**Caso A: El repositorio personal ya está configurado**
(La URL de origin en `git remote -v` contiene el nombre de usuario)

Mostrar:
```text
Su repositorio personal ya está configurado.
  Repositorio: https://github.com/{nombre_de_usuario}/ai-agent-camp

Sin problemas. Pasemos al siguiente paso.
```
-> Ir a la sección de Finalización

**Caso B: origin todavía apunta a minicoohei/ai-agent-camp (fuente de distribución del curso)**

Mostrar:
```text
La configuración actual apunta al repositorio de distribución del curso.
Crearemos su repositorio privado personal.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Crear repositorio personal",
  "questions": [{
    "id": "create_repo",
    "prompt": "Crearemos un repositorio privado llamado {nombre_de_usuario}/ai-agent-camp para usted. ¿Está de acuerdo?",
    "options": [
      {"id": "yes", "label": "Crear"},
      {"id": "different_name", "label": "Quiero un nombre diferente"},
      {"id": "explain", "label": "¿Qué es un repositorio?"}
    ]
  }]
}
```

(yes -> Ejecutar la creación del repositorio)
(different_name -> "¿Qué nombre desea? Puede usar caracteres alfanuméricos y guiones." y aceptar la entrada)
(explain -> "Un repositorio es un lugar de almacenamiento de archivos. Piense en él como una carpeta de Google Drive. Se configurará como privado, por lo que solo usted podrá acceder." -> Volver a mostrar la AskQuestion)

**Ejecutar la creación del repositorio:**

La IA ejecuta lo siguiente en orden:

1. Renombrar origin existente a upstream (mantener como fuente de distribución del curso):
   ```bash
   git remote rename origin upstream
   ```
   (Omitir si upstream ya existe)

2. Crear repositorio personal y configurar como origin:
   ```bash
   gh repo create {nombre_de_usuario}/ai-agent-camp --private --source . --remote origin --push
   ```

3. Verificar el resultado:
   ```bash
   git remote -v
   ```

**En caso de éxito:**
```text
¡Su repositorio privado personal ha sido creado!

  URL del repositorio: https://github.com/{nombre_de_usuario}/ai-agent-camp
  Visibilidad: privado (solo usted puede acceder)

Sus entregables del curso ahora se guardarán de forma segura.
```
-> Ir a la sección de Finalización

**En caso de fallo:**

La IA analiza el mensaje de error e identifica la causa:

- "already exists" -> Ya existe un repositorio con el mismo nombre:
  ```text
  Ya existe un repositorio con el mismo nombre.
  ```
  **Configuración de AskQuestion:**
  ```json
  {
    "title": "El repositorio ya existe",
    "questions": [{
      "id": "repo_exists",
      "prompt": "Se encontró un repositorio con el mismo nombre. ¿Qué desea hacer?",
      "options": [
        {"id": "use_existing", "label": "Usar el repositorio existente"},
        {"id": "different_name", "label": "Crear con un nombre diferente"}
      ]
    }]
  }
  ```
  (use_existing -> La IA ejecuta `git remote add origin https://github.com/{nombre_de_usuario}/ai-agent-camp.git` y `git push -u origin main`)
  (different_name -> "¿Qué nombre desea?" y aceptar la entrada, luego volver a ejecutar con ese nombre)

- "permission denied" -> Problema de autenticación:
  -> Volver al flujo de autenticación del Step 2

- Otros errores -> Mostrar el contenido del error y preguntar "Dígame qué se muestra en su pantalla." para asistir

**Caso C: No existe origin**
(`git remote -v` no muestra nada)

Mostrar:
```text
No hay repositorio remoto configurado.
Crearemos un nuevo repositorio privado para usted.
```
-> Ejecutar los mismos pasos de "Ejecutar la creación del repositorio" del Caso B (pero omitir el paso 1 de renombrar)

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
      {"id": "trouble_1", "label": "El navegador no se abre"},
      {"id": "trouble_2", "label": "No hay pantalla para ingresar el código de autenticación"},
      {"id": "trouble_3", "label": "Obtengo un error al crear el repositorio"},
      {"id": "trouble_4", "label": "Olvidé mi contraseña de GitHub"},
      {"id": "trouble_5", "label": "Otro problema"}
    ]
  }]
}
```

### Problema 1: "El navegador no se abre"
**Causa**: Configuración del navegador predeterminado o bloqueo del software de seguridad
**Solución**:
```text
Abra el navegador manualmente y vaya a una de estas URLs:
- Creación de cuenta: https://github.com/signup
- Inicio de sesión: https://github.com/login
- Autenticación de dispositivo: https://github.com/login/device
```

### Problema 2: "No hay pantalla para ingresar el código de autenticación"
**Causa**: Se abrió en otra pestaña del navegador o bloqueador de ventanas emergentes
**Solución**:
```text
1. Verifique las pestañas de su navegador (puede haberse abierto una nueva pestaña)
2. Si no la encuentra, abra https://github.com/login/device en su navegador
3. Ingrese el código mostrado
```

### Problema 3: "Error al crear el repositorio"
**Causa**: Autenticación expirada, problemas de red o permisos insuficientes
**Solución**:
La IA ejecuta `gh auth status` para verificar el estado de autenticación.
- Autenticación expirada -> Volver al flujo de autenticación del Step 2
- Problema de red -> Indicar que verifique la conexión a internet
- Permisos insuficientes -> Ejecutar `gh auth refresh -s repo` para actualizar permisos

### Problema 4: "Olvidé mi contraseña de GitHub"
**Solución**:
```text
La IA abrirá la página de restablecimiento de contraseña.
```
```bash
# La IA ejecuta:
# Mac:
open https://github.com/password_reset
# Windows:
start https://github.com/password_reset
```

```text
1. Ingrese su dirección de correo electrónico y haga clic en "Send password reset email"
2. Haga clic en el enlace del correo que recibirá
3. Establezca una nueva contraseña
4. Una vez completado, escriba "listo" aquí
```

### Problema 5: "Otro problema"
**Solución**:
```text
¿Qué tipo de problema tiene? Dígame el mensaje de error o la situación en su pantalla.
La IA diagnosticará la causa y sugerirá una solución.
```

---

## Punto de control

La IA verifica automáticamente todos los elementos y muestra los resultados:

| Elemento | Comando de verificación | Resultado esperado |
|----------|------------------------|-------------------|
| Autenticación de GitHub | `gh auth status` | Se muestra el nombre de usuario |
| Repositorio remoto | `git remote -v` | origin apunta a su repositorio |
| Estado de Push | `git log --oneline -1` | Existe el último commit |

---

## Finalización

```text
¡Felicitaciones! ¡La configuración de GitHub está completa!

  Nombre de usuario de GitHub: {nombre_de_usuario}
  URL del repositorio: https://github.com/{nombre_de_usuario}/ai-agent-camp
  Visibilidad: privado (solo usted puede acceder)

Ya está listo/a para comenzar el curso.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija qué hacer a continuación",
    "options": [
      {"id": "next_lesson", "label": "Comenzar el curso (/start-0-1)"},
      {"id": "view_repo", "label": "Ver el repositorio creado en el navegador"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

(next_lesson -> Indicar: "Abra un nuevo chat y escriba /start-0-1")
(view_repo -> La IA ejecuta `open https://github.com/{nombre_de_usuario}/ai-agent-camp` / `start https://github.com/{nombre_de_usuario}/ai-agent-camp` para mostrar en el navegador -> Luego indicar: "Para comenzar el curso, abra un nuevo chat y escriba /start-0-1")
(finish -> Indicar: "¡Buen trabajo! Cuando esté listo/a para comenzar el curso, escriba /start-0-1.")

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-github` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, configure la API de Gemini con `/setup-gemini`"
