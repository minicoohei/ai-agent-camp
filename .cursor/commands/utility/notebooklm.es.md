---
nonInteractiveMode: compliant
---

# NotebookLM - Notebooks de API

Utilice la API de NotebookLM Enterprise para crear u obtener notebooks.

## Datos de entrada requeridos
- Número de proyecto (número de proyecto de GCP)
- Ubicación (por defecto: `global`)
- Ubicación del endpoint (por defecto: `global-`, `us-`, `eu-`)

## Autenticación
- Por defecto: `gcloud auth print-access-token`
- Alternativa: `NOTEBOOKLM_ACCESS_TOKEN` o `--access-token`

## Uso

### Crear un notebook
```bash
uv run python tools/notebooklm_cli.py create \
  --title "My Notebook" \
  --project-number "123456789012" \
  --location "global" \
  --endpoint-location "global-"
```

### Obtener un notebook
```bash
uv run python tools/notebooklm_cli.py get \
  --notebook-id "NOTEBOOK_ID" \
  --project-number "123456789012" \
  --location "global" \
  --endpoint-location "global-"
```

### Listar notebooks vistos recientemente
```bash
uv run python tools/notebooklm_cli.py list-recent \
  --project-number "123456789012" \
  --location "global" \
  --endpoint-location "global-" \
  --page-size 50
```

## Consejos
- Utilice `--raw` para imprimir la respuesta cruda de la API.
- Puede establecer valores por defecto mediante variables de entorno:
  - `NOTEBOOKLM_PROJECT_NUMBER`
  - `NOTEBOOKLM_LOCATION`
  - `NOTEBOOKLM_ENDPOINT_LOCATION`
  - `NOTEBOOKLM_ACCESS_TOKEN`
