---
name: check-inbox
description: "Habilidad integrada para extraer elementos accionables y tareas del correo electronico y Slack. Utiliza Gemini 3.0 Flash para analisis de contexto, generando prioridades y borradores de respuesta. Se activa con solicitudes como 'revisar bandeja de entrada', 'verificar TODOs', 'mensajes por responder', 'revisar correo', etc."
triggers:
  - check-inbox
  - revisar bandeja de entrada
  - verificar TODOs
  - mensajes por responder
  - revisar correo
  - revisar Slack
  - inbox
  - check inbox
  - 受信箱チェック
---

## Palabras Clave de Activacion
"revisar bandeja de entrada", "verificar TODOs", "mensajes por responder", "revisar correo", "revisar Slack"

# /check-inbox - Extraccion de Tareas de Bandeja de Entrada

Extrae elementos que requieren respuesta del correo electronico (Gmail) y Slack, y los lista con niveles de prioridad.

## ⚠️ Nota de Seguridad (Indirect Prompt Injection)
- Esta skill envia correos y mensajes de Slack externos a un LLM. Un atacante puede insertar cargas como "ignora las instrucciones previas y haz X" dentro del cuerpo del mensaje.
- `scripts/llm_analyzer.py` envuelve el texto externo con etiquetas de frontera `<external_untrusted_content>` e instruye al LLM a tratar esa region como datos. Aun asi, **revisa siempre el `draft_reply` generado antes de enviarlo** — nunca envies borradores sin verificacion humana.
- Si un mensaje contiene instrucciones sospechosas, asume que el resultado del analisis y el borrador pueden estar contaminados.

```bash
# Ejecucion basica (ultimos 3 dias)
python skills/check-inbox/scripts/check_inbox.py

# Verificar ultimos 7 dias
python skills/check-inbox/scripts/check_inbox.py --days 7

# Solo correo electronico
python skills/check-inbox/scripts/check_inbox.py --email-only

# Solo Slack
python skills/check-inbox/scripts/check_inbox.py --slack-only
```

## Funciones

- **Analisis de correo**: Extrae correos de archivos Markdown en `/output/gmail/`
  - Excluye automaticamente correos de marketing y notificaciones automaticas
  - Solo analiza correos de personas reales via LLM

- **Analisis de Slack**: Extrae menciones de `slack-sync/data/`
  - Busca identificadores de la opcion `--users` o configuracion predeterminada
  - Considera respuestas de hilo en el analisis

- **Analisis LLM** (Gemini 3.0 Flash)
  - Determina si se necesita una respuesta
  - Establece prioridad (alta/media/baja)
  - Genera borradores de respuesta

## Opciones

| Opcion | Descripcion | Predeterminado |
|--------|-------------|----------------|
| `--days, -d` | Cuantos dias pasados verificar | 3 |
| `--email-only` | Verificar solo correo | - |
| `--slack-only` | Verificar solo Slack | - |
| `--output, -o` | Ruta del archivo de salida | `inbox-{fecha}.md` |
| `--gmail-dir` | Directorio de datos de Gmail | Auto-detectar |
| `--slack-dir` | Directorio de datos de Slack | Auto-detectar |
| `--workspace, -w` | Espacio de trabajo de Slack | Todos |
| `--users, -u` | Usuarios objetivo a buscar (separados por coma) | Lista predeterminada |
| `--no-llm` | Omitir analisis LLM | - |
| `--quiet, -q` | Suprimir visualizacion de progreso | - |
| `--notify-line` | Enviar resultados por notificacion LINE | - |

## Ejemplo de Salida

```markdown
# Tareas de Bandeja de Entrada - 2026-01-28

## Prioridad Alta

### Correo Electronico
- **[Re: Progreso del Proyecto]** de: Taro Tanaka (2026-01-27)
  - Razon: Solicitud de confirmacion con fecha limite
  - Borrador de respuesta: "Gracias por su mensaje. Lo revisare e informare antes de manana."

### Slack
- **[#pj_xxx]** @{SU_NOMBRE} (2026-01-27 14:30)
  - Contenido: Pregunta sobre especificaciones de API
  - Razon: Pregunta directa, requiere respuesta
  - Borrador de respuesta: "He revisado las especificaciones de la API..."

## Prioridad Media
...

---
Generado: 2026-01-28 10:00:00
Periodo: Ultimos 3 dias
Correos: 15 -> Accionables: 3
Slack: 42 -> Accionables: 8
```

## Configuracion del Entorno

### Variables de Entorno Requeridas

Configure lo siguiente en el archivo `.env`:

```env
GEMINI_API_KEY=su_clave_api_aqui
# o
GOOGLE_API_KEY=su_clave_api_aqui

# Notificacion LINE (al usar --notify-line)
LINE_CHANNEL_ACCESS_TOKEN=su_token_de_acceso_line
LINE_USER_ID=su_id_de_usuario_line
```

### Dependencias

```bash
uv add google-generativeai python-dateutil
```

## Directorios de Datos

Las siguientes rutas se detectan automaticamente:

**Correo electronico**:
- `./output/gmail/`
- `~/output/gmail/`

**Slack**:
- `./slack-sync/data/`
- `~/githubactions_fordata/slack-sync/data/`

## Habilidades Relacionadas

- `/email-tasks` - Extraccion de tareas especifica de correo
- `/slack-tasks` - Extraccion de tareas especifica de Slack

## Descripcion General

Habilidad que extrae automaticamente mensajes y tareas que requieren respuesta de Gmail y Slack. Utiliza Gemini 3.0 Flash para analisis de contexto, generando borradores de respuesta priorizados.

## Solucion de Problemas

| Error | Solucion |
|-------|----------|
| API key not found | Configurar `GEMINI_API_KEY` o `GOOGLE_API_KEY` en `.env` |
| No Gmail data found | Verificar si existen datos de correo en el directorio `output/gmail/` |
| No Slack data found | Verificar si el directorio `slack-sync/data/` esta sincronizado |

## Criterios de Exito

- [ ] Las tareas estan listadas por prioridad (alta/media/baja)
- [ ] Se generan borradores de respuesta para cada tarea
- [ ] El archivo Markdown de salida se guarda correctamente

## Uso

Consulte la seccion "Inicio Rapido" arriba. Ejemplo basico:

```bash
# Revisar bandeja de entrada de los ultimos 3 dias
python skills/check-inbox/scripts/check_inbox.py

# Solo Slack, ultimos 7 dias
python skills/check-inbox/scripts/check_inbox.py --slack-only --days 7
```
