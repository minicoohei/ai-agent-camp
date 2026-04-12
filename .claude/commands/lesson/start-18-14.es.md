---
description: "When the user says /start-18-14 — Module 18 Lesson 18-14: PM - Pruebas E2E con Playwright"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-13", "output/pm/prototype/"]
level: "intermediate"
tags: ["pm", "test", "e2e", "playwright"]
---

# 🎓 Lesson 18-14: Pruebas E2E con Playwright

| Elemento | Detalles |
|------|------|
| Objetivo | Generar y ejecutar código de pruebas E2E con Playwright para el prototipo de TaskFlow |
| Duración | ~25 min |
| Habilidades utilizadas | habilidad test-planner |
| Requisitos previos | Lesson 18-13 completada, el prototipo HTML existe en output/pm/prototype/ |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

---

## 📍 Paso 1: Configuración del entorno Playwright

Playwright es una herramienta para ejecutar pruebas automatizadas de navegador. En este paso, prepare el entorno para probar el prototipo de TaskFlow.

### Flujo de configuración del entorno

1. Inicializar un nuevo proyecto con npm init playwright@latest
2. Configurar los ajustes basicos en playwright.config.ts
3. Instalar controladores de navegador
4. Verificar el entorno de ejecución de pruebas

```json
{
  "type": "AskQuestion",
  "question": "Tiene experiencia con Playwright?",
  "options": [
    {
      "id": "beginner",
      "label": "Primera vez usandolo",
      "value": "beginner",
      "description": "Proporciona una guia detallada de configuracion"
    },
    {
      "id": "intermediate",
      "label": "Conozco lo basico",
      "value": "intermediate",
      "description": "Proporciona pasos de configuracion estandar"
    },
    {
      "id": "advanced",
      "label": "Experiencia practica",
      "value": "advanced",
      "description": "Proceder con una guia minima"
    },
    {
      "id": "setup_only",
      "label": "Solo ayudeme con la configuracion",
      "value": "setup_only",
      "description": "Ejecutar script de configuracion"
    }
  ],
  "required": true,
  "helpText": "El nivel de detalle de la guia de configuracion cambia segun el nivel de experiencia"
}
```

### Comandos de configuración

**Opciones: Primera vez usando / Ya conoce lo básico**

```bash
# Mover al directorio del proyecto (directorio con el prototipo)
cd output/pm

# Inicializar Playwright (interactivo)
npm init playwright@latest

# O configuracion explicita
npm install -D @playwright/test
npx playwright install
```

**Configuración básica de playwright.config.ts**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e-tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npx serve . -l 8080',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
});
```

✅ **Punto de control: Configuración del entorno Playwright completa**

```bash
npx playwright --version  # Verificar v1.40.0 o superior
ls -la playwright.config.ts  # Verificar archivo de configuracion
```

---

## 📍 Paso 2: Diseño de escenarios de pruebas E2E

Diseñe escenarios de prueba para el prototipo de TaskFlow. Seleccione escenarios que cubran los flujos de usuario clave basandose en los casos de uso definidos en la Lección 18-6.

### Selección de escenarios de prueba

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el alcance de los escenarios de prueba",
  "options": [
    {
      "id": "minimal",
      "label": "3 escenarios basicos (minimo)",
      "value": "minimal",
      "description": "Pruebas minimas que cubren solo los flujos principales"
    },
    {
      "id": "standard",
      "label": "5 escenarios estandar (recomendado)",
      "value": "standard",
      "description": "Cubre flujos principales + casos limite"
    },
    {
      "id": "comprehensive",
      "label": "Integral (8+ escenarios)",
      "value": "comprehensive",
      "description": "Pruebas integrales de todos los casos de uso"
    },
    {
      "id": "ai_suggest",
      "label": "Obtener sugerencias de IA",
      "value": "ai_suggest",
      "description": "La IA analiza el prototipo y sugiere escenarios optimos"
    }
  ],
  "required": true,
  "helpText": "Seleccione segun el alcance de aseguramiento de calidad de su prototipo. Se recomiendan los 5 escenarios estandar"
}
```

### Definición de escenarios

**3 escenarios basicos (mínimo)**

| # | Nombre del escenario | Objeto de prueba | Elemento de verificación |
|----|----------|----------|--------|
| 1 | Verificación de carga de página | Visualización de página principal | Visualización de título, renderización de encabezado, visualización de formulario inicial |
| 2 | Flujo de creación de tareas | Caso de uso principal | Entrada de formulario, botón de envio, visualización de pantalla de finalización |
| 3 | Verificación de navegación | Transiciones de menu/página | Clic en menu, cambio de URL de página, comportamiento del botón de retroceso |

**5 escenarios estándar (recomendado)**

| # | Nombre del escenario | Objeto de prueba | Elemento de verificación |
|----|----------|----------|--------|
| 1 | Verificación de carga de página | Visualización de página principal | Visualización de título, renderización de encabezado, visualización de formulario inicial |
| 2 | Flujo de creación de tareas | Caso de uso principal | Entrada de formulario, botón de envio, visualización de pantalla de finalización |
| 3 | Verificación de navegación | Transiciones de menu/página | Clic en menu, cambio de URL de página, comportamiento del botón de retroceso |
| 4 | Verificación de visualización responsive | Móvil/Tableta | Diseño al cambiar tamaño de pantalla, operaciones tactiles |
| 5 | Verificación de manejo de errores | Validación de entrada | Visualización de error cuando los campos obligatorios estan vacios, confirmación de mensajes de error |

**Integral (8+ escenarios)**

Además de los 5 escenarios anteriores:

| # | Nombre del escenario | Objeto de prueba | Elemento de verificación |
|----|----------|----------|--------|
| 6 | Verificación de almacenamiento local | Persistencia de datos | Guardado de datos de entrada, restauración después de recargar la página |
| 7 | Gestión de multiples tareas | Funcionalidad de lista | Adición/eliminación/edición de tareas, visualización de lista de tareas |
| 8 | Verificación de integración API | Comunicación con backend | Llamadas API, procesamiento de respuestas, manejo de errores de red |
| 9 | Verificación de rendimiento | Velocidad de carga | Medición de LCP (Largest Contentful Paint), rendimiento de desplazamiento |

### Mapeo de escenarios

Cada escenario se mapea a los casos de uso definidos en la Lección 18-6:

```text
UC-1: Creacion de tareas → Escenario #2 (Estandar)
UC-2: Visualizacion de lista de tareas → Escenario #7 (Integral)
UC-3: Actualizacion de tareas → Escenario #7 (Integral)
UC-4: Navegacion → Escenario #3 (Basico)
UC-5: Manejo de errores → Escenario #5 (Estandar)
```

✅ **Punto de control: 3 o más escenarios de prueba disenados**

```bash
# Crear documento de escenarios de prueba
cat > output/pm/e2e-tests/SCENARIOS.md << 'EOF'
# E2E Test Scenarios

## Selected Scenarios
- [x] Verificacion de carga de pagina
- [x] Flujo de creacion de tareas
- [x] Verificacion de navegacion
- [x] (Opcional) Verificacion de visualizacion responsiva
- [x] (Opcional) Verificacion de manejo de errores
EOF
```

---

## 📍 Paso 3: Generación automática de código de pruebas

Utilice la habilidad test-planner para generar automáticamente código de prueba basado en los escenarios disenados.

### Seleccionar método de generación de código de prueba

```json
{
  "type": "AskQuestion",
  "question": "Seleccione como generar el codigo de prueba",
  "options": [
    {
      "id": "auto_generate",
      "label": "Generar automaticamente con la habilidad test-planner",
      "value": "auto_generate",
      "description": "La IA genera el codigo de prueba en lote basandose en los escenarios"
    },
    {
      "id": "from_template",
      "label": "Modificar desde plantilla",
      "value": "from_template",
      "description": "Personalizar basandose en la plantilla"
    },
    {
      "id": "interactive",
      "label": "Crear uno por uno de forma interactiva",
      "value": "interactive",
      "description": "Crear una prueba a la vez en conversacion con la IA"
    },
    {
      "id": "import_existing",
      "label": "Importar archivos de prueba existentes",
      "value": "import_existing",
      "description": "Cargar y ampliar archivos de prueba existentes"
    }
  ],
  "required": true,
  "helpText": "Seleccione generacion automatica para eficiencia o creacion interactiva para personalizacion"
}
```

### Generación automática (recomendado)

```bash
# Ejecutar la habilidad test-planner
# La IA genera archivos .spec.ts basandose en los escenarios
```

### Estructura de archivos de prueba

Los archivos de prueba generados tienen la siguiente estructura:

**01-page-load.spec.ts - Verificación de carga de página**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Verificacion de carga de pagina', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('El titulo se muestra correctamente', async ({ page }) => {
    const title = page.locator('h1');
    await expect(title).toContainText('TaskFlow');
  });

  test('El encabezado se renderiza', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });

  test('El formulario inicial se muestra', async ({ page }) => {
    const form = page.locator('form');
    await expect(form).toBeVisible();
  });
});
```

**02-task-creation.spec.ts - Flujo de creación de tareas**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Flujo de creacion de tareas', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Puede crear una tarea', async ({ page }) => {
    // Entrada del formulario
    await page.locator('input[name="taskName"]').fill('Tarea de prueba');
    await page.locator('input[name="dueDate"]').fill('2025-12-31');

    // Enviar
    await page.locator('button[type="submit"]').click();

    // Verificar finalizacion
    const successMessage = page.locator('.success-message');
    await expect(successMessage).toContainText('Creado exitosamente');
  });

  test('Redirige despues del envio del formulario', async ({ page }) => {
    await page.locator('input[name="taskName"]').fill('Tarea de prueba');
    await page.locator('button[type="submit"]').click();

    // Verificar redireccion de pagina
    await page.waitForURL('/tasks');
    expect(page.url()).toContain('/tasks');
  });
});
```

**03-navigation.spec.ts - Verificación de navegación**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Verificacion de navegacion', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Navegar haciendo clic en el menu', async ({ page }) => {
    await page.locator('a[href="/tasks"]').click();
    await expect(page).toHaveURL('/tasks');
  });

  test('Volver a la pagina anterior con el boton atras', async ({ page }) => {
    await page.goto('/tasks');
    await page.goBack();
    await expect(page).toHaveURL('/');
  });
});
```

**04-responsive.spec.ts - Visualización responsive (opcional)**

```typescript
import { test, expect, devices } from '@playwright/test';

test.describe('Verificacion de visualizacion responsiva', () => {
  test('El diseno no se rompe en la visualizacion movil', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
    });
    const page = await context.newPage();
    await page.goto('/');

    const header = page.locator('header');
    await expect(header).toBeVisible();

    await context.close();
  });
});
```

**05-error-handling.spec.ts - Manejo de errores (opcional)**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Verificacion de manejo de errores', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Se muestra un error cuando los campos obligatorios estan vacios', async ({ page }) => {
    await page.locator('button[type="submit"]').click();

    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('Campo obligatorio');
  });

  test('Se muestra un error para un formato de fecha invalido', async ({ page }) => {
    await page.locator('input[name="dueDate"]').fill('invalid-date');
    await page.locator('button[type="submit"]').click();

    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toContainText('Formato de fecha invalido');
  });
});
```

### Ubicación de archivos

Los archivos de prueba generados se colocan en la siguiente estructura:

```text
output/pm/
├── e2e-tests/
│   ├── 01-page-load.spec.ts
│   ├── 02-task-creation.spec.ts
│   ├── 03-navigation.spec.ts
│   ├── 04-responsive.spec.ts (Opcional)
│   ├── 05-error-handling.spec.ts (Opcional)
│   ├── SCENARIOS.md
│   └── fixtures/ (segun sea necesario)
├── playwright.config.ts
└── package.json
```

✅ **Punto de control: Código de prueba (.spec.ts) generado**

```bash
# Verificar archivos de prueba
ls -la output/pm/e2e-tests/*.spec.ts

# Verificacion de sintaxis del codigo de prueba
npx tsc --noEmit e2e-tests/*.spec.ts
```

---

## 🚀 Paso 4: Ejecución de pruebas y revisión de informes

Ejecute el código de prueba generado y revise los resultados.

### Seleccionar método de ejecución de pruebas

```json
{
  "type": "AskQuestion",
  "question": "Seleccione como ejecutar las pruebas",
  "options": [
    {
      "id": "run_all",
      "label": "Ejecutar todas las pruebas (recomendado)",
      "value": "run_all",
      "description": "Ejecutar todas las suites de pruebas a la vez y generar informe"
    },
    {
      "id": "headless",
      "label": "Modo sin cabeza (rapido)",
      "value": "headless",
      "description": "Ejecucion rapida sin visualizacion del navegador"
    },
    {
      "id": "ui_mode",
      "label": "Modo UI (con navegador)",
      "value": "ui_mode",
      "description": "Mostrar el navegador para verificacion visual"
    },
    {
      "id": "one_by_one",
      "label": "Verificar una prueba a la vez",
      "value": "one_by_one",
      "description": "Ejecutar pruebas una a la vez y verificar resultados"
    }
  ],
  "required": true,
  "helpText": "Se recomienda el modo UI para la verificacion inicial, luego el modo sin cabeza para la ejecucion rapida posterior"
}
```

### Ejecutar todas las pruebas

```bash
# Verificar que el servidor del prototipo esta en ejecucion
# (Inicio automatico por la configuracion webServer en playwright.config.ts)

# Ejecutar pruebas
npx playwright test

# O ejecutar individualmente
npx playwright test 01-page-load.spec.ts
npx playwright test 02-task-creation.spec.ts
```

### Ejecución en modo headless (rápido)

```bash
npx playwright test --headed=false

# Para entorno CI
CI=true npx playwright test
```

### Ejecución en modo UI (visualización en navegador)

```bash
npx playwright test --ui

# O ejecutar pruebas especificas en modo UI
npx playwright test 02-task-creation.spec.ts --ui
```

### Verificar una prueba a la vez

```bash
# Ejecutar en modo de depuracion
npx playwright test --debug

# O usar Playwright Inspector
PWDEBUG=1 npx playwright test 02-task-creation.spec.ts
```

### Revisión de informes

```bash
# Generar y mostrar informe HTML
npx playwright show-report

# Solo generar informe (sin mostrar)
npx playwright test --reporter=html
```

El informe generado incluye la siguiente información:

- ✅ **Pruebas aprobadas**: Marca de verificación, tiempo de ejecución
- ❌ **Pruebas fallidas**: Traza de pila, captura de pantalla
- ⚠️ **Pruebas omitidas**: Razon de omisión
- 📊 **Estadísticas**: Total de ejecuciones, aprobados, fallos, omisiones
- 📸 **Capturas de pantalla**: Capturadas automáticamente en caso de error

### Solución de problemas

| Problema | Causa y solución |
|------|----------|
| **Error de instalación de Playwright** | Ejecutar `npx playwright install` después de `npm install` |
| **El navegador no se inicia** | Reinstalar controlador de navegador con `npx playwright install chromium` |
| **Selector no encontrado** | Verificar la estructura DOM con `npx playwright test --debug` y corregir selectores |
| **Tiempo de espera de prueba** | Especificar `timeout: 30000` en playwright.config.ts, o usar `test.setTimeout(30000)` |
| **webServer no se inicia** | Verificar el script `dev` en package.json, verificar conflictos de puerto |

✅ **Punto de control: Ejecución de pruebas exitosa**

```bash
# Verificar resultados de pruebas
# Verificar que el resultado de ejecucion termina con "X passed"
npx playwright test

# Verificar informe
npx playwright show-report
```

---

## ✅ Verificación de finalización

Verifique que los siguientes elementos esten completos:

- ✅ Configuración del entorno Playwright completa
  - v1.40.0 o posterior con `npx playwright --versión`
  - playwright.config.ts esta configurado

- ✅ 3 o más escenarios de prueba disenados
  - Documentado en output/pm/e2e-tests/SCENARIOS.md
  - Mapeo con los casos de uso de la Lección 18-6 completado

- ✅ Código de prueba (.spec.ts) generado
  - Los archivos *.spec.ts existen en output/pm/e2e-tests/
  - Cada archivo contiene test.describe, test.beforeEach y multiples test()

- ✅ Ejecución de pruebas exitosa
  - Confirmado "X passed" con `npx playwright test`
  - Sin fallos (o solo fallos conocidos)

- ✅ Informe revisado
  - Informe HTML mostrado con `npx playwright show-report`
  - Se pueden confirmar los detalles de cada prueba

---

## ⚠️ Notas importantes

- **Controladores de navegador**: En la primera configuración, instalar cada navegador con `npx playwright install` (aproximadamente 500MB)
- **Servidor local**: Si la configuración de WebServer no esta configurada, ejecutar `npm run dev` en una terminal separada
- **Mantenimiento de selectores**: Cuando cambie la UI del prototipo, los selectores del código de prueba también necesitan actualizarse
- **Integración CI/CD**: Al usar GitHub Actions o GitLab CI, agregar un paso de instalación de dependencias de Playwright al runner


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── deployment-plan.md  (Plan de despliegue)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/deployment-plan.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/deployment-plan.md
```

> 💡 Texto completo: Ejecute `cat output/pm/deployment-plan.md` para mostrar el texto completo

---

## ➡️ Siguientes pasos

**→ Lesson 18-15: Plan de pruebas y generación de casos de prueba**

En la siguiente lección, realizará lo siguiente:

- Crear un plan de pruebas
- Generar casos de prueba detallados
- Crear automáticamente informes de resultados de pruebas

**Nota**: La Fase C (Diseño e implementación) esta completa!
A partir de la Lección 18-15, proceda a la Fase D (Pruebas y operaciones).

---

## 📚 Recursos relacionados

- [Playwright Official Documentation](https://playwright.dev/)
- [Playwright Test API Reference](https://playwright.dev/docs/api/class-test)
- [Best Practices for E2E Testing](https://playwright.dev/docs/best-practices)
- [Lección anterior: Lesson 18-13](./start-18-13.md)
- [Página del módulo: Module 18 Definición de sistema PM](https://ai-agent.camp/es/course/module-18)

---

**Fecha de creación**: Febrero 2025
**Curso**: TaskFlow PM Training Course
**Fase**: Fase C - Diseño e implementación (etapa final)
