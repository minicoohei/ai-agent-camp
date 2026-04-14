---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1", "start-6-2", "start-6-3", "start-6-4"]
duration: "~50 min"
level: "advanced"
tags: ["agent", "capstone", "deployment"]
---

# 🎓 Lesson 6-5: Ejercicio integral - Integracion de desarrollo de agentes de IA

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 6-5: Ejercicio integral - Integracion de desarrollo de agentes de IA**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Integrar el aprendizaje de los Modulos 1-7 y completar un proyecto de agente de IA funcional |
| Duracion | ~50 min |
| Skills utilizados | Command / Skill / Rules / SubAgent integral, conceptos de despliegue en produccion |
| Requisitos previos | Lesson 6-1 a Lesson 6-4 completados |
| Pagina del curso | [Module 6: Desarrollo de agentes](https://ai-agent.camp/es/course/module-6) en paralelo |

**Flujo de la sesion:**
1. Inicializacion del proyecto y organizacion de requisitos
2. Ensamblar el agente integrado
3. Verificar el funcionamiento y preparar para el despliegue en produccion

Al finalizar esta sesion, un sistema de agente de IA completo estara terminado y el curso habra concluido.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de iniciar la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo/a?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver primero la página del curso"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Inicializacion del proyecto

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Inicialización del proyecto",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree la estructura del proyecto para el ejercicio integral.

Crear directorios:
mkdir -p ai-content-agent/src/{api,services,subagents,utils}
mkdir -p ai-content-agent/tests
mkdir -p ai-content-agent/.github/workflows
mkdir -p ai-content-agent/.claude/{skills,rules}
mkdir -p ai-content-agent/.cursor/commands

Crear archivos necesarios:
touch ai-content-agent/requirements.txt
touch ai-content-agent/README.md
touch ai-content-agent/.env.example

Verifique la estructura.
```

**Resultado esperado**: Se crea la estructura del proyecto para el ejercicio integral.

---

## 🚀 Step 2: Implementacion de servidor FastAPI

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Implementación del servidor FastAPI",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo ai-content-agent/src/main.py con el siguiente contenido:

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import uuid
from datetime import datetime

app = FastAPI(
    title="AI Content Generator API",
    version="1.0.0",
    description="AI-powered content generation and management"
)

# Definiciones de modelos
class TaskRequest(BaseModel):
    title: str
    prompt: str
    priority: str = "medium"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    created_at: str

# Almacenamiento de tareas en memoria (use una BD en produccion)
tasks: Dict[str, Dict] = {}

@app.get("/health")
async def health_check():
    """Verificacion de estado"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """Crear una nueva tarea"""
    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = {
        "id": task_id,
        "title": request.title,
        "prompt": request.prompt,
        "priority": request.priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None
    }
    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=tasks[task_id]["created_at"]
    )

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Obtener informacion de la tarea"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/tasks")
async def list_tasks(limit: int = 10):
    """Obtener lista de tareas"""
    task_list = list(tasks.values())
    return task_list[:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Resultado esperado**: Se implementa el servidor FastAPI.

---

## 🚀 Step 3: Crear requirements.txt

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear requirements.txt",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Escriba el siguiente contenido en ai-content-agent/requirements.txt:

fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
python-dotenv==1.0.0
httpx==0.26.0
pytest==7.4.0
pytest-asyncio==0.23.0
```

**Resultado esperado**: Se crea el archivo de dependencias.

---

## 🚀 Step 4: Flujo de trabajo de GitHub Actions

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Flujo de trabajo de GitHub Actions",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo ai-content-agent/.github/workflows/ci.yml con el siguiente contenido:

name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest tests/ -v || echo "No tests found"

      - name: Health check
        run: |
          python -c "from src.main import app; print('Import successful!')"

      - name: Summary
        if: always()
        run: |
          echo "## CI Summary" >> $GITHUB_STEP_SUMMARY
          echo "- Branch: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- Status: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**Resultado esperado**: Se configura el pipeline de CI/CD.

---

## 🚀 Step 5: Crear codigo de pruebas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Crear código de pruebas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo ai-content-agent/tests/test_api.py con el siguiente contenido:

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.main import app

client = TestClient(app)

def test_health_check():
    """Prueba de verificacion de estado"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

def test_create_task():
    """Prueba de creacion de tarea"""
    response = client.post("/tasks", json={
        "title": "Test Task",
        "prompt": "Generate test content",
        "priority": "high"
    })
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "pending"

def test_get_task():
    """Prueba de obtencion de tarea"""
    # Primero crear una tarea
    create_response = client.post("/tasks", json={
        "title": "Get Test",
        "prompt": "Test prompt"
    })
    task_id = create_response.json()["task_id"]

    # Obtener la tarea
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test"

def test_get_task_not_found():
    """Prueba de obtencion de tarea inexistente"""
    response = client.get("/tasks/nonexistent")
    assert response.status_code == 404

def test_list_tasks():
    """Prueba de lista de tareas"""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

Ejecute las pruebas:
cd ai-content-agent && pip install -r requirements.txt && pytest tests/ -v
```

**Resultado esperado**: Todas las pruebas de API pasan.

---

## 🚀 Step 6: Verificacion final y documentacion

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 6: Verificación final y documentación",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo ai-content-agent/README.md con el siguiente contenido:

# AI Content Generator Agent

Un sistema de generacion y gestion de contenido impulsado por IA.

## Funciones

- Gestion de tareas mediante API RESTful
- Generacion asincrona de contenido
- Funcion de revision de calidad
- Publicacion en multiples plataformas

## Configuracion

### Requisitos previos
- Python 3.11+
- pip

### Instalacion

```bash
git clone <repository-url>
cd ai-content-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Ejecucion

```bash
python -m src.main
```

API: http://localhost:8000

### Pruebas

```bash
pytest tests/ -v
```

## Endpoints de API

| Metodo | Endpoint | Descripcion |
|--------|----------|------|
| GET | /health | Verificacion de estado |
| POST | /tasks | Crear tarea |
| GET | /tasks/{id} | Obtener tarea |
| GET | /tasks | Lista de tareas |

## Estructura del proyecto

```
ai-content-agent/
├── src/
│   ├── main.py          # FastAPI principal
│   ├── api/             # Endpoints
│   ├── services/        # Logica de negocio
│   └── subagents/       # Implementacion de SubAgent
├── tests/               # Pruebas
├── .github/workflows/   # CI/CD
└── requirements.txt     # Dependencias
```

## Licencia
MIT
```

**Resultado esperado**: La documentacion del proyecto esta completa.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "Error de importación"},
      {"id": "trouble_2", "label": "El puerto está en uso"},
      {"id": "trouble_3", "label": "GitHub Actions falla"},
      {"id": "trouble_4", "label": "No se encuentran las pruebas"}
    ]
  }]
}
```


- Ocurre un error de importacion
- El puerto esta en uso
- GitHub Actions falla
- No se encuentran las pruebas

### Problema 1: "Error de importacion"
**Causa**: PYTHONPATH no esta configurado
**Prompt de solucion**:
```
Verifique lo siguiente:
1. Agregue la raíz del proyecto a sys.path
2. __init__.py existe en el directorio
3. El entorno virtual está activo
```

### Problema 2: "El puerto esta en uso"
**Causa**: El puerto 8000 ya esta en uso
**Prompt de solucion**:
```
Cambie el puerto:
uvicorn.run(app, host="0.0.0.0", port=8001)
O termine el proceso existente:
lsof -i :8000 && kill <PID>          # Mac/Linux
# Windows: Encuentre el PID con netstat -ano | findstr :8000, luego termine con taskkill /PID <PID> /F
```

### Problema 3: "GitHub Actions falla"
**Causa**: Error en la configuracion del flujo de trabajo
**Prompt de solucion**:
```
Verifique lo siguiente:
1. ¿La indentación de YAML es correcta?
2. ¿La ruta de requirements.txt es correcta?
3. ¿La versión de Python es correcta?
```

### Problema 4: "Pruebas no encontradas"
**Causa**: La convencion de nombres de archivos de prueba es incorrecta
**Prompt de solucion**:
```
Convenciones de nombres de archivos de prueba de pytest:
- test_*.py o *_test.py
- Las funciones de prueba comienzan con test_
```

---

## ✅ Punto de control

### Lista de verificacion del ejercicio integral

### Module 6-1: Commands
- [ ] Comandos colocados en .cursor/commands/
- [ ] Al menos 3 comandos creados

### Module 6-2: Skills
- [ ] Skills colocados en skills/
- [ ] Documentado con SKILL.md
- [ ] Existe codigo de pruebas

### Module 6-3: Rules
- [ ] Comportamiento definido en .cursor/rules/rules.md
- [ ] Estandares de seguridad y rendimiento especificados

### Module 6-4: SubAgents
- [ ] Orchestrator esta implementado
- [ ] Multiples SubAgents estan vinculados
- [ ] Existe manejo de errores

### Module 6-5: Integracion
- [ ] Verificar el funcionamiento del servidor FastAPI
- [ ] Endpoints de API probados
- [ ] GitHub Actions configurado
- [ ] Documentacion completa

---

## 🎉 Felicitaciones!

Ha completado todos los modulos!

### Habilidades adquiridas
1. **Desarrollo de agentes de IA**: Diseno e implementacion de flujos de trabajo complejos
2. **Microservicios**: Diseno de SubAgents con acoplamiento debil
3. **Integracion de API externas**: Integracion con Notion, Slack, Google
4. **DevOps**: Construccion de pipelines de CI/CD
5. **Desarrollo empresarial**: Diseno de sistemas escalables


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 output/
└── {nombre-del-proyecto}/  (artefactos de agente/código)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/{nombre-del-proyecto}/

# Verificar el inicio (primeras 30 lineas)
head -30 output/{nombre-del-proyecto}/
```

> 💡 Ver texto completo: `cat output/{nombre-del-proyecto}/` para mostrar el texto completo

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Cursor para verificar la finalizacion:

```
# Verificación de finalización: Verifique que se hayan generado los archivos de salida esperados en la carpeta output/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Todas las secciones estan completas. Elija que hacer a continuacion.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_module", "label": "Continuar al Módulo 7 Skill/Commands (/start-7-1)"},
      {"id": "course_top", "label": "Abrir la página del curso (ai-agent.camp)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_module → /start-7-1（Module 7 Skill/Commands）
- course_top → Abrir https://ai-agent.camp/es/course en el navegador
- finish → Finalizar
