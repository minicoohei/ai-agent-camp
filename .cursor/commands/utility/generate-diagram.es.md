---
nonInteractiveMode: compliant
---

# Generate Diagram con Nano Banana Pro

Este comando utiliza `.cursor/tools/generate_diagram.py` para generar diagramas e infografías basados en un tema especificado.
También puede pegar texto largo o párrafos completos para visualizarlos.

## Pasos

1.  **Extraer parámetros**:
    Extraiga la siguiente información de la entrada del usuario.
    - **Tema/Contenido**: El contenido o texto a visualizar (obligatorio)
    - **Estilo**: `colorful_infographic` (predeterminado), `sketch`, `photorealistic`, `minimalist`, `claymation`, `pixel_art`
    - **Relación de aspecto**: `16:9` (predeterminado), `1:1`, `4:3`, `3:4`, `9:16`, `21:9`

2.  **Ejecutar la herramienta**:
    Ejecute el comando en el siguiente formato. Para texto largo, encierre todo el texto entre comillas o páselo tal cual (la herramienta lo concatenará).
    ```bash
    python .cursor/tools/generate_diagram.py "{tema/contenido}" --style "{estilo}" --aspect_ratio "{relación_de_aspecto}"
    ```

3.  **Verificar resultados**:
    - Verifique la ruta de la imagen generada e informe al usuario.
    - Si ocurre un error, muestre el mensaje de error.

## Ejemplos de uso

- Uso básico:
  `/generate-diagram Cómo funciona la fotosíntesis`

- Visualizar texto largo:
  `/generate-diagram "Gemini 3 Pro es un nuevo modelo de IA con capacidades de razonamiento. Genera respuestas a través de un proceso de pensamiento, lo que le permite manejar tareas complejas. También ofrece Nano Banana Pro, un modelo de generación de imágenes..." --style minimalist`

- Generar desde un archivo (cuando un Agente lee el archivo y lo pasa como argumento):
  El Agente lee el contenido del archivo y lo pasa como argumento, o ejecuta directamente `python .cursor/tools/generate_diagram.py --file path/to/file.txt`.
