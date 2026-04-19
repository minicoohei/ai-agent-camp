---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-4"]
duration: "~15 min"
level: "intermediate"
tags: ["lp", "vercel", "deploy", "hosting"]
---

# 🎓 Lección 13-5: Despliegue en Vercel

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 13-5: Despliegue en Vercel**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Desplegar la Landing Page/sitio web creado en Vercel y obtener una URL pública |
| Duración | ~15 min |
| Habilidades utilizadas | lp-designer, Vercel CLI |
| Requisitos previos | Lección 13-4 completada (`output/lp-project/` existe). Si no está completada, se generará un proyecto de ejemplo cómo alternativa |
| Página del curso | Consulte [Módulo 13: Diseño de Landing Page/Sitio web](https://ai-agent.camp/es/course/module-13) en paralelo |

> **⚠️ Nota para entornos no interactivos (Codex, CI, etc.)**: `vercel login` requiere autenticación con navegador y no se puede ejecutar en entornos no interactivos. En ese caso, use autenticación por token mediante la variable de entorno `VERCEL_TOKEN`, u omita el paso de despliegue.

**Flujo de la sesión:**
1. Verificar existencia del proyecto (generar muestra si falta)
2. Instalar y autenticar Vercel CLI
3. Despliegue de vista previa
4. Verificar en el navegador
5. Despliegue de producción

Al finalizar la sesión, la Landing Page estará publicada en una URL accesible desde todo el mundo.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar. Las respuestas pueden pausarse dependiendo de la herramienta, pero no es un error.

---

## 🎯 Verificación de preparación

Primero, confirmemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la página del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Paso 0)
(check_prereq → Verificar existencia de Node.js, npm + finalización de Lección 13-4)
(view_html → Mostrar la ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🔍 Paso 0: Verificar existencia del proyecto

Verificar que el entregable de 13-4 (`output/lp-project/`) existe.

**Pasos de verificación:**
```bash
# Verificar si existe el directorio output/lp-project
ls output/lp-project/index.html 2>/dev/null && echo "OK: El proyecto existe" || echo "NO ENCONTRADO: El proyecto no se encontró"
```

**Alternativa si el proyecto no existe:**

Si `output/lp-project/` no existe, complete primero 13-4 o use el siguiente proyecto de ejemplo mínimo cómo alternativa.

```bash
# Generar proyecto de ejemplo
mkdir -p output/lp-project
cat > output/lp-project/index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LP de ejemplo - Práctica de despliegue en Vercel</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <header class="bg-blue-600 text-white py-16 text-center">
    <h1 class="text-4xl font-bold mb-4">LP de ejemplo</h1>
    <p class="text-xl">Esta es una página de práctica para despliegue en Vercel</p>
  </header>
  <main class="max-w-3xl mx-auto py-12 px-4">
    <section class="bg-white rounded-lg shadow p-8 mb-8">
      <h2 class="text-2xl font-bold mb-4">Acerca de esta página</h2>
      <p class="text-gray-700">Esta es una página de ejemplo generada automáticamente para la práctica de despliegue en Vercel de 13-5. Complete 13-4 para desplegar su Landing Page real.</p>
    </section>
  </main>
  <footer class="bg-gray-800 text-gray-400 py-6 text-center">
    <p>&copy; 2026 Capacitación de agentes de IA</p>
  </footer>
</body>
</html>
HTMLEOF
echo "Proyecto de ejemplo generado en output/lp-project/"
```

> **Recomendado**: Idealmente, use la Landing Page creada en 13-4 (`/start-13-4`). El ejemplo es para practicar el procedimiento de despliegue.

**Resultado esperado**: `output/lp-project/index.html` existe.

---

## 🚀 Paso 1: Instalar y autenticar Vercel CLI

Instalar e iniciar sesión en Vercel CLI.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Configuración de Vercel CLI",
  "questions": [{
    "id": "vercel_status",
    "prompt": "¿Cuál es el estado de Vercel CLI?",
    "options": [
      {"id": "not_installed", "label": "Aún no está instalado"},
      {"id": "installed", "label": "Instalado (ya con sesión iniciada)"},
      {"id": "installed_no_login", "label": "Instalado (sin sesión iniciada)"},
      {"id": "no_account", "label": "No tengo cuenta de Vercel"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (not_installed)**:
Entrada:
```text
Instale e inicie sesión en Vercel CLI.

Pasos:
1. Instalar
   npm i -g vercel

2. Verificar versión
   vercel --version

3. Iniciar sesión (Método A: Autenticación con navegador - solo entornos interactivos)
   vercel login

   Se abrirá un navegador, inicie sesión con su cuenta de Vercel.
   Si no tiene una cuenta, cree una gratis en https://vercel.com/signup.

4. Verificar inicio de sesión
   vercel whoami
```

**Instrucciones posteriores a la selección (installed_no_login)**:

> **⚠️ Para entornos no interactivos (Codex, CI, SSH, etc.)**: `vercel login` necesita un navegador y no se puede ejecutar. Use el "Método B: Autenticación por token" a continuación.

Entrada:
```text
■ Método A: Autenticación con navegador (entorno local)
  vercel login
  → Se abrirá un navegador para autenticarse

■ Método B: Autenticación por token (entornos no interactivos / CI)
  1. Vaya a https://vercel.com/account/tokens
  2. Haga clic en "Create Token" para generar un token (nombre arbitrario, ej.: "aiagent-deploy")
  3. Configure como variable de entorno:
     export VERCEL_TOKEN="su-token-generado"

  4. Persistir en .env (opcional):
     Abra el archivo .env directamente en un editor de texto y agregue VERCEL_TOKEN=su-token-generado.

     > **Nota de seguridad**: Agregar con comando como `echo 'VERCEL_TOKEN=...' >> .env` tiene el riesgo de dejar el token en el historial del shell. Se recomienda la edición directa con un editor de texto.

  5. Desplegar con autenticación por token:
     vercel --token "$VERCEL_TOKEN"
     vercel --prod --token "$VERCEL_TOKEN"

■ Verificar inicio de sesión:
  vercel whoami
  # Para auth por token: vercel whoami --token "$VERCEL_TOKEN"
```

**Instrucciones posteriores a la selección (no_account)**:
```text
Cree una cuenta de Vercel:

1. Vaya a https://vercel.com/signup
2. Regístrese con su cuenta de GitHub o correo electrónico (plan gratuito)
3. Después del registro, ejecute vercel login en la terminal
   (Para entornos no interactivos, genere un token en https://vercel.com/account/tokens)
```

**Resultado esperado**: Vercel CLI está instalado y autenticado.

---

## 🚀 Paso 2: Despliegue de vista previa

Primero, desplegar en un entorno de vista previa para verificación.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Despliegue de vista previa",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Despliegue el proyecto de Landing Page en Vercel como vista previa.

■ Método A: Interactivo (entorno local)
1. Navegar al directorio del proyecto
   cd output/lp-project

2. Ejecutar despliegue de Vercel
   vercel

   Configurar lo siguiente interactivamente:
   - Set up and deploy? → Y
   - Which scope? → Seleccionar su cuenta
   - Link to existing project? → N
   - Project name? → my-lp (cualquier nombre)
   - In which directory is your code located? → ./
   - Override settings? → N

3. Después del despliegue, se mostrará una URL de vista previa
   Ejemplo: https://my-lp-xxxxx.vercel.app

■ Método B: Modo no interactivo (entornos CI/Codex, o autenticación por token)
1. Navegar al directorio del proyecto
   cd output/lp-project

2. Desplegar con el flag --yes para omitir las preguntas
   vercel --yes --token "$VERCEL_TOKEN"

   ※ Si VERCEL_TOKEN no está configurado, consulte las instrucciones de autenticación por token del Paso 1

3. Después del despliegue, se mostrará una URL de vista previa

Registre la URL de vista previa mostrada.
```

> **⚠️ Si obtiene un error de `~/.vercel` no encontrado**: Se creará automáticamente en el primer despliegue. Si el error persiste, ejecute `mkdir -p ~/.vercel`.

**Resultado esperado**: Se obtiene una URL de vista previa.

---

## 🚀 Paso 3: Verificar en el navegador

Verificar la URL de vista previa en un navegador.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Verificación de vista previa",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Abra la URL de vista previa en un navegador y verifique.

Elementos de verificación:
1. ¿La página se muestra correctamente?
2. ¿Las imágenes y fuentes se cargan?
3. ¿El diseño responsive funciona correctamente? (Intente cambiar el tamaño del navegador)
4. ¿Las animaciones funcionan?
5. ¿Los enlaces y botones funcionan?

Verifique con cursor-ide-browser MCP:
Navegue a la URL de vista previa con browser_navigate,
y tome una captura de pantalla con browser_snapshot.

Si hay problemas, corrija el código y vuelva a desplegar con vercel.
```

**Resultado esperado**: La Landing Page se muestra correctamente en el entorno de vista previa.

---

## 🚀 Paso 4: Despliegue de producción

Si todo se ve bien, desplegar a producción.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Despliegue de producción",
  "questions": [{
    "id": "deploy_action",
    "prompt": "¿Desplegar a producción?",
    "options": [
      {"id": "deploy_prod", "label": "Desplegar a producción"},
      {"id": "fix_first", "label": "Corregir primero, luego desplegar a producción"},
      {"id": "skip_prod", "label": "Solo vista previa, terminar aquí"},
      {"id": "custom_domain", "label": "También quiero configurar un dominio personalizado"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (deploy_prod)**:
Entrada:
```text
Despliegue a producción.

Pasos:
1. Ejecutar despliegue de producción
   cd output/lp-project
   vercel --prod
   # Para auth por token: vercel --prod --token "$VERCEL_TOKEN"

2. Se mostrará una URL de producción
   Ejemplo: https://my-lp.vercel.app

3. Verificación final en URL de producción
   - Velocidad de carga de la página
   - Imagen OGP (vista previa al compartir en redes sociales)
   - Vista móvil

Registre la URL de producción.
```

**Instrucciones posteriores a la selección (custom_domain)**:

> **Nota**: La configuración de dominio personalizado es opcional. Solo proceda si posee un dominio personalizado. También es posible publicar con el subdominio gratuito de Vercel (*.vercel.app).

Entrada:
```text
Configure un dominio personalizado (solo si posee un dominio personalizado).

Pasos:
1. Agregar dominio
   vercel domains add your-domain.com

2. Configuración DNS (configurar en el lado de su proveedor de dominio)
   - Tipo: CNAME
   - Nombre: @ o www
   - Valor: cname.vercel-dns.com

3. Certificado SSL (emisión automática)
   Vercel emitirá automáticamente un certificado Let's Encrypt.

4. Verificar configuración
   vercel domains inspect your-domain.com
```

**Resultado esperado**: La Landing Page se pública en una URL de producción.

---

## ⚠️ Problemas comunes y soluciones

En Codex, normalmente se presentan opciones en el chat para que el usuario seleccione su problema y reciba orientación al instante.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "Comando vercel no encontrado"},
      {"id": "trouble_2", "label": "No puedo iniciar sesión"},
      {"id": "trouble_3", "label": "Error en el despliegue"},
      {"id": "trouble_4", "label": "La página está completamente en blanco"}
    ]
  }]
}
```

### Problema 1: Comando vercel no encontrado
**Solución**: Instale globalmente con `npm i -g vercel`. Si no funciona, intente ejecutar con `npx vercel`.

### Problema 2: No puedo iniciar sesión
**Solución**: Intente el inicio de sesión basado en token con `vercel login --token <token>`. Puede generar un token en https://vercel.com/account/tokens.

### Problema 3: Error en el despliegue
**Solución**: Verifique el mensaje de error. Causas comunes:
- Límite de tamaño de archivo excedido → Comprima imágenes
- Error de sintaxis en package.json → Verifique el formato JSON
- Error de compilación → Verifique que funcione localmente

### Problema 4: La página está completamente en blanco
**Solución**: Verifique la configuración del directorio raíz del destino de despliegue. Confirme que especificó `./` en `In which directory is your code located?` al ejecutar el comando `vercel`.

---

## ✅ Punto de control
- [ ] El proyecto desplegable existe en `output/lp-project/`
- [ ] Vercel CLI está instalado
- [ ] Sesión iniciada en Vercel (auth con navegador o auth por token)
- [ ] El despliegue de vista previa fue exitoso
- [ ] La Landing Page se muestra correctamente en la URL de vista previa
- [ ] El despliegue de producción está completó (opcional)


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/lp/
├── index.html  (Landing Page)
├── style.css
└── assets/
```

### Comandos de verificación
```bash
# Lista de archivos
ls -lh output/lp/

# Abrir en el navegador (macOS: open / Linux: xdg-open)
open output/lp/index.html
```

> 💡 Verificar estructura HTML: `head -30 output/lp/index.html`

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```bash
Muestre la lista de despliegues actual con vercel ls,
y verifique la URL, estado y fecha de creación del despliegue más reciente.
# Para auth por token: vercel ls --token "$VERCEL_TOKEN"
```

**Resultado esperado**: Se muestra la lista de despliegues y URLs.

---

## 🎉 ¡Felicitaciones!

Ha completado todas las lecciones del Módulo 13.

### Habilidades adquiridas
1. **Diseño de propuesta de valor**: Definición de persona, organización de beneficios, copywriting
2. **Wireframe**: WF ASCII, WF visual, arquitectura de información
3. **Diseño con Pencil**: Creación de diseño de calidad profesional usando MCP
4. **Implementación frontend**: Construcción de Landing Page con HTML/CSS(Tailwind)/JS
5. **Despliegue**: Publicación inmediata con Vercel

### Resumen de la experiencia en 3 etapas
- **Etapa 1**: Texto → HTML creación directa de Landing Page (13-1, 13-2, 13-4)
- **Etapa 2**: Construcción de sitio web más complejo (practicado en ejercicios aplicados)
- **Etapa 3**: Pencil → Conversión a código (13-3 → 13-4)

---

## ➡️ Siguientes pasos

Todas las secciones están completas. Seleccione qué hacer a continuación.

En Codex, normalmente puede seleccionar entre opciones en el chat.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione qué hacer a continuación",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-1)"},
      {"id": "course_top", "label": "Abrir la página del curso (ai-agent.camp)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-1 en una nueva ventana
- course_top → Abrir https://ai-agent.camp/es/course en el navegador
- finish → Finalizar
