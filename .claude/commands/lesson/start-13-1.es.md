---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
duration: "~20 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["lp", "copywriting", "persona", "brief"]
---

# 🎓 Lección 13-1: Organización de la propuesta de valor (Entrevista y copywriting)

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 13-1: Organización de la propuesta de valor**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Realizar una entrevista con AskQuestion, organizar persona, ejes de propuesta y copy para construir la base de la creación de la Landing Page |
| Duración | ~20 min |
| Habilidades utilizadas | Flujo de diálogo interactivo con opciones, habilidad lp-designer |
| Requisitos previos | Lección 0-1 completada, ai-agent-camp abierto |
| Página del curso | Consulte [Módulo 13: Diseño de Landing Page/Sitio web](https://ai-agent.camp/es/course/module-13) en paralelo |

**Flujo de la sesión:**
1. Entrevista sobre tipo de Landing Page/sitio web e información del servicio
2. Definición del persona objetivo
3. Generación de beneficios y copy
4. Elaboración del plan de estructura de secciones

Al finalizar la sesión, el brief de propuesta de valor necesario para la creación de la Landing Page estará completó.

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

## 🚀 Paso 1: Entrevista sobre el tipo de proyecto

Primero, decidamos qué tipo de página crear. Usaremos AskQuestionTool para la entrevista.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: ¿Qué tipo de página creará?",
  "questions": [
    {
      "id": "project_type",
      "prompt": "Seleccione el tipo de página a crear",
      "options": [
        {"id": "lp", "label": "Landing Page - Enfocada en un solo CTA"},
        {"id": "hp", "label": "Página principal - Estructura de múltiples secciones"},
        {"id": "product", "label": "Página de producto - Centrada en características"},
        {"id": "event", "label": "Página de evento/campaña"}
      ]
    },
    {
      "id": "service_category",
      "prompt": "Seleccione la categoría de su servicio",
      "options": [
        {"id": "saas", "label": "SaaS / Servicio web"},
        {"id": "ec", "label": "Comercio electrónico / Venta de productos"},
        {"id": "consulting", "label": "Consultoría / Servicios profesionales"},
        {"id": "education", "label": "Educación / Escuela"},
        {"id": "event", "label": "Evento / Seminario"},
        {"id": "portfolio", "label": "Portafolio / Personal"},
        {"id": "other", "label": "Otro"}
      ]
    }
  ]
}
```

**Después de la selección**: Confirmar información específica del servicio mediante entrada de texto libre basada en las opciones del usuario.

Ingrese la siguiente información:
```text
Cuéntenos sobre la Landing Page/sitio web que va a crear:

1. Nombre del servicio (nombre oficial):
2. Resumen del servicio (1-2 oraciones):
3. El mensaje más importante a transmitir:
4. URL de sitio de referencia (si la tiene):
```

**Resultado esperado**: Se recopila la información básica del servicio.

---

## 🚀 Paso 2: Definición del persona objetivo

A continuación, clarifiquemos a quién va dirigida la página.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Persona objetivo",
  "questions": [
    {
      "id": "target_age",
      "prompt": "¿Cuál es el rango de edad principal del público objetivo?",
      "options": [
        {"id": "20s", "label": "20s"},
        {"id": "30s", "label": "30s"},
        {"id": "40s", "label": "40s"},
        {"id": "50plus", "label": "50 y más"},
        {"id": "all", "label": "Amplio rango de edad"}
      ]
    },
    {
      "id": "target_role",
      "prompt": "¿Cuál es el rol/posición principal del público objetivo?",
      "options": [
        {"id": "executive", "label": "Ejecutivo / Directivo"},
        {"id": "manager", "label": "Director / Gerente"},
        {"id": "marketer", "label": "Especialista en marketing / Comunicaciones"},
        {"id": "engineer", "label": "Ingeniero / Técnico"},
        {"id": "sales", "label": "Ventas"},
        {"id": "individual", "label": "Individuo / Consumidor general"},
        {"id": "other", "label": "Otro"}
      ]
    },
    {
      "id": "cta_goal",
      "prompt": "¿Cuál es el objetivo del CTA? (La acción que desea que realice el usuario)",
      "options": [
        {"id": "signup", "label": "Registro gratuito / Creación de cuenta"},
        {"id": "inquiry", "label": "Contacto / Consulta"},
        {"id": "download", "label": "Descarga de materiales"},
        {"id": "purchase", "label": "Compra / Suscripción"},
        {"id": "trial", "label": "Inicio de prueba gratuita"},
        {"id": "event", "label": "Registro al evento"}
      ]
    }
  ]
}
```

**Después de la selección**: Confirmar los desafíos (puntos de dolor) del persona.

Ingrese información adicional:
```text
Enumere 3 desafíos que enfrenta su público objetivo:

1. El mayor desafío:
2. Una frustración cotidiana:
3. Algo que quieren resolver pero han abandonado:
```

**Resultado esperado**: Se define un persona claro.

---

## 🚀 Paso 3: Generación de beneficios y copy

Generar el copy de propuesta de valor basado en los resultados de la entrevista.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Selección del tono de diseño",
  "questions": [{
    "id": "design_tone",
    "prompt": "Seleccione el tono de diseño",
    "options": [
      {"id": "professional", "label": "Profesional / Confiable"},
      {"id": "modern", "label": "Moderno / Elegante"},
      {"id": "playful", "label": "Divertido / Accesible"},
      {"id": "luxury", "label": "Lujoso / Sofisticado"},
      {"id": "minimal", "label": "Minimalista / Simple"},
      {"id": "tech", "label": "Tecnológico / Vanguardista"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección**:

La IA generará automáticamente lo siguiente:
```text
Basándose en los resultados de la entrevista de los Pasos 1-2, genere lo siguiente:

## 3 Beneficios
1. Beneficio principal (mayor valor)
2. Sub-beneficio 1 (eficiencia / ahorro de tiempo)
3. Sub-beneficio 2 (tranquilidad / soporte)

## Propuestas de copy
- Titular (H1): Copy impactante de máximo 15 caracteres
- Subtítulo: Explicación complementaria de máximo 30 caracteres
- Texto del CTA: Texto de acción de máximo 7 caracteres
- Complemento del CTA: Texto de confianza debajo del botón CTA (ej.: Gratis, sin tarjeta de crédito)

Genere 3 variantes.
```

**Resultado esperado**: Se generan 3 variantes de propuestas de copy.

---

## 🚀 Paso 4: Elaboración del plan de estructura de secciones

Determinar la estructura de secciones de la Landing Page basándose en el copy.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Estructura de secciones",
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
Compile todos los resultados de la entrevista (información del servicio, persona, beneficios, copy) en
output/lp-brief.md.

Genere con el siguiente formato:

# Brief de LP: {Nombre del servicio}

## Persona
- Nombre: {Alias}
- Edad: {Edad}
- Rol: {Rol}
- Desafíos: {3 desafíos}

## Ejes de propuesta
1. {Beneficio principal}
2. {Sub-beneficio 1}
3. {Sub-beneficio 2}

## Copy (seleccionado)
- Titular: {Copy seleccionado}
- Subtítulo: {Copy seleccionado}
- CTA: {CTA seleccionado}

## Estructura de secciones
1. Hero - Titular + CTA
2. Pain Points - 3 planteamientos de desafío
3. Solution - Presentación de la solución
4. Features - 3-4 características/puntos destacados
5. Social Proof - Resultados/Testimonios
6. FAQ - 3-5 preguntas frecuentes
7. Final CTA - Acción final

## Tono de diseño
{Tono seleccionado}
```

**Resultado esperado**: El brief se guarda en `output/lp-brief.md`.

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
      {"id": "trouble_1", "label": "No sé qué ingresar"},
      {"id": "trouble_2", "label": "El copy no se siente adecuado"},
      {"id": "trouble_3", "label": "No estoy seguro de la estructura de secciones"},
      {"id": "trouble_4", "label": "El archivo de salida no se genera"}
    ]
  }]
}
```

### Problema 1: No sé qué ingresar
**Solución**: Un servicio ficticio está bien. Pruebe con algo familiar cómo "Un servicio de generación automática de Landing Pages con IA".

### Problema 2: El copy no se siente adecuado
**Solución**: Dé instrucciones cómo "hazlo más casual", "agrega números" o "agrega urgencia" para regenerar.

### Problema 3: No estoy seguro de la estructura de secciones
**Solución**: Comience con la estructura básica (Hero → Pain → Solution → Features → Proof → CTA), luego agregue o elimine secciones después.

### Problema 4: El archivo de salida no se genera
**Solución**: Verifique si el directorio `output/` existe. Si no, créelo con `mkdir -p output`.

---

## ✅ Punto de control
- [ ] El tipo y categoría del servicio están decididos
- [ ] El persona objetivo está definido
- [ ] Los 3 beneficios son claros
- [ ] El titular y el texto del CTA están decididos
- [ ] Existe un borrador de la estructura de secciones
- [ ] Se ha generado `output/lp-brief.md`


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── lp-brief.md  (Brief de planificación de la Landing Page)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño del archivo
ls -lh output/lp-brief.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/lp-brief.md
```

> 💡 Ver contenido completó: `cat output/lp-brief.md` para mostrar el archivo completó

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```text
Verifique el contenido de output/lp-brief.md y confirme que el persona,
los ejes de propuesta, el copy y la estructura de secciones estén completos.
```

**Resultado esperado**: Se confirma la completitud del brief.

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
      {"id": "next_auto", "label": "Iniciar la siguiente sección (Creación de wireframe)"},
      {"id": "next_window", "label": "Abrir /start-13-2 en una nueva ventana"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → Ejecutar /start-13-2
- next_window → Abrir /start-13-2 en una nueva ventana
- finish → Finalizar
