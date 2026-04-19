---
name: tdd-guide
description: Flujo de trabajo de desarrollo guiado por pruebas con generación de pruebas, análisis de cobertura y soporte para múltiples frameworks
triggers:
  - generar pruebas
  - analizar cobertura
  - flujo de trabajo TDD
  - rojo verde refactorizar
  - Jest tests
  - Pytest tests
  - JUnit tests
  - informe de cobertura
source: github.com/alirezarezvani/claude-skills@main
---

# Guía TDD

Habilidad de desarrollo guiado por pruebas para generar pruebas, analizar cobertura y guiar flujos de trabajo rojo-verde-refactorizar en Jest, Pytest, JUnit y Vitest.

## Tabla de Contenidos

- [Capacidades](#capacidades)
- [Flujos de Trabajo](#flujos-de-trabajo)
- [Herramientas](#herramientas)
- [Requisitos de Entrada](#requisitos-de-entrada)
- [Limitaciones](#limitaciones)

---

## Capacidades

| Capacidad | Descripción |
|-----------|-------------|
| Generación de Pruebas | Convertir requisitos o código en casos de prueba con estructura adecuada |
| Análisis de Cobertura | Analizar informes LCOV/JSON/XML, identificar brechas, priorizar correcciones |
| Flujo de Trabajo TDD | Guiar ciclos rojo-verde-refactorizar con validación |
| Adaptadores de Framework | Generar pruebas para Jest, Pytest, JUnit, Vitest, Mocha |
| Puntuación de Calidad | Evaluar aislamiento de pruebas, aserciones, nomenclatura, detectar olores de prueba |
| Generación de Fixtures | Crear datos de prueba realistas, mocks y fábricas |

---

## Flujos de Trabajo

### Generar Pruebas desde Código

1. Proporcionar código fuente (TypeScript, JavaScript, Python, Java)
2. Especificar framework objetivo (Jest, Pytest, JUnit, Vitest)
3. Ejecutar `test_generator.py` con los requisitos
4. Revisar los esqueletos de prueba generados
5. **Validación:** Las pruebas compilan y cubren camino feliz, casos de error, casos límite

### Analizar Brechas de Cobertura

1. Generar informe de cobertura desde el ejecutor de pruebas (`npm test -- --coverage`)
2. Ejecutar `coverage_analyzer.py` sobre el informe LCOV/JSON/XML
3. Revisar brechas priorizadas (P0/P1/P2)
4. Generar pruebas faltantes para rutas no cubiertas
5. **Validación:** La cobertura alcanza el umbral objetivo (típicamente 80%+)

### TDD para Nueva Funcionalidad

1. Escribir la prueba que falla primero (ROJO)
2. Ejecutar `tdd_workflow.py --phase red` para validar
3. Implementar el código mínimo para pasar (VERDE)
4. Ejecutar `tdd_workflow.py --phase green` para validar
5. Refactorizar manteniendo las pruebas en verde (REFACTORIZAR)
6. **Validación:** Todas las pruebas pasan después de cada ciclo

---

## Herramientas

| Herramienta | Propósito | Uso |
|-------------|-----------|-----|
| `test_generator.py` | Generar casos de prueba desde código/requisitos | `python scripts/test_generator.py --input source.py --framework pytest` |
| `coverage_analyzer.py` | Analizar informes de cobertura | `python scripts/coverage_analyzer.py --report lcov.info --threshold 80` |
| `tdd_workflow.py` | Guiar ciclos rojo-verde-refactorizar | `python scripts/tdd_workflow.py --phase red --test test_auth.py` |
| `framework_adapter.py` | Convertir pruebas entre frameworks | `python scripts/framework_adapter.py --from jest --to pytest` |
| `fixture_generator.py` | Generar datos de prueba y mocks | `python scripts/fixture_generator.py --entity User --count 5` |
| `metrics_calculator.py` | Calcular métricas de calidad de pruebas | `python scripts/metrics_calculator.py --tests tests/` |
| `format_detector.py` | Detectar lenguaje y framework | `python scripts/format_detector.py --file source.ts` |
| `output_formatter.py` | Formatear salida para CLI/escritorio/CI | `python scripts/output_formatter.py --format markdown` |

---

## Requisitos de Entrada

**Para Generación de Pruebas:**
- Código fuente (ruta de archivo o contenido pegado)
- Framework objetivo (Jest, Pytest, JUnit, Vitest)
- Alcance de cobertura (unitaria, integración, casos límite)

**Para Análisis de Cobertura:**
- Archivo de informe de cobertura (formato LCOV, JSON o XML)
- Opcional: Código fuente para contexto
- Opcional: Porcentaje de umbral objetivo

**Para Flujo de Trabajo TDD:**
- Requisitos de funcionalidad o historia de usuario
- Fase actual (ROJO, VERDE, REFACTORIZAR)
- Código de prueba y estado de implementación

---

## Limitaciones

| Alcance | Detalles |
|---------|----------|
| Enfoque en pruebas unitarias | Las pruebas de integración y E2E requieren patrones diferentes |
| Análisis estático | No puede ejecutar pruebas ni medir comportamiento en tiempo de ejecución |
| Soporte de lenguajes | Mejor para TypeScript, JavaScript, Python, Java |
| Formatos de informe | Solo LCOV, JSON, XML; otros formatos necesitan conversión |
| Pruebas generadas | Proporcionan esqueleto; requieren revisión humana para lógica compleja |

**Cuándo usar otras herramientas:**
- Pruebas E2E: Playwright, Cypress, Selenium
- Pruebas de rendimiento: k6, JMeter, Locust
- Pruebas de seguridad: OWASP ZAP, Burp Suite
