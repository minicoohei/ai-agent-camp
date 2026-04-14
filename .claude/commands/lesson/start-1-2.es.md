---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
prerequisites: ["start-1-1"]
duration: "~30 min"
level: "beginner"
tags: ["banner", "image", "sns", "multi-platform"]
---

# 🎓 Lesson 1-2: Banners avanzados (Instagram, Facebook)

## 📍 Lo que hará en está sesion

Bienvenido a **Lesson 1-2: Banners avanzados (Instagram, Facebook)**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar banners optimizados en lote para X, Instagram y Facebook |
| Duración | ~30 min |
| Skills utilizados | banner-creator (soporte multiplataforma) |
| Requisitos previos | Lesson 1-1 completada, clave de Gemini API configurada |
| Página del curso | Consulte [Module 1: Generación de banners e imágenes](https://ai-agent.camp/es/course/module-1) en paralelo |

**Flujo de la sesion:**
1. Revisar los tamaños para cada plataforma
2. Generar banners en lote para 3 plataformas
3. Verificar la consistencia del diseño
4. Practicar con una campaña diferente

Al finalizar está sesion, los banners para múltiples redes sociales estarán guardados en outputs.

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

## 🚀 Step 1: Revisar los tamaños para cada plataforma

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Revisar los tamanos para cada plataforma",
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
Muestreme los tamanos recomendados de banners para publicaciones en X, Instagram y Facebook en formato de tabla.
Incluya la relacion de aspecto y el caso de uso.
```

**Resultado esperado**: Se muestra una tabla cómo la siguiente:
| Plataforma | Tamaño | Relación de aspecto |
|------------|--------|---------------------|
| X | 1200x675px | 16:9 |
| Instagram | 1080x1080px | 1:1 |
| Facebook | 1200x630px | 1.91:1 |

---

## 🚀 Step 2: Generar banners en lote para 3 plataformas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Generar banners en lote para 3 plataformas",
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
Cree banners para las siguientes 3 plataformas con el tema "Evento de venta de verano":

1. Para X (1200x675px)
2. Para Instagram (1080x1080px)
3. Para Facebook (1200x630px)

Guardelos como banner-1-2-x.png, banner-1-2-ig.png y banner-1-2-fb.png respectivamente.
```

**Resultado esperado**: Se generan tres banners de diferentes tamaños, cada uno optimizado para su plataforma.

---

## 🚀 Step 3: Verificar la consistencia del diseño

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Verificar la consistencia del diseno",
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
Revise los 3 banners recien creados.
Verifique si se mantiene la consistencia del diseno (colores, fuentes, mensajes)
e indique cualquier area de mejora.
```

**Resultado esperado**: Se evalua la consistencia de marca entre los 3 banners, con sugerencias de mejora según sea necesario.

---

## 🚀 Step 4: Practicar con una campaña diferente

Cree un conjunto de banners para una campaña diferente usando los siguientes prompts:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Practicar con una campana diferente",
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
Cree un conjunto de banners para X, Instagram y Facebook con el tema
"Lanzamiento de nuevo producto - Bonus exclusivo para los primeros 100 clientes."
Estilo: Lujoso, sensacion premium
Colores: Base de dorado y negro
```

**Resultado esperado**: Se generan banners para 3 plataformas con un tema de diseño unificado.

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
      {"id": "trouble_1", "label": "Nombre de plataforma no reconocido"},
      {"id": "trouble_2", "label": "Error en la generacion en lote"},
      {"id": "trouble_3", "label": "Los disenos carecen de consistencia"},
      {"id": "trouble_4", "label": "El diseno cuadrado de Instagram esta roto"}
    ]
  }]
}
```


### Problema 1: "Nombre de plataforma no reconocido"
**Causa**: Se específico un nombre de plataforma incorrecto
**Prompt de solución**:
```
Muestreme la lista de nombres de plataformas disponibles para banner-creator.
Verifique con la opcion --help.
```

### Problema 2: "Error en la generación en lote"
**Causa**: Se produjo un error de API o de escritura de archivo a mitad del proceso
**Prompt de solución**:
```
Ejecute la generacion de banners uno a la vez para identificar que plataforma causa el error.
Muestre el mensaje de error.
```

### Problema 3: "Los diseños carecen de consistencia"
**Causa**: El prompt se interpreto por separado para cada plataforma
**Prompt de solución**:
```
Unifique lo siguiente en los 3 banners:
- Color principal: #FF6B00 (naranja)
- Fuente: Sans-serif moderna
- Eslogan: El mismo texto
```

### Problema 4: "El diseño cuadrado de Instagram está roto"
**Causa**: Diseño horizontal forzado en formato cuadrado
**Prompt de solución**:
```
Regenere el banner de Instagram con un diseno optimizado para formato cuadrado (1:1).
Centre el texto y proporcione margenes amplios.
```

---

## ✅ Punto de control
- [ ] Comprendio los tamaños recomendados para cada plataforma
- [ ] Genero banners para X, Instagram y Facebook
- [ ] Verifico la consistencia del diseño
- [ ] Completo el ejercicio de práctica (conjunto de banners para otra campaña)


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
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-1-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-1-3
- finish → Finalizar
