---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Codex Desktop o Cursor instalado"]
level: "beginner"
tags: ["setup", "environment"]
---

# Configuración del entorno de capacitación

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-start` para mostrar el progreso actual
2. Verificar automáticamente lo siguiente; si todo tiene éxito, preguntar "Las herramientas básicas ya están instaladas. ¿Desea omitir?":
   - `python3 --version`
   - `node --version`
   - `git --version`
   - `gh --version`
3. En Mac, verificar si Homebrew está disponible con `which brew`. Si está disponible, ofrecer la opción de instalar automáticamente las herramientas faltantes con `brew install`

## Lo que hará en esta sesión

**¡Bienvenido a la configuración del entorno de capacitación!**

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Verificar que Python / Node.js / Git / GitHub CLI estén instalados, y guiar la instalación si falta algo |
| Duración | ~10 minutos (3 minutos si todo ya está instalado) |
| Habilidades utilizadas | Ninguna (la IA verifica todo automáticamente) |
| Requisitos previos | Codex Desktop o Cursor instalado, carpeta ai-agent-camp abierta |
| Siguiente comando | `/setup-github` (configuración de cuenta de GitHub) |

**Flujo de la sesión:**
1. Detección automática del sistema operativo (Mac / Windows)
2. Verificar Python
3. Verificar Node.js
4. Verificar Git
5. Verificar GitHub CLI

> **Importante**: No necesita escribir ningún comando en el terminal. La IA ejecuta todo automáticamente en segundo plano. Solo revise los resultados que se muestran en pantalla.
>
> **Nota para Codex**: En Codex, en lugar de llamar `/setup-start` como comando slash, siga los elementos de verificación de este documento en orden. La IA le delegará solo los pasos que requieran descargas o autenticación del navegador.
>
> **Consejo**: Si la IA deja de responder a mitad del proceso, escriba "por favor continúa" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no una falla.

---

## Confirmación previa a la sesión

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "what_is_this", "label": "¿Qué hace este comando?"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(what_is_this -> Indicar: "Este comando hace que la IA verifique automáticamente si el software necesario para la capacitación está instalado en su computadora. Si falta algo, solo siga las instrucciones en pantalla para instalarlo. No necesita ingresar ningún comando." -> Ir al Step 1)
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Detección automática del sistema operativo

**Lo que la IA ejecuta automáticamente:**
La IA ejecuta lo siguiente en segundo plano para detectar el sistema operativo:

```bash
uname -s
```

Mac devuelve `Darwin`, Linux/WSL devuelve `Linux`. Si devuelve `Linux`, verificar adicionalmente si es WSL:

```bash
grep -qi microsoft /proc/version 2>/dev/null && echo "WSL" || echo "Native Linux"
```

**Mostrar el resultado de la detección:**
- Mac: "Su computadora es un **Mac**. Procederemos con los pasos específicos para Mac."
- WSL: "Su computadora ejecuta **Windows (WSL)**. Procederemos con los pasos basados en Linux."
- Linux: "Su computadora ejecuta **Linux**. Procederemos con los pasos específicos para Linux."

**La información del sistema operativo detectado se usa en todos los pasos siguientes.**

> Acción requerida del usuario: Ninguna (la IA detecta todo automáticamente)

---

## Step 2: Verificar Python

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar lo siguiente para verificar la versión:

```bash
# Mac / Linux
python3 --version

# Windows
python --version
```

2. Evaluar el resultado:
   - Si se muestra una versión -> Instalado
   - Si no se encuentra el comando -> No instalado

### Si Python está instalado

Ejemplo de visualización:
```text
Python 3.12.x encontrado. Sin problemas.
```
-> Proceder automáticamente al Step 3

### Si Python no está instalado

**Configuración de AskQuestion:**
```json
{
  "title": "Se requiere instalar Python",
  "questions": [{
    "id": "python_install",
    "prompt": "Python 3 no está instalado. Le guiaremos a través de la instalación.",
    "options": [
      {"id": "guide_me", "label": "Muéstreme los pasos de instalación"},
      {"id": "already_done", "label": "Lo instalé de otra manera (volver a verificar)"}
    ]
  }]
}
```

(guide_me -> Mostrar instrucciones específicas del sistema operativo)
(already_done -> Volver a ejecutar `python3 --version` / `python --version` para verificar)

**Instrucciones para Mac:**
```text
Siga estos pasos para instalar:

1. La IA abrirá automáticamente su navegador (espere un momento)
2. Haga clic en el botón amarillo "Download Python 3.12.x" en la página
3. Haga doble clic en el archivo .pkg descargado
4. Siga el instalador: haga clic en "Continuar" -> "Instalar"
5. Cuando termine, escriba "terminé" aquí
```

```bash
La IA ejecuta: open https://www.python.org/downloads/
```

**Instrucciones para Windows:**
```text
Siga estos pasos para instalar:

1. La IA abrirá automáticamente su navegador (espere un momento)
   * Si el navegador no se abre, abra la aplicación Microsoft Store y busque "Python 3.12"
2. Haga clic en el botón "Obtener" para "Python 3.12" en Microsoft Store
3. Cuando se complete la instalación, escriba "terminé" aquí
```

```bash
La IA ejecuta: start https://apps.microsoft.com/search?query=Python+3.12
# Si falla, cambia a start https://www.python.org/downloads/
```

**Después de la instalación:**
La IA vuelve a ejecutar `python3 --version` / `python --version` para verificar.
- Éxito -> Mostrar "¡Instalación de Python completa!" e ir al Step 3
- Fallo -> Guiar a la sección de solución de problemas

---

## Step 3: Verificar Node.js

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar lo siguiente para verificar la versión:

```bash
node --version
```

2. Evaluar el resultado:
   - Se muestra versión 18.x o superior -> Instalado
   - Versión antigua -> Guiar la actualización
   - No se encuentra el comando -> No instalado

### Si Node.js está instalado (18.x o superior)

Ejemplo de visualización:
```text
Node.js v20.x.x encontrado. Sin problemas.
```
-> Proceder automáticamente al Step 4

### Si Node.js no está instalado / versión antigua

**Configuración de AskQuestion:**
```json
{
  "title": "Se requiere instalar Node.js",
  "questions": [{
    "id": "node_install",
    "prompt": "Se requiere Node.js 18 o superior. Le guiaremos a través de la instalación.",
    "options": [
      {"id": "guide_me", "label": "Muéstreme los pasos de instalación"},
      {"id": "already_done", "label": "Lo instalé de otra manera (volver a verificar)"}
    ]
  }]
}
```

(guide_me -> Mostrar instrucciones específicas del sistema operativo)
(already_done -> Volver a ejecutar `node --version` para verificar)

**Instrucciones comunes para Mac / Windows:**
```text
Siga estos pasos para instalar:

1. La IA abrirá automáticamente su navegador (espere un momento)
2. Haga clic en el botón verde "LTS" en la página (esta es la versión recomendada)
3. Abra el archivo descargado para iniciar el instalador
4. Siga el instalador: haga clic en "Next" -> "Install"
5. Cuando termine, escriba "terminé" aquí
```

```bash
# La IA ejecuta:
# Mac:
open https://nodejs.org/
# Windows:
start https://nodejs.org/
```

**Después de la instalación:**
La IA vuelve a ejecutar `node --version` para verificar.
- Éxito -> Mostrar "¡Instalación de Node.js completa!" e ir al Step 4
- Fallo -> Indicar: "Cierre Cursor completamente y vuélvalo a abrir, luego ejecute este comando (/setup-start) nuevamente"

---

## Step 4: Verificar Git

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar lo siguiente para verificar la versión:

```bash
git --version
```

2. Evaluar el resultado:
   - Si se muestra una versión -> Instalado
   - Si no se encuentra el comando -> No instalado

### Si Git está instalado

Ejemplo de visualización:
```text
Git 2.x.x encontrado. Sin problemas.
```
-> Proceder automáticamente al Step 5

### Si Git no está instalado

**Instrucciones para Mac:**
```text
Instalaremos Git.
La IA ejecutará automáticamente el comando de instalación.
Si aparece una ventana emergente, haga clic en "Instalar".
```

```bash
La IA ejecuta: xcode-select --install
# Se inicia el instalador de Xcode Command Line Tools. El usuario solo hace clic en "Instalar" en la ventana emergente
```

Después de la instalación, la IA vuelve a ejecutar `git --version` para verificar.

**Instrucciones para Windows:**
```text
Siga estos pasos para instalar:

1. La IA abrirá automáticamente su navegador (espere un momento)
2. La descarga comenzará automáticamente (si no, haga clic en "Click here to download")
3. Abra el archivo .exe descargado para iniciar el instalador
4. Mantenga todas las configuraciones predeterminadas y haga clic en "Next" -> "Install"
5. Cuando termine, escriba "terminé" aquí
```

```bash
La IA ejecuta: start https://git-scm.com/download/win
```

**Después de la instalación:**
La IA vuelve a ejecutar `git --version` para verificar.
- Éxito -> Mostrar "¡Instalación de Git completa!" e ir al Step 5
- Fallo -> Indicar: "Cierre Cursor completamente y vuélvalo a abrir, luego ejecute este comando (/setup-start) nuevamente"

---

## Step 5: Verificar GitHub CLI

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar lo siguiente para verificar la versión:

```bash
gh --version
```

2. Evaluar el resultado:
   - Si se muestra una versión -> Instalado
   - Si no se encuentra el comando -> No instalado

### Si GitHub CLI está instalado

Ejemplo de visualización:
```text
GitHub CLI 2.x.x encontrado. Sin problemas.
```
-> Ir a la sección de finalización

### Si GitHub CLI no está instalado

**Configuración de AskQuestion:**
```json
{
  "title": "Se requiere instalar GitHub CLI",
  "questions": [{
    "id": "gh_install",
    "prompt": "GitHub CLI no está instalado. Le guiaremos a través de la instalación.",
    "options": [
      {"id": "guide_me", "label": "Muéstreme los pasos de instalación"},
      {"id": "already_done", "label": "Lo instalé de otra manera (volver a verificar)"}
    ]
  }]
}
```

(guide_me -> Mostrar instrucciones específicas del sistema operativo)
(already_done -> Volver a ejecutar `gh --version` para verificar)

**Instrucciones para Mac:**

Primero verificar si Homebrew está instalado:

```bash
brew --version
```

Si Homebrew está disponible:
```text
La IA ejecutará automáticamente la instalación. Espere por favor...
```

```bash
La IA ejecuta: brew install gh
```

Si Homebrew no está disponible:
```text
Siga estos pasos para instalar:

1. La IA abrirá automáticamente su navegador (espere un momento)
2. Haga clic en "Download for macOS" en la página
3. Haga doble clic en el archivo .pkg descargado
4. Siga el instalador: haga clic en "Continuar" -> "Instalar"
5. Cuando termine, escriba "terminé" aquí
```

```bash
La IA ejecuta: open https://cli.github.com/
```

**Instrucciones para Windows:**
```text
Siga estos pasos para instalar:

1. La IA abrirá automáticamente su navegador (espere un momento)
2. Haga clic en "Download for Windows" en la página
3. Abra el archivo .msi descargado para iniciar el instalador
4. Mantenga todas las configuraciones predeterminadas y haga clic en "Next" -> "Install"
5. Cuando termine, escriba "terminé" aquí
```

```bash
La IA ejecuta: start https://cli.github.com/
```

**Después de la instalación:**
La IA vuelve a ejecutar `gh --version` para verificar.
- Éxito -> Mostrar "¡Instalación de GitHub CLI completa!" e ir a la sección de finalización
- Fallo -> Indicar: "Cierre Cursor completamente y vuélvalo a abrir, luego ejecute este comando (/setup-start) nuevamente"

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
      {"id": "trouble_1", "label": "El navegador no se abrió automáticamente"},
      {"id": "trouble_2", "label": "Dice 'no encontrado' aunque lo instalé"},
      {"id": "trouble_3", "label": "El instalador da un error"},
      {"id": "trouble_4", "label": "No aparece ventana emergente en Mac (Git)"},
      {"id": "trouble_5", "label": "Otro problema"}
    ]
  }]
}
```

### Problema 1: "El navegador no se abrió automáticamente"
**Causa**: Configuración del navegador predeterminado o bloqueo del software de seguridad
**Solución**:
```text
Si el navegador no se abre, copie y pegue las siguientes URL directamente en la barra de direcciones de su navegador:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git (Windows): https://git-scm.com/download/win
- GitHub CLI: https://cli.github.com/
```

### Problema 2: "Dice 'no encontrado' aunque lo instalé"
**Causa**: Cursor (terminal) no ha reconocido la información de instalación
**Solución**:
```text
Cierre Cursor completamente (haga clic en el botón X en la esquina superior derecha) y vuélvalo a abrir.
Luego, ejecute /setup-start nuevamente.
Esto resuelve el problema en la mayoría de los casos.
```

### Problema 3: "El instalador da un error"
**Causa**: Permisos insuficientes, espacio en disco insuficiente o problemas de red
**Solución**:
La IA realiza un diagnóstico automático:

```bash
# 1. Verificar espacio libre en disco
df -h /                          # Mac / Linux
wmic logicaldisk get freespace   # Windows

# 2. Verificar conexión de red
ping -c 1 google.com             # Mac / Linux
ping -n 1 google.com             # Windows
```

3. Proporcionar soluciones específicas según los resultados

### Problema 4: "No aparece ventana emergente de Git en Mac"
**Causa**: Las Xcode Command Line Tools ya están instaladas u otro problema
**Solución**:
La IA ejecuta `xcode-select -p` para verificar la ruta.
Si se muestra una ruta, ya está instalado. Volver a verificar `git --version`.

### Problema 5: "Otro problema"
**Solución**:
```text
¿Qué problema está experimentando? Indíqueme el mensaje de error o la situación mostrada en pantalla.
La IA diagnosticará la causa y sugerirá una solución.
```

---

## Punto de verificación

La IA verifica automáticamente todos los elementos y muestra los resultados:

| Elemento | Estado | Versión |
|----------|--------|---------|
| Sistema operativo | (auto-mostrado) | Mac / Windows |
| Python | (auto-mostrado) | 3.x.x |
| Node.js | (auto-mostrado) | 20.x.x |
| Git | (auto-mostrado) | 2.x.x |
| GitHub CLI | (auto-mostrado) | 2.x.x |

Solo proceder al siguiente paso si todos los elementos están OK.

---

## Siguientes pasos

**Si todo está instalado:**

```text
¡Felicitaciones! ¡Todo el software necesario está listo!

A continuación, configuraremos GitHub.
Ingrese lo siguiente en el chat de Cursor:

/setup-github
```

**Si algunos elementos no están instalados:**

```text
Los siguientes elementos aún no están instalados:
- (listar elementos faltantes)

Complete las instalaciones anteriores y luego ejecute /setup-start nuevamente.
```

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Actualizar el progreso con el siguiente comando:
   ```bash
   uv run python tools/setup_progress.py complete setup-start --details "{\"python\":\"$(python3 --version 2>&1 | awk '{print $2}')\",\"node\":\"$(node --version 2>&1)\",\"git\":\"$(git --version 2>&1 | awk '{print $3}')\"}"
   ```
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "A continuación, configuremos GitHub con `/setup-github`"
