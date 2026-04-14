---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1", "start-6-2", "start-6-3"]
duration: "~40 min"
level: "advanced"
tags: ["agent", "subagent", "orchestration"]
---

# 🎓 Lesson 6-4: Integracion de SubAgents

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 6-4: Integracion de SubAgents**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Disenar e implementar una arquitectura que combine multiples SubAgents para construir flujos de trabajo eficientes |
| Duracion | ~40 min |
| Skills utilizados | Claude Code SubAgent, descomposicion de tareas y orquestacion |
| Requisitos previos | Lesson 6-1 a Lesson 6-3 completados |
| Pagina del curso | [Module 6: Desarrollo de agentes](https://ai-agent.camp/es/course/module-6) en paralelo |

**Flujo de la sesion:**
1. Disenar la arquitectura de SubAgent
2. Definir y vincular Agents especializados
3. Verificar el funcionamiento del flujo integrado

Al finalizar esta sesion, un flujo de trabajo que combina multiples Agents estara operativo.

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

## 🚀 Step 1: Disenar arquitectura de SubAgents

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Diseñar arquitectura de SubAgent",
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
Cree la estructura de directorios para el sistema SubAgent:

mkdir -p .claude/subagents/orchestrator
mkdir -p .claude/subagents/content_agent
mkdir -p .claude/subagents/review_agent
mkdir -p .claude/subagents/publish_agent
mkdir -p .claude/subagents/common

Cree un archivo __init__.py en cada directorio.

Verifique la estructura.
```

**Resultado esperado**: Se crea la estructura de directorios del sistema SubAgent.

---

## 🚀 Step 2: Implementar agente orquestador

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Implementar Orchestrator Agent",
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
Cree el archivo .claude/subagents/orchestrator/agent.py con el siguiente contenido:

import asyncio
from typing import Dict, Any, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class OrchestratorAgent:
    """Agente superior que coordina multiples SubAgents"""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_queue = asyncio.Queue()

    def submit_task(self, task_id: str, task_data: Dict[str, Any]) -> str:
        """Enviar una tarea a la cola"""
        self.tasks[task_id] = {
            **task_data,
            'status': TaskStatus.PENDING,
            'progress': 0,
            'result': None
        }
        self.task_queue.put_nowait({'id': task_id, **task_data})
        logger.info(f"Task submitted: {task_id}")
        return task_id

    async def process_workflow(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar el flujo de trabajo de la tarea"""
        task_id = task['id']
        self.tasks[task_id]['status'] = TaskStatus.IN_PROGRESS

        try:
            # Paso 1: Generacion de contenido
            logger.info(f"Step 1: Content generation for {task_id}")
            self.tasks[task_id]['progress'] = 33
            content = f"Generated content for: {task.get('prompt', 'default')}"

            # Paso 2: Revision
            logger.info(f"Step 2: Review for {task_id}")
            self.tasks[task_id]['progress'] = 66
            review_passed = True

            # Paso 3: Publicacion
            logger.info(f"Step 3: Publish for {task_id}")
            self.tasks[task_id]['progress'] = 100

            self.tasks[task_id]['status'] = TaskStatus.COMPLETED
            self.tasks[task_id]['result'] = {
                'content': content,
                'review_passed': review_passed,
                'published': True
            }

            return self.tasks[task_id]

        except Exception as e:
            logger.error(f"Workflow failed for {task_id}: {e}")
            self.tasks[task_id]['status'] = TaskStatus.FAILED
            self.tasks[task_id]['error'] = str(e)
            return self.tasks[task_id]

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Obtener el estado de la tarea"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Obtener todas las tareas"""
        return list(self.tasks.values())

# Ejemplo de uso
async def main():
    orchestrator = OrchestratorAgent()

    # Enviar tarea
    task_id = orchestrator.submit_task("task_001", {
        "prompt": "Articulo sobre agentes de IA",
        "priority": "high"
    })

    # Ejecutar flujo de trabajo
    task_data = orchestrator.tasks[task_id]
    result = await orchestrator.process_workflow({'id': task_id, **task_data})

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Resultado esperado**: Se implementa el Orchestrator Agent.

---

## 🚀 Step 3: Implementar agente de contenido

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Implementar Content Agent",
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
Cree el archivo .claude/subagents/content_agent/agent.py con el siguiente contenido:

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ContentAgent:
    """SubAgent especializado en generacion de contenido"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.model = self.config.get('model', 'claude-3-5-sonnet')

    async def generate(
        self,
        prompt: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generar contenido basado en un prompt"""

        logger.info(f"Generating content for prompt: {prompt[:50]}...")

        # En una implementacion real, se llamaria a la API de Claude
        # Aqui simulamos
        content = f"""
# {prompt}

## Descripcion general
Este contenido fue generado automaticamente.

## Detalles
- Punto 1: Informacion importante
- Punto 2: Informacion adicional
- Punto 3: Resumen

## Conclusion
Lo anterior es la explicacion de {prompt}.
"""

        return {
            'content': content.strip(),
            'tokens_used': len(content.split()),
            'model': self.model
        }

    async def summarize(self, text: str, max_length: int = 100) -> str:
        """Resumir texto"""
        logger.info("Summarizing text...")

        # Simulacion
        words = text.split()[:max_length]
        return ' '.join(words) + "..."

    async def translate(self, text: str, target_lang: str = "en") -> str:
        """Traducir texto"""
        logger.info(f"Translating to {target_lang}...")

        # Simulacion
        return f"[Translated to {target_lang}]: {text[:100]}..."

# Para pruebas
async def test_content_agent():
    agent = ContentAgent()
    result = await agent.generate("Patrones de diseno de agentes de IA")
    print(result['content'])

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_content_agent())
```

**Resultado esperado**: Se implementa el Content Agent.

---

## 🚀 Step 4: Implementar agente de revision

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Implementar Review Agent",
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
Cree el archivo .claude/subagents/review_agent/agent.py con el siguiente contenido:

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ReviewAgent:
    """SubAgent que realiza revisiones y controles de calidad"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.rules = {
            'min_length': 100,
            'max_length': 5000,
            'forbidden_words': ['prueba', 'TODO'],
            'quality_threshold': 7
        }

    async def review(
        self,
        content: str,
        custom_rules: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Revisar contenido"""

        rules = {**self.rules, **(custom_rules or {})}
        feedback = []
        score = 10

        # Verificacion 1: Verificar longitud
        length = len(content)
        if length < rules['min_length']:
            feedback.append(f"Content too short: {length} chars (min: {rules['min_length']})")
            score -= 2

        if length > rules['max_length']:
            feedback.append(f"Content too long: {length} chars (max: {rules['max_length']})")
            score -= 2

        # Verificacion 2: Verificar palabras prohibidas
        for word in rules.get('forbidden_words', []):
            if word in content:
                feedback.append(f"Forbidden word found: '{word}'")
                score -= 1

        # Resultado
        approved = score >= rules.get('quality_threshold', 7)

        logger.info(f"Review completed: score={score}, approved={approved}")

        return {
            'approved': approved,
            'score': max(0, score),
            'feedback': feedback,
            'details': {
                'length': length,
                'forbidden_words_found': sum(1 for w in rules.get('forbidden_words', []) if w in content)
            }
        }

# Para pruebas
async def test_review_agent():
    agent = ReviewAgent()

    # Contenido corto
    result1 = await agent.review("Short")
    print(f"Short content: {result1}")

    # Contenido normal
    normal_content = "Este es contenido normal. " * 20
    result2 = await agent.review(normal_content)
    print(f"Normal content: {result2}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_review_agent())
```

**Resultado esperado**: Se implementa el Review Agent.

---

## 🚀 Step 5: Prueba de integracion

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Prueba de integración",
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
Cree y ejecute pruebas de integracion para el sistema SubAgent.

Cree el archivo .claude/subagents/tests/test_integration.py:

import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.agent import OrchestratorAgent, TaskStatus
from content_agent.agent import ContentAgent
from review_agent.agent import ReviewAgent

@pytest.mark.asyncio
async def test_orchestrator_submit_task():
    """Prueba de envio de tareas del Orchestrator"""
    orchestrator = OrchestratorAgent()
    task_id = orchestrator.submit_task("test_001", {"prompt": "test"})

    assert task_id == "test_001"
    assert orchestrator.tasks[task_id]['status'] == TaskStatus.PENDING

@pytest.mark.asyncio
async def test_orchestrator_workflow():
    """Prueba de flujo de trabajo del Orchestrator"""
    orchestrator = OrchestratorAgent()
    task_id = orchestrator.submit_task("test_002", {"prompt": "Articulo de IA"})

    result = await orchestrator.process_workflow({'id': task_id, 'prompt': 'Articulo de IA'})

    assert result['status'] == TaskStatus.COMPLETED
    assert result['progress'] == 100

@pytest.mark.asyncio
async def test_content_agent_generate():
    """Prueba de generacion de ContentAgent"""
    agent = ContentAgent()
    result = await agent.generate("prompt de prueba")

    assert 'content' in result
    assert len(result['content']) > 0

@pytest.mark.asyncio
async def test_review_agent_approve():
    """Prueba de aprobacion de ReviewAgent"""
    agent = ReviewAgent()
    long_content = "Este es contenido normal. " * 50

    result = await agent.review(long_content)

    assert result['approved'] == True
    assert result['score'] >= 7

@pytest.mark.asyncio
async def test_review_agent_reject():
    """Prueba de rechazo de ReviewAgent"""
    agent = ReviewAgent()
    short_content = "corto"

    result = await agent.review(short_content)

    assert result['approved'] == False

Ejecute las pruebas:
cd .claude/subagents && pytest tests/test_integration.py -v
```

**Resultado esperado**: Todas las pruebas de integracion pasan.

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
      {"id": "trouble_1", "label": "Error de asyncio"},
      {"id": "trouble_2", "label": "Error de importación de módulo"},
      {"id": "trouble_3", "label": "El procesamiento asíncrono se cuelga"},
      {"id": "trouble_4", "label": "La tarea no se completa"}
    ]
  }]
}
```


### Problema 1: "Error de asyncio"
**Causa**: El bucle de eventos no esta configurado correctamente
**Prompt de solucion**:
```
Instale pytest-asyncio:
pip install pytest-asyncio

Configure en pytest.ini o pyproject.toml:
[pytest]
asyncio_mode = auto
```

### Problema 2: "Error de importacion de modulo"
**Causa**: Falta __init__.py o la ruta no esta configurada
**Prompt de solucion**:
```
Cree __init__.py en cada directorio.
Agregue la raíz del proyecto a sys.path.
```

### Problema 3: "El procesamiento asincrono se cuelga"
**Causa**: Falta await o hay un bloqueo mutuo
**Prompt de solucion**:
```
Agregue await a todas las llamadas de funciones asíncronas.
Configure tiempos de espera con asyncio.wait_for().
```

### Problema 4: "La tarea no se completa"
**Causa**: Se esta produciendo una excepcion dentro del flujo de trabajo
**Prompt de solucion**:
```
Capture errores con try-except y regístrelos en el log.
Configure TaskStatus.FAILED apropiadamente.
```

---

## ✅ Punto de control
- [ ] SubAgentLa estructura del directorio esta creada
- [ ] Orchestrator Agent esta implementado
- [ ] Content Agent esta implementado
- [ ] Review Agent esta implementado
- [ ] Las pruebas de integracion pasan


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

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Cursor para verificar la finalizacion:

```
# Verificación de finalización: Verifique que se hayan generado los archivos de salida esperados en la carpeta output/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-6-5)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-6-5
- finish → Finalizar
