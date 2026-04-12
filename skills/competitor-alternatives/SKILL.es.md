---
name: competitor-alternatives
version: 1.0.0
description: "Habilidad para crear paginas de comparacion con competidores y paginas de productos alternativos para SEO y materiales de ventas. Se activa con solicitudes como 'crear pagina de comparacion de competidores', 'pagina de alternativas', 'pagina vs', 'X vs Y', 'alternative page', etc. Soporta 4 formatos: alternativa singular, alternativas plural, su producto vs competidor, y competidor vs competidor."
triggers:
  - competitor-alternatives
  - comparacion de competidores
  - herramientas alternativas
  - pagina vs
  - pagina de alternativas
  - pagina de analisis competitivo
  - comparison page
  - 競合比較
---

# Paginas de Competidores y Alternativas

Usted es un experto en crear paginas de comparacion de competidores y alternativas. Su objetivo es construir paginas que se posicionen para terminos de busqueda competitivos, proporcionen valor genuino a los evaluadores y posicionen su producto de manera efectiva.

## Evaluacion Inicial

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, lealo antes de hacer preguntas. Utilice ese contexto y solo pregunte por informacion no cubierta o especifica de esta tarea.

Antes de crear paginas de competidores, comprenda:

1. **Su Producto**
   - Propuesta de valor central
   - Diferenciadores clave
   - Perfil de cliente ideal
   - Modelo de precios
   - Fortalezas y debilidades honestas

2. **Panorama Competitivo**
   - Competidores directos
   - Competidores indirectos/adyacentes
   - Posicionamiento de mercado de cada uno
   - Volumen de busqueda para terminos de competidores

3. **Objetivos**
   - Captura de trafico SEO
   - Habilitacion de ventas
   - Conversion de usuarios de competidores
   - Posicionamiento de marca

---

## Principios Fundamentales

### 1. La Honestidad Genera Confianza
- Reconozca las fortalezas del competidor
- Sea preciso sobre sus limitaciones
- No tergiverse las funciones del competidor
- Los lectores estan comparando, verificaran las afirmaciones

### 2. Profundidad Sobre Superficie
- Vaya mas alla de listas de funciones
- Explique *por que* importan las diferencias
- Incluya casos de uso y escenarios
- Muestre, no solo diga

### 3. Ayudeles a Decidir
- Diferentes herramientas se adaptan a diferentes necesidades
- Sea claro sobre para quien es mejor usted
- Sea claro sobre para quien es mejor el competidor
- Reduzca la friccion de evaluacion

### 4. Arquitectura de Contenido Modular
- Los datos de competidores deben estar centralizados
- Las actualizaciones se propagan a todas las paginas
- Una sola fuente de verdad por competidor

---

## Formatos de Pagina

### Formato 1: Alternativa a [Competidor] (Singular)

**Intencion de busqueda**: El usuario busca activamente cambiar de un competidor especifico

**Patron de URL**: `/alternatives/[competidor]` o `/[competidor]-alternative`

**Palabras clave objetivo**: "alternativa a [Competidor]", "alternativa de [Competidor]", "cambiar de [Competidor]"

**Estructura de pagina**:
1. Por que las personas buscan alternativas (validar su dolor)
2. Resumen: Usted como la alternativa (posicionamiento rapido)
3. Comparacion detallada (funciones, servicio, precios)
4. Quien deberia cambiar (y quien no)
5. Ruta de migracion
6. Prueba social de quienes cambiaron
7. CTA

---

### Formato 2: Alternativas a [Competidor] (Plural)

**Intencion de busqueda**: El usuario esta investigando opciones, en etapa temprana del recorrido

**Patron de URL**: `/alternatives/[competidor]-alternatives`

**Palabras clave objetivo**: "alternativas a [Competidor]", "mejores alternativas a [Competidor]", "herramientas como [Competidor]"

**Estructura de pagina**:
1. Por que las personas buscan alternativas (puntos de dolor comunes)
2. Que buscar en una alternativa (marco de criterios)
3. Lista de alternativas (usted primero, pero incluya opciones reales)
4. Tabla comparativa (resumen)
5. Desglose detallado de cada alternativa
6. Recomendacion por caso de uso
7. CTA

**Importante**: Incluya 4-7 alternativas reales. Ser genuinamente util genera confianza y posiciona mejor.

---

### Formato 3: Usted vs [Competidor]

**Intencion de busqueda**: El usuario lo esta comparando directamente con un competidor especifico

**Patron de URL**: `/vs/[competidor]` o `/compare/[usted]-vs-[competidor]`

**Palabras clave objetivo**: "[Usted] vs [Competidor]", "[Competidor] vs [Usted]"

**Estructura de pagina**:
1. Resumen TL;DR (diferencias clave en 2-3 oraciones)
2. Tabla comparativa de un vistazo
3. Comparacion detallada por categoria (Funciones, Precios, Soporte, Facilidad de uso, Integraciones)
4. Para quien es mejor [Usted]
5. Para quien es mejor [Competidor] (sea honesto)
6. Que dicen los clientes (testimonios de quienes cambiaron)
7. Soporte de migracion
8. CTA

---

### Formato 4: [Competidor A] vs [Competidor B]

**Intencion de busqueda**: Usuario comparando dos competidores (no a usted directamente)

**Patron de URL**: `/compare/[competidor-a]-vs-[competidor-b]`

**Estructura de pagina**:
1. Descripcion general de ambos productos
2. Comparacion por categoria
3. Para quien es mejor cada uno
4. La tercera opcion (presentarse usted)
5. Tabla comparativa (los tres)
6. CTA

**Por que funciona**: Captura trafico de busqueda para terminos de competidores, lo posiciona como conocedor.

---

## Secciones Esenciales

### Resumen TL;DR
Comience cada pagina con un resumen rapido para quienes escanean: diferencias clave en 2-3 oraciones.

### Comparaciones en Parrafo
Vaya mas alla de las tablas. Para cada dimension, escriba un parrafo explicando las diferencias y cuando importa cada una.

### Comparacion de Funciones
Para cada categoria: describa como cada uno lo maneja, liste fortalezas y limitaciones, de la recomendacion final.

### Comparacion de Precios
Incluya comparacion nivel por nivel, que esta incluido, costos ocultos y calculo del costo total para un tamano de equipo de muestra.

### Para Quien Es
Sea explicito sobre el cliente ideal para cada opcion. Las recomendaciones honestas generan confianza.

### Seccion de Migracion
Cubra que se transfiere, que necesita reconfiguracion, soporte ofrecido y citas de clientes que cambiaron.

**Para plantillas detalladas**: Consulte [references/templates.md](references/templates.md)

---

## Arquitectura de Contenido

### Datos Centralizados de Competidores
Cree una sola fuente de verdad para cada competidor con:
- Posicionamiento y audiencia objetivo
- Precios (todos los niveles)
- Calificaciones de funciones
- Fortalezas y debilidades
- Mejor para / no ideal para
- Quejas comunes (de resenas)
- Notas de migracion

**Para estructura de datos y ejemplos**: Consulte [references/content-architecture.md](references/content-architecture.md)

---

## Proceso de Investigacion

### Investigacion Profunda de Competidores

Para cada competidor, recopile:

1. **Investigacion de producto**: Registrese, uselo, documente funciones/UX/limitaciones
2. **Investigacion de precios**: Precios actuales, que esta incluido, costos ocultos
3. **Mineria de resenas**: G2, Capterra, TrustRadius para temas comunes de elogio/queja
4. **Retroalimentacion de clientes**: Hable con clientes que cambiaron (en ambas direcciones)
5. **Investigacion de contenido**: Su posicionamiento, sus paginas de comparacion, su registro de cambios

### Actualizaciones Continuas

- **Trimestral**: Verificar precios, comprobar cambios importantes de funciones
- **Cuando se notifique**: Un cliente menciona un cambio del competidor
- **Anualmente**: Actualizacion completa de todos los datos de competidores

---

## Consideraciones SEO

### Segmentacion de Palabras Clave

| Formato | Palabras Clave Principales |
|---------|---------------------------|
| Alternativa (singular) | alternativa a [Competidor], alternativa de [Competidor] |
| Alternativas (plural) | alternativas a [Competidor], mejores alternativas a [Competidor] |
| Usted vs Competidor | [Usted] vs [Competidor], [Competidor] vs [Usted] |
| Competidor vs Competidor | [A] vs [B], [B] vs [A] |

### Enlaces Internos
- Enlace entre paginas de competidores relacionadas
- Enlace desde paginas de funciones a comparaciones relevantes
- Crear pagina hub enlazando a todo el contenido de competidores

### Schema Markup
Considere schema de FAQ para preguntas comunes como "¿Cual es la mejor alternativa a [Competidor]?"

---

## Formato de Salida

### Archivo de Datos del Competidor
Perfil completo del competidor en formato YAML para uso en todas las paginas de comparacion.

### Contenido de Pagina
Para cada pagina: URL, meta tags, copia completa de pagina organizada por seccion, tablas comparativas, CTAs.

### Plan de Conjunto de Paginas
Paginas recomendadas a crear con orden de prioridad basado en volumen de busqueda.

---

## Preguntas Especificas de la Tarea

1. ¿Cuales son las razones comunes por las que las personas cambian a usted?
2. ¿Tiene citas de clientes sobre el cambio?
3. ¿Cuales son sus precios vs. los de competidores?
4. ¿Ofrece soporte de migracion?

---

## Habilidades Relacionadas

- **programmatic-seo**: Para construir paginas de competidores a escala
- **copywriting**: Para escribir textos de comparacion convincentes
- **seo-audit**: Para optimizar paginas de competidores
- **schema-markup**: Para schema de FAQ y comparaciones
