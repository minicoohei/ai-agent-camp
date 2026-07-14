---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "30 min"
prerequisites: ["start-16-1"]
level: "intermediate"
tags: ["email", "sequence", "drip-campaign", "marketing"]
nonInteractiveMode: deferred
---
# Lección 16-4: Diseño de Secuencia de Correos

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-4: Diseño de Secuencia de Correos**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Disenar campanas de goteo y secuencias de bienvenida con la habilidad email-sequence |
| Duración | ~30 min |
| Habilidades utilizadas | email-sequence |
| Requisitos previos | Lección 16-1 completada (gogcli autenticado) |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

**Flujo de la sesión:**
1. Comprender los conceptos básicos de secuencias de correo
2. Disenar una secuencia de bienvenida
3. Crear plantillas de correo
4. Optimizar tiempos de envío y estrategia de asuntos

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Paso 1: Conceptos Básicos de Secuencias de Correo

Una secuencia de correo es una serie de correos enviados automáticamente en respuesta a un disparador específico.

**Tipos principales de secuencias:**
| Tipo | Propósito | Ejemplo |
|------|-----------|---------|
| Bienvenida | Dar la bienvenida a nuevos registrados | Presentación del servicio -> Guía de uso -> Consejos |
| Onboarding | Apoyo al inicio del uso | Configuración -> Primera operación -> Aplicación |
| Lead nurturing | Cultivar prospectos | Planteamiento del problema -> Solución -> Caso de éxito -> CTA |
| Re-engagement | Recuperar usuarios inactivos | Actualizaciones -> Nuevas funciones -> Ofertas |

---

## Paso 2: Disenar una Secuencia de Bienvenida

**Ejecute el siguiente prompt en Cursor / Claude Code:**
```text
Use la habilidad email-sequence para disenar una secuencia de correos de bienvenida para un producto SaaS.

Condiciones:
- Destinatarios: Nuevos usuarios registrados gratuitamente
- Numero de correos: 5
- Periodo: 14 dias desde el registro
- Objetivo: Actualizacion a plan de pago
```

---

## Paso 3: Crear Plantillas de Correo

**Componentes de la plantilla:**
- **Asunto**: El elemento más importante que afecta la tasa de apertura
- **Pre-header**: Complemento del asunto (se muestra en la vista previa del cliente de correo)
- **Cuerpo**: Contenido principal
- **CTA**: Boton/enlace de llamada a la acción

---

## Paso 4: Tiempos de Envió y Estrategia de Asuntos

**Mejores prácticas de tiempo de envió:**
| Correo | Tiempo | Razon |
|--------|--------|-------|
| 1er correo | Inmediatamente después del registro | Momento de máximo interes |
| 2do correo | Día siguiente | Seguimiento de la primera operación |
| 3er correo | 3 días después | Apoyo en la formación de habitos |
| 4to correo | 7 días después | Reconfirmación de valor |
| 5to correo | 14 días después | Propuesta de actualización |

**Estrategia de A/B testing para asuntos:**
- Personalización: Incluir "{nombre}" o no
- Urgencia: "Por tiempo limitado", "Quedan 3 días"
- Pregunta: "Tiene problemas con...?"
- Números: "En 3 pasos"

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| No puede decidir la estructura de la secuencia | Comience con una plantilla y personalice gradualmente |
| Demasiados/pocos correos | Disene con el mínimo de pasos necesarios para el objetivo |
| No se le ocurren ideas para asuntos | Referencie correos de la competencia o pida multiples propuestas a la IA |

---

## Punto de Control

- [ ] El diseño de la secuencia de correos (5 o más) esta completo
- [ ] Se crearon plantillas de asunto y cuerpo para cada correo
- [ ] Se establecieron los tiempos de envío

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-4 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_lesson", "label": "Ir a 16-5 -> Flujo de trabajo de automatizacion de correo"},
      {"id": "practice", "label": "Quiero disenar otro tipo de secuencia"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
