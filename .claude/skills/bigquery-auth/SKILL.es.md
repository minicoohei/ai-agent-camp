---
name: bigquery-auth
description: "Habilidad para configurar la autenticacion de BigQuery por proyecto de GCP. Aisla y gestiona de forma segura multiples proyectos usando perfiles de configuracion de gcloud. Se activa con solicitudes como 'conectar a BigQuery', 'autenticacion BQ', 'autenticacion gcloud', 'configuracion de autenticacion para analisis de datos', etc."
triggers:
  - bigquery-auth
  - autenticacion BigQuery
  - conectar a BQ
  - autenticacion gcloud
  - autenticacion para analisis de datos
  - conexion BigQuery
  - autenticacion GCP
  - BigQuery authentication
  - BigQuery認証
---

## Palabras Clave de Activacion
"autenticacion BigQuery", "conectar a BQ", "autenticacion para analisis de datos", "autenticacion gcloud"

# Autenticacion de BigQuery (Basada en Proyecto)

Habilidad para crear perfiles de configuracion de gcloud por proyecto de GCP y realizar la autenticacion de BigQuery.

## Flujo de Trabajo

1. El usuario dice "Quiero usar BigQuery" o "Quiero ver datos de {proyecto}"
2. **Confirmar el ID del proyecto GCP** (requerido)
3. Verificar perfiles de configuracion existentes
4. Crear un nuevo perfil si es necesario
5. Guiar a traves de la autenticacion del navegador
6. Ejecutar prueba de conexion

## Pasos de Autenticacion

### Paso 1: Verificar Perfiles de Configuracion

```bash
gcloud config configurations list
```

Mostrar perfiles existentes y verificar si hay uno para el proyecto objetivo.

### Paso 2: Crear Perfil (si es nuevo)

```bash
# Crear perfil
gcloud config configurations create {NOMBRE_PERFIL}

# Configurar proyecto
gcloud config set project {PROJECT_ID}
```

### Paso 3: Autenticacion gcloud

```bash
# Autenticacion principal (abre el navegador)
gcloud auth login

# Autenticacion para Python SDK (abre el navegador)
gcloud auth application-default login --quiet
```

**Nota**: Ambos comandos requieren autenticacion en el navegador.

### Paso 4: Verificar Autenticacion

```bash
# Verificar perfil actual
gcloud config configurations list

# Verificar proyecto
gcloud config get-value project

# Verificar token ADC
gcloud auth application-default print-access-token
```

### Paso 5: Prueba de Conexion a BigQuery

```python
import os
# Evitar conflictos de variables de entorno
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

from google.cloud import bigquery
client = bigquery.Client(project="{PROJECT_ID}")
datasets = list(client.list_datasets())
print(f"¡Conexion exitosa! {len(datasets)} conjuntos de datos encontrados")
```

## Cambio de Perfiles

```bash
# Listar perfiles
gcloud config configurations list

# Cambiar
gcloud config configurations activate {NOMBRE_PERFIL}
```

## Perfiles Registrados (Plantilla)

### Autenticacion ADC (gcloud login)

| Perfil | ID del Proyecto | Cuenta | Proposito |
|--------|-----------------|--------|-----------|
| `default` | {SU_PROJECT_ID} | {SU_EMAIL} | Predeterminado |
| `{PERFIL_2}` | {PROJECT_ID_2} | {EMAIL_2} | Analisis |

> Reemplace con la informacion de su propio proyecto.

### Autenticacion con Cuenta de Servicio (Proyectos Externos)

| Perfil | ID del Proyecto | Archivo de Clave | Proposito |
|--------|-----------------|------------------|-----------|
| `{PERFIL_SA}` | {SA_PROJECT_ID} | `~/.gcp/{SA_KEY_FILE}.json` | Analisis de proyecto externo |

## Como Usar la Autenticacion con Cuenta de Servicio

Cuando se conecta a proyectos externos con una cuenta de servicio:

```python
import os
from google.cloud import bigquery
from google.oauth2 import service_account

# Autenticar con clave de cuenta de servicio
credentials = service_account.Credentials.from_service_account_file(
    os.path.expanduser("~/.gcp/{SA_KEY_FILE}.json")
)

# Crear cliente BigQuery
client = bigquery.Client(
    project="{SA_PROJECT_ID}",
    credentials=credentials
)

# Prueba de conexion
datasets = list(client.list_datasets())
print(f"¡Conexion exitosa! {len(datasets)} conjuntos de datos encontrados")
```

## Solucion de Problemas

| Error | Causa | Solucion |
|-------|-------|----------|
| File xxx was not found | GOOGLE_APPLICATION_CREDENTIALS es invalido | `unset GOOGLE_APPLICATION_CREDENTIALS` |
| Reauthentication needed | Autenticacion expirada | Ejecutar autenticacion nuevamente |
| Permission denied | Sin permisos de BigQuery | Verificar configuracion de IAM |

## Notas Importantes

### Conflictos de Variables de Entorno

Si la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` esta configurada, tiene prioridad sobre ADC.
Ejecute lo siguiente en codigo Python para evitarlo:

```python
import os
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
```

### Al Usar marimo Notebook

Siga las reglas en `.cursor/rules/notebook.mdc`:
1. Antes de comenzar a trabajar, pregunte "¿Con que proyecto GCP va a trabajar?"
2. Mostrar lista de perfiles con `gcloud config configurations list`
3. Cambiar perfiles segun sea necesario

## Requisitos

- Google Cloud SDK (`gcloud`) instalado
- Capacidad de iniciar sesion en cuenta de Google via navegador
- Permisos de visualizacion de BigQuery en el proyecto objetivo
