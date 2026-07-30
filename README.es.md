[English](README.md) | [日本語](README.ja.md) | **Español**

# ai-agent-camp

**Capacitacion en Agentes de IA para No Ingenieros - Guia Completa de Claude Code / Cursor / Codex**

[![GitHub](https://img.shields.io/badge/GitHub-minicoohei%2Faiagent--base-181717?style=flat&logo=github)](https://github.com/minicoohei/ai-agent-camp)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](https://github.com/minicoohei/ai-agent-camp/releases)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776ab.svg?style=flat&logo=python)](https://www.python.org/)

> ### ⚠️ Antes de clonar
>
> **Repositorio oficial** (mantenido por los autores):
> - `https://github.com/minicoohei/ai-agent-camp`
>
> Ejecutar agentes de IA desde este repo les otorga permisos de shell, escritura de archivos y APIs externas en tu maquina. **Los forks y mirrors pueden alterar silenciosamente las lecciones o skills.** Antes de ejecutar cualquier leccion, verifica tu clon:
>
> ```bash
> python3 tools/scripts/verify_integrity.py
> ```
>
> Si la verificacion reporta un fork o archivos faltantes, revisa `git diff upstream/main -- .claude/ skills/ tools/ scripts/` antes de continuar. Consulta [`docs/security-guardrails.md`](docs/security-guardrails.md).

<!-- AGENT-META v1
schema: https://github.com/minicoohei/ai-agent-camp/blob/main/docs/release-process.md#agent-meta-v1
repo: minicoohei/ai-agent-camp
primary_branch: main
languages: [ja, en, es]
default_language: ja
latest_tag_api: https://api.github.com/repos/minicoohei/ai-agent-camp/releases/latest
release_asset_pattern: https://github.com/minicoohei/ai-agent-camp/releases/download/{tag}/ai-agent-camp-{lang}-{tag}.zip
manifest_raw_pattern: https://raw.githubusercontent.com/minicoohei/ai-agent-camp/{ref}/courses/lessons.manifest{lang_suffix}.yaml
lang_suffix: {ja: "", en: ".en", es: ".es"}
integrity_cli: python3 tools/scripts/verify_integrity.py
-->

## Versiones y descargas

Las versiones se publican desde `main` como tags que coinciden con `v*` (semver). Un solo tag produce tres archivos zip especificos por idioma, todos adjuntos a la misma GitHub Release.

**Patron de URL de descarga** (fijo, no cambia una vez publicado):

```
https://github.com/minicoohei/ai-agent-camp/releases/download/{tag}/ai-agent-camp-{lang}-{tag}.zip
```

| Idioma | Asset | Checksum |
|--------|-------|----------|
| 日本語 | `ai-agent-camp-ja-{tag}.zip` | `ai-agent-camp-ja-{tag}.zip.sha256` |
| English | `ai-agent-camp-en-{tag}.zip` | `ai-agent-camp-en-{tag}.zip.sha256` |
| Español | `ai-agent-camp-es-{tag}.zip` | `ai-agent-camp-es-{tag}.zip.sha256` |

Cada zip contiene `courses/`, `skills/`, `.claude/`, `.cursor/`, `docs/` ya con los sufijos de idioma eliminados, mas un `CHECKSUMS.txt` que cubre todos los archivos incluidos.

### Para humanos

```bash
# Ultima version, cualquier idioma
gh release download --repo minicoohei/ai-agent-camp --pattern 'ai-agent-camp-es-*.zip'

# Version especifica
gh release download v0.1.0 --repo minicoohei/ai-agent-camp \
  --pattern 'ai-agent-camp-es-v0.1.0.zip'
```

### Para agentes de IA

Parsea el bloque `<!-- AGENT-META v1 -->` de arriba, luego:

1. (opcional) consulta `latest_tag_api` para resolver el tag actual
2. rellena `release_asset_pattern` con `{tag}` y `{lang}`
3. descarga, verifica contra el asset `.sha256` correspondiente y descomprime

Si solo necesitas el manifest de lecciones, usa `manifest_raw_pattern` con el mapa `lang_suffix` para obtener `courses/lessons.manifest[.en|.es].yaml` directamente desde un ref (rama, tag o commit SHA).

Consulta [`docs/release-process.md`](docs/release-process.md) para la especificacion completa, politica de versionado, procedimiento de rollback y un ejemplo de parsing en Python.

> **Antes del primer tag**: aun no hay assets de Release, por lo que el patron de URL anterior devolvera 404 hasta que se publique `v0.1.0`. Hasta entonces, clona el repo directamente (`git clone https://github.com/minicoohei/ai-agent-camp.git`) o obten archivos individuales via `raw.githubusercontent.com/.../main/...`.

## Tabla de Contenidos

- [Descripcion del Proyecto](#descripcion-del-proyecto)
- [Caracteristicas Principales](#caracteristicas-principales)
- [Inicio Rapido](#inicio-rapido)
- [Curso Web (Recomendado)](#curso-web-recomendado)
- [Diferencias por Herramienta](#diferencias-por-herramienta)
- [Ruta de Aprendizaje](#ruta-de-aprendizaje)
- [Estructura del Directorio](#estructura-del-directorio)
- [Matriz de Habilidades](#matriz-de-habilidades)
- [APIs Necesarias](#apis-necesarias)
- [Versiones y descargas](#versiones-y-descargas)
- [Documentacion](#documentacion)
- [Preguntas Frecuentes](#preguntas-frecuentes)
- [Contribuciones](#contribuciones)
- [Soporte](#soporte)

---

## Descripcion del Proyecto

**ai-agent-camp** es un material de capacitacion integral para que profesionales **no ingenieros** en marketing, ventas, planificacion y administracion automaticen y optimicen su trabajo utilizando agentes de IA como Claude Code, Cursor y Codex.

### Publico Objetivo

- Personas sin experiencia en programacion
- Quienes desean utilizar herramientas de IA en su trabajo
- Interesados en automatizacion y analisis de datos
- Quienes buscan mejorar la alfabetizacion en IA de todo el equipo

### Vision del Proyecto

Democratizar los agentes de IA, transformandolos de "herramientas para especialistas" a "herramientas que todos los profesionales pueden utilizar", mejorando la productividad de toda la organizacion.

---

## Caracteristicas Principales

- **Optimizado para no ingenieros**
  - No requiere conocimientos de programacion
  - Tutoriales paso a paso
  - Material basado en escenarios reales de trabajo

- **Conjunto de habilidades practicas**
  - Comandos listos para usar documentados en la [Referencia de Commands](docs/commands-reference.md)
  - Habilidades implementadas documentadas en la [Referencia de Skills](docs/skills-reference.md)
  - Muestras de flujos de trabajo por area de negocio

- **Curriculo integral**
  - Fundamentos de IA (Foundation): 26 capitulos
  - Configuracion del entorno (Setup): 3 capitulos
  - 26 modulos principales disponibles (incluyendo Google Workspace, produccion de video, definicion de requisitos, marketing, etc.)
  - Metadatos YAML compatibles con CursorBootcamp (25 capitulos en total)
  - Tiempo total de aprendizaje: aprox. 24 horas (mas de 30 horas con ejercicios)

- **Seguridad y mejores practicas**
  - Directrices de gestion de claves API
  - Metodos seguros de procesamiento de datos
  - Politicas de implementacion empresarial

- **Flujos de trabajo por area**
  - Soporte al cliente
  - Procesos de ventas
  - Marketing de contenidos
  - Automatizacion de onboarding
  - Optimizacion de flujos de aprobacion

---

## Inicio Rapido

### Prerrequisitos

- Git instalado
- Python 3.9 o superior
- Conexion a internet
- Cursor, Claude Code o Codex disponible
- **Usuarios de Windows: se requiere WSL2 + Ubuntu.** Windows nativo (PowerShell / cmd) no está soportado. Consulte [docs/terminal-guide.md](docs/terminal-guide.md) para la configuración de WSL2.

> **Cual herramienta elegir?** Con `/start-0-8` (Guia de seleccion de herramientas) puedes comparar Cursor / Claude Code / Codex y ver como elegir.

### La forma mas rapida de empezar

1. Clonar este repositorio
2. Leer el punto de entrada de tu herramienta
   - Codex: `AGENTS.md`
   - Claude Code: `CLAUDE.md`
   - Cursor: `.cursor/commands/lesson/start-0-1.md` y demas archivos en `.cursor/commands/*` (para el material de Google Workspace del Modulo 4, usa `/module-18-google-auth`, etc. `module-18-*.md`)
3. Revisar las reglas de seguridad
   - Codex: `docs/codex-safety.md`
   - Claude / Cursor: `docs/security-guardrails.md`
4. Verificar la configuracion
   - Codex: `aiagent-check-setup`
   - Cursor: `/check-setup`
5. Comenzar la primera leccion con `start-0-1`

### Crear tu propio repositorio

Metodos para copiar este repositorio como tu repositorio privado:

#### Metodo 1: Import repository (operacion GUI, sencillo)

Se completa solo con la interfaz de GitHub.

1. Inicia sesion en GitHub, selecciona "+" en la esquina superior derecha -> "Import repository"
2. Ingresa lo siguiente:
   - **Your old repository's clone URL**: `https://github.com/minicoohei/ai-agent-camp.git`
   - **Repository name**: un nombre de tu eleccion (ej: `my-aiagent`)
   - **Privacy**: selecciona **Private**
3. Haz clic en "Begin import"
4. Una vez completada la importacion, clona tu repositorio:
   ```bash
   git clone https://github.com/{tu-nombre-de-usuario}/my-aiagent.git
   cd my-aiagent
   ```

#### Metodo 2: Clone & Push (linea de comandos)

Para quienes estan familiarizados con la terminal.

```bash
# 1. Crear un repositorio privado vacio en GitHub

# 2. Crear un mirror clone
git clone --bare https://github.com/minicoohei/ai-agent-camp.git my-aiagent.git
cd my-aiagent.git

# 3. Configurar el nuevo origin y hacer push
git push --mirror https://github.com/{tu-nombre-de-usuario}/my-aiagent.git

# 4. Obtener un clone de trabajo normal
cd ..
git clone https://github.com/{tu-nombre-de-usuario}/my-aiagent.git
```

### Incorporar actualizaciones del repositorio original

Cuando el material de la fuente original se actualice, puedes incorporar los cambios asi:

```bash
# Solo la primera vez: agregar el repositorio original como upstream
git remote add upstream https://github.com/minicoohei/ai-agent-camp.git

# Incorporar actualizaciones
git fetch upstream
git merge upstream/main
```

Si usas Cursor, puedes ejecutar **`/update-material`** en el chat para realizar la misma operacion.

> **Nota**: Si has realizado cambios propios, pueden producirse conflictos. En ese caso, resuelvelos manualmente.

### Instrucciones de Instalacion

#### 1. Clonar el repositorio

```bash
git clone https://github.com/minicoohei/ai-agent-camp.git ~/ai-agent-camp
cd ~/ai-agent-camp
```

#### 2. Configurar variables de entorno

```bash
# Primero, preparar las lineas de claves necesarias en .env.local
uv run python tools/credential_manager.py prepare-dotenv GEMINI_API_KEY

# Despues de guardar, migrar a Credential Store si es necesario
# uv run python tools/credential_manager.py import-dotenv GEMINI_API_KEY --delete
```

> No pegues las claves API en el chat; guardalas en `.env.local`.

#### 3. Instalar paquetes de dependencias de Python

```bash
# Instalar dependencias con uv
uv sync
```

#### 4. Iniciar el curso

```bash
# Abrir el material en el navegador
# macOS: open https://ai-agent.camp
# WSL2:  wslview https://ai-agent.camp   (o abra la URL directamente en el navegador de Windows)

# Abrir el workspace en Cursor
cursor .

# Claude Code / Codex tambien pueden abrir el mismo repositorio
claude
codex
```

### Como empezar segun la herramienta

#### Cursor

```bash
/check-setup
/overview
/start-0-1
```

#### Claude Code

- Leer `CLAUDE.md`
- Revisar `docs/security-guardrails.md`
- Despues de verificar la configuracion, avanzar al flujo de lecciones

#### Codex

- Leer `AGENTS.md`
- Abrir `docs/codex-guide.md`
- Verificar el entorno con la skill `aiagent-check-setup`
- Pasar `start-0-1` a la skill `aiagent-lesson-runner` para iniciar la primera leccion

---

## Curso Web (Recomendado)

> **Quieres una experiencia de aprendizaje guiada y estructurada?**
>
> [AI Agent Camp](https://ai-agent.camp) ofrece un curso web completo con 28 modulos, mas de 100 lecciones y mas de 70 habilidades practicas, incluyendo un tutor de IA 24/7 y una aplicacion de escritorio dedicada para la configuracion automatica del entorno.
>
> El curso web cubre el mismo plan de estudios que este repositorio, ademas de contenido adicional y funciones interactivas disenadas para no ingenieros.
>
> **[Comienza a aprender en ai-agent.camp](https://ai-agent.camp)**

<p align="center">
  <a href="https://ai-agent.camp">
    <img src="docs/images/ai-agent-camp-preview.png" alt="Curso Web AI Agent Camp" width="600">
  </a>
</p>

---

## Diferencias por Herramienta

El material en si es comun. Lo que difiere es "por donde entrar" y "como operar".

| Elemento | Codex | Claude Code | Cursor |
| --- | --- | --- | --- |
| Entrada | `AGENTS.md` | `CLAUDE.md` | `.cursor/commands/*` |
| Iniciar leccion | `aiagent-lesson-runner` | Flujo de leccion de Claude | `/start-*` |
| Verificar setup | `aiagent-check-setup` | Verificacion desde Claude | `/check-setup` |
| Modelo de seguridad | sandbox + approval | Claude hooks + permissions | Cursor rules + commands |
| ID de leccion | `start-*` | `start-*` | `start-*` |

Puntos en comun:
- Se usa el mismo repositorio
- Se usan los mismos IDs de leccion
- Los principios de seguridad para informacion confidencial y Git son los mismos

Reglas basicas para participantes:
- Avanzar con pasos pequenos para tareas simples
- Escribir un breve plan antes de abordar tareas grandes
- Leer la guia de seguridad correspondiente antes de tocar Git, MCP o informacion confidencial

---

## Ruta de Aprendizaje

### Fase 1: Foundation (Fundamentos de IA) - 5 horas

Aprende los conceptos basicos de los agentes de IA. La ruta siguiente cubre los primeros 11 capitulos (unas 5 horas); la leccion Foundation tiene 26 capitulos en total.

| Capitulo | Contenido | Tiempo |
|----------|-----------|--------|
| 0-1 | Principios basicos y funcionamiento de LLM | 30 min |
| 0-2 | Concepto de Token y metodos de calculo | 30 min |
| 0-3 | Que es un Agente de IA | 30 min |
| 0-4 | Context Engineering y Prompt | 30 min |
| 0-5 | Como usar Cursor | 25 min |
| 0-6 | MCP (Model Context Protocol) | 25 min |
| 0-7 | IA Multimodal | 25 min |
| 0-8 | RAG (Generacion Aumentada por Recuperacion) | 25 min |
| 0-9 | Skill / SubAgent / Agent Team | 25 min |
| 0-10 | Medidas contra la alucinacion | 25 min |
| 0-11 | Seguridad de IA | 25 min |

**Objetivos de aprendizaje**
- Comprender los fundamentos de LLM
- Saber que son los tokens
- Entender el concepto de agentes de IA
- Escribir mejores prompts
- Comprender el funcionamiento de MCP, RAG y multimodal
- Conocer los riesgos de seguridad al usar IA

---

### Fase 2: Setup (Configuracion del Entorno) - 1.5 horas

Preparacion para usar agentes de IA en la practica.

| Modulo | Contenido | Tiempo |
|--------|-----------|--------|
| 0 | Configuracion de Claude Code / Cursor | 30 min |
| 0.5 | Extensiones y personalizacion | 15 min |
| 0.9 | Configuracion de claves API y autenticacion | 45 min |

**Objetivos de aprendizaje**
- Instalar Claude Code / Cursor
- Gestionar claves API de forma segura
- Completar la configuracion basica

---

### Fase 3: Core Modules (Habilidades Principales) - 17.5 horas

Adquiere habilidades que puedes usar en el trabajo real.

| # | Modulo | Skills principales | Lecciones | Dificultad |
|---|--------|-------------------|-----------|------------|
| **1** | **Generacion de banners e imagenes** | banner-creator, nanobanana | 3 | * |
| **2** | **Creacion de diagramas y flujos** | diagram-generator, PlantUML | 3 | ** |
| **3** | **Tutoriales** | screenshot-analyzer, tutorial-generator | 6 | ** |
| **4** | **Google Workspace** | gogcli, Gmail, Calendar, Drive, Sheets | 7 | *** |
| **5** | **Analisis y edicion de PPTX** | pptx-analyzer, pptx-creator, pptx-converter | 2 | ** |
| **6** | **Desarrollo de agentes** | Creacion de Commands/Skills, personalizacion | 5 | **** |
| **7** | **Skill/Commands** | Diseno de Skills, implementacion de SKILL.md, pruebas, patrones de diseno | 8 | **** |
| **8** | **Analisis de datos y EDA** | data-analyst, BigQuery, Marimo | 4 | *** |
| **9** | **Integracion con Slack** | slack-search, check-inbox, task-manager | 2 | * |
| **10** | **Automatizacion con GAS** | gas-clasp-ops, Calendar, Sheets | 3 | *** |
| **11** | **GitHub Actions** | Workflow, Secrets, CI/CD | 2 | *** |
| **12** | **Integracion con Notion** | Notion MCP, operaciones de BD, ncli | 6 | ** |
| **13** | **Creacion de LP/HP** | Propuestas, wireframes, diseno con Pencil, implementacion HTML, despliegue en Vercel | 5 | *** |
| **14** | **Creacion de articulos** | article-writer, copy-editing, fact-checker | 7 | *** |
| **15** | **Produccion de video** | Kling, HeyGen, Veo, Remotion, MV | 8 | *** |
| **16** | **Automatizacion de email/LINE** | email-sequence, Resend, LINE API | 8 | *** |
| **17** | **Marketing** | Publicaciones en X, investigacion SEO, copywriting, maquetas de diseno | 4 | *** |
| **18** | **Definicion de requisitos/Desarrollo de sistemas** | pm-toolkit, test-planner, integracion con Notion | 20 | ***** |
| **19** | **Microsoft Office (Outlook)** | Integracion con Outlook MCP | 1 | ** |
| **20** | **Freee/MoneyForward** | Operaciones contables con Freee MCP | 1 | ** |

**Tiempo total de aprendizaje: aprox. 24 horas (mas de 30 horas con ejercicios y practicas)**

### Opciones de Aprendizaje

**Orden recomendado (principiantes)**
```text
Module 1 -> Module 2 -> Module 3 -> Module 5 -> Module 6 -> Module 8
```

**Orden recomendado (eficiencia laboral)**
```text
Module 4 -> Module 9 -> Module 10 -> Module 11 -> Module 12 -> Module 8
```

**Orden recomendado (enfoque creativo)**
```text
Module 1 -> Module 2 -> Module 3 -> Module 15 -> Module 13 -> Module 14
```

**Orden recomendado (enfoque en marketing)**
```text
Module 1 -> Module 17 -> Module 13 -> Module 15 -> Module 14 -> Module 16
```

---

### Metadatos YAML de CursorBootcamp

En `courses/aiagent/` se encuentran los metadatos YAML para la plataforma CursorBootcamp. Algunos capitulos incluyen `practice/` (ejercicios) y `final/` (tarea final); los que enlazan a los materiales web no los tienen.

| Leccion | Capitulos | Contenido |
|---------|-----------|-----------|
| **Lesson 01: Foundation** | 26 | Fundamentos de LLM, Token, Agent, Context Engineering, MCP, Multimodal, RAG, SubAgent, Alucinacion, Seguridad, Medicion, Viabilidad |
| **Lesson 02: Setup** | 6 | Configuracion del entorno, extensiones, configuracion de API, verificacion de seguridad, entorno remoto, base de conocimiento |
| **Lesson 03: Core** | 26 | Banner a slide-forge (todos los modulos principales) |
| **Lesson 04: Practice** | 4 | Diagramas, sesiones en paralelo, de la investigacion a la propuesta, operacion de PMO |

Total: **62 capitulos**.

---

## Estructura del Directorio

```
ai-agent-camp/
|
+-- courses/                              # Curriculo (fuente de verdad)
|   +-- lessons.manifest.yaml             # Manifiesto de lecciones
|   +-- aiagent/
|       +-- course.yaml                   # Definicion del curso (JP)
|       +-- course.en.yaml                # Definicion del curso (EN)
|       +-- course.es.yaml                # Definicion del curso (ES)
|       +-- cover.png                     # Imagen de portada del curso
|       +-- lesson01-foundation/          # Fundamentos (26 capitulos)
|       |   +-- ch00 ~ ch24/             # LLM, Token, Agent, MCP, RAG, Seguridad, medicion, viabilidad, etc.
|       +-- lesson02-setup/              # Configuracion del entorno (3 capitulos)
|       |   +-- ch01 ~ ch03/             # Entorno, extensiones, configuracion de API
|       +-- lesson03-core/               # Habilidades principales (26 modulos disponibles)
|       |   +-- module01 ~ module25, module29/ # Banner a slide-forge
|       +-- lesson04-practice/           # Ejercicios practicos (4 capitulos)
|           +-- ex01 ~ ex04/             # Diagrama, sesiones paralelas, propuesta, PMO
|
+-- .cursor/commands/                     # Ver docs/commands-reference.md
|   +-- lesson/                           # Comandos de aprendizaje
|   |   +-- /start-0-1 ~ /start-0-8      # Module 0: Setup
|   |   +-- /start-1-1 ~ /start-1-3      # Module 1: Banners
|   |   +-- /start-2-1 ~ /start-2-3      # Module 2: Diagramas
|   |   +-- /start-3-1 ~ /start-3-6      # Module 3: Tutoriales
|   |   +-- /start-4-1 ~ /start-4-7      # Module 4: Google Workspace
|   |   +-- /start-5-1 ~ /start-5-2      # Module 5: PPTX
|   |   +-- /start-6-1 ~ /start-6-9      # Module 6: Desarrollo de agentes
|   |   +-- /start-7-1 ~ /start-7-8      # Module 7: Skill/Commands
|   |   +-- /start-8-1 ~ /start-8-4      # Module 8: Analisis de datos
|   |   +-- /start-9-1 ~ /start-9-3      # Module 9: Slack
|   |   +-- /start-10-1 ~ /start-10-4    # Module 10: GAS
|   |   +-- /start-11-1 ~ /start-11-5    # Module 11: GitHub Actions
|   |   +-- /start-12-1 ~ /start-12-6    # Module 12: Notion
|   |   +-- /start-13-1 ~ /start-13-5    # Module 13: Creacion de LP
|   |   +-- /start-14-1 ~ /start-14-7    # Module 14: Creacion de articulos
|   |   +-- /start-15-1 ~ /start-15-13   # Module 15: Produccion de video (+ 7a-7d)
|   |   +-- /start-16-1 ~ /start-16-8    # Module 16: Email/LINE
|   |   +-- /start-17-1 ~ /start-17-5    # Module 17: Marketing
|   |   +-- /start-18-1 ~ /start-18-20   # Module 18: Requisitos/Desarrollo
|   |   +-- /setup-m365cli + /start-19-1 ~ /start-19-2 # Module 19: Outlook
|   |   +-- /setup-freee + /start-20-1    # Module 20: Freee/MoneyForward
|   |   +-- /setup-figma + /start-21-1    # Module 21: Figma
|   |   +-- /setup-discord + /start-22-1  # Module 22: Discord
|   |   +-- /setup-line-harness + /start-23-1 # Module 23: LINE
|   |   +-- /setup-salesforce + /start-24-1 # Module 24: Salesforce
|   |   +-- /setup-google-ads + /start-25-1 # Module 25: Google Ads
|   |   +-- /start-29-1 ~ /start-29-4    # Module 29: slide-forge
|   |
|   +-- utility/                          # Comandos de utilidad
|       +-- /check-setup                  # Verificacion de configuracion
|       +-- /overview                     # Descripcion del proyecto
|       +-- /guide                        # Guia de uso
|       +-- /tutor                        # Ayuda interactiva
|       +-- /update-material              # Actualizar material a la ultima version
|       +-- ... otros helpers
|
+-- skills/                               # Ver docs/skills-reference.md
|   |
|   |  -- Generacion de imagenes/banners --
|   +-- banner-creator/                   # Generacion de banners para redes sociales
|   +-- nanobanana/                       # Generacion/edicion de imagenes generica
|   +-- diagram-generator/               # Generacion de infografias
|   |
|   |  -- Capturas de pantalla/Tutoriales --
|   +-- screenshot-analyzer/             # Analisis de capturas de pantalla
|   +-- screenshot-annotator/            # Anotacion de capturas de pantalla
|   +-- tutorial-generator/              # Generacion automatica de tutoriales
|   |
|   |  -- Procesamiento de documentos --
|   +-- pptx-analyzer/                   # Analisis de estructura PPTX
|   +-- pptx-converter/                  # Conversion de plantillas PPTX
|   +-- pptx-creator/                    # Generacion automatica de PPTX
|   +-- document-processor/              # Procesamiento de PDF/Word
|   +-- pdf-compressor/                  # Compresion de PDF
|   |
|   |  -- Video/Medios --
|   +-- storyboard-generator/            # Storyboard + generacion de video con Kling
|   +-- video-frame-reader/              # Extraccion de keyframes de video
|   +-- media-generator/                 # Generacion de archivos multimedia
|   |
|   |  -- Analisis de datos/Autenticacion --
|   +-- data-analyst/                    # Analisis de datos y EDA
|   +-- bigquery-auth/                   # Autenticacion de BigQuery
|   +-- gcp-auth/                        # Autenticacion y configuracion de GCP
|   |
|   |  -- Slack/Comunicacion --
|   +-- check-inbox/                     # Extraccion de TODOs de email/Slack
|   +-- slack-search/                    # Busqueda semantica en Slack
|   +-- slack-task-manager/              # Gestion de tareas en Slack
|   +-- slack-unanswered/                # Deteccion de mensajes sin respuesta
|   |
|   |  -- GAS y otros --
|   +-- gas-clasp-ops/                   # Operaciones de Google Apps Script
|   +-- lp-designer/                     # Flujo de trabajo de creacion de LP/HP
|   |
|   |  -- Marketing (20 skills) --
|   +-- ab-test-setup/                   # Diseno e implementacion de pruebas A/B
|   +-- analytics-tracking/             # Tracking con GA4/GTM
|   +-- competitor-alternatives/         # Paginas de comparacion con competencia
|   +-- content-strategy/               # Estrategia de contenidos
|   +-- copy-editing/                    # Edicion y revision de textos
|   +-- copywriting/                     # Copywriting de marketing
|   +-- email-sequence/                  # Secuencias de email
|   +-- free-tool-strategy/             # Estrategia de herramientas gratuitas
|   +-- launch-strategy/                # Estrategia de lanzamiento
|   +-- marketing-ideas/                # Ideas de marketing
|   +-- marketing-psychology/           # Psicologia del marketing
|   +-- paid-ads/                       # Campanas de publicidad paga
|   +-- pricing-strategy/              # Estrategia de precios
|   +-- product-marketing-context/     # Marketing de producto
|   +-- programmatic-seo/              # SEO programatico
|   +-- referral-program/              # Programas de referidos
|   +-- schema-markup/                 # Datos estructurados
|   +-- seo-audit/                     # Auditoria SEO
|   +-- social-content/               # Contenido para redes sociales
|
+-- mv-composer/                        # Herramientas Remotion solo para operaciones/produccion (no necesarias para cursar)
+-- gas-example/                        # Ejemplos GAS solo para operaciones/produccion (no necesarios para cursar)
+-- ops/                                # Scripts solo para operaciones/produccion (no necesarios para cursar)
|
+-- data/                                # Datos minimos para lecciones / ejecucion de Codex
|   +-- codex-command-manifest.json      # Definicion de enrutamiento de Codex
|   +-- google-sync/                     # Scripts y plantillas para sincronizacion con Google
|   +-- slack-sync/                      # Scripts y almacenamiento para sincronizacion con Slack
|   +-- videos/                          # Muestras para lecciones de video
|
+-- tests/                               # Suite de pruebas
|   +-- e2e/                             # Pruebas end-to-end
|   +-- security/                        # Pruebas de seguridad
|   +-- skills/                          # Pruebas de habilidades
|   +-- knowledge_base/                  # Pruebas de base de conocimiento
|   +-- tools/                           # Pruebas de herramientas
|
+-- tools/                               # Scripts y herramientas de Python
|   +-- ugc/                             # Motor de generacion de video
|   |   +-- remotion/                    # Remotion (video con React)
|   |   +-- ... otras herramientas de video
|   +-- ... otras utilidades
|
+-- docs/                                # Documentacion
|   +-- commands-reference.md            # Referencia completa de Commands
|   +-- skills-reference.md              # Informacion detallada de Skills
|   +-- troubleshoot.md                  # Solucion de problemas
|   +-- security-guardrails.md           # Guia de seguridad
|   +-- codex-guide.md                   # Guia de inicio de Codex
|   +-- codex-safety.md                  # Principios de seguridad de Codex
|   +-- i18n-glossary.md                 # Glosario de internacionalizacion
|   +-- setup-guides/                    # Guias de configuracion de API
|   |   +-- docs/                        # Documentos adicionales de configuracion
|   +-- images/                          # Imagenes para documentacion
|   +-- bootcamp/                        # Materiales de bootcamp
|   +-- generated/                       # Documentos generados
|
+-- .cursor/                             # Reglas de Cursor
|   +-- rules/                           # Reglas personalizadas
|   +-- commands/                        # Comandos de Cursor
|
+-- .claude/                             # Configuracion de Claude Code
|   +-- commands/                        # Comandos de Claude
|   +-- hooks/                           # Hooks de Claude
|   +-- settings.json                    # Configuracion de Claude
|
+-- .github/                             # GitHub Actions
|   +-- workflows/                       # Flujos de trabajo CI/CD
|
+-- .env.example                         # Plantilla de variables de entorno
+-- .gitignore                           # Reglas de exclusion de Git
+-- AGENTS.md                            # Guia de Codex
+-- CLAUDE.md                            # Guia de Claude Code
+-- PROGRESS_CHECKLIST.md                # Lista de progreso de aprendizaje
+-- package.json                         # Configuracion de paquetes NPM
+-- requirements.txt                     # Dependencias de Python
+-- requirements-test.txt                # Paquetes para pruebas
+-- README.md                            # README principal (ingles)
```

---

## Matriz de Habilidades

### Mapa de Resultados de Aprendizaje

Lista de habilidades que adquiriras al completar el curso.

#### Clasificacion de Habilidades por Tipo

**Procesamiento y analisis de datos**
- Analisis de datos con BigQuery
- EDA (Analisis Exploratorio de Datos) con Python
- Procesamiento de archivos CSV/Excel
- Visualizacion de datos

**Generacion de contenido**
- Generacion de imagenes con IA
- Creacion de banners y miniaturas para redes sociales
- Generacion de infografias y diagramas
- Anotacion automatica de capturas de pantalla

**Video y medios**
- Generacion de video con IA (Kling, HeyGen)
- Creacion automatica de videos cortos
- Extraccion y analisis de keyframes
- Generacion automatica de storyboards

**Procesamiento de documentos**
- Generacion y edicion automatica de diapositivas PPTX
- Procesamiento y compresion de PDF
- Operaciones con documentos Word
- Analisis de contenido de documentos

**Automatizacion de comunicacion**
- Automatizacion de flujos de trabajo en Slack
- Extraccion automatica de TODOs de correo electronico
- Desarrollo de chatbots
- Enrutamiento de mensajes

**Automatizacion empresarial**
- Operaciones automaticas de Google Sheets/Calendar
- Desarrollo con GAS (Google Apps Script)
- CI/CD con GitHub Actions
- Operaciones con bases de datos de Notion

**Desarrollo de agentes de IA**
- Creacion de Commands personalizados
- Desarrollo de Skills personalizados
- Optimizacion de prompts para LLM
- Diseno de flujos de trabajo

**Marketing y CRO**
- Diseno e implementacion de pruebas A/B
- Auditoria SEO y SEO programatico
- Copywriting y edicion de textos
- Secuencias de email y contenido para redes sociales
- Campanas publicitarias y estrategia de precios
- Implementacion de tracking GA4 / GTM

**Creacion de LP/HP**
- Organizacion de propuestas y copywriting
- Creacion de wireframes
- Diseno con Pencil MCP
- Implementacion HTML/CSS/JS
- Despliegue en Vercel

#### Habilidades Adquiridas por Modulo

| Modulo | Habilidades adquiridas | Ejemplos de aplicacion |
|--------|------------------------|----------------------|
| **1** | Generacion de imagenes, creacion de banners | Marketing en redes sociales, presentaciones |
| **2** | Diagramas de flujo, diagramas | Diseno de procesos, diseno de sistemas |
| **3** | Analisis de capturas, tutoriales | Creacion de manuales, informes de mejora UI/UX |
| **4** | Integracion con Google Workspace | Analisis de Gmail, gestion de Calendar, operaciones de Drive, asistente IA |
| **5** | Automatizacion de PowerPoint | Creacion de presentaciones, informes periodicos |
| **6** | Desarrollo de agentes | Creacion de Commands/Skills, herramientas personalizadas |
| **7** | Diseno de Skill/Commands | Skills especializados, patrones de diseno |
| **8** | Analisis de datos, visualizacion | Analisis de negocio, automatizacion de informes |
| **9** | Integracion con Slack, gestion de tareas | Automatizacion de notificaciones, eficiencia operativa |
| **10** | Automatizacion con GAS | Gestion de calendarios, integracion de datos |
| **11** | GitHub Actions | Pipelines CI/CD, pruebas automaticas |
| **12** | Integracion con Notion | Gestion de conocimiento, gestion de proyectos |
| **13** | Creacion de LP/HP | Propuestas, wireframes, diseno, implementacion, despliegue |
| **14** | Creacion de articulos | Configuracion de temas, aplicacion de estilos, revision, fact-checking |
| **15** | Generacion de video con IA | Presentacion de productos, MV, videos de diapositivas |
| **16** | Automatizacion de email/LINE | Secuencias de email, LINE Bot |
| **17** | Marketing | Publicaciones en X, SEO, copywriting |
| **18** | Definicion de requisitos/Desarrollo | PRD, diseno, pruebas, exportacion a Notion |
| **19** | Integracion con Outlook | Integracion con Microsoft Office |
| **20** | Freee/MoneyForward | Operaciones contables |
| **21** | Integracion con Figma | Sistemas de diseno y colaboracion UI |
| **22** | Integracion con Discord | Operaciones de bots y canales |
| **23** | Cuenta oficial de LINE | Mensajeria y operaciones de cuenta |
| **24** | Integracion con Salesforce CLI | Consultas CRM y operaciones de metadatos |
| **25** | Integracion con Google Ads | Operaciones de datos publicitarios |
| **29** | slide-forge | Flujos de generacion y revision de diapositivas |

---

## APIs Necesarias

### Obligatorias

| API | Descripcion | Donde obtenerla | Uso |
|-----|-------------|-----------------|-----|
| **Gemini API** | API de IA generativa de Google | [Google AI Studio](https://aistudio.google.com/) | Generacion de imagenes, analisis de texto, creacion de contenido |

### Altamente recomendadas (necesarias para los Modulos 4, 8, 9, 12)

| API | Descripcion | Donde obtenerla | Uso | Modulo necesario |
|-----|-------------|-----------------|-----|-----------------|
| **Google OAuth** | Integracion de cuenta de Google | [Google Cloud Console](https://console.cloud.google.com/) | Operaciones de Gmail, Calendar, Drive | 4, 10 |
| **BigQuery** | Data warehouse SQL de Google | [Google Cloud Console](https://console.cloud.google.com/) | Analisis de datos a gran escala | 8 |
| **Slack API** | Integracion con workspace de Slack | [Slack App Directory](https://api.slack.com/apps) | Obtencion de mensajes, respuestas automaticas | 9 |
| **Notion (OAuth)** | Integracion con workspace de Notion | `ncli login` (OAuth en navegador) + Notion Hosted MCP (`https://mcp.notion.com/mcp`) | Operaciones de base de datos | 12 |

### Opcionales (recomendadas para el Modulo 15)

| API | Descripcion | Donde obtenerla | Uso |
|-----|-------------|-----------------|-----|
| **FAL.ai** | Generacion de imagenes/video con IA | [fal.ai](https://fal.ai) | Generacion rapida de imagenes |
| **Kling AI** | Generacion de video a partir de texto | [Kling](https://klingai.com/) | Creacion automatica de videos cortos |
| **HeyGen** | Generacion de video con avatar | [HeyGen](https://www.heygen.com/) | Creacion automatica de videos explicativos |
| **Google Veo** | Modelo de generacion de video con IA | [Google AI Studio](https://aistudio.google.com/) | Generacion de video de alta calidad |
| **GitHub Token** | Integracion con GitHub | [GitHub Settings](https://github.com/settings/tokens) | Operaciones CI/CD |

### Pasos para Obtener Claves API

Consulta los siguientes documentos para mas detalles:

- [Configuracion de Gemini API](docs/setup-guides/GEMINI_API_SETUP.md)
- [Configuracion de Google OAuth](docs/setup-guides/GOOGLE_OAUTH_SETUP.md)
- [Configuracion de BigQuery](docs/setup-guides/BIGQUERY_SETUP.md)
- [Configuracion de Slack API](docs/setup-guides/SLACK_TOKEN_SETUP.md)
- [Configuracion de Notion API](docs/setup-guides/NOTION_API_SETUP.md)

---

## Documentacion

### Material de Aprendizaje

| Documento | Descripcion |
|-----------|-------------|
| [courses/aiagent](courses/aiagent) | Curriculo (fuente de verdad) |
| [docs/codex-guide.md](docs/codex-guide.md) | Guia de inicio de Codex |
| [Lista de progreso](PROGRESS_CHECKLIST.md) | Lista de verificacion de progreso |

### Referencia

| Documento | Descripcion |
|-----------|-------------|
| [Referencia de Commands](docs/commands-reference.md) | Inventario autogenerado de todos los comandos |
| [Referencia de Skills](docs/skills-reference.md) | Inventario autogenerado de todas las habilidades |
| [Guia de Claude Code](CLAUDE.md) | Funciones especificas de Claude Code |

### Guias de Configuracion de API

Todas las guias estan en el directorio `docs/setup-guides/`:

```
docs/setup-guides/
+-- GEMINI_API_SETUP.md      # Gemini API
+-- GOOGLE_OAUTH_SETUP.md    # Google OAuth
+-- BIGQUERY_SETUP.md        # BigQuery
+-- SLACK_TOKEN_SETUP.md     # Slack
+-- NOTION_API_SETUP.md      # Notion
+-- ...
```

### Solucion de Problemas

Consulta la [Guia de solucion de problemas](docs/troubleshoot.md) para soluciones a problemas comunes.

---

## Preguntas Frecuentes (FAQ)

### Sobre la Configuracion

**P: Que hago si no tengo Python instalado?**

R: Descargalo e instalalo desde aqui:
- [Sitio oficial de Python](https://www.python.org/downloads/)
- Al instalar, marca la opcion "Add Python to PATH"

**P: No puedo instalar paquetes en macOS**

R: Usa Homebrew:
```bash
brew install python3
```

**P: Puedo avanzar sin una clave API especifica?**

R: Si. Solo la Gemini API es obligatoria. Las demas se pueden obtener cuando se necesiten para el modulo correspondiente.

### Sobre el Aprendizaje

**P: Puedo participar sin experiencia en programacion?**

R: Si. Todos los comandos y habilidades estan disenados sin requerir conocimientos de programacion.

**P: El orden de los modulos es fijo?**

R: No. Puedes aprender en el orden que te interese. Sin embargo, se recomienda completar los modulos Foundation (0-1 a 0-4) primero.

**P: Cuanto tiempo toma el aprendizaje?**

R: La parte teorica toma aproximadamente 24 horas, y con ejercicios y practicas mas de 30 horas. Con 2-3 horas diarias, se puede completar en unas 2 semanas.

**P: Se obtiene un certificado de finalizacion?**

R: Puedes seguir tu progreso con la lista de verificacion del repositorio ([PROGRESS_CHECKLIST.md](PROGRESS_CHECKLIST.md)).

### Sobre la Aplicacion Practica

**P: Se puede personalizar para nuestro trabajo?**

R: Si. En el Modulo 6 (Desarrollo de agentes) y el Modulo 7 (Skill/Commands), puedes crear Commands y Skills personalizados.

**P: Estamos considerando implementarlo en toda la organizacion**

R: Consulta sobre la guia de licencias y personalizacion empresarial creando un Issue.

**P: Necesitamos una seguridad mas estricta**

R: Consulta la [Guia de seguridad](docs/security-guardrails.md). Tambien es posible configurar para entornos empresariales.

---

## Contribuciones

Damos la bienvenida a comentarios y sugerencias de mejora.

### Reportar Errores / Solicitar Funciones

1. Verifica si ya existe en [Issues](https://github.com/minicoohei/ai-agent-camp/issues)
2. Si es nuevo, crea un Issue
3. Completa la informacion detallada siguiendo la plantilla

### Pull Request

1. Haz Fork de este repositorio
2. Crea una rama de funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz commit (`git commit -m 'Add amazing feature'`)
4. Haz Push a la rama (`git push origin feature/amazing-feature`)
5. Crea un Pull Request

### Mejora de Documentacion

Correcciones de errores tipograficos y mejoras de explicaciones son bienvenidas. Envia tu PR con el siguiente formato:

- Especifica el archivo objetivo
- Describe la razon de la mejora
- Si es posible, presenta la propuesta de correccion

### Preguntas y Consultas

Los Issues se pueden escribir en espanol, ingles o japones.

---

## Soporte

### Documentacion

- [Lista de documentacion](#documentacion)
- [Sitio del curso](https://ai-agent.camp)
- [Solucion de problemas](docs/troubleshoot.md)

### Preguntas y Consultas

| Metodo | Uso |
|--------|-----|
| [GitHub Issues](https://github.com/minicoohei/ai-agent-camp/issues) | Reportar errores, solicitar funciones, preguntas tecnicas |
| [Discussions](https://github.com/minicoohei/ai-agent-camp/discussions) | Preguntas generales, intercambio de informacion, propuesta de ideas |

### Ayuda por Comandos

```bash
# Verificar configuracion
Cursor: /check-setup
Codex: aiagent-check-setup

# Guia de uso
/guide

# Descripcion del proyecto
/overview

# Ayuda interactiva
/tutor

# Sobre un modulo especifico
/help-module-1
```

### Otros Recursos

- **Repositorio oficial**: [github.com/minicoohei/ai-agent-camp](https://github.com/minicoohei/ai-agent-camp)
- **Issue tracker**: [Issues](https://github.com/minicoohei/ai-agent-camp/issues)
- **Notas de version**: [Releases](https://github.com/minicoohei/ai-agent-camp/releases)

---

## Recursos Relacionados

### Documentacion Oficial

- [Claude AI Documentation](https://claude.ai/docs)
- [Cursor Official Docs](https://cursor.com/docs)
- [Google Gemini API Docs](https://ai.google.dev/docs)

### Comunidad

- [Claude Community Discord](https://discord.gg/claude)
- [Cursor Community](https://community.cursor.sh)
