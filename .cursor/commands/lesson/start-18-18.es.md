---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-17"]
level: "intermediate"
tags: ["pm", "meeting", "minutes", "spec-change"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-18: Diseno de reuniones y analisis de actas

| Elemento | Detalles |
|------|------|
| Objetivo | Disenar estructuras de reuniones para el proyecto TaskFlow y extraer automaticamente cambios de especificacion de actas de muestra usando IA |
| Duracion | ~25 min |
| Habilidades utilizadas | habilidad pm-toolkit |
| Requisitos previos | Lesson 18-17 completada |
| Pagina del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 📍 Paso 1: Diseno de tipos y propositos de reuniones

En la gestion de proyectos, una estructura de reuniones apropiada afecta en gran medida la eficiencia del flujo de informacion y la toma de decisiones. Para el proyecto TaskFlow, es necesario disenar una estructura de reuniones apropiada a la escala del proyecto.

### Clasificacion basica de reuniones

**Reuniones regulares (semanal/quincenal)**
- Reunion de pie: Informes de progreso y compartir problemas (15 min)
- Reunion de planificacion de sprint: Seleccion de tareas para el siguiente sprint (60 min)
- Retrospectiva de sprint: Reflexion sobre resultados y planificacion de mejoras (45 min)

**Reuniones de revision (segun necesidad)**
- Revision de diseno: Discusion y aprobacion de especificaciones (90 min)
- Revision de codigo: Aseguramiento de calidad y compartir conocimientos (60 min)
- Revision de negocio: Informes a partes interesadas (120 min)

**Reuniones de retrospectiva (fin de sprint)**
- Taller de retrospectiva: Aprendizaje entre equipos y descubrimiento de mejoras (60 min)
- Retrospectiva de riesgos: Evaluacion de riesgos del proyecto (45 min)

**Reuniones ad-hoc**
- Reunion de respuesta de emergencia: Discusion para incidentes en produccion (30 min)
- Reunion de solicitudes de clientes: Discusion de nuevos requisitos (60 min)

```json
{
  "type": "AskQuestion",
  "question": "Como desea disenar la escala de la estructura de reuniones del proyecto TaskFlow?",
  "options": [
    {
      "id": "small_team",
      "label": "Equipo pequeno (3-5 personas) - 3 tipos de reuniones",
      "meetings": [
        "Daily Standup",
        "Sprint Planning & Review",
        "Design Review"
      ],
      "frequency": "lightweight"
    },
    {
      "id": "medium_team",
      "label": "Equipo mediano (6-15 personas) - 6 tipos de reuniones",
      "meetings": [
        "Daily Standup",
        "Sprint Planning",
        "Sprint Review",
        "Sprint Retrospective",
        "Design Review",
        "Business Review"
      ],
      "frequency": "standard"
    },
    {
      "id": "large_org",
      "label": "Organizacion grande (16+ personas) - 7+ tipos de reuniones",
      "meetings": [
        "Daily Standup",
        "Sprint Planning",
        "Sprint Review",
        "Sprint Retrospective",
        "Design Review",
        "Code Review",
        "Business Review",
        "Risk Review",
        "Executive Steering"
      ],
      "frequency": "comprehensive"
    }
  ],
  "context": "La escala de la estructura de reuniones se determina por la composicion del equipo, la complejidad del proyecto y el numero de partes interesadas. Las reuniones excesivas reducen la productividad, por lo que se busca una configuracion minima pero efectiva."
}
```

## 🚀 Paso 2: Creacion de diagramas de estructura de reuniones con PlantUML

Cree diagramas de estructura con PlantUML para expresar visualmente la estructura de reuniones, relaciones y flujo.

```json
{
  "type": "AskQuestion",
  "question": "Que estilo desea para el diagrama de estructura de reuniones?",
  "options": [
    {
      "id": "org_chart",
      "label": "Tipo organigrama (jerarquia y subordinacion de reuniones)",
      "focus": "hierarchy",
      "best_for": "Flujo de toma de decisiones, clarificacion de la distribucion de responsabilidades"
    },
    {
      "id": "flow_chart",
      "label": "Tipo flujo (flujo de reuniones a lo largo de una linea de tiempo)",
      "focus": "timeline",
      "best_for": "Ciclo de sprint, proceso de toma de decisiones"
    },
    {
      "id": "matrix",
      "label": "Tipo matriz (tabla de correspondencia de reuniones, asistentes y salidas)",
      "focus": "relationship",
      "best_for": "Distribucion de roles de asistentes, alcance de responsabilidad"
    }
  ],
  "context": "La eleccion del estilo del diagrama se determina por la audiencia de la presentacion (ejecutivos o personal de campo) y la legibilidad de la informacion."
}
```

### Ejemplo de diagrama PlantUML (tipo flujo)

```plantuml
@startuml TaskFlow_MeetingStructure
!define ACCENT_COLOR #FF6B6B
!define PRIMARY_COLOR #4ECDC4
!define SUCCESS_COLOR #95E1D3

skinparam defaultFontName "Courier New"
skinparam defaultFontSize 12
skinparam backgroundColor #FFFACD
skinparam classBorderColor #333
skinparam classBackgroundColor #FFF
skinparam arrowColor #333

rectangle "Sprint Cycle (2 weeks)" #E8F8F5 {
  node "Monday\nSprint Planning\n(10:00-11:00)" as planning #PRIMARY_COLOR
  node "Daily\nStandup\n(09:30-10:00)" as standup #4ECDC4
  node "Wednesday\nDesign Review\n(14:00-15:30)" as design #FF9999
  node "Friday\nSprint Review\n(15:00-16:30)" as review #ACCENT_COLOR
  node "Friday\nRetro\n(16:30-17:30)" as retro #95E1D3

  planning --> standup: attend
  standup --> design: issues found
  design --> review: design approved
  review --> retro: feedback
  retro --> planning: improvements
}

rectangle "Ad-hoc Meetings" #FFE8E8 {
  node "Customer Request\nMeeting" as customer #FF6B6B
  node "Emergency\nResponse" as emergency #DD3C51
}

note right of planning
  Attendees: Team Lead, Dev, PM
  Output: Sprint Goal, Task Board
end note

note right of design
  Attendees: Architect, Senior Dev
  Output: Design Approval, Issues
end note

@enduml
```

Este diagrama incluye los siguientes elementos:

- **Ciclo principal**: Reuniones regulares dentro de un ciclo de sprint de 2 semanas
- **Asistentes**: Lista de asistentes para cada reunion
- **Salidas**: Entregables generados de las reuniones
- **Dependencias**: Flujo donde las decisiones de reuniones anteriores afectan las siguientes

Genere el archivo: **output/pm/meeting-structure.puml**

## ⚠️ Paso 3: Carga de actas de reuniones de muestra

Utilice las siguientes actas de reunion de muestra como objetivos de analisis.

Las actas de reunion tipicamente contienen la siguiente informacion:

- **Informacion de la reunion**: Fecha/hora, ubicacion, asistentes
- **Agenda**: Lista de temas de discusion
- **Decisiones**: Politicas y especificaciones acordadas
- **Elementos de accion**: Tareas de seguimiento, responsables, plazos
- **Problemas/Riesgos**: Problemas identificados
- **Siguiente reunion programada**: Seguimiento

Ejemplo parcial de actas de reunion de muestra:

```markdown
# Actas de la reunión

## Información de la reunión
- Fecha/Hora: 2024-02-09 10:00-11:30
- Lugar: Zoom / Meeting Room A
- Asistentes: PM (Tanaka), Dev Lead (Sato), Architect (Suzuki), QA (Ando)

## Agenda
1. Informe de progreso del Sprint #5
2. Especificación de UI de la pantalla de creación de tareas
3. Estrategia de optimización del tiempo de respuesta de la API
4. Plan de pruebas previo al lanzamiento a producción

## Decisiones
- Pantalla de creación de tareas: Agregar campo "Prioridad" (desplegable: Baja/Media/Alta/Urgente)
- Objetivo de tiempo de respuesta de API: Establecer en 500ms o menos en P95
- Lanzamiento a producción: Programado para mediados de marzo

## Cambios de especificación
- Agregar campo priority a la API de creación de tareas (enum: low, medium, high, urgent)
- Implementar función de filtro en la API de lista de tareas (filter by status, assignee, priority)
- UI: Agregar visualización de "Prioridad" en la pantalla de detalle de tareas

## Elementos de acción
| Elemento | Responsable | Plazo |
|------|------|------|
| Creación de especificación del campo de prioridad | Suzuki | 2024-02-12 |
| Actualización del esquema de API | Sato | 2024-02-13 |
| Actualización del documento de diseño de UI | Tanaka | 2024-02-14 |
| Diseño de casos de prueba | Ando | 2024-02-16 |

## Riesgos/Problemas
- La optimización del tiempo de respuesta de la API tiene alta complejidad técnica -> Extender el período de respuesta en 1 semana
- Se necesita evaluación de impacto por la adición de índices de BD
```

```json
{
  "type": "AskQuestion",
  "question": "A que nivel de profundidad desea realizar el analisis de las actas de reunion?",
  "options": [
    {
      "id": "spec_changes_only",
      "label": "Extraer solo cambios de especificacion",
      "extraction_target": [
        "Cambios de esquema de API",
        "Cambios de requisitos de UI",
        "Cambios de esquema de BD",
        "Adición de nuevas funciones"
      ]
    },
    {
      "id": "all_decisions",
      "label": "Extraer todas las decisiones (especificaciones + politicas + aprobaciones)",
      "extraction_target": [
        "Cambios de especificación",
        "Decisiones técnicas",
        "Decisiones de asignación de recursos",
        "Finalización del cronograma de lanzamiento"
      ]
    },
    {
      "id": "comprehensive",
      "label": "Analisis completo incluyendo elementos de accion",
      "extraction_target": [
        "Cambios de especificación",
        "Todas las decisiones",
        "Elementos de acción (responsable + plazo)",
        "Registro de riesgos/problemas",
        "Nivel de acuerdo de las partes interesadas"
      ]
    }
  ],
  "context": "La profundidad del analisis se determina por la escala del proyecto y los sistemas de seguimiento. Para proyectos medianos o grandes, la gestion de elementos de accion a traves de analisis completo es importante."
}
```

## ✅ Paso 4: Extraccion automatica de cambios de especificacion por IA

Extraer automaticamente las secciones correspondientes a cambios de especificacion de las actas de reunion y generarlas como un informe estructurado.

Informacion a extraer:

- **Contenido del cambio**: Que componente (API/UI/DB) cambia
- **Alcance del impacto**: Que funciones o modulos se ven afectados
- **Razon del cambio**: Por que se necesita este cambio (requisito de negocio o razon tecnica)
- **Prioridad de respuesta**: Prioridad para implementar este cambio (Critical/High/Medium/Low)
- **Esfuerzo estimado**: Trabajo necesario para la implementacion (horas o Story Points)
- **Plazo de respuesta**: Cuando necesita ser atendido

Formato de salida para resultados de extraccion automatica (Markdown):

```markdown
# Informe de extracción de cambios de especificación

Fecha de generación: 2024-02-10 15:45 JST
Fuente: meeting-minutes-sample.md (2024-02-09)
Objetivo de análisis: Se extrajeron 3 cambios de especificación de 4 decisiones

## Lista de cambios de especificación

### Cambio #1: Adición del campo de prioridad de tareas

| Elemento | Detalles |
|------|------|
| **Contenido del cambio** | Agregar campo priority a la API de creación de tareas (enum: low/medium/high/urgent) |
| **Alcance del impacto** | - API: POST /tasks, GET /tasks, PUT /tasks/{id}<br>- BD: Agregar columna priority a la tabla tasks<br>- UI: Agregar desplegable a pantallas de creación/edición de tareas<br>- Pruebas: Agregar casos de prueba para filtro de prioridad |
| **Razón del cambio** | Requisito de negocio. La priorización de tareas permite al equipo priorizar el trabajo según la importancia. Solicitud del cliente. |
| **Prioridad de respuesta** | **High** |
| **Esfuerzo estimado** | 8 Story Points (API 3 días + UI 2 días + Pruebas 2 días) |
| **Plazo de respuesta** | 2024-02-16 |
| **Responsable de diseño** | Suzuki |
| **Responsable de implementación** | Equipo Sato |

Elementos de acción relacionados:
- [ ] Detalle de la especificación (plazo: 2024-02-12)
- [ ] Actualización del esquema de API (plazo: 2024-02-13)
- [ ] Actualización del documento de diseño de pantallas (plazo: 2024-02-14)
- [ ] Diseño de casos de prueba (plazo: 2024-02-16)

### Cambio #2: Implementación de función de filtro de lista de tareas

| Elemento | Detalles |
|------|------|
| **Contenido del cambio** | Agregar función de filtro basada en parámetros de consulta a GET /tasks API<br>Filtros soportados: status, assignee, priority |
| **Alcance del impacto** | - API: Extensión del endpoint GET /tasks<br>- BD: Optimización de índices (mejora de rendimiento)<br>- Frontend: Implementación de UI de filtro |
| **Razón del cambio** | Mejora de usabilidad. Los usuarios pueden buscar eficientemente las tareas necesarias de una gran lista. |
| **Prioridad de respuesta** | **High** |
| **Esfuerzo estimado** | 13 Story Points (API 3 días + Frontend 2 días + Optimización de BD 1 día + Pruebas 2 días) |
| **Plazo de respuesta** | 2024-02-23 |
| **Responsable de diseño** | Suzuki |
| **Responsable de implementación** | Sato, Tanaka |

Riesgo: Se necesita evaluación de impacto en datos existentes por la adición de índices de BD

### Cambio #3: Establecimiento de objetivos de tiempo de respuesta de API

| Elemento | Detalles |
|------|------|
| **Contenido del cambio** | Establecer requisitos no funcionales de tiempo de respuesta de API<br>P95: 500ms o menos, P99: 1000ms o menos |
| **Alcance del impacto** | - API: Optimización de todos los endpoints<br>- Infraestructura: Introducción de estrategia de caché<br>- Pruebas: Automatización de pruebas de rendimiento |
| **Razón del cambio** | Necesidad técnica. Mejora de la experiencia del usuario. Condición esencial para el cumplimiento del SLA. |
| **Prioridad de respuesta** | **Critical** |
| **Esfuerzo estimado** | 21 Story Points (Investigación/análisis 2 días + Implementación 4 días + Pruebas 2 días + Verificación en producción 1 día) |
| **Plazo de respuesta** | 2024-03-01 (antes del lanzamiento a producción) |
| **Responsable de diseño** | Suzuki |
| **Responsable de implementación** | Sato (Backend), Equipo de infraestructura |

## Resumen

- **Cambios de especificación extraídos**: 3
- **Critical**: 1
- **High**: 2
- **Esfuerzo total estimado**: 42 Story Points
- **Cantidad de riesgos**: 1 (verificación de índices de BD)
- **Próximo seguimiento**: 2024-02-13 Reunión de revisión de progreso

## Confianza de la extracción automática

- Confianza de la IA para todos los elementos extraídos: 95%
- Elemento de revisión manual recomendado: Evaluación de impacto de índices de BD del Cambio #2
- Responsable de verificación: Líder de infraestructura (Yamada)
```

Genere el archivo: **output/pm/spec-changes.md**


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── retrospective.md  (informe de retrospectiva)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/retrospective.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/retrospective.md
```

> 💡 Texto completo: Ejecute `cat output/pm/retrospective.md` para mostrar el texto completo

## ➡️ Finalizacion y siguientes pasos

Verifique que los siguientes entregables esten completos y ubicados en output/pm/.

**Archivos a generar:**

1. **meeting-structure.puml** - Diagrama de estructura de reuniones en formato PlantUML
   - Mostrar reuniones regulares dentro del ciclo de sprint
   - Documentar asistentes y salidas de cada reunion
   - Mostrar reuniones ad-hoc en una seccion separada

2. **spec-changes.md** - Informe de extraccion de cambios de especificacion
   - Formato de tabla incluyendo contenido del cambio, alcance del impacto y razones
   - Evaluacion de prioridad y riesgos
   - Mapeo a elementos de accion

**Criterios de finalizacion:**
- El diagrama PlantUML se renderiza correctamente (sin errores)
- Se extraen al menos 3 cambios de especificacion
- La prioridad y el esfuerzo estimado estan especificados para cada cambio
- La confianza de extraccion de IA es del 90% o superior

**Next Lesson**: Continuar con la creacion del panel de control marimo con `/start-18-19`

Las habilidades de diseno de reuniones y analisis de actas con IA adquiridas en esta leccion son practicas importantes para visualizar la toma de decisiones del proyecto y prevenir requisitos de cambio perdidos. La gestion estructurada de reuniones y la extraccion automatizada de informacion mejoran significativamente la eficiencia y precision del PM.
