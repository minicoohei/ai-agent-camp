---
name: slide-forge
version: 1.1.0
description: "Skill para construir, a partir de un esquema (outline) o de resultados de investigación, presentaciones con un formato uniforme (HTML autocontenido, 16:9). Se usa ante solicitudes como «conviértelo en diapositivas», «crea un mazo de propuesta», «pásalo a diapositivas» o «slide forge»."
triggers:
  - conviértelo en diapositivas
  - crea un mazo de propuesta
  - pásalo a diapositivas
  - resúmelo en un mazo de diapositivas
  - haz una presentación
  - crea una presentación
  - genera las diapositivas
  - slide forge
  - make slides
  - turn this into a slide deck
  - create a presentation
---

# Slide Forge — Forjando diapositivas a partir del esquema

Skill que convierte un esquema (outline) o resultados de investigación en diapositivas HTML autocontenidas, listas para proyectar y compartir tal cual. La clave no está en diseñar cada diapositiva por separado, sino en **verter el contenido en una plantilla común**, de modo que el formato general quede uniforme automáticamente.

## Resumen

- El formato de salida por defecto es **HTML autocontenido (16:9, 1280×720)**. No depende de CDN externos (bibliotecas JS/CSS cargadas desde otro servidor en internet), imágenes externas ni fuentes tipográficas externas; así el archivo se puede abrir y visualizar incluso sin conexión a internet
- Se aplica estrictamente la regla de 1 diapositiva = 1 mensaje, para evitar sobrecargar el contenido
- Antes de verter el contenido, primero se define el encabezado (etiqueta de sección + título) y el pie de página (nombre del proyecto, número de página) comunes a todas las páginas

## Sobre el nombre de la skill

Esta skill no está pensada para un proyecto específico; se ha nombrado como skill de uso general. Si en el entorno ya existe otra skill llamada `slide-forge` con una definición distinta, al introducirla verifica primero si existe: si no existe, añádela tal cual; si existe, el contenido de este SKILL.md prevalece y debe sobrescribirla/integrarse con ella (para evitar que un registro duplicado deje indeterminado a qué definición apunta el disparador).

Nota: el slide-forge que se trata en la lección lesson03 de este repositorio («module29-slide-forge») es algo **distinto**: el OSS externo `github.com/minicoohei/slide-forge` (una CLI de Python que genera PPTX editable y otros formatos). Esta skill es una variante ligera que construye rápidamente una presentación HTML autocontenida a partir de un esquema; al escribir `/slide-forge` se activa esta skill (no la CLI de Python de la lección). Cuando necesites PPTX editable o salida en varios formatos, sigue los pasos de la lección.

## Casos de uso

Escenarios concretos en los que esta skill resulta útil:

1. **Resultados de investigación → mazo de propuesta**: cuando se quiere dar formato de diapositivas de propuesta, dirigidas a quienes toman decisiones, a los resultados de una investigación/análisis (hechos y cifras con fuente)
2. **Esquema → HTML para proyectar**: cuando ya existe un esquema (estructura de capítulos, mensajes clave) y se quiere volcarlo en diapositivas con un aspecto uniforme
3. **Unificar el formato de notas o documentos existentes**: cuando se quiere reordenar notas o listas con aspecto dispar en diapositivas con una plantilla unificada
4. **Producción en serie de diapositivas multilingües**: cuando se quieren crear varios juegos de diapositivas en distintos idiomas a partir del mismo esquema y la misma plantilla
5. **Mazo ligero para uso interno**: cuando se necesita algo que se pueda mostrar de inmediato, en formato de diapositivas, sin tener que abrir PowerPoint
6. **Mazo de propuesta con fotos o gráficos**: cuando se quieren incluir fotos de producto o imágenes de gráficos (las imágenes se incrustan en el HTML como URI de datos base64; no se crean referencias externas)

**Casos en los que es mejor NO usarla (fuera de alcance)**:
- PPTX que requiera animaciones y transiciones de pantalla elaboradas (→ si se solicita explícitamente, considerar aparte una conversión a PPTX; el formato por defecto es HTML)
- Un único diagrama o infografía suelta (→ la skill `diagram-generator` es más adecuada)
- Cuando se quiere editar directamente, tal cual, una plantilla existente de PowerPoint o Google Slides
- Dashboards interactivos o informes con filtros que manejan grandes volúmenes de datos (→ la skill `interactive-dashboard-builder` es más adecuada)
- Etapa en la que aún no se dispone de hechos ni cifras con fuente (→ si el entorno cuenta con una skill de verificación de hechos como `ycp-research-factcheck`, úsala primero para investigar y verificar; si no existe, confirma las fuentes por tu cuenta antes de usar esta skill)
- Mazos con muchas diapositivas (más de 50 aprox.) o de gran extensión que abarcan varias secciones (→ un solo archivo se vuelve pesado y difícil de mantener; divide por capítulos en varios archivos o reduce el número de diapositivas antes de usarla)

## Workflow

1. **Confirmar las entradas y las convenciones de guardado**
   Primero confirma con el usuario el nombre del proyecto/cliente (se usará en el nombre del archivo). Si existe un archivo de esquema (sigue la convención del proyecto; p. ej. `outline/proposal.md`), úsalo. Si no existe, entrevista al usuario en el momento o, si el entorno cuenta con una skill de creación de esquemas como `ycp-proposal-outline`, úsala primero para crear el esquema y luego continúa. Si se van a usar cifras o hechos, consulta resultados de investigación con fuente (sigue la convención del proyecto; p. ej. `research/<tema>/findings.md`). En proyectos sin una convención de guardado establecida, confirma aquí con el usuario el destino de salida que se usará en el paso 4
2. **Definir la plantilla común** (autocontenida con CSS dentro de un único archivo)
   - Formato fijo 16:9 (1280×720), 1 sección = 1 diapositiva
   - Común a todas las páginas: encabezado superior (etiqueta de sección + título) / pie de página inferior (nombre del proyecto, número de página)
   - Paleta de colores: hasta 2 colores + gradaciones de gris. Si no se especifica lo contrario, por defecto se usa azul marino (#1F3A5F) como color principal, naranja (#E8833A) como color de acento, y gris (#333333/#666666) para el cuerpo del texto. Si se conoce el color de marca del proyecto, tiene prioridad sobre lo anterior
   - Tipografía: fuentes del sistema (prohibido cargar fuentes externas). El tamaño de fuente del cuerpo debe ser de 18px o más por defecto
   - En las diapositivas que citen cifras o hechos, indica la fuente (nombre del medio y año/mes, o un número de nota al pie) justo debajo del pasaje correspondiente, con un tamaño de letra pequeño de unos 8px
   - Si se usan imágenes, incrústalas en el HTML como URI de datos base64 (prohibidas las referencias a archivos externos o URLs externas). Si la incrustación hace que el archivo se vuelva excesivamente pesado, comprime la imagen antes de incrustarla
3. **Construir con la regla 1 diapositiva = 1 mensaje**
   - La línea del título es el mensaje clave (una sola línea en forma afirmativa/concluyente). Prohibidos los títulos meramente descriptivos del tipo «Sobre…»
     - Mal ejemplo: «Sobre las tendencias del mercado»
     - Buen ejemplo: «El mercado nacional se expandirá 1,5 veces en los próximos 3 años»
   - El cuerpo debe tener como máximo 4 viñetas (cada elemento debe ser conciso, de una sola línea) o, como alternativa, un solo diagrama. No sobrecargar el contenido
   - En las diapositivas que necesiten un diagrama, reserva un área de diagrama en el centro (puede ser un marcador de posición; deja la estructura preparada para insertar la imagen más adelante y define el texto alternativo alt)
4. **Generar la salida**
   Guarda el archivo según la convención del proyecto (si no existe, `output/slides/<nombre del proyecto o tema>.html`) como HTML autocontenido (sin depender de CDN, imágenes ni fuentes externas). Debe quedar en un estado que se pueda proyectar directamente al abrirlo en el navegador. Si se van a crear versiones en varios idiomas, primero completa y revisa la versión en el idioma por defecto; luego, para cada idioma, guarda el archivo como `<mismo nombre>_<código de idioma>.html` (p. ej. `_es.html` / `_en.html`), manteniendo la plantilla (colores y diseño) igual y sustituyendo únicamente el texto. Dado que la cantidad de texto varía según el idioma, vuelve a comprobar el límite de caracteres del cuerpo para cada idioma y ajusta el texto si se desborda (sin modificar el diseño en sí)
5. **Autorrevisión**
   Haz doble clic en el archivo HTML guardado para abrirlo en el navegador por defecto y comprueba realmente la visualización diapositiva por diapositiva; antes de entregar, verifica siempre la lista de comprobación de abajo

## Lista de comprobación (antes de entregar)

- [ ] ¿Cada diapositiva tiene **un solo mensaje**? (¿no hay dos o más afirmaciones mezcladas en una misma diapositiva?)
- [ ] Al **leer solo los títulos**, ¿la historia general tiene sentido? (Cómo comprobarlo: lee en voz alta, de arriba abajo, solo la línea de título de todas las diapositivas y verifica que el hilo no dé saltos bruscos ni se repita el mismo punto)
- [ ] ¿El **encabezado, pie de página, márgenes y paleta de colores están unificados** en todas las diapositivas?
- [ ] ¿Se usan **únicamente cifras y hechos con fuente**, y aparece la referencia de la fuente en la diapositiva (nota al pie o pie de página)?
- [ ] ¿Es realmente **HTML autocontenido**? (¿no quedan referencias a CDN, imágenes o fuentes externas?)
- [ ] ¿Se muestra correctamente en **16:9 (1280×720)** sin romperse? (¿sin desbordamiento de texto ni elementos que se salen del marco?)
- [ ] ¿El **tamaño de fuente del cuerpo es legible a la distancia de proyección**? (referencia: cuerpo de 18px o más; cada viñeta, de una línea concisa)
- [ ] ¿El **contraste entre el color de fondo y el color del texto es suficiente**? (¿no hay texto gris claro sobre fondo claro?)
- [ ] ¿Se evita **distinguir significados solo por color**? (p. ej., rojo = mal / verde = bien también indicado con símbolos o etiquetas, no solo con el color)
- [ ] ¿Los marcadores de posición de diagramas e imágenes tienen definido el **texto alternativo alt**?
- [ ] ¿El destino de guardado y el nombre del archivo siguen la **convención del proyecto** (si no existe, `output/slides/<nombre>.html`)?
- [ ] ¿No hay erratas ni errores en las cifras, unidades o dígitos (yenes/dólares, %, etc.)?
- [ ] Si se crean versiones multilingües, ¿en cada idioma se ha comprobado que **no haya texto desbordado, saltos de línea extraños ni fuentes que se rompan**?

## Notas
- Guarda siempre el resultado dentro de `output/slides/`. Normaliza el nombre de archivo a solo caracteres alfanuméricos, guiones y guiones bajos, y rechaza entradas que contengan `..`, una barra inicial o caracteres de control (para evitar escrituras en ubicaciones no deseadas).

- La salida en PPTX se considera **solo si se solicita explícitamente** (por defecto es HTML)
- Usa únicamente cifras y hechos que figuren en resultados de investigación con fuente. No añadas números decorativos sin fuente
- No empieces a convertir a diapositivas sin tener el esquema o los datos con fuente. Primero reúne las entradas (no te saltes el paso 1 del Workflow)
