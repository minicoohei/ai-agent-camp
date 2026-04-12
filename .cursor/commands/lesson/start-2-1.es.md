---
description: "When the user says /start-2-1 — Module 2 Lesson 2-1: Generación de diagramas de flujo"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
duration: "~25 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["diagram", "flowchart", "gemini"]
---

# 🎓 Lesson 2-1: Generación de diagramas de flujo

## 📍 Lo que hará en está sesion

Bienvenido a **Lesson 2-1: Generación de diagramas de flujo**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear diagramas de flujo de procesos empresariales cómo aprobacion de gastos usando el Skill diagram-generator |
| Duración | ~25 min |
| Skills utilizados | diagram-generator (Gemini Image Generation API) |
| Requisitos previos | Clave de Gemini API configurada, entorno Python configurado |
| Página del curso | Consulte [Module 2: Diagramas y flujos](https://ai-agent.camp/es/course/module-2) en paralelo |

**Flujo de la sesion:**
1. Comprender los elementos básicos de un diagrama de flujo
2. Crear un diagrama de flujo simple
3. Intentar un diagrama de flujo avanzado

Al finalizar está sesion, las imágenes que ilustran flujos empresariales estarán guardadas en outputs.

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

## 🚀 Step 1: Comprender los elementos básicos de un diagrama de flujo

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Comprender los elementos basicos de un diagrama de flujo",
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
Explique las formas basicas utilizadas en los diagramas de flujo y sus significados.
Cubra inicio/fin, proceso, decision, datos y flechas.
```

**Resultado esperado**: Se explican los elementos básicos del diagrama de flujo:
- Inicio/Fin: Ovalo
- Proceso: Rectangulo
- Decisión: Rombo
- Datos: Paralelogramo
- Flechas: Flujo del proceso

---

## 🚀 Step 2: Crear un diagrama de flujo simple

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear un diagrama de flujo simple",
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
Use diagram-generator para crear un diagrama de flujo del proceso de aprobacion de gastos:

1. El solicitante envia la solicitud de gastos
2. El supervisor revisa
3. Aprueba o rechaza
4. Si se aprueba, el departamento de contabilidad procesa
5. Si se rechaza, se devuelve al solicitante

Salida: ~/ai-agent-camp/output/flow-expense.png
```

**Resultado esperado**: Se genera un diagrama de flujo de aprobacion de gastos con ramas de decisión.

---

## 🚀 Step 3: Crear un flujo complejo con ramas condicionales

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear un flujo complejo con ramas condicionales",
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
Cree un diagrama de flujo para un proceso de seleccion de personal:

Recepcion de solicitud → Revision de documentos → ¿Aprobado?
  → Si: Primera entrevista → ¿Aprobado?
    → Si: Segunda entrevista → ¿Aprobado?
      → Si: Carta de oferta
      → No: Notificacion de rechazo
    → No: Notificacion de rechazo
  → No: Notificacion de rechazo

Haga que las ramas de decision sean claramente visibles.
Salida: ~/ai-agent-camp/output/flow-recruitment.png
```

**Resultado esperado**: Se visualiza un flujo de reclutamiento con múltiples ramas de decisión.

---

## 🚀 Step 4: Ejercicio práctico - Proceso de pedido de productos

Cree un diagrama de flujo práctico usando los siguientes prompts:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Ejercicio practico - Proceso de pedido de productos",
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
Cree un diagrama de flujo para un proceso de pedido de productos:

Verificacion de inventario → ¿Stock bajo?
  → Si: Crear orden de compra → Solicitar aprobacion → ¿Aprobado?
    → Si: Ejecutar pedido → Esperar entrega → Confirmar entrega → Inspeccion → Procesar pago
    → No: Revisar orden de compra (volver a creacion de orden)
  → No: No se necesita reabastecimiento (fin)

Salida: ~/ai-agent-camp/output/flow-order.png
```

**Resultado esperado**: Se genera un diagrama del proceso de pedido que incluye procesamiento de bucles.

---

## 🚀 Step 5: Ejercicio práctico - Flujo de corrección de errores

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Ejercicio practico - Flujo de correccion de errores",
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
Cree un diagrama de flujo para un flujo de trabajo de correccion de errores de software:

Reporte de error → Triaje → Evaluacion de prioridad
  → Alta prioridad: Asignar al equipo de respuesta inmediata
  → Prioridad media: Agregar al siguiente sprint
  → Baja prioridad: Agregar al backlog

Luego, flujo comun:
Correccion → Revision de codigo → ¿Aprobado?
  → Si: Prueba → ¿Aprobada?
    → Si: Lanzamiento
    → No: Volver a correccion
  → No: Volver a correccion

Salida: ~/ai-agent-camp/output/flow-bugfix.png
```

**Resultado esperado**: Se genera un diagrama de flujo de trabajo con múltiples ramas y bucles de retorno.

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
      {"id": "trouble_1", "label": "El flujo es demasiado complejo para leer"},
      {"id": "trouble_2", "label": "Las ramas condicionales no son claras"},
      {"id": "trouble_3", "label": "Las direcciones de las flechas son confusas"},
      {"id": "trouble_4", "label": "El diagrama no se genera"}
    ]
  }]
}
```


### Problema 1: "El flujo es demasiado complejo para leer"
**Causa**: Demasiada información en un solo diagrama
**Prompt de solución**:
```
Divida este flujo en subprocesos.
Separelo en un flujo principal y flujos detallados, creando cada uno como un diagrama separado.
```

### Problema 2: "Las ramas condicionales no son claras"
**Causa**: Las condiciones de decisión se expresan de forma vaga
**Prompt de solución**:
```
Clarifique las condiciones de las ramas de decision:
- "¿Aprobado?" → "¿El monto es menor a 100,000 yenes?"
- "¿Aprobado?" → "¿La calificacion de la entrevista es A o superior?"
Incluya criterios especificos en el diagrama.
```

### Problema 3: "Las direcciones de las flechas son confusas"
**Causa**: El flujo es complejo y difícil de seguir
**Prompt de solución**:
```
Unifique la direccion del flujo de izquierda a derecha, de arriba a abajo.
Represente los bucles de retorno con lineas punteadas.
```

### Problema 4: "El diagrama no se genera"
**Causa**: Problema con el entorno de ejecución de diagram-generator
**Prompt de solución**:
```
Ejecute una verificacion de diagram-generator.
Verifique que los paquetes necesarios esten instalados
y muestre cualquier mensaje de error.
```

---

## ✅ Punto de control
- [ ] Comprendio los elementos básicos del diagrama de flujo (inicio/fin, proceso, decisión, flechas)
- [ ] Creo un flujo lineal simple
- [ ] Creo un flujo con ramas condicionales
- [ ] Completo el ejercicio práctico (pedido de productos)
- [ ] Completo el ejercicio práctico (flujo de corrección de errores)


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 output/diagrams/
├── flow-{nombre-del-tema}.png
└── (variaciones)
```
> Formato: PNG | Tamaño: Configuración automática

### Comandos de verificación
```bash
# Listado de archivos
ls -la output/diagrams/

# Abrir imagenes (macOS: open / Linux: xdg-open)
open output/diagrams/
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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-2-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-2-2
- finish → Finalizar
