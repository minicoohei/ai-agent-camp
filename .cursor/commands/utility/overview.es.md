---
nonInteractiveMode: compliant
---

# Overview - Visualización de la estructura del proyecto

Este comando utiliza `tools/project_overview.py` para aprovechar serena MCP en la visualización de la estructura del proyecto y la extracción de funcionalidades faltantes o partes no implementadas.

## Funcionalidades

- Explorar simbólicamente el código fuente con serena MCP
- Visualizar la estructura del proyecto en formato PlantUML (mostrado como imágenes SVG)
- **Mostrar lista de archivos y lista de funciones/clases**
- Extraer funcionalidades faltantes y partes no implementadas
- Generar informes en formato HTML
- **Solicitar aclaración cuando la información es insuficiente**

## Filosofía de diseño

- **Uso de serena MCP**: Análisis preciso de la estructura mediante exploración simbólica
- **Enfoque en la visualización**: Mostrar diagramas de estructura como imágenes SVG a través del servidor oficial de PlantUML
- **Lista de archivos/funciones**: Mostrar descripciones y funciones principales de cada archivo
- **Identificación de funcionalidades faltantes**: Distinguir claramente entre funcionalidades implementadas y faltantes

## Pasos de ejecución

1. **Extracción de parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Directorio de destino**: El directorio a analizar (opcional, por defecto: raíz del proyecto)
   - **Formato de salida**: plantuml / wbs / all (opcional, por defecto: all)
   - **Ruta de salida**: Por defecto `docs/bootcamp/overview/overview_{timestamp}.html` si se omite

2. **Manejo de información insuficiente**:
   Si falta información necesaria, pregunte al usuario de la siguiente manera:
   ```
   Para generar el resumen del proyecto, proporcione lo siguiente:
   
   1. ¿Qué directorio desea analizar? (ej.: src/, scripts/)
   2. ¿Tiene alguna preferencia de formato de salida? (plantuml / wbs / all)
   ```

3. **Ejecución de la herramienta**:
   Ejecute el comando en el siguiente formato.
   ```bash
   uv run python tools/project_overview.py --directory "{directorio_destino}" --format "{formato_salida}" --output "{ruta_salida}"
   ```

4. **Verificación de resultados**:
   - Confirme la ruta del archivo HTML generado e infórmelo al usuario.
   - Proporcione instrucciones sobre cómo abrirlo con Live Server.
   - Muestre los mensajes de error si ocurre algún problema.

## Ejemplos de uso

### Uso básico (analizar todo el proyecto)
```
/overview
```

### Analizar un directorio específico
```
/overview --directory src/
```

### Especificar formato de salida (solo mapa mental WBS)
```
/overview --format wbs
```

### Combinar múltiples opciones
```
/overview --directory scripts/ --format plantuml --output docs/bootcamp/overview/scripts_overview.html
```

## Flujo de procesamiento

1. **Explorar código fuente con serena MCP**: Analizar simbólicamente la estructura del proyecto
2. **Analizar con Gemini API**: Extraer lista de archivos, lista de funciones y descripciones
3. **Visualizar estructura**: Generar diagramas de componentes y mapas mentales con PlantUML
4. **Generar informe HTML**: Producir un informe en formato fácil de entender

## Contenido de la salida

- **Lista de archivos y funciones**: Ruta, descripción y funciones/clases principales de cada archivo
- **Diagrama de estructura del proyecto**: Diagrama de componentes en formato PlantUML (imagen SVG)
- **Mapa mental (WBS)**: Diagrama jerárquico en formato PlantUML (imagen SVG)
- **Lista de módulos**: Roles y relaciones de cada módulo
- **Funcionalidades implementadas**: Lista de funcionalidades actualmente implementadas
- **Funcionalidades faltantes**: Lista de funcionalidades no implementadas o faltantes
- **Recomendaciones**: Recomendaciones para mejorar el proyecto

## Acerca de serena MCP

serena MCP es un MCP (Model Context Protocol) que permite la exploración simbólica de código fuente.

- Comprender claramente la estructura del proyecto
- Entender qué hace cada archivo
- Confirmar qué funcionalidades se han completado

## Notas

- Ejecute en un entorno donde serena MCP esté disponible
- El análisis puede tardar en proyectos grandes
- Se requiere conexión al servidor oficial de PlantUML (plantuml.com)
