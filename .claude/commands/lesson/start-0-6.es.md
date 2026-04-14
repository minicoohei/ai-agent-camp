---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "~15 min"
prerequisites: ["Node.js 18 o superior instalado", "Clave de OpenAI API obtenida"]
level: "beginner"
tags: ["setup", "codex", "cli"]
---

# Lección 0-6: Configuración de Codex CLI

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar y autenticar Codex CLI para poder ejecutar lecciones en ai-agent-camp |
| Duración | ~15 min |
| Requisitos previos | Node.js 18 o superior; clave de OpenAI API obtenida |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Esta lección es para usuarios de Codex CLI. Los usuarios de Cursor deben comenzar desde la Lección 0-1.

---

## Step 1: Instalar Codex CLI

Instale Codex CLI via npm. Ejecute lo siguiente en su terminal:

**Recomendado: Ejecutar directamente con npx (sin instalación necesaria)**

```bash
npx @openai/codex --version
```

Usar npx le permite ejecutar la última versión sin una instalación global.

**Alternativa: Instalación global**

Si usa nvm o fnm, no se requiere sudo:

```bash
npm install -g @openai/codex
codex --version
```

> **Nota**: Se requiere Node.js 18 o superior. Verifique con `node --version`.
> Si obtiene un error de permisos, consulte la [guía oficial de npm](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally) para cambiar el prefix. No se recomienda `sudo npm install -g`.

---

## Step 2: Autenticación (Clave de OpenAI API)

Codex CLI se autentica con una clave de OpenAI API. Configurela usando uno de los siguientes métodos:

### Método A: Usar credential_manager (Recomendado)

Use `tools/credential_manager.py` para administrar claves API de forma segura:

```bash
uv run python tools/credential_manager.py store OPENAI_API_KEY
```

Siga el indicador para ingresar su clave. Se guardará en un almacen de claves cifrado.

### Método B: Configurar como variable de entorno

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Agreguelo a `.bashrc` o `.zshrc` para persistir entre sesiones.

### Método C: Configurar en archivo .env (alternativa)

Solo si los métodos anteriores no están disponibles, agregue lo siguiente al `.env` en el repositorio ai-agent-camp:

```dotenv
OPENAI_API_KEY=your-api-key-here
```

> **Advertencia de seguridad**: El archivo `.env` contiene información confidencial. **Nunca lo haga commit a Git.** Siempre verifique que `.env` este incluido en `.gitignore`. Los commits accidentales arriesgan la filtración de claves API.

---

## Step 3: Configuración de ejecución

Configuración recomendada para Codex CLI:

El modo de aprobación de Codex CLI se especifica con `-a` (`--ask-for-approval`):

| Modo de aprobación | Descripción |
|-------------------|-------------|
| `on-request` | El modelo determina automáticamente cuando solicitar aprobación del usuario (recomendado para aprendizaje) |
| `never` | Ejecución automática sin confirmación (solo usuarios avanzados, no recomendado) |

Ejemplo de comando de inicio:

```bash
codex -a on-request
```

> **Importante**: Codex administra el sandbox automáticamente. Siga la configuración recomendada en `AGENTS.md` para la configuración detallada. No use el modo `never` durante el aprendizaje normal. Consulte `docs/codex-safety.md` para más detalles.

---

## Step 4: Cómo ejecutar lecciones en Codex

En Cursor, se inician lecciones con comandos slash como `/start-0-1`, pero en Codex CLI se usan **skills** en su lugar.

### Tabla de correspondencia entre comandos slash y skills

| Comando de Cursor | Método en Codex |
|-------------------|----------------|
| `/overview` | Usar el skill `aiagent-guide` |
| `/check-setup` | Usar el skill `aiagent-check-setup` |
| `/start-0-1` | Usar el skill `aiagent-lesson-runner` con `start-0-1` |
| `/setup-security` | Usar el skill `aiagent-tooling-setup` |

### Cómo usar

Inicie Codex CLI y haga una solicitud como:

```text
Usa el skill aiagent-lesson-runner para iniciar la leccion start-0-1
```

O:

```text
Quiero comenzar la leccion start-0-1
```

Codex reconoce automáticamente `AGENTS.md` y el directorio `skills/` y utiliza el skill apropiado.

---

## Step 5: Verificar funcionamiento

Siga estos pasos para confirmar que Codex CLI funciona correctamente:

1. **Inicie Codex en el directorio ai-agent-camp**:
   ```bash
   cd /path/to/ai-agent-camp
   codex
   ```

2. **Verifique la configuración de hooks del repositorio**:
   ```text
   Por favor ejecute bash scripts/install_hooks.sh
   ```

3. **Ejecute el skill de verificación de configuración**:
   ```text
   Use el skill aiagent-check-setup para verificar el entorno
   ```

---

## Ejemplo de salida esperada

```text
Informe de verificacion del entorno
| Elemento    | Estado | Detalles          |
|------------|--------|------------------|
| Node.js    | OK     | 22.x             |
| Codex CLI  | OK     | 1.x.x            |
| OpenAI API | OK     | Autenticado      |
| Git        | OK     | 2.x              |
| Hooks      | OK     | pre-commit configurado |
```

## Solución de problemas comunes

- `codex: command not found` -> Ejecute directamente con `npx @openai/codex` o vuelva a ejecutar `npm install -g @openai/codex`
- Error de autenticación de API -> Verifique que `OPENAI_API_KEY` esté configurada correctamente
- Error de permisos -> Use nvm/fnm o [cambie el prefix de npm](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally)
- Skill no encontrado -> Verifique que inicio Codex desde el directorio raíz de ai-agent-camp

---

## Punto de verificación
- [ ] Codex CLI está instalado (`codex --version` funciona)
- [ ] La clave de OpenAI API está configurada
- [ ] El modo de aprobación está configurado en `on-request` (ver configuración recomendada en AGENTS.md)
- [ ] Los hooks están configurados con `bash scripts/install_hooks.sh`
- [ ] El skill `aiagent-check-setup` se ejecuta correctamente

---

## Siguientes pasos

Una vez completada la configuración de Codex CLI, puede comenzar las lecciones.

**Flujo recomendado para usuarios de Codex:**

1. Verificación de configuración: Ejecute `start-0-1` (Verificación de configuración del entorno) con el skill `aiagent-lesson-runner`
2. Comenzar lecciones: Inicie `start-1-1` (Módulo 1 Introducción a generación de banners) con el skill `aiagent-lesson-runner`
3. Ejecute los comandos slash de cada lección a través de skills
4. Si tiene dudas, use el skill `aiagent-guide` para ver la visión general

> **Nota**: Los archivos de lecciones en `.cursor/commands/lesson/` también pueden usarse como materiales de referencia en Codex. Sin embargo, no pueden ejecutarse directamente como comandos slash.
