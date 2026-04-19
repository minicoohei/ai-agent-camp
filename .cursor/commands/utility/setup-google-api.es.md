# Setup Google API for MCP - Guía de configuración de Google API

Este comando utiliza Cursor Browser para proporcionar una guía paso a paso para la configuración de Google API y la autenticación OAuth 2.0 para MCP (Model Context Protocol).

## APIs de destino

- Gmail API
- Google Calendar API
- Google Drive API
- Google Sheets API

## Funcionalidades

- **Uso de Cursor Browser**: Semiautomatizar la configuración mediante operaciones del navegador
- **Guía paso a paso**: Avanzar verificando el estado en cada paso
- **Acciones del usuario claras**: Indicar explícitamente las operaciones manuales requeridas por seguridad
- **Flujo de autenticación OAuth**: Desde la obtención de credenciales hasta la finalización de la autenticación

## Pasos de ejecución

### Fase 1: Confirmar parámetros

Confirme la siguiente información de la entrada del usuario:

1. **APIs de destino** (selección múltiple permitida):
   - `gmail` - Gmail API
   - `calendar` - Google Calendar API
   - `drive` - Google Drive API
   - `sheets` - Google Sheets API

2. **Nombre del proyecto** (opcional, por defecto: `mcp-google-api`)

3. **Directorio de salida** (opcional, por defecto: raíz del proyecto)

### Fase 2: Configuración de Google Cloud Console (Cursor Browser)

Ejecute los siguientes pasos utilizando Cursor Browser.

#### Paso 1: Acceder a Google Cloud Console

```
browser_navigate: https://console.cloud.google.com/
```

Después de la ejecución, verifique el estado de la página con `browser_snapshot` y compruebe el estado de inicio de sesión.

**Guíe al usuario:**
- Si no ha iniciado sesión: "Inicie sesión en su cuenta de Google"
- Si ya ha iniciado sesión: Continuar al siguiente paso

#### Paso 2: Crear proyecto (si es necesario)

Se puede omitir si utiliza un proyecto existente.

```
browser_navigate: https://console.cloud.google.com/projectcreate
```

**Guíe al usuario:**
```
[Creación del proyecto]
1. Ingrese un nombre de proyecto (recomendado: mcp-google-api)
2. Seleccione su organización (seleccione "Sin organización" para cuentas personales)
3. Haga clic en "Crear"

Escriba "listo" cuando esté preparado.
```

#### Paso 3: Habilitar APIs

Habilite las APIs seleccionadas en orden. Patrón de URL:

```
Gmail API:     https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={PROJECT_ID}
Calendar API:  https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project={PROJECT_ID}
Drive API:     https://console.cloud.google.com/apis/library/drive.googleapis.com?project={PROJECT_ID}
Sheets API:    https://console.cloud.google.com/apis/library/sheets.googleapis.com?project={PROJECT_ID}
```

Para cada página de API:
1. Navegue a la página de la API con `browser_navigate`
2. Verifique el estado de la página con `browser_snapshot`
3. Si encuentra el botón "Habilitar", guíe al usuario para que haga clic en él

**Guíe al usuario:**
```
[Habilitación de API: {nombre de la API}]
Haga clic en el botón azul "Habilitar".
Escriba "listo" cuando la habilitación esté completa.
```

#### Paso 4: Configuración de la pantalla de consentimiento OAuth

```
browser_navigate: https://console.cloud.google.com/auth/overview?project={PROJECT_ID}
```

**Guíe al usuario:**
```
[Configuración de la pantalla de consentimiento OAuth]
1. Seleccione "Externo" como tipo de usuario y haga clic en "Crear"
2. Ingrese la siguiente información:
   - Nombre de la aplicación: Cualquier nombre (ej.: MCP Google API)
   - Correo electrónico de soporte al usuario: Su dirección de correo electrónico
   - Información de contacto del desarrollador: Su dirección de correo electrónico
3. Haga clic en "Guardar y continuar"
4. En la pantalla de Ámbitos, haga clic en "Guardar y continuar" tal como está
5. En la pantalla de Usuarios de prueba, agregue su dirección de correo electrónico
6. Haga clic en "Guardar y continuar" -> "Volver al panel"

Escriba "listo" cuando haya terminado.
```

#### Paso 5: Crear ID de cliente OAuth

```
browser_navigate: https://console.cloud.google.com/auth/clients?project={PROJECT_ID}
```

**Guíe al usuario:**
```
[Creación del ID de cliente OAuth]
1. Haga clic en "+ Crear cliente" o "Crear credenciales"
2. Tipo de aplicación: Seleccione "Aplicación de escritorio"
3. Nombre: Cualquier nombre (ej.: MCP Desktop Client)
4. Haga clic en "Crear"
5. En el diálogo que aparece, haga clic en "Descargar JSON"
6. Guarde el archivo descargado en un lugar seguro

Proporcione la ruta del archivo JSON
(Ejemplo macOS: ~/Downloads/client_secret_xxx.json)
(Ejemplo Windows WSL2: /mnt/c/Users/<NombreUsuarioWindows>/Downloads/client_secret_xxx.json)
```

### Fase 3: Ejecutar el flujo de autenticación OAuth

Utilice el JSON de credenciales descargado para ejecutar el flujo de autenticación.

```bash
uv run python tools/google_api_setup.py auth \
  --credentials "{ruta_json_credenciales}" \
  --scopes "{ámbitos_seleccionados}" \
  --output "{directorio_salida}"
```

**Correspondencia de ámbitos:**
- gmail: `https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.modify`
- calendar: `https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.events`
- drive: `https://www.googleapis.com/auth/drive`
- sheets: `https://www.googleapis.com/auth/spreadsheets`

### Fase 4: Confirmación de finalización

Al completar la autenticación exitosamente, se generan los siguientes archivos:
- `token.json` - Token de autenticación
- `mcp_config.json` - Archivo de configuración MCP (referencia)

**Informe al usuario:**
```
[Configuración completa]
La configuración de Google API se ha completado.

Archivos generados:
- token.json: Token de autenticación (importante: manténgalo seguro)
- mcp_config.json: Ejemplo de configuración MCP

Siguientes pasos:
1. Editar el archivo de configuración del servidor MCP
2. Establecer la ruta del token generado en la configuración
3. Iniciar el servidor MCP y probar

Consulte la documentación de cada servidor MCP para obtener instrucciones detalladas de configuración.
```

## Ejemplos de uso

### Uso básico (todas las APIs)
```
/setup-google-api gmail calendar drive sheets
```

### Solo APIs específicas
```
/setup-google-api gmail sheets
```

### Especificar nombre del proyecto
```
/setup-google-api gmail --project my-mcp-project
```

## Notas

### Precauciones de seguridad
- **Nunca exponga el JSON de credenciales ni el token.json**
- Con estos archivos, cualquier persona puede acceder a su cuenta de Google
- Agréguelos a `.gitignore` para evitar incluirlos en el repositorio

### Acciones que requieren intervención del usuario
Las siguientes acciones deben ser realizadas por el usuario por razones de seguridad:
1. Iniciar sesión en una cuenta de Google
2. Otorgar permisos en la pantalla de consentimiento OAuth
3. Descargar el JSON de credenciales
4. Aprobar en el navegador durante el flujo de autenticación

### Solución de problemas

#### Error: "Access blocked: This app's request is invalid"
- Es posible que la configuración de la pantalla de consentimiento OAuth no esté completa
- Verifique que su dirección de correo electrónico se haya agregado como usuario de prueba

#### Error: "invalid_grant"
- El token.json puede haberse invalidado
- Elimine token.json y ejecute el flujo de autenticación nuevamente

#### Error: "API not enabled"
- Es posible que la API requerida no esté habilitada
- Verifique que la API esté habilitada en Google Cloud Console
