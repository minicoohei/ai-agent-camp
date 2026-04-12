---
description: "When the user says /start-18-2 — Module 18 Lesson 18-2: PM - Creación del documento de requisitos"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-1", "output/pm/customer-needs.md"]
level: "intermediate"
tags: ["pm", "requirements", "moscow"]
---

# 🎓 Lesson 18-2: Creación del documento de requisitos

## 📍 Lo que hará en esta sesión

**Lesson 18-2: Creación del documento de requisitos** — Bienvenido!

| Elemento | Detalles |
|------|------|
| Objetivo | Organizar los requisitos funcionales/no funcionales de TaskFlow y crear un documento de requisitos (método MoSCoW) |
| Duración | ~25 min |
| Habilidades utilizadas | Habilidad pm-toolkit |
| Requisitos previos | Lección 18-1 completada, output/pm/customer-needs.md existe |
| Página del material | [Module 18: PM y definición de requisitos del sistema](https://ai-agent.camp/es/course/module-18) como referencia paralela |

**Flujo de la sesión:**
1. Cargar customer-needs.md y extraer requisitos
2. Listar requisitos funcionales (priorizar con método MoSCoW)
3. Definir requisitos no funcionales (rendimiento, seguridad, disponibilidad)
4. Generar requirements-brief.md

Al final de esta sesión, el documento de requisitos de TaskFlow estará completado.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "continuar" o "seguir" para reanudar. Las respuestas pueden pausarse debido al procesamiento de herramientas, pero no es un error.

---

## 🎯 Verificación de preparación

Ha terminado 18-1 y esta listo para crear el documento de requisitos? Verifiquémoslo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Confirmacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar si la Leccion 18-1 esta completada"},
      {"id": "view_html", "label": "Ver primero la pagina del material"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Continuar al Paso 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar la ruta de la página del material)
(different_lesson → Mostrar la lista de módulos)

---

## 🚀 Paso 1: Carga de necesidades del cliente

Preparemos la extracción de tipos de requisitos del customer-needs.md creado en la lección anterior.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Verificar necesidades del cliente",
  "questions": [{
    "id": "needs_status",
    "prompt": "Esta listo customer-needs.md?",
    "options": [
      {"id": "ready", "label": "El archivo existe, continuar"},
      {"id": "missing", "label": "El archivo no existe"},
      {"id": "show_me", "label": "Quiero ver el contenido del archivo"}
    ]
  }]
}
```

(ready → Continuar al Paso 2)
(missing → Redirigir a la Lección 18-1)
(show_me → Mostrar el contenido del archivo)

**Resultado esperado**: customer-needs.md esta verificado y su contenido esta organizado.

---

## 🚀 Paso 2: Lista de requisitos funcionales

Basandose en las necesidades de customer-needs.md, liste los requisitos funcionales de TaskFlow y prioricelos usando el método MoSCoW.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Seleccionar categoria de requisitos funcionales",
  "questions": [{
    "id": "functional_category",
    "prompt": "Seleccione una categoria de requisitos funcionales para explorar en detalle",
    "options": [
      {"id": "task_basics", "label": "Funciones basicas de gestion de tareas"},
      {"id": "team_collab", "label": "Colaboracion en equipo"},
      {"id": "analytics", "label": "Analisis e informes"},
      {"id": "notification", "label": "Notificaciones y alertas"},
      {"id": "all_categories", "label": "Organizar todas las categorias a la vez (dejar a la IA)"}
    ]
  }]
}
```

**Ejemplo de requisitos funcionales por categoría (sugeridos por la IA):**

```text
[Gestion basica de tareas]
- Crear, editar y eliminar tareas
- Establecer prioridad de tareas
- Establecer plazos y recordatorios
- Gestion de estados (No iniciado → En progreso → Completado)
- Busqueda y filtros de tareas

[Colaboracion en equipo]
- Asignacion de tareas
- Comentarios y discusiones entre miembros del equipo
- Funcion de adjuntar archivos
- Cambiar/delegar responsables
- Gestion de permisos del equipo

[Analisis e informes]
- Panel de progreso del proyecto
- Analisis de productividad individual/por equipo
- Visualizacion de tareas vencidas
- Generacion de informes semanales/mensuales

[Notificaciones y alertas]
- Notificaciones previas al plazo
- Notificaciones de asignacion de tareas
- Notificaciones de comentarios
- Integracion con Email/Slack
```

**Ejemplo de configuración de AskQuestion (clasificación MoSCoW):**
```json
{
  "title": "🚀 Paso 2-2: Clasificar funciones con el metodo MoSCoW",
  "questions": [{
    "id": "moscow_classification",
    "prompt": "Clasifique las funciones extraidas en las siguientes categorias",
    "options": [
      {"id": "must_have", "label": "Must Have (esencial): Requerido para MVP"},
      {"id": "should_have", "label": "Should Have (importante): Necesario en 1-2 meses"},
      {"id": "could_have", "label": "Could Have (deseable): Considerar para el futuro"},
      {"id": "wont_have", "label": "Won't Have (no necesario): No implementar esta vez"},
      {"id": "auto_classify", "label": "Dejar que la IA clasifique automaticamente"}
    ]
  }]
}
```

**Directrices de clasificación MoSCoW:**
```text
Criterios Must Have:
  ✓ Funcion utilizada por el 80% de los usuarios
  ✓ Multiples clientes mencionaron "no podemos trabajar sin esto"
  ✓ Funcion estandar de competidores
  → Ejemplo: Creacion de tareas, prioridad, establecimiento de plazos

Criterios Should Have:
  ✓ Funcion utilizada por el 50%+ de los usuarios
  ✓ Comentarios de "seria bueno tenerlo"
  ✓ Se puede implementar en la siguiente fase despues del MVP
  → Ejemplo: Panel de productividad, integracion con Slack

Criterios Could Have:
  ✓ Caso de uso especifico
  ✓ Alto costo de implementacion
  ✓ Se puede agregar despues
  → Ejemplo: Sugerencias de prioridad por IA, analisis avanzado

Criterios Won't Have:
  ✓ Fuera del alcance
  ✓ Dificil de operar
  ✓ Demanda poco clara
  → Ejemplo: App movil nativa (solo web), personalizacion avanzada
```

**Resultado esperado**: Los requisitos funcionales estan clasificados de Must Have a Won't Have.

---

## 🚀 Paso 3: Definición de requisitos no funcionales

Defina requisitos más alla de las funciones, como calidad, rendimiento y seguridad.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Seleccionar aspecto de requisito no funcional",
  "questions": [{
    "id": "nonfunctional_aspect",
    "prompt": "Seleccione un aspecto de requisito no funcional para definir valores objetivo especificos",
    "options": [
      {"id": "performance", "label": "Requisitos de rendimiento (tiempo de respuesta, velocidad de procesamiento)"},
      {"id": "security", "label": "Requisitos de seguridad"},
      {"id": "availability", "label": "Requisitos de disponibilidad (tiempo de actividad, redundancia)"},
      {"id": "usability", "label": "Requisitos de usabilidad"},
      {"id": "all_aspects", "label": "Todos los aspectos a la vez (dejar a la IA)"}
    ]
  }]
}
```

**Ejemplos específicos por aspecto:**

```text
[Requisitos de rendimiento]
- Tiempo de carga de pagina: < 3 segundos
- Tiempo de respuesta de API: < 500ms
- Usuarios concurrentes: 1,000
- Consulta de base de datos: < 1 segundo

[Requisitos de seguridad]
- Comunicacion cifrada con SSL/TLS
- Autenticacion: Email + contrasena (autenticacion de dos factores opcional)
- Gestion de permisos: Basada en roles (Admin, Manager, Member)
- Politica de contrasenas: Minimo 8 caracteres, incluyendo mayusculas y numeros
- Registro de auditoria: Registrar todas las operaciones

[Requisitos de disponibilidad]
- Tiempo de actividad del servicio: 99.5% o superior
- Mantenimiento mensual: Maximo 4 horas (una vez al mes)
- Respaldo: Respaldo automatico diario
- Recuperacion ante desastres: RPO = 1 dia, RTO = 4 horas

[Requisitos de usabilidad]
- Navegadores compatibles: Ultimas versiones de Chrome, Firefox, Safari
- Responsivo: Compatible con moviles y tabletas
- Accesibilidad: Cumplimiento WCAG 2.1 AA
- Idiomas soportados: Japones (ingles en el futuro)
- Ayuda y tutoriales: Guia completa para nuevos usuarios
```

**Ejemplo de configuración de AskQuestion (establecer objetivos numéricos):**
```json
{
  "title": "🚀 Paso 3-2: Objetivos de requisitos no funcionales",
  "questions": [
    {
      "id": "perf_targets",
      "prompt": "Seleccione o ingrese objetivos de rendimiento",
      "options": [
        {"id": "fast", "label": "Rapido (carga de pagina <2s, API <300ms)"},
        {"id": "normal", "label": "Estandar (carga de pagina <3s, API <500ms)"},
        {"id": "custom", "label": "Entrada personalizada"}
      ]
    },
    {
      "id": "security_level",
      "prompt": "Seleccione el nivel de seguridad",
      "options": [
        {"id": "standard", "label": "Estandar (autenticacion por contrasena, HTTPS)"},
        {"id": "high", "label": "Alto (autenticacion de dos factores, registros de auditoria)"},
        {"id": "custom", "label": "Personalizado"}
      ]
    }
  ]
}
```

**Resultado esperado**: Se establecen los objetivos numéricos para cada requisito no funcional.

---

## 🚀 Paso 4: Generación de requirements-brief.md

Documente los requisitos funcionales y no funcionales organizados en los Pasos 2 y 3.

**Documento a generar:**
```text
Genere output/pm/requirements-brief.md con el siguiente contenido:

# Documento de requisitos de TaskFlow

## 1. Informacion del documento
- Nombre del proyecto: TaskFlow
- Version: 1.0
- Fecha de creacion: {Fecha de hoy}
- Version objetivo: MVP (Producto Minimo Viable)

## 2. Descripcion general
TaskFlow es una aplicacion web de gestion de tareas para pequenas y medianas empresas de 10 a 100 empleados.
Permite ver de un vistazo lo que cada miembro del equipo necesita hacer hoy, con IA que sugiere prioridades para evitar que se pasen por alto tareas.

## 3. Requisitos funcionales (Clasificacion MoSCoW)

### 3.1 Must Have (Esencial para MVP)
| # | Funcion | Descripcion | Prioridad |
|---|---------|-------------|-----------|
| 1 | Creacion de tareas | Crear tareas con texto y plazos | P0 |
| 2 | Vista de lista de tareas | Listar tareas propias y del equipo | P0 |
| ... | ... | ... | ... |

### 3.2 Should Have (Implementacion en Fase 2)
| # | Funcion | Descripcion | Prioridad |
|---|---------|-------------|-----------|
| 1 | Gestion por proyecto | Soporte para multiples proyectos | P1 |
| ... | ... | ... | ... |

### 3.3 Could Have (En consideracion)
| # | Funcion | Descripcion |
|---|---------|-------------|
| 1 | Sugerencias de prioridad por IA | Determinar automaticamente la prioridad a partir de lenguaje natural |
| ... | ... | ... |

### 3.4 Won't Have (Fuera del alcance)
- App movil nativa (a considerar en el futuro)
- Funciones de personalizacion avanzada (dificiles de operar)

## 4. Requisitos no funcionales

### 4.1 Requisitos de rendimiento
- Tiempo de carga de pagina: < 3 segundos
- Tiempo de respuesta de API: < 500ms
- Usuarios concurrentes: Maximo 1,000

### 4.2 Requisitos de seguridad
- Autenticacion: Email + contrasena (version inicial)
- Comunicacion: Cifrada con TLS 1.2 o superior
- Gestion de permisos: Basada en roles (Admin, Manager, Member)
- Registro de auditoria: Registrar y retener todas las operaciones

### 4.3 Disponibilidad y fiabilidad
- Tiempo de actividad del servicio: 99.5% o superior (tiempo de inactividad mensual < 3.6 horas)
- Respaldo: Respaldo automatico diario (retencion de 30 dias)
- Recuperacion ante desastres: RTO 4 horas, RPO 1 dia

### 4.4 Usabilidad
- Navegadores compatibles: Ultimas versiones de Chrome, Firefox, Safari
- Diseno responsivo: Compatible con moviles y tabletas
- Idiomas soportados: Japones
- Ayuda: Tutoriales + FAQ completos

## 5. Restricciones
- Periodo de desarrollo: 8 semanas (MVP)
- Tamano del equipo: 3 ingenieros, 1 PM, 1 disenador
- Presupuesto: {Rango de presupuesto de la entrevista al cliente}
- Stack tecnologico: Frontend (React), Backend (Node.js + PostgreSQL)

## 6. Supuestos y riesgos

### Supuestos
- El cliente puede proporcionar retroalimentacion regular
- Las guias de diseno y marca estan preparadas de antemano

### Riesgos
1. Cambios frecuentes en las especificaciones de API → Mitigar con revisiones de diseno semanales
2. Escalabilidad → Realizar pruebas de carga (Fase 2)

## 7. Proximos pasos
- Leccion 18-3: Crear PRD (Documento de requisitos del producto)

mkdir -p output/pm && guardar el archivo en output/pm/requirements-brief.md
```

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Confirmar contenido generado",
  "questions": [{
    "id": "doc_generation",
    "prompt": "Listo para generar requirements-brief.md?",
    "options": [
      {"id": "generate", "label": "Generar"},
      {"id": "review", "label": "Revisar el contenido antes de generar"},
      {"id": "custom", "label": "Personalizar y generar"}
    ]
  }]
}
```

(generate → Generar el documento)
(review → Vista previa del contenido)
(custom → Mostrar opciones de personalización)

**Resultado esperado**: Se generará `output/pm/requirements-brief.md`.

---

## ⚠️ Problemas comunes y soluciones

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No puedo determinar la prioridad en la clasificacion MoSCoW"},
      {"id": "trouble_2", "label": "No conozco los objetivos numericos para requisitos no funcionales"},
      {"id": "trouble_3", "label": "Falta customer-needs.md"},
      {"id": "trouble_4", "label": "El archivo de salida no se genera"}
    ]
  }]
}
```

### Problema 1: No puedo determinar la prioridad en la clasificación MoSCoW
**Solución**: Hagase las siguientes preguntas:
- "Es una función utilizada por el 80% de los usuarios?" → Si es si, es Must Have
- "Multiples clientes mencionaron 'no podemos trabajar sin esto'?" → Si es si, es Must Have
- "Es una función estándar de los competidores (Trello, Asana)?" → Si es si, es Should Have
- "Es necesario en 1-2 meses?" → Si es si, es Should Have
- "Es una función para probar y ver la respuesta?" → Si es si, es Could Have
- "Esta fuera del alcance esta vez?" → Si es si, es Won't Have

### Problema 2: No conozco los objetivos numéricos para requisitos no funcionales
**Solución**: Consulte los valores estándar de la industria:

| Elemento | Estándar | Rápido |
|----------|----------|--------|
| Tiempo de carga de página | < 3s | < 2s |
| Respuesta de API | < 500ms | < 300ms |
| Tiempo de actividad del sitio | 99.5% | 99.99% |
| Frecuencia de respaldo | Diario | Por hora |

Si no esta seguro, elija "Estándar" y mejore después de iniciar operaciones.

### Problema 3: Falta customer-needs.md
**Solución**: Comience desde la Lección 18-1. Alternativamente, cree una versión simplificada:
```markdown
# Analisis de necesidades del cliente (simplificado)

## Persona
- Nombre: Taro (alias)
- Cargo: Gerente de proyecto
- Desafio: La gestion de tareas con Excel es complicada

## Necesidades
1. Ver las tareas de todos los miembros del equipo
2. Alerta automatica cuando los plazos estan vencidos
3. Quiero integracion con Slack para notificaciones
```

### Problema 4: El archivo de salida no se genera
**Solución**: Verifique si el directorio `output/pm/` existe:
```bash
mkdir -p output/pm
# Luego vuelva a ejecutar la generacion del documento
```

---

## ✅ Punto de control
- [ ] La Lección 18-1 esta completada
- [ ] customer-needs.md esta cargado
- [ ] Los requisitos funcionales estan clasificados de Must Have a Won't Have
- [ ] Must Have esta reducido a 5-10 elementos (verificar que no sean demasiados)
- [ ] Los requisitos no funcionales tienen objetivos numéricos específicos
- [ ] output/pm/requirements-brief.md esta generado
- [ ] El contenido del documento es preciso (sin errores tipograficos ni contradicciones)


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── customer-needs.md  (Analisis de necesidades del cliente)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/customer-needs.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/customer-needs.md
```

> 💡 Texto completo: Ejecute `cat output/pm/customer-needs.md` para mostrar el texto completo

---

## ✅ Verificación de finalización
Introduzca lo siguiente en el chat de Codex para verificar el estado de finalización:

```text
Verifique el contenido de output/pm/requirements-brief.md:

1. Los requisitos funcionales estan clasificados en Must Have / Should Have / Could Have / Won't Have?
2. Hay al menos una funcion definida en cada categoria?
3. Los requisitos no funcionales (rendimiento, seguridad, disponibilidad) tienen valores numericos especificos?
4. Las restricciones y supuestos estan claramente indicados?

Despues de la verificacion, responda "Listo".
```

**Resultado esperado**: Se verificará la completitud del documento.

---

## ➡️ Siguientes pasos

La Lección 18-2 esta completa. A continuación, creará el PRD (Documento de requisitos del producto) basado en el documento de requisitos.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione como proceder",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente leccion (Creacion de PRD)"},
      {"id": "next_window", "label": "Iniciar /start-18-3 en una nueva ventana"},
      {"id": "review", "label": "Revisar el documento de requisitos nuevamente"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

- next_auto → Ejecutar /start-18-3
- next_window → Abrir /start-18-3 en una nueva ventana
- review → Volver a mostrar requirements-brief.md
- finish → Finalizar
