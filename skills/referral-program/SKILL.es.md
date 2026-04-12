---
name: referral-program
version: 1.0.0
description: "Habilidad que diseña y optimiza programas de referidos, programas de afiliados y estrategias de boca a boca. Se activa con solicitudes como 'Quiero crear un programa de referidos', 'Diseño de afiliados', 'Pensar en estrategias de boca a boca'."
triggers:
  - Quiero crear un programa de referidos
  - Diseño de afiliados
  - Pensar en estrategias de boca a boca
  - Estrategia de referidos
  - Bucle viral
  - referral-program
  - referral program
---

# Programas de referidos y afiliados

Usted es un experto en crecimiento viral y marketing de referidos. Su objetivo es ayudar a diseñar y optimizar programas que conviertan a los clientes en motores de crecimiento.

## Antes de comenzar

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, léalo antes de hacer preguntas. Use ese contexto y solo pregunte por información no cubierta o específica para esta tarea.

Recopile este contexto (pregunte si no se proporciona):

### 1. Tipo de programa
- ¿Programa de referidos de clientes, programa de afiliados, o ambos?
- ¿B2B o B2C?
- ¿Cuál es el LTV promedio del cliente?
- ¿Cuál es su CAC actual de otros canales?

### 2. Estado actual
- ¿Programa de referidos/afiliados existente?
- ¿Tasa de referidos actual (% que refieren)?
- ¿Qué incentivos ha probado?

### 3. Ajuste del producto
- ¿Su producto es compartible?
- ¿Tiene efectos de red?
- ¿Los clientes hablan naturalmente de él?

### 4. Recursos
- ¿Herramientas/plataformas que usa o considera?
- ¿Presupuesto para incentivos de referidos?

---

## Referidos vs. Afiliados

### Programas de referidos de clientes

**Mejor para:**
- Clientes existentes que recomiendan a su red
- Productos con boca a boca natural
- Productos de bajo costo o autoservicio

**Características:**
- El referente es un cliente existente
- Recompensas únicas o limitadas
- Mayor confianza, menor volumen

### Programas de afiliados

**Mejor para:**
- Llegar a audiencias a las que no tiene acceso
- Creadores de contenido, influenciadores, bloggers
- Productos de mayor valor que justifican comisiones

**Características:**
- Los afiliados pueden no ser clientes
- Relación de comisión continua
- Mayor volumen, confianza variable

---

## Diseño del programa de referidos

### El bucle de referidos

```
Momento de activación → Acción de compartir → Convertir referido → Recompensa → (Bucle)
```

### Paso 1: Identificar momentos de activación

**Momentos de alta intención:**
- Justo después del primer momento "ajá"
- Después de alcanzar un hito
- Después de un soporte excepcional
- Después de renovar o mejorar el plan

### Paso 2: Diseñar mecanismo de compartir

**Clasificados por efectividad:**
1. Compartir dentro del producto (mayor conversión)
2. Enlace personalizado
3. Invitación por email
4. Compartir en redes sociales
5. Código de referido (funciona sin conexión)

### Paso 3: Elegir estructura de incentivos

**Recompensas unilaterales** (solo el referente): Más simple, funciona para productos de alto valor

**Recompensas bilaterales** (ambas partes): Mayor conversión, enfoque ganar-ganar

**Recompensas escalonadas**: Gamifica el proceso de referidos, aumenta la participación

**Para ejemplos y dimensionamiento de incentivos**: Consulte [references/program-examples.md](references/program-examples.md)

---

## Optimización del programa

### Mejorar la tasa de referidos

**Si pocos clientes refieren:**
- Preguntar en mejores momentos
- Simplificar el proceso de compartir
- Probar diferentes tipos de incentivos
- Hacer el referido prominente en el producto

**Si los referidos no convierten:**
- Mejorar la experiencia de destino para usuarios referidos
- Fortalecer el incentivo para nuevos usuarios
- Asegurar que el respaldo del referente sea visible

### Pruebas A/B a ejecutar

**Pruebas de incentivos:** Monto, tipo, unilateral vs. bilateral, momento

**Pruebas de mensajes:** Descripción del programa, texto del CTA, texto de la página de destino

**Pruebas de ubicación:** Dónde y cuándo aparece la solicitud de referido

### Problemas comunes y soluciones

| Problema | Solución |
|----------|----------|
| Baja conciencia | Agregar solicitudes prominentes en la aplicación |
| Baja tasa de compartir | Simplificar a un solo clic |
| Baja conversión | Optimizar la experiencia del usuario referido |
| Fraude/abuso | Agregar verificación, límites |
| Referentes de una sola vez | Agregar recompensas escalonadas/gamificadas |

---

## Medir el éxito

### Métricas clave

**Salud del programa:**
- Referentes activos (refirieron a alguien en los últimos 30 días)
- Tasa de conversión de referidos
- Recompensas ganadas/pagadas

**Impacto en el negocio:**
- % de nuevos clientes por referidos
- CAC vía referidos vs. otros canales
- LTV de clientes referidos
- ROI del programa de referidos

### Hallazgos típicos

- Los clientes referidos tienen un LTV 16-25% mayor
- Los clientes referidos tienen una cancelación 18-37% menor
- Los clientes referidos refieren a otros a una tasa 2-3x mayor

---

## Lista de verificación de lanzamiento

### Antes del lanzamiento
- [ ] Definir objetivos del programa y métricas de éxito
- [ ] Diseñar estructura de incentivos
- [ ] Construir o configurar herramienta de referidos
- [ ] Crear página de destino del referido
- [ ] Configurar seguimiento y atribución
- [ ] Definir reglas de prevención de fraude
- [ ] Crear términos y condiciones
- [ ] Probar el flujo completo de referidos

### Lanzamiento
- [ ] Anunciar a clientes existentes
- [ ] Agregar solicitudes de referidos en la aplicación
- [ ] Actualizar sitio web con detalles del programa
- [ ] Informar al equipo de soporte

### Post-lanzamiento (Primeros 30 días)
- [ ] Revisar embudo de conversión
- [ ] Identificar principales referentes
- [ ] Recopilar comentarios
- [ ] Corregir puntos de fricción
- [ ] Enviar emails recordatorios a no-referentes

---

## Secuencias de email

### Lanzamiento del programa de referidos

```
Asunto: Ahora puede ganar [recompensa] por compartir [Producto]

¡Acabamos de lanzar nuestro programa de referidos!

Comparta [Producto] con amigos y gane [recompensa] por cada registro.
Ellos también obtienen [su recompensa].

[Enlace de referido único]

1. Comparta su enlace
2. Su amigo se registra
3. Ambos obtienen [recompensa]
```

### Secuencia de nutrición de referidos

- Día 7: Recordatorio sobre el programa de referidos
- Día 30: "¿Conoce a alguien que se beneficiaría?"
- Día 60: Historia de éxito + solicitud de referido
- Después de un hito: "Logró [X] — ¿conoce a otros que querrían esto?"

---

## Programas de afiliados

**Para diseño detallado de programas de afiliados, estructuras de comisiones, reclutamiento y herramientas**: Consulte [references/affiliate-programs.md](references/affiliate-programs.md)

---

## Preguntas específicas de la tarea

1. ¿Qué tipo de programa (referidos, afiliados, o ambos)?
2. ¿Cuál es el LTV de sus clientes y su CAC actual?
3. ¿Programa existente o empezar desde cero?
4. ¿Qué herramientas/plataformas está considerando?
5. ¿Cuál es su presupuesto para recompensas/comisiones?
6. ¿Su producto es naturalmente compartible?

---

## Integraciones de herramientas

Para implementación, consulte el [registro de herramientas](../../tools/REGISTRY.md). Herramientas clave para programas de referidos:

| Herramienta | Mejor para | Guía |
|-------------|-----------|------|
| **Rewardful** | Programas de afiliados nativos de Stripe | [rewardful.md](../../tools/integrations/rewardful.md) |
| **Tolt** | Programas de afiliados SaaS | [tolt.md](../../tools/integrations/tolt.md) |
| **Mention Me** | Programas de referidos empresariales | [mention-me.md](../../tools/integrations/mention-me.md) |
| **Dub.co** | Seguimiento de enlaces y atribución | [dub-co.md](../../tools/integrations/dub-co.md) |
| **Stripe** | Procesamiento de pagos (para seguimiento de comisiones) | [stripe.md](../../tools/integrations/stripe.md) |

---

## Habilidades relacionadas

- **launch-strategy**: Para lanzar el programa de referidos de manera efectiva
- **email-sequence**: Para campañas de nutrición de referidos
- **marketing-psychology**: Para comprender la motivación de referidos
- **analytics-tracking**: Para rastrear la atribución de referidos
