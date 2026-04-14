---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1"]
duration: "~25 min"
level: "intermediate"
tags: ["agent", "rules", "cursor"]
---

# 🎓 Lesson 6-3: Configuracion de Cursor Rules

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 6-3: Configuracion de Cursor Rules**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Controlar el comportamiento, contexto y restricciones de la IA con Cursor Rules (.cursor/rules/) |
| Duracion | ~25 min |
| Skills utilizados | Cursor Rules, archivos .mdc |
| Requisitos previos | Leccion 6-1 completada, usando Cursor |
| Pagina del curso | [Module 6: Desarrollo de agentes](https://ai-agent.camp/es/course/module-6) en paralelo |

**Flujo de la sesion:**
1. Crear el directorio de Rules
2. Definir reglas del proyecto (estandares de codificacion, seguridad)
3. Verificar el funcionamiento

Al finalizar esta sesion, la IA respondera de acuerdo con las reglas del proyecto.

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

## 🚀 Step 1: Crear directorio de Rules

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Crear el directorio de Rules",
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
Cree el directorio .cursor/rules/ y prepare la estructura para Cursor Rules.

mkdir -p .cursor/rules

Verifique que el directorio haya sido creado.
```

**Resultado esperado**: Se crea el directorio `.cursor/rules/`.

---

## 🚀 Step 2: Crear Rules basicas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear Rules básicas",
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
Cree el archivo .cursor/rules/rules.md con el siguiente contenido:

# Cursor Rules - Proyecto de desarrollo de agentes de IA

## Descripcion del proyecto
Plataforma base para el desarrollo de agentes de IA
- Python 3.11+
- API REST con FastAPI
- Integracion con la API de Claude AI
- GitHub Actions CI/CD

---

## Convenciones de codificacion

### Estilo Python
- **Cumplimiento de PEP 8**: Todo el codigo
- **Longitud de linea**: 100 caracteres o menos
- **Indentacion**: 4 espacios
- **Naming**:
  - Funciones/variables: snake_case
  - Clases: PascalCase
  - Constantes: UPPER_CASE

### Ejemplo de codigo
```python
# Buen ejemplo
def calculate_user_score(user_id: int) -> float:
    """Calcular la puntuacion del usuario"""
    user = get_user(user_id)
    return user.points * user.multiplier

# Evitar esto
def calc(u):
    return get_user(u).pts * get_user(u).m
```

---

## Reglas de seguridad

### Elementos de verificacion obligatorios
- Validacion de entrada: Todos los endpoints
- Prevencion de inyeccion SQL: Uso de ORM
- Autenticacion: Uso de tokens JWT
- Registro: No incluir informacion confidencial
- Variables de entorno: Gestionadas con .env

### Prohibido
- Contrasenas codificadas en el codigo
- Informacion confidencial en la salida de registros
- Ejecucion directa de sentencias SQL

---

## Directrices de IA (Claude)

### Que hacer
- Concision: Implementar funciones con codigo minimo
- Legibilidad: Implementacion facil de entender para otros
- Manejo de errores: Responder a errores previsibles
- Codigo de prueba: Proporcionar junto con la implementacion

### Que evitar
- Funciones largas: Mantener 30 lineas o menos por funcion
- Variables globales: Evitar siempre que sea posible
- Numeros magicos: Definir como constantes
```

**Resultado esperado**: Se crea un archivo de Rules basico.

---

## 🚀 Step 3: Crear Rules de seguridad

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear Rules de seguridad",
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
Cree el archivo .cursor/rules/security.md con el siguiente contenido:

# Reglas enfocadas en seguridad

## Autenticacion y autorizacion

### Tokens JWT
Verificacion JWT obligatoria para todos los endpoints de API

```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/data")
async def get_data(token = Depends(security)):
    user = verify_token(token.credentials)
    return fetch_user_data(user.id)
```

### Validacion de entrada
Validacion automatica usando modelos Pydantic

```python
from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    email: EmailStr
    age: int  # Verificacion automatica de tipos
```

## Seguridad de registros

```python
# Evitar
logger.info(f"User {user.password} logged in")

# Recomendado
logger.info(f"User {user.id} logged in")
```

## Gestion de variables de entorno

```python
# Gestionado en archivo .env
DATABASE_URL=postgresql://...
API_KEY=secret_xxx

# Cargar en el codigo
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
```
```

**Resultado esperado**: Se crea un archivo de reglas especifico para seguridad.

---

## 🚀 Step 4: Crear Rules de pruebas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Crear Rules de pruebas",
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
Cree el archivo .cursor/rules/testing.md con el siguiente contenido:

# Convenciones de pruebas

## Objetivos de cobertura de pruebas
- General: 80% o mas
- Logica de negocio: 90% o mas
- Endpoints de API: 85% o mas

## Tipos de pruebas

### Pruebas unitarias
Verificar entradas y salidas de funciones

```python
def test_calculate_score():
    result = calculate_score(points=100)
    assert result > 0
    assert result <= 100
```

### Pruebas de integracion
Pruebas que combinan multiples modulos

```python
def test_user_registration_flow():
    user = create_user(email="test@example.com")
    assert user.id > 0
    assert db.query(User).filter(User.id == user.id).first()
```

## Comandos de ejecucion de pruebas

```bash
# Todas las pruebas
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src/ --cov-report=term-missing

# Marcador especifico
pytest tests/ -m "unit"
```

## Convenciones de nomenclatura de pruebas
- Nombre de archivo: test_<nombre_del_modulo>.py
- Nombre de funcion: test_<funcion>_<condicion>_<resultado_esperado>

Ejemplo: test_login_with_invalid_password_returns_401
```

**Resultado esperado**: Se crea un archivo de reglas especifico para pruebas.

---

## 🚀 Step 5: Verificar aplicacion de Rules

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificar aplicación de Rules",
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
Por favor, verifique la lista y el contenido de los archivos Rules que creo:

1. Listar los archivos en el directorio .cursor/rules/
2. Resumir los puntos principales de cada archivo Rules
3. Verificar que las Rules se apliquen a todo el proyecto

Despues de la verificacion, escriba una funcion simple de Python y verifique que siga las Rules.
Ejemplo: Un endpoint de API para obtener informacion del usuario
```

**Resultado esperado**: Los archivos de reglas son reconocidos por Cursor y referenciados durante la generacion de codigo.

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
      {"id": "trouble_1", "label": "Las Rules no se aplican"},
      {"id": "trouble_2", "label": "Las Rules son demasiado largas para cargar"},
      {"id": "trouble_3", "label": "La IA ignora las Rules"},
      {"id": "trouble_4", "label": "Las Rules entran en conflicto"}
    ]
  }]
}
```


### Problema 1: "Las Rules no se aplican"
**Causa**: La ruta del archivo es incorrecta o Cursor no se ha recargado
**Prompt de solucion**:
```
Verifique lo siguiente:
1. ¿El archivo está en .cursor/rules/?
2. Reinicie Cursor para recargar las Rules
3. Verifique que la extensión del archivo sea .md
```

### Problema 2: "Las Rules son demasiado largas para cargar"
**Causa**: El tamano del archivo es demasiado grande
**Prompt de solucion**:
```
Divida sus archivos de Rules:
- rules.md (reglas básicas)
- security.md (seguridad)
- testing.md (pruebas)
Mantenga cada archivo en un tamaño razonable.
```

### Problema 3: "La IA ignora las Rules"
**Causa**: La descripcion de las reglas es ambigua o la prioridad es demasiado baja
**Prompt de solucion**:
```
Escriba las Rules de forma más clara:
- Use "obligatorio" en lugar de "recomendado"
- Incluya ejemplos de código específicos
- Indique claramente las acciones prohibidas
```

### Problema 4: "Las Rules entran en conflicto"
**Causa**: Multiples archivos de reglas tienen instrucciones contradictorias
**Prompt de solucion**:
```
Verifique que no haya contradicciones entre los archivos de Rules.
Priorice las reglas básicas (rules.md) y use las reglas especializadas como complemento.
```

---

## ✅ Punto de control
- [ ] El directorio .cursor/rules/ existe
- [ ] rules.md ha sido creado
- [ ] security.md ha sido creado
- [ ] testing.md ha sido creado
- [ ] Se genera codigo de acuerdo con las reglas


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-6-4)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-6-4
- finish → Finalizar
