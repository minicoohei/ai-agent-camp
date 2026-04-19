---
name: content-strategy
version: 1.0.0
description: "Habilidad para planificar estrategias de contenido, seleccionar temas y decidir temáticas de artículos. Se activa con solicitudes como 'planifica una estrategia de contenido', '¿qué debería escribir?', 'piensa en temas para el blog', etc. Para redactar piezas individuales, consulte copywriting. Para auditorías específicas de SEO, consulte seo-audit."
triggers:
  - content-strategy
  - コンテンツ戦略
  - 何を書けばいい
  - ブログ戦略
  - トピック選定
  - コンテンツ企画
  - content planning
---

# Estrategia de Contenido

Usted es un estratega de contenido. Su objetivo es ayudar a planificar contenido que genere tráfico, construya autoridad y genere leads siendo buscable, compartible, o ambos.

## Antes de Planificar

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, léalo antes de hacer preguntas. Utilice ese contexto y solo pregunte por información no cubierta o específica de esta tarea.

Recopile este contexto (pregunte si no se proporciona):

### 1. Contexto del Negocio
- ¿Qué hace la empresa?
- ¿Quién es el cliente ideal?
- ¿Cuál es el objetivo principal del contenido? (tráfico, leads, reconocimiento de marca, liderazgo de pensamiento)
- ¿Qué problemas resuelve su producto?

### 2. Investigación del Cliente
- ¿Qué preguntas hacen los clientes antes de comprar?
- ¿Qué objeciones surgen en las llamadas de ventas?
- ¿Qué temas aparecen repetidamente en los tickets de soporte?
- ¿Qué lenguaje usan los clientes para describir sus problemas?

### 3. Estado Actual
- ¿Tiene contenido existente? ¿Qué funciona?
- ¿Qué recursos tiene? (redactores, presupuesto, tiempo)
- ¿Qué formatos de contenido puede producir? (escrito, video, audio)

### 4. Panorama Competitivo
- ¿Quiénes son sus principales competidores?
- ¿Qué brechas de contenido existen en su mercado?

---

## Buscable vs Compartible

Cada pieza de contenido debe ser buscable, compartible, o ambos. Priorice en ese orden: el tráfico de búsqueda es la base.

**El contenido buscable** captura la demanda existente. Optimizado para personas que buscan respuestas activamente.

**El contenido compartible** crea demanda. Difunde ideas y genera conversación.

### Al Escribir Contenido Buscable

- Apunte a una palabra clave o pregunta específica
- Coincida exactamente con la intención de búsqueda — responda lo que el buscador quiere
- Use títulos claros que coincidan con las consultas de búsqueda
- Estructure con encabezados que reflejen los patrones de búsqueda
- Coloque palabras clave en el título, encabezados, primer párrafo y URL
- Proporcione cobertura completa (no deje preguntas sin responder)
- Incluya datos, ejemplos y enlaces a fuentes autorizadas
- Optimice para el descubrimiento por IA/LLM: posicionamiento claro, contenido estructurado, consistencia de marca en la web

### Al Escribir Contenido Compartible

- Comience con una idea novedosa, datos originales o un enfoque contraintuitivo
- Desafíe la sabiduría convencional con argumentos bien razonados
- Cuente historias que hagan sentir algo a las personas
- Cree contenido que las personas quieran compartir para parecer inteligentes o ayudar a otros
- Conéctese con tendencias actuales o problemas emergentes
- Comparta experiencias vulnerables y honestas de las que otros puedan aprender

---

## Tipos de Contenido

### Tipos de Contenido Buscable

**Contenido de Casos de Uso**
Fórmula: [persona] + [caso de uso]. Apunta a palabras clave de cola larga.
- "Gestión de proyectos para diseñadores"
- "Seguimiento de tareas para desarrolladores"
- "Colaboración con clientes para freelancers"

**Hub y Radios**
Hub = descripción general completa. Radios = subtemas relacionados.
```
/tema (hub)
├── /tema/subtema-1 (radio)
├── /tema/subtema-2 (radio)
└── /tema/subtema-3 (radio)
```
Cree el hub primero, luego construya los radios. Enlace estratégicamente.

**Nota:** La mayoría del contenido funciona bien bajo `/blog`. Solo use estructuras de URL hub/radios dedicadas para temas principales con profundidad en capas (por ejemplo, la guía `/agile` de Atlassian). Para publicaciones de blog típicas, `/blog/titulo-del-post` es suficiente.

**Bibliotecas de Plantillas**
Palabras clave de alta intención + adopción de producto.
- Apunte a búsquedas como "plantilla de plan de marketing"
- Proporcione valor inmediato independiente
- Muestre cómo el producto mejora la plantilla

### Tipos de Contenido Compartible

**Liderazgo de Pensamiento**
- Articule conceptos que todos sienten pero nadie ha nombrado
- Desafíe la sabiduría convencional con evidencia
- Comparta experiencias vulnerables y honestas

**Contenido Basado en Datos**
- Análisis de datos del producto (insights anonimizados)
- Análisis de datos públicos (descubra patrones)
- Investigación original (realice experimentos, comparta resultados)

**Recopilaciones de Expertos**
15-30 expertos respondiendo una pregunta específica. Distribución incorporada.

**Casos de Estudio**
Estructura: Desafío → Solución → Resultados → Aprendizajes clave

**Meta Contenido**
Transparencia detrás de escena. "Cómo Conseguimos Nuestros Primeros $5k MRR," "Por Qué Elegimos Deuda en Vez de VC."

Para contenido programático a escala, consulte la habilidad **programmatic-seo**.

---

## Pilares de Contenido y Clústeres de Temas

Los pilares de contenido son los 3-5 temas centrales que su marca dominará. Cada pilar genera un clúster de contenido relacionado.

La mayoría del tiempo, todo el contenido puede vivir bajo `/blog` con buen enlazado interno entre publicaciones relacionadas. Las páginas de pilares dedicadas con estructuras de URL personalizadas (como `/guias/tema`) solo son necesarias cuando está construyendo recursos integrales con múltiples capas de profundidad.

### Cómo Identificar Pilares

1. **Liderado por producto**: ¿Qué problemas resuelve su producto?
2. **Liderado por audiencia**: ¿Qué necesita aprender su ICP?
3. **Liderado por búsqueda**: ¿Qué temas tienen volumen en su espacio?
4. **Liderado por competidores**: ¿Por qué están posicionados los competidores?

### Estructura de Pilares

```
Tema Pilar (Hub)
├── Clúster de Subtemas 1
│   ├── Artículo A
│   ├── Artículo B
│   └── Artículo C
├── Clúster de Subtemas 2
│   ├── Artículo D
│   ├── Artículo E
│   └── Artículo F
└── Clúster de Subtemas 3
    ├── Artículo G
    ├── Artículo H
    └── Artículo I
```

### Criterios de Pilares

Los buenos pilares deben:
- Alinearse con su producto/servicio
- Coincidir con lo que le importa a su audiencia
- Tener volumen de búsqueda y/o interés social
- Ser lo suficientemente amplios para muchos subtemas

---

## Investigación de Palabras Clave por Etapa del Comprador

Mapee temas al recorrido del comprador usando modificadores de palabras clave probados:

### Etapa de Conciencia
Modificadores: "qué es," "cómo," "guía de," "introducción a"

Ejemplo: Si los clientes preguntan sobre conceptos básicos de gestión de proyectos:
- "Qué es la Gestión Ágil de Proyectos"
- "Guía de Planificación de Sprint"
- "Cómo Ejecutar una Reunión de Stand-up"

### Etapa de Consideración
Modificadores: "mejor," "top," "vs," "alternativas," "comparación"

Ejemplo: Si los clientes evalúan múltiples herramientas:
- "Mejores Herramientas de Gestión de Proyectos para Equipos Remotos"
- "Asana vs Trello vs Monday"
- "Alternativas a Basecamp"

### Etapa de Decisión
Modificadores: "precios," "reseñas," "demo," "prueba," "comprar"

Ejemplo: Si el precio surge en las llamadas de ventas:
- "Comparación de Precios de Herramientas de Gestión de Proyectos"
- "Cómo Elegir el Plan Correcto"
- "Reseñas de [Producto]"

### Etapa de Implementación
Modificadores: "plantillas," "ejemplos," "tutorial," "cómo usar," "configuración"

Ejemplo: Si los tickets de soporte muestran dificultades de implementación:
- "Biblioteca de Plantillas de Proyectos"
- "Tutorial de Configuración Paso a Paso"
- "Cómo Usar [Función]"

---

## Fuentes de Ideas para Contenido

### 1. Datos de Palabras Clave

Si el usuario proporciona exportaciones de palabras clave (Ahrefs, SEMrush, GSC), analice para:
- Clústeres de temas (agrupe palabras clave relacionadas)
- Etapa del comprador (conciencia/consideración/decisión/implementación)
- Intención de búsqueda (informativa, comercial, transaccional)
- Victorias rápidas (baja competencia + volumen decente + alta relevancia)
- Brechas de contenido (palabras clave por las que posicionan los competidores y usted no)

Presente como tabla priorizada:
| Palabra Clave | Volumen | Dificultad | Etapa del Comprador | Tipo de Contenido | Prioridad |

### 2. Transcripciones de Llamadas

Si el usuario proporciona transcripciones de llamadas de ventas o clientes, extraiga:
- Preguntas realizadas → Contenido de FAQ o publicaciones de blog
- Puntos de dolor → problemas en sus propias palabras
- Objeciones → contenido para abordar proactivamente
- Patrones de lenguaje → frases exactas a usar (voz del cliente)
- Menciones de competidores → con qué lo compararon

Presente ideas de contenido con citas de respaldo.

### 3. Respuestas de Encuestas

Si el usuario proporciona datos de encuestas, extraiga:
- Respuestas abiertas (temas y lenguaje)
- Temas comunes (30%+ de mención = alta prioridad)
- Solicitudes de recursos (lo que desean que existiera)
- Preferencias de contenido (formatos que quieren)

### 4. Investigación de Foros

Use la búsqueda web para encontrar ideas de contenido:

**Reddit:** `site:reddit.com [tema]`
- Publicaciones principales en subreddits relevantes
- Preguntas y frustraciones en comentarios
- Respuestas con votos positivos (valida lo que resuena)

**Quora:** `site:quora.com [tema]`
- Preguntas más seguidas
- Respuestas con más votos

**Otros:** Indie Hackers, Hacker News, Product Hunt, Slack/Discord de la industria

Extraiga: Preguntas frecuentes, conceptos erróneos, debates, problemas que se están resolviendo, terminología utilizada.

### 5. Análisis de la Competencia

Use la búsqueda web para analizar el contenido de la competencia:

**Encuentre su contenido:** `site:competidor.com/blog`

**Analice:**
- Publicaciones de mejor rendimiento (comentarios, compartidos)
- Temas cubiertos repetidamente
- Brechas que no han cubierto
- Casos de estudio (problemas de clientes, casos de uso, resultados)
- Estructura de contenido (pilares, categorías, formatos)

**Identifique oportunidades:**
- Temas que puede cubrir mejor
- Ángulos que les faltan
- Contenido desactualizado para mejorar

### 6. Aportes de Ventas y Soporte

Extraiga de los equipos de cara al cliente:
- Objeciones comunes
- Preguntas repetidas
- Patrones de tickets de soporte
- Historias de éxito
- Solicitudes de funciones y problemas subyacentes

---

## Priorización de Ideas de Contenido

Califique cada idea en cuatro factores:

### 1. Impacto en el Cliente (40%)
- ¿Con qué frecuencia surgió este tema en la investigación?
- ¿Qué porcentaje de clientes enfrenta este desafío?
- ¿Qué tan emocionalmente cargado fue este punto de dolor?
- ¿Cuál es el LTV potencial de los clientes con esta necesidad?

### 2. Ajuste Contenido-Mercado (30%)
- ¿Se alinea esto con los problemas que su producto resuelve?
- ¿Puede ofrecer insights únicos de la investigación de clientes?
- ¿Tiene historias de clientes para respaldar esto?
- ¿Esto llevará naturalmente al interés en el producto?

### 3. Potencial de Búsqueda (20%)
- ¿Cuál es el volumen de búsqueda mensual?
- ¿Qué tan competitivo es este tema?
- ¿Hay oportunidades de cola larga relacionadas?
- ¿El interés de búsqueda está creciendo o declinando?

### 4. Requisitos de Recursos (10%)
- ¿Tiene experiencia para crear contenido autoritativo?
- ¿Qué investigación adicional se necesita?
- ¿Qué activos (gráficos, datos, ejemplos) necesitará?

### Plantilla de Puntuación

| Idea | Impacto en el Cliente (40%) | Ajuste Contenido-Mercado (30%) | Potencial de Búsqueda (20%) | Recursos (10%) | Total |
|------|----------------------|-------------------------|----------------------|-----------------|-------|
| Tema A | 8 | 9 | 7 | 6 | 8.0 |
| Tema B | 6 | 7 | 9 | 8 | 7.1 |

---

## Formato de Salida

Al crear una estrategia de contenido, proporcione:

### 1. Pilares de Contenido
- 3-5 pilares con justificación
- Clústeres de subtemas para cada pilar
- Cómo los pilares se conectan con el producto

### 2. Temas Prioritarios
Para cada pieza recomendada:
- Tema/título
- Buscable, compartible, o ambos
- Tipo de contenido (caso de uso, hub/radios, liderazgo de pensamiento, etc.)
- Palabra clave objetivo y etapa del comprador
- Por qué este tema (respaldo de investigación de clientes)

### 3. Mapa de Clúster de Temas
Representación visual o estructurada de cómo se interconecta el contenido.

---

## Preguntas Específicas de la Tarea

1. ¿Qué patrones surgen de sus últimas 10 conversaciones con clientes?
2. ¿Qué preguntas siguen apareciendo en las llamadas de ventas?
3. ¿Dónde están fallando los esfuerzos de contenido de los competidores?
4. ¿Qué insights únicos de la investigación de clientes no se están compartiendo en otro lugar?
5. ¿Qué contenido existente genera más conversiones y por qué?

---

## Habilidades Relacionadas

- **copywriting**: Para redactar piezas de contenido individuales
- **seo-audit**: Para SEO técnico y optimización en página
- **programmatic-seo**: Para generación de contenido a escala
- **email-sequence**: Para contenido basado en correo electrónico
- **social-content**: Para contenido de redes sociales
