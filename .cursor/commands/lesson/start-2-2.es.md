---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
prerequisites: ["start-2-1"]
duration: "~25 min"
level: "beginner"
tags: ["diagram", "infographic", "visualization"]
---

# 🎓 Lesson 2-2: Creación de infografias

## 📍 Lo que hará en está sesion

Bienvenido a **Lesson 2-2: Creación de infografias**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Visualizar datos estadisticos con infografias y crear diagramas persuasivos |
| Duración | ~25 min |
| Skills utilizados | diagram-generator (soporte de infografias) |
| Requisitos previos | Lesson 2-1 completada, clave de Gemini API configurada |
| Página del curso | Consulte [Module 2: Diagramas y flujos](https://ai-agent.camp/es/course/module-2) en paralelo |

**Flujo de la sesion:**
1. Comprender los elementos de una infografia
2. Visualizar datos estadisticos
3. Ajustar el diseño y los colores

Al finalizar está sesion, las infografias que visualizan datos estarán guardadas en outputs.

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

## 🚀 Step 1: Comprender los elementos de una infografia

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Comprender los elementos de una infografia",
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
Explique los elementos basicos para crear infografias efectivas.
Cubra la visualizacion de datos, iconos, uso del color y consejos de diseno.
```

**Resultado esperado**: Se explican cuatro elementos básicos de infografias:
- Visualización de datos (gráficos, diagramas)
- Iconos e ilustraciones
- Uso del color y énfasis
- Jerarquía y diseño

---

## 🚀 Step 2: Visualizar datos estadisticos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Visualizar datos estadisticos",
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
Use diagram-generator para visualizar los siguientes datos como infografia:

Resultados de implementacion de trabajo remoto:
- Reduccion de tiempo de traslado: 75%
- Aumento de productividad: 30%
- Ahorro de costos: 40%
- Satisfaccion de empleados: 85%

Disenelo para que los numeros sean claros de un vistazo.
Salida: ~/ai-agent-camp/output/infographic-remote.png
```

**Resultado esperado**: Se genera una infografia dónde cuatro métricas se representan visualmente de forma clara.

---

## 🚀 Step 3: Crear una comparación Antes/Después

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear una comparacion Antes/Despues",
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
Cree una infografia comparando antes y despues de la adopcion de IA:

[Antes]
- Tiempo de procesamiento: 8 horas
- Tasa de error: 15%
- Casos atendidos: 100/dia

[Despues]
- Tiempo de procesamiento: 30 minutos
- Tasa de error: 2%
- Casos atendidos: 500/dia

[Mejora]
- Tiempo: 94% de reduccion
- Errores: 87% de reduccion
- Eficiencia: mejora de 5x

Use un diseno que muestre claramente la comparacion antes/despues.
Salida: ~/ai-agent-camp/output/infographic-comparison.png
```

**Resultado esperado**: Se genera una infografia comparativa que muestra los cambios antes y después de un vistazo.

---

## 🚀 Step 4: Ejercicio práctico - Estadisticas de uso del servicio

Cree una infografia práctica usando los siguientes prompts:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Ejercicio practico - Estadisticas de uso del servicio",
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
Visualice las estadisticas de uso de un servicio SaaS como infografia:

Metricas clave:
- Usuarios activos mensuales: 500,000 (crecimiento interanual del 150%)
- Tiempo promedio de uso: 25 min/dia
- Usuarios de pago: 50,000 (tasa de conversion del 10%)
- Ingresos anuales: 1,000 millones de yenes

Enfatice la tendencia de crecimiento, mostrando la comparacion interanual y la tasa de conversion.
Salida: ~/ai-agent-camp/output/infographic-saas.png
```

**Resultado esperado**: Se genera una infografia con métricas de negocio organizadas jerárquicamente.

---

## 🚀 Step 5: Crear una infografia narrativa

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Crear una infografia narrativa",
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
Visualice "Patron de comportamiento diario de un usuario" como infografia:

En formato de linea de tiempo, exprese lo siguiente:
- 7:00 Despertar, consultar el clima en la app (tasa de uso 80%)
- 8:00 Traslado, navegar noticias (tasa de uso 65%)
- 12:00 Hora de almuerzo, revisar redes sociales (tasa de uso 90%)
- 18:00 Regreso a casa, ver videos (tasa de uso 75%)
- 21:00 Antes de dormir, navegar sitios de compras (tasa de uso 55%)

Disenelo como una narrativa que siga el flujo del tiempo.
Salida: ~/ai-agent-camp/output/infographic-timeline.png
```

**Resultado esperado**: Se expresa visualmente el comportamiento del usuario a lo largo de una línea de tiempo.

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
      {"id": "trouble_1", "label": "Demasiados numeros, dificil de leer"},
      {"id": "trouble_2", "label": "La comparacion no es clara"},
      {"id": "trouble_3", "label": "El diseno es monotono"},
      {"id": "trouble_4", "label": "La historia no se transmite"}
    ]
  }]
}
```


### Problema 1: "Demasiados numeros, difícil de leer"
**Causa**: Demasiada información acumulada
**Prompt de solución**:
```
Reduzca a las 3 metricas mas importantes.
Mueva la informacion restante a una infografia separada o agreguela como texto complementario.
```

### Problema 2: "La comparación no es clara"
**Causa**: Expresion inconsistente de valores
**Prompt de solución**:
```
Exprese todos los valores como porcentajes o multiplos:
- "8 horas → 30 minutos" → en su lugar "94% de reduccion"
- "100 casos → 500 casos" → en su lugar "aumento de 5x"
```

### Problema 3: "El diseño es monótono"
**Causa**: Faltan elementos visuales
**Prompt de solución**:
```
Agregue los siguientes elementos:
- Iconos para cada metrica
- Fuente grande para numeros importantes
- Codigo de colores para distinguir elementos
- Use graficos y diagramas
```

### Problema 4: "La historia no se transmite"
**Causa**: El flujo y las relaciones entre la información no son claros
**Prompt de solución**:
```
Agregue los siguientes elementos a la infografia:
- Un titulo claro (que muestre la conclusion)
- Flechas que indiquen el flujo de informacion
- Agrupe las metricas relacionadas
- Haga que el mensaje clave sea el mas destacado
```

---

## ✅ Punto de control
- [ ] Comprendio los elementos básicos de infografias
- [ ] Represento visualmente datos estadisticos
- [ ] Presento efectivamente una comparación Antes/Después
- [ ] Completo el ejercicio práctico (estadisticas SaaS)
- [ ] Creo una infografia narrativa


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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-2-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-2-3
- finish → Finalizar
