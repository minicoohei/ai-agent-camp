---
name: analytics-tracking
version: 1.0.0
description: "Habilidad para apoyar la configuracion, mejora y auditoria del seguimiento analitico. Se activa con solicitudes como 'configurar seguimiento', 'implementar GA4', 'seguimiento de conversiones', 'seguimiento de eventos', 'parametros UTM', 'configuracion de GTM', etc. Para seguimiento de pruebas A/B, consulte ab-test-setup."
triggers:
  - analytics-tracking
  - configuracion de seguimiento
  - GA4
  - Google Analytics
  - seguimiento de conversiones
  - seguimiento de eventos
  - parametros UTM
  - GTM
  - tracking setup
  - トラッキング設定
---

# Seguimiento Analitico

Usted es un experto en implementacion y medicion analitica. Su objetivo es ayudar a configurar el seguimiento que proporcione informacion accionable para decisiones de marketing y producto.

## Evaluacion Inicial

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, lealo antes de hacer preguntas. Utilice ese contexto y solo pregunte por informacion no cubierta o especifica de esta tarea.

Antes de implementar el seguimiento, comprenda:

1. **Contexto del Negocio** - ¿Que decisiones informaran estos datos? ¿Cuales son las conversiones clave?
2. **Estado Actual** - ¿Que seguimiento existe? ¿Que herramientas estan en uso?
3. **Contexto Tecnico** - ¿Cual es el stack tecnologico? ¿Hay requisitos de privacidad/cumplimiento?

---

## Principios Fundamentales

### 1. Rastree para Decisiones, No para Datos
- Cada evento debe informar una decision
- Evite metricas de vanidad
- Calidad > cantidad de eventos

### 2. Comience con las Preguntas
- ¿Que necesita saber?
- ¿Que acciones tomara basandose en estos datos?
- Trabaje hacia atras hasta lo que necesita rastrear

### 3. Nombre las Cosas Consistentemente
- Las convenciones de nombres importan
- Establezca patrones antes de implementar
- Documente todo

### 4. Mantenga la Calidad de Datos
- Valide la implementacion
- Monitoree problemas
- Datos limpios > mas datos

---

## Marco del Plan de Seguimiento

### Estructura

```
Nombre del Evento | Categoria | Propiedades | Disparador | Notas
----------------- | --------- | ----------- | ---------- | -----
```

### Tipos de Eventos

| Tipo | Ejemplos |
|------|----------|
| Vistas de pagina | Automaticas, mejoradas con metadatos |
| Acciones del usuario | Clics en botones, envios de formularios, uso de funciones |
| Eventos del sistema | Registro completado, compra, suscripcion cambiada |
| Conversiones personalizadas | Completacion de objetivos, etapas del embudo |

**Para listas completas de eventos**: Consulte [references/event-library.md](references/event-library.md)

---

## Convenciones de Nombres de Eventos

### Formato Recomendado: Objeto-Accion

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### Mejores Practicas
- Minusculas con guiones bajos
- Sea especifico: `cta_hero_clicked` vs. `button_clicked`
- Incluya contexto en propiedades, no en el nombre del evento
- Evite espacios y caracteres especiales
- Documente las decisiones

---

## Eventos Esenciales

### Sitio de Marketing

| Evento | Propiedades |
|--------|-------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### Producto/Aplicacion

| Evento | Propiedades |
|--------|-------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**Para la biblioteca completa de eventos por tipo de negocio**: Consulte [references/event-library.md](references/event-library.md)

---

## Propiedades de Eventos

### Propiedades Estandar

| Categoria | Propiedades |
|-----------|-------------|
| Pagina | page_title, page_location, page_referrer |
| Usuario | user_id, user_type, account_id, plan_type |
| Campana | source, medium, campaign, content, term |
| Producto | product_id, product_name, category, price |

### Mejores Practicas
- Use nombres de propiedades consistentes
- Incluya contexto relevante
- No duplique propiedades automaticas
- Evite PII en propiedades

---

## Implementacion de GA4

### Configuracion Rapida

1. Crear propiedad GA4 y flujo de datos
2. Instalar gtag.js o GTM
3. Habilitar medicion mejorada
4. Configurar eventos personalizados
5. Marcar conversiones en Administracion

### Ejemplo de Evento Personalizado

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**Para implementacion detallada de GA4**: Consulte [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Estructura del Contenedor

| Componente | Proposito |
|------------|-----------|
| Tags | Codigo que se ejecuta (GA4, pixeles) |
| Triggers | Cuando se activan los tags (vista de pagina, clic) |
| Variables | Valores dinamicos (texto de clic, capa de datos) |

### Patron de Capa de Datos

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**Para implementacion detallada de GTM**: Consulte [references/gtm-implementation.md](references/gtm-implementation.md)

---

## Estrategia de Parametros UTM

### Parametros Estandar

| Parametro | Proposito | Ejemplo |
|-----------|-----------|---------|
| utm_source | Fuente de trafico | google, newsletter |
| utm_medium | Medio de marketing | cpc, email, social |
| utm_campaign | Nombre de campana | spring_sale |
| utm_content | Diferenciar versiones | hero_cta |
| utm_term | Palabras clave de busqueda pagada | running+shoes |

### Convenciones de Nombres
- Todo en minusculas
- Use guiones bajos o guiones consistentemente
- Sea especifico pero conciso: `blog_footer_cta`, no `cta1`
- Documente todos los UTMs en una hoja de calculo

---

## Depuracion y Validacion

### Herramientas de Prueba

| Herramienta | Uso |
|-------------|-----|
| GA4 DebugView | Monitoreo de eventos en tiempo real |
| Modo de Vista Previa de GTM | Probar disparadores antes de publicar |
| Extensiones del Navegador | Tag Assistant, dataLayer Inspector |

### Lista de Verificacion de Validacion

- [ ] Eventos disparandose en los disparadores correctos
- [ ] Valores de propiedades llenandose correctamente
- [ ] Sin eventos duplicados
- [ ] Funciona en todos los navegadores y movil
- [ ] Conversiones registradas correctamente
- [ ] Sin fuga de PII

### Problemas Comunes

| Problema | Verificar |
|----------|-----------|
| Eventos no se disparan | Configuracion del disparador, GTM cargado |
| Valores incorrectos | Ruta de variable, estructura de capa de datos |
| Eventos duplicados | Multiples contenedores, disparador activandose dos veces |

---

## Privacidad y Cumplimiento

### Consideraciones
- Consentimiento de cookies requerido en UE/RU/CA
- Sin PII en propiedades analiticas
- Configuraciones de retencion de datos
- Capacidades de eliminacion de usuarios

### Implementacion
- Usar modo de consentimiento (esperar consentimiento)
- Anonimizacion de IP
- Solo recopilar lo necesario
- Integrar con plataforma de gestion de consentimiento

---

## Formato de Salida

### Documento del Plan de Seguimiento

```markdown
# Plan de Seguimiento de [Sitio/Producto]

## Descripcion General
- Herramientas: GA4, GTM
- Ultima actualizacion: [Fecha]

## Eventos

| Nombre del Evento | Descripcion | Propiedades | Disparador |
|-------------------|-------------|-------------|------------|
| signup_completed | Usuario completa registro | method, plan | Pagina de exito |

## Dimensiones Personalizadas

| Nombre | Alcance | Parametro |
|--------|---------|-----------|
| user_type | Usuario | user_type |

## Conversiones

| Conversion | Evento | Conteo |
|------------|--------|--------|
| Registro | signup_completed | Una vez por sesion |
```

---

## Preguntas Especificas de la Tarea

1. ¿Que herramientas esta usando (GA4, Mixpanel, etc.)?
2. ¿Que acciones clave desea rastrear?
3. ¿Que decisiones informaran estos datos?
4. ¿Quien implementa - equipo de desarrollo o marketing?
5. ¿Hay requisitos de privacidad/consentimiento?
6. ¿Que se esta rastreando actualmente?

---

## Integraciones de Herramientas

Para implementacion, consulte el [registro de herramientas](../../tools/REGISTRY.md). Herramientas analiticas clave:

| Herramienta | Mejor Para | MCP | Guia |
|-------------|-----------|:---:|------|
| **GA4** | Analitica web, ecosistema Google | ✓ | [ga4.md](../../tools/integrations/ga4.md) |
| **Mixpanel** | Analitica de producto, seguimiento de eventos | - | [mixpanel.md](../../tools/integrations/mixpanel.md) |
| **Amplitude** | Analitica de producto, analisis de cohortes | - | [amplitude.md](../../tools/integrations/amplitude.md) |
| **PostHog** | Analitica de codigo abierto, reproduccion de sesiones | - | [posthog.md](../../tools/integrations/posthog.md) |
| **Segment** | Plataforma de datos de clientes, enrutamiento | - | [segment.md](../../tools/integrations/segment.md) |

---

## Habilidades Relacionadas

- **ab-test-setup**: Para seguimiento de experimentos
- **seo-audit**: Para analisis de trafico organico
- **page-cro**: Para optimizacion de conversiones (usa estos datos)
