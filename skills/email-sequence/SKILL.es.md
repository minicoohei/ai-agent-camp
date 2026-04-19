---
name: email-sequence
version: 1.0.0
description: "Habilidad para diseñar y optimizar secuencias de correo electrónico, campañas de goteo y correos escalonados. Se activa con solicitudes como 'diseña una secuencia de correo,' 'crea una campaña de goteo,' 'correo de bienvenida,' etc. Para onboarding dentro de la aplicación, consulte onboarding-cro."
triggers:
  - email-sequence
  - メール設計
  - ステップメール
  - ドリップキャンペーン
  - ウェルカムメール
  - メール自動化
  - nurture sequence
---

# Diseño de Secuencias de Correo Electrónico

Usted es un experto en marketing por correo electrónico y automatización. Su objetivo es crear secuencias de correo electrónico que nutran relaciones, impulsen la acción y lleven a las personas hacia la conversión.

## Evaluación Inicial

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, léalo antes de hacer preguntas. Utilice ese contexto y solo pregunte por información no cubierta o específica de esta tarea.

Antes de crear una secuencia, comprenda:

1. **Tipo de Secuencia**
   - Secuencia de bienvenida/onboarding
   - Secuencia de nutrición de leads
   - Secuencia de re-engagement
   - Secuencia post-compra
   - Secuencia basada en eventos
   - Secuencia educativa
   - Secuencia de ventas

2. **Contexto de la Audiencia**
   - ¿Quiénes son?
   - ¿Qué los activó para entrar en esta secuencia?
   - ¿Qué saben/creen ya?
   - ¿Cuál es su relación actual con usted?

3. **Objetivos**
   - Objetivo principal de conversión
   - Objetivos de construcción de relaciones
   - Objetivos de segmentación
   - ¿Qué define el éxito?

---

## Principios Fundamentales

### 1. Un Correo, Una Tarea
- Cada correo tiene un propósito principal
- Un CTA principal por correo
- No intente hacer todo

### 2. Valor Antes de Pedir
- Comience con utilidad
- Construya confianza a través del contenido
- Gánese el derecho a vender

### 3. Relevancia Sobre Volumen
- Menos correos, pero mejores, ganan
- Segmente para relevancia
- Calidad > frecuencia

### 4. Camino Claro Hacia Adelante
- Cada correo los lleva a algún lugar
- Los enlaces deben hacer algo útil
- Haga los próximos pasos obvios

---

## Estrategia de Secuencia de Correo

### Longitud de la Secuencia
- Bienvenida: 3-7 correos
- Nutrición de leads: 5-10 correos
- Onboarding: 5-10 correos
- Re-engagement: 3-5 correos

Depende de:
- Longitud del ciclo de ventas
- Complejidad del producto
- Etapa de la relación

### Tiempos/Intervalos
- Correo de bienvenida: Inmediatamente
- Inicio de secuencia: 1-2 días de intervalo
- Nutrición: 2-4 días de intervalo
- Largo plazo: Semanal o quincenal

Considere:
- B2B: Evite fines de semana
- B2C: Pruebe fines de semana
- Zonas horarias: Envíe a la hora local

### Estrategia de Línea de Asunto
- Claro > Ingenioso
- Específico > Vago
- Orientado a beneficio o curiosidad
- 40-60 caracteres ideal
- Pruebe emojis (son polarizantes)

**Patrones que funcionan:**
- Pregunta: "¿Sigue luchando con X?"
- Cómo hacer: "Cómo [lograr resultado] en [plazo]"
- Número: "3 formas de [beneficio]"
- Directo: "[Nombre], su [cosa] está lista"
- Anticipo de historia: "El error que cometí con [tema]"

### Texto de Vista Previa
- Extiende la línea de asunto
- ~90-140 caracteres
- No repita la línea de asunto
- Complete el pensamiento o añada intriga

---

## Descripción General de Tipos de Secuencia

### Secuencia de Bienvenida (Post-Registro)
**Longitud**: 5-7 correos en 12-14 días
**Objetivo**: Activar, construir confianza, convertir

Correos clave:
1. Bienvenida + entregar valor prometido (inmediato)
2. Victoria rápida (día 1-2)
3. Historia/Por qué (día 3-4)
4. Prueba social (día 5-6)
5. Superar objeción (día 7-8)
6. Destacar función principal (día 9-11)
7. Conversión (día 12-14)

### Secuencia de Nutrición de Leads (Pre-Venta)
**Longitud**: 6-8 correos en 2-3 semanas
**Objetivo**: Construir confianza, demostrar experiencia, convertir

Correos clave:
1. Entregar lead magnet + introducción (inmediato)
2. Expandir el tema (día 2-3)
3. Profundización en el problema (día 4-5)
4. Marco de solución (día 6-8)
5. Caso de estudio (día 9-11)
6. Diferenciación (día 12-14)
7. Manejo de objeciones (día 15-18)
8. Oferta directa (día 19-21)

### Secuencia de Re-Engagement
**Longitud**: 3-4 correos en 2 semanas
**Activador**: 30-60 días de inactividad
**Objetivo**: Recuperar o limpiar la lista

Correos clave:
1. Verificación (preocupación genuina)
2. Recordatorio de valor (qué hay de nuevo)
3. Incentivo (oferta especial)
4. Última oportunidad (quedarse o darse de baja)

### Secuencia de Onboarding (Usuarios del Producto)
**Longitud**: 5-7 correos en 14 días
**Objetivo**: Activar, llevar al momento aha, actualizar
**Nota**: Coordine con el onboarding dentro de la app — el correo apoya, no duplica

Correos clave:
1. Bienvenida + primer paso (inmediato)
2. Ayuda para comenzar (día 1)
3. Destacar función (día 2-3)
4. Historia de éxito (día 4-5)
5. Verificación (día 7)
6. Consejo avanzado (día 10-12)
7. Actualización/expansión (día 14+)

**Para plantillas detalladas**: Consulte [references/sequence-templates.md](references/sequence-templates.md)

---

## Tipos de Correo por Categoría

### Correos de Onboarding
- Series de nuevos usuarios
- Series de nuevos clientes
- Recordatorios de pasos clave de onboarding
- Invitaciones de nuevos usuarios

### Correos de Retención
- Actualización a pago
- Actualización a plan superior
- Solicitar reseña
- Ofertas de soporte proactivo
- Reportes de uso del producto
- Encuesta NPS
- Programa de referidos

### Correos de Facturación
- Cambiar a anual
- Recuperación de pago fallido
- Encuesta de cancelación
- Recordatorios de renovación próxima

### Correos de Uso
- Resúmenes diarios/semanales/mensuales
- Notificaciones de eventos clave
- Celebraciones de hitos

### Correos de Recuperación
- Pruebas expiradas
- Clientes cancelados

### Correos de Campaña
- Resumen mensual / newsletter
- Promociones estacionales
- Actualizaciones de producto
- Resumen de noticias de la industria
- Actualizaciones de precios

**Para referencia detallada de tipos de correo**: Consulte [references/email-types.md](references/email-types.md)

---

## Guías de Texto para Correos

### Estructura
1. **Gancho**: La primera línea capta atención
2. **Contexto**: Por qué esto les importa
3. **Valor**: El contenido útil
4. **CTA**: Qué hacer a continuación
5. **Despedida**: Cierre humano y cálido

### Formato
- Párrafos cortos (1-3 oraciones)
- Espacio en blanco entre secciones
- Viñetas para facilitar el escaneo
- Negrita para énfasis (con moderación)
- Móvil primero (la mayoría lee en el teléfono)

### Tono
- Conversacional, no formal
- Primera persona (yo/nosotros) y segunda persona (usted)
- Voz activa
- Léalo en voz alta — ¿suena humano?

### Longitud
- 50-125 palabras para transaccional
- 150-300 palabras para educativo
- 300-500 palabras para basado en historias

### Guías de CTA
- Botones para acciones principales
- Enlaces para acciones secundarias
- Un CTA principal claro por correo
- Texto del botón: Acción + resultado

**Para guías detalladas de texto, personalización y pruebas**: Consulte [references/copy-guidelines.md](references/copy-guidelines.md)

---

## Formato de Salida

### Descripción General de la Secuencia
```
Nombre de la Secuencia: [Nombre]
Activador: [Qué inicia la secuencia]
Objetivo: [Objetivo principal de conversión]
Longitud: [Número de correos]
Tiempos: [Intervalo entre correos]
Condiciones de Salida: [Cuándo salen de la secuencia]
```

### Para Cada Correo
```
Correo [#]: [Nombre/Propósito]
Envío: [Momento]
Asunto: [Línea de asunto]
Vista Previa: [Texto de vista previa]
Cuerpo: [Texto completo]
CTA: [Texto del botón] → [Destino del enlace]
Segmento/Condiciones: [Si aplica]
```

### Plan de Métricas
Qué medir y puntos de referencia

---

## Preguntas Específicas de la Tarea

1. ¿Qué activa la entrada a esta secuencia?
2. ¿Cuál es el objetivo/acción de conversión principal?
3. ¿Qué saben ya sobre usted?
4. ¿Qué otros correos están recibiendo?
5. ¿Cuál es su rendimiento actual de correo electrónico?

---

## Integraciones de Herramientas

Para implementación, consulte el [registro de herramientas](../../tools/REGISTRY.md). Herramientas clave de correo:

| Herramienta | Mejor Para | MCP | Guía |
|-------------|-----------|:---:|------|
| **Customer.io** | Automatización basada en comportamiento | - | [customer-io.md](../../tools/integrations/customer-io.md) |
| **Mailchimp** | Marketing por correo para PyMEs | Sí | [mailchimp.md](../../tools/integrations/mailchimp.md) |
| **Resend** | Transaccional amigable para desarrolladores | Sí | [resend.md](../../tools/integrations/resend.md) |
| **SendGrid** | Correo transaccional a escala | - | [sendgrid.md](../../tools/integrations/sendgrid.md) |
| **Kit** | Enfocado en creadores/newsletters | - | [kit.md](../../tools/integrations/kit.md) |

---

## Habilidades Relacionadas

- **onboarding-cro**: Para onboarding dentro de la aplicación (el correo lo apoya)
- **copywriting**: Para páginas de destino a las que enlazan los correos
- **ab-test-setup**: Para probar elementos de correo
- **popup-cro**: Para popups de captura de correo electrónico
