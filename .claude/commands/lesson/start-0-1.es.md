---
description: "When the user says /start-0-1 — Módulo 0 Lección 0-1: Verificación de configuración del entorno"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "~15 min"
prerequisites: ["Codex Desktop o Cursor instalado", "La carpeta ai-agent-camp esta abierta"]
level: "beginner"
tags: ["setup", "environment"]
---

# Lección 0-1: Verificación de configuración del entorno

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Verificar que su entorno — incluyendo Node.js, Python y GitHub CLI — esté listo para comenzar a aprender con Codex |
| Duración | ~15 min |
| Requisitos previos | Codex Desktop o Cursor instalado; la carpeta ai-agent-camp esta abierta |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Si la IA deja de responder, escriba "por favor continua" o "se detuvo" para reanudar.

---

## Cómo configurar

En esta lección, utilizará los siguientes dos comandos para configurar su entorno.
**No se requieren operaciones de terminal. La IA se encarga de todo automáticamente.**

> **Nota para Codex**: En Codex, en lugar de ejecutar `/setup-start` o `/check-setup` directamente como comandos slash de Cursor, siga los pasos de verificación escritos en este archivo en orden. Cuando se necesiten operaciones GUI como autenticación en el navegador, cambie a operación manual del usuario en ese momento.

### Step 1: Iniciar configuración

Ejecute `/setup-start` primero. Este comando realiza **automáticamente** lo siguiente:

- Detectar su sistema operativo (Mac / Windows)
- Verificar Python / Node.js / Git / GitHub CLI y sus versiones
- Proporcionar URLs de instaladores GUI para herramientas faltantes

**Configuración de AskQuestion:**
```json
{
  "title": "Step 1: Iniciar configuracion",
  "questions": [{
    "id": "action",
    "prompt": "Comencemos a configurar su entorno. Que desea hacer?",
    "options": [
      {"id": "run_setup", "label": "Iniciar configuracion (ejecutar /setup-start)"},
      {"id": "run_check", "label": "Solo verificar el entorno (ejecutar /check-setup)"},
      {"id": "already_done", "label": "Ya esta configurado"},
      {"id": "view_html", "label": "Ver la pagina del curso primero"}
    ]
  }]
}
```

(run_setup -> Ejecutar el contenido de `/setup-start`)
(run_check -> Ejecutar el contenido de `/check-setup`)
(already_done -> Ir al Step 2)
(view_html -> Proporcionar la URL de la página del curso `https://ai-agent.camp/es/course/module-0`)

---

### Step 2: Configuración de GitHub y creación de repositorio personal

Ejecute `/setup-github`. Este comando realiza **automáticamente** lo siguiente:

- Verificar la existencia de una cuenta de GitHub
- Abrir automáticamente el navegador para iniciar sesión en GitHub (`gh auth login --web`)
- Crear automáticamente su repositorio privado personal

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Configuracion de GitHub",
  "questions": [{
    "id": "github_action",
    "prompt": "Configuraremos GitHub. Que desea hacer?",
    "options": [
      {"id": "run_github", "label": "Iniciar configuracion de GitHub (ejecutar /setup-github)"},
      {"id": "already_done", "label": "Ya tengo sesion iniciada en GitHub y mi propio repositorio"},
      {"id": "skip", "label": "Omitir e ir a la siguiente leccion"}
    ]
  }]
}
```

(run_github -> Ejecutar el contenido de `/setup-github`)
(already_done -> Ir a la verificación de finalización)
(skip -> Ir al siguiente paso)

---

### Step 3: Verificación integral del entorno

Una vez completada toda la configuración, ejecute `/check-setup` para verificar el estado de su entorno.
La IA verificará automáticamente todo lo siguiente y mostrará un informe:

- Herramientas básicas (Python, Node.js, Git, GitHub CLI)
- Autenticación y APIs (autenticación de GitHub, Gemini API, Slack API)
- Configuración del proyecto (.env, .gitignore, hooks de seguridad)
- Extensiones

Si algún elemento tiene problemas, la IA lo reparará automáticamente o le guiará al comando de configuración correspondiente.

---

## Comandos a ejecutar

```text
/setup-start
/setup-github
/check-setup
```

## Ejemplo de salida esperada

```text
Informe de verificacion del entorno
| Elemento   | Estado | Detalles       |
|-----------|--------|---------------|
| Python    | OK     | 3.12.x        |
| Node.js   | OK     | 24.x          |
| Git       | OK     | 2.x           |
| GitHub CLI | OK    | Sesion iniciada |
```

## Solución de problemas comunes
- La respuesta de la IA se detiene -> Escriba "por favor continua"
- La autenticación de GitHub falla -> Vuelva a ejecutar `/setup-github`
- Herramienta no encontrada -> Instale desde la URL del instalador proporcionada por la IA

---

## Punto de verificación
- [ ] Codex Desktop o Cursor se inicia correctamente
- [ ] Python 3.9 o superior está instalado
- [ ] Node.js 18 o superior está instalado
- [ ] Git está instalado
- [ ] Sesión iniciada en GitHub CLI
- [ ] Push realizado a su propio repositorio privado

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next", "label": "Instalar extensiones (/start-0-2)"},
      {"id": "gemini", "label": "Configurar Gemini API (/start-0-3)"},
      {"id": "check", "label": "Verificar el entorno (/check-setup)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(next -> Guiar a /start-0-2)
(gemini -> Guiar a /start-0-3)
(check -> Ejecutar el contenido de /check-setup)
(finish -> Fin)
