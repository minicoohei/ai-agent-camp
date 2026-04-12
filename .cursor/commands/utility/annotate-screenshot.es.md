# Annotate Screenshot con Nano Banana Pro

Este comando utiliza `tools/annotate_screenshot.py` para agregar anotaciones de tipo manual (recuadros rojos, flechas, globos de texto, texto) a capturas de pantalla.

## Principio clave

**La captura de pantalla original nunca se modifica.**

- No se altera ningún píxel de la imagen de entrada
- Las anotaciones se agregan como superposiciones sobre la imagen original
- La salida siempre se guarda como un archivo separado
- Diseñado para uso en manuales/documentación, preservando exactamente el contenido real de la pantalla

## Pasos

1. **Extraer parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Ruta de la imagen de entrada**: La captura de pantalla a anotar (obligatorio)
   - **Instrucciones de anotación**: Qué agregar y dónde (obligatorio) ej.: "Rodear el botón Guardar con un recuadro rojo"
   - **Etiqueta de texto**: Texto para mostrar en flechas o globos (opcional)
   - **Estilo**: `red_box` (predeterminado), `arrow`, `callout`, `highlight`, `circle`, `number`
   - **Ruta de salida**: Si se omite, se usa `{nombre_archivo_original}_annotated.png`

2. **Ejecutar la herramienta**:
   Ejecute el comando en el siguiente formato.
   ```bash
   uv run python tools/annotate_screenshot.py "{ruta_imagen_entrada}" "{instrucciones_anotacion}" --style "{estilo}" --text "{etiqueta_texto}" --output "{ruta_salida}"
   ```

3. **Verificar resultados**:
   - Verifique la ruta de la imagen anotada generada e informe al usuario.
   - **Indique claramente que la imagen original no ha sido modificada.**
   - Si ocurre un error, muestre el mensaje de error.

## Referencia de estilos

| Estilo | Descripción |
|--------|-------------|
| `red_box` | Rodea el elemento con un rectángulo rojo y agrega una flecha (predeterminado) |
| `arrow` | Señala el elemento con una flecha roja |
| `callout` | Agrega un globo de texto (globo de comentario) |
| `highlight` | Agrega un resaltado semitransparente estilo marcador |
| `circle` | Rodea el elemento con un círculo rojo |
| `number` | Agrega marcadores numerados (para mostrar el orden de los pasos) |

## Ejemplos de uso

### Uso básico (recuadro rojo + flecha)
```
/annotate-screenshot docs/manual_screenshots/login.png Rodear el botón "Iniciar sesión" con un recuadro rojo y agregar una flecha
```

### Con etiqueta de texto
```
/annotate-screenshot settings.png El icono de "Configuración" en la esquina superior derecha --text "Haga clic aquí"
```

### Estilo globo de texto
```
/annotate-screenshot dashboard.png La barra de menú --style callout --text "Opere desde esta área"
```

### Resaltado estilo marcador
```
/annotate-screenshot form.png El campo de entrada --style highlight
```

### Especificar ruta de salida
```
/annotate-screenshot original.png El botón "Enviar" --output docs/manual_screenshots/step3_annotated.png
```

### Agregar múltiples anotaciones en secuencia (marcadores numerados)
```
/annotate-screenshot workflow.png El primer campo de entrada --style number --text "1"
/annotate-screenshot workflow_annotated.png El siguiente menú desplegable --style number --text "2" --output workflow_step2.png
```

## Notas

- Requiere que `GEMINI_API_KEY` o `GOOGLE_API_KEY` estén configuradas en las variables de entorno (o `.env`).
- Si la ruta del archivo de salida es la misma que la del archivo de entrada, se producirá un error por seguridad.
- Esta herramienta utiliza Nano Banana Pro (Gemini 3 Pro Image Preview). El prompt instruye firmemente preservar la imagen original, pero debido a la naturaleza de la generación por IA, pueden ocurrir diferencias menores. Si se requiere precisión pixel-perfect estricta, considere usar la versión anterior `src/gemini_annotate.py` (versión con dibujo Pillow).
