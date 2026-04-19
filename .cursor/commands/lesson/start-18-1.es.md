---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: []
level: "intermediate"
tags: ["pm", "interview", "customer-needs"]
---

# 🎓 Lesson 18-1: Entrevista al cliente y recopilación de necesidades

## 📍 Lo que hará en esta sesión

**Lesson 18-1: Entrevista al cliente y recopilación de necesidades** — Bienvenido!

| Elemento | Detalles |
|------|------|
| Objetivo | La IA interpreta el rol de cliente para una simulación de entrevista. Defina personas y extraiga necesidades |
| Duración | ~25 min |
| Habilidades utilizadas | Habilidad pm-toolkit, flujo de diálogo interactivo con opciones |
| Requisitos previos | ai-agent-camp esta abierto |
| Página del material | [Module 18: PM y definición de requisitos del sistema](https://ai-agent.camp/es/course/module-18) como referencia paralela |

**Flujo de la sesión:**
1. Revisar la descripción general del proyecto TaskFlow
2. Simulación de entrevista al cliente con IA
3. Estructurar los resultados de la entrevista (personas, necesidades, puntos de dolor)
4. Generar y revisar customer-needs.md

Al final de esta sesión, el documento de análisis de necesidades del cliente de TaskFlow estará completado.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "continuar" o "seguir" para reanudar. Las respuestas pueden pausarse debido al procesamiento de herramientas, pero no es un error.

---

## 🎯 Verificación de preparación

Verifiquemos primero que la preparación esta en orden.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Confirmacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
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

## 🚀 Paso 1: Introducción al proyecto TaskFlow

Primero, revisemos la descripción general de "TaskFlow", que construiremos a lo largo de este módulo.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Descripcion general del proyecto TaskFlow",
  "questions": [{
    "id": "taskflow_intro",
    "prompt": "Conozcamos TaskFlow. Donde desea comenzar?",
    "options": [
      {"id": "overview", "label": "Cuenteme sobre TaskFlow"},
      {"id": "skip", "label": "Ya conozco la descripcion general, ir a la entrevista"},
      {"id": "context", "label": "Quiero conocer el flujo general de este modulo"}
    ]
  }]
}
```

**Que es TaskFlow:**
```text
TaskFlow es una aplicacion web de gestion de tareas para pequenas y medianas empresas.

[Concepto]
- Vea de un vistazo lo que cada miembro del equipo necesita hacer hoy
- La IA sugiere prioridades y evita que se pasen por alto tareas
- Simple, pero equipada con las funciones necesarias para empresas en crecimiento

[Usuarios objetivo]
- Empresas de 10 a 100 empleados
- Actualmente gestionan tareas con Excel/hojas de calculo
- Las herramientas existentes (Trello, Asana, etc.) son demasiado complejas para usar eficazmente

En este modulo, experimentara el ciclo de vida completo de TaskFlow:
Planificacion → Diseno → Implementacion → Pruebas → Operaciones
a lo largo de las 20 lecciones.
```

**Resultado esperado**: Comprenderá la descripción general de TaskFlow.

---

## 🚀 Paso 2: Preparación de la entrevista al cliente

La IA interpretara el rol de cliente para una simulación de entrevista. Primero, seleccione el objetivo de la entrevista.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Seleccionar objetivo de entrevista",
  "questions": [
    {
      "id": "persona_type",
      "prompt": "Seleccione el tipo de cliente a entrevistar (la IA interpretara el rol)",
      "options": [
        {"id": "pm", "label": "Gerente de proyecto (35 anos, empresa de TI)"},
        {"id": "sales_mgr", "label": "Director de ventas (42 anos, manufactura)"},
        {"id": "startup_ceo", "label": "CEO de startup (29 anos, empresa SaaS)"},
        {"id": "hr", "label": "Personal de RRHH (31 anos, consultora)"}
      ]
    },
    {
      "id": "interview_style",
      "prompt": "Seleccione el formato de entrevista",
      "options": [
        {"id": "structured", "label": "Entrevista estructurada (lista de preguntas preparada)"},
        {"id": "semi", "label": "Semiestructurada (temas definidos, discusion libre)"},
        {"id": "guided", "label": "Guiada (la IA sugiere preguntas)"}
      ]
    }
  ]
}
```

**Después de la selección**: La simulación comenzará con la persona y el formato de entrevista elegidos.

---

## 🚀 Paso 3: Ejecución de la simulación de entrevista

La IA respondera como el cliente seleccionado. Haga preguntas sobre los siguientes temas.

**Guía de entrevista:**
```text
Entreviste al cliente (IA) sobre los siguientes temas:

1. [Situacion actual] Cual es su metodo actual de gestion de tareas? Que herramientas utiliza?
2. [Desafios] Cual es su mayor problema? Puede compartir un episodio especifico?
3. [Estado ideal] Que le haria feliz? Cual es el estado ideal?
4. [Prioridades] Si pudiera nombrar las 3 cosas principales que desea mejorar?
5. [Restricciones] Cual es su rango de presupuesto, plazo de implementacion y requisitos indispensables?

La IA dara respuestas realistas como la persona seleccionada.
Realice entre 5 y 10 rondas de conversacion.
```

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Progreso de la entrevista",
  "questions": [{
    "id": "interview_status",
    "prompt": "Como va la entrevista?",
    "options": [
      {"id": "continue", "label": "Aun tengo preguntas, continuar"},
      {"id": "enough", "label": "He recopilado suficiente, pasar a organizar"},
      {"id": "help", "label": "No se que preguntar"},
      {"id": "restart", "label": "Comenzar de nuevo con otra persona"}
    ]
  }]
}
```

(continue → Continuar la entrevista)
(enough → Continuar al Paso 4)
(help → Mostrar preguntas de ejemplo)
(restart → Volver al Paso 2)

**Resultado esperado**: Se completaran entre 5 y 10 rondas de entrevista.

---

## 🚀 Paso 4: Estructuración de los resultados de la entrevista

Analice el contenido de la entrevista y compilelo en un documento.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Como organizar los resultados",
  "questions": [{
    "id": "output_format",
    "prompt": "Seleccione el formato de salida",
    "options": [
      {"id": "full", "label": "Analisis completo (Persona + Necesidades + Puntos de dolor + Oportunidades)"},
      {"id": "persona_focus", "label": "Enfocarse en la definicion de persona"},
      {"id": "needs_focus", "label": "Enfocarse en la lista de necesidades"},
      {"id": "auto", "label": "Dejar que la IA decida"}
    ]
  }]
}
```

**Documento a generar:**
```text
Genere output/pm/customer-needs.md con el siguiente contenido:

# Analisis de necesidades del cliente: TaskFlow

## 1. Resumen de la entrevista
- Objetivo: {Informacion de la persona}
- Fecha: {Fecha de hoy}
- Formato: {Formato seleccionado}

## 2. Definicion de persona
### Persona principal
- Nombre (alias):
- Edad:
- Cargo:
- Tamano de la empresa:
- Nivel de TI:
- Desafios actuales:

## 3. Necesidades descubiertas (por prioridad)
| # | Necesidad | Tipo | Prioridad | Evidencia (cita) |
|---|-----------|------|-----------|-----------------|

## 4. Puntos de dolor
1.
2.
3.

## 5. Oportunidades
-

## 6. Implicaciones para los proximos pasos
- Puntos a reflejar en el documento de requisitos
- Temas a explorar en profundidad en el PRD

mkdir -p output/pm && guardar el archivo en output/pm/customer-needs.md
```

**Resultado esperado**: Se generará `output/pm/customer-needs.md`.

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
      {"id": "trouble_1", "label": "El rol de cliente de la IA da respuestas poco naturales"},
      {"id": "trouble_2", "label": "No se que preguntar en la entrevista"},
      {"id": "trouble_3", "label": "No se como organizar las necesidades"},
      {"id": "trouble_4", "label": "El archivo de salida no se genera"}
    ]
  }]
}
```

### Problema 1: El rol de cliente de la IA es poco natural
**Solución**: Indique "Por favor responda de manera más realista, incluyendo episodios específicos". También puede agregar restricciones específicas como "El presupuesto es de hasta 10,000 yenes por mes".

### Problema 2: No se que preguntar
**Solución**: Siga la guía de entrevista del Paso 3 (5 temas). Hacer 2 preguntas por tema es suficiente.

### Problema 3: No se como organizar las necesidades
**Solución**: Indique a la IA "Basandose en el contenido de la entrevista, organice las necesidades por prioridad" y se organizaran automáticamente.

### Problema 4: El archivo de salida no se genera
**Solución**: Verifique si el directorio `output/pm/` existe. Si no, creelo con `mkdir -p output/pm`.

---

## ✅ Punto de control
- [ ] Comprendio la descripción general del proyecto TaskFlow
- [ ] Realizo 5 o más rondas de entrevista al cliente con IA
- [ ] Al menos 1 persona esta definida
- [ ] Al menos 3 necesidades estan extraidas
- [ ] Los puntos de dolor estan claramente identificados
- [ ] `output/pm/customer-needs.md` esta generado


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── stakeholder-map.md  (Mapa de partes interesadas)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/stakeholder-map.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/stakeholder-map.md
```

> 💡 Texto completo: Ejecute `cat output/pm/stakeholder-map.md` para mostrar el texto completo

---

## ✅ Verificación de finalización
Introduzca lo siguiente en el chat de Codex para verificar el estado de finalización:

```text
Verifique el contenido de output/pm/customer-needs.md y confirme que la definicion de persona,
la lista de necesidades y los puntos de dolor estan todos completados.
```

**Resultado esperado**: Se verificará la completitud del documento.

---

## ➡️ Siguientes pasos

La Lección 18-1 esta completa. A continuación, creará el documento de requisitos basado en los resultados de la entrevista.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione como proceder",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente leccion (Creacion de documento de requisitos)"},
      {"id": "next_window", "label": "Iniciar /start-18-2 en una nueva ventana"},
      {"id": "review", "label": "Revisar las necesidades del cliente nuevamente"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

- next_auto → Ejecutar /start-18-2
- next_window → Abrir /start-18-2 en una nueva ventana
- review → Volver a mostrar customer-needs.md
- finish → Finalizar
