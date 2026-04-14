---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Node.js 18 o superior instalado"]
level: "beginner"
tags: ["setup", "remotion", "video", "react", "npm"]
---

# Configuración de Remotion

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-remotion` para mostrar el progreso
2. Detectar automáticamente el entorno existente:
   - Verificar la versión de Node.js con `node --version` (se requiere 18 o superior)
   - Verificar si existe `mv-composer/node_modules/remotion`
   - Si ya está configurado, solo ejecutar Step 3 (prueba de operación) y marcar como completado

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Configurar Remotion (un framework de generación de video basado en React) en mv-composer/ y tener Remotion Studio listo para iniciar |
| Duración | ~10 minutos |
| Requisitos previos | Node.js 18 o superior instalado |
| Nivel de operación | Todo lo ejecuta la IA automáticamente (solo confirmación) |

**¿Qué es Remotion?**
Remotion es un framework que permite crear videos usando componentes de React. Puede generar videos animados de forma programática y se usa para crear MVs promocionales, TikTok/YouTube Shorts, videos de presentación de productos y más.

**Sobre el precio:**
Remotion es de código abierto y el renderizado local es gratuito. Solo se necesita una licencia separada al usar Remotion Lambda (renderizado en la nube), que no usaremos en esta capacitación.

**Flujo de la sesión:**
1. Verificar la versión de Node.js
2. Instalar paquetes de dependencia con npm install
3. Prueba de inicio de Remotion Studio
4. Renderizado de prueba (opcional)

> **Consejo**: Si la IA deja de responder a mitad del proceso, escriba "por favor continúa" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(check_prereq -> Indicar: "Se requiere Node.js 18 o superior. Puede verificarlo con `node --version`. Si no está instalado, descárguelo de https://nodejs.org")
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Verificar Node.js

**Lo que hace la IA:**
1. Verificar la versión de Node.js:

```bash
node --version
```

2. Verificar la versión de npm:

```bash
npm --version
```

**Criterios:**
- Node.js 18.x o superior -> OK, ir al Step 2
- Node.js no instalado o inferior a 18 -> Guiar la instalación

**Si Node.js no está instalado:**

```text
Se requiere Node.js 18 o superior. Instálelo desde:
  https://nodejs.org (se recomienda la versión LTS)

En Mac, también puede instalar con Homebrew:
  brew install node
```

**Comandos para abrir el navegador:**
```bash
# Mac:
open https://nodejs.org
# Windows:
start https://nodejs.org
# Linux:
xdg-open https://nodejs.org
```

Después de la instalación, pedir al usuario que escriba "listo", luego ejecutar `node --version` nuevamente para verificar.

---

## Step 2: Instalar Remotion

**Lo que hace la IA:**
1. Navegar al directorio mv-composer y ejecutar npm install:

```bash
cd mv-composer && npm install
```

2. Verificar la instalación:

```bash
ls mv-composer/node_modules/remotion/package.json && echo "Remotion installed OK"
```

**Resultado esperado:**
- Se muestra un mensaje `added XX packages`
- Se muestra `Remotion installed OK`

**Solución de problemas:**
- Error `EACCES` -> No usar `sudo`. Evítelo con `npm config set prefix ~/.npm-global`
- Error `ERESOLVE` -> Probar `npm install --legacy-peer-deps`
- Error de red -> Verificar la configuración del proxy

---

## Step 3: Prueba de inicio de Remotion Studio

**Lo que hace la IA:**
1. Iniciar Remotion Studio:

```bash
cd mv-composer && npx remotion studio
```

**Resultado esperado:**
- El navegador se abre automáticamente y muestra Remotion Studio
- Una lista de composiciones (ScreenExplainer, etc.) aparece en el panel izquierdo
- Un video se renderiza en el área de vista previa

**Indicación al usuario:**
```text
¿Apareció Remotion Studio en su navegador?
Si puede ver la lista de composiciones en el panel izquierdo, ¡está funcionando!

Una vez confirmado, presione Ctrl+C para detener el servidor.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Verificación de Remotion Studio",
  "questions": [{
    "id": "studio_check",
    "prompt": "¿Apareció Remotion Studio en su navegador?",
    "options": [
      {"id": "success", "label": "¡Apareció!"},
      {"id": "no_browser", "label": "El navegador no se abrió"},
      {"id": "error", "label": "Obtuve un error"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

(success -> Ir al Step 4)
(no_browser -> Indicar que ingrese `http://localhost:3000` manualmente en el navegador)
(error -> Pedir que pegue el mensaje de error y resolver problemas)
(skip -> Ir al Step 4)

---

## Step 4: Renderizado de prueba (opcional)

**Configuración de AskQuestion:**
```json
{
  "title": "Renderizado de prueba",
  "questions": [{
    "id": "render_test",
    "prompt": "¿Desea probar un renderizado de prueba? (~30 segundos a 1 minuto)",
    "options": [
      {"id": "yes", "label": "Probar"},
      {"id": "no", "label": "Omitir y finalizar"}
    ]
  }]
}
```

(yes -> Ejecutar renderizado de prueba)
(no -> Ir a la verificación de finalización)

**Lo que hace la IA (si elige sí):**
1. Renderizar una composición corta:

```bash
cd mv-composer && npx remotion render src/index.ts ScreenExplainer --frames=0-30 --codec h264 out/test_render.mp4
```

2. Verificar el archivo de salida:

```bash
ls -lh mv-composer/out/test_render.mp4
```

**Resultado esperado:**
- Se genera `out/test_render.mp4`
- El tamaño del archivo es mayor que 0

**Indicación después del renderizado:**
```text
El renderizado de prueba está completo.
Se generó out/test_render.mp4.

Para ver el video:
  open mv-composer/out/test_render.mp4  (Mac)
  start mv-composer\out\test_render.mp4  (Windows)
```

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
      {"id": "trouble_1", "label": "npm install falla"},
      {"id": "trouble_2", "label": "Remotion Studio no se abre"},
      {"id": "trouble_3", "label": "El renderizado falla"},
      {"id": "trouble_4", "label": "Errores de TypeScript"}
    ]
  }]
}
```

### Problema 1: "npm install falla"
**Causa**: Versión de Node.js insuficiente, problemas de red
**Guía de resolución:**
```text
Verifique lo siguiente en orden:
1. ¿Es node --version 18.x o superior?
2. Ejecute npm cache clean --force y reintente
3. Pruebe npm install --legacy-peer-deps
```

### Problema 2: "Remotion Studio no se abre"
**Causa**: Conflicto de puerto, configuración del navegador
**Guía de resolución:**
```text
1. Ingrese http://localhost:3000 directamente en su navegador
2. Cambiar puerto: npx remotion studio --port 3001
3. Verificar la configuración del firewall
```

### Problema 3: "El renderizado falla"
**Causa**: FFmpeg no instalado, memoria insuficiente
**Guía de resolución:**
```text
Remotion usa un FFmpeg integrado, por lo que normalmente no se necesita instalación adicional.
Verifique el mensaje de error.
Si hay falta de memoria: agregue la opción --concurrency=1
```

### Problema 4: "Errores de TypeScript"
**Causa**: Incompatibilidad de definiciones de tipo
**Guía de resolución:**
```text
1. Eliminar node_modules y reinstalar:
   rm -rf mv-composer/node_modules && cd mv-composer && npm install
2. Verificar la versión de TypeScript:
   npx tsc --version
```

---

## Punto de verificación
- [ ] Node.js 18 o superior está instalado
- [ ] Existe mv-composer/node_modules/remotion
- [ ] Remotion Studio se mostró en el navegador
- [ ] (Opcional) El renderizado de prueba fue exitoso

---

## Verificación de finalización

**Lo que hace la IA:**
```bash
# Verificar versión de Node.js
node --version

# Verificar instalación de Remotion
ls mv-composer/node_modules/remotion/package.json && echo "OK: Remotion installed"

# Marcar progreso de configuración como completado
uv run python tools/setup_progress.py complete setup-remotion
```

---

## Vista previa de resultados

El entregable de esta lección es la salida del terminal.

### Ejemplo de salida esperada
```text
┌─────────────────────────────────────┐
│  Configuración de Remotion completa  │
│  Node.js: v18.x.x                  │
│  Remotion: 4.0.434                  │
│  Studio: Inicio verificado         │
└─────────────────────────────────────┘
```

---

## Siguientes pasos

La configuración de Remotion está completa. Ahora puede continuar con las lecciones de producción de video.

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija qué hacer a continuación",
    "options": [
      {"id": "lesson_15_8", "label": "Lección 15-8: Generar automáticamente materiales de marketing con Remotion"},
      {"id": "mv_composer", "label": "Crear un video con MV Composer"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Después de la selección:**
- lesson_15_8 -> /start-15-8
- mv_composer -> Escriba "crear un video MV" para iniciar el skill mv-composer
- finish -> Finalizar
