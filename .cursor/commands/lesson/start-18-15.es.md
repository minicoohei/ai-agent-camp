---
description: "When the user says /start-18-15 — Module 18 Lesson 18-15: PM - Plan de pruebas y generacion de casos de prueba"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-14", "output/pm/usecases.md"]
level: "intermediate"
tags: ["pm", "test", "test-plan", "test-cases"]
---

# 🎓 Lesson 18-15: Plan de pruebas y generacion de casos de prueba

| Elemento | Detalles |
|------|------|
| Objetivo | Generar automaticamente planes de prueba y casos de prueba a partir de los casos de uso de TaskFlow |
| Duracion | ~25 min |
| Habilidades utilizadas | habilidad test-planner |
| Requisitos previos | output/pm/usecases.md existe |
| Pagina del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 📍 Paso 1: Explicacion de la estructura del plan de pruebas

### Elementos basicos de un plan de pruebas

Un plan de pruebas consta de los siguientes elementos:

- **Alcance de pruebas**: Que partes del sistema se van a probar
- **Estrategia de pruebas**: Que y como verificar
- **Entorno de pruebas**: Configuracion del entorno para pruebas
- **Cronograma**: Periodo de ejecucion de pruebas y momento de cada fase
- **Recursos**: Herramientas y personal necesarios para la ejecucion de pruebas
- **Criterios de exito**: Criterios de aprobacion de pruebas

Los casos de prueba son procedimientos especificos y valores esperados para probar funciones y escenarios individuales.

### Cual es su nivel de experiencia en pruebas?

```json
{
  "type": "AskQuestion",
  "question": "Seleccione su nivel de experiencia en pruebas. Esto ajustara el detalle y la complejidad del plan de pruebas.",
  "options": [
    {
      "id": "beginner",
      "label": "Principiante - Experiencia limitada en pruebas o perspectivas de prueba poco claras",
      "value": "beginner",
      "description": "La IA sugerira mas perspectivas de prueba e incluira explicaciones detalladas"
    },
    {
      "id": "intermediate",
      "label": "Intermedio - Comprende las perspectivas basicas de prueba",
      "value": "intermediate",
      "description": "Genera planes de prueba y casos de prueba estandar"
    },
    {
      "id": "advanced",
      "label": "Avanzado - Considera la estrategia de pruebas y optimizacion",
      "value": "advanced",
      "description": "Propone planes que incluyen analisis de riesgos, optimizacion de cobertura y mejoras de eficiencia"
    }
  ],
  "required": true,
  "helpText": "Genera planes de prueba y casos de prueba con el nivel de detalle apropiado segun su seleccion."
}
```

---

## 🚀 Paso 2: Generacion de casos de prueba a partir de casos de uso

### Clasificacion de perspectivas de prueba

Para generar casos de prueba de manera efectiva, se requieren pruebas desde multiples perspectivas:

1. **Pruebas de flujo normal**: Probar el flujo normal de los casos de uso
2. **Pruebas de flujo de error**: Probar errores y entradas inesperadas
3. **Pruebas de valores limite**: Probar valores minimos, maximos y circundantes de entrada
4. **Pruebas de seguridad**: Probar autorizacion, autenticacion y validacion de entradas

### Hasta que punto desea generar casos de prueba?

```json
{
  "type": "AskQuestion",
  "question": "Cuanta cobertura desea para la generacion de casos de prueba? El detalle aumenta progresivamente.",
  "options": [
    {
      "id": "normal_only",
      "label": "Solo flujo normal",
      "value": "normal_only",
      "description": "Generar casos de prueba solo para flujos normales de casos de uso (minimo)"
    },
    {
      "id": "normal_abnormal",
      "label": "Flujo normal + Flujo de error",
      "value": "normal_abnormal",
      "description": "Cubre flujos normales y patrones de error comunes (estandar)"
    },
    {
      "id": "normal_abnormal_boundary",
      "label": "Flujo normal + Flujo de error + Valores limite",
      "value": "normal_abnormal_boundary",
      "description": "Incluye pruebas de valores limite ademas de lo anterior (mas detallado)"
    },
    {
      "id": "comprehensive",
      "label": "Flujo normal + Flujo de error + Valores limite + Seguridad",
      "value": "comprehensive",
      "description": "Cobertura completa de pruebas incluyendo pruebas de seguridad (el mas detallado)"
    }
  ],
  "required": true,
  "helpText": "El numero de casos de prueba y el nivel de detalle se determinan segun las perspectivas seleccionadas. Comience con 'Flujo normal + Flujo de error' para un enfoque equilibrado."
}
```

### Proceso de generacion de casos de prueba

Segun su seleccion, se ejecutan los siguientes procesos:

1. Cargar output/pm/usecases.md
2. Generar automaticamente casos de prueba de cada caso de uso segun las perspectivas seleccionadas
3. Asignar ID, descripcion, precondiciones, pasos y valores esperados a cada caso de prueba
4. Agrupar casos de prueba (por caso de uso, por funcion, etc.)
5. Guardar en output/pm/test-cases.md

Los casos de prueba se generan en el siguiente formato:

```text
### ID del caso de prueba: TC-001
**Caso de uso**: UC-001 - Registro de usuario
**Perspectiva**: Flujo normal
**Descripción**: El registro de usuario se realiza correctamente con correo electrónico y contraseña

**Precondiciones**:
- El sistema está accesible
- El usuario no está registrado

**Pasos de prueba**:
1. Abrir la pantalla de registro
2. Ingresar la dirección de correo electrónico (ej.: user@example.com)
3. Ingresar la contraseña (ej.: Pass1234!)
4. Hacer clic en el botón de registro

**Valores esperados**:
- El registro se realiza correctamente
- Se envía un correo de confirmación
- El usuario puede iniciar sesión
```

---

## ⚠️ Paso 3: Priorizacion de casos de prueba

### Enfoque de priorizacion

Cuando hay muchos casos de prueba, puede ser dificil ejecutarlos todos.
Cuando los recursos son limitados, priorice y ejecute las pruebas importantes primero.

Metodos principales de priorizacion:

1. **Basado en riesgo**: Priorizar pruebas para funciones con alto riesgo de negocio
2. **Basado en cobertura**: Priorizar pruebas que cubran mas funciones y ramas
3. **Sugerido por IA**: La IA propone prioridades basadas en datos historicos y mejores practicas

### Seleccione un metodo de priorizacion de casos de prueba

```json
{
  "type": "AskQuestion",
  "question": "Seleccione un metodo de priorizacion para los casos de prueba generados. Esto es efectivo cuando el periodo de pruebas es limitado.",
  "options": [
    {
      "id": "risk_based",
      "label": "Priorizacion basada en riesgo",
      "value": "risk_based",
      "description": "Colocar casos de prueba para funciones de alto riesgo de negocio (autenticacion, pagos, etc.) en la parte superior"
    },
    {
      "id": "coverage_based",
      "label": "Priorizacion basada en cobertura",
      "value": "coverage_based",
      "description": "Colocar casos de prueba con alta cobertura de funciones/ramas en la parte superior (lograr maxima cobertura con presupuesto limitado)"
    },
    {
      "id": "ai_suggested",
      "label": "Priorizacion recomendada por IA",
      "value": "ai_suggested",
      "description": "La IA propone prioridades combinando mejores practicas y complejidad de funciones"
    },
    {
      "id": "priority_all",
      "label": "Priorizar todo (recomendado)",
      "value": "priority_all",
      "description": "Adoptar las 3 perspectivas anteriores y mostrar multiples rangos de prioridad (el mas flexible)"
    }
  ],
  "required": true,
  "helpText": "Basado en riesgo es el mas comun. Si se necesitan multiples perspectivas, seleccione 'Recomendado por IA' o 'Priorizar todo'."
}
```

### Ejecucion de priorizacion

Segun el metodo seleccionado:

1. Calcular una puntuacion de prioridad para cada caso de prueba
2. Generar matrices de riesgo, mapas de cobertura, etc.
3. Determinar el orden de ejecucion por prioridad
4. Agregar informacion de prioridad a output/pm/test-cases.md

---

## ✅ Paso 4: Ejecucion de generacion de plan de pruebas y casos de prueba

### Archivos generados

**output/pm/test-plan.md**
```text
# Plan de pruebas

## 1. Alcance de pruebas
- TaskFlow Backend API
- Frontend UI
- Funciones de autenticación/autorización
- Funciones de gestión de tareas
- Funciones de notificación

## 2. Estrategia de pruebas
- Pruebas unitarias (Unit Test)
- Pruebas de integración (Integration Test)
- Pruebas E2E (End-to-End Test)

## 3. Entorno de pruebas
- Entorno de desarrollo: localhost:3000
- BD de prueba: SQLite (exclusiva para pruebas)

## 4. Cronograma
- Fase 1: Pruebas unitarias (5 días hábiles)
- Fase 2: Pruebas de integración (3 días hábiles)
- Fase 3: Pruebas E2E (2 días hábiles)

## 5. Criterios de éxito
- Tasa de ejecución de casos de prueba: 100%
- Tasa de éxito de casos de prueba: 95% o superior
- Defectos críticos: 0
```

**output/pm/test-cases.md**
```text
# Lista de casos de prueba

## Caso de uso UC-001: Registro de usuario

### TC-001 Flujo normal - Registro de usuario estándar
**Prioridad**: High (basado en riesgo)
**Prioridad**: High (basado en cobertura)
**Valor esperado**: Registro exitoso

### TC-002 Flujo de error - Correo electrónico duplicado
**Prioridad**: High
**Valor esperado**: Mensaje de error mostrado

### TC-003 Flujo de error - Contraseña insuficiente
**Prioridad**: Medium
**Valor esperado**: Error de validación mostrado

## Caso de uso UC-002: Creación de tareas
...
```

### Comandos de ejecucion

```bash
# Ejecutar la habilidad test-planner (responder las opciones del Paso 1-3 de forma interactiva)
/test-planner
```

Alternativamente, la habilidad ejecuta automaticamente lo siguiente:

1. **Generacion del plan de pruebas**
   ```bash
   uv run python tools/test_planner.py \
     --input output/pm/usecases.md \
     --output output/pm/test-plan.md \
     --experience-level <valor_seleccionado> \
     --test-scope <valor_seleccionado>
   # En Windows, reemplace python3 por python
   ```

2. **Generacion de casos de prueba**
   ```bash
   uv run python tools/test_case_generator.py \
     --input output/pm/usecases.md \
     --output output/pm/test-cases.md \
     --coverage <valor_seleccionado> \
     --prioritize <valor_seleccionado>
   # En Windows, reemplace python3 por python
   ```

3. **Verificacion de generacion de archivos**
   ```bash
   ls -la output/pm/test-plan.md output/pm/test-cases.md
   ```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── test-cases.md  (casos de prueba)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/test-cases.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/test-cases.md
```

> 💡 Texto completo: Ejecute `cat output/pm/test-cases.md` para mostrar el texto completo

---

## ➡️ Siguiente paso

Esta listo para continuar con la siguiente leccion:

**[start-18-16: Pruebas unitarias (pytest)](./start-18-16.md)**

En la Leccion 18-16, ejecutara pruebas unitarias en la logica del backend usando pytest basadas en los casos de prueba generados.
