---
name: marketing-planner
description: "Skill de formulación de planes de marketing y creación de contexto de marketing de producto. Se activa con 'plan de marketing', 'posicionamiento', 'creación de persona', 'análisis competitivo', etc. Genera product-marketing-context.md para servir como base de otros skills de marketing."
triggers:
  - plan de marketing
  - planificación de marketing
  - posicionamiento
  - persona
  - análisis competitivo
  - estrategia de contenido
  - definición de objetivo
  - product marketing context
---

# Marketing Planner

Crea el documento base de marketing para su producto y construye la base para todas las iniciativas de marketing.

## Archivo de Salida

`marketing/product-context.md` -- Un contexto compartido referenciado por otros skills (content-creator, post-publisher, etc.).

## Flujo de Trabajo

### Paso 1: Verificar Contexto Existente

Verifique si existe `marketing/product-context.md`.
- **Si existe**: Cárguelo y verifique qué secciones necesitan actualización
- **Si no existe**: Proceda al flujo de creación nuevo

### Paso 2: Recopilación de Información

Complete las siguientes secciones a través de conversación. No pregunte todo a la vez.

1. **Resumen del Producto** -- Descripción en una línea, categoría, modelo de negocio, precios
2. **Objetivo** -- Segmentos de usuarios, personas, casos de uso principales
3. **Desafíos y Puntos de Dolor** -- Problemas que enfrentan los usuarios, deficiencias de las soluciones existentes
4. **Competidores** -- Competidores directos/indirectos, puntos de diferenciación
5. **Voz de Marca** -- Tono, estilo, palabras a usar/evitar
6. **Metas** -- Objetivos de negocio, KPIs, acciones de conversión

Framework detallado -> `references/context-template.md`

### Paso 3: Generación del Documento de Contexto

Genere `marketing/product-context.md` a partir de la información recopilada.

### Paso 4: Estrategia de Canales (Opcional)

Proponga la combinación óptima de canales basada en el contexto.
Detalles -> `references/channel-strategy.md`

### Paso 5: Calendario de Contenido (Opcional)

Genere un plan de publicación de contenido mensual/semanal en `marketing/content-calendar.md`.

## Skills Relacionados

- `content-creator` -- Crea contenido referenciando el contexto
- `post-publisher` -- Publica el contenido creado en cada plataforma
- Skills originales: `product-marketing-context`, `content-strategy`, `marketing-ideas`, `launch-strategy`
