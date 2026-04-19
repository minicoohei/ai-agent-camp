# NotebookLM - API notebooks

Use the NotebookLM Enterprise API to create or fetch notebooks.

## Required inputs
- Project number (GCP project number)
- Location (default: `global`)
- Endpoint location (default: `global-`, `us-`, `eu-`)

## Auth
- Default: `gcloud auth print-access-token`
- Override: `NOTEBOOKLM_ACCESS_TOKEN` or `--access-token`

## Usage

### Create a notebook
```bash
uv run python tools/notebooklm_cli.py create \
  --title "My Notebook" \
  --project-number "123456789012" \
  --location "global" \
  --endpoint-location "global-"
```

### Get a notebook
```bash
uv run python tools/notebooklm_cli.py get \
  --notebook-id "NOTEBOOK_ID" \
  --project-number "123456789012" \
  --location "global" \
  --endpoint-location "global-"
```

### List recently viewed notebooks
```bash
uv run python tools/notebooklm_cli.py list-recent \
  --project-number "123456789012" \
  --location "global" \
  --endpoint-location "global-" \
  --page-size 50
```

## Tips
- Use `--raw` to print the raw API response.
- You can set defaults via environment variables:
  - `NOTEBOOKLM_PROJECT_NUMBER`
  - `NOTEBOOKLM_LOCATION`
  - `NOTEBOOKLM_ENDPOINT_LOCATION`
  - `NOTEBOOKLM_ACCESS_TOKEN`
