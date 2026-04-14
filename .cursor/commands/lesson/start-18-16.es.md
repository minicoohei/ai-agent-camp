---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-15", "output/pm/test-cases.md"]
level: "intermediate"
tags: ["pm", "test", "unit-test", "pytest"]
---

# 🎓 Lesson 18-16: Pruebas unitarias

| Elemento | Detalles |
|------|------|
| Objetivo | Ejecutar pruebas unitarias en la logica del backend de TaskFlow con pytest y recopilar evidencia |
| Duracion | ~25 min |
| Habilidades utilizadas | habilidad test-planner |
| Requisitos previos | Lesson 18-15 completada、output/pm/test-cases.md existe |
| Pagina del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 📍 Paso 1: Identificacion de funciones a probar

### Modulos principales del backend de TaskFlow

El backend de TaskFlow consta de los siguientes modulos funcionales:

1. **Modulo de autenticacion/autorizacion** (`auth.py`)
   - Autenticacion de usuarios, generacion de tokens, verificacion de permisos

2. **Modulo CRUD de tareas** (`tasks.py`)
   - Creacion, lectura, actualizacion y eliminacion de tareas

3. **Modulo de validacion** (`validators.py`)
   - Validacion de entradas, verificacion de logica de negocio

4. **Modulo de notificaciones** (`notifications.py`)
   - Envio de correo electronico, notificaciones de Slack

5. **Modulo de acceso a BD** (`database.py`)
   - Operaciones de base de datos, gestion de transacciones

### Que modulo desea probar?

```json
{
  "type": "AskQuestion",
  "question": "Seleccione los modulos funcionales a probar. Se permiten selecciones multiples.",
  "options": [
    {
      "id": "auth_logic",
      "label": "Logica de autenticacion (auth.py)",
      "value": "auth_logic",
      "description": "Probar autenticacion de usuarios, generacion de tokens y verificacion de permisos"
    },
    {
      "id": "task_crud",
      "label": "CRUD de tareas (tasks.py)",
      "value": "task_crud",
      "description": "Probar creacion, actualizacion, eliminacion y busqueda de tareas"
    },
    {
      "id": "validation",
      "label": "Validacion (validators.py)",
      "value": "validation",
      "description": "Probar validacion de entradas y verificacion de logica de negocio"
    },
    {
      "id": "notifications",
      "label": "Modulo de notificaciones (notifications.py)",
      "value": "notifications",
      "description": "Probar funciones de notificacion por correo y Slack (usando simulaciones)"
    },
    {
      "id": "all_modules",
      "label": "Todos los modulos",
      "value": "all_modules",
      "description": "Pruebas integrales de todos los modulos anteriores"
    }
  ],
  "required": true,
  "helpText": "Se recomienda comenzar con 'CRUD de tareas' o 'Validacion' para pruebas mas faciles."
}
```

### Extraccion de funciones objetivo

Segun el modulo seleccionado, se analiza la siguiente informacion:

- La firma de cada funcion (entrada/salida)
- Dependencias (de otras funciones o bibliotecas)
- Efectos secundarios (operaciones de BD, llamadas a API externas, etc.)
- Codigo de prueba existente (si lo hay)
- Lineas aun no cubiertas

Ejemplo de funciones extraidas:

```python
# auth.py
def authenticate_user(email: str, password: str) -> Dict[str, Any]
def verify_token(token: str) -> Dict[str, Any]
def check_permission(user_id: int, resource_id: int) -> bool

# tasks.py
def create_task(user_id: int, title: str, description: str) -> Task
def update_task(task_id: int, updates: Dict) -> Task
def delete_task(task_id: int) -> bool
def get_tasks_by_user(user_id: int, filters: Dict) -> List[Task]

# validators.py
def validate_email(email: str) -> bool
def validate_password(password: str) -> bool
def validate_task_input(title: str, description: str) -> bool
```

---

## 🚀 Paso 2: Generacion de codigo de prueba pytest

### Estilos de prueba pytest

En pytest, hay multiples estilos de escritura de codigo de prueba:

1. **Pruebas estilo funcion** - Simples y legibles (para principiantes)
   ```python
   def test_authenticate_user_success():
       result = authenticate_user("user@example.com", "Pass1234!")
       assert result["success"] is True
   ```

2. **Pruebas estilo clase** - Organizar pruebas relacionadas (para proyectos medianos)
   ```python
   class TestAuthentication:
       def test_authenticate_user_success(self):
           ...
   ```

3. **Uso de Fixtures** - Procesamiento previo/posterior y gestion de simulaciones (para proyectos grandes)
   ```python
   @pytest.fixture
   def test_user():
       return create_test_user()

   def test_authenticate_user(test_user):
       result = authenticate_user(test_user.email, "Pass1234!")
       assert result["success"] is True
   ```

4. **Estilo recomendado por IA** - Estilo optimo basado en la escala y complejidad del proyecto

### Que estilo de prueba desea utilizar?

```json
{
  "type": "AskQuestion",
  "question": "Seleccione un estilo de escritura de codigo de prueba pytest. Elija segun la escala y complejidad del proyecto.",
  "options": [
    {
      "id": "function_style",
      "label": "Pruebas estilo funcion",
      "value": "function_style",
      "description": "Simples y legibles. Ideal para principiantes y pruebas a pequena escala"
    },
    {
      "id": "class_style",
      "label": "Pruebas estilo clase",
      "value": "class_style",
      "description": "Agrupar pruebas relacionadas. Para proyectos de escala media"
    },
    {
      "id": "fixture_style",
      "label": "Uso de Fixtures",
      "value": "fixture_style",
      "description": "Optimizar configuracion previa/posterior a pruebas. Para proyectos a gran escala"
    },
    {
      "id": "ai_recommended",
      "label": "Estilo recomendado por IA",
      "value": "ai_recommended",
      "description": "La IA selecciona el estilo optimo segun la escala y complejidad del proyecto"
    }
  ],
  "required": true,
  "helpText": "Se recomienda comenzar con 'Pruebas estilo funcion' por simplicidad. Seleccione 'Uso de Fixtures' para configuraciones complejas."
}
```

### Proceso de generacion de codigo de prueba

Segun el estilo seleccionado, se ejecuta lo siguiente:

1. **Cargar los casos de prueba generados en la Leccion 18-15**
   - Extraer casos de prueba de output/pm/test-cases.md

2. **Generar plantillas de funciones de prueba**
   ```python
   # test_tasks.py
   import pytest
   from app.tasks import create_task, update_task, delete_task
   from app.models import Task

   # Prueba de flujo normal
   def test_create_task_success():
       """TC-004: Flujo normal - Creación de tarea exitosa"""
       task = create_task(
           user_id=1,
           title="New Task",
           description="Task description"
       )
       assert task.title == "New Task"
       assert task.user_id == 1

   # Prueba de flujo de error
   def test_create_task_empty_title():
       """TC-005: Flujo de error - Título vacío"""
       with pytest.raises(ValueError, match="Title cannot be empty"):
           create_task(user_id=1, title="", description="desc")

   # Prueba de valor límite
   def test_create_task_max_title_length():
       """TC-006: Valor límite - Longitud máxima del título"""
       long_title = "x" * 255
       task = create_task(user_id=1, title=long_title, description="desc")
       assert len(task.title) == 255
   ```

3. **Crear simulaciones y fixtures**
   ```python
   @pytest.fixture
   def test_user():
       return User(id=1, email="test@example.com")

   @pytest.fixture
   def test_db(monkeypatch):
       # Configurar BD de prueba
       monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
   ```

4. **Generar archivos de codigo de prueba**
   - output/pm/unit-test-code/test_auth.py
   - output/pm/unit-test-code/test_tasks.py
   - output/pm/unit-test-code/test_validators.py
   - output/pm/unit-test-code/conftest.py (Fixtures compartidos)

---

## ⚠️ Paso 3: Ejecucion de pruebas y captura de evidencia

### Seleccion del metodo de ejecucion de pytest

Hay varios patrones para la ejecucion de pruebas:

1. **Ejecutar todas las pruebas** - Ejecutar todas las pruebas a la vez
2. **Ejecutar por categoria** - Ejecutar por modulo (pruebas de auth, pruebas de tasks, etc.)
3. **Ejecutar una por una** - Ejecutar pruebas individuales para depuracion

### Seleccione el metodo de ejecucion de pruebas

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el metodo de ejecucion de pruebas pytest. Se requiere captura detallada de evidencia.",
  "options": [
    {
      "id": "run_all",
      "label": "Ejecutar todas las pruebas",
      "value": "run_all",
      "description": "Ejecutar todas las pruebas a la vez. Tiempo de ejecucion corto (recomendado)"
    },
    {
      "id": "run_by_category",
      "label": "Ejecutar por categoria",
      "value": "run_by_category",
      "description": "Ejecutar por modulo (auth, tasks, validators). Proporciona resultados detallados"
    },
    {
      "id": "run_individually",
      "label": "Ejecutar una por una",
      "value": "run_individually",
      "description": "Ejecutar pruebas individuales para verificacion. Conveniente para depuracion (toma mas tiempo)"
    }
  ],
  "required": true,
  "helpText": "Comience con 'Ejecutar todas las pruebas' para obtener una vision general, luego use 'Ejecutar por categoria' para revision detallada de pruebas fallidas."
}
```

### Ejecucion de pruebas y captura de evidencia

Segun el metodo seleccionado, se ejecuta lo siguiente:

1. **Preparar el entorno de ejecucion de pruebas**
   ```bash
   # Verificar entorno virtual
   python3 -m venv venv          # En Windows: python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate

   # Instalar paquetes de dependencia
   pip install pytest pytest-cov pytest-html pydantic
   ```

2. **Ejecutar pruebas y capturar resultados**
   ```bash
   # Ejecutar todas las pruebas (con informe HTML y reporte de cobertura)
   pytest output/pm/unit-test-code/ \
     --html=output/pm/unit-test-evidence/report.html \
     --self-contained-html \
     --cov=app \
     --cov-report=html:output/pm/unit-test-evidence/coverage \
     --cov-report=term \
     -v --tb=short > output/pm/unit-test-evidence/test-output.log 2>&1
   ```

3. **Generar archivos de evidencia**
   ```
   output/pm/unit-test-evidence/
   ├── report.html              # Informe HTML de pytest
   ├── coverage/                # Informe de cobertura (HTML)
   │   └── index.html
   ├── test-output.log          # Registro de ejecución de pruebas
   ├── summary.md               # Resumen de resultados de pruebas
   └── failed-tests.txt         # Detalles de pruebas fallidas
   ```

4. **Generar automaticamente el resumen de resultados de pruebas**
   ```
   # Ejemplo de resumen
   Resumen de resultados de ejecución de pruebas
   =======================

   Pruebas ejecutadas: 42
   Exitosas: 40
   Fallidas: 2
   Omitidas: 0
   Tiempo de ejecución: 12.34 seg

   Cobertura: 87.5%

   Pruebas fallidas:
   - test_create_task_with_null_user() - ValueError
   - test_update_nonexistent_task() - KeyError
   ```

---

## ✅ Paso 4: Generacion de informes de resultados de pruebas

### Informes generados

**output/pm/unit-test-evidence/report.html**
- Resultados de ejecucion de todos los casos de prueba (aprobado/fallido)
- Tiempo de ejecucion de cada prueba
- Traza de pila (en caso de fallo)
- Mapa de cobertura

**output/pm/unit-test-evidence/summary.md**
```markdown
# Informe de ejecución de pruebas unitarias

## Resumen
- Fecha/hora de ejecución: 2026-02-10 15:30:45
- Módulos objetivo: auth.py, tasks.py, validators.py
- Estilo de prueba: Pruebas estilo función
- Método de ejecución: Ejecutar todas las pruebas

## Resultados de pruebas
| Elemento | Resultado |
|------|------|
| Pruebas ejecutadas | 42 |
| Exitosas | 40 (95.2%) |
| Fallidas | 2 (4.8%) |
| Omitidas | 0 |
| Tiempo de ejecución | 12.34 seg |

## Cobertura
| Módulo | Cobertura |
|-----------|-----------|
| auth.py | 92% |
| tasks.py | 85% |
| validators.py | 88% |
| **Total** | **87.5%** |

## Detalles de pruebas fallidas
### test_create_task_with_null_user()
- **Error**: ValueError: user_id cannot be null
- **Esperado**: Debe ocurrir un error cuando el ID de usuario es null al crear una tarea
- **Real**: El mensaje de error no coincide

### test_update_nonexistent_task()
- **Error**: KeyError: task not found
- **Esperado**: Se devuelve un mensaje de error apropiado al actualizar una tarea inexistente
- **Real**: Se produce un KeyError (manejo de errores no implementado)

## Propuestas de mejora
1. Estandarización de mensajes de error
2. Fortalecimiento de verificaciones de null
3. Unificación del manejo de excepciones
```

### Comandos de ejecucion de informes

```bash
# Ejecutar la habilidad test-planner (responder las opciones del Paso 1-3 de forma interactiva)
/test-planner --mode execute
```

O ejecutar manualmente:

```bash
# Ejecutar pruebas y capturar resultados
pytest output/pm/unit-test-code/ \
  --html=output/pm/unit-test-evidence/report.html \
  --self-contained-html \
  --cov=app \
  --cov-report=term \
  -v

# Generar resumen
uv run python tools/test_report_generator.py \
  --input output/pm/unit-test-evidence/report.html \
  --output output/pm/unit-test-evidence/summary.md
```

### Verificacion de archivos

```bash
# Verificar archivos generados
ls -la output/pm/unit-test-evidence/
cat output/pm/unit-test-evidence/summary.md
```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/unit-test-code/
└──   (codigo de pruebas unitarias)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/unit-test-code/

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/unit-test-code/
```

> 💡 Texto completo: Ejecute `cat output/pm/unit-test-code/` para mostrar el texto completo

---

## ➡️ Siguiente paso

Las pruebas unitarias estan completas. Esta listo para continuar con el siguiente paso:

**[Lesson 18-17: Pruebas de integracion y E2E](./start-18-17.md)**

En la siguiente leccion, realizara pruebas de integracion entre multiples modulos y pruebas de extremo a extremo.
