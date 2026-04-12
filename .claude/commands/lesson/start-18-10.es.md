---
description: "When the user says /start-18-10 — Module 18 Lesson 18-10: PM - WBS y diagrama de Gantt"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-9", "output/pm/api-spec.yaml"]
level: "intermediate"
tags: ["pm", "wbs", "gantt", "schedule"]
---

# 🎓 Lesson 18-10: WBS y diagrama de Gantt

| Elemento | Detalles |
|------|------|
| Objetivo | Crear un WBS para el proyecto TaskFlow y generar un diagrama de Gantt con PlantUML |
| Duración | ~25 min |
| Habilidades utilizadas | habilidad pm-toolkit |
| Requisitos previos | Lesson 18-9 completada, todos los documentos de diseño hasta este punto estan disponibles |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

---

## 📍 Objetivos de aprendizaje

En esta lección, aprenderá lo siguiente:

- Como crear un **WBS (Work Breakdown Structure)**
- Descomposición de tareas y estructuración jerárquica del proyecto
- Métodos clave de estimación de esfuerzo
- Generación y utilización de diagramas de Gantt PlantUML
- Análisis de ruta crítica

---

## 🚀 Paso 1: Creación del WBS

Una Work Breakdown Structure (WBS) es un método para descomponer un proyecto en tareas más pequeñas y manejables. Visualice la estructura general del proyecto TaskFlow.

### 📊 Estructura WBS de TaskFlow

```text
Proyecto TaskFlow
├── 1. Fase de planificacion
│   ├── 1.1 Definicion de requisitos
│   ├── 1.2 Analisis competitivo
│   └── 1.3 Plan del proyecto
├── 2. Fase de diseno
│   ├── 2.1 Diseno del sistema
│   ├── 2.2 Diseno UI/UX
│   ├── 2.3 Diseno de base de datos
│   └── 2.4 Diseno de especificaciones de API
├── 3. Fase de implementacion
│   ├── 3.1 Desarrollo backend
│   ├── 3.2 Desarrollo frontend
│   ├── 3.3 Integracion
│   └── 3.4 Configuracion del entorno de pruebas
├── 4. Fase de pruebas
│   ├── 4.1 Pruebas unitarias
│   ├── 4.2 Pruebas de integracion
│   ├── 4.3 UAT
│   └── 4.4 Pruebas en entorno de produccion
└── 5. Fase de despliegue y operaciones
    ├── 5.1 Preparacion del entorno de produccion
    ├── 5.2 Despliegue
    ├── 5.3 Inicio de operaciones
    └── 5.4 Configuracion de soporte al usuario
```

### ❓ Seleccionar granularidad del WBS

```json
{
  "type": "AskQuestion",
  "id": "wbs-granularity",
  "question": "Seleccione la granularidad del WBS",
  "description": "Seleccione el nivel de descomposicion del WBS segun la escala y complejidad del proyecto",
  "options": [
    {
      "value": "level2",
      "label": "Solo elementos principales (Nivel 2)",
      "description": "Solo 5 fases principales. Para proyectos pequenos",
      "recommended": false
    },
    {
      "value": "level3",
      "label": "Hasta elementos de nivel medio (Nivel 3)",
      "description": "Tareas principales de cada fase. Nivel recomendado",
      "recommended": true
    },
    {
      "value": "level4",
      "label": "Detallado (Nivel 4)",
      "description": "Mas subdividido. Para proyectos complejos",
      "recommended": false
    },
    {
      "value": "ai-suggest",
      "label": "Obtener sugerencia de granularidad optima de IA",
      "description": "Determinacion automatica a partir de la escala del proyecto"
    }
  ],
  "default": "level3"
}
```

---

## 💼 Paso 2: Estimación de esfuerzo

Estime el esfuerzo necesario para cada tarea del WBS. La estimación precisa del esfuerzo es clave para el éxito del proyecto.

### 📌 Métodos clave de estimación

| Método | Características | Escenario de aplicación |
|------|------|---------|
| **Estimación analoga** | Estimar a partir de proyectos similares anteriores | Cuando existe amplia experiencia |
| **Estimación de tres puntos** | Calcular a partir de valores optimista/más probable/pesimista | Cuando la incertidumbre es alta |
| **Método de puntos de función** | Calcular por complejidad de función | Desarrollo de software |
| **Estimación ascendente** | Acumular a partir de tareas detalladas | Después del diseño detallado |

### ❓ Seleccionar método de estimación

```json
{
  "type": "AskQuestion",
  "id": "estimation-method",
  "question": "Seleccione el metodo de estimacion",
  "description": "Seleccione el metodo de estimacion apropiado segun las caracteristicas del proyecto",
  "options": [
    {
      "value": "analogy",
      "label": "Estimacion analoga",
      "description": "Estimacion a partir de proyectos similares anteriores. Para estimacion rapida"
    },
    {
      "value": "three-point",
      "label": "Estimacion de 3 puntos (Optimista/Mas probable/Pesimista)",
      "description": "Metodo PERT. Estimacion precisa considerando la incertidumbre"
    },
    {
      "value": "function-point",
      "label": "Analisis de puntos de funcion",
      "description": "Cuantificacion por complejidad de funcionalidades. Optimo para desarrollo de software"
    },
    {
      "value": "ai-estimate",
      "label": "Obtener estimacion de IA",
      "description": "Estimacion automatica analizando el WBS"
    }
  ],
  "default": "three-point"
}
```

### 📋 Ejemplo de estimación de esfuerzo de TaskFlow (estimación de tres puntos)

| Código WBS | Tarea | Optimista (dias) | Más probable (dias) | Pesimista (dias) | Esperado (dias) |
|-----------|--------|----------|----------|----------|-----------|
| 1.1 | Definición de requisitos | 2 | 3 | 5 | 3.2 |
| 1.2 | Análisis competitivo | 1 | 2 | 4 | 2.2 |
| 1.3 | Planificación del proyecto | 1 | 2 | 3 | 2.0 |
| 2.1 | Diseño del sistema | 3 | 5 | 8 | 5.2 |
| 2.2 | Diseño UI/UX | 2 | 4 | 7 | 4.2 |
| 2.3 | Diseño de BD | 2 | 3 | 5 | 3.2 |
| 2.4 | Diseño de especificación API | 2 | 3 | 5 | 3.2 |
| 3.1 | Desarrollo backend | 8 | 12 | 18 | 12.3 |
| 3.2 | Desarrollo frontend | 6 | 10 | 15 | 10.2 |
| 3.3 | Integración | 2 | 4 | 7 | 4.2 |
| 3.4 | Configuración de entorno de pruebas | 1 | 2 | 3 | 2.0 |
| 4.1 | Pruebas unitarias | 3 | 5 | 8 | 5.2 |
| 4.2 | Pruebas de integración | 2 | 4 | 6 | 4.0 |
| 4.3 | UAT | 2 | 3 | 5 | 3.2 |
| 4.4 | Pruebas en entorno de producción | 1 | 2 | 3 | 2.0 |
| 5.1 | Preparación del entorno de producción | 1 | 2 | 4 | 2.2 |
| 5.2 | Despliegue | 1 | 2 | 3 | 2.0 |
| 5.3 | Inicio de operaciones | 1 | 2 | 3 | 2.0 |
| 5.4 | Configuración de soporte | 1 | 1 | 2 | 1.2 |

**Esfuerzo total planificado: 73.7 dias-persona**

---

## 📅 Paso 3: Generación de diagramas de Gantt PlantUML

Los diagramas de Gantt visualizan cronogramas de proyectos, dependencias de tareas y progreso.

### ❓ Seleccionar período de visualización del diagrama de Gantt

```json
{
  "type": "AskQuestion",
  "id": "gantt-period",
  "question": "Seleccione el periodo de visualizacion del diagrama de Gantt",
  "description": "Seleccione el periodo de visualizacion segun la duracion del proyecto",
  "options": [
    {
      "value": "1month",
      "label": "1 mes",
      "description": "Visualizacion detallada diaria"
    },
    {
      "value": "3months",
      "label": "3 meses",
      "description": "Recomendado. Duracion tipica del proyecto"
    },
    {
      "value": "6months",
      "label": "6 meses",
      "description": "Para proyectos a gran escala"
    },
    {
      "value": "custom",
      "label": "Personalizado",
      "description": "Especificar cualquier periodo"
    }
  ],
  "default": "3months"
}
```

### 📊 Ejemplo de diagrama de Gantt PlantUML

```plantuml
@startgantt
title Diagrama de Gantt del proyecto TaskFlow
dateFormat YYYY-MM-DD
projectScale monthly
axisFormat %Y-%m

section Planificacion
Definicion de requisitos :crit, wbs-1-1, 2024-04-01, 3d
Analisis competitivo   :crit, wbs-1-2, after wbs-1-1, 2d
Plan del proyecto      :crit, wbs-1-3, after wbs-1-2, 2d

section Diseno
Diseno del sistema     :des1, wbs-2-1, after wbs-1-3, 5d
Diseno UI/UX           :des1, wbs-2-2, after wbs-1-3, 4d
Diseno de BD           :des2, wbs-2-3, after wbs-2-1, 3d
Diseno de espec. API   :des2, wbs-2-4, after wbs-2-1, 3d
Revision de diseno     :milestone, des-review, after wbs-2-4, 1d

section Implementacion
Desarrollo backend     :impl1, wbs-3-1, after des-review, 12d
Desarrollo frontend    :impl1, wbs-3-2, after des-review, 10d
Integracion            :impl2, wbs-3-3, after wbs-3-1, 4d
Config. entorno pruebas:impl2, wbs-3-4, after wbs-3-1, 2d

section Pruebas
Pruebas unitarias      :test1, wbs-4-1, after wbs-3-3, 5d
Pruebas de integracion :test1, wbs-4-2, after wbs-4-1, 4d
UAT              :test2, wbs-4-3, after wbs-4-2, 3d
Pruebas entorno prod.  :test2, wbs-4-4, after wbs-4-3, 2d
Pruebas completadas    :milestone, test-complete, after wbs-4-4, 1d

section Despliegue y operaciones
Preparacion entorno prod.:deploy1, wbs-5-1, after test-complete, 2d
Despliegue             :deploy1, wbs-5-2, after wbs-5-1, 2d
Inicio de operaciones  :deploy2, wbs-5-3, after wbs-5-2, 2d
Configuracion soporte  :deploy2, wbs-5-4, after wbs-5-3, 1d
Lanzamiento            :crit, milestone, after wbs-5-4, 1d

@endgantt
```

### 🎯 Elementos clave de sintaxis de Gantt PlantUML

```markdown
- **dateFormat**: Formato de fecha (YYYY-MM-DD, etc.)
- **projectScale**: Unidad de visualizacion (diario/semanal/mensual)
- **section**: Nombre de seccion (fase)
- **Definicion de tarea**: `Nombre de tarea :type, id, start, duration`
  - type: `crit` (critico), `milestone` (hito), `active` (en progreso)
  - start: `2024-04-01` o `after id`
  - duration: `5d` (5 dias), `1w` (1 semana)
- **Hito**: Se muestra con el tipo `milestone`
```

---

## 🔍 Paso 4: Análisis de ruta crítica

La ruta crítica es el camino más largo hasta la finalización del proyecto y el conjunto de tareas con mayor impacto por retrasos.

### ❓ Realizar análisis de ruta crítica

```json
{
  "type": "AskQuestion",
  "id": "critical-path",
  "question": "Realizar analisis de ruta critica?",
  "description": "Gestione el riesgo de retraso del proyecto identificando la ruta critica",
  "options": [
    {
      "value": "ai-analyze",
      "label": "Si, que la IA analice",
      "description": "Analisis automatico a partir del WBS y estimaciones de esfuerzo. Recomendado"
    },
    {
      "value": "manual",
      "label": "Verificar por mi mismo",
      "description": "Identificar manualmente verificando el WBS y las dependencias"
    },
    {
      "value": "skip",
      "label": "Omitir",
      "description": "Omitir el analisis de ruta critica"
    }
  ],
  "default": "ai-analyze"
}
```

### 📍 Ejemplo de ruta crítica de TaskFlow

**Camino más largo (aproximadamente 55 dias de esfuerzo total):**
```text
Definicion de requisitos (3.2 dias)
→ Analisis competitivo (2.2 dias)
→ Plan del proyecto (2.0 dias)
→ Diseno del sistema (5.2 dias)
→ Diseno de espec. API (3.2 dias)
→ Desarrollo backend (12.3 dias)
→ Integracion (4.2 dias)
→ Pruebas unitarias (5.2 dias)
→ Pruebas de integracion (4.0 dias)
→ UAT (3.2 dias)
→ Pruebas entorno produccion (2.0 dias)
→ Preparacion entorno produccion (2.2 dias)
→ Despliegue (2.0 dias)
→ Inicio de operaciones (2.0 dias)
→ Configuracion soporte (1.2 dias)
```

### ⚠️ Identificación de areas de riesgo

| Area de riesgo | Factor | Contramedida |
|-----------|------|------|
| Desarrollo backend | Tarea de implementación más larga (12.3 dias) | Inicio temprano, asegurar recursos |
| Integración | Interacciones inesperadas | Realizar pruebas de integración tempranas |
| Diseño de base de datos | Posibilidad de cambios en requisitos | Priorizar la finalización de requisitos |

---

## 📝 Lista de verificación de entregables

### ✅ Archivos de salida

1. **output/pm/wbs.md** - Estructura WBS y descripción detallada
2. **output/pm/gantt-chart.puml** - Diagrama de Gantt PlantUML

### ✅ Punto de control

```markdown
□ WBS descompuesto a Nivel 3 o superior
□ Estimaciones de esfuerzo establecidas para todas las tareas
□ Diagrama de Gantt generado
□ 3 o mas hitos establecidos
□ Archivo wbs.md generado
□ Archivo gantt-chart.puml generado
□ Ruta critica identificada (opcional)
□ Areas de riesgo identificadas (opcional)
```

---

## 🔧 Solución de problemas

### ❓ No sabe la granularidad de descomposición del WBS

**Solución:**
- Se recomienda comenzar con el Nivel 3 (elementos de nivel medio)
- 20-30 tareas es un rango manejable
- 3-5 elementos WBS por fase es una guía

### ❓ No hay base para la estimación de esfuerzo

**Solución:**
- Consultar el rendimiento de tareas similares anteriores
- Considerar los niveles de habilidad de los miembros del equipo
- Absorber la incertidumbre con estimación de tres puntos
- Asegurar un buffer (10-20%)

### ❓ No entiende la sintaxis de Gantt PlantUML

**Solución:**
- Consulte la [documentación oficial de Gantt PlantUML](https://plantuml.com/gantt-diagram)
- Expresar dependencias con la palabra clave `after`
- Mostrar hitos principales con `milestone`
- Resaltar tareas críticas con `crit`

### ❓ No puede comprender el concepto de ruta crítica

**Solución:**
- Aprender lo básico del CPM (Critical Path Method)
- Calcular la "fecha de inicio más temprana" y "fecha de inicio más tardia" para cada tarea
- Las tareas con holgura (float) cero forman la ruta crítica
- Gestionarlas como prioridad ya que tienen el mayor impacto por retrasos

---

## 🎬 Siguientes pasos

### ➡️ Siguiente lección

**[Lesson 18-11: Integración con Notion](./start-18-11.md)**

A traves de la integración con Notion, comparta el WBS y el diagrama de Gantt con todo el equipo y gestione el progreso en tiempo real.

### 📚 Recursos relacionados

- [Module 18: PM y definición de sistema](https://ai-agent.camp/es/course/module-18)
- [Documentación oficial de Gantt PlantUML](https://plantuml.com/gantt-diagram)

---

## 📌 Puntos clave

🎯 **El WBS aclara "que hacer"**
- Las tareas ambiguas conducen a problemas más adelante
- Cada tarea debe ser independiente y completa (principio MECE)

⏱️ **Sea conservador con las estimaciones de esfuerzo**
- Agregar un buffer de 20-30% a las estimaciones iniciales
- Si la incertidumbre disminuye durante la implementación, el buffer se puede reducir

📊 **El diagrama de Gantt es un documento vivo**
- Actualizar regularmente incluso después de que comience el proyecto
- Verificar regularmente las discrepancias entre lo real y lo planificado (tasa de progreso, esfuerzo restante)

🚨 **Las tareas fuera de la ruta crítica tienen flexibilidad**
- Utilizar eficazmente el buffer (holgura) para el ajuste de recursos
- Sin embargo, tenga en cuenta que cuando se consume la holgura, la ruta crítica puede cambiar

---

**Cuando se complete esta lección, proceda a la Lección 18-11.**
