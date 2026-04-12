---
name: content-creator
description: "Habilidad de creacion de contenido de marketing. Crea publicaciones de X/Instagram, articulos de Note/Medium, imagenes de banner, guiones de video y mas. Se activa con solicitudes como 'crear una publicacion', 'crear un banner', 'escribir un articulo', 'crear copia', etc. Referencia product-context.md para mantener consistencia de marca."
triggers:
  - crear una publicacion
  - creacion de contenido
  - crear un banner
  - escribir un articulo
  - crear copia
  - publicacion en redes sociales
  - crear tweet
  - publicacion Instagram
  - articulo Note
  - articulo Medium
  - 投稿作って
  - コンテンツ作成
---

# Creador de Contenido

Habilidad para crear contenido de marketing. Genera contenido consistente con la marca basandose en el contexto del producto.

## Prerequisitos

Debe existir `marketing/product-context.md`. Si no existe, solicite su creacion primero con la habilidad `marketing-planner`.

## Tipos de Contenido

### 1. Publicaciones en Redes Sociales (X / Instagram)

**Entrada**: Tema o prompt
**Salida**: Texto de publicacion + hashtags + (si es necesario) prompt de imagen

Formato -> `references/post-formats.md`

#### X (Twitter)
- Dentro de 280 caracteres (aproximadamente 140 caracteres para japones)
- Formato de hilo tambien compatible (3-7 tweets)
- El CTA debe ser claro

#### Instagram
- Caption: dentro de 2200 caracteres, los primeros 125 caracteres son criticos
- Hashtags: 20-30 (en orden de relevancia)
- Guiones de Reels/Stories tambien compatibles

### 2. Articulos (Note / Medium / Blog)

**Entrada**: Tema, audiencia objetivo, proposito
**Salida**: Propuesta de estructura -> Texto del cuerpo -> Meta informacion

Proceso:
1. Propuesta de esquema (estructura H2/H3)
2. Redaccion del cuerpo tras aprobacion
3. Generacion de meta SEO (titulo, descripcion, OGP)

### 3. Imagenes de Banner

**Entrada**: Caso de uso, texto, estilo
**Salida**: Prompt de generacion de imagen Gemini -> Generacion -> Revision

Guia de tamanos:
- X: 1200x675px
- Instagram Feed: 1080x1080px
- Instagram Stories: 1080x1920px
- Note/Medium OGP: 1200x630px

### 4. Guiones de Video

**Entrada**: Tema, duracion, plataforma
**Salida**: Guion (dialogos + indicaciones de pantalla)

- Corto (15-60 seg): Gancho -> Tema principal -> CTA
- Largo (5-15 min): Intro -> Secciones -> Resumen -> CTA

### 5. Correo Electronico

**Entrada**: Proposito, audiencia objetivo, posicion en la secuencia
**Salida**: Linea de asunto + Cuerpo + CTA

Detalles -> `references/email-templates.md`

## Verificacion de Calidad del Contenido

Siempre verifique despues de la generacion:
- [ ] Coincide con la voz de marca en product-context.md
- [ ] Apropiado para el persona objetivo
- [ ] El CTA es claro
- [ ] Cumple con las restricciones de la plataforma (conteo de caracteres, tamano de imagen, etc.)
- [ ] No utiliza palabras a evitar

## Generacion por Lotes

Maneja solicitudes como "Crear publicaciones para una semana":
1. Referencia content-calendar.md (si esta disponible)
2. Generar variaciones de temas
3. Optimizar por dia de la semana/hora del dia
4. Salida por lotes -> guardar en `marketing/drafts/`

## Habilidades Relacionadas

- `marketing-planner` -- Creacion de documento de contexto
- `post-publisher` -- Publicacion del contenido creado
- Habilidades fuente: `copywriting`, `copy-editing`, `social-content`, `email-sequence`
