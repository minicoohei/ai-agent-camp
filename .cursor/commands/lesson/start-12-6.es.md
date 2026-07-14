---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-5"]
duration: "~35 min"
level: "intermediate"
tags: ["notion", "mcp", "write", "update"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 12-6: Automatizacion de flujos de trabajo con Notion

## 📍 Lo que hara en esta sesion

**Lesson 12-6** !

| Elemento | Contenido |
|------|------|
| Objetivo | Realizar **adicion al cuerpo de la pagina, actualizacion de propiedades y creacion de nuevas subpaginas** mientras aprende **procedimientos de verificacion que no danen produccion** |
| Duracion | ~35 min |
| Habilidades utilizadas | Notion MCP (create / update / append), ncli segun sea necesario |
| Requisitos previos | `/start-12-5` completada |
| Pagina del curso | [Module 12: Notion](https://ai-agent.camp/es/course/module-12)  como referencia paralela |

**Flujo de la sesion:**
1. Duplicar/crear una página o BD de **borrador** y probar solo allí
2. **Presentar los cambios como diferencia al usuario** antes de ejecutar
3. Después de la ejecución, verificar la visualización en Notion y comprender el procedimiento de reversión

> **Seguridad**: En wikis compartidos o BDs de producción, **trabaje siempre en una página duplicada**. No sobrescriba propiedades de producción sin la aprobación explícita del usuario.

---

## 🎯 Verificacion de preparacion

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de escribir",
  "questions": [{
    "id": "target",
    "prompt": "¿Cuál es el objetivo de los cambios?",
    "options": [
      {"id": "sandbox", "label": "Solo páginas de borrador/duplicadas (recomendado)"},
      {"id": "existing", "label": "Página de producción existente (el usuario asume la responsabilidad)"},
      {"id": "read_only", "label": "Solo revisión del procedimiento esta vez"}
    ]
  }]
}
```

---

## 🚀 Step 1: Prepare Sandbox

Ejemplo de instrucciones del agente:
```text
Cree una subpágina con la fecha de hoy debajo de la página "Notion de práctica",
y solo añada texto allí. No toque otros bloques de la página principal.
```

---

## 🚀 Step 2: Append or Update Properties

1. **Añadir**: Agregar encabezados + viñetas con block append (confirmar IDs de bloques existentes con el usuario)
2. **Propiedades**: Escribir los **valores antes y después** de Select / Status / Date, etc. en el chat antes de hacer PATCH
3. **Nueva fila de BD**: Completar solo el título y las propiedades obligatorias, dejando el resto para que el usuario las complete manualmente

---

## 🚀 Step 3: Verification and Rollback

1. Abrir Notion y confirmar con el usuario que se muestra como se esperaba
2. Si hay errores, **revertir usando la misma herramienta** o guiar al historial de página (si está disponible)
3. Incluir la URL de la página modificada, el nombre del elemento y el nuevo valor en el **informe de finalización**

---

## ✅ Completion Criteria

- [ ] Si se editó producción directamente, la aprobación del usuario se registró previamente en el chat
- [ ] El usuario confirmó la diferencia antes/después al menos una vez
- [ ] Se incluyó la URL de la página/BD de ejercicio en el informe final

---

## ➡️ Siguientes pasos

El Módulo 12 (Integración con Notion) está completo.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-13-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-13-1
- finish → Finalizar
