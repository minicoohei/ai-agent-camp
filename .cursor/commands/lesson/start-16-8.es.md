---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "30 min"
prerequisites: ["start-16-6", "start-16-7"]
level: "intermediate"
tags: ["email", "resend", "resend-cli", "sequences", "drip-campaign", "automation"]
nonInteractiveMode: deferred
---
# Lección 16-8: Campaña de Goteo con Resend Sequence y CLI

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-8: Campaña de Goteo con Resend Sequence**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear una secuencia de bienvenida con Resend Sequences y automatizar la gestión de contactos con CLI |
| Duración | ~30 min |
| Herramientas utilizadas | Resend CLI (`resend-cli`), Resend Dashboard, habilidad email-sequence |
| Requisitos previos | Lecciones 16-6 y 16-7 completadas (dominio verificado y clave API creada) |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

> **Consejo**: Si automatiza la gestión de contactos con Resend CLI, puede agregar automáticamente nuevos usuarios registrados a las secuencias.

---

## Paso 1: Concepto Básico de Secuencias

**Qué es una secuencia?**
Un mecanismo que envía correos automáticamente a intervalos predefinidos, activado por un disparador específico.

**Ejemplo de secuencia de bienvenida:**
| Correo | Tiempo | Asunto | Propósito |
|--------|--------|--------|-----------|
| 1er | Día 0 (inmediato) | Bienvenido! Guía de inicio | Primera impresión, visión general del servicio |
| 2do | Día 3 | 3 consejos para aprovecharlo al máximo | Presentación de funciones principales |
| 3ro | Día 7 | Caso de éxito de [nombre] | Prueba social |
| 4to | Día 14 | Cuéntenos su opinión | Engagement |

---

## Paso 2: Crear Secuencia en Resend Dashboard

1. Dashboard de Resend -> **Sequences** -> Create Sequence
2. Ingrese el nombre de la secuencia (ejemplo: "Welcome Series")
3. Configure la condición de disparador (ejemplo: cuando se agrega a una Audience)
4. Agregue los pasos de correo (asunto, cuerpo, intervalo de envío)

**Generar plantillas con la habilidad email-sequence:**
```text
Use la habilidad email-sequence para disenar una secuencia de bienvenida para SaaS.

Condiciones:
- Destinatarios: Nuevos usuarios registrados gratuitamente
- Numero de correos: 4
- Periodo: 14 dias
- Objetivo: Adopcion del producto e induccion a plan de pago
- Tono: Amigable y cercano
```

---

## Paso 3: Gestión de Contactos y Audiences con Resend CLI

**Crear una Audience:**
```bash
resend audiences create --name "Welcome Series"
```

**Agregar un contacto:**
```bash
resend contacts create \
  --audience-id <audience-id> \
  --email "user@example.com" \
  --first-name "Taro"
```

**Verificar lista de contactos:**
```bash
resend contacts list --audience-id <audience-id>
```

**Salida JSON (para automatización/scripts):**
```bash
resend contacts list --audience-id <audience-id> --json
```

> **Punto de automatización**: Si agrega contactos automáticamente via Webhook -> Resend CLI al registrarse un nuevo usuario, la secuencia se inicia automáticamente.

---

## Paso 4: Envió de Prueba y Monitoreo

**Ejecutar la secuencia con contacto de prueba:**
1. Agregue su propia dirección de correo como contacto
2. Verifique que llegue el primer correo de la secuencia
3. Monitoree el estado de entrega en el Dashboard de Resend

**Puntos de verificación de metricas de entrega:**
- Tasa de entrega (Delivery Rate)
- Tasa de apertura (Open Rate)
- Tasa de clics (Click Rate)
- Tasa de desuscripción (Unsubscribe Rate)

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| La secuencia no se inicia | Verifique que los contactos esten correctamente agregados a la Audience |
| El correo no llega | Re-verifique el dominio. Revise la configuración SPF/DKIM |
| La Audience no se encuentra en CLI | Verifique el ID con `resend audiences list` |
| La plantilla no resulta como se esperaba | Agregue condiciones más detalladas a la habilidad email-sequence y regenere |

---

## Punto de Control

- [ ] Comprendio los patrones de diseño de secuencias
- [ ] Creó una secuencia en Resend Dashboard
- [ ] Administro Audiences y contactos con Resend CLI
- [ ] Verificó el funcionamiento de la secuencia con envío de prueba

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-8 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-17-1)"},
      {"id": "practice", "label": "Quiero crear otra secuencia tambien"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
