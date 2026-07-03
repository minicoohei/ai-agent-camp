---
description: "Lesson command — Setup de Google Ads API"
duration: "~180 min (la mayoría es la aprobación del API Center)"
prerequisites: ["cuenta de Google Ads API"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-25"]
---

# /setup-google-ads -- Setup de Google Ads API

> El viaje de 3 días para de verdad llamar a Google Ads API v21 (Python SDK). Necesitas MCC + Basic Access + refresh_token OAuth.

**Punto clave**: El Basic Access puede tardar un día hábil. El OAuth requiere flujo web

## Pasos de setup

1. Crea una Manager Account (MCC) de Google Ads

   ```bash
   https://ads.google.com/aw/signup/manager
   ```

2. Solicita el Developer Token en el API Center — `MCC → Tools → API Center → Apply for Basic Access`

3. Crea un proyecto GCP y un OAuth Client (web)

   ```bash
   https://console.cloud.google.com/apis/credentials
   ```

4. Genera un refresh_token con el flujo web (listener local) — `# Usa Google OAuth Playground o `gcloud auth application-default login` para emitir un refresh_token (o tu propio helper OAuth)`

5. Guarda 5 secrets en Keychain + GitHub Secrets — `GOOGLE_ADS_DEVELOPER_TOKEN / CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / LOGIN_CUSTOMER_ID`

6. Prueba con el SDK de Python (dry-run validate_only=True) — `python -c "from google.ads.googleads.client import GoogleAdsClient; print('SDK loaded ok')"  # detalles del dry-run en la próxima lección`

## Tropezones

- Los Test Accounts no pueden lanzar anuncios pagos. Cambia a producción cuando aprueben Basic Access
- Pon siempre el estado de EU political advertising en campaign_operation (`DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`)
- Aun con validate_only=True hay que usar un batch atómico de `mutate` (budget + campaign con temp resource_name `-1`); si no, el chequeo de resource_name lo rechaza

## Modo no interactivo

El OAuth en navegador es obligatorio — no termina bajo `claude -p` / `cursor-agent --print`. Re-ejecuta en modo interactivo.

## Slides relacionadas

- aiagent-course Module 25: https://ai-agent.camp/es/course/module-25?slideId=module-overview
