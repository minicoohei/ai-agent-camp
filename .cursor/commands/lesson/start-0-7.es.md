---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "~15 min"
prerequisites: ["Node.js 18 o superior instalado", "Familiarizado con operaciones de terminal"]
level: "beginner"
tags: ["setup", "claude-code", "cli"]
nonInteractiveMode: incompatible
---
# Lección 0-7: Configuración de Claude Code

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar Claude Code, completar la autenticación e inicialización del proyecto. Comprender cómo usar los comandos slash y los skills |
| Duración | ~15 min |
| Requisitos previos | Node.js 18 o superior instalado; familiarizado con operaciones de terminal |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Si la IA deja de responder, escriba "por favor continua" o "se detuvo" para reanudar.

---

## Qué es Claude Code?

Claude Code es la herramienta CLI oficial de Anthropic. Puede llamar a Claude directamente desde la terminal para editar código, manipular archivos y ejecutar comandos usando lenguaje natural.

Diferencias con Cursor:
- **Cursor**: Usar IA dentro de un editor GUI (chat y edición en línea)
- **Claude Code**: Usar IA desde la terminal (basado en CLI, adecuado para automatización)

Puede tomar las lecciones de este currículo con cualquiera de las dos herramientas.

---

## Step 1: Instalación

Instale Claude Code globalmente via npm.

```bash
npm install -g @anthropic-ai/claude-code
```

Después de la instalación, verifique la versión:

```bash
claude --version
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 1: Instalacion",
  "questions": [{
    "id": "install_status",
    "prompt": "Cual es el estado de su instalacion de Claude Code?",
    "options": [
      {"id": "not_installed", "label": "Instalar ahora (ejecutar el comando anterior)"},
      {"id": "already_installed", "label": "Ya esta instalado"},
      {"id": "error", "label": "Obtuve un error durante la instalacion"}
    ]
  }]
}
```

(not_installed -> Ejecutar `npm install -g @anthropic-ai/claude-code` y verificar el resultado)
(already_installed -> Ir al Step 2)
(error -> Verificar si Node.js es 18+ con `node --version`. Guiar para limpiar cache de npm con `npm cache clean --force`)

---

## Step 2: Autenticación (Inicio de sesión OAuth)

Claude Code inicia automáticamente el flujo de autenticación en el primer inicio. Ejecutar el siguiente comando abrirá su navegador:

```bash
claude
```

Inicie sesión en su cuenta de Anthropic en el navegador y complete la autenticación.

> **Nota**: Se requiere un plan Claude Pro / Max / Team / Enterprise. El plan gratuito no es compatible.
>
> **Para autenticar con clave API**: Ejecute `source ./.env` primero (si `ANTHROPIC_API_KEY` está configurada en `.env`), luego inicie `claude`.
>
> **Para re-autenticar dentro de una sesión**: Escriba `/login` en el chat de Claude Code.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Autenticacion",
  "questions": [{
    "id": "auth_status",
    "prompt": "Cual es el estado de su autenticacion?",
    "options": [
      {"id": "run_auth", "label": "Iniciar autenticacion (ejecutar claude)"},
      {"id": "already_authed", "label": "Ya estoy autenticado"},
      {"id": "api_key", "label": "Quiero autenticar con clave API"},
      {"id": "error", "label": "Obtuve un error durante la autenticacion"}
    ]
  }]
}
```

(run_auth -> Ejecutar `claude`. El navegador se abre en el primer inicio y comienza el flujo de autenticación)
(already_authed -> Ir al Step 3)
(api_key -> Guiar para configurar `ANTHROPIC_API_KEY=sk-ant-...` en `.env`, ejecutar `source ./.env`, luego iniciar `claude`)
(error -> Verificar estado con `claude auth status` y guiar solución de problemas. Dentro de una sesión, re-autenticar con `/login`)

---

## Step 3: Inicialización del proyecto

Inicie `claude` en la raíz del repositorio ai-agent-camp:

```bash
cd /path/to/ai-agent-camp
claude
```

En el primer inicio, Claude Code automáticamente:

1. Lee `CLAUDE.md` para entender la configuración del proyecto
2. Reconoce los comandos bajo `.claude/commands/`
3. Reconoce los skills bajo `skills/`

---

## Step 4: Cómo usar los comandos slash

En Claude Code, puede invocar lecciones y utilidades con **`/nombre-del-comando`**.

### Cómo iniciar una lección

```text
/start-0-1    -> Verificacion de configuracion del entorno
/start-0-7    -> Esta leccion (Configuracion de Claude Code)
/start-1-1    -> Introduccion a generacion de banners
```

### Comandos de utilidad

```text
/check-setup  -> Verificacion integral del entorno
/overview     -> Vista general del proyecto
```

> **Consejo**: En Cursor, se ejecutan comandos desde Cmd+Shift+P -> Paleta de Comandos, pero en Claude Code simplemente escriba `/nombre-del-comando` directamente en el chat.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 4: Verificacion de comandos",
  "questions": [{
    "id": "command_check",
    "prompt": "Probemos un comando slash",
    "options": [
      {"id": "try_check", "label": "Probar /check-setup"},
      {"id": "understood", "label": "Entendido, continuar"},
      {"id": "more_info", "label": "Quiero saber mas"}
    ]
  }]
}
```

(try_check -> Ejecutar el contenido de `/check-setup`)
(understood -> Ir al Step 5)
(more_info -> Mostrar la lista de archivos bajo `.claude/commands/lesson/` y describir cada comando)

---

## Step 5: Comprender el sistema de skills

Los **skills** de Claude Code son modulos especializados para ejecutar tareas específicas. Se almacenan bajo `skills/`.

### Diferencias entre skills y comandos slash

| Función | Mecanismo | Ejemplos |
|---------|-----------|---------|
| **Comandos slash** (`/command`) | Ejecutan archivos en `.claude/commands/` | `/start-0-1`, `/check-setup` |
| **Skills** | Se seleccionan automáticamente por frases de activación en lenguaje natural | "Crea un banner" -> banner-creator |

> **Importante**: Los skills no se pueden invocar con comandos slash como `/nombre-del-skill`. Los comandos slash son exclusivamente para archivos en `.claude/commands/`.

### Cómo invocar skills

Los skills se **seleccionan automáticamente cuando solicita una tarea en lenguaje natural**, basándose en frases de activación definidas en el `SKILL.md` de cada skill:

```text
"Crea un banner"              -> banner-creator se selecciona automaticamente
"Analiza datos"               -> data-analyst se selecciona automaticamente
"Anota una captura de pantalla" -> screenshot-annotator se selecciona automaticamente
```

> **Consejo**: Para asegurar que se use un skill específico, incluya su frase de activación (por ejemplo, "creación de banner", "análisis de datos") en su solicitud.

### Verificar skills disponibles

```text
Escriba "Dime que skills estan disponibles"
```

---

## Step 6: El rol de CLAUDE.md

`CLAUDE.md` es un archivo de configuración ubicado en la raíz del proyecto. Claude Code lo lee primero y comprende:

- Reglas y convenciones del proyecto
- Lista de skills disponibles
- Cómo ejecutar comandos
- Politicas de seguridad

> **Importante**: Puede personalizar el comportamiento de Claude Code editando CLAUDE.md. Esto se cubre en detalle en el Módulo 6 (Desarrollo de Agentes).

---

## Flujo de trabajo recomendado

Pasos recomendados para avanzar en este currículo con Claude Code:

1. **Revisar CLAUDE.md**: Comprender las reglas del proyecto y la lista de skills
2. **Verificación del entorno**: Ejecutar `/check-setup` para verificar su entorno
3. **Iniciar lecciones**: Comenzar lecciones con `/start-{modulo}-{leccion}`
4. **Aprovechar skills**: Los skills necesarios se invocan automáticamente durante las lecciones

---

## Configuración del modo de permisos (Recomendado: Auto Mode)

Claude Code tiene modos de confirmación de permisos para la ejecución de herramientas. Este currículo recomienda usar **Auto Mode**.

### Lista de modos

| Modo | Método de inicio | Comportamiento |
|------|-----------------|---------------|
| **Default** | `claude` | Solicita confirmación en cada edición de archivo y ejecución de comando |
| **Auto-accept edits** | Escribir `/permissions` en el chat -> acceptEdits | Las ediciones de archivos se aprueban automáticamente; la ejecución de comandos requiere confirmación |
| **Auto Mode (Recomendado)** | Escribir `/permissions` en el chat -> auto | Aprueba automáticamente según las reglas de permisos |
| **Full auto** | `claude --dangerously-skip-permissions` | Ejecuta todas las operaciones sin confirmación |

### Cómo configurar Auto Mode

Después de iniciar Claude Code, escriba lo siguiente en el chat:

```text
/permissions
```

Seleccione **auto** del menu que se muestra.

> **Sobre los riesgos**: En Auto Mode, las operaciones que coinciden con las reglas de permisos (ediciones de archivos, ejecución de comandos de shell, etc.) se ejecutan sin confirmación. Pueden ocurrir cambios de archivos o ejecuciones de comandos no deseados. Este currículo recomienda Auto Mode ya que esta pensado para usarse con un repositorio de aprendizaje local, pero **use el modo Default para entornos de producción o repositorios que contengan datos confidenciales**.
>
> `--dangerously-skip-permissions` (Full auto) omite todas las confirmaciones de seguridad y generalmente no es necesario incluso para fines de aprendizaje.

---

## Comandos a ejecutar

```text
npm install -g @anthropic-ai/claude-code
claude
/check-setup
```

## Ejemplo de salida esperada

```text
$ claude --version
2.x.x (Claude Code)

$ claude auth status
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty",
  "email": "your-email@example.com",
  ...
}

$ claude
╭─────────────────────────────────────╮
│ ✻ Welcome to Claude Code!          │
│                                     │
│   /help for available commands      │
╰─────────────────────────────────────╯
```

## Solución de problemas comunes
- `npm install` falla -> Verifique que Node.js sea 18+ con `node --version`
- No puede autenticarse -> Verifique que tenga un plan Pro / Max / Team / Enterprise
- Los comandos no se reconocen -> Verifique que inicio `claude` desde la raíz del repositorio. Si agregó o cambio archivos en `.claude/commands/`, salga de Claude Code (`/exit` o Ctrl+C) y reinicie
- No se encuentran skills -> Verifique que el directorio `skills/` existe

---

## Punto de verificación
- [ ] Claude Code está instalado (`claude --version` funciona)
- [ ] La autenticación OAuth está completa (`claude auth status` muestra sesión iniciada)
- [ ] Puede iniciar `claude` en el repositorio ai-agent-camp
- [ ] `/check-setup` se ejecuta correctamente
- [ ] Comprende cómo usar los comandos slash
- [ ] Comprende la visión general del sistema de skills
- [ ] El modo de permisos (Auto Mode) está configurado

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "La configuracion de Claude Code esta completa. Que desea hacer a continuacion?",
    "options": [
      {"id": "check", "label": "Verificar el entorno (/check-setup)"},
      {"id": "start_lesson", "label": "Comenzar la primera leccion (/start-1-1: Generacion de banners)"},
      {"id": "overview", "label": "Revisar la vista general del proyecto (/overview)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(check -> Ejecutar el contenido de /check-setup)
(start_lesson -> Guiar a /start-1-1)
(overview -> Guiar a /overview)
(finish -> Mostrar "Excelente trabajo! Puede comenzar la primera lección en cualquier momento con /start-1-1")

---

## Complemento: Uso de Claude for Chrome

Usar Claude Code requiere un plan Claude Pro / Team / Enterprise. Esto significa que usted ya puede usar Claude!

Recomendamos instalar la extensión "Claude for Chrome" para mejorar su productividad en el navegador.

### Cómo instalar
1. Busque "Claude" en la Chrome Web Store
2. Instale "Claude" (oficial de Anthropic)
3. Acceda a Claude desde el icono de extensiones en la esquina superior derecha de su navegador

### Usos principales
- **Resumen de páginas web**: Resumir artículos y documentos extensos
- **Comprensión de código**: Explicar código en GitHub
- **Traducción**: Traducir documentos en inglés
- **Investigación**: Investigación técnica y revisión de especificaciones de API

### Cuando usar Claude Code vs. Chrome
| Escenario | Herramienta recomendada |
|-----------|------------------------|
| Editar y ejecutar código en terminal | Claude Code |
| Leer documentos en el navegador | Claude for Chrome |
| Revisar y comprender especificaciones de API | Claude for Chrome |
| Operaciones de archivos y Git | Claude Code |
| Extraer información de páginas web | Claude for Chrome |
