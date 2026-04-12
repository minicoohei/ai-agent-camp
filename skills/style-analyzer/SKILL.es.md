---
name: style-analyzer
description: "Lee múltiples textos existentes del usuario, extrae características del estilo de escritura (patrones de terminación de oraciones, longitud de oraciones, ratio kanji/hiragana, tono, tendencias de conjunciones) y genera un perfil de estilo. Se activa con solicitudes como 'Analizar estilo de escritura', 'Imitar esta escritura', 'Aprender estilo de escritura', etc."
triggers:
  - Analizar estilo de escritura
  - Aprender estilo de escritura
  - Imitar esta escritura
  - Extraer estilo de escritura
  - Análisis de tono
  - style-analyzer
  - style profile
---

## Palabras de Activación
"Análisis de estilo", "Análisis de tono", "Estilo de escritura", "Estilo de texto"

# Analizador de Estilo - Análisis de Estilo de Escritura y Generación de Perfil

Lee múltiples archivos de texto escritos por el usuario, extrae cuantitativamente las características del estilo de escritura y genera un perfil de estilo (formato YAML). El perfil generado puede utilizarse para reproducir el estilo de escritura en la generación de texto o para verificar la consistencia del estilo.

## Funcionalidades

1. **Análisis de patrones de terminación de oraciones**: Determina forma cortés (desu/masu), forma llana (da/dearu) o mixta
2. **Análisis de longitud de oraciones**: Promedio, mínimo y máximo de caracteres por oración
3. **Ratio de tipos de caracteres**: Ratio de aparición de kanji, hiragana, katakana, ASCII y símbolos
4. **Análisis de conjunciones**: Contabiliza tipos y frecuencias de conjunciones utilizadas
5. **Estructura de párrafos**: Calcula el número promedio de oraciones por párrafo
6. **Detección de terminación nominal**: Mide la frecuencia de oraciones que terminan con sustantivos
7. **Patrones de puntuación**: Determina el uso de puntuación de ancho completo/medio
8. **Análisis de modificadores**: Estima la densidad de modificadores y adverbios
9. **Balance coloquial/formal**: Estima el ratio de expresiones coloquiales vs. literarias

## Uso

```bash
# Uso básico (especificar múltiples archivos)
python scripts/style_analyzer.py --input "article1.md" --input "article2.md"

# Especificar destino de salida
python scripts/style_analyzer.py --input "article1.md" --input "article2.md" --output style_profile.yaml

# Analizar 3+ archivos
python scripts/style_analyzer.py \
  --input "blog_post_1.md" \
  --input "blog_post_2.md" \
  --input "report.txt" \
  --output my_style.yaml

# Modo de prueba (generar perfil de muestra)
python scripts/style_analyzer.py --test
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| --input | Sí* | - | Ruta al archivo de texto/Markdown para análisis (múltiples permitidos) |
| --output | No | output/style_profile.yaml | Ruta del archivo YAML de salida |
| --test | No | false | Modo de prueba: genera perfil de muestra y sale |

\* `--input` no es requerido cuando se usa `--test`

## Elementos de Análisis

### Patrones de Terminación de Oraciones (sentence_endings)

| Clasificación | Patrones Correspondientes | Ejemplo |
|---------------|---------------------------|---------|
| desu_masu | desu, masu, deshita, mashita, masen, deshou | Forma cortés |
| da_dearu | da, dearu, deatta, datta, dewanai | Forma llana/académica |
| other | Interrogativo, exclamatorio, terminación nominal, etc. | Preguntas, énfasis |

### Ratio de Tipos de Caracteres (char_ratios)

Ratio de cada tipo de carácter calculado según rangos Unicode:

- **Kanji**: U+4E00 - U+9FFF, U+3400 - U+4DBF
- **Hiragana**: U+3040 - U+309F
- **Katakana**: U+30A0 - U+30FF
- **ASCII**: U+0020 - U+007E
- **Otros**: Todo lo demás (símbolos, emoji, etc.)

### Conjunciones (conjunctions)

Principales conjunciones detectadas:

| Categoría | Conjunciones |
|-----------|-------------|
| Consecutivas | dakara, shitagatte, sonotame, sorede, yueni |
| Adversativas | shikashi, daga, tokoroga, keredomo, nimokakawarazu, ippode |
| Paralelas/Aditivas | mata, sarani, soshite, kuwaete, soreni, sonoueni |
| Explicativas/Suplementarias | tsumari, sunawachi, yousuruni, nazenara, toiunomo |
| Transitivas | sate, tokorode, dewa, soredewa, chinamini |
| Contrastivas | mushiro, gyakuni, hantaini, sorenishite |
| Ejemplificadoras | tatoeba, gutaitekiniwa, iwaba |

### Terminación Nominal (taigen_dome)

Detecta patrones donde las oraciones terminan con un sustantivo o frase nominal.

### Patrones de Puntuación (punctuation)

| Nombre del Patrón | Punto | Coma |
|-------------------|-------|------|
| standard | Punto japonés | Coma japonesa |
| academic | Punto de ancho completo | Coma de ancho completo |
| mixed | Mixto | Mixto |

## Formato de Salida

Perfil de estilo en formato YAML:

```yaml
style_profile:
  generated_at: "2026-02-12T10:30:00+09:00"
  source_files:
    - path: "article1.md"
      chars: 2450
    - path: "article2.md"
      chars: 3120
  total_chars: 5570
  total_sentences: 142
  total_paragraphs: 28

  sentence_endings:
    desu_masu: 0.72
    da_dearu: 0.18
    other: 0.10
    dominant_style: "desu_masu"

  sentence_length:
    average: 39.2
    median: 35.0
    min: 8
    max: 98
    std_dev: 15.4

  char_ratios:
    kanji: 0.31
    hiragana: 0.48
    katakana: 0.08
    ascii: 0.06
    other: 0.07

  conjunctions:
    total_count: 34
    per_sentence: 0.24
    top_5:
      - word: "mata"
        count: 8
      - word: "shikashi"
        count: 6
      - word: "soshite"
        count: 5
      - word: "sarani"
        count: 4
      - word: "tsumari"
        count: 3

  paragraph_structure:
    avg_sentences_per_paragraph: 5.1

  taigen_dome:
    frequency: 0.07
    count: 10

  punctuation:
    period_style: "Punto japonés"
    comma_style: "Coma japonesa"
    pattern: "standard"

  modifiers:
    density: 0.12
    common_adverbs:
      - "hijou-ni (muy)"
      - "tokuni (especialmente)"
      - "jissaini (en realidad)"

  colloquial_formal_balance:
    colloquial_ratio: 0.25
    formal_ratio: 0.75
    assessment: "Ligeramente inclinado hacia lo literario"
```

## Ejemplos

### Análisis de Estilo de Artículos de Blog

```bash
python scripts/style_analyzer.py \
  --input "blog/2026-01-intro.md" \
  --input "blog/2026-01-review.md" \
  --input "blog/2026-02-tips.md" \
  --output output/blog_style.yaml
```

Ejemplo de salida (stdout):

```
=== Analizador de Estilo - Informe de Estilo de Escritura ===

Archivos analizados: 3
Total de caracteres: 8,420
Total de oraciones: 215

--- Patrones de Terminación de Oraciones ---
  Forma cortés (desu/masu): 78.1%
  Forma llana (da/dearu): 12.6%
  Otros: 9.3%
  -> Estilo dominante: Forma cortés (desu/masu)

--- Longitud de Oraciones ---
  Promedio: 39.2 caracteres  Mediana: 35.0 caracteres
  Mín: 5 caracteres  Máx: 102 caracteres

--- Ratio de Tipos de Caracteres ---
  Kanji: 30.5%  Hiragana: 48.2%  Katakana: 8.1%

--- Top 5 Conjunciones ---
  mata(12) shikashi(8) soshite(7) sarani(5) tsumari(4)

--- Terminación Nominal ---
  Tasa de uso: 6.5% (14/215 oraciones)

Perfil guardado en: output/blog_style.yaml
```

### Modo de Prueba

```bash
python scripts/style_analyzer.py --test
```

Genera un perfil de muestra sin archivos de entrada para confirmar el formato de salida.

## Requisitos

- Python 3.8+
- No se requieren bibliotecas externas (funciona solo con la biblioteca estándar)

## Habilidades Relacionadas

- **article-writer**: Carga el perfil de estilo para generar artículos reproduciendo el estilo de escritura
- **copy-editing**: Utiliza el perfil para verificaciones de consistencia de estilo y corrección
