---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
prerequisites: ["start-11-1"]
duration: "~35 min"
level: "intermediate"
tags: ["github-actions", "secrets", "google-api"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 11-2: Pruebas automatizadas y despliegue

## 📍 Lo que hara en esta sesion

**Lección 11-2: GitHub Actions e integración con API**!

| Elemento | Contenido |
|------|------|
| Objetivo | Construir pipelines de obtencion y procesamiento automatico de datos usando Secrets en GitHub Actions para integracion con Google API |
| Duracion | ~35 min |
| Habilidades utilizadas | GitHub Actions, Repository Secrets, Google API |
| Requisitos previos | Leccion 11-1 completada, repositorio GitHub |
| Pagina del curso | [Module 11: GitHub Actions](https://ai-agent.camp/es/course/module-11)  como referencia paralela |

**Flujo de la sesion:**
1. Configurar Repository Secrets
2. Llamar APIs desde flujos de trabajo
3. Ejecutar obtención y procesamiento automático de datos

Al final de esta sesion, tendra un pipeline seguro de integracion API usando Secrets.

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

## 🚀 Step 1: Configure Repository Secrets

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Configuración de Repository Secrets",
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
```text
Por favor, explique el procedimiento de configuración de GitHub Repository Secrets.
Ubicación de configuración: Repositorio > Settings > Secrets and variables > Actions
Se configurarán los siguientes Secrets:
- GOOGLE_CREDENTIALS (clave de cuenta de servicio)
- SLACK_WEBHOOK (para notificaciones)
```

**Resultado esperado:** Se explican los pasos de configuracion de Secrets. La configuracion real se realiza en la interfaz web de GitHub.

---

## 🚀 Step 2: Google Authentication Workflow

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Flujo de trabajo de autenticación de Google",
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

> **Recomendación**: Si es posible, priorice Workload Identity Federation (OIDC).  
> Al usar claves de cuenta de servicio, minificar el JSON en una sola línea antes de guardarlo en Secrets lo hace menos propenso a errores.

```yaml
Por favor, cree el archivo .github/workflows/google-auth.yml con el siguiente contenido:

name: Google API Integration

on:
  workflow_dispatch:
    inputs:
      operation:
        description: 'Operación a ejecutar'
        required: true
        default: 'test'
        type: choice
        options:
          - test
          - fetch_data
          - update_sheet

jobs:
  google-operation:
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
          uv add google-auth google-auth-oauthlib google-api-python-client

      - name: Create credentials file
        run: |
          printf '%s' '${{ secrets.GOOGLE_CREDENTIALS }}' > credentials.json
          chmod 600 credentials.json

      - name: Test Google auth
        if: github.event.inputs.operation == 'test'
        run: |
          python -c "
          from google.oauth2 import service_account
          import json

          try:
              creds = service_account.Credentials.from_service_account_file('credentials.json')
              print('¡Autenticación de Google exitosa!')
              print(f'Cuenta de servicio: {creds.service_account_email}')
          except Exception as e:
              print(f'Error de autenticación: {e}')
              exit(1)
          "

      - name: Cleanup credentials
        if: always()
        run: rm -f credentials.json
```

**Resultado esperado:** Se crea un flujo de trabajo para autenticacion segura de Google.

---

## 🚀 Step 3: Data Retrieval Pipeline

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Pipeline de obtención de datos",
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
```text
Por favor, cree el archivo .github/workflows/data-pipeline.yml con el siguiente contenido:

name: Data Pipeline

on:
  schedule:
    - cron: '0 1 * * *'  # Diariamente a las 01:00 UTC
  workflow_dispatch:

jobs:
  data-pipeline:
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
          uv add pandas requests

      - name: Step 1 - Fetch data
        run: |
          python -c "
          import json
          from datetime import datetime

          # Generar datos de ejemplo (en realidad se obtienen de la API)
          data = {
              'timestamp': datetime.now().isoformat(),
              'records': [
                  {'id': 1, 'value': 100},
                  {'id': 2, 'value': 200},
                  {'id': 3, 'value': 300}
              ]
          }

          with open('data.json', 'w') as f:
              json.dump(data, f)

          print('Obtención de datos completada')
          "

      - name: Step 2 - Process data
        run: |
          python -c "
          import json
          import pandas as pd

          with open('data.json', 'r') as f:
              data = json.load(f)

          df = pd.DataFrame(data['records'])
          df['processed_at'] = data['timestamp']

          summary = {
              'total_records': len(df),
              'sum_value': int(df['value'].sum()),
              'avg_value': float(df['value'].mean())
          }

          with open('summary.json', 'w') as f:
              json.dump(summary, f)

          print(f'Procesamiento completado: {summary}')
          "

      - name: Step 3 - Save results
        run: |
          mkdir -p output
          mv data.json output/
          mv summary.json output/
          echo "Results saved to output/"
          ls -la output/

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: pipeline-results-${{ github.run_number }}
          path: output/
          retention-days: 7
```

**Resultado esperado:** Se crea un pipeline de obtencion, procesamiento y almacenamiento de datos.

---

## 🚀 Step 4: Workflow with Notifications

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Flujo de trabajo con notificaciones",
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
```text
Por favor, cree el archivo .github/workflows/notify.yml con el siguiente contenido:

name: Pipeline with Notification

on:
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build-and-notify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run build
        id: build
        run: |
          echo "Building project..."
          echo "status=success" >> $GITHUB_OUTPUT
          echo "Build completed!"

      - name: Run tests
        id: test
        run: |
          echo "Running tests..."
          echo "Tests passed!"

      - name: Send success notification
        if: success()
        run: |
          echo "Sending success notification..."
          # Si el Webhook de Slack está configurado
          # curl -X POST -H 'Content-type: application/json' \
          #   --data '{"text":"Pipeline exitoso: ${{ github.repository }}"}' \
          #   ${{ secrets.SLACK_WEBHOOK }}
          echo "Notification: Pipeline completed successfully!"

      - name: Send failure notification
        if: failure()
        run: |
          echo "Sending failure notification..."
          echo "Notification: Pipeline failed!"

      - name: Summary
        if: always()
        run: |
          echo "## Workflow Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Repository**: ${{ github.repository }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Branch**: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Actor**: ${{ github.actor }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status**: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**Resultado esperado:** Se crea un flujo de trabajo que envia notificaciones despues de completar la compilacion.

---

## 🚀 Step 5: Matrix Build

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Build de matriz",
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
```text
Por favor, cree el archivo .github/workflows/matrix.yml con el siguiente contenido:

name: Matrix Build

on:
  workflow_dispatch:
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
      fail-fast: false

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python version
        run: |
          python --version
          echo "OS: ${{ matrix.os }}"
          echo "Python: ${{ matrix.python-version }}"

      - name: Run tests
        run: |
          python -c "print('Test passed on ${{ matrix.os }} with Python ${{ matrix.python-version }}')"
```

**Resultado esperado:** Se crea un flujo de trabajo para pruebas simultaneas en multiples SO y versiones de Python.

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
      {"id": "trouble_1", "label": "Invalid credentials"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "No se pueden referenciar los Secrets"},
      {"id": "trouble_4", "label": "Los artefactos no se suben"}
    ]
  }]
}
```


### Problema 1: "Invalid credentials"
**Causa:** El valor del Secret es incorrecto o el formato JSON es invalido
**Prompt de solucion:**
```text
Por favor, verifique el valor del Secret GOOGLE_CREDENTIALS.
Copie todo el contenido del archivo JSON y configúrelo.
Verifique que los saltos de línea y espacios estén correctamente incluidos.
```

### Problema 2: "Permission denied"
**Causa:** Permisos insuficientes de la cuenta de servicio
**Prompt de solucion:**
```text
Por favor, verifique los permisos de la cuenta de servicio en Google Cloud Console.
Verifique que las APIs necesarias estén habilitadas.
Verifique que los roles de IAM estén configurados correctamente.
```

### Problema 3: No se pueden referenciar los Secrets
**Causa:** Error tipografico en el nombre del Secret o el Secret no esta configurado
**Prompt de solucion:**
```text
Por favor, verifique el nombre del Secret en Settings > Secrets and variables > Actions del repositorio de GitHub.
Verifique que se esté referenciando en el formato secrets.SECRET_NAME.
```

### Problema 4: Los artefactos no se suben
**Causa:** La ruta no existe o el tamano del archivo excede el limite
**Prompt de solucion:**
```text
Por favor, verifique que el directorio especificado en path exista.
Verifique que el tamaño del archivo no exceda el límite (500MB).
```

---

## ✅ Punto de control
- [ ] Comprende el procedimiento de configuración de Repository Secrets
- [ ] google-auth.yml ha sido creado
- [ ] data-pipeline.yml ha sido creado
- [ ] notify.yml ha sido creado
- [ ] matrix.yml ha sido creado
- [ ] Comprende cómo manejar Secrets de forma segura


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 .github/workflows/
└── {workflow}.yml  (flujo de trabajo de GitHub Actions)
```

### Comandos de verificacion
```bash
# Lista de archivos de flujo de trabajo
ls -la .github/workflows/

# Verificar contenido del archivo
cat .github/workflows/{workflow}.yml

# Verificar estado de ejecución en GitHub
gh run list --limit 5
```

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```text
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestran el estado completado/incompleto y los elementos faltantes.

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-12-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-12-1
- finish → Finalizar
