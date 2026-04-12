---
description: "When the user says /start-12-5 — Module 12 Lesson 12-5: Integracion de Notion y Slack"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-4"]
duration: "~30 min"
level: "intermediate"
tags: ["notion", "mcp", "files", "attachments"]
---

# 🎓 Lesson 12-5: Integracion de Notion y Slack

## 📍 Lo que hara en esta sesion

**Lesson 12-5** !

| Elemento | Contenido |
|------|------|
| Objetivo | Identificar **bloques de archivos, adjuntos y URLs exportables** en Notion, permitiendo al agente **verificar el contenido y mostrarlo claramente al usuario** |
| Duracion | ~30 min |
| Habilidades utilizadas | Notion MCP (obtencion de paginas/bloques), API oficial segun sea necesario |
| Requisitos previos | `/start-12-4` completada, con acceso a la pagina objetivo |
| Pagina del curso | [Module 12: Notion](https://ai-agent.camp/es/course/module-12)  como referencia paralela |

**Flujo de la sesion:**
1. Identificar bloques que contienen **archivos / PDFs / imágenes** de la lista de bloques de la página objetivo
2. Elegir el **formato obtenible** (extracción de texto, URL temporal, guardado local) disponible a través del MCP o API en uso
3. No pegar binario directamente en el chat; devolver como **nombre de archivo, tipo, resumen y enlace de referencia**

Al final de esta sesion, podra reproducir el flujo: "Donde esta el archivo -> Como obtenerlo -> Como mostrarselo al usuario".

> **Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" para reanudar.

> **Información secreta**: No pegue URLs de descarga ni tokens en bruto en registros o chat.

---

## 🎯 Verificacion de preparacion

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Tiene una página de Notion con archivos adjuntos preparada?",
    "options": [
      {"id": "ready", "label": "Listo"},
      {"id": "need_page", "label": "Quiero crear una página de prueba"},
      {"id": "skip_practice", "label": "Solo verificar el procedimiento"}
    ]
  }]
}
```

---

## 🚀 Step 1: Identify File Blocks

El agente realiza lo siguiente:

1. Confirmar la **URL de la página o el ID de la página** con el usuario
2. Recorrer bloques con MCP / `retrieve block children` etc., y listar bloques correspondientes a `type: file` o incrustaciones
3. Devolver una lista corta de "nombre de archivo, tipo de bloque" al usuario

**Ejemplos de prompts para el usuario:**
```text
Por favor, enumere todos los archivos adjuntos en esta página de Notion,
y añada una breve nota para cada uno sobre cómo obtenerlo (a través de MCP o abrir en el navegador).
Página: <URL>
```

---

## 🚀 Step 2: Retrieve and Verify Locally

1. Seguir las instrucciones de la herramienta MCP para intentar **obtener el contenido del archivo** o **guardarlo en la máquina local del usuario**
2. Si la herramienta solo devuelve binario, informar solo el **tamaño del archivo y el hash**, dejando el procedimiento de apertura al usuario
3. Si se puede convertir a texto/Markdown, extraer solo los **primeros cientos de caracteres** y los encabezados

---

## 🚀 Step 3: "Display" in Chat

**Reglas obligatorias:**
- Imágenes: Cuando sea posible, mostrar `![](URL)` o rutas de archivo **brevemente** (evitar base64 grandes)
- PDF: Solo resumen a nivel de número de páginas/índice (OCR de texto completo solo cuando el usuario lo solicite explícitamente)
- Incluir "qué archivo" y "hasta dónde se leyó" en el **informe de finalización**

---

## ✅ Completion Criteria

- [ ] Puede explicar la ruta de obtención de al menos un archivo adjunto
- [ ] Se convirtió a un formato legible en el chat (resumen/enlaces)
- [ ] No se pegaron URLs con información secreta directamente en el chat público
