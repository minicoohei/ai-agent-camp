---
nonInteractiveMode: incompatible
---

# Configuración de cuenta de Google (para Calendar/Drive)

Asiste con la configuración de la integración de Calendar/Drive de cuentas personales de Google.
**Puede reutilizar el mismo OAuth Client ID usado para Gmail.**

## Por qué se necesita una configuración separada

Gmail/Calendar/Drive requieren cada uno diferentes scopes (permisos).
Este script autentica los tres scopes juntos.

---

## Verificación de requisitos previos

### 1. Verificar GitHub CLI

```bash
gh auth status
```

Si no está autenticado:
```bash
gh auth login
```

### 2. Verificar OAuth Client ID

Pregunte al usuario:
"¿Ya ha creado un OAuth Client ID en Google Cloud Console?"

**Si no lo ha hecho, guíelo de la siguiente manera:**

Consulte `docs/GMAIL_OAUTH_SETUP.md`, o vaya a https://console.cloud.google.com/ y:

1. Cree un proyecto (solo la primera vez)
2. **Habilite Gmail API / Calendar API / Drive API**
3. Configure la pantalla de consentimiento OAuth (externa, solo campos obligatorios)
4. Credenciales -> Crear OAuth Client ID (**Aplicación de escritorio**)
5. Copie el Client ID y el Secret

---

## Ejecutar configuración

> **Importante**: Dado que se requiere autenticación por navegador, **ejecute esto directamente en la terminal.**
> La ejecución por pipe desde el chat de Cursor expirará por tiempo de espera.

```bash
python scripts/setup_google_account.py --label <nombre_cuenta>
```

### Ejemplos

```bash
python scripts/setup_google_account.py --label my-account
python scripts/setup_google_account.py --label work
python scripts/setup_google_account.py --label work
```

### Entrada durante la ejecución

1. Client ID (copiar de Google Cloud Console)
2. Client Secret (igual)
3. Iniciar sesión en Google vía navegador -> Otorgar permiso

---

## Configuración posterior a la instalación

### 1. Verificar Secrets

```bash
gh secret list --repo <owner/repo> | grep GOOGLE
```

Se registrarán los siguientes Secrets:
- `GOOGLE_<LABEL>_CLIENT_ID`
- `GOOGLE_<LABEL>_CLIENT_SECRET`
- `GOOGLE_<LABEL>_REFRESH_TOKEN`

### 2. Actualizar GOOGLE_ACCOUNTS_CONFIG

**Esto debe actualizarse cada vez que agregue una cuenta:**

```bash
# Ejemplo: 2 cuentas - my-account y work
gh secret set GOOGLE_ACCOUNTS_CONFIG \
  --body '{"accounts":[{"label":"my-account","type":"oauth"},{"label":"work","type":"oauth"}]}' \
  --repo <owner/repo>
```

### 3. Configurar ID de carpeta de Drive (opcional)

Si obtiene archivos de Drive, configure el ID de la carpeta objetivo:

```bash
gh secret set GOOGLE_MYACCOUNT_DRIVE_FOLDER_ID \
  --body '<ID de carpeta de Google Drive>' \
  --repo <owner/repo>
```

Alternativamente, puede incluir el ID de la carpeta en GOOGLE_ACCOUNTS_CONFIG:

```json
{
  "accounts": [
    {
      "label": "my-account",
      "type": "oauth",
      "drive_folder_id": "1234567890abcdef"
    }
  ]
}
```

### 4. Agregar variables de entorno al workflow

Agregue variables de entorno para la nueva cuenta en `.github/workflows/fetch_data.yml`:

```yaml
env:
  # Para Calendar/Drive
  GOOGLE_<LABEL>_CLIENT_ID: ${{ secrets.GOOGLE_<LABEL>_CLIENT_ID }}
  GOOGLE_<LABEL>_CLIENT_SECRET: ${{ secrets.GOOGLE_<LABEL>_CLIENT_SECRET }}
  GOOGLE_<LABEL>_REFRESH_TOKEN: ${{ secrets.GOOGLE_<LABEL>_REFRESH_TOKEN }}
  GOOGLE_<LABEL>_DRIVE_FOLDER_ID: ${{ secrets.GOOGLE_<LABEL>_DRIVE_FOLDER_ID }}
```

### 5. Confirmar y enviar cambios

```bash
git add .github/workflows/fetch_data.yml
git commit -m "feat: Add Google account <label> for Calendar/Drive"
git push
```

---

## Verificación

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

Verifique los registros:
```
Starting Multi-Calendar fetch (OAuth mode)...
Processing Calendar for account: my-account
[my-account] OAuth authentication successful for Calendar
[my-account] Fetched 5 calendar events
Starting Multi-Drive fetch (OAuth mode)...
Processing Drive for account: my-account
[my-account] OAuth authentication successful for Drive
[my-account] Fetched 10 Drive files
```

---

## Estructura del directorio de salida

```
output/
├── calendar/
│   ├── my-account/
│   │   ├── 2026-01-16_events.md
│   │   └── 2026-01-17_events.md
│   └── work/
│       └── 2026-01-16_events.md
└── drive/
    ├── my-account/
    │   ├── docs/
    │   ├── sheets/
    │   └── slides/
    └── work/
        └── docs/
```

---

## Solución de problemas

### Aparece el mensaje "Esta aplicación no está verificada"

Esto es normal. Haga clic en "Avanzado" -> "Ir a [nombre de la aplicación]" para continuar.

### Ocurre un error de autenticación

Verifique lo siguiente:
1. ¿Están habilitadas las API de Gmail / Calendar / Drive?
2. ¿Está configurada la pantalla de consentimiento OAuth?
3. ¿Son correctos el Client ID/Secret?

### Falla el registro en GitHub Secrets

```bash
gh auth status
```
Verifique el estado de autenticación. Si no está autenticado, ejecute `gh auth login`.

### Los archivos de Drive no se obtienen

- Verifique que `drive_folder_id` o `GOOGLE_<LABEL>_DRIVE_FOLDER_ID` esté configurado
- Verifique que tenga permisos de lectura para la carpeta objetivo

### Error "multiple remotes detected"

```bash
python scripts/setup_google_account.py --label my-account --repo owner/repo
```
Especifique el repositorio explícitamente.
