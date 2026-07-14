---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-16", "output/pm/unit-test-code/"]
level: "intermediate"
tags: ["pm", "test", "integration", "api-test"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-17: Pruebas de integracion

| Elemento | Detalles |
|------|------|
| Objetivo | Ejecutar pruebas de integracion en las interacciones de API de TaskFlow y recopilar evidencia |
| Duracion | ~25 min |
| Habilidades utilizadas | habilidad test-planner |
| Requisitos previos | Lesson 18-16 completada |
| Pagina del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 📍 Paso 1: Diseno de escenarios de pruebas de integracion

Las pruebas de integracion son un proceso critico para verificar la coordinacion entre multiples APIs. En el sistema TaskFlow, se prueban los siguientes patrones de coordinacion.

- **Coordinacion API a BD**: El flujo completo desde la creacion de tareas por API hasta el almacenamiento en base de datos y busqueda
- **Autenticacion a operaciones de tareas**: Verificacion de permisos para creacion, edicion y eliminacion de tareas despues de la autenticacion del usuario
- **Pipeline de notificaciones**: Verificacion de completitud de notificaciones internas a envio de Webhook en actualizaciones de tareas
- **Integracion completa**: Verificacion de operacion completa entre multiples sistemas

```json
{
  "type": "AskQuestion",
  "question": "Cual alcance de prueba desea priorizar?",
  "options": [
    {
      "id": "api_db",
      "label": "Coordinacion API a BD (desde creacion de tareas hasta busqueda)",
      "nextStep": "start-test-api-db"
    },
    {
      "id": "auth_task",
      "label": "Autenticacion a operaciones de tareas (incluyendo verificacion de permisos)",
      "nextStep": "start-test-auth-task"
    },
    {
      "id": "notification",
      "label": "Pipeline de notificaciones (notificaciones internas a Webhook)",
      "nextStep": "start-test-notification"
    },
    {
      "id": "all",
      "label": "Ejecutar todas las pruebas",
      "nextStep": "start-test-all"
    }
  ],
  "context": "La seleccion del alcance de pruebas de integracion se basa en la evaluacion de riesgos del proyecto y las restricciones de tiempo. Consulte los comentarios de las partes interesadas."
}
```

## 🚀 Paso 2: Generacion de codigo de prueba (pytest + requests)

Genere codigo de pruebas de integracion de API utilizando el framework pytest y la biblioteca requests. El codigo de prueba debe seguir esta estructura.

- Seccion de importacion: Importar pytest, requests y unittest.mock
- Configuracion de fixtures: Inicializar URL base de prueba, tokens de autenticacion y datos de prueba
- Casos de prueba: Funciones correspondientes a cada escenario de coordinacion de API
- Aserciones: Verificar codigos de estado HTTP, cuerpos de respuesta y estado de la base de datos
- Limpieza: Restauracion del entorno despues de las pruebas

```json
{
  "type": "AskQuestion",
  "question": "Como desea configurar su estrategia de simulacion (mock)?",
  "options": [
    {
      "id": "real_db",
      "label": "Usar BD de prueba (verificacion cercana a produccion)",
      "config": {
        "strategy": "integration_testing",
        "database": "test_database",
        "external_apis": "mocked"
      }
    },
    {
      "id": "mock_db",
      "label": "Usar BD simulada (pruebas rapidas y aisladas) (recomendado)",
      "config": {
        "strategy": "unit_testing",
        "database": "in_memory_mock",
        "external_apis": "mocked"
      }
    },
    {
      "id": "hybrid",
      "label": "Estrategia hibrida (BD de prueba para funciones principales, simulacion para APIs externas)",
      "config": {
        "strategy": "hybrid_testing",
        "database": "test_database",
        "external_apis": "mocked"
      }
    }
  ],
  "context": "La estrategia de simulacion se elige equilibrando la fiabilidad de las pruebas y la velocidad de ejecucion. Las pruebas con BD real ofrecen mayor precision de verificacion, pero agregan complejidad a la configuracion y gestion del entorno de pruebas."
}
```

Ejemplo de codigo de prueba:

```python
import pytest
import requests
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

class TestTaskFlowIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "http://localhost:8000/api"
        self.auth_token = "test-token-xyz123"
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        yield
        # Procesamiento de limpieza
        self._cleanup_test_data()

    def test_create_task_and_retrieve(self):
        """Prueba de integración: Creación de tarea -> Búsqueda"""
        payload = {
            "title": "Integration Test Task",
            "description": "Testing API→DB coordination",
            "priority": "high"
        }
        response = requests.post(
            f"{self.base_url}/tasks",
            json=payload,
            headers=self.headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # Verificación de búsqueda en BD
        get_response = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        assert get_response.status_code == 200
        assert get_response.json()["title"] == payload["title"]

    def test_auth_required_for_task_operations(self):
        """Rechazar operaciones de tareas sin autenticación"""
        response = requests.get(f"{self.base_url}/tasks")
        assert response.status_code == 401

    def _cleanup_test_data(self):
        """Limpieza de datos de prueba"""
        pass
```

## ⚠️ Paso 3: Ejecucion de pruebas y captura de evidencia

La ejecucion de pruebas y el registro de resultados sirven como base para el aseguramiento de la calidad del proyecto.

Ejecute las pruebas utilizando el siguiente procedimiento.

1. Verificar el entorno de pruebas
   - La BD de prueba esta funcionando de forma independiente?
   - Los endpoints de la API de prueba estan funcionando correctamente?
   - Las dependencias externas estan correctamente simuladas?

2. Comando de ejecucion de pruebas
   ```bash
   pytest tests/integration/ -v --tb=short --html=report.html --cov=src
   ```

3. Recopilacion de evidencia
   - Registro de ejecucion de pruebas (formato JSON)
   - Capturas de pantalla (estado de la pantalla en caso de fallo)
   - Metricas de rendimiento (tiempo de respuesta, uso de memoria)
   - Registro de verificacion de base de datos (registros INSERT/UPDATE/DELETE)

Estructura de archivos de evidencia:

```text
output/pm/integration-test-evidence/
├── test-execution-log.json
├── test-results.html
├── failed-cases/              # Se genera solo cuando hay pruebas fallidas
│   └── case-XXX-description.md
├── performance-metrics.csv
└── summary.md
```

## ✅ Paso 4: Creacion de informes de defectos

Los defectos encontrados durante la ejecucion de pruebas deben documentarse en un formato apropiado.

```json
{
  "type": "AskQuestion",
  "question": "Que formato de informe de defectos desea utilizar?",
  "options": [
    {
      "id": "simple",
      "label": "Formato simple (solo titulo, causa y solucion)",
      "template": "simple-defect-report.md"
    },
    {
      "id": "detailed",
      "label": "Formato detallado (incluye pasos de reproduccion, valores esperados, valores reales y capturas de pantalla)",
      "template": "detailed-defect-report.md"
    },
    {
      "id": "jira",
      "label": "Formato Jira (campos: prioridad, responsable, sprint)",
      "template": "jira-defect-format.json"
    }
  ],
  "context": "El formato del informe de defectos se elige segun los procesos y el sistema de seguimiento de su organizacion. El formato detallado mejora la eficiencia de correccion del equipo de desarrollo."
}
```

Plantilla de informe de defectos (formato detallado):

```markdown
# Informe de defectos #001

## Resumen
- **Título**: Error de escritura en BD al crear tarea después de autenticación de usuario
- **Severidad**: High
- **Fecha de descubrimiento**: 2024-02-10
- **Responsable**: Dev Team A

## Pasos de reproducción
1. Iniciar sesión con usuario de prueba
2. Llamar a la API de creación de tareas (POST /api/tasks)
3. Se devuelve un error 500

## Valores esperados
- Código de estado: 201 Created
- Respuesta: JSON de la tarea creada

## Valores reales
- Código de estado: 500 Internal Server Error
- Mensaje de error: "Database constraint violation on tasks.user_id"

## Causa raíz
La lógica de validación del ID de usuario durante la creación de tareas es inconsistente con las restricciones de la BD

## Soluciones propuestas
- Corrección de la lógica de validación del ID de usuario
- Ejecución de migración de BD
- Adición de pruebas de regresión

## Evidencia
- Captura de pantalla: error-500-screenshot.png
- Extracto de registro: output/pm/logs/api-error.log
- Respuesta de API: response-dump.json
```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── operation-manual.md  (manual de operacion)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/operation-manual.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/operation-manual.md
```

> 💡 Texto completo: Ejecute `cat output/pm/operation-manual.md` para mostrar el texto completo

## ➡️ Finalizacion y siguientes pasos

Verifique que los siguientes entregables esten listos en output/pm/integration-test-evidence/.

- test-execution-log.json: Registros completos de ejecucion de pruebas
- test-results.html: Informe de resultados de pruebas visualizable en navegador
- failed-cases/*.md: Informes detallados de defectos descubiertos
- performance-metrics.csv: Datos de rendimiento como tiempos de respuesta de API

**Next Lesson**: → Lesson 18-18 Diseno de reuniones y analisis de actas

Las habilidades de pruebas de integracion adquiridas en esta leccion son una parte critica del proceso de aseguramiento de la calidad en el desarrollo de sistemas. La evidencia recopilada se utiliza para informes de fiabilidad a las partes interesadas y la verificacion final antes de produccion.
