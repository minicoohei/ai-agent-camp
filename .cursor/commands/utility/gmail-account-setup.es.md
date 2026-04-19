# Configuración de cuenta de Gmail

Asiste con la configuración de la integración de cuentas personales de Gmail.

## Por qué se necesita un OAuth Client ID

Gmail personal (@gmail.com) requiere que **el usuario inicie sesión y otorgue permiso a través del navegador** por razones de seguridad. El OAuth Client ID sirve como identificación de "qué aplicación está solicitando acceso."

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
2. Habilite la Gmail API
3. Configure la pantalla de consentimiento OAuth (externa, solo campos obligatorios)
4. Credenciales -> Crear OAuth Client ID (**Aplicación de escritorio**)
5. Copie el Client ID y el Secret

---

## Ejecutar configuración

> **Importante**: Dado que se requiere autenticación por navegador, **ejecute esto directamente en la terminal.**
> La ejecución por pipe desde el chat de Cursor expirará por tiempo de espera.

```bash
python scripts/setup_gmail_account.py --label <nombre_cuenta>
```

### Ejemplos

```bash
python scripts/setup_gmail_account.py --label my-account
python scripts/setup_gmail_account.py --label work
python scripts/setup_gmail_account.py --label work
```

### Entrada durante la ejecución

1. Client ID (copiar de Google Cloud Console)
2. Client Secret (igual)
3. Iniciar sesión en Google vía navegador -> Otorgar permiso

---

## Configuración posterior a la instalación

### 1. Verificar Secrets

```bash
gh secret list --repo <owner/repo> | grep GMAIL
```

### 2. Actualizar GMAIL_ACCOUNTS_CONFIG

**Esto debe actualizarse cada vez que agregue una cuenta:**

```bash
# Ejemplo: 2 cuentas - my-account y work
gh secret set GMAIL_ACCOUNTS_CONFIG \
  --body '{"accounts":[{"label":"my-account","type":"oauth"},{"label":"work","type":"oauth"}]}' \
  --repo <owner/repo>
```

### 3. Agregar variables de entorno al workflow

Agregue variables de entorno para la nueva cuenta en `.github/workflows/fetch_data.yml`:

```yaml
env:
  GMAIL_<LABEL>_CLIENT_ID: ${{ secrets.GMAIL_<LABEL>_CLIENT_ID }}
  GMAIL_<LABEL>_CLIENT_SECRET: ${{ secrets.GMAIL_<LABEL>_CLIENT_SECRET }}
  GMAIL_<LABEL>_REFRESH_TOKEN: ${{ secrets.GMAIL_<LABEL>_REFRESH_TOKEN }}
```

### 4. Confirmar y enviar cambios

```bash
git add .github/workflows/fetch_data.yml
git commit -m "feat: Add Gmail account <label>"
git push
```

---

## Verificación

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

Verifique los registros:
```
Starting Multi-Gmail fetch...
Processing account: my-account
[my-account] OAuth authentication successful
Processing account: work
[work] OAuth authentication successful
```

---

## Solución de problemas

### Aparece el mensaje "Esta aplicación no está verificada"

Esto es normal. Haga clic en "Avanzado" -> "Ir a [nombre de la aplicación]" para continuar.

### Ocurre un error de autenticación

Verifique lo siguiente:
1. ¿Está habilitada la Gmail API?
2. ¿Está configurada la pantalla de consentimiento OAuth?
3. ¿Son correctos el Client ID/Secret?

### Falla el registro en GitHub Secrets

```bash
gh auth status
```
Verifique el estado de autenticación. Si no está autenticado, ejecute `gh auth login`.

### Error "multiple remotes detected"

```bash
python scripts/setup_gmail_account.py --label my-account --repo owner/repo
```
Especifique el repositorio explícitamente.

### Error de conflicto en git push

Esto ocurre cuando múltiples workflows se ejecutan simultáneamente. Ejecutar nuevamente lo resolverá.

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```
