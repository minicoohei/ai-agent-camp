---
description: "When the user says /start-14-3 — Module 14 Lesson 14-3: Redacción de artículos - Creación de borrador con estilo aplicado"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~35 min"
prerequisites: ["start-14-1", "start-14-2"]
level: "intermediate"
tags: ["article", "writing"]
---

# 🎓 Lección 14-3: Redacción de artículos - Creación de borrador con estilo aplicado

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-3: Redacción de artículos - Creación de borrador con estilo aplicado**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Aplicar el perfil de estilo para generar un borrador del artículo |
| Duración | ~35 min |
| Habilidades utilizadas | article-writer, style-analyzer |
| Requisitos previos | Lección 14-1 (esquema) y Lección 14-2 (perfil de estilo) completadas |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Revisar el esquema de la 14-1 y el perfil de estilo de la 14-2
2. Generar un borrador con estilo aplicado usando article-writer
3. Revisar y ajustar manualmente el borrador

Al finalizar la sesión, un borrador del artículo (formato Markdown) que refleja su estilo de escritura estará completó.

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

(ready → Ir al Paso 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar la ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Paso 1: Revisar el esquema y el perfil de estilo

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Revisar entregables anteriores",
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
Lea los siguientes 2 archivos y verifique el estado de preparación para la redacción del artículo.

1. Esquema: output/article-14-1-outline-final.md
2. Perfil de estilo: output/style_profile.yaml

Puntos de verificación:
- ¿La estructura de títulos del esquema es apropiada?
- Parámetros principales del perfil de estilo (terminaciones de oraciones, longitud, tono)
- La imagen del artículo esperada al combinar ambos

Si hay problemas, proponga correcciones.
```

**Resultado esperado**: Se confirman los contenidos del esquema y el perfil de estilo, y la preparación para la redacción del artículo está completa.

---

## 🚀 Paso 2: Generar borrador con estilo aplicado usando article-writer

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Generar borrador con estilo aplicado",
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
Use la habilidad article-writer para generar un borrador del artículo combinando el esquema y el perfil de estilo.

Comando de ejecución:
python skills/article-writer/scripts/article_writer.py --theme output/article-14-1-outline-final.md --style output/style_profile.yaml --output output/article-14-3-draft.md

Condiciones de generación:
- Esquema: Seguir la estructura en output/article-14-1-outline-final.md
- Estilo: Aplicar los parámetros de estilo de output/style_profile.yaml
- Marcadores de ilustración: Mantener <!-- illustration: ... --> en las posiciones especificadas en el esquema
- Extensión: Ajustar a la extensión estimada definida en el esquema

Guarde los resultados en output/article-14-3-draft.md.
```

**Resultado esperado**: Se genera un borrador del artículo en formato Markdown que refleja su estilo de escritura. Los marcadores de ilustración están colocados en las posiciones apropiadas.

---

## 🚀 Paso 3: Revisar y ajustar manualmente el borrador

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Revisar y ajustar el borrador",
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
Revise el borrador en output/article-14-3-draft.md.

Revise y proporcione comentarios desde estas perspectivas:
1. Consistencia de estilo: ¿Las características del perfil de estilo se reflejan en todo el artículo?
2. Gancho de introducción: ¿Las primeras 3 líneas capturan el interés del lector?
3. Transiciones entre secciones: ¿Las conjunciones y oraciones introductorias son naturales?
4. Especificidad: ¿Hay secciones demasiado abstractas?
5. Resumen y CTA: ¿Incentiva la acción del lector?

Si desea modificar alguna sección, indíquelo.
Guarde el borrador final revisado en output/article-14-3-draft-final.md.
```

**Resultado esperado**: Se muestran los resultados de la revisión del borrador y se guarda el borrador final revisado.

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
      {"id": "trouble_1", "label": "El estilo no coincide con el perfil de estilo"},
      {"id": "trouble_2", "label": "El artículo es demasiado largo o demasiado corto"},
      {"id": "trouble_3", "label": "Los marcadores de ilustración desaparecieron"},
      {"id": "trouble_4", "label": "No se encuentran los archivos anteriores"}
    ]
  }]
}
```


### Problema 1: "El estilo no coincide con el perfil de estilo"
**Causa**: Los parámetros del perfil de estilo no se cargaron correctamente
**Prompt de solución**:
```text
Verifique nuevamente el perfil de estilo (output/style_profile.yaml) y
regenere especificando explícitamente los siguientes parámetros:
- Terminaciones de oraciones: forma cortés (desu/masu)
- Longitud promedio de oraciones: 40-60 caracteres
- Tono: amable pero cortés
Especifique explícitamente el perfil con la opción --style.
```

### Problema 2: "El artículo es demasiado largo o demasiado corto"
**Causa**: La especificación de extensión fue ambigua
**Prompt de solución**:
```text
Regenere el borrador con extensiones objetivo explícitas por sección:
- Introducción: 300-400 caracteres
- Cada sección del cuerpo: 500-700 caracteres
- Resumen: 200-300 caracteres
Ajuste para que se ajuste a la extensión objetivo total.
```

### Problema 3: "Los marcadores de ilustración desaparecieron"
**Causa**: Los marcadores se eliminaron durante la generación del borrador
**Prompt de solución**:
```text
Extraiga los marcadores de ilustración del esquema (output/article-14-1-outline-final.md)
y reinsértelos en las posiciones correspondientes del borrador.
Formato: <!-- illustration: type=image|diagram, description="texto descriptivo" -->
```

### Problema 4: "No se encuentran los archivos anteriores"
**Causa**: La Lección 14-1/14-2 no se completó, o las rutas de archivo son diferentes
**Prompt de solución**:
```bash
Verifique el contenido del directorio output:
ls -la ~/ai-agent-camp/output/
Si no se encuentran el esquema o el perfil de estilo,
complete primero la Lección 14-1 (/start-14-1) y la Lección 14-2 (/start-14-2).
```

---

## ✅ Punto de control
- [ ] Se revisó el contenido del esquema y el perfil de estilo
- [ ] Se generó un borrador con estilo aplicado usando article-writer
- [ ] El estilo de escritura del borrador coincide con el perfil de estilo
- [ ] Se guardó el borrador final revisado y ajustado en output/

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-3-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-3-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-3-*.md
```

> 💡 Ver texto completó: `cat output/article-14-3-*.md` para mostrar el archivo completó

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```bash
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de finalización/incompleto y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar.

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-4)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-4 en una nueva ventana
- finish → Finalizar
