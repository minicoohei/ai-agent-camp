# BigQuery Auth - Autenticación de BigQuery a nivel de proyecto

Este comando utiliza Cursor Browser para configurar la autenticación de BigQuery por proyecto de GCP. Aprovecha los perfiles de configuración de gcloud para gestionar múltiples proyectos de forma segura.

## Funcionalidades

- **Aislamiento de proyectos**: Gestione múltiples proyectos de GCP de forma segura con perfiles de configuración de gcloud
- **Autenticación por navegador**: Guía la autenticación a través de Google Cloud Console
- **Application-default credentials**: Obtenga credenciales utilizables desde el SDK de Python
- **Soporte de variables de entorno**: Evite conflictos con `GOOGLE_APPLICATION_CREDENTIALS` existentes

## Pasos

### Fase 1: Confirmar parámetros

Confirme la siguiente información de la entrada del usuario:

1. **ID del proyecto de GCP** (obligatorio):
   - Ejemplo: `my-project-123`, `my-gcp-project`

2. **Nombre del perfil** (opcional, predeterminado: generado automáticamente a partir del ID del proyecto):
   - Ejemplo: `my-profile`, `my-dev`, `default`

3. **Cuenta de Google** (opcional, seleccionada por el usuario)

### Fase 2: Verificar perfiles de configuración existentes

```bash
gcloud config configurations list
```

Muestre los perfiles existentes y confirme:
- Si ya existe un perfil para el proyecto objetivo
- Cuál es el perfil activo actualmente

**Guíe al usuario:**
```
[Perfiles de configuración existentes]
NAME     IS_ACTIVE  ACCOUNT                     PROJECT
default  True       user@example.com            my-project
...

¿Tiene un perfil para el proyecto objetivo?
- "Crear nuevo": Crear un nuevo perfil
- "{nombre_perfil}": Usar un perfil existente
```

### Fase 3: Crear perfil de configuración (si es nuevo)

```bash
# Crear un nuevo perfil
gcloud config configurations create {PROFILE_NAME}

# Configurar el ID del proyecto
gcloud config set project {PROJECT_ID}
```

### Fase 4: Autenticación por navegador (Cursor Browser)

#### Paso 1: gcloud auth login

```bash
gcloud auth login
```

Cuando se abra el navegador, verifique el estado de la página con `browser_snapshot`.

**Guíe al usuario:**
```
[Autenticación de cuenta de Google]
El navegador se ha abierto.
1. Seleccione la cuenta de Google que desea utilizar
2. Otorgue acceso a "Google Cloud SDK"
3. Está completo cuando se muestre "Puede cerrar esta ventana"

Ingrese "listo" cuando la autenticación esté completa.
```

#### Paso 2: application-default credentials

```bash
gcloud auth application-default login --quiet
```

Cuando el navegador se abra nuevamente, guíe la autenticación.

**Guíe al usuario:**
```
[Autenticación de Application Default Credentials]
El navegador se ha abierto.
1. Seleccione la misma cuenta de Google
2. Otorgue acceso a "Google Auth Library"
3. La autenticación es exitosa cuando se muestra un mensaje de finalización

Ingrese "listo" cuando la autenticación esté completa.
```

### Fase 5: Verificar autenticación

```bash
# Verificar estado de autenticación
gcloud auth list

# Verificar proyecto
gcloud config get-value project

# Verificar token ADC (OK si no hay error)
gcloud auth application-default print-access-token 2>/dev/null && echo "Autenticación ADC OK" || echo "Autenticación ADC fallida"
```

### Fase 6: Prueba de conexión a BigQuery

```python
# Limpiar variables de entorno antes de la prueba
import os
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

from google.cloud import bigquery
client = bigquery.Client(project="{PROJECT_ID}")
datasets = list(client.list_datasets())
print(f"¡Conexión exitosa! {len(datasets)} conjuntos de datos encontrados")
```

### Fase 7: Informe de finalización

**Informe al usuario:**
```
[Autenticación de BigQuery completa]

Perfil: {PROFILE_NAME}
Proyecto: {PROJECT_ID}
Cuenta: {ACCOUNT}
Conexión a BigQuery: Exitosa

Comando para cambiar de perfil:
   gcloud config configurations activate {PROFILE_NAME}

Nota: Si la variable de entorno GOOGLE_APPLICATION_CREDENTIALS está configurada,
   ejecute `del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]` en el código Python
   o desactívela antes de usar.
```

## Ejemplos de uso

### Uso básico
```
/bigquery-auth my-gcp-project
```

### Especificar nombre de perfil
```
/bigquery-auth my-dev-project --profile my-dev
```

### Cambiar de perfil
```
/bigquery-auth --switch my-profile
```

## Perfiles de GCP disponibles (referencia)

| Nombre del perfil | ID del proyecto | Propósito |
|-------------------|-----------------|-----------|
| `default` | - | Entorno predeterminado |
| `my-profile` | my-gcp-project | Análisis de datos en producción |
| `my-dev` | my-dev-project | Análisis de desarrollo |

## Solución de problemas

### Error: "File xxx was not found"
- La variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` apunta a una ruta inválida
- Solución: `unset GOOGLE_APPLICATION_CREDENTIALS` o eliminarla en Python

### Error: "Reauthentication is needed"
- La autenticación ha expirado
- Solución: Ejecute `/bigquery-auth {PROJECT_ID}` nuevamente

### Error: "User does not have permission"
- No tiene permisos de acceso a BigQuery
- Solución: Verifique los permisos IAM en la consola de GCP

## Notas

- **Prevenir olvido de cambio de perfil**: Verifique el perfil actual con `gcloud config configurations list` antes de comenzar a trabajar
- **Conflictos de variables de entorno**: Si `GOOGLE_APPLICATION_CREDENTIALS` está configurada, tiene prioridad sobre ADC
- **Al usar marimo notebook**: Siga las reglas en notebook.mdc y siempre verifique el entorno de GCP antes de comenzar a trabajar
