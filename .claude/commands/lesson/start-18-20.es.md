---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-1", "start-18-2", "start-18-3", "start-18-4", "start-18-5", "start-18-6", "start-18-7", "start-18-8", "start-18-9", "start-18-10", "start-18-11", "start-18-12", "start-18-13", "start-18-14", "start-18-15", "start-18-16", "start-18-17", "start-18-18", "start-18-19"]
level: "intermediate"
tags: ["pm", "capstone", "review", "traceability"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-20: Ejercicio integral (Capstone)

| Elemento | Detalles |
|------|------|
| Objetivo | Realizar una revisión integrada de todos los entregables de las 20 lecciones del Módulo 18 y revisar todo el proceso de desarrollo de producto |
| Duración | ~30 min |
| Habilidades utilizadas | habilidades pm-toolkit, test-planner, monitoring-dashboard |
| Requisitos previos | Lesson 18-1〜Lesson 18-19 completada |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 📍 Paso 1: Revisión de todos los entregables

Revise todos los entregables de las 20 lecciones creados a lo largo del Módulo 18 y evaluar la finalización y el progreso.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione como verificar los entregables",
  "options": [
    "Escaneo automatico (todos los archivos en output/pm/)",
    "Verificar por fase",
    "Verificar solo los elementos faltantes",
    "Omitir"
  ],
  "multiple": false
}
```

### Lista de entregables esperados

Los siguientes son los entregables que se deben generar en las 20 lecciones del Módulo 18:

**Fase de planificación (18-1 a 18-3):**
- Lesson 18-1: customer-needs.md (documento de análisis de necesidades del cliente)
- Lesson 18-2: requirements-brief.md (resumen de requisitos)
- Lesson 18-3: prd.md (PRD - método Working Backwards)

**Fase de requisitos (18-4 a 18-7):**
- Lesson 18-4: review-summary.md (resultados integrados de 3 tipos de revisión)
- Lesson 18-5: requirements-spec.md (especificación de requisitos)
- Lesson 18-6: usecases.md (descripciones de casos de uso y diagramas de secuencia)
- Lesson 18-7: wireframes.md (diagramas de transición de pantalla y wireframes)

**Fase de diseño (Lección 18-8 a 18-12):**
- Lesson 18-8: er-diagram.puml (diagrama ER y especificaciones de entidades)
- Lesson 18-9: system-architecture.puml (diagrama de arquitectura del sistema y diseño de API)
- Lesson 18-10: wbs.md (WBS y diagrama de Gantt)
- Lesson 18-11: notion-export.md (exportación de integración con Notion)
- Lesson 18-12: design-system.md (especificación del sistema de diseño)

**Fase de implementación/pruebas (Lección 18-13 a 18-18):**
- Lesson 18-13: prototype/ (prototipo HTML)
- Lesson 18-14: e2e-tests/ (pruebas E2E con Playwright)
- Lesson 18-15: test-plan.md (plan de pruebas y casos de prueba)
- Lesson 18-16: unit-test-evidence/ (resultados de ejecución de pruebas unitarias)
- Lesson 18-17: integration-test-evidence/ (resultados de ejecución de pruebas de integración)
- Lesson 18-18: spec-changes.md (diseño de reuniones y análisis de actas)

**Integración/Resumen (Lección 18-19 a 18-20):**
- Lesson 18-19: dashboard.py (panel de control marimo)
- Lesson 18-20: capstone-review-summary.html (revisión de resumen del capstone)

### Escaneo automático de entregables

```python
import os
from pathlib import Path

output_dir = Path("output/pm")

# Obtener lista de archivos
deliverables = {
    "planning": [],
    "requirements": [],
    "design": [],
    "implementation": [],
    "integration": []
}

if output_dir.exists():
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            print(f"✓ {file.name} ({file.stat().st_size} bytes)")
else:
    print(f"Directorio output/pm/ no encontrado")

# Calcular tasa de finalizaci\u00f3n
total_expected = 20
total_found = len(list(output_dir.glob("*"))) if output_dir.exists() else 0
completion_rate = (total_found / total_expected) * 100

print(f"\nFinalizaci\u00f3n: {completion_rate:.1f}% ({total_found}/{total_expected} archivos)")
```

### Finalización por fase

```json
{
  "type": "AskQuestion",
  "question": "Que detalles de fase desea revisar?",
  "options": [
    "Fase de planificacion (1-3)",
    "Fase de requisitos (4-7)",
    "Fase de diseno (8-12)",
    "Fase de implementacion/pruebas (13-18)",
    "Resumen de todas las fases"
  ],
  "multiple": false
}
```

## 📍 Paso 2: Verificación de trazabilidad (Requisitos → Diseño → Pruebas)

Verificación importante en el desarrollo de productos: confirmar que "todos los requisitos estan implementados en el diseño, y todos los diseños estan cubiertos por pruebas."

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el alcance de la verificacion de trazabilidad",
  "options": [
    "5 requisitos principales",
    "Todos los requisitos",
    "Dejar que la IA seleccione los importantes",
    "Verificar solo el panel de control"
  ],
  "multiple": false
}
```

### Estructura de la matriz de trazabilidad

Realice el siguiente seguimiento para cada requisito:

```text
Requisito (Req-001)
├── Referencia de documento de dise\u00f1o (Design-Section-2.3)
│   ├── Wireframe de UI (WF-005)
│   ├── Endpoint de API (POST /api/users)
│   └── Tabla de BD (users table)
├── Casos de prueba (TC-USER-001, TC-USER-002, TC-USER-003)
│   ├── Unit Test: UserModel
│   ├── Integration Test: Auth Flow
│   └── UI Test: Registration Form
└── Resultados de ejecuci\u00f3n de pruebas
    ├── TC-USER-001: PASS
    ├── TC-USER-002: PASS
    └── TC-USER-003: PASS
```

### Script de verificación de trazabilidad

```python
import json
import csv
from pathlib import Path

# Cargar archivo de requisitos
req_file = Path("output/pm/requirements-spec.md")
test_file = Path("output/pm/test-plan.md")

traceability_matrix = {
    "total_requirements": 53,
    "requirements_with_tests": 49,
    "requirements_without_tests": 4,
    "tests_without_requirements": 2,
    "coverage_percentage": 92.45
}

# Generar matriz de trazabilidad
with open("output/pm/traceability-matrix.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Requirement ID",
        "Requirement",
        "Design Reference",
        "Test Cases",
        "Status",
        "Coverage"
    ])
    writer.writeheader()

    # Requisitos de ejemplo
    requirements = [
        {
            "id": "REQ-001",
            "name": "Registro de usuario",
            "design_ref": "Section 3.1, API-001",
            "tests": "TC-AUTH-001, TC-AUTH-002",
            "status": "Covered",
            "coverage": "✓"
        },
        {
            "id": "REQ-002",
            "name": "Inicio de sesi\u00f3n de usuario",
            "design_ref": "Section 3.2, API-002",
            "tests": "TC-AUTH-003, TC-AUTH-004, TC-AUTH-005",
            "status": "Covered",
            "coverage": "✓"
        },
        {
            "id": "REQ-003",
            "name": "Restablecimiento de contrase\u00f1a",
            "design_ref": "Section 3.3, API-003",
            "tests": "TC-AUTH-006, TC-AUTH-007",
            "status": "Partially Covered",
            "coverage": "⚠"
        }
    ]

    for req in requirements:
        writer.writerow(req)

print("Generaci\u00f3n de matriz de trazabilidad completada")
print(f"Total de requisitos: {traceability_matrix['total_requirements']}")
print(f"Requisitos con pruebas: {traceability_matrix['requirements_with_tests']}")
print(f"Tasa de cobertura: {traceability_matrix['coverage_percentage']:.1f}%")
```

### Análisis de brechas

```json
{
  "type": "AskQuestion",
  "question": "Como desea abordar los resultados del analisis de brechas?",
  "options": [
    "Corregir todas las brechas encontradas",
    "Corregir solo brechas de alta prioridad",
    "Documentar brechas y aplazar",
    "Decidir despues de la evaluacion de impacto"
  ],
  "multiple": false
}
```

**Ejemplo de brechas detectadas:**
- Req-045 (limitación de tasa de API): No hay casos de prueba definidos
- Req-051 (registros de monitoreo): Detalles poco claros en documentos de diseño
- TC-PERF-012 (prueba de rendimiento): Requisito correspondiente no identificado

## 📍 Paso 3: Cálculo de métricas de calidad

Cuantifique el estado de calidad general del proyecto y evalue objetivamente.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el nivel de detalle de las metricas",
  "options": [
    "Solo resumen",
    "Analisis detallado",
    "Con comparacion de referencia",
    "Analisis de IA recomendado"
  ],
  "multiple": false
}
```

### Métricas clave

```python
import json
from datetime import datetime

quality_metrics = {
    "timestamp": datetime.now().isoformat(),
    "project_name": "TaskFlow v1",
    "evaluation_date": "2024-07-15",

    # 1. Cobertura de requisitos
    "requirements": {
        "total": 53,
        "specified": 53,
        "coverage_rate": 100,
        "status": "✓ Excellent"
    },

    # 2. Cobertura de pruebas
    "test_coverage": {
        "total_requirements": 53,
        "tested_requirements": 49,
        "coverage_rate": 92.45,
        "status": "✓ Good"
    },

    # 3. Resultados de ejecuci\u00f3n de pruebas
    "test_results": {
        "total_test_cases": 156,
        "passed": 136,
        "failed": 12,
        "skipped": 8,
        "pass_rate": 87.18,
        "status": "⚠ Need Improvement"
    },

    # 4. Finalizaci\u00f3n de documentaci\u00f3n
    "documentation": {
        "required_docs": 9,
        "completed_docs": 8,
        "draft_docs": 1,
        "completion_rate": 88.89,
        "status": "✓ Good"
    },

    # 5. M\u00e9tricas de calidad de c\u00f3digo
    "code_quality": {
        "lines_of_code": 12450,
        "code_duplication": 8.5,
        "cyclomatic_complexity_avg": 3.2,
        "test_code_ratio": 0.45,
        "status": "✓ Good"
    },

    # 6. Progreso del cronograma
    "schedule": {
        "planned_duration_days": 180,
        "actual_elapsed_days": 173,
        "progress_percentage": 96.1,
        "status": "✓ On Track"
    },

    # 7. Gesti\u00f3n de riesgos
    "risk_management": {
        "identified_risks": 24,
        "mitigated_risks": 22,
        "active_risks": 2,
        "mitigation_rate": 91.67,
        "status": "✓ Good"
    },

    # 8. Puntuaci\u00f3n general
    "overall_health": {
        "score": 88.5,
        "level": "GREEN",
        "status": "✓ Project Health: Excellent"
    }
}

# Guardar en formato JSON
with open("output/pm/quality-metrics.json", "w") as f:
    json.dump(quality_metrics, f, indent=2, ensure_ascii=False)

# Mostrar en formato de tabla
print("=" * 70)
print("TASKFLOW V1 - Resumen de m\u00e9tricas de calidad")
print("=" * 70)
print(f"Fecha de evaluaci\u00f3n: {quality_metrics['evaluation_date']}")
print()

print("📊 Lista de m\u00e9tricas")
print("-" * 70)
print(f"Cobertura de requisitos:   {quality_metrics['requirements']['coverage_rate']}%")
print(f"Cobertura de pruebas:      {quality_metrics['test_coverage']['coverage_rate']:.2f}%")
print(f"Tasa de \u00e9xito de pruebas:  {quality_metrics['test_results']['pass_rate']:.2f}%")
print(f"Documentaci\u00f3n:             {quality_metrics['documentation']['completion_rate']:.2f}%")
print(f"Progreso del cronograma:   {quality_metrics['schedule']['progress_percentage']:.1f}%")
print(f"Mitigaci\u00f3n de riesgos:     {quality_metrics['risk_management']['mitigation_rate']:.2f}%")
print()
print(f"🎯 Puntuaci\u00f3n general del proyecto: {quality_metrics['overall_health']['score']}/100")
print(f"Estado: {quality_metrics['overall_health']['status']}")
print("=" * 70)
```

### Comparación de referencia

```text
Est\u00e1ndar de la industria vs TaskFlow v1
┌──────────────────────────────┬──────────────┬────────────┬──────────────┐
│ M\u00e9trica                       │ Est\u00e1ndar      │ TaskFlow   │ Evaluaci\u00f3n   │
├──────────────────────────────┼──────────────┼────────────┼──────────────┤
│ Cobertura de requisitos      │ 85-95%       │ 100%       │ Excelente    │
│ Cobertura de pruebas         │ 80-90%       │ 92.45%     │ Excelente    │
│ Tasa de \u00e9xito de pruebas     │ 90%+         │ 87.18%     │ Necesita mej │
│ Documentaci\u00f3n                 │ 85%+         │ 88.89%     │ Excelente    │
│ Cumplimiento del cronograma  │ 95%+         │ 96.1%      │ Excelente    │
│ Mitigaci\u00f3n de riesgos        │ 85%+         │ 91.67%     │ Excelente    │
└──────────────────────────────┴──────────────┴────────────┴──────────────┘
```

## 📍 Paso 4: Generación de propuestas de mejora

Desarrolle propuestas de mejora específicas para los problemas detectados en cada fase.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el alcance de las propuestas de mejora",
  "options": [
    "Fase de planificacion",
    "Fase de diseno",
    "Fase de implementacion",
    "Fase de pruebas/operaciones",
    "Todo"
  ],
  "multiple": true
}
```

### Plantilla de propuesta de mejora

```python
improvement_plan = {
    "planning_phase": {
        "issues": [
            {
                "id": "IMP-P-001",
                "title": "Investigaci\u00f3n adicional de an\u00e1lisis de mercado",
                "description": "An\u00e1lisis comparativo de funciones con competidores es insuficiente",
                "priority": "Medium",
                "effort": "3 d\u00edas",
                "recommendation": "Realizar benchmark detallado de productos de la competencia en Q4"
            }
        ]
    },

    "requirements_phase": {
        "issues": [
            {
                "id": "IMP-R-001",
                "title": "Detalle de requisitos no funcionales",
                "description": "Los requisitos de rendimiento no son cuantitativos",
                "priority": "High",
                "effort": "2 d\u00edas",
                "recommendation": "Definir valores espec\u00edficos para tiempo de respuesta de API y procesamiento de BD"
            },
            {
                "id": "IMP-R-002",
                "title": "Ampliaci\u00f3n de casos de uso",
                "description": "Escenarios de manejo de errores insuficientes",
                "priority": "Medium",
                "effort": "3 d\u00edas",
                "recommendation": "Agregar flujos de excepci\u00f3n a cada caso de uso"
            }
        ]
    },

    "design_phase": {
        "issues": [
            {
                "id": "IMP-D-001",
                "title": "Unificar dise\u00f1o de API",
                "description": "Formato de respuesta de error inconsistente",
                "priority": "High",
                "effort": "2 d\u00edas",
                "recommendation": "Definir esquema est\u00e1ndar de respuesta de error y aplicar a todas las APIs"
            }
        ]
    },

    "implementation_phase": {
        "issues": [
            {
                "id": "IMP-I-001",
                "title": "Fallo en ejecuci\u00f3n de prueba",
                "description": "Fallo de prueba en funci\u00f3n de restablecimiento de contrase\u00f1a (TC-AUTH-007)",
                "priority": "High",
                "effort": "1 d\u00eda",
                "recommendation": "Corregir l\u00f3gica de manejo de errores y re-ejecutar pruebas"
            }
        ]
    },

    "testing_phase": {
        "issues": [
            {
                "id": "IMP-T-001",
                "title": "Mejorar cobertura de pruebas",
                "description": "Pruebas de casos l\u00edmite insuficientes (4 requisitos sin cobertura)",
                "priority": "Medium",
                "effort": "5 d\u00edas",
                "recommendation": "Agregar an\u00e1lisis de valores l\u00edmite y pruebas de ramificaci\u00f3n de errores"
            }
        ]
    }
}

# Guardar como JSON
with open("output/pm/improvement-plan.json", "w") as f:
    json.dump(improvement_plan, f, indent=2, ensure_ascii=False)
```

### Documento de lecciones aprendidas

```markdown
# Lecciones aprendidas - Proyecto TaskFlow v1

## Pr\u00e1cticas exitosas

### 1. Matriz de trazabilidad de requisitos
**Impacto**: Detecci\u00f3n exitosa de brechas y duplicaciones en el dise\u00f1o
**Continuidad**: Adoptar el mismo enfoque en el pr\u00f3ximo proyecto

### 2. Revisi\u00f3n de seguridad temprana
**Impacto**: La detecci\u00f3n de riesgos fue posible en la etapa de dise\u00f1o
**Continuidad**: Hacer del dise\u00f1o de seguridad de Lesson 18-12 un est\u00e1ndar para todos los proyectos

### 3. Dise\u00f1o basado en casos de uso
**Impacto**: Creaci\u00f3n exitosa de wireframes de UI desde la perspectiva del usuario
**Continuidad**: Generar casos de prueba directamente desde los casos de uso

## \u00c1reas de mejora

### 1. Momento de ejecuci\u00f3n de pruebas
**Problema**: Tasa de \u00e9xito de pruebas 87.2% (objetivo 90%)
**Causa**: Pruebas ejecutadas inmediatamente despu\u00e9s de finalizar la implementaci\u00f3n, con implementaci\u00f3n incompleta
**Acci\u00f3n**: Asegurar un per\u00edodo de amortiguaci\u00f3n de al menos 2 d\u00edas despu\u00e9s del fin del sprint

### 2. Mantenimiento de documentaci\u00f3n
**Problema**: Retraso en actualizaciones de especificaciones de API
**Causa**: Implementaci\u00f3n de c\u00f3digo y actualizaci\u00f3n de documentaci\u00f3n as\u00edncronas
**Acci\u00f3n**: Introducir generaci\u00f3n autom\u00e1tica de especificaciones OpenAPI en el pipeline CI/CD

### 3. Continuidad de la gesti\u00f3n de riesgos
**Problema**: Revisiones de riesgos semanales retrocedieron a mensuales
**Causa**: Reducci\u00f3n de reuniones por presi\u00f3n de cronograma
**Acci\u00f3n**: Fijar el cronograma de revisi\u00f3n de riesgos, nunca sujeto a reducci\u00f3n

## Recomendaciones para el pr\u00f3ximo proyecto (TaskFlow v2)

1. **Escalamiento**: El dise\u00f1o b\u00e1sico es reutilizable
2. **Automatizaci\u00f3n de pruebas**: Introducir herramientas de automatizaci\u00f3n de pruebas de UI
3. **Expansi\u00f3n DevOps**: Construir monitoreo continuo en el entorno de producci\u00f3n
4. **Expansi\u00f3n del equipo**: Contratar ingenieros de pruebas dedicados
```

### Hoja de ruta de próximos pasos

```json
{
  "type": "AskQuestion",
  "question": "Cuales son los problemas prioritarios para TaskFlow v2?",
  "options": [
    "Fortalecer la automatizacion de pruebas",
    "Automatizar la gestion de especificaciones de API",
    "Optimizacion del rendimiento",
    "Fortalecimiento de la seguridad",
    "Automatizacion de operaciones"
  ],
  "multiple": true
}
```

## ✅ Entregables

Entregables generados en este ejercicio de capstone:

```text
output/pm/
├── traceability-matrix.csv        # Matriz de seguimiento Requisitos → Dise\u00f1o → Pruebas
├── quality-metrics.json           # Resumen de m\u00e9tricas de calidad
├── improvement-plan.json          # Lista de propuestas de mejora
├── lessons-learned.md             # Lecciones aprendidas
└── capstone-review-summary.html   # Resumen de capstone en formato HTML
```

## 🚀 Lista de verificación

```text
□ Verificados todos los entregables en output/pm/ (20+ archivos)
□ Creada matriz de trazabilidad (53 requisitos)
□ Calculadas m\u00e9tricas de calidad (8 m\u00e9tricas)
□ Completado an\u00e1lisis de brechas (4 brechas detectadas)
□ Generadas propuestas de mejora (para cada fase)
□ Creado documento de lecciones aprendidas
□ Revisado todo el Module 18 (18-1 a 18-20)
□ Organizadas recomendaciones para el pr\u00f3ximo proyecto
```

## 📍 Verificación final

```json
{
  "type": "AskQuestion",
  "question": "Cual es el estado de finalizacion del ejercicio de capstone?",
  "options": [
    "Todo completo - Modulo 18 dominado",
    "Casi completo - Corrigiendo detalles",
    "Parcialmente completo - Algunas areas necesitan revision",
    "Necesito soporte - Tengo preguntas"
  ],
  "multiple": false
}
```

---

## 🎯 Puntos clave al completar el Módulo 18

Al completar este módulo, ha adquirido las siguientes habilidades:

✅ **Habilidades de planificación**: Análisis de mercado, definición de requisitos de negocio
✅ **Habilidades de requisitos**: Especificaciones de requisitos del sistema, casos de uso, historias de usuario
✅ **Habilidades de diseño**: Arquitectura del sistema, diseño de BD, diseño de API, diseño de seguridad
✅ **Habilidades de implementación**: Estructura de código, pipelines CI/CD
✅ **Habilidades de pruebas**: Planes de prueba, casos de prueba, automatización de pruebas
✅ **Habilidades de integración**: Gestión de trazabilidad, métricas de calidad, gestión de riesgos


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── project-summary.md  (resumen del proyecto)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/project-summary.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/project-summary.md
```

> 💡 Texto completo: Ejecute `cat output/pm/project-summary.md` para mostrar el texto completo

## ➡️ Siguientes pasos

```json
{
  "type": "AskQuestion",
  "question": "Excelente trabajo! Seleccione su siguiente accion",
  "options": [
    "Realizar el ejercicio de capstone (course/exercises/18-pm-sysdef/capstone/README.md)",
    "Ir a otro modulo",
    "Confirmar entregables en Git",
    "Terminar aqui"
  ],
  "multiple": false
}
```

### Como proceder al ejercicio de capstone (opcional)

En el **ejercicio práctico de capstone** avanzado, basado en definiciones de proyecto reales en lugar de datos de prueba, realizará:

1. **Crear especificaciones de proyecto reales** (aplicando métodos de 18-1 a 18-20)
2. **Ejercicio en equipo**: Distribución de roles entre multiples miembros
3. **Ciclo de retroalimentación**: Revisión de partes interesadas
4. **Verificación de calidad de entregables**: Evaluar con todas las listas de verificación del Módulo 18

Consulte `course/exercises/18-pm-sysdef/capstone/README.md` para más detalles.

### Confirmar en Git

```bash
# Confirmar entregables en Git
git add output/pm/
git commit -m "Lesson 18-20: Revisi\u00f3n integrada del proyecto TaskFlow PM completada

- Matriz de trazabilidad: 53 requisitos, cobertura 92.45%
- Resumen de m\u00e9tricas de calidad: puntuaci\u00f3n general 88.5/100
- An\u00e1lisis de brechas: 4 propuestas de mejora
- Lecciones aprendidas: documentados \u00e9xitos y \u00e1reas de mejora

Module 18 (PM System Definition) completado
"

git push
```

---

## 🎓 Resumen de la ruta de aprendizaje

| Elemento | Lesson | Entregable |
|------|--------|--------|
| Análisis de necesidades del cliente | 18-1 | customer-needs.md |
| Resumen de requisitos | 18-2 | requirements-brief.md |
| PRD | 18-3 | prd.md |
| Revisión de 3 tipos | 18-4 | review-summary.md |
| Especificación de requisitos | 18-5 | requirements-spec.md |
| Casos de uso | 18-6 | usecases.md |
| Transiciones de pantalla/WF | 18-7 | wireframes.md |
| Diseño de BD | 18-8 | er-diagram.puml |
| Arquitectura del sistema/API | 18-9 | system-architecture.puml |
| WBS/Diagrama de Gantt | 18-10 | wbs.md |
| Integración con Notion | 18-11 | notion-export.md |
| Diseño de UI | 18-12 | design-system.md |
| Prototipo | 18-13 | prototype/ |
| Pruebas E2E | 18-14 | e2e-tests/ |
| Plan de pruebas | 18-15 | test-plan.md |
| Pruebas unitarias | 18-16 | unit-test-evidence/ |
| Pruebas de integración | 18-17 | integration-test-evidence/ |
| Reuniones/Actas | 18-18 | spec-changes.md |
| Panel de control | 18-19 | dashboard.py |
| Revisión integrada | 18-20 | capstone-review-summary.html |

---

**Ha completado el Módulo 18 y dominado todo el proceso de desarrollo de productos. Excelente trabajo!**
