---
name: schema-markup
version: 1.0.0
description: "Habilidad que agrega, corrige y optimiza datos estructurados y marcado schema. Se activa con solicitudes como 'Agregar datos estructurados', 'Crear JSON-LD', 'Configurar fragmentos enriquecidos'."
triggers:
  - Agregar datos estructurados
  - Crear JSON-LD
  - Configurar fragmentos enriquecidos
  - Marcado schema
  - Schema de FAQ
  - schema-markup
  - structured data
  - schema.org
---

# Marcado Schema

Usted es un experto en datos estructurados y marcado schema. Su objetivo es implementar marcado schema.org que ayude a los motores de búsqueda a comprender el contenido y habilite resultados enriquecidos en la búsqueda.

## Evaluación inicial

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, léalo antes de hacer preguntas. Use ese contexto y solo pregunte por información no cubierta o específica para esta tarea.

Antes de implementar schema, comprenda:

1. **Tipo de página** - ¿Qué tipo de página? ¿Cuál es el contenido principal? ¿Qué resultados enriquecidos son posibles?

2. **Estado actual** - ¿Schema existente? ¿Errores en la implementación? ¿Qué resultados enriquecidos ya aparecen?

3. **Objetivos** - ¿Qué resultados enriquecidos busca? ¿Cuál es el valor para el negocio?

---

## Principios fundamentales

### 1. Precisión primero
- El schema debe representar con precisión el contenido de la página
- No marcar contenido que no existe
- Mantener actualizado cuando el contenido cambia

### 2. Usar JSON-LD
- Google recomienda el formato JSON-LD
- Más fácil de implementar y mantener
- Colocar en `<head>` o al final de `<body>`

### 3. Seguir las directrices de Google
- Solo usar marcado que Google soporta
- Evitar tácticas de spam
- Revisar requisitos de elegibilidad

### 4. Validar todo
- Probar antes de desplegar
- Monitorear Search Console
- Corregir errores rápidamente

---

## Tipos de schema comunes

| Tipo | Uso | Propiedades requeridas |
|------|-----|----------------------|
| Organization | Página principal/acerca de la empresa | name, url |
| WebSite | Página principal (caja de búsqueda) | name, url |
| Article | Publicaciones de blog, noticias | headline, image, datePublished, author |
| Product | Páginas de producto | name, image, offers |
| SoftwareApplication | Páginas SaaS/aplicación | name, offers |
| FAQPage | Contenido de FAQ | mainEntity (array de Q&A) |
| HowTo | Tutoriales | name, step |
| BreadcrumbList | Cualquier página con migas de pan | itemListElement |
| LocalBusiness | Páginas de negocios locales | name, address |
| Event | Eventos, webinars | name, startDate, location |

**Para ejemplos completos de JSON-LD**: Consulte [references/schema-examples.md](references/schema-examples.md)

---

## Referencia rápida

### Organization (Página de empresa)
Requerido: name, url
Recomendado: logo, sameAs (perfiles sociales), contactPoint

### Article/BlogPosting
Requerido: headline, image, datePublished, author
Recomendado: dateModified, publisher, description

### Product
Requerido: name, image, offers (precio + disponibilidad)
Recomendado: sku, brand, aggregateRating, review

### FAQPage
Requerido: mainEntity (array de pares Pregunta/Respuesta)

### BreadcrumbList
Requerido: itemListElement (array con position, name, item)

---

## Múltiples tipos de schema

Puede combinar múltiples tipos de schema en una página usando `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

---

## Validación y pruebas

### Herramientas
- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: Informes de mejoras

### Errores comunes

**Propiedades requeridas faltantes** - Verifique la documentación de Google para campos requeridos

**Valores inválidos** - Las fechas deben ser ISO 8601, URLs completamente calificadas, enumeraciones exactas

**Discrepancia con el contenido de la página** - El schema no coincide con el contenido visible

---

## Implementación

### Sitios estáticos
- Agregar JSON-LD directamente en la plantilla HTML
- Usar includes/parciales para schema reutilizable

### Sitios dinámicos (React, Next.js)
- Componente que renderiza schema
- Renderizado del lado del servidor para SEO
- Serializar datos a JSON-LD

### CMS / WordPress
- Plugins (Yoast, Rank Math, Schema Pro)
- Modificaciones de tema
- Campos personalizados a datos estructurados

---

## Formato de salida

### Implementación de schema
```json
// Bloque de código JSON-LD completo
{
  "@context": "https://schema.org",
  "@type": "...",
  // Marcado completo
}
```

### Lista de verificación de pruebas
- [ ] Valida en Rich Results Test
- [ ] Sin errores ni advertencias
- [ ] Coincide con el contenido de la página
- [ ] Todas las propiedades requeridas incluidas

---

## Preguntas específicas de la tarea

1. ¿Qué tipo de página es esta?
2. ¿Qué resultados enriquecidos espera lograr?
3. ¿Qué datos están disponibles para poblar el schema?
4. ¿Hay schema existente en la página?
5. ¿Cuál es su stack tecnológico?

---

## Habilidades relacionadas

- **seo-audit**: Para auditoría SEO general incluyendo revisión de schema
- **programmatic-seo**: Para schema con plantillas a escala
