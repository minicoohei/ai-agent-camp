# Gmail Pending Replies - Extraer correos sin responder

Extraiga correos electrónicos que necesitan respuesta de Gmail y **genere borradores de respuesta automáticamente**.

## Categorías objetivo

1. **Correos sin responder**: Correos dirigidos a usted (TO/CC) a los que no ha respondido
2. **Respuestas en hilos**: Hilos que usted inició donde la última respuesta es de otra persona

## Fuentes de datos

### Método 1: Usar datos sincronizados (recomendado)

Analice archivos Markdown sincronizados en `output/gmail/{nombre_cuenta}/`.

| Cuenta | Ruta | Su dirección |
|--------|------|-------------|
| default | `output/gmail/default/` | `user@example.com` |
| work | `output/gmail/work/` | Dirección correspondiente |

### Método 2: Vía API (cuando GMAIL_ACCOUNTS_CONFIG está configurado)

```bash
python src/get_gmail_pending_replies.py --days {días}
```

## Pasos

### Paso 1: Extraer parámetros

Extraiga lo siguiente de la entrada del usuario:
- **Días**: Número de días objetivo (predeterminado: 7)
- **Cuenta**: Solo una cuenta específica (predeterminado: all)
- **Formato de salida**: markdown / json (predeterminado: pantalla)

### Paso 2: Escanear correos

Analice los datos sincronizados en `output/gmail/{cuenta}/YYYY-MM-DD/*.md` y extraiga:
- Correos recibidos de personas que no sean usted
- Excluir correos de notificación (noreply, bank, peatix, etc.)
- Excluir invitaciones a reuniones (adjuntos .ics)
- Excluir correos con el mismo asunto donde ya haya respondido

### Paso 3: Mostrar resultados + Generar borradores de respuesta automáticamente

1. Muestre la lista de correos sin responder
2. **Analice el contenido de cada correo y determine su tipo**:
   - **Solicitud/Tarea**: Algo que requiere una acción específica
   - **Pregunta**: Algo que requiere una respuesta
   - **Información compartida**: No requiere respuesta (compartido por CC, etc.)

3. **Genere automáticamente borradores de respuesta para correos de solicitud y pregunta**:
   - Lea el cuerpo del correo
   - Haga referencia a información de proyectos relacionados si está disponible
   - Cree un borrador de respuesta apropiado

## Opciones

| Opción | Descripción | Predeterminado |
|--------|-------------|----------------|
| `--days INT` / `-d` | Número de días objetivo | 7 |
| `--account TEXT` / `-a` | Solo cuenta específica (nombre de etiqueta) | all |
| `--output PATH` / `-o` | Ruta del archivo de salida (.json / .md) | stdout |

## Ejemplos de uso

### Ejecución básica

```
/gmail-pending-replies
```

Se ejecuta con la configuración predeterminada (7 días, todas las cuentas).

### Especificar número de días

```
/gmail-pending-replies 3 días
```

Se ejecuta con `--days 3`.

### Solo cuenta específica

```
/gmail-pending-replies solo cuenta personal
```

Se ejecuta con `--account personal`.

### Guardar como Markdown

```
/gmail-pending-replies guardar en output/pending.md
```

Se ejecuta con `--output output/pending.md`.

## Requisitos previos

### Al usar datos sincronizados (recomendado)

Los correos deben estar sincronizados en `output/gmail/{nombre_cuenta}/`.

```
output/gmail/
├── my-account/
│   ├── 2026-01-27/
│   │   ├── index.md          # Índice diario
│   │   ├── 19bfd03adcbf0235.md  # Correo individual
│   │   └── ...
│   └── ...
└── work/
    └── ...
```

Formato de cada archivo de correo:
```yaml
---
id: 19bfd03adcbf0235
subject: Asunto
from: Remitente <email@example.com>
date: 2026-01-27 10:13:51
attachments: file1.pdf, file2.xlsx  # Opcional
---

# Asunto

Cuerpo del correo...
```

### Al usar API (opcional)

La variable de entorno `GMAIL_ACCOUNTS_CONFIG` debe estar configurada con la configuración de múltiples cuentas:

```json
{
  "accounts": [
    {
      "label": "work",
      "type": "service_account",
      "subject": "user@company.com"
    },
    {
      "label": "personal",
      "type": "oauth",
      "client_id_env": "GMAIL_PERSONAL_CLIENT_ID",
      "client_secret_env": "GMAIL_PERSONAL_CLIENT_SECRET",
      "refresh_token_env": "GMAIL_PERSONAL_REFRESH_TOKEN"
    }
  ]
}
```

## Formato de salida

### 1. Lista de correos sin responder

```
Correos que requieren respuesta (default): 2 elementos
Período objetivo: Últimos 7 días

======================================================================

1. Sobre el informe de progreso del proyecto - Acción requerida
   Fecha: 2026-01-27 10:13
   De: Taro Yamada <taro.yamada@example.com>
   Tipo: Solicitud/Tarea
   Resumen: Solicitud de revisión del informe
   Enlace: https://mail.google.com/mail/u/0/#inbox/xxx

2. Sobre la agenda de la reunión mensual
   Fecha: 2026-01-23 13:53
   De: Hanako Sato <hanako.sato@example.com>
   Tipo: Información compartida (CC)
   Resumen: Compartir borrador de agenda
   Enlace: https://mail.google.com/mail/u/0/#inbox/yyy

======================================================================
```

### 2. Borradores de respuesta generados automáticamente (solo para correos de solicitud/pregunta)

Se generan automáticamente borradores de respuesta para correos que contienen solicitudes o preguntas:

```
---
## Borrador de respuesta: Sobre el informe de progreso del proyecto

Asunto: Re: Sobre el informe de progreso del proyecto

Estimado Sr. Yamada,

Gracias por comunicarse.
Acuso recibo de su solicitud del informe.

Estoy planeando preparar el informe en las siguientes categorías:

[1. Recopilación de información/búsqueda]
- Búsqueda cruzada y generación de resúmenes para Slack/Gmail/Calendario

[2. Creación de documentos/materiales]
- Generación automática de diagramas de flujo de trabajo

[3. Formato/transcripción]
- Limpieza de datos y conversión de formato

Enviaré los materiales antes del final de esta semana.
---
```

## Patrones de exclusión

Los siguientes correos se excluyen automáticamente:

| Categoría | Patrones de ejemplo |
|-----------|---------------------|
| Notificaciones | noreply, no-reply, notification |
| Bancos | @bank.gmo-aozora.com |
| Eventos | @peatix.com, @morningpitch.com |
| Envío automático | spamdigest, Moderator |
| Invitaciones a reuniones | adjuntos .ics, teams.microsoft.com |

## Comandos relacionados

- `/extract-tasks` - Extracción de tareas de múltiples fuentes (incluye Gmail)
- `/slack-pending-replies` - Versión Slack de extracción de mensajes sin responder
