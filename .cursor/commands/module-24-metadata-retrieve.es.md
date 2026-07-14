---
description: Cuando el usuario dice /module-24-metadata-retrieve - Module 24 - retrieve de Apex / Flow / Layout
nonInteractiveMode: incompatible
---
## Empieza Aqui (ruta mas corta)

Cuando ejecutes **`/module-24-metadata-retrieve`** en el chat, se cargan las instrucciones para metadata retrieve.

# Module 24 - Metadata retrieve

El usuario esta trabajando en la parte de **retrieve** del material "metadata deploy/retrieve."

## Pasos

1. Si todavia no existe, ejecutar `sf project generate --name my-sf-project`
2. Ejecutar `cd my-sf-project`
3. Ejecutar `sf project retrieve start -o dev --metadata ApexClass --metadata Flow --metadata Layout`
4. Resumir los archivos agregados bajo `force-app/main/default/`
5. Reportar las rutas principales con `git status`

## Notas

- Si los cambios de la UI de Sandbox no coinciden, revisar primero con `sf org open -o dev`
- Hacer retrieve desde produccion solo cuando `-o prod` sea explicito

## Referencias

- Curso: `slideId=project-deploy` (ejemplo: `/es/course/module-24?slideId=project-deploy`)
