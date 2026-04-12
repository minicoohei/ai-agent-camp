---
name: proofreading-agent
description: "Agente de corrección de artículos en japonés. Verifica errores tipográficos, gramática, consistencia de expresiones y legibilidad, generando sugerencias de corrección como anotaciones en línea. Se activa con solicitudes como 'Corregir esto', 'Verificar el texto', 'Buscar errores tipográficos', 'Revisar el artículo'."
triggers:
  - Corregir esto
  - Verificar el texto
  - Buscar errores tipográficos
  - Revisar el artículo
  - Pulir la redacción
  - Editar el texto
  - proofreading-agent
---

## Palabras clave de activación
"Corregir", "Verificar texto", "Errores tipográficos", "Pulir", "Editar"

# Proofreading Agent - Agente de corrección de artículos en japonés

Un agente que corrige sistemáticamente artículos en japonés. Inspirado en la metodología de edición de copia "Seven Sweeps", utiliza **Five Sweeps** (cinco pasadas) optimizadas para contenido en japonés para revisar artículos desde múltiples ángulos.

## Five Sweeps (5 pasadas de corrección)

La corrección se realiza en las siguientes 5 etapas. Cada pasada puede ejecutarse de forma independiente, permitiendo una revisión enfocada en categorías específicas.

### 1. Verificación de precisión (Accuracy)

Detecta errores a nivel de caracteres.

- **Errores tipográficos**: Errores de conversión de kanji, errores de escritura
- **Errores de okurigana**: Sufijos de inflexión incorrectos en verbos/adjetivos
- **Uso incorrecto de homófonos**: Confusión entre palabras que suenan igual
- **Errores en nombres propios**: Precisión de nombres de productos, personas, organizaciones

### 2. Verificación gramatical (Grammar)

Verifica la corrección gramatical.

- **Discordancia sujeto-predicado**: Desacuerdo entre sujeto y predicado
- **Uso incorrecto de partículas**: Uso incorrecto de partículas japonesas
- **Consistencia de honoríficos**: Mezcla de diferentes niveles de cortesía
- **Errores de relación modificador-modificado**: Problemas con conexiones de palabras modificadoras
- **Inconsistencia de tiempo verbal**: Mezcla de tiempo pasado y presente

### 3. Verificación de consistencia (Consistency)

Confirma la consistencia de notación a lo largo del artículo.

- **Variaciones de notación**: Ortografía inconsistente de la misma palabra
- **Consistencia de finales de oración**: Mezcla de estilos formales e informales
- **Notación de números**: Mezcla de caracteres de ancho completo y medio
- **Consistencia de símbolos**: Tipos de paréntesis, puntuación
- **Consistencia de abreviaturas**: Escritura completa en el primer uso

### 4. Verificación de legibilidad (Readability)

Evalúa la legibilidad del texto.

- **Longitud de oraciones**: Detección de oraciones que superan 80 caracteres
- **Kanji difícil**: Uso de kanji difícil para lectores generales
- **Expresiones redundantes**: Simplificación de frases verbosas
- **Dobles negaciones**: Simplificación de construcciones de doble negación
- **Uso excesivo de voz pasiva**: Sugerencias para reescribir en voz activa
- **Exceso de katakana**: Señalamiento donde equivalentes japoneses son suficientes

### 5. Verificación de estructura (Structure)

Revisa la estructura general del artículo y el flujo lógico.

- **Conexiones lógicas entre párrafos**: Conexiones entre párrafos anteriores y siguientes
- **Contenido duplicado**: Repetición innecesaria de la misma información
- **Vacíos de información**: Explicaciones insuficientes, información innecesaria
- **Jerarquía de encabezados**: Adecuación de los niveles de encabezado
- **Alineación introducción-conclusión**: Correspondencia entre el planteamiento del problema inicial y la conclusión

## Uso

```bash
# Corrección completa con todas las pasadas (por defecto)
python scripts/proofreading_agent.py --input article.md --output review.md

# Ejecutar solo pasadas específicas
python scripts/proofreading_agent.py --input article.md --sweep accuracy
python scripts/proofreading_agent.py --input article.md --sweep grammar
python scripts/proofreading_agent.py --input article.md --sweep consistency
python scripts/proofreading_agent.py --input article.md --sweep readability
python scripts/proofreading_agent.py --input article.md --sweep structure

# Especificar perfil de estilo
python scripts/proofreading_agent.py --input article.md --style style_profile.yaml

# Filtro de severidad (mostrar solo alta)
python scripts/proofreading_agent.py --input article.md --severity high

# Modo de prueba (sin API necesaria, se ejecuta con texto de ejemplo)
python scripts/proofreading_agent.py --test
```

## Parámetros

| Parámetro | Requerido | Por defecto | Descripción |
|-----------|-----------|-------------|-------------|
| --input | Sí* | - | Ruta del archivo a corregir (Markdown/texto). No requerido en modo --test |
| --output | No | output/review_{timestamp}.md | Destino de salida de resultados de corrección |
| --sweep | No | all | Pasada a ejecutar: all, accuracy, grammar, consistency, readability, structure |
| --style | No | - | Ruta del perfil de estilo (YAML) |
| --severity | No | medium | Severidad mínima a mostrar: low, medium, high |
| --test | No | false | Modo de prueba (verificación con texto de ejemplo sin API) |

## Perfil de estilo (YAML)

Personalice reglas según el tipo de artículo.

```yaml
# Ejemplo de style_profile.yaml
name: "Blog técnico"
tone: "desu/masu"  # Estilo formal japonés
terminology:
  preferred:
    - { term: "servidor", reject: ["svr"] }
    - { term: "usuario", reject: ["usr"] }
    - { term: "interfaz", reject: ["i/f"] }
  domain_terms:
    - "API"
    - "SDK"
    - "CI/CD"
rules:
  max_sentence_length: 80
  number_style: "medio ancho"
  punctuation: "coma-punto"
```

## Formato de salida

### Anotaciones en línea

Las anotaciones se insertan directamente en las ubicaciones relevantes del texto original.

```markdown
Esto se ejecuta en un svr[Corrección: "svr" → "servidor" (Razón: Variación de notación. "servidor" es la notación principal en este artículo)]. Los datos se pueden guardar usando la función de guardado[Corrección: "se pueden guardar usando la función de guardado" → "se pueden guardar" (Razón: Expresión redundante)].
```

### Informe de resumen

Se generan estadísticas al final de los resultados de corrección.

```markdown
---
## Resumen de corrección

### Conteo de detecciones
| Categoría | Cantidad |
|-----------|----------|
| Precisión (errores tipográficos) | 3 |
| Gramática | 2 |
| Consistencia (variaciones de notación) | 5 |
| Legibilidad | 4 |
| Estructura | 1 |
| **Total** | **15** |

### Puntuación de legibilidad: 72/100
- Longitud promedio de oración: 42 caracteres (apropiada)
- Proporción de kanji difícil: 3% (ligeramente alta)
- Expresiones redundantes: 4 ubicaciones

### Por severidad
| Severidad | Cantidad |
|-----------|----------|
| ALTA | 3 |
| MEDIA | 8 |
| BAJA | 4 |

### Top 5 correcciones críticas
1. [ALTA] L12: Uso incorrecto de homófonos
2. [ALTA] L34: Sujeto y predicado no concuerdan
3. [ALTA] L56: Variación de notación (5 instancias)
4. [MEDIA] L23: La oración supera los 120 caracteres
5. [MEDIA] L45: Expresión redundante
```

## Cálculo de la puntuación de legibilidad

La puntuación de legibilidad (0-100) se calcula a partir de los siguientes elementos.

| Elemento | Puntos | Criterios |
|----------|--------|-----------|
| Longitud promedio de oración | 30 pts | 40 caracteres o menos: 30, 60 o menos: 20, 80 o menos: 10, superior: 0 |
| Proporción de kanji | 20 pts | 20-35%: 20, 35-45%: 15, otro: 10 |
| Tasa de redundancia | 20 pts | 0%: 20, reducida proporcionalmente |
| Adecuación de párrafos | 15 pts | 3-5 oraciones por párrafo: 15, otro: reducido |
| Adecuación de conjunciones | 15 pts | Conexiones claras entre párrafos: 15 |

## Requisitos

- **Clave de API**: GEMINI_API_KEY o GOOGLE_API_KEY (variable de entorno o .env)
- **Paquetes de Python**: google-genai, pyyaml, python-dotenv

## Habilidades relacionadas

- **document-processor**: Procesamiento integrado de PDF/PPTX/Excel
- **pptx-analyzer**: Análisis de estructura de diapositivas PowerPoint
- **screenshot-analyzer**: Extracción de información desde capturas de pantalla
