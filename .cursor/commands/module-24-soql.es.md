---
description: Cuando el usuario dice /module-24-soql - Module 24 SOQL - obtener Account / Opportunity con sf data query
nonInteractiveMode: incompatible
---
## Empieza Aqui (ruta mas corta)

Cuando ejecutes **`/module-24-soql`** en el chat, las instrucciones del ejercicio SOQL se cargan en el contexto.

# Module 24 - Obtener datos con SOQL

El usuario esta trabajando en el material "Obtener datos con SOQL." **El agente debe ejecutar comandos sf en la terminal** y resumir los resultados.

## Requisitos previos

- Login ya hecho en Sandbox (`-o dev` o `target-org=dev`) con `sf org login web`
- No consultar un Org de produccion a menos que `-o prod` sea explicito

## Pasos

1. Revisar los Orgs conectados con `sf org list`
2. `sf data query -o dev -q "SELECT Id, Name, Industry FROM Account LIMIT 5"`
3. Opportunities abiertas: `IsClosed = false`, `ORDER BY Amount DESC LIMIT 20`
4. Total de opportunities cerradas el mes pasado: `--json` + `SUM(Amount)` (usar jq si hace falta)
5. Si ocurre `MALFORMED_QUERY`, cambiar a `-f query.soql`

## Referencias

- Curso: `slideId=soql` (ejemplo: `/es/course/module-24?slideId=soql`)
