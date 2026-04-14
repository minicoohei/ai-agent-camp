---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Tener una cuenta de Google", "Navegador disponible"]
level: "beginner"
tags: ["setup", "bigquery", "gcp", "gcloud"]
---

# Configuración de autenticación BigQuery / GCP

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-bigquery` para mostrar el progreso
2. Detectar automáticamente la instalación existente de gcloud CLI:
   - Ejecutar `gcloud --version`
   - Si gcloud CLI ya está instalado y autenticado, saltar al Step 4 (prueba de conexión)
   - Si no está instalado, comenzar desde el Step 1

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar gcloud CLI, autenticarse con Application Default Credentials (ADC) y ejecutar consultas SQL en BigQuery |
| Duración | ~15 minutos |
| Requisitos previos | Tener una cuenta de Google y un navegador disponible |
| Nivel de operación | Pocos comandos CLI + autenticación por navegador (la IA le guía en cada paso) |

**Flujo de la sesión:**
1. Instalar gcloud CLI (la IA le guía en cada paso)
2. Iniciar sesión con su cuenta de Google (el navegador se abre automáticamente)
3. Configurar un proyecto de GCP (la IA le guía)
4. Configurar Application Default Credentials (un solo comando)
5. Prueba de conexión con BigQuery (la IA lo ejecuta automáticamente)

> **Sobre los costos**: BigQuery ofrece hasta 1 TB de consultas gratuitas al mes. El curso utiliza conjuntos de datos públicos, por lo que los costos son prácticamente nulos. Google le notificará antes de superar el nivel gratuito.
>
> **Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación antes de la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está preparado/a?",
    "options": [
      {"id": "ready", "label": "¡Preparado/a! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(check_prereq -> Indicar: "Si puede iniciar sesión en un navegador con una cuenta de Google, está listo/a. BigQuery es gratuito hasta 1 TB de consultas al mes, por lo que el uso durante el curso es prácticamente gratuito.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Instalación de gcloud CLI

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Windows / Linux)
2. Ejecutar `gcloud --version` para verificar si ya está instalado
3. Si ya está instalado, saltar al Step 2
4. Si no está instalado, guiar al usuario con los pasos de instalación según el SO

**Mac (se recomienda Homebrew):**
```bash
brew install google-cloud-sdk
```

**Mac (si Homebrew no está disponible) / Windows:**
Descargar el instalador a través del navegador:
```bash
# Mac:
open https://cloud.google.com/sdk/docs/install
# Windows:
start https://cloud.google.com/sdk/docs/install
```

**Verificación posterior a la instalación:**
```bash
gcloud --version
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 1: Instalación de gcloud CLI",
  "questions": [{
    "id": "install_status",
    "prompt": "Indique el estado de su instalación de gcloud CLI:",
    "options": [
      {"id": "installed", "label": "Instalado (o ya lo tenía instalado)"},
      {"id": "homebrew_issue", "label": "No puedo usar Homebrew (Mac)"},
      {"id": "windows_help", "label": "Necesito ayuda con las instrucciones de Windows"},
      {"id": "install_error", "label": "Obtuve un error durante la instalación"}
    ]
  }]
}
```

(installed -> Verificar con `gcloud --version`, luego ir al Step 2)
(homebrew_issue -> Indicar: "Abra https://cloud.google.com/sdk/docs/install en su navegador y descargue el instalador para macOS. Extraiga el archivo descargado y ejecute ./install.sh para instalarlo.")
(windows_help -> Indicar: "Abra https://cloud.google.com/sdk/docs/install en su navegador y descargue el instalador de Windows (.exe). Haga doble clic en el archivo descargado y siga las instrucciones en pantalla. Después de la instalación, abra una nueva terminal (Símbolo del sistema o PowerShell).")
(install_error -> Verificar el mensaje de error e identificar la causa. Si el PATH no está configurado, indicar al usuario que ejecute `source ~/.zshrc` o abra una nueva terminal)

---

## Step 2: Configuración del proyecto GCP

**Lo que hace la IA:**
1. Ejecutar `gcloud auth login` para iniciar la autenticación de Google en el navegador
2. El navegador se abre automáticamente, solicitándole que inicie sesión con su cuenta de Google

```bash
gcloud auth login
```

**Instrucciones de autenticación por navegador para el usuario:**

```text
El navegador se abrirá automáticamente. Siga estos pasos para autenticarse:

┌─────────────────────────────────────────────────────────────┐
│ 1. Seleccione su cuenta de Google e inicie sesión           │
│ 2. "Google Cloud SDK solicita acceso"                       │
│    → Haga clic en "Permitir"                                │
│ 3. Cuando aparezca "Autenticación completada", cierre el    │
│    navegador                                                │
│ 4. Regrese a la terminal para ver el mensaje de éxito       │
└─────────────────────────────────────────────────────────────┘
```

**Después de la autenticación, configure el proyecto:**
```bash
# Listar proyectos existentes
gcloud projects list

# Configurar el proyecto (reemplace PROJECT_ID con su ID real)
gcloud config set project PROJECT_ID
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Configuración del proyecto GCP",
  "questions": [{
    "id": "auth_status",
    "prompt": "¿Completó la autenticación de la cuenta de Google en el navegador?",
    "options": [
      {"id": "auth_done", "label": "¡Autenticación completada!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "auth_denied", "label": "Obtuve un error en la pantalla de autenticación"},
      {"id": "no_project", "label": "No tengo un proyecto GCP (quiero crear uno)"}
    ]
  }]
}
```

(auth_done -> Mostrar la lista de proyectos con `gcloud projects list`. Si hay un proyecto existente disponible, indicar al usuario que ejecute `gcloud config set project PROJECT_ID` e ir al Step 3)
(browser_not_open -> Indicar: "Copie la URL que aparece en la terminal y péguela en la barra de direcciones del navegador.")
(auth_denied -> Indicar: "Intente usar el modo incógnito/navegación privada del navegador. Si está bloqueado por la cuenta de su empresa, intente con una cuenta personal de Google.")
(no_project -> Indicar: "Vamos a crear un nuevo proyecto GCP. Ejecute el siguiente comando: `gcloud projects create PROJECT_ID --name='Nombre del proyecto'` (PROJECT_ID puede ser cualquier nombre con caracteres alfanuméricos y guiones, por ejemplo: `my-bigquery-lab`). Alternativamente, puede crear un nuevo proyecto en https://console.cloud.google.com.")

---

## Step 3: Configuración de Application Default Credentials (ADC)

**Lo que hace la IA:**

1. Ejecutar el comando de configuración de ADC:
```bash
gcloud auth application-default login
```

2. El navegador se abrirá nuevamente para crear las credenciales de ADC (misma autenticación por navegador que en el Step 2)

**Mensaje para mostrar al usuario:**
```text
El navegador se abrirá una vez más. Esto es para crear las credenciales de
autenticación (ADC) para que aplicaciones como Python puedan conectarse a BigQuery.

┌─────────────────────────────────────────────────────────────┐
│ 1. Seleccione su cuenta de Google e inicie sesión           │
│ 2. Haga clic en "Permitir"                                  │
│ 3. Si aparece "Credentials saved to file: ..." en la        │
│    terminal, la operación fue exitosa                        │
└─────────────────────────────────────────────────────────────┘
```

3. Después de configurar ADC, habilitar la API de BigQuery:
```bash
gcloud services enable bigquery.googleapis.com
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Configuración de ADC",
  "questions": [{
    "id": "adc_status",
    "prompt": "¿Completó la autenticación ADC y la activación de la API de BigQuery?",
    "options": [
      {"id": "adc_done", "label": "¡Se mostró 'Credentials saved to file'!"},
      {"id": "adc_browser_issue", "label": "La autenticación del navegador no funciona"},
      {"id": "api_enable_error", "label": "Obtuve un error al habilitar la API de BigQuery"},
      {"id": "adc_what", "label": "¿Qué es ADC?"}
    ]
  }]
}
```

(adc_done -> Ir al Step 4)
(adc_browser_issue -> Indicar: "Siga los mismos pasos de autenticación por navegador que en el Step 2. Si no funciona, copie la URL que aparece en la terminal y péguela en su navegador.")
(api_enable_error -> Indicar: "Vamos a verificar el mensaje de error. Si dice 'permission denied', necesita permisos de propietario del proyecto. También puede habilitarla manualmente en https://console.cloud.google.com/apis/library/bigquery.googleapis.com.")
(adc_what -> Explicar: "ADC (Application Default Credentials) es un mecanismo para que aplicaciones como scripts de Python encuentren automáticamente las credenciales de autenticación de GCP. Una vez configurado, puede conectarse a BigQuery de forma segura sin especificar claves de API en su código.")

---

## Step 4: Prueba de conexión con BigQuery

**Lo que la IA ejecuta automáticamente:**

1. Verificar que los paquetes necesarios estén instalados:
```bash
pip install google-cloud-bigquery
```

2. Ejecutar la prueba de conexión con BigQuery:
```python
from google.cloud import bigquery

client = bigquery.Client()
query = "SELECT COUNT(*) as cnt FROM `bigquery-public-data.samples.shakespeare`"
result = client.query(query).result()
for row in result:
    print(f"¡Conexión exitosa! Dataset Shakespeare: {row.cnt} filas")
```

3. Mostrar una AskQuestion según el resultado de la prueba:

**En caso de éxito:**
```text
¡La prueba de conexión con BigQuery fue exitosa!

Resultado de la prueba: La consulta al conjunto de datos público (Shakespeare) se ejecutó correctamente.
Ahora puede usar BigQuery para ejecución de SQL, análisis de datos y EDA.
```

**En caso de fallo — AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de conexión con BigQuery. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Ejecutar la prueba de nuevo"},
      {"id": "reauth", "label": "Rehacer la autenticación (volver al Step 2)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(reauth -> Volver al Step 2)
(show_error -> Mostrar el mensaje de error e indicar la causa y la solución)
(skip_test -> Indicar: "Se omitió la prueba de conexión. Puede verificarla más tarde con /check-setup.")

---

## Problemas comunes y soluciones

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el tipo de problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda a su situación",
    "options": [
      {"id": "trouble_install", "label": "Obtengo errores al instalar gcloud CLI"},
      {"id": "trouble_auth", "label": "La autenticación por navegador falla"},
      {"id": "trouble_project", "label": "No tengo un proyecto GCP / no puedo seleccionarlo"},
      {"id": "trouble_api", "label": "No puedo habilitar la API de BigQuery"},
      {"id": "trouble_permission", "label": "Obtengo un error 'permission denied'"},
      {"id": "trouble_package", "label": "Error con el paquete google-cloud-bigquery"},
      {"id": "trouble_cost", "label": "Me preocupan los costos"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: Error en la instalación de gcloud CLI
**Causa**: Problemas con Homebrew, PATH no configurado, permisos insuficientes
**Lo que hace la IA**:
1. Verificar el estado de instalación con `which gcloud`
2. Si hay errores de Homebrew, ejecutar `brew doctor` para identificar el problema
3. Si el PATH no está configurado, indicar al usuario que ejecute `source ~/.zshrc` o abra una nueva terminal
4. Si aún no se resuelve, guiar la instalación manual a través del navegador

### Problema 2: La autenticación por navegador falla
**Causa**: El navegador no se abre, políticas de seguridad corporativas, permisos de cuenta
**Lo que hace la IA**:
1. Indicar al usuario que pegue manualmente la URL de la terminal en el navegador
2. Sugerir la autenticación en modo incógnito
3. Guiar a través de `gcloud auth login --no-launch-browser` para la entrada manual de URL

### Problema 3: No hay proyecto GCP
**Causa**: Es la primera vez que se usa GCP
**Indicación de la IA**: "Puede crear un proyecto con `gcloud projects create my-bigquery-lab --name='BigQuery Lab'`. Alternativamente, vaya a https://console.cloud.google.com y cree un nuevo proyecto a través de 'Seleccionar un proyecto' > 'Nuevo proyecto' en la parte superior de la página."

### Problema 4: No se puede habilitar la API de BigQuery
**Causa**: Faltan permisos de propietario del proyecto, la facturación no está habilitada
**Lo que hace la IA**:
1. Volver a ejecutar `gcloud services enable bigquery.googleapis.com`
2. Verificar el mensaje de error; si es necesario habilitar la facturación, dirigir a https://console.cloud.google.com/billing
3. Si es un problema de permisos, recomendar solicitar al propietario del proyecto que otorgue permisos

### Problema 5: Error "Permission Denied"
**Causa**: ADC no configurado correctamente, API de BigQuery deshabilitada, permisos de proyecto insuficientes
**Lo que hace la IA**:
1. Verificar el estado de ADC con `gcloud auth application-default print-access-token`
2. Si ADC no está configurado, volver a ejecutar `gcloud auth application-default login`
3. Verificar si la API de BigQuery está habilitada con `gcloud services list --enabled`

### Problema 6: Error con el paquete google-cloud-bigquery
**Causa**: Paquete no instalado, incompatibilidad de versiones
**Lo que hace la IA**: Ejecutar automáticamente `pip install google-cloud-bigquery`. Si el venv está dañado, indicar al usuario que lo recree con `bash tools/scripts/setup.sh`

### Problema 7: Preocupación por los costos
**Indicación de la IA**: "BigQuery ofrece hasta 1 TB de consultas gratuitas al mes. El acceso a los conjuntos de datos públicos utilizados en el curso también es gratuito. Google le notificará antes de superar el nivel gratuito. Para el uso a nivel de curso, el nivel gratuito es más que suficiente."

### Problema 8: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar al usuario la solución

---

## Punto de control
- [ ] gcloud CLI está instalado
- [ ] La autenticación con la cuenta de Google está completada
- [ ] El proyecto GCP está configurado
- [ ] Application Default Credentials está configurado
- [ ] La API de BigQuery está habilitada
- [ ] La prueba de conexión con BigQuery fue exitosa

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de autenticación BigQuery / GCP está completa! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_bigquery", "label": "Aprender conexión y configuración de autenticación de BigQuery (/start-8-1)"},
      {"id": "try_eda", "label": "Probar a ejecutar EDA (/start-8-2)"},
      {"id": "setup_other", "label": "Ir a otra configuración (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_bigquery -> Dirigir a /start-8-1
- try_eda -> Dirigir a /start-8-2
- setup_other -> Dirigir a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-bigquery` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, aprenda la conexión y configuración de autenticación de BigQuery con `/start-8-1`"
