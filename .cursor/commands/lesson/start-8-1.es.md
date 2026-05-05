---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
duration: "~25 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["data", "bigquery", "gcp", "authentication"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 8-1: Conexion y autenticacion de BigQuery

## 📍 Lo que hara en esta sesion

**Lesson 8-1: Conexion y configuracion de autenticacion de BigQuery** !

| Elemento | Contenido |
|------|------|
| Objetivo | Configurar la autenticacion de GCP, conectar a BigQuery y acceder a conjuntos de datos publicos |
| Duracion | ~25 min |
| Habilidades utilizadas | bigquery-auth, gcloud CLI |
| Requisitos previos | Acceso a un proyecto de Google Cloud, Python 3.8+, gcloud CLI instalado |
| Pagina del curso | [Module 8: Analisis de datos](https://ai-agent.camp/es/course/module-8) como referencia paralela |

**Flujo de la sesion:**
1. Verificar la autenticacion de GCP
2. Ejecutar la autenticacion (si no esta configurada)
3. Prueba de conexion a BigQuery
4. Acceder a conjuntos de datos publicos

Al final de esta sesion, podra ejecutar consultas en BigQuery.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Verify GCP Authentication

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verify GCP Authentication",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, verifique el estado de autenticación de GCP (Google Cloud Platform).

Elementos a verificar:
1. Si gcloud CLI está instalado
2. Cuenta de autenticación actual
3. ID del proyecto actual
4. Estado de Application Default Credentials (ADC)

Si hay problemas, proporcione las soluciones.
```

**Resultado esperado:** Se muestra el estado de autenticacion y se proporcionan los pasos de configuracion segun sea necesario.

---

## 🚀 Step 2: Run Authentication (If Not Configured)

Si la autenticacion no esta configurada, configurela con el siguiente prompt:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Run Authentication (If Not Configured)",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, configure la autenticación para acceder a BigQuery.

Autenticación a ejecutar:
1. gcloud auth login (autenticación principal)
2. gcloud auth application-default login (para Python SDK)

Por favor, ejecute cada comando y
confirme si fueron exitosos.
```

**Resultado esperado:** Se abre el navegador y se completa la autenticacion con su cuenta de Google.

---

## 🚀 Step 3: BigQuery Connection Test

Despues de completar la autenticacion, pruebe la conexion a BigQuery:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: BigQuery Connection Test",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, ejecute una prueba de conexión a BigQuery.

Contenido de la prueba:
1. Inicializar el cliente Python de BigQuery
2. Obtener el ID del proyecto actual
3. Ejecutar una consulta de prueba simple

Consulta de prueba:
SELECT CURRENT_TIMESTAMP() as current_time,
       @@project_id as project_id,
       "conexion_exitosa" as status
```

**Resultado esperado:** Se muestra un mensaje de conexion exitosa y el ID del proyecto.

---

## 🚀 Step 4: Access Public Datasets

Acceda al conjunto de datos publico de Google (muestra de E-commerce GA4):

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Access Public Datasets",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, verifique el acceso al conjunto de datos público de BigQuery
(muestra de E-commerce GA4).

Consulta de prueba:
SELECT
    COUNT(*) as event_count,
    COUNT(DISTINCT user_pseudo_id) as unique_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210101`

Por favor, muestre los resultados.
```

**Resultado esperado:** Se muestran el recuento de eventos y el recuento de usuarios del conjunto de datos de muestra de GA4.

---

## ⚠️ Problemas comunes y soluciones

Utilice AskQuestion para seleccionar el problema y luego siga las indicaciones.

**Configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "gcloud: command not found"},
      {"id": "trouble_2", "label": "File xxx was not found"},
      {"id": "trouble_3", "label": "403 Forbidden / Permission denied"},
      {"id": "trouble_4", "label": "Reauthentication needed"}
    ]
  }]
}
```


### Problema 1: "gcloud: command not found"
**Causa:** gcloud CLI no esta instalado
**Prompt de solucion:**
```
Por favor, muestre cómo instalar gcloud CLI (Google Cloud SDK).
Proporcione los pasos para macOS.
```

### Problema 2: "File xxx was not found"
**Causa:** La variable de entorno GOOGLE_APPLICATION_CREDENTIALS apunta a una ruta invalida
**Prompt de solucion:**
```
Por favor, verifique la variable de entorno GOOGLE_APPLICATION_CREDENTIALS.
Si tiene un valor inválido, muestre cómo borrarlo.
```

### Problema 3: "403 Forbidden / Permission denied"
**Causa:** No tiene permisos de BigQuery
**Prompt de solucion:**
```
Por favor, indique los permisos IAM necesarios para acceder a BigQuery.
Además, muestre cómo verificar los permisos configurados en la cuenta actual.
```

### Problema 4: "Reauthentication needed"
**Causa:** El token de autenticacion ha expirado
**Prompt de solucion:**
```
El token de autenticación de BigQuery ha expirado.
Por favor, ejecute la reautenticación.
```

### Resetting ADC Authentication
Si `GOOGLE_APPLICATION_CREDENTIALS` apunta a una ruta antigua:
```bash
unset GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```

---

## ✅ Punto de control
- [ ] gcloud CLI is installed
- [ ] Authentication completed with gcloud auth login
- [ ] ADC configured with gcloud auth application-default login
- [ ] BigQuery client initialized
- [ ] Test query executed successfully
- [ ] Accessed public dataset (GA4 Sample)

---

## 📚 Suplementario: Multi-project environment

When managing multiple GCP projects:

```
Por favor, muestre cómo crear perfiles de configuración de gcloud
para administrar múltiples proyectos de GCP.

Ejemplo:
- project-a: entorno de desarrollo
- project-b: entorno de producción

También muestre cómo cambiar entre perfiles.
```


---

## 📋 Vista previa de entregables

Los entregables de esta leccion son salidas de terminal.

### Ejemplo de salida esperada
```
┌─────────────────────────────────────┐
│  Resultado de la ejecución               │
│  Estado: ✅ Éxito                        │
│  Registros procesados: N                 │
└─────────────────────────────────────┘
```

> 💡 Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-8-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-8-2
- finish → Finalizar
