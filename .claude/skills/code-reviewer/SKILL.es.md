---
name: code-reviewer
description: "Habilidad automatizada de revision de codigo compatible con TypeScript, JavaScript, Python, Go, Swift y Kotlin. Analisis de complejidad/riesgo de PR, deteccion de violaciones SOLID y code smells, y generacion de informes de revision. Se activa con solicitudes como 'revisar codigo', 'analizar PR', 'verificar calidad de codigo', 'informe de revision', etc."
source: github.com/alirezarezvani/claude-skills@main
triggers:
  - code-reviewer
  - revision de codigo
  - analizar PR
  - verificar calidad de codigo
  - informe de revision
  - revision de pull request
  - code review
  - コードレビュー
---

# Revisor de Codigo

Herramientas automatizadas de revision de codigo para analizar pull requests, detectar problemas de calidad de codigo y generar informes de revision.

---

## Tabla de Contenidos

- [Herramientas](#herramientas)
  - [Analizador de PR](#analizador-de-pr)
  - [Verificador de Calidad de Codigo](#verificador-de-calidad-de-codigo)
  - [Generador de Informes de Revision](#generador-de-informes-de-revision)
- [Guias de Referencia](#guias-de-referencia)
- [Lenguajes Soportados](#lenguajes-soportados)

---

## Herramientas

### Analizador de PR

Analiza el diff de git entre ramas para evaluar la complejidad de revision e identificar riesgos.

```bash
# Analizar rama actual contra main
python scripts/pr_analyzer.py /ruta/al/repo

# Comparar ramas especificas
python scripts/pr_analyzer.py . --base main --head feature-branch

# Salida JSON para integracion
python scripts/pr_analyzer.py /ruta/al/repo --json
```

**Lo que detecta:**
- Secretos codificados (contrasenas, claves API, tokens)
- Patrones de inyeccion SQL (concatenacion de cadenas en consultas)
- Declaraciones de depuracion (debugger, console.log)
- Desactivacion de reglas ESLint
- Tipos `any` de TypeScript
- Comentarios TODO/FIXME

**La salida incluye:**
- Puntuacion de complejidad (1-10)
- Categorizacion de riesgo (critico, alto, medio, bajo)
- Priorizacion de archivos para orden de revision
- Validacion de mensajes de commit

---

### Verificador de Calidad de Codigo

Analiza el codigo fuente en busca de problemas estructurales, code smells y violaciones SOLID.

```bash
# Analizar un directorio
python scripts/code_quality_checker.py /ruta/al/codigo

# Analizar lenguaje especifico
python scripts/code_quality_checker.py . --language python

# Salida JSON
python scripts/code_quality_checker.py /ruta/al/codigo --json
```

**Lo que detecta:**
- Funciones largas (>50 lineas)
- Archivos grandes (>500 lineas)
- Clases dios (>20 metodos)
- Anidamiento profundo (>4 niveles)
- Demasiados parametros (>5)
- Alta complejidad ciclomatica
- Manejo de errores faltante
- Importaciones no utilizadas
- Numeros magicos

**Umbrales:**

| Problema | Umbral |
|----------|--------|
| Funcion larga | >50 lineas |
| Archivo grande | >500 lineas |
| Clase dios | >20 metodos |
| Demasiados parametros | >5 |
| Anidamiento profundo | >4 niveles |
| Alta complejidad | >10 ramas |

---

### Generador de Informes de Revision

Combina el analisis de PR y los hallazgos de calidad de codigo en informes de revision estructurados.

```bash
# Generar informe para el repo actual
python scripts/review_report_generator.py /ruta/al/repo

# Salida Markdown
python scripts/review_report_generator.py . --format markdown --output review.md

# Usar analisis pre-computados
python scripts/review_report_generator.py . \
  --pr-analysis pr_results.json \
  --quality-analysis quality_results.json
```

**El informe incluye:**
- Veredicto de revision (aprobar, solicitar cambios, bloquear)
- Puntuacion (0-100)
- Elementos de accion priorizados
- Resumen de problemas por severidad
- Orden de revision sugerido

**Veredictos:**

| Puntuacion | Veredicto |
|------------|-----------|
| 90+ sin problemas altos | Aprobar |
| 75+ con ≤2 problemas altos | Aprobar con sugerencias |
| 50-74 | Solicitar cambios |
| <50 o problemas criticos | Bloquear |

---

## Guias de Referencia

### Lista de Verificacion de Revision de Codigo
`references/code_review_checklist.md`

Listas de verificacion sistematicas que cubren:
- Verificaciones previas a la revision (compilacion, pruebas, higiene del PR)
- Correccion (logica, manejo de datos, manejo de errores)
- Seguridad (validacion de entrada, prevencion de inyeccion)
- Rendimiento (eficiencia, cache, escalabilidad)
- Mantenibilidad (calidad de codigo, nomenclatura, estructura)
- Pruebas (cobertura, calidad, mocking)
- Verificaciones especificas por lenguaje

### Estandares de Codificacion
`references/coding_standards.md`

Estandares especificos por lenguaje para:
- TypeScript (anotaciones de tipo, seguridad null, async/await)
- JavaScript (declaraciones, patrones, modulos)
- Python (type hints, excepciones, diseno de clases)
- Go (manejo de errores, structs, concurrencia)
- Swift (opcionales, protocolos, errores)
- Kotlin (seguridad null, data classes, coroutines)

### Antipatrones Comunes
`references/common_antipatterns.md`

Catalogo de antipatrones con ejemplos y soluciones:
- Estructurales (clase dios, metodo largo, anidamiento profundo)
- Logica (ceguera booleana, codigo basado en cadenas)
- Seguridad (inyeccion SQL, credenciales codificadas)
- Rendimiento (consultas N+1, colecciones sin limite)
- Pruebas (duplicacion, probar implementacion)
- Asincrono (promesas flotantes, callback hell)

---

## Lenguajes Soportados

| Lenguaje | Extensiones |
|----------|-------------|
| Python | `.py` |
| TypeScript | `.ts`, `.tsx` |
| JavaScript | `.js`, `.jsx`, `.mjs` |
| Go | `.go` |
| Swift | `.swift` |
| Kotlin | `.kt`, `.kts` |
