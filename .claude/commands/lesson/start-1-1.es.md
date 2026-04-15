---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
duration: "~30 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["banner", "image", "gemini"]
---

# 🎓 Lesson 1-1: Introducción a la generación de banners

## 📍 Lo que hará en está sesion

Bienvenido a **Lesson 1-1: Introducción a la generación de banners**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear un banner para publicaciones en X usando el Skill banner-creator |
| Duración | ~30 min |
| Skills utilizados | banner-creator (Gemini Image Generation API) |
| Requisitos previos | Clave de Gemini API configurada, entorno Python configurado |
| Página del curso | Consulte [Module 1: Generación de banners e imágenes](https://ai-agent.camp/es/course/module-1) en paralelo |

**Flujo de la sesion:**
1. Comprender los tamaños de banners para publicaciones en X
2. Generar su primer banner
3. Practicar con 3 temas diferentes

Al finalizar está sesion, las imágenes de banners generadas estarán guardadas en la carpeta outputs.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificación de preparación

Verifiquemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar ruta de la página del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Comprender los tamaños de banners para publicaciones en X

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Comprender los tamanos de banners para publicaciones en X",
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

**Después de la selección (ejemplo)**:
Entrada:
```
Indiqueme los tamanos recomendados para banners de publicaciones en X (Twitter) y las diferencias en tamanos de imagen entre las distintas redes sociales.
```

**Resultado esperado**: Se explica el tamaño recomendado para publicaciones en X (1200x675px, 16:9) y las diferencias con otras plataformas.

---

## 🚀 Step 2: Generar su primer banner

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Generar su primer banner",
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

**Después de la selección (ejemplo)**:
Entrada:
```
Use banner-creator para crear un banner para publicaciones en X.
Tema: "Mejora de la eficiencia empresarial con IA"
Estilo: Moderno, orientado a negocios
Salida: docs/generated/banners/banner-1-1.png
```

**Resultado esperado**: Se genera una imagen de banner en la carpeta `docs/generated/banners/`.

---

## 🚀 Step 3: Practicar con diferentes temas

Cree banners con diferentes temas usando los siguientes prompts:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Practicar con diferentes temas",
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

**Después de la selección (ejemplo)**:
Entrada:
```
Cree banners para publicaciones en X con los siguientes 3 temas:
1. "Venta exclusiva de fin de semana"
2. "Campana de lanzamiento de nuevo servicio"
3. "Estamos contratando: Se buscan ingenieros"

Guarde cada uno con un nombre de archivo diferente.
```

**Resultado esperado**: Se generan tres banners diferentes, con diseños que varian según el tema.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "Error \"Modulo no encontrado\""},
      {"id": "trouble_2", "label": "La imagen no se genera"},
      {"id": "trouble_3", "label": "No estoy satisfecho con el diseno"},
      {"id": "trouble_4", "label": "Se produce un error de API"}
    ]
  }]
}
```


### Problema 1: Error "Módulo no encontrado"
**Causa**: Los paquetes de Python necesarios no están instalados
**Prompt de solución**:
```
Instale los paquetes necesarios para ejecutar banner-creator.
Ejecute `uv add pillow requests`.
```

### Problema 2: "La imagen no se genera"
**Causa**: El directorio de salida no existe o hay un problema de permisos
**Prompt de solución**:
```
Verifique si el directorio docs/generated/banners/ existe, y creelo si no existe.
```

### Problema 3: "No estoy satisfecho con el diseño"
**Causa**: La descripción del tema es demasiado abstracta
**Prompt de solución**:
```
Regenere con un tema mas especifico:
"Mejora de la eficiencia empresarial con IA" → "Automatice el 80% de las consultas de clientes con un chatbot de IA"
```

### Problema 4: "Se produce un error de API"
**Causa**: La clave de Gemini API no está configurada o se alcanzo el limite de solicitudes
**Prompt de solución**:
```
Verifique que la clave de Gemini API este correctamente configurada.
Compruebe si la variable de entorno GEMINI_API_KEY está configurada (no vacia).
* Por seguridad, no muestre el valor real de la clave.
```

---

## ✅ Punto de control
- [ ] Comprendio los tamaños recomendados para banners de publicaciones en X
- [ ] Genero exitosamente un banner usando banner-creator
- [ ] Los archivos de imagen se guardaron en la carpeta `docs/generated/banners/`
- [ ] Completo el ejercicio de práctica (3 banners)


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 docs/generated/banners/
├── banner-{nombre-del-tema}.png
└── (variaciones)
```
> Formato: PNG | Tamaño: Configuración automática

### Comandos de verificación
```bash
# Listado de archivos
ls -la docs/generated/banners/

# Abrir imagenes (macOS: open / Linux: xdg-open)
open docs/generated/banners/
```

> 💡 **Claude Code**: Especifique la ruta del archivo con la herramienta Read para previsualizar imágenes en el chat
> 💡 **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat de Cursor para verificar la finalización:

```
# Verificacion de finalizacion: Verifique que se hayan generado imagenes de banners en la carpeta docs/generated/banners/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar una nueva sección.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija su siguiente accion",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-1-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-1-2
- finish → Finalizar
