---
description: "Lesson command"
duration: "~2 min"
prerequisites: ["La carpeta ai-agent-camp esta abierta en Codex o Cursor"]
level: "beginner"
tags: ["setup", "check"]
---

# /check-setup -- Verificación automática del entorno

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current check-setup` para mostrar el progreso general
2. Si hay pasos incompletos, advertir: "Los siguientes pasos están incompletos: {nombres de pasos}. Se recomienda completarlos primero, pero la verificación puede ejecutarse."

---

## Qué hace este comando

La IA **verifica de forma completamente automática** el estado de su entorno de desarrollo y muestra los resultados como un informe.
Para los elementos con problemas, sugiere guiarlo al comando de configuración correspondiente o propone correcciones automáticas.

**No necesita escribir ningún comando en la terminal. La IA ejecuta todo en segundo plano.**

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Verificar la salud de su entorno y proporcionar guía de corrección si se encuentran problemas |
| Duración | ~2 min (ejecución automática) |
| Requisitos previos | La carpeta ai-agent-camp esta abierta en Codex o Cursor |
| Acción del usuario | Solo revisar los resultados (no se necesita entrada de comandos CLI) |

> **Nota para Codex**: El comando slash `/check-setup` no existe en Codex, por lo que la IA ejecuta secuencialmente los comandos de verificación listados en este documento para armar el mismo informe.

---

## Procedimiento de verificación ejecutado automáticamente por la IA

Cuando se ejecuta este comando, la IA **ejecuta automáticamente todo lo siguiente en segundo plano** y muestra los resultados como un informe resumido. No solicite al usuario que ingrese comandos.

### Verificación 1: Herramientas básicas

La IA ejecuta los siguientes comandos **en segundo plano** para verificar cada herramienta y su versión:

| Objetivo de verificación | Comando a ejecutar | Criterio de aprobación |
|--------------------------|--------------------|-----------------------|
| Tipo de SO | `uname -s` (Mac/Linux), PowerShell `$env:OS` (Windows) | Solo mostrar |
| Python | `python3 --version 2>/dev/null \|\| python --version 2>/dev/null` | Aprobado si versión 3.9+ |
| Node.js | `node --version 2>/dev/null` | Aprobado si versión 18+ |
| Git | `git --version 2>/dev/null` | Aprobado si está presente |
| GitHub CLI | `gh --version 2>/dev/null` | Aprobado si está presente |

### Verificación 2: Autenticación y APIs

La IA ejecuta los siguientes comandos **en segundo plano** para verificar el estado de autenticación y la configuración de API:

| Objetivo de verificación | Comando a ejecutar | Criterio de aprobación |
|--------------------------|--------------------|-----------------------|
| Autenticación GitHub | `gh auth status 2>&1` | Aprobado si incluye "Logged in" |
| Gemini API | Leer archivo `.env` y verificar `GEMINI_API_KEY` | Aprobado si la clave está configurada (no mostrar el valor) |
| Slack API | Leer archivo `.env` y verificar `SLACK_BOT_TOKEN` | Configurado o "se puede configurar después" |
| fal.ai API | Verificar `FAL_KEY` con `uv run python tools/credential_manager.py status` | Configurado o "se puede configurar después" |
| ElevenLabs API | Verificar `ELEVENLABS_API_KEY` con `uv run python tools/credential_manager.py status` | Configurado o "se puede configurar después" |
| Notion API | Verificar si existe entrada `notion` en archivo de configuración MCP (`~/.claude/mcp_settings.json` o `.cursor/mcp.json`) | Configurado o "se puede configurar después" |
| Clasp (GAS) | `clasp --version 2>/dev/null` | Aprobado si está presente o "se puede configurar después" |
| Typefully API | Verificar `TYPEFULLY_API_KEY` con `uv run python tools/credential_manager.py status` | Configurado o "se puede configurar después" |
| X API | Verificar `X_BEARER_TOKEN` con `uv run python tools/credential_manager.py status` | Configurado o "se puede configurar después" |
| gogcli (Google) | `gog version 2>/dev/null` | Aprobado si está presente o "se puede configurar después" |
| BigQuery/GCP | `gcloud --version 2>/dev/null` + `gcloud auth application-default print-access-token 2>/dev/null` | gcloud presente + ADC configurado o "se puede configurar después" |
| Vercel CLI | `vercel --version 2>/dev/null` + `vercel whoami 2>/dev/null` | Presente + sesión iniciada o "se puede configurar después" |

**Importante: Nunca muestre valores de claves API en pantalla. Solo muestre "Configurado" o "No configurado".**

### Verificación 3: Configuración del proyecto

La IA verifica lo siguiente **en segundo plano**:

| Objetivo de verificación | Método de verificación | Criterio de aprobación |
|--------------------------|------------------------|----------------------|
| Carpeta del proyecto | Verificar si el directorio actual es ai-agent-camp | Aprobado si el nombre del directorio contiene `ai-agent-camp` |
| Repositorio personal | Ejecutar `git remote -v` y verificar la URL de origin | Aprobado si origin apunta a `minicoohei/ai-agent-camp` o su propio fork |
| Archivo .env | Verificar si existe el archivo `.env` | Aprobado si el archivo existe |
| .gitignore | Leer `.gitignore` y verificar si `.env` está excluido | Aprobado si existe la entrada `.env` |
| Hook de seguridad | Verificar existencia y permisos de ejecución de `.git/hooks/pre-commit` | Aprobado si el archivo existe y es ejecutable |

### Verificación 4: Extensiones

La IA ejecuta el siguiente comando **en segundo plano**:
```bash
cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null
```

Extensiones a verificar:

| Extensión | ID |
|-----------|----|
| Python | `ms-python.python` |
| Marp | `marp-team.marp-vscode` |
| Draw.io | `hediet.vscode-drawio` |
| PlantUML | `jebbs.plantuml` |
| AIDE Pro | `nicepkg.aide-pro` |
| Pylance | `ms-python.vscode-pylance` |
| Prettier | `esbenp.prettier-vscode` |

---

## Formato de salida del informe

Después de completar las verificaciones, muestre los resultados al usuario en el siguiente formato:

```markdown
## Informe de verificacion del entorno

### Herramientas basicas
| Elemento | Estado | Detalles |
|----------|--------|----------|
| SO | (valor) | macOS 14.x / Windows 11 / Linux |
| Python | (aprobado/reprobado) | 3.12.x / No instalado |
| Node.js | (aprobado/reprobado) | 20.x / No instalado |
| Git | (aprobado/reprobado) | 2.x / No instalado |
| GitHub CLI | (aprobado/reprobado) | 2.x / No instalado |

### Autenticacion y APIs
| Elemento | Estado | Detalles |
|----------|--------|----------|
| Autenticacion GitHub | (aprobado/reprobado) | Sesion iniciada (nombre de usuario) / No autenticado |
| Gemini API | (aprobado/reprobado) | Configurado en .env / No configurado |
| Slack API | (aprobado/reprobado u omitible) | Configurado en .env / No configurado (se puede configurar despues) |

### Configuracion del proyecto
| Elemento | Estado | Detalles |
|----------|--------|----------|
| Carpeta del proyecto | (aprobado/reprobado) | ai-agent-camp esta abierto / Carpeta diferente |
| Repositorio personal | (aprobado/reprobado) | origin es su repositorio / Aun es upstream |
| Archivo .env | (aprobado/reprobado) | Existe / No creado |
| .gitignore | (aprobado/reprobado) | Exclusion de .env configurada / No configurado |
| Hook de seguridad | (aprobado/reprobado) | pre-commit configurado / No configurado |

### Extensiones
| Elemento | Estado |
|----------|--------|
| Python | (aprobado/reprobado) |
| Marp | (aprobado/reprobado) |
| Draw.io | (aprobado/reprobado) |
| PlantUML | (aprobado/reprobado) |
```

**Reglas de visualización de estado:**
- Aprobado: Mostrar "OK" a la derecha del nombre del elemento (ej: `Python | OK | 3.12.1`)
- Reprobado: Mostrar "Acción necesaria" a la derecha (ej: `Python | Accion necesaria | No instalado`)
- Omitible: Mostrar "Opcional" a la derecha (ej: `Slack API | Opcional | No configurado (se puede configurar despues)`)

---

## Mostrar acciones recomendadas

Después del informe, muestre acciones recomendadas si hay elementos con "Acción necesaria".

### Si existen elementos con "Acción necesaria"

```markdown
### Acciones recomendadas

Los siguientes elementos necesitan atencion:

1. Python no esta instalado
   -> Mac: Descargue el instalador de https://www.python.org/downloads/
   -> Windows: Busque "Python" en Microsoft Store e instale

2. .gitignore no esta configurado
   -> Ejecute /setup-security para configurar automaticamente

3. Extensiones faltantes
   -> Ejecute /setup-extensions para instalar automaticamente
```

**Configuración de AskQuestion:**
```json
{
  "title": "Desea corregir los problemas?",
  "questions": [{
    "id": "fix_action",
    "prompt": "Hay elementos que necesitan atencion. Que desea hacer?",
    "options": [
      {"id": "auto_fix", "label": "Corregir automaticamente todo lo que la IA pueda corregir"},
      {"id": "guide_fix", "label": "Guiarme en las correcciones una por una"},
      {"id": "extensions_only", "label": "Configurar extensiones primero (/setup-extensions)"},
      {"id": "security_only", "label": "Configurar seguridad primero (/setup-security)"},
      {"id": "skip", "label": "Omitir por ahora"}
    ]
  }]
}
```

(auto_fix -> Ejecutar todos los elementos que la IA puede corregir automáticamente)

Elementos que la IA puede corregir automáticamente:
- Configuración de .gitignore -> Agregar automáticamente entradas faltantes a `.gitignore`
- Hooks de seguridad -> Crear automáticamente `.git/hooks/pre-commit`
- Instalación de extensiones -> Ejecutar automáticamente `cursor --install-extension`
- Creación de archivo .env -> Copiar `.env.example` para crear `.env`

Elementos que requieren acción del usuario (no se pueden corregir automáticamente):
- Instalación de Python / Node.js / Git -> Proporcionar URLs de páginas de descarga
- Instalación e inicio de sesión de GitHub CLI -> Proporcionar pasos de instalación y guía GUI
- Obtención de clave de Gemini API -> Guiar a `/start-0-3`
- Creación de repositorio personal -> Guiar al Step 1.5 de `/start-0-1`

(guide_fix -> Guiar elementos con "Acción necesaria" uno por uno con AskQuestion)
(extensions_only -> Guiar a /setup-extensions)
(security_only -> Guiar a /setup-security)
(skip -> Fin)

### Si todo aprueba

```markdown
### Configuracion completada

Todos los elementos de verificacion han aprobado. Su entorno esta configurado correctamente.

**Para aprender mas efectivamente**: El curso web (https://ai-agent.camp) ofrece un tutor de IA 24/7, una aplicacion de escritorio dedicada y entornos de ejercicios interactivos. Pruebelo si aun no lo ha hecho.

Comience la primera leccion (Introduccion a generacion de banners) con /start-1-1!
```

**Configuración de AskQuestion:**
```json
{
  "title": "Configuracion completada! Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Todas las verificaciones aprobaron. Que desea hacer a continuacion?",
    "options": [
      {"id": "start_lesson", "label": "Comenzar la primera leccion (/start-1-1)"},
      {"id": "web_course", "label": "Ver el curso web (ai-agent.camp)"},
      {"id": "overview", "label": "Revisar la vista general del proyecto (/overview)"},
      {"id": "guide", "label": "Ver la guia de uso (/guide)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(web_course -> Guiar: "Puede acceder al curso web en https://ai-agent.camp. Incluye 28 modulos, 100+ lecciones, 70+ habilidades prácticas, además de un tutor de IA y una aplicación de escritorio dedicada.")

(start_lesson -> Guiar a /start-1-1)
(overview -> Guiar a /overview)
(guide -> Guiar a /guide)
(finish -> Mostrar "Excelente trabajo!")

---

## Solución de problemas comunes

**Configuración de AskQuestion:**
```json
{
  "title": "Tiene algun problema?",
  "questions": [{
    "id": "trouble",
    "prompt": "Esta experimentando algun problema?",
    "options": [
      {"id": "trouble_1", "label": "No se como instalar Python"},
      {"id": "trouble_2", "label": "No se como instalar Node.js"},
      {"id": "trouble_3", "label": "No puedo iniciar sesion en GitHub"},
      {"id": "trouble_4", "label": "No se como obtener una clave de Gemini API"},
      {"id": "trouble_5", "label": "La verificacion 'La carpeta ai-agent-camp esta abierta' fallo"},
      {"id": "no_trouble", "label": "Sin problemas"}
    ]
  }]
}
```

### Problema 1: No sabe cómo instalar Python
**Remediación de IA (pasos GUI)**:
- **Mac**: "Abra https://www.python.org/downloads/ en su navegador, haga clic en el boton 'Download Python 3.x' para descargar el instalador. Haga doble clic en el archivo descargado y siga las instrucciones en pantalla para instalar."
- **Windows**: "Abra Microsoft Store y escriba 'Python' en la barra de búsqueda. Seleccione 'Python 3.x' y haga clic en 'Obtener' para instalar. Alternativamente, descargue el instalador de https://www.python.org/downloads/. Recuerde marcar 'Add Python to PATH' durante la instalación."
- Después de la instalación: "Reinicie Cursor, luego ejecute /check-setup nuevamente."

### Problema 2: No sabe cómo instalar Node.js
**Remediación de IA (pasos GUI)**:
- **Mac**: "Abra https://nodejs.org/ en su navegador y haga clic en el boton verde 'LTS' para descargar el instalador. Haga doble clic en el archivo descargado y siga las instrucciones en pantalla para instalar."
- **Windows**: "Abra https://nodejs.org/ en su navegador y haga clic en el boton verde 'LTS' para descargar el instalador. Haga doble clic en el archivo .msi descargado y siga las instrucciones en pantalla para instalar."
- Después de la instalación: "Reinicie Cursor, luego ejecute /check-setup nuevamente."

### Problema 3: No puede iniciar sesión en GitHub
**Remediación de IA**:
1. La IA ejecuta `gh auth status` en segundo plano para verificar el estado actual
2. Si no está autenticado:
   - "Abra https://github.com/ en su navegador e inicie sesión en su cuenta"
   - "Luego escriba 'Iniciar sesión en GitHub' en el chat de Cursor. La IA le guiará a través del proceso de inicio de sesión"

### Problema 4: No sabe cómo obtener una clave de Gemini API
**Remediación de IA**:
- Guiar: "Ejecute /start-0-3 y le guiará a través del proceso de obtención de la clave API paso a paso"

### Problema 5: La verificación "La carpeta ai-agent-camp esta abierta" falló
**Remediación de IA (pasos GUI)**:
- "Desde el menu de Cursor, seleccione 'Archivo' > 'Abrir carpeta' (Mac: Cmd+O / Windows: Ctrl+O) y elija la carpeta ai-agent-camp para abrirla"
- "Después de abrir la carpeta, ejecute /check-setup nuevamente"

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Si todas las verificaciones son OK: Actualizar progreso con `uv run python tools/setup_progress.py complete check-setup`
2. Mostrar resumen de progreso actualizado
3. Si todos los pasos están completos: "La configuración está completamente terminada! Comience la primera lección con `/start-1-1`!"
4. Si quedan pasos incompletos: Guiar "Por favor complete los siguientes pasos: {nombres de pasos}"
