---
name: post-publisher
description: "Skill de publicación y distribución de contenido. Publica en X a través de Typefully, sube imágenes y programa publicaciones. Se activa con solicitudes como 'publicar esto', 'programar publicación', 'crear borrador en Typefully', etc."
triggers:
  - publicar esto
  - publicar
  - programar publicación
  - Typefully
  - crear borrador
  - distribuir
  - publish
  - schedule post
---

# Post Publisher

Publique y programe contenido pre-elaborado en diversas plataformas.

## Plataformas Compatibles

| Plataforma | Método | Estado |
|------------|--------|--------|
| X (Twitter) | Typefully API | ✅ Compatible |
| Hilos de X | Typefully API | ✅ Compatible |
| LinkedIn | Typefully API | ✅ Compatible |
| Instagram | Manual / Meta API (por implementar) | 🔧 Planificado |
| TikTok | Manual / TikTok API (por implementar) | 🔧 Planificado |
| Note | Manual / API (investigación necesaria) | 🔧 Planificado |
| Medium | Medium API | 🔧 Planificado |

## Typefully API

### Autenticación
Variable de entorno: `TYPEFULLY_API_KEY`

### Endpoints

#### Crear Borrador
```bash
curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Texto de la publicación",
    "threadify": false,
    "schedule-date": "2025-01-15T09:00:00Z",
    "auto_retweet_enabled": false,
    "auto_plug_enabled": false
  }'
```

#### Publicación de Hilos
Separe los tweets dentro de `content` usando `\n\n\n\n` (4 saltos de línea).
```json
{
  "content": "1/🧵 Gancho\n\n\n\n2/ Punto principal\n\n\n\n3/ CTA",
  "threadify": true
}
```

#### Publicación Programada
- `schedule-date`: formato ISO 8601 (UTC)
- `schedule-date: "next-free-slot"` para colocar automáticamente en el siguiente espacio disponible

#### Publicación Inmediata (Sin Borrador)
```json
{
  "content": "Texto",
  "schedule-date": "next-free-slot"
}
```

### Publicaciones con Imágenes

La API de Typefully no soporta carga directa de imágenes. Flujo de trabajo:
1. Subir imagen a catbox.moe
2. Publicar solo texto como borrador en Typefully
3. Adjuntar URL de la imagen como comentario (puede requerir adjunto manual)

## Flujo de Trabajo de Publicación

### Publicación Individual
1. Cargar contenido de `marketing/drafts/` (o generar con content-creator)
2. Confirmar plataforma
3. Crear borrador o programación vía Typefully API
4. Enviar mensaje de confirmación

### Publicación por Lotes
1. Cargar múltiples contenidos de `marketing/drafts/`
2. Distribuir programación (optimizar horarios)
3. Llamadas API por lotes
4. Enviar resumen de resultados

### Horarios Óptimos de Publicación (Mercado Japonés)
| Día | X | Instagram | TikTok |
|-----|---|-----------|--------|
| Días laborables | 7-8am, 12pm, 6-9pm | 12pm, 6-9pm | 6-10pm |
| Fines de semana | 9-11am, 2-4pm | 10am-12pm, 3-5pm | 12-10pm |

## Registro

Registrar resultados de publicación en `marketing/post-log.md`:
```markdown
| Fecha/Hora | Plataforma | Resumen del Contenido | URL | Estado |
```

## Skills Relacionados

- `marketing-planner` — Planificación de estrategia
- `content-creator` — Creación de contenido
