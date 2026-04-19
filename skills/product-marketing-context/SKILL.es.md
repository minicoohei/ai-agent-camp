---
name: product-marketing-context
version: 1.0.0
description: "Habilidad que crea y actualiza documentos de contexto de marketing de producto. Se activa con solicitudes como 'Crear contexto de marketing', 'Organizar posicionamiento', 'Resumir información del producto'."
triggers:
  - Crear contexto de marketing
  - Organizar posicionamiento
  - Resumir información del producto
  - Contexto de producto
  - Definir clientes objetivo
  - product-marketing-context
  - product context
---

# Contexto de marketing de producto

Usted ayuda a los usuarios a crear y mantener un documento de contexto de marketing de producto. Este captura información fundamental de posicionamiento y mensajes que otras habilidades de marketing referencian, para que los usuarios no se repitan.

El documento se almacena en `.claude/product-marketing-context.md`.

## Flujo de trabajo

### Paso 1: Verificar contexto existente

Primero, verifique si `.claude/product-marketing-context.md` ya existe.

**Si existe:**
- Léalo y resuma lo que está capturado
- Pregunte qué secciones desean actualizar
- Solo recopile información para esas secciones

**Si no existe, ofrezca dos opciones:**

1. **Auto-borrador desde el código fuente** (recomendado): Estudiará el repositorio — README, páginas de destino, textos de marketing, package.json, etc. — y redactará una V1 del documento de contexto. El usuario luego revisa, corrige y completa vacíos. Esto es más rápido que empezar desde cero.

2. **Empezar desde cero**: Recorrer cada sección conversacionalmente, recopilando información una sección a la vez.

La mayoría de los usuarios prefieren la opción 1. Después de presentar el borrador, pregunte: "¿Qué necesita corrección? ¿Qué falta?"

### Paso 2: Recopilar información

**Si se auto-redacta:**
1. Leer el código fuente: README, páginas de destino, textos de marketing, páginas "acerca de", meta descripciones, package.json, documentación existente
2. Redactar todas las secciones basándose en lo encontrado
3. Presentar el borrador y preguntar qué necesita corrección o qué falta
4. Iterar hasta que el usuario esté satisfecho

**Si se empieza desde cero:**
Recorra cada sección a continuación conversacionalmente, una a la vez. No presente todas las preguntas de una vez.

Para cada sección:
1. Explique brevemente qué está capturando
2. Haga preguntas relevantes
3. Confirme la precisión
4. Pase a la siguiente

**Importante:** Insista en obtener el lenguaje textual del cliente. Las frases exactas son más valiosas que las descripciones pulidas.

---

## Secciones a capturar

### 1. Descripción general del producto
- Descripción en una línea
- Qué hace (2-3 oraciones)
- Categoría del producto (en qué "estante" se encuentra — cómo los clientes lo buscan)
- Tipo de producto (SaaS, marketplace, e-commerce, servicio, etc.)
- Modelo de negocio y precios

### 2. Público objetivo
- Tipo de empresa objetivo (industria, tamaño, etapa)
- Tomadores de decisiones objetivo (roles, departamentos)
- Caso de uso principal (el problema principal que resuelve)
- Trabajos por realizar (2-3 cosas para las que los clientes lo "contratan")
- Casos de uso o escenarios específicos

### 3. Personas (solo B2B)
Si múltiples interesados participan en la compra, capture para cada uno:
- Usuario, Campeón, Tomador de decisiones, Comprador financiero, Influenciador técnico
- Qué le importa a cada uno, su desafío y el valor que les promete

### 4. Problemas y puntos de dolor
- Desafío principal que enfrentan los clientes antes de encontrarlo
- Por qué las soluciones actuales se quedan cortas
- Lo que les cuesta (tiempo, dinero, oportunidades)
- Tensión emocional (estrés, miedo, duda)

### 5. Panorama competitivo
- **Competidores directos**: Misma solución, mismo problema (ej., Calendly vs SavvyCal)
- **Competidores secundarios**: Diferente solución, mismo problema (ej., Calendly vs programación de Superhuman)
- **Competidores indirectos**: Enfoque conflictivo (ej., Calendly vs asistente personal)
- Cómo cada uno se queda corto para los clientes

### 6. Diferenciación
- Diferenciadores clave (capacidades que carecen las alternativas)
- Cómo lo resuelve de manera diferente
- Por qué es mejor (beneficios)
- Por qué los clientes lo eligen sobre las alternativas

### 7. Objeciones y anti-personas
- Las 3 principales objeciones escuchadas en ventas y cómo abordarlas
- Quién NO es un buen candidato (anti-persona)

### 8. Dinámicas de cambio
Las cuatro fuerzas de JTBD:
- **Empuje**: Qué frustraciones los alejan de la solución actual
- **Atracción**: Qué los atrae hacia usted
- **Hábito**: Qué los mantiene atascados con el enfoque actual
- **Ansiedad**: Qué les preocupa sobre cambiar

### 9. Lenguaje del cliente
- Cómo los clientes describen el problema (textual)
- Cómo describen su solución (textual)
- Palabras/frases a usar
- Palabras/frases a evitar
- Glosario de términos específicos del producto

### 10. Voz de marca
- Tono (profesional, casual, divertido, etc.)
- Estilo de comunicación (directo, conversacional, técnico)
- Personalidad de marca (3-5 adjetivos)

### 11. Puntos de prueba
- Métricas o resultados clave para citar
- Clientes/logos notables
- Fragmentos de testimonios
- Temas de valor principales y evidencia de respaldo

### 12. Objetivos
- Objetivo principal del negocio
- Acción de conversión clave (qué quiere que la gente haga)
- Métricas actuales (si se conocen)

---

## Paso 3: Crear el documento

Después de recopilar información, cree `.claude/product-marketing-context.md` con esta estructura:

```markdown
# Contexto de marketing de producto

*Última actualización: [fecha]*

## Descripción general del producto
**Una línea:**
**Qué hace:**
**Categoría del producto:**
**Tipo de producto:**
**Modelo de negocio:**

## Público objetivo
**Empresas objetivo:**
**Tomadores de decisiones:**
**Caso de uso principal:**
**Trabajos por realizar:**
-
**Casos de uso:**
-

## Personas
| Persona | Le importa | Desafío | Valor que prometemos |
|---------|-----------|---------|---------------------|
| | | | |

## Problemas y puntos de dolor
**Problema principal:**
**Por qué las alternativas se quedan cortas:**
-
**Lo que les cuesta:**
**Tensión emocional:**

## Panorama competitivo
**Directo:** [Competidor] — se queda corto porque...
**Secundario:** [Enfoque] — se queda corto porque...
**Indirecto:** [Alternativa] — se queda corto porque...

## Diferenciación
**Diferenciadores clave:**
-
**Cómo lo hacemos diferente:**
**Por qué es mejor:**
**Por qué los clientes nos eligen:**

## Objeciones
| Objeción | Respuesta |
|----------|----------|
| | |

**Anti-persona:**

## Dinámicas de cambio
**Empuje:**
**Atracción:**
**Hábito:**
**Ansiedad:**

## Lenguaje del cliente
**Cómo describen el problema:**
- "[textual]"
**Cómo nos describen:**
- "[textual]"
**Palabras a usar:**
**Palabras a evitar:**
**Glosario:**
| Término | Significado |
|---------|------------|
| | |

## Voz de marca
**Tono:**
**Estilo:**
**Personalidad:**

## Puntos de prueba
**Métricas:**
**Clientes:**
**Testimonios:**
> "[cita]" — [quién]
**Temas de valor:**
| Tema | Prueba |
|------|--------|
| | |

## Objetivos
**Objetivo del negocio:**
**Acción de conversión:**
**Métricas actuales:**
```

---

## Paso 4: Confirmar y guardar

- Mostrar el documento completado
- Preguntar si algo necesita ajuste
- Guardar en `.claude/product-marketing-context.md`
- Decirles: "Otras habilidades de marketing ahora usarán este contexto automáticamente. Ejecute `/product-marketing-context` en cualquier momento para actualizarlo."

---

## Consejos

- **Sea específico**: Pregunte "¿Cuál es la frustración #1 que los trae hacia usted?" no "¿Qué problema resuelven?"
- **Capture palabras exactas**: El lenguaje del cliente supera las descripciones pulidas
- **Pida ejemplos**: "¿Puede darme un ejemplo?" desbloquea mejores respuestas
- **Valide sobre la marcha**: Resuma cada sección y confirme antes de continuar
- **Omita lo que no aplica**: No todos los productos necesitan todas las secciones (ej., Personas para B2C)
