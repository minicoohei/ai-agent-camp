---
description: "When the user says /start-2-3 — Module 2 Lesson 2-3: Diagramas para materiales de presentación"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
prerequisites: ["start-2-1"]
duration: "~30 min"
level: "intermediate"
tags: ["diagram", "presentation", "architecture"]
---

# 🎓 Lesson 2-3: Diagramas para materiales de presentación

## 📍 Lo que hará en está sesion

Bienvenido a **Lesson 2-3: Diagramas para materiales de presentación**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear diagramas de arquitectura de sistemas, diagramas de secuencia y otros diagramas para presentaciones y documentación técnica |
| Duración | ~30 min |
| Skills utilizados | diagram-generator (basado en generación de imágenes de Gemini) |
| Requisitos previos | Lesson 2-1 completada, clave de Gemini API configurada |
| Página del curso | Consulte [Module 2: Diagramas y flujos](https://ai-agent.camp/es/course/module-2) en paralelo |

**Flujo de la sesion:**
1. Comprender los tipos de diagramas necesarios para presentaciones
2. Crear un diagrama de arquitectura de sistemas
3. Intentar diagramas de secuencia y otros tipos de gráficos

Al finalizar está sesion, los diagramas utilizables en materiales de propuesta estarán guardados en outputs.

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

## 🚀 Step 1: Comprender los tipos de diagramas para presentaciones

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Comprender los tipos de diagramas para presentaciones",
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
Explique los tipos de diagramas utilizados en presentaciones de negocios y sus respectivos casos de uso.
Cubra diagramas de resumen, diagramas de flujo, graficos de comparacion, graficos de impacto y hojas de ruta con pautas especificas de uso.
```

**Resultado esperado**: Se explican cinco tipos de diagramas para presentaciones:
1. Diagramas de resumen (vision general)
2. Diagramas de flujo (explicación de procesos)
3. Gráficos de comparación (evaluación de opciones)
4. Gráficos de impacto (visualización de resultados)
5. Hojas de ruta (planificación futura)

---

## 🚀 Step 2: Crear un diagrama de arquitectura de sistemas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear un diagrama de arquitectura de sistemas",
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
Use diagram-generator para crear un diagrama de arquitectura de sistemas para una plataforma SaaS:

Componentes:
[Empresas clientes] → [Aplicacion web] → [API Gateway]
  ↓
[Microservicios]
  - Servicio de autenticacion
  - Servicio de gestion de datos
  - Servicio de analisis
  ↓
[Base de datos] + [Integraciones externas] (Slack, Gmail)

Use un diseno profesional adecuado para documentacion tecnica.
Salida: ~/ai-agent-camp/output/system-architecture.png
```

**Resultado esperado**: Se genera un diagrama profesional con la arquitectura del sistema organizada jerárquicamente.

---

## 🚀 Step 3: Crear una hoja de ruta de implementación

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear una hoja de ruta de implementacion",
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
Cree una hoja de ruta para la implementacion de un nuevo sistema:

Mes 1: Firma de contrato e inicio
Mes 2: Definicion de requisitos y analisis del estado actual
Mes 3: Migracion de datos y configuracion del entorno
Mes 4: Operacion de prueba y capacitacion
Mes 5: Lanzamiento en produccion y operacion paralela
Mes 6: Medicion de impacto y mejoras

Use un formato de linea de tiempo que muestre los hitos de cada fase.
Salida: ~/ai-agent-camp/output/roadmap.png
```

**Resultado esperado**: Se genera un plan de proyecto visualizado a lo largo de una línea de tiempo.

---

## 🚀 Step 4: Crear una tabla de comparación con competidores

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Crear una tabla de comparacion con competidores",
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
Cree una tabla de comparacion con competidores en formato de infografia:

[Nuestro servicio]
- Precio: 5,000 yenes/mes ◎
- Funciones: 15 funciones ◎
- Soporte: 24/7 ◎

[Competidor A]
- Precio: 8,000 yenes/mes △
- Funciones: 10 funciones ○
- Soporte: Solo dias habiles △

[Competidor B]
- Precio: 6,000 yenes/mes ○
- Funciones: 8 funciones △
- Soporte: Solo correo electronico ×

Disenelo para que nuestra ventaja competitiva sea inmediatamente clara.
Salida: ~/ai-agent-camp/output/comparison.png
```

**Resultado esperado**: Se genera una comparación visual clara de 3 empresas.

---

## 🚀 Step 5: Ejercicio práctico - Propuesta de renovación de sistema empresarial

Cree un conjunto práctico de diagramas para materiales de propuesta usando los siguientes prompts:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Ejercicio practico - Propuesta de renovacion de sistema empresarial",
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
Cree los siguientes 4 diagramas para una propuesta de renovacion de sistema empresarial:

1. Diagrama de problemas del sistema actual
   - Demasiado trabajo manual (eficiencia del 30%)
   - Datos dispersos en 3 sistemas
   - Errores frecuentes (20/mes)
   Salida: ~/ai-agent-camp/output/proposal-issues.png

2. Diagrama de arquitectura del nuevo sistema
   - Base de datos unificada
   - Flujos de trabajo automatizados
   - Panel de control en tiempo real
   Salida: ~/ai-agent-camp/output/proposal-new-system.png

3. Pasos de migracion (plan de 6 meses)
   Salida: ~/ai-agent-camp/output/proposal-migration.png

4. Beneficios proyectados de la implementacion
   - Eficiencia: 30% → 80%
   - Errores: 20/mes → 2/mes
   - Costo: ahorro anual de 3 millones de yenes
   Salida: ~/ai-agent-camp/output/proposal-benefits.png
```

**Resultado esperado**: Se genera un conjunto de 4 diagramas alineados con la narrativa de la propuesta.

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
      {"id": "trouble_1", "label": "El diagrama de arquitectura es demasiado complejo"},
      {"id": "trouble_2", "label": "La linea de tiempo de la hoja de ruta no es clara"},
      {"id": "trouble_3", "label": "La tabla de comparacion no transmite nuestra ventaja"},
      {"id": "trouble_4", "label": "El conjunto de diagramas carece de consistencia"}
    ]
  }]
}
```


### Problema 1: "El diagrama de arquitectura es demasiado complejo"
**Causa**: Todo está empaquetado en un solo diagrama
**Prompt de solución**:
```
Divida la arquitectura del sistema en 3 diagramas:
1. Nivel de resumen (vision general, solo componentes principales)
2. Nivel de detalle (estructura interna de cada servicio)
3. Flujo de datos (enfocado en el movimiento de datos)
```

### Problema 2: "La línea de tiempo de la hoja de ruta no es clara"
**Causa**: La representacion de la línea de tiempo es vaga
**Prompt de solución**:
```
Agregue lo siguiente a la hoja de ruta:
- Etiquetas claras de fecha o periodo
- Hitos que indiquen el inicio/fin de cada fase
- Use formato de diagrama de Gantt si hay tareas superpuestas
```

### Problema 3: "La tabla de comparación no transmite nuestra ventaja"
**Causa**: Énfasis visual insuficiente
**Prompt de solución**:
```
Para destacar nuestra ventaja competitiva:
- Rellene nuestra columna con un color prominente (azul o verde)
- Agregue insignias de "Recomendado" o "No.1" a los elementos superiores
- Muestre los numeros que superan a los competidores en fuente mas grande
```

### Problema 4: "El conjunto de diagramas carece de consistencia"
**Causa**: Cada diagrama se creó de forma independiente
**Prompt de solución**:
```
Unifique lo siguiente en los 4 diagramas:
- Paleta de colores: Azul (#0066CC) como base
- Fuente: Sans-serif, negrita para titulos
- Diseno: Titulo arriba a la izquierda, numero de pagina abajo a la derecha
- Coloque el logo o elementos de marca
```

---

## ✅ Punto de control
- [ ] Comprendio los tipos de diagramas necesarios para presentaciones
- [ ] Creo un diagrama de arquitectura de sistemas
- [ ] Creo una hoja de ruta de implementación
- [ ] Creo una tabla de comparación con competidores
- [ ] Completo el ejercicio práctico (conjunto de diagramas de propuesta)


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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-3-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-3-1
- finish → Finalizar
