# Tools Index - Lista de herramientas

Una lista y descripción general de las herramientas disponibles en este proyecto.

## Herramientas por categoría

### Análisis de proyectos
- **project_overview**: Visualiza la estructura del proyecto en formato PlantUML/Mermaid/WBS y resume módulos, funcionalidades y partes faltantes.

### Análisis y procesamiento de capturas de pantalla
- **screenshot_analyzer**: Herramienta integrada de análisis de capturas de pantalla.
  - Modo `analyze`: Detección de errores, identificación de causas, sugerencias de NextStep
  - Modo `tutorial`: Análisis de pasos de operación y generación de tutoriales anotados paso a paso
- **annotate_screenshot**: Agrega anotaciones como bordes rojos, flechas y leyendas a capturas de pantalla (superpone sin modificar la imagen original).
- **video_frame_reader**: Extrae fotogramas clave de videos + realiza análisis con Gemini.

### Generación de anuncios y banners
- **banner_creator**: Genera banners/creatividades para diversas redes sociales y plataformas publicitarias.
  - Compatible con X, Facebook, Instagram, PR Times, YouTube, LINE y anuncios web
  - Control detallado sobre tono, esquema de colores, estilo de fuente y prioridad
  - Generación simultánea de texto de publicación (texto, hashtags, CTA)
  - Compatible con especificación de imágenes de referencia y obtención mediante búsqueda web

### Generación de diapositivas y diagramas
- **generate_aitutor_slide**: Genera imágenes de diapositivas de capacitación de IA BRAIN PARTNERS basadas en 17 tipos de diapositivas de referencia.
- **generate_slide**: Genera imágenes de diapositivas para conferencias a partir de temas (diseño simple con fondo blanco/azul principal/amarillo de acento).
- **generate_diagram**: Genera imágenes de infografías/diagramas a partir de temas o texto.
- **generate_plantuml_diagram**: Genera imágenes de diagramas de flujo modernos estilo Visio a partir de archivos PlantUML.
- **pptx_template**: Extrae el formato de PPTX en plantillas YAML y genera nuevas diapositivas con solo el texto reemplazado.

### Soporte de aprendizaje y guías
- **guide_action**: Analiza la situación actual del historial de SpecStory y presenta explicaciones de contexto y próximas acciones.
- **tutor_generate**: Extrae brechas de aprendizaje del historial de SpecStory y genera contenido de aprendizaje para principiantes (HTML).

### Configuración y utilidades
- **google_api_setup**: Configura la autenticación OAuth de Google API para MCP (compatible con Gmail, Calendar, Drive, Sheets).
- **gmail_account_setup**: Configura la autenticación OAuth para múltiples cuentas de Gmail y las registra automáticamente en GitHub Secrets.
- **google_account_setup**: Configura la autenticación OAuth de Calendar/Drive para múltiples cuentas de Google y las registra automáticamente en GitHub Secrets. Puede reutilizar el mismo ID de cliente que para Gmail.
- **bigquery_auth**: Configura la autenticación de BigQuery por proyecto de GCP. Gestiona de forma segura múltiples proyectos utilizando perfiles de configuración de gcloud.
- **notebooklm_cli**: Crea/obtiene/lista notebooks vistos recientemente utilizando la API de NotebookLM Enterprise.
- **bootcamp_utils**: Utilidades comunes (inicialización del cliente de Gemini API, generación de plantillas HTML, etc.). Uso interno.

## Lista de comandos

| Comando | Herramienta correspondiente | Descripción |
|---------|---------------------------|-------------|
| `/overview` | project_overview | Visualizar la estructura del proyecto |
| `/screenshot-analyzer` | screenshot_analyzer | Análisis de capturas de pantalla (error/tutorial) |
| `/annotate-screenshot` | annotate_screenshot | Agregar anotaciones a imágenes |
| `/video-frame-reader` | video_frame_reader | Extracción de fotogramas clave + análisis Gemini |
| `/create-banner` | banner_creator | Generación de banners/creatividades publicitarias |
| `/generate-aitutor-slide` | generate_aitutor_slide | Generación de diapositivas de capacitación |
| `/generate-slide` | generate_slide | Generación de diapositivas de uso general |
| `/generate-diagram` | generate_diagram | Generación de diagramas |
| `/generate-plantuml-diagram` | generate_plantuml_diagram | Generación de diagramas PlantUML |
| `/pptx-template` | pptx_template | Extracción y generación de plantillas PPTX |
| `/guide` | guide_action | Sugerencias de próximas acciones |
| `/tutor` | tutor_generate | Generación de contenido de aprendizaje |
| `/setup-google-api` | google_api_setup | Configuración de autenticación de Google API |
| `/gmail-account-setup` | gmail_account_setup | Autenticación OAuth de Gmail y registro de Secrets |
| `/google-account-setup` | google_account_setup | Autenticación OAuth de Calendar/Drive y registro de Secrets |
| `/bigquery-auth` | bigquery_auth | Autenticación de BigQuery (por proyecto) |
| `/notebooklm` | notebooklm_cli | Creación/obtención/listado de notebooks de NotebookLM |
