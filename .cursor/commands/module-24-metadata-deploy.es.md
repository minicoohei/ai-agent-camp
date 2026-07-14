---
description: Cuando el usuario dice /module-24-metadata-deploy - Module 24 - deploy de metadatos a Sandbox
nonInteractiveMode: incompatible
---
## Empieza Aqui (ruta mas corta)

Cuando ejecutes **`/module-24-metadata-deploy`** en el chat, se cargan las instrucciones para deploy.

# Module 24 - Metadata deploy

El usuario esta trabajando en la parte de **deploy** del material "metadata deploy/retrieve."

## Pasos

1. Validar con `sf project deploy start -o dev --dry-run`
2. Si no hay problemas, ejecutar `sf project deploy start -o dev`
3. Clase individual: `--metadata ApexClass:MyController`

## Notas

- Durante el aprendizaje, usar solo Sandbox (`-o dev`)
- Hacer deploy a produccion solo cuando el usuario especifique explicitamente `-o prod`

## Referencias

- Curso: `slideId=project-deploy`
