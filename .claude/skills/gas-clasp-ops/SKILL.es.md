---
name: gas-clasp-ops
description: "Habilidad para operar proyectos de Google Apps Script (GAS) a través de clasp. Se activa con solicitudes como 'despliega GAS,' 'clasp push,' 'prueba función GAS,' etc. Realiza push / deploy / run individual o por lotes. Soporta gestión de múltiples proyectos."
triggers:
  - gas-clasp-ops
  - GASデプロイ
  - clasp push
  - Apps Script
  - GASテスト
  - スクリプト反映
  - clasp
---

# Habilidad de Operaciones GAS clasp

Una habilidad para operaciones por lotes en proyectos de Google Apps Script a través del CLI de clasp.

## Prerrequisitos

```bash
# clasp se ejecuta via npx (no requiere instalación)
# Iniciar sesión con su cuenta de Google (solo la primera vez)
npx -y @google/clasp login
```

## Inicio Rápido

```bash
# Push de todos los proyectos
python skills/gas-clasp-ops/scripts/clasp_ops.py push

# Push y deploy de un proyecto específico
python skills/gas-clasp-ops/scripts/clasp_ops.py push deploy --project work/10.X-Calendar-GAS

# Ejecutar una función (prueba)
python skills/gas-clasp-ops/scripts/clasp_ops.py run --project work/10.X-Calendar-GAS --function myFunction

# Dry-run para verificar
python skills/gas-clasp-ops/scripts/clasp_ops.py push --dry-run
```

## Comandos

| Comando | Descripción |
|---------|-------------|
| `push` | Enviar código local a GAS |
| `deploy` | Desplegar una nueva versión |
| `run` | Ejecutar una función especificada (`--function` requerido) |
| `status` | Mostrar lista de despliegues |
| `open` | Abrir el editor de GAS en el navegador |

## Opciones

| Opción | Descripción | Predeterminado |
|--------|-------------|----------------|
| `--project PATH` | Proyecto objetivo (múltiples permitidos) | Todos los proyectos |
| `--function NAME` | Nombre de la función a ejecutar (requerido para run) | - |
| `--dry-run` | Solo verificar sin ejecutar | false |
| `--base-dir PATH` | Directorio base de búsqueda | Raíz del workspace |

## Objetivos de Detección

Detecta automáticamente directorios que contienen `.clasp.json`:

- `work/10.X-Calendar-GAS/`
- `work/03.AiTutor/session_workshop/03.gas/samples/clasp-slides-generator/`
- `work/03.AiTutor/session_workshop/03.gas/samples/clasp-weather-recorder/`

## Ejemplos

### Verificar lista de proyectos

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py --list
```

Ejemplo de salida:
```
Proyectos detectados (3):
  - work/03.AiTutor/.../clasp-slides-generator (scriptId: 1uIfFp1vuV...)
  - work/03.AiTutor/.../clasp-weather-recorder (scriptId: 1O6SBnHgY-...)
  - work/10.X-Calendar-GAS (scriptId: 1qLnnrFfzX...)
```

### Push y deploy de todos los proyectos

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py push deploy
```

### Ejecutar una función en un proyecto específico (prueba)

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py run \
  --project work/10.X-Calendar-GAS \
  --function processUnreadTweets
```

## Solución de Problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `Not logged in` | clasp no ha iniciado sesión | Ejecute `npx -y @google/clasp login` |
| `Script API disabled` | API de GAS deshabilitada | Habilite en [API de GAS](https://script.google.com/home/usersettings) |
| `Permission denied` | Alcance de OAuth insuficiente | Añada los alcances necesarios a `appsscript.json` |
| `Function not found` | Nombre de función inválido | Verifique el nombre de la función en el editor de GAS |

## Notas

- `clasp run` requiere que la API de GAS esté habilitada y configuración de alcance OAuth
- Siempre haga `push` del código antes de desplegar
- En caso de error, los registros se generan por objetivo y el procesamiento continúa
- El tiempo de espera está configurado en 120 segundos (para procesos largos, se recomienda ejecutar desde el editor de GAS)

## Descripción General

Una habilidad para operaciones por lotes en proyectos de Google Apps Script (GAS) a través del CLI de clasp. Detecta automáticamente proyectos que contienen `.clasp.json` y ejecuta operaciones de push, deploy y run de manera eficiente.

## Criterios de Éxito

- [ ] push/deploy a los proyectos objetivo completado sin errores
- [ ] Cuando se especifica `--function`, la función se ejecutó exitosamente
- [ ] Para operaciones por lotes multi-proyecto, los resultados se registran para todos los proyectos

## Uso

Consulte la sección "Inicio Rápido" anterior. Ejemplos básicos:

```bash
# Push de todos los proyectos
python skills/gas-clasp-ops/scripts/clasp_ops.py push

# Ejecutar una función en un proyecto específico
python skills/gas-clasp-ops/scripts/clasp_ops.py run --project work/10.X-Calendar-GAS --function myFunction
```
