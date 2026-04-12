---
description: "When the user says /start-18-3 — Module 18 Lesson 18-3: PM - Creación de PRD (Método Working Backwards)"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-2", "output/pm/requirements-brief.md"]
level: "intermediate"
tags: ["pm", "prd", "working-backwards"]
---

# 🎓 Lesson 18-3: Creación de PRD (Método Working Backwards)

## 📍 Lo que hará en esta sesión

| Elemento | Detalles |
|------|------|
| Objetivo | Crear el PRD de TaskFlow utilizando el método Amazon Working Backwards |
| Duración | ~30 min |
| Habilidades utilizadas | habilidad pm-toolkit |
| Requisitos previos | Lesson 18-2 completada、output/pm/requirements-brief.md existe |
| Página del material | [Module 18: PM y definición de requisitos del sistema](https://ai-agent.camp/es/course/module-18) como referencia paralela |

**Flujo de la sesión:**
1. Explicación del método Working Backwards
2. Redacción de un PRD en formato de comunicado de prensa
3. Adición de FAQ e historias de usuario
4. Generación y formato de prd.md

Entregable: `output/pm/prd.md`

---

## 🎯 Verificación de preparación - readiness check

```json
{
  "type": "AskQuestion",
  "question": "Verificacion de preparacion para iniciar esta leccion",
  "description": "Antes de comenzar la Leccion 18-3, verifique las condiciones necesarias.",
  "options": [
    {
      "label": "Listo. Leccion 18-2 completada, requirements-brief.md existe",
      "value": "ready",
      "next_action": "continue"
    },
    {
      "label": "Quiero revisar la Leccion 18-2",
      "value": "review_previous",
      "next_action": "view_html",
      "url": "../../start-18-2"
    },
    {
      "label": "Quiero verificar la estructura actual de archivos",
      "value": "check_structure",
      "next_action": "bash",
      "command": "ls -la output/pm/ 2>/dev/null || echo 'Directory not found'"
    },
    {
      "label": "Quiero aprender el Modulo 18 desde el principio",
      "value": "start_module",
      "next_action": "view_html",
      "url": "https://ai-agent.camp/es/course/module-18"
    }
  ]
}
```

**Elementos de confirmación:**
- ✓ Lesson 18-2 (Informe de definición de requisitos) esta completada
- ✓ `output/pm/requirements-brief.md` existe
- ✓ Se comprende el contexto del proyecto

---

## 🚀 Step 1: Comprensión y preparación del método Working Backwards

```json
{
  "type": "AskQuestion",
  "question": "Que tan familiarizado esta con el metodo Amazon Working Backwards?",
  "description": "El metodo Working Backwards es un enfoque innovador de desarrollo de productos adoptado por Amazon. Verificaremos su nivel de conocimiento con este metodo y ajustaremos el nivel de explicacion en consecuencia.",
  "options": [
    {
      "label": "Lo conozco bien (aprendi de casos de Amazon y libros)",
      "value": "expert",
      "next_action": "continue"
    },
    {
      "label": "Solo conozco la descripcion general (desarrollar desde la perspectiva del cliente)",
      "value": "intermediate",
      "next_action": "continue"
    },
    {
      "label": "Primera vez que lo escucho, o 'que es eso?'",
      "value": "beginner",
      "next_action": "continue"
    }
  ]
}
```

### Que es el método Working Backwards

El método Working Backwards es un enfoque de desarrollo de Amazon que **"define el producto trabajando hacia atras desde la perspectiva del cliente."**

**Diferencias con los métodos de desarrollo tradicionales:**

| Método tradicional | Working Backwards |
|--------|-----------------|
| Comenzar desde especificaciones técnicas | **Comenzar desde la experiencia del cliente** |
| Pensar en el uso después de completar | **Escribir el comunicado de prensa primero** |
| Definición de requisitos desde perspectiva interna | **Escribir primero las preguntas del cliente (FAQ)** |

**Los 5 pasos de Working Backwards:**

1. **Comunicado de prensa (Press Release)** - Escribir el anuncio del producto para los clientes
2. **FAQ (Preguntas frecuentes)** - Responder preguntas de clientes y partes interesadas
3. **Historias de usuario (User Stories)** - Definir escenarios de uso específicos
4. **Definición de alcance (Scope)** - Distinguir entre MVP y versiones futuras
5. **Métricas de éxito (Success Metrics)** - Definir KPIs

**Al aplicar a TaskFlow:**
- Aclarar quien "tiene dificultades con la gestión de tareas"
- Expresar "que cambios harian felices a los usuarios" en el comunicado de prensa
- Explicar "por que es necesario" en las FAQ

### Preparación: Revisar documentos anteriores

```json
{
  "type": "AskQuestion",
  "question": "Desea revisar el contenido de requirements-brief.md?",
  "description": "El Requirements Brief anterior servira como material de referencia al crear el comunicado de prensa en el Paso 2. Se recomienda revisar el contenido de antemano.",
  "options": [
    {
      "label": "Verificar el contenido (mostrar el archivo)",
      "value": "view",
      "next_action": "bash",
      "command": "cat output/pm/requirements-brief.md || echo 'File not found'"
    },
    {
      "label": "Ya verificado, continuar al siguiente paso",
      "value": "skip",
      "next_action": "continue"
    },
    {
      "label": "Archivo no encontrado, necesito ayuda",
      "value": "help",
      "next_action": "bash",
      "command": "find . -name 'requirements-brief.md' -o -name '*requirement*' 2>/dev/null | head -10"
    }
  ]
}
```

---

## 🚀 Paso 2: Redacción del PRD en formato de comunicado de prensa

Al escribir el PRD en formato de comunicado de prensa, se crea un documento donde **los beneficios para el cliente son claros** y que es **fácil de entender para los ingenieros internos**.

```json
{
  "type": "AskQuestion",
  "question": "Como desea configurar el tono y el publico objetivo del comunicado de prensa?",
  "description": "En el metodo Working Backwards, la forma de redactar el comunicado de prensa es importante. Ajuste el tono y el contenido segun el publico objetivo.",
  "options": [
    {
      "label": "Orientado a negocios (formal, asumiendo accionistas/inversores)",
      "value": "formal",
      "next_action": "continue"
    },
    {
      "label": "Orientado a startups (casual, asumiendo comunidad de usuarios)",
      "value": "casual",
      "next_action": "continue"
    },
    {
      "label": "Interno (practico, para ingenieros)",
      "value": "internal",
      "next_action": "continue"
    },
    {
      "label": "Orientado a inversores (enfocado en numeros, enfatizando crecimiento)",
      "value": "investor",
      "next_action": "continue"
    }
  ]
}
```

### Plantilla de comunicado de prensa

El comunicado de prensa de Working Backwards requiere las siguientes secciones:

**Secciones requeridas:**

```text
# [HEADLINE: Titulo conciso y poderoso]

## Resumen
[Describa la esencia del producto en un parrafo]

## Problema
[Que desafios enfrentan los clientes objetivo]

## Solucion
[Como TaskFlow resuelve esto, 3-5 puntos]

## Beneficios para el cliente
[Ventajas especificas para el cliente]

## Disponibilidad / Precios
[Disponibilidad y estrategia de precios]

## Mas informacion
[Sitio web, documentacion, informacion de contacto]

---

## Testimonios de clientes
"[Exprese los beneficios esperados en palabras del cliente]" - [Nombre de empresa, Cargo]
```

### Ejecución del Paso 2

```json
{
  "type": "AskQuestion",
  "question": "Desea que la IA genere el borrador del comunicado de prensa, o prefiere crearlo manualmente?",
  "description": "En el Paso 2, puede elegir que la IA genere automaticamente un borrador del comunicado de prensa leyendo requirements-brief.md, o crearlo manualmente usted mismo.",
  "options": [
    {
      "label": "Que la IA lo genere (auto-generar con pm-toolkit)",
      "value": "ai_generate",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-pressrelease --tone-mode {tone_option} --input-file output/pm/requirements-brief.md"
    },
    {
      "label": "Crear manualmente (la IA solo asiste en la revision)",
      "value": "manual",
      "next_action": "continue"
    },
    {
      "label": "Quiero ver el borrador de la IA y luego ajustar",
      "value": "hybrid",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-pressrelease-draft --tone-mode {tone_option} --input-file output/pm/requirements-brief.md"
    }
  ]
}
```

**Pasos para la creación manual:**

1. Abrir el editor: `output/pm/prd-draft.md`
2. Pegar la plantilla anterior
3. Consultar el requirements-brief y completar cada sección
4. Antes de enviar para revisión interna, verificar que los "beneficios para el cliente" esten claramente indicados

**Lista de verificación de calidad del comunicado de prensa:**
- [ ] El titular expresa "que cambia" de un vistazo
- [ ] La sección de problemas describe los puntos de dolor del cliente de manera realista
- [ ] La sección de solución se enfoca en "Que/Por que" en lugar de "Como"
- [ ] Los testimonios de clientes expresan específicamente el valor de negocio
- [ ] La jerga técnica esta minimizada, usando palabras que cualquiera pueda entender

---

## 🚀 Step 3: Agregar FAQ e historias de usuario

Una vez completado el comunicado de prensa, agregue **FAQ (Preguntas frecuentes)** e **Historias de usuario** para hacer el PRD más detallado.

### 3-1: Creación de FAQ (Preguntas frecuentes)

```json
{
  "type": "AskQuestion",
  "question": "Seleccione que perspectivas cubrir en las FAQ",
  "description": "Las FAQ requieren dos tipos de preguntas: (1) preguntas de usuarios finales, y (2) preguntas de partes interesadas (ejecutivos e ingenieros). Cual desea priorizar?",
  "options": [
    {
      "label": "FAQ para usuarios (uso, funciones, soporte)",
      "value": "user_faq",
      "next_action": "continue"
    },
    {
      "label": "FAQ para partes interesadas (valor de negocio, tecnologia, escalabilidad)",
      "value": "stakeholder_faq",
      "next_action": "continue"
    },
    {
      "label": "Historias de usuario (escenarios de uso especificos)",
      "value": "user_stories",
      "next_action": "continue"
    },
    {
      "label": "Todo (FAQ de usuario + FAQ de partes interesadas + Historias de usuario)",
      "value": "all",
      "next_action": "continue"
    }
  ]
}
```

**Ejemplo de FAQ para usuarios:**

```markdown
## FAQ - Para usuarios

### Q1: Cuantas tareas puede gestionar TaskFlow?
A: TaskFlow admite la gestion simultanea de miles de tareas. ...

### Q2: Puedo migrar desde herramientas existentes (Notion, Asana, etc.)?
A: Si, puede migrar en bloque utilizando la funcion de importacion CSV/JSON. ...

### Q3: Hay una aplicacion movil?
A: La version MVP proporciona una aplicacion web. La aplicacion movil esta planeada para la v2. ...

### Q4: Puedo usarlo sin conexion?
A: Si, las funciones basicas estan disponibles en modo sin conexion. ...

### Q5: Que tan detallada puede ser la configuracion de permisos del equipo?
A: Proporcionamos tres niveles de permisos: Propietario, Miembro y Visor. ...
```

**Ejemplo de FAQ para partes interesadas:**

```markdown
## FAQ - Para partes interesadas

### Q1: Que tan grande es el mercado objetivo de TaskFlow?
A: El mercado global de gestion de proyectos es de XX mil millones de dolares anuales, con una tasa de crecimiento del Y%. ...

### Q2: Que diferencia a TaskFlow de la competencia (Jira, Monday.com, etc.)?
A: TaskFlow se especializa en "simplicidad" y "colaboracion en equipo." ...

### Q3: Cual es el modelo de ingresos?
A: Adoptamos un modelo de suscripcion SaaS (freemium + planes de pago). ...

### Q4: Es adecuada la escalabilidad tecnica?
A: Con arquitectura nativa en la nube, anticipamos escalar a millones de usuarios. ...

### Q5: Que hay de la seguridad y el cumplimiento?
A: Hemos obtenido la certificacion SOC 2 Type II y cumplimos con GDPR/leyes de proteccion de datos. ...
```

### 3-2: Definición de historias de usuario

```json
{
  "type": "AskQuestion",
  "question": "Como desea priorizar las historias de usuario?",
  "description": "Las historias de usuario se clasifican en Must/Should/Could por prioridad de implementacion. Cuantas historias desea escribir para cada nivel?",
  "options": [
    {
      "label": "Enfocarse solo en Must (esencial MVP): 3-5 historias",
      "value": "must_only",
      "next_action": "continue"
    },
    {
      "label": "Must + Should: 8-10 en total",
      "value": "must_should",
      "next_action": "continue"
    },
    {
      "label": "Conjunto completo (Must/Should/Could): 15+",
      "value": "full_set",
      "next_action": "continue"
    },
    {
      "label": "Dejar que la IA genere automaticamente",
      "value": "ai_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-user-stories --input-file output/pm/requirements-brief.md --count 10"
    }
  ]
}
```

**Plantilla de historias de usuario:**

```text
As a [rol], I want [funcion/accion], so that [valor de negocio/beneficio]

Ejemplo 1) As a busy project manager, I want to set recurring tasks, so that I don't have to manually recreate them every week.

Ejemplo 2) As a team lead, I want to see real-time progress on all projects, so that I can identify blockers immediately.

Ejemplo 3) As a new user, I want a guided onboarding tutorial, so that I can set up my first project in under 5 minutes.
```

**Prioridad MoSCoW:**

```text
## Historias de usuario (priorizadas)

### MUST (Esencial MVP)
- [ ] US-1: As a user, I want to create tasks with title and description
- [ ] US-2: As a team lead, I want to assign tasks to team members
- [ ] US-3: As a user, I want to mark tasks as complete/incomplete

### SHOULD (Deseable para implementar en v1)
- [ ] US-4: As a user, I want to set due dates and reminders
- [ ] US-5: As a user, I want to organize tasks into projects/folders

### COULD (Implementacion en versiones futuras)
- [ ] US-6: As a user, I want to integrate with Slack notifications
- [ ] US-7: As a user, I want to generate reports on productivity metrics
```

---

## 🚀 Step 4: Definición de alcance y métricas de éxito

Finalmente, aclare **que hacer y que no hacer**, y defina **como medir el éxito**.

### 4-1: In Scope (MVP) vs Out of Scope (Versiones futuras)

```json
{
  "type": "AskQuestion",
  "question": "Como desea proceder con la definicion del alcance?",
  "description": "Decidir que incluir y excluir impacta significativamente el esfuerzo de desarrollo y el cronograma. Elija entre los metodos a continuacion.",
  "options": [
    {
      "label": "Dejar que la IA sugiera (extraccion automatica del requirements-brief)",
      "value": "ai_suggest",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-scope-definition --input-file output/pm/requirements-brief.md"
    },
    {
      "label": "Decidir manualmente (entrada manual usando plantilla)",
      "value": "manual",
      "next_action": "continue"
    },
    {
      "label": "Hibrido (revisar y ajustar las sugerencias de la IA)",
      "value": "hybrid",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-scope-definition-draft --input-file output/pm/requirements-brief.md"
    }
  ]
}
```

**Plantilla de definición de alcance:**

```text
## In Scope (MVP v1.0)

### Core Features
- Task creation, editing, deletion
- Task assignment to team members
- Due date and priority setting
- Project/folder organization
- Basic filtering and search
- Team collaboration (comments on tasks)
- Email notifications

### Technical
- Web application (responsive design for desktop, tablet)
- SQLite/PostgreSQL database
- REST API for future mobile app
- Basic authentication

## Out of Scope (v2+)

### Future Features
- Mobile native apps (iOS/Android)
- Advanced reporting and analytics
- Integration with Slack/Teams
- Time tracking and estimation
- Resource allocation algorithms
- Advanced permission management

### Not Planned
- Desktop client (will use web)
- Complex workflow automation
- AI-powered task recommendations (future AI phase)
```

### 4-2: Definición de métricas de éxito (Success Metrics / KPIs)

```json
{
  "type": "AskQuestion",
  "question": "Que marco desea utilizar para definir las metricas de exito (KPI)?",
  "description": "Las metricas de exito del producto son indicadores medibles directamente vinculados a los objetivos de negocio. Generalmente se utiliza el marco AARRR (Acquisition, Activation, Retention, Revenue, Referral).",
  "options": [
    {
      "label": "Definir usando AARRR (Pirate Metrics)",
      "value": "aarrr",
      "next_action": "continue"
    },
    {
      "label": "Definir usando OKR (Objectives & Key Results)",
      "value": "okr",
      "next_action": "continue"
    },
    {
      "label": "Definir usando KPI generales de SaaS",
      "value": "saas_kpi",
      "next_action": "continue"
    },
    {
      "label": "Dejar que la IA genere todo",
      "value": "ai_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-success-metrics --input-file output/pm/requirements-brief.md --framework aarrr"
    }
  ]
}
```

**Ejemplos de definición de KPI usando el marco AARRR:**

```text
## Success Metrics (KPIs)

### Acquisition (Adquisicion)
- Monthly signup rate: Objetivo 500 usuarios/mes (al final de v1)
- Organic traffic rate: Objetivo 30% (vs marketing pago)
- Sign-up conversion rate: Objetivo 3% (desde landing page)

### Activation (Activacion)
- First project creation rate: Objetivo 70% (dentro de 7 dias del registro)
- First task creation rate: Objetivo 85% (dentro de 24 horas)
- Tutorial completion rate: Objetivo 60%

### Retention (Retencion)
- Monthly active users (MAU): Objetivo 80% de registros
- Weekly active users (WAU): Objetivo 50% de registros
- Churn rate: Objetivo < 5% por mes (para usuarios de pago)

### Revenue (Ingresos)
- Conversion to paid: Objetivo 10% de usuarios gratuitos
- Average revenue per account (ARPA): Objetivo $50/mes
- Customer lifetime value (LTV): Objetivo $2,400

### Referral (Referencia)
- Viral coefficient: Objetivo 1.2 (cada usuario trae 1.2 nuevos usuarios)
- Referral signup rate: Objetivo 15% de nuevos usuarios
```

---

## 🚀 Step 5: Finalización y salida del PRD

Finalmente, integre todas las secciones y genere el PRD final (`prd.md`).

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el metodo para generar el PRD (prd.md)",
  "description": "Integre todas las secciones anteriores (comunicado de prensa, FAQ, historias de usuario, alcance, KPI) para generar el PRD final.",
  "options": [
    {
      "label": "Que la IA integre y genere todo (auto-generar con pm-toolkit)",
      "value": "full_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-full-prd --input-files output/pm/requirements-brief.md,output/pm/prd-draft.md --output output/pm/prd.md"
    },
    {
      "label": "Ensamblar manualmente cada seccion",
      "value": "manual_assembly",
      "next_action": "continue"
    },
    {
      "label": "Revisar el borrador de la IA y luego finalizar",
      "value": "review_then_finalize",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-draft --input-files output/pm/requirements-brief.md,output/pm/prd-draft.md"
    }
  ]
}
```

**Estructura final del PRD:**

```text
# Product Requirements Document (PRD)
## TaskFlow v1.0

---

## Executive Summary
[Resumen condensado del comunicado de prensa]

---

## Press Release
[Texto completo del comunicado de prensa creado en el Paso 2]

---

## FAQ

### FAQ para usuarios
[FAQ de usuarios creado en el Paso 3]

### FAQ para partes interesadas
[FAQ de partes interesadas creado en el Paso 3]

---

## User Stories

### MUST (MVP v1.0)
[Historias de usuario priorizadas]

### SHOULD (Version futura)
[...]

### COULD (Futuro adicional)
[...]

---

## Scope Definition

### In Scope (MVP v1.0)
- Core Features
- Technical Requirements
- Design Scope

### Out of Scope (v2+)
- Future Features
- Not Planned

---

## Success Metrics (KPIs)

### AARRR Framework
- Acquisition: ...
- Activation: ...
- Retention: ...
- Revenue: ...
- Referral: ...

---

## Dependencies & Risks

### Dependencies
- Integracion con sistemas existentes
- Disponibilidad de servicios externos

### Risk & Mitigation
- Factores de riesgo y estrategias de mitigacion

---

## Timeline & Milestones
- Kick-off: ...
- Soft launch: ...
- GA: ...
```

### Verificar archivos de salida

```json
{
  "type": "AskQuestion",
  "question": "Desea revisar el PRD generado?",
  "description": "Verifique que prd.md se haya generado correctamente.",
  "options": [
    {
      "label": "Mostrar contenido del archivo (verificacion)",
      "value": "view",
      "next_action": "bash",
      "command": "cat output/pm/prd.md | head -100"
    },
    {
      "label": "Verificar tamano del archivo y fecha de creacion",
      "value": "check_meta",
      "next_action": "bash",
      "command": "ls -lh output/pm/prd.md && wc -l output/pm/prd.md"
    },
    {
      "label": "Revisar la ultima seccion (KPI)",
      "value": "view_end",
      "next_action": "bash",
      "command": "tail -50 output/pm/prd.md"
    }
  ]
}
```

---

## ⚠️ Problemas comunes y soluciones

### Problema 1: No se le ocurre un titular para el comunicado de prensa

**Sintoma:** Reescribir el titular muchas veces, o solo contiene la palabra "TaskFlow"

**Causa:** El titular debe transmitir "beneficios para el cliente" en lugar del "nombre del producto"

**Solución:**

```json
{
  "type": "AskQuestion",
  "question": "Tiene dificultades para crear el titular?",
  "options": [
    {
      "label": "Si, me gustaria una plantilla",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "No, estoy bien",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**Plantilla:**

```text
Patron 1) Resolver el [problema] del [objetivo] con [solucion]
  Ejemplo: "Reducir la carga de gestion de tareas para lideres de equipo ocupados con visualizacion en tiempo real"

Patron 2) [Nombre del producto] que logra [resultado de negocio]
  Ejemplo: "TaskFlow - Reduzca el tiempo de finalizacion de proyectos en un 30%"

Patron 3) Un [nuevo enfoque] que es [beneficio cualitativo]
  Ejemplo: "Simple pero poderoso. TaskFlow transforma la gestion de tareas"

Puntos clave:
- Evitar jerga (terminos burocraticos como "visualizacion" u "optimizacion" no son recomendables)
- Enfocarse en el "Por que" (no "que funciones" sino "que impacto")
```

---

### Problema 2: El alcance es demasiado amplio y la definición de MVP es vaga

**Sintoma:** Más de 20 funciones listadas en In Scope, o todo esta etiquetado como "todo es MVP"

**Causa:** No se puede distinguir entre "seria bueno tener" y "imprescindible"

**Solución:**

```json
{
  "type": "AskQuestion",
  "question": "Siente que el alcance es demasiado amplio?",
  "options": [
    {
      "label": "Si, quiero reducir el alcance",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "No, estoy bien",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**Como definir MVP:**

```text
**MVP = Un conjunto de alcance minimo que resuelve completamente un punto de dolor**

Ejemplo de MVP de TaskFlow:
  ✓ Incluir en MVP: Crear/editar/eliminar tareas + asignacion de equipo + configuracion de plazos
  ✗ Excluir del MVP: Estadisticas/analisis, integracion con Slack, seguimiento de tiempo, permisos avanzados

Criterios de decision:
- "Puede el usuario percibir valor sin esto?" → Si ⇒ Esencial para MVP
- "Se puede manejar con un hack/solucion alternativa?" → Si ⇒ OK para v2+
- "Porque la competencia lo hace" → Eso solo no es una razon valida ✗
```

---

### Problema 3: No sabe como configurar los KPIs

**Sintoma:** El KPI es solo "aumentar el número de usuarios" o no tiene base numérica

**Causa:** La relación entre el modelo de negocio y las métricas de medición no esta clara

**Solución:**

```json
{
  "type": "AskQuestion",
  "question": "Tiene dificultades para establecer los KPI?",
  "options": [
    {
      "label": "Si, enseneme el marco",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "No, estoy bien",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**Ejemplo de implementación del marco AARRR:**

```text
### Acquisition (Como adquirir usuarios)
- Ejemplos de KPI: Monthly signup rate, Cost per acquisition (CPA), Sign-up conversion rate
- Ejemplo de TaskFlow: Lanzamiento en Product Hunt ⇒ Objetivo 1000 registros

### Activation (Tiempo hasta que el usuario percibe valor)
- Ejemplos de KPI: % usuarios que completan onboarding, Time to first action, Feature adoption rate
- Ejemplo de TaskFlow: 70%+ de usuarios crean su primer proyecto dentro de 7 dias

### Retention (Retencion)
- Ejemplos de KPI: Monthly/Weekly active users (MAU/WAU), Churn rate, Engagement score
- Ejemplo de TaskFlow: 80%+ de usuarios activos mensuales

### Revenue (Monetizacion)
- Ejemplos de KPI: ARPU (Average Revenue Per User), Conversion to paid, LTV (Life Time Value)
- Ejemplo de TaskFlow: Freemium ⇒ 10%+ tasa de conversion a plan de pago ⇒ LTV $2400

### Referral (Crecimiento viral)
- Ejemplos de KPI: Viral coefficient, Referral rate, NPS (Net Promoter Score)
- Ejemplo de TaskFlow: Cada usuario invita un promedio de 0.5 nuevos usuarios
```

---

### Problema 4: No se encuentra requirements-brief.md

**Sintoma:** Error "File not found" o el directorio `/output/pm/` no existe

**Causa:** La Lección 18-2 no se completo, o el archivo se guardo en una ubicación diferente

**Solución:**

```json
{
  "type": "AskQuestion",
  "question": "No puede encontrar requirements-brief.md?",
  "options": [
    {
      "label": "No encontrado. Quiero rehacer la Leccion 18-2",
      "value": "redo_lesson",
      "next_action": "view_html",
      "url": "../../start-18-2"
    },
    {
      "label": "Podria estar en otra ubicacion (busquelo)",
      "value": "search",
      "next_action": "bash",
      "command": "find . -name 'requirements-brief*' -o -name '*brief*' 2>/dev/null"
    },
    {
      "label": "Quiero crear uno nuevo (Me gustaria una plantilla)",
      "value": "create_new",
      "next_action": "continue"
    }
  ]
}
```

---

## ✅ Punto de control

Después de completar esta sesión, verifique que todas las siguientes casillas esten marcadas:

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "label": "Comprendio el metodo Working Backwards",
      "required": true
    },
    {
      "label": "El PRD en formato de comunicado de prensa ha sido redactado",
      "required": true
    },
    {
      "label": "Las FAQ (para usuarios + partes interesadas) contienen 5+ elementos",
      "required": true
    },
    {
      "label": "3+ historias de usuario definidas (prioridad MUST)",
      "required": true
    },
    {
      "label": "El alcance (In Scope / Out of Scope) esta claramente definido",
      "required": true
    },
    {
      "label": "Las metricas de exito (KPI) estan configuradas usando el marco AARRR",
      "required": true
    },
    {
      "label": "El archivo `output/pm/prd.md` ha sido generado",
      "required": true
    },
    {
      "label": "prd.md tiene 300+ lineas (detalle suficiente)",
      "required": false,
      "hint": "Recomendado: aproximadamente 300-500 lineas"
    }
  ]
}
```

**Comandos de verificación finales:**

```bash
# Verificar si el archivo existe
ls -lh output/pm/prd.md

# Verificar el numero de lineas
wc -l output/pm/prd.md

# Vista previa del contenido
head -50 output/pm/prd.md
```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── prd.md  (Documento de requisitos del producto)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/prd.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/prd.md
```

> 💡 Texto completo: Ejecute `cat output/pm/prd.md` para mostrar el texto completo

---

## ➡️ Siguientes pasos

Lesson 18-3  esta completa, continue con la siguiente lección:

```json
{
  "type": "NextStep",
  "next_lesson": "start-18-4",
  "title": "18-4: Tres revisiones (Negocio / UX / Tecnologia)",
  "description": "Revise el PRD creado desde tres perspectivas (negocio, experiencia de usuario, viabilidad tecnica) y finalice la version definitiva.",
  "estimated_duration": "~25 min",
  "what_you_will_do": [
    "Verificar la consistencia logica del PRD (revision de negocio)",
    "Evaluar la viabilidad de la experiencia de usuario (revision UX)",
    "Verificar la viabilidad tecnica (revision tecnica)",
    "Integrar retroalimentacion para completar el PRD final",
    "Aprobacion y gestion de versiones del PRD"
  ],
  "button_label": "Continuar a 18-4",
  "button_action": "open_lesson",
  "button_target": "start-18-4"
}
```

---

## 📌 Materiales complementarios

### Referencia: Información oficial sobre Amazon Working Backwards

Para obtener más información sobre el método Working Backwards, consulte los siguientes recursos:

- **Libro:** "Working Backwards" de Colin Bryar & Bill Carr (escrito por VP de Producto de Amazon)
- **Guía oficial de Amazon:** "Customer Obsession," uno de los Principios de Liderazgo
- **Caso de estudio:** Ejemplo de desarrollo de Kindle (materiales de conferencia de prensa)

### Referencia: Marco PARD (Versión extendida)

Además de Working Backwards, los siguientes marcos de PRD también son útiles:

```text
## PARD Framework
- P (Purpose): Por que estamos construyendo esto
- A (Approach): Que enfoque resuelve esto
- R (Result): Resultados esperados
- D (Dependency): Dependencias y riesgos
```

### Reference: PRD Template Variations

Las plantillas de PRD varian según la industria y la etapa:

| Plantilla | Aplicación | Características |
|---------|------|------|
| **Lean PRD** | Startups en etapa inicial | 1-3 páginas, ágil |
| **Working Backwards** | Estilo Amazon | Centrado en comunicado de prensa |
| **Full PRD** | Grandes empresas/establecidas | Más de 100 páginas, detallado |
| **One-Pager** | Para ejecutivos | Resumido en 1 página |

**TaskFlow adopta Working Backwards (versión Lean).**

---

## 🎓 Cuestionario de repaso

Para repasar lo que aprendio en esta lección、aquí tiene un cuestionario breve：

```json
{
  "type": "AskQuestion",
  "question": "Cuales de las siguientes son caracteristicas del metodo Working Backwards? (Seleccion multiple permitida)",
  "options": [
    {
      "label": "Comienza desde la perspectiva del cliente",
      "value": "correct_1",
      "is_correct": true
    },
    {
      "label": "Escribir primero el comunicado de prensa",
      "value": "correct_2",
      "is_correct": true
    },
    {
      "label": "Comienza desde las especificaciones tecnicas",
      "value": "incorrect_1",
      "is_correct": false
    },
    {
      "label": "Pensar en como usarlo despues de completarlo",
      "value": "incorrect_2",
      "is_correct": false
    }
  ]
}
```

```json
{
  "type": "AskQuestion",
  "question": "Cual es la mejor definicion de MVP (Minimum Viable Product)?",
  "options": [
    {
      "label": "La primera version con la mayor cantidad de funciones posibles",
      "value": "wrong",
      "is_correct": false
    },
    {
      "label": "El conjunto minimo de funciones que puede entregar valor a los clientes",
      "value": "correct",
      "is_correct": true
    },
    {
      "label": "Una version que incluye todas las funciones planificadas",
      "value": "wrong2",
      "is_correct": false
    }
  ]
}
```

```json
{
  "type": "AskQuestion",
  "question": "Nombre las tres R del marco AARRR. (Pregunta abierta)",
  "hint": "Retention, Revenue, Referral",
  "expected_answer": "Retention (Retencion), Revenue (Ingresos), Referral (Referencia)"
}
```

---

**Felicidades! Lesson 18-3 (Creación de PRD) esta completa!**

A continuación, en la Lección 18-4, revisará el PRD creado desde multiples perspectivas y lo finalizara.
