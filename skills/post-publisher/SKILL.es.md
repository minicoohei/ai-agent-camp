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

## Typefully API v2

### Autenticación
Variable de entorno: `TYPEFULLY_API_KEY`
Encabezado: `Authorization: Bearer $TYPEFULLY_API_KEY`

### Obtención de social_set_id (obligatorio)

Todos los endpoints v2 requieren social_set_id. Obténlo primero.

```bash
curl -X GET "https://api.typefully.com/v2/social-sets" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY"
# Copia el id de la respuesta y guárdalo en una variable de entorno
export TYPEFULLY_SOCIAL_SET_ID="el-id-obtenido"
```

### Endpoints

#### Crear Borrador (publicación X única)
```bash
curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [{"text": "Texto de la publicación"}]
      }
    },
    "publish_at": "2025-01-15T09:00:00Z"
  }'
```

#### Publicación de Hilos
Coloca múltiples entradas en el array `posts` (el `\n\n\n\n` + `threadify` de v1 están obsoletos).
```json
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [
        {"text": "1/🧵 Gancho"},
        {"text": "2/ Punto principal"},
        {"text": "3/ CTA"}
      ]
    }
  }
}
```

#### Publicación Programada
- `publish_at`: formato ISO 8601 (UTC)
- `publish_at: "next-free-slot"` para colocar automáticamente en el siguiente espacio disponible

#### Publicación simultánea en X y Threads
```json
{
  "platforms": {
    "x":       {"enabled": true, "posts": [{"text": "Texto"}]},
    "threads": {"enabled": true, "posts": [{"text": "Texto"}]}
  },
  "publish_at": "next-free-slot"
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
