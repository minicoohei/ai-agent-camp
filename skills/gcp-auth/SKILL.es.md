---
name: gcp-auth
description: "Habilidad para ejecutar la autenticación de Credenciales Predeterminadas de Aplicación de Google Cloud Platform (GCP). Se activa con solicitudes como 'autenticar GCP,' 'autenticación de Google Cloud,' 'gcloud login,' etc. Guía los procedimientos de autenticación antes de usar servicios de GCP como BigQuery o Cloud Storage."
triggers:
  - gcp-auth
  - GCP認証
  - Google Cloud認証
  - gcloud login
  - サービスアカウント
  - ADC認証
---

## Palabras Clave de Activación
"Autenticación GCP," "Autenticación Google Cloud," "gcloud login," "cuenta de servicio"

# Autenticación de GCP

Una habilidad para ejecutar la autenticación de Credenciales Predeterminadas de Aplicación (ADC) de Google Cloud.

## Flujo de Trabajo

1. El usuario dice "autenticar GCP," "quiero usar BigQuery," etc.
2. Guíe al usuario para ejecutar el comando de autenticación en su terminal
3. Autenticarse con la cuenta de Google en el navegador
4. Confirmar la finalización de la autenticación

## Uso

### Comando de Autenticación (ejecutar directamente en la terminal)

```bash
gcloud auth application-default login
```

**Nota**: Este comando requiere autenticación basada en navegador, así que ejecútelo directamente en su terminal.

## Flujo de Autenticación

1. **Ejecutar comando** -> El navegador se abre automáticamente
2. **Seleccionar cuenta de Google** -> Elija la cuenta a usar
3. **Conceder permisos** -> Haga clic en "Permitir" en "Permitir acceso a Google Auth Library"
4. **Confirmar finalización** -> La terminal muestra "Credentials saved to file"

## Solución de Problemas

| Error | Solución |
|-------|----------|
| Reauthentication is needed | Autenticación expirada. Ejecute `gcloud auth application-default login` nuevamente |
| Advertencia GOOGLE_APPLICATION_CREDENTIALS | Elimine la línea correspondiente de `.env`, o use ADC |
| Project not set | Configure el proyecto con `gcloud config set project PROJECT_ID` |

## Verificar Estado de Autenticación

```bash
# Si se muestra un token, la autenticación está completa
gcloud auth application-default print-access-token

# Verificar el proyecto actual
gcloud config get-value project
```

## Requisitos

- Google Cloud SDK (`gcloud`) instalado
- Posibilidad de iniciar sesión en una cuenta de Google en el navegador
