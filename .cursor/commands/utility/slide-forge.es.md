---
nonInteractiveMode: compliant
---

# Slide Forge — Crear diapositivas a partir del esquema

Crea diapositivas HTML autocontenidas (16:9), con un formato uniforme, a partir de un esquema (outline) o de resultados de investigación. Aplica una plantilla común (encabezado / pie de página) a todas las diapositivas y estructura cada una con la regla 1 diapositiva = 1 mensaje. La salida por defecto es HTML autocontenido (sin depender de CDN externos —bibliotecas JS/CSS cargadas desde otro servidor en internet—, ni de imágenes o fuentes externas), de modo que el archivo se pueda abrir y visualizar incluso sin conexión a internet.

Esta skill no está pensada para un proyecto específico; se ha nombrado como comando de uso general. Si en el entorno ya existe otro comando llamado `slide-forge` con una definición distinta, al introducirlo verifica primero si existe: si no existe, añádelo tal cual; si existe, el contenido de este archivo prevalece y debe sobrescribirlo/integrarse con él.

## Funcionalidad

- A partir de un archivo de esquema (sigue la convención del proyecto; p. ej. `outline/proposal.md`) o de resultados de investigación (sigue la convención del proyecto; p. ej. `research/<tema>/findings.md`), genera diapositivas HTML autocontenidas sin dependencias externas
- Fija de antemano el encabezado, el pie de página, la paleta de colores y la tipografía comunes a todas las páginas, para evitar inconsistencias de formato
- No usa cifras ni hechos que carezcan de fuente
- Incrusta las imágenes en el HTML como URI de datos base64; no crea referencias externas

## Cuándo usarlo / cuándo no

**Úsalo cuando**: se quiere convertir resultados de investigación en un mazo de propuesta, convertir un esquema en HTML para proyectar, unificar el formato de notas existentes, producir en serie diapositivas multilingües, se necesita un mazo ligero para uso interno, o se quiere crear un mazo de propuesta con fotos o imágenes de gráficos.

**No lo uses (considera otra alternativa)**:
- PPTX que requiera animaciones y transiciones de pantalla elaboradas (solo si se solicita explícitamente, considerar aparte una conversión a PPTX)
- Un único diagrama o infografía suelta (→ la skill `diagram-generator` es más adecuada)
- Cuando se quiere editar directamente, tal cual, una plantilla existente de PowerPoint o Google Slides
- Dashboards interactivos o informes con filtros que manejan grandes volúmenes de datos (→ la skill `interactive-dashboard-builder` es más adecuada)
- Etapa en la que aún no se dispone de hechos ni cifras con fuente (→ si el entorno cuenta con una skill de verificación de hechos como `ycp-research-factcheck`, úsala primero para completar esa parte; si no existe, confirma las fuentes por tu cuenta antes de usar este comando)
- Mazos con muchas diapositivas (más de 50 aprox.) o de gran extensión que abarcan varias secciones (→ un solo archivo se vuelve pesado y difícil de mantener; divide por capítulos en varios archivos o reduce el número de diapositivas antes de usarlo)

## Pasos de ejecución

1. **Extracción de parámetros y confirmación del destino de guardado**
   A partir de la solicitud del usuario, extrae lo siguiente:
   - Nombre del proyecto/cliente (obligatorio; se usará en el nombre del archivo)
   - Existencia y ruta del archivo de esquema (sigue la convención del proyecto; p. ej. `outline/proposal.md`)
   - Existencia y ruta de los resultados de investigación/datos con fuente (sigue la convención del proyecto; p. ej. `research/<tema>/findings.md`)
   - Destino de salida (si el proyecto no tiene convención establecida, confírmalo aquí con el usuario; si no se indica nada, el valor por defecto es `output/slides/<nombre del proyecto o tema>.html`)

2. **Confirmación del esquema**
   Si existe un archivo de esquema, léelo. Si no existe, entrevista al usuario o, si el entorno cuenta con una skill de creación de esquemas como `ycp-proposal-outline`, úsala primero para organizar la estructura de capítulos y los mensajes clave, y luego continúa. Si se van a usar cifras o hechos, comprueba si existen resultados de investigación con fuente (si no existen, comunica que «no se pueden usar cifras sin fuente» y, si el entorno cuenta con una skill de verificación de hechos como `ycp-research-factcheck`, indícala al usuario).

3. **Definición de la plantilla común**
   Fija lo siguiente con CSS dentro de un único archivo:
   - Tamaño: 16:9 (1280×720) fijo
   - Encabezado común: etiqueta de sección + título
   - Pie de página común: nombre del proyecto, número de página
   - Paleta de colores: hasta 2 colores + gradaciones de gris. Por defecto, azul marino (#1F3A5F) como color principal, naranja (#E8833A) como color de acento, y gris (#333333/#666666) para el cuerpo del texto. Si se conoce el color de marca, tiene prioridad
   - Tipografía: solo fuentes del sistema (prohibido cargar fuentes externas). El tamaño de fuente del cuerpo debe ser de 18px o más por defecto
   - Referencia de fuente: en las diapositivas que citen cifras o hechos, indica la fuente (nombre del medio y año/mes, o un número de nota al pie) justo debajo del pasaje correspondiente, con un tamaño de letra pequeño de unos 8px
   - Imágenes: si se usan, incrústalas en el HTML como URI de datos base64 (prohibidas las referencias a archivos externos o URLs externas). Si el archivo se vuelve excesivamente pesado, comprime la imagen antes de incrustarla

4. **Crear las diapositivas con la regla 1 diapositiva = 1 mensaje**
   - La línea del título debe ser el mensaje clave (una sola línea en forma afirmativa/concluyente). No uses títulos meramente descriptivos del tipo «Sobre…»
     - Mal ejemplo: «Sobre las tendencias del mercado»
     - Buen ejemplo: «El mercado nacional se expandirá 1,5 veces en los próximos 3 años»
   - El cuerpo debe tener como máximo 4 viñetas (cada elemento debe ser conciso, de una sola línea) o, como alternativa, un solo diagrama
   - En las diapositivas que necesiten un diagrama, reserva un área de diagrama en el centro (puede ser un marcador de posición; define el texto alternativo alt)

5. **Guardado**
   Guarda el archivo según la convención del proyecto (si no existe, `output/slides/<nombre del proyecto o tema>.html`) como HTML autocontenido, sin depender de CDN, imágenes ni fuentes externas. Debe quedar en un estado que se pueda proyectar directamente al abrirlo en el navegador.

6. **Si se crean versiones multilingües**
   Primero completa y revisa la versión en el idioma por defecto; luego vierte las traducciones en la misma plantilla para generar las versiones en otros idiomas. El nombre del archivo, para cada idioma, será `<mismo nombre>_<código de idioma>.html` (p. ej. `_es.html` / `_en.html`). Dado que la cantidad de texto varía según el idioma, vuelve a comprobar el límite de caracteres de las viñetas del cuerpo para cada idioma y ajusta el texto si se desborda (sin modificar el diseño en sí).

7. **Autorrevisión**
   Haz doble clic en el archivo HTML guardado para abrirlo en el navegador por defecto y comprueba realmente la visualización diapositiva por diapositiva, siguiendo la lista de comprobación de abajo. Si hay problemas, corrígelos antes de dar por completada la entrega.

## Ejemplos de uso

```
/slide-forge convierte outline/proposal.md en diapositivas
/slide-forge usa research/market-trends/findings.md para crear un mazo de propuesta
/slide-forge crea las diapositivas para el tema «Propuesta de adopción de agentes de IA»
```

## Lista de comprobación (antes de entregar)

- [ ] ¿Cada diapositiva tiene un solo mensaje? (¿no hay dos o más afirmaciones mezcladas?)
- [ ] Al leer solo los títulos, ¿la historia general tiene sentido? (Cómo comprobarlo: lee en voz alta, de arriba abajo, solo la línea de título de todas las diapositivas y verifica que el hilo no dé saltos bruscos ni se repita el mismo punto)
- [ ] ¿El encabezado, pie de página, márgenes y paleta de colores están unificados en todas las diapositivas?
- [ ] ¿Se usan únicamente cifras y hechos con fuente, y aparece la referencia de la fuente en la diapositiva (nota al pie o pie de página)?
- [ ] ¿Es realmente HTML autocontenido? (¿no quedan referencias a CDN, imágenes o fuentes externas?)
- [ ] ¿Se muestra correctamente en 16:9 (1280×720) sin romperse?
- [ ] ¿El tamaño de fuente del cuerpo es legible a la distancia de proyección? (referencia: cuerpo de 18px o más; cada viñeta, de una línea concisa)
- [ ] ¿El contraste entre el color de fondo y el color del texto es suficiente? (¿no hay texto gris claro sobre fondo claro?)
- [ ] ¿Se evita distinguir significados solo por color? (p. ej., rojo = mal / verde = bien también indicado con símbolos o etiquetas, no solo con el color)
- [ ] ¿Los marcadores de posición de diagramas e imágenes tienen definido el texto alternativo alt?
- [ ] ¿El destino de guardado y el nombre del archivo siguen la convención del proyecto (si no existe, `output/slides/<nombre>.html`)?
- [ ] ¿No hay erratas ni errores en las cifras, unidades o dígitos (yenes/dólares, %, etc.)?
- [ ] Si se crean versiones multilingües, ¿en cada idioma se ha comprobado que no haya texto desbordado, saltos de línea extraños ni fuentes que se rompan?

## Notas
- Guarda siempre el resultado dentro de `output/slides/`. Normaliza el nombre de archivo a solo caracteres alfanuméricos, guiones y guiones bajos, y rechaza entradas que contengan `..`, una barra inicial o caracteres de control (para evitar escrituras en ubicaciones no deseadas).

- La salida en PPTX se considera solo si el usuario la solicita explícitamente (por defecto es HTML)
- No empieces a convertir a diapositivas sin tener listos el esquema y los datos con fuente. Primero, en los pasos 1 y 2, reúne las entradas y confirma la convención de destino de guardado
- Un único diagrama suelto o un PPTX que requiera animaciones elaboradas quedan fuera del alcance de este comando
