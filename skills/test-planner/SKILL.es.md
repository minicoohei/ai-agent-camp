---
name: test-planner
description: "Se utiliza para generar planes de prueba, casos de prueba e informes de prueba. Se activa con solicitudes como 'Crear un plan de pruebas', 'Generar casos de prueba', 'Escribir pruebas E2E', etc."
triggers:
  - Crear un plan de pruebas
  - Generar casos de prueba
  - Escribir pruebas E2E
  - Resumen de resultados de pruebas
  - Analizar perspectivas de prueba
  - test-planner
  - Prueba Playwright
---

# Planificador de Pruebas - Herramienta de Planificación y Ejecución de Pruebas

Genera automáticamente planes de prueba, casos de prueba y código de prueba a partir de descripciones de casos de uso.

## Flujo de Trabajo

1. Recibir descripción de caso de uso (usecases.md) como entrada
2. Analizar perspectivas de prueba (normal/anormal/valores límite/seguridad)
3. Producir plan de pruebas y casos de prueba estructurados
4. Generar código de prueba E2E con Playwright según sea necesario

## Plantillas

### Plantilla de Plan de Pruebas

```markdown
# Plan de Pruebas: {Nombre del Sistema}

## 1. Descripción General de Pruebas
### 1.1 Objetivo de las Pruebas
### 1.2 Alcance de las Pruebas
### 1.3 Entorno de Pruebas

## 2. Estrategia de Pruebas
### 2.1 Niveles de Prueba
| Nivel | Objetivo | Método | Herramienta |
|-------|----------|--------|-------------|
| Prueba Unitaria | Funciones/métodos individuales | Caja blanca | pytest |
| Prueba de Integración | Coordinación entre APIs | Caja gris | pytest + requests |
| Prueba E2E | Flujos de operación en pantalla | Caja negra | Playwright |

### 2.2 Perspectivas de Prueba
- Pruebas funcionales (casos normales/anormales)
- Pruebas de valores límite
- Pruebas de seguridad (autenticación/autorización)
- Pruebas de rendimiento (tiempo de respuesta)
- Pruebas de usabilidad

## 3. Cronograma de Pruebas
| Fase | Duración | Responsable | Entregables |
|------|----------|-------------|-------------|

## 4. Criterios de Aprobación/Rechazo
- Tasa de ejecución de casos de prueba: 100%
- Errores críticos (Severidad: Crítica/Alta): 0
- Cobertura de pruebas: 80% o superior
```

### Plantilla de Caso de Prueba

```markdown
# Lista de Casos de Prueba

## TC-{Número}: {Nombre de la Prueba}
- **Nivel de Prueba:** Unitaria / Integración / E2E
- **Caso de Uso Relacionado:** UC-{Número}
- **Precondiciones:**
- **Pasos de Prueba:**
  1. {Paso 1}
  2. {Paso 2}
  3. {Paso 3}
- **Resultado Esperado:**
- **Datos de Prueba:**
- **Prioridad:** Alta / Media / Baja
- **Resultado:** No ejecutada / Aprobada / Fallida
```

### Plantilla de Prueba E2E con Playwright

```typescript
import { test, expect } from '@playwright/test';

test.describe('{Nombre de la Funcionalidad}', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('{Nombre de la Prueba}', async ({ page }) => {
    // Preparar
    // Actuar
    // Verificar
    await expect(page.locator('{selector}')).toBeVisible();
  });
});
```

### Plantilla de Evidencia de Prueba

```markdown
# Evidencia de Prueba: {ID del Caso de Prueba}

## Información de Ejecución
- Fecha de Ejecución: {datetime}
- Ejecutor: {name}
- Entorno: {environment}

## Resultado
- Estado: Aprobada / Fallida
- Captura de pantalla: {path}
- Log: {path}

## Observaciones
```

### Plantilla de Resumen de Resultados de Pruebas

```markdown
# Resumen de Resultados de Pruebas

## Descripción General
| Elemento | Valor |
|----------|-------|
| Total de Casos de Prueba | {total} |
| Ejecutados | {executed} |
| Aprobados | {passed} |
| Fallidos | {failed} |
| Omitidos | {skipped} |
| Tasa de Aprobación | {rate}% |

## Lista de Pruebas Fallidas
| TC-ID | Nombre de Prueba | Razón del Fallo | Severidad | Estado |
|-------|-----------------|-----------------|-----------|--------|

## Evaluación de Calidad
- [ ] Se cumplen los criterios de aprobación/rechazo
- [ ] Los errores críticos son 0
- [ ] La cobertura de pruebas es 80% o superior
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| input | Sí | - | Ruta al archivo de descripción de caso de uso |
| type | No | all | Tipo de prueba (unit/integration/e2e/all) |
| output_dir | No | output/pm/ | Directorio de salida |
| format | No | markdown | Formato de salida (markdown/playwright) |

## Formato de Salida

- Plan de pruebas -> `output/pm/test-plan.md`
- Casos de prueba -> `output/pm/test-cases.md`
- Código de prueba E2E -> `output/pm/e2e-tests/*.spec.ts`
- Evidencia de pruebas -> `output/pm/unit-test-evidence/`, `output/pm/integration-test-evidence/`
- Resumen de resultados -> `output/pm/test-summary.md`

## Ejemplo

```
Use la habilidad test-planner para generar un plan de pruebas y casos de prueba desde usecases.md.
-> Se generan output/pm/test-plan.md y output/pm/test-cases.md
```
