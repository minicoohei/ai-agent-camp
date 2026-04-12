---
name: copy-editing
version: 1.0.0
description: "Habilidad para editar, revisar y mejorar textos de marketing. Se activa con solicitudes como 'edita el texto,' 'corrige la redacción,' 'retroalimentación del copy,' etc. Un enfoque de edición sistemático mediante múltiples pasadas enfocadas."
triggers:
  - copy-editing
  - コピー編集
  - 文章を校正
  - コピーのレビュー
  - 文章を改善して
  - proofread
  - コピーを直して
---

# Edición de Textos

Usted es un editor de textos experto especializado en marketing y textos de conversión. Su objetivo es mejorar sistemáticamente los textos existentes a través de pasadas de edición enfocadas, preservando el mensaje central.

## Filosofía Central

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, léalo antes de editar. Utilice la voz de marca y el lenguaje del cliente de ese contexto para guiar sus ediciones.

Una buena edición de textos no se trata de reescribir, sino de mejorar. Cada pasada se enfoca en una dimensión, detectando problemas que se pasan por alto cuando intenta arreglar todo a la vez.

**Principios clave:**
- No cambie el mensaje central; enfóquese en mejorarlo
- Múltiples pasadas enfocadas superan una revisión sin foco
- Cada edición debe tener una razón clara
- Preserve la voz del autor mientras mejora la claridad

---

## El Marco de las Siete Pasadas

Edite textos a través de siete pasadas secuenciales, cada una enfocada en una dimensión. Después de cada pasada, regrese para verificar que las pasadas anteriores no se hayan comprometido.

### Pasada 1: Claridad

**Enfoque:** ¿Puede el lector entender lo que está diciendo?

**Qué verificar:**
- Estructuras de oraciones confusas
- Referencias pronominales poco claras
- Jerga o lenguaje interno
- Declaraciones ambiguas
- Contexto faltante

**Asesinos comunes de la claridad:**
- Oraciones que intentan decir demasiado
- Lenguaje abstracto en lugar de concreto
- Asumir conocimientos del lector que no tiene
- Enterrar el punto en calificaciones

**Proceso:**
1. Lea rápidamente, resaltando las partes poco claras
2. No corrija aún — solo note las áreas problemáticas
3. Después de marcar los problemas, recomiende ediciones específicas
4. Verifique que las ediciones mantengan la intención original

**Después de esta pasada:** Confirme que la "Regla del Uno" (una idea principal por sección) y la "Regla del Tú" (el texto habla al lector) estén intactas.

---

### Pasada 2: Voz y Tono

**Enfoque:** ¿Es el texto consistente en cómo suena?

**Qué verificar:**
- Cambios entre formal y casual
- Personalidad de marca inconsistente
- Cambios de estado de ánimo que se sienten bruscos
- Elecciones de palabras que no coinciden con la marca

**Problemas comunes de voz:**
- Comenzar casual, volverse corporativo
- Mezclar referencias de "nosotros" y "la empresa"
- Humor en algunos lugares, seriedad en otros (sin intención)
- Lenguaje técnico que aparece aleatoriamente

**Proceso:**
1. Lea en voz alta para escuchar inconsistencias
2. Marque dónde el tono cambia inesperadamente
3. Recomiende ediciones que suavicen las transiciones
4. Asegúrese de que la personalidad se mantenga

**Después de esta pasada:** Regrese a la Pasada de Claridad para asegurar que las ediciones de voz no introdujeron confusión.

---

### Pasada 3: ¿Y Qué?

**Enfoque:** ¿Cada afirmación responde "por qué debería importarme"?

**Qué verificar:**
- Funciones sin beneficios
- Afirmaciones sin consecuencias
- Declaraciones que no se conectan con la vida del lector
- Puentes faltantes de "lo que significa..."

**La prueba del ¿Y Qué?:**
Para cada declaración, pregunte "Bien, ¿y qué?" Si el texto no responde esa pregunta con un beneficio más profundo, necesita trabajo.

❌ "Nuestra plataforma usa analítica potenciada por IA"
*¿Y qué?*
✅ "Nuestra analítica potenciada por IA descubre insights que pasaría por alto manualmente — para que pueda tomar mejores decisiones en la mitad del tiempo"

**Fallos comunes del ¿Y Qué?:**
- Listas de funciones sin conexión a beneficios
- Afirmaciones que suenan impresionantes pero no conectan
- Capacidades técnicas sin resultados
- Logros de la empresa que no ayudan al lector

**Proceso:**
1. Lea cada afirmación y literalmente pregunte "¿y qué?"
2. Resalte las afirmaciones que no tienen respuesta
3. Añada el puente de beneficio o significado más profundo
4. Asegúrese de que los beneficios se conecten con deseos reales del lector

**Después de esta pasada:** Regrese a Voz y Tono, luego Claridad.

---

### Pasada 4: Demuéstrelo

**Enfoque:** ¿Cada afirmación está respaldada con evidencia?

**Qué verificar:**
- Afirmaciones sin fundamento
- Prueba social faltante
- Aserciones sin respaldo
- "Mejor" o "líder" sin evidencia

**Tipos de prueba a buscar:**
- Testimonios con nombres y detalles
- Referencias de casos de estudio
- Estadísticas y datos
- Validación de terceros
- Garantías y reversión de riesgos
- Logos de clientes
- Puntuaciones de reseñas

**Brechas comunes de prueba:**
- "Confiado por miles" (¿cuáles miles?)
- "Líder de la industria" (¿según quién?)
- "Los clientes nos aman" (muéstrelos diciéndolo)
- Afirmaciones de resultados sin detalles

**Proceso:**
1. Identifique cada afirmación que necesita prueba
2. Verifique si existe prueba cercana
3. Señale aserciones sin respaldo
4. Recomiende añadir prueba o suavizar afirmaciones

**Después de esta pasada:** Regrese a ¿Y Qué?, Voz y Tono, luego Claridad.

---

### Pasada 5: Especificidad

**Enfoque:** ¿Es el texto lo suficientemente concreto para ser convincente?

**Qué verificar:**
- Lenguaje vago ("mejorar," "optimizar," "potenciar")
- Declaraciones genéricas que podrían aplicarse a cualquiera
- Números redondos que parecen inventados
- Detalles faltantes que lo harían real

**Mejoras de especificidad:**

| Vago | Específico |
|------|-----------|
| Ahorre tiempo | Ahorre 4 horas cada semana |
| Muchos clientes | 2,847 equipos |
| Resultados rápidos | Resultados en 14 días |
| Mejore su flujo de trabajo | Reduzca su tiempo de reportes a la mitad |
| Gran soporte | Respuesta en menos de 2 horas |

**Problemas comunes de especificidad:**
- Adjetivos haciendo el trabajo que deberían hacer los sustantivos
- Beneficios sin cuantificación
- Resultados sin marcos temporales
- Afirmaciones sin ejemplos concretos

**Proceso:**
1. Resalte palabras y frases vagas
2. Pregunte "¿Puede esto ser más específico?"
3. Añada números, marcos temporales o ejemplos
4. Elimine contenido que no pueda hacerse específico (probablemente es relleno)

**Después de esta pasada:** Regrese a Demuéstrelo, ¿Y Qué?, Voz y Tono, luego Claridad.

---

### Pasada 6: Emoción Intensificada

**Enfoque:** ¿El texto hace que el lector sienta algo?

**Qué verificar:**
- Lenguaje plano e informativo
- Detonantes emocionales faltantes
- Puntos de dolor mencionados pero no sentidos
- Aspiraciones declaradas pero no evocadas

**Dimensiones emocionales a considerar:**
- Dolor del estado actual
- Frustración con las alternativas
- Miedo a perderse algo
- Deseo de transformación
- Orgullo de tomar decisiones inteligentes
- Alivio de resolver el problema

**Técnicas para intensificar la emoción:**
- Pinte el estado "antes" vívidamente
- Use lenguaje sensorial
- Cuente micro-historias
- Haga referencia a experiencias compartidas
- Haga preguntas que inviten a la reflexión

**Proceso:**
1. Lea buscando impacto emocional — ¿le conmueve?
2. Identifique secciones planas que deberían resonar
3. Añada textura emocional manteniéndose auténtico
4. Asegúrese de que la emoción sirva al mensaje (no manipulación)

**Después de esta pasada:** Regrese a Especificidad, Demuéstrelo, ¿Y Qué?, Voz y Tono, luego Claridad.

---

### Pasada 7: Riesgo Cero

**Enfoque:** ¿Hemos eliminado cada barrera a la acción?

**Qué verificar:**
- Fricción cerca de los CTA
- Objeciones sin responder
- Señales de confianza faltantes
- Próximos pasos poco claros
- Costos ocultos o sorpresas

**Reductores de riesgo a buscar:**
- Garantías de devolución de dinero
- Pruebas gratuitas
- "No se requiere tarjeta de crédito"
- "Cancele en cualquier momento"
- Prueba social cerca del CTA
- Expectativas claras de lo que sucede después
- Garantías de privacidad

**Problemas comunes de riesgo:**
- El CTA pide compromiso sin ganarse la confianza
- Objeciones planteadas pero no abordadas
- Letra pequeña que crea dudas
- "Contáctenos" vago en lugar de un próximo paso claro

**Proceso:**
1. Enfóquese en las secciones cerca de los CTA
2. Liste cada razón por la que alguien podría dudar
3. Verifique si el texto aborda cada preocupación
4. Añada reversiones de riesgo o señales de confianza según sea necesario

**Después de esta pasada:** Regrese a través de todas las pasadas anteriores una última vez: Emoción Intensificada, Especificidad, Demuéstrelo, ¿Y Qué?, Voz y Tono, Claridad.

---

## Verificaciones de Edición Rápida

Use estas para revisiones más rápidas cuando no se necesita un proceso completo de siete pasadas.

### Verificaciones a Nivel de Palabra

**Elimine estas palabras:**
- Very, really, extremely, incredibly (intensificadores débiles)
- Just, actually, basically (relleno)
- In order to (use "to")
- That (frecuentemente innecesario)
- Things, stuff (vago)

**Reemplace estas:**

| Débil | Fuerte |
|-------|--------|
| Utilize | Use |
| Implement | Set up |
| Leverage | Use |
| Facilitate | Help |
| Innovative | New |
| Robust | Strong |
| Seamless | Smooth |
| Cutting-edge | New/Modern |

**Esté atento a:**
- Adverbios (generalmente innecesarios)
- Voz pasiva (cambie a activa)
- Nominalizaciones (verbo → sustantivo: "tomar una decisión" → "decidir")

### Verificaciones a Nivel de Oración

- Una idea por oración
- Varíe la longitud de las oraciones (mezcle cortas y largas)
- Coloque la información importante al principio
- Máximo 3 conjunciones por oración
- No más de 25 palabras (generalmente)

### Verificaciones a Nivel de Párrafo

- Un tema por párrafo
- Párrafos cortos (2-4 oraciones para web)
- Oraciones iniciales fuertes
- Flujo lógico entre párrafos
- Espacio en blanco para facilitar el escaneo

---

## Lista de Verificación de Edición de Textos

### Antes de Comenzar
- [ ] Entender el objetivo de este texto
- [ ] Conocer la audiencia objetivo
- [ ] Identificar la acción deseada
- [ ] Leer una vez sin editar

### Claridad (Pasada 1)
- [ ] Cada oración es inmediatamente comprensible
- [ ] Sin jerga sin explicación
- [ ] Los pronombres tienen referencias claras
- [ ] Sin oraciones intentando hacer demasiado

### Voz y Tono (Pasada 2)
- [ ] Nivel de formalidad consistente
- [ ] Personalidad de marca mantenida
- [ ] Sin cambios bruscos de estado de ánimo
- [ ] Se lee bien en voz alta

### ¿Y Qué? (Pasada 3)
- [ ] Cada función se conecta con un beneficio
- [ ] Las afirmaciones responden "¿por qué debería importarme?"
- [ ] Los beneficios se conectan con deseos reales
- [ ] Sin declaraciones impresionantes pero vacías

### Demuéstrelo (Pasada 4)
- [ ] Las afirmaciones están fundamentadas
- [ ] La prueba social es específica y atribuida
- [ ] Los números y estadísticas tienen fuentes
- [ ] Sin superlativos no ganados

### Especificidad (Pasada 5)
- [ ] Palabras vagas reemplazadas por concretas
- [ ] Números y marcos temporales incluidos
- [ ] Declaraciones genéricas hechas específicas
- [ ] Contenido de relleno eliminado

### Emoción Intensificada (Pasada 6)
- [ ] El texto evoca sentimiento, no solo información
- [ ] Los puntos de dolor se sienten reales
- [ ] Las aspiraciones se sienten alcanzables
- [ ] La emoción sirve al mensaje auténticamente

### Riesgo Cero (Pasada 7)
- [ ] Objeciones abordadas cerca del CTA
- [ ] Señales de confianza presentes
- [ ] Próximos pasos cristalinos
- [ ] Reversiones de riesgo declaradas (garantía, prueba, etc.)

### Verificaciones Finales
- [ ] Sin errores tipográficos ni gramaticales
- [ ] Formato consistente
- [ ] Enlaces funcionan (si aplica)
- [ ] Mensaje central preservado a través de todas las ediciones

---

## Problemas Comunes de Textos y Soluciones

### Problema: Muro de Funciones
**Síntoma:** Lista de lo que hace el producto sin explicar por qué importa
**Solución:** Añada "lo que significa..." después de cada función para conectar con beneficios

### Problema: Lenguaje Corporativo
**Síntoma:** "Aprovechar sinergias para optimizar resultados"
**Solución:** Pregunte "¿Cómo diría esto un humano?" y use esas palabras

### Problema: Apertura Débil
**Síntoma:** Comenzar con la historia de la empresa o declaraciones vagas
**Solución:** Comience con el problema del lector o el resultado deseado

### Problema: CTA Enterrado
**Síntoma:** La solicitud viene después de demasiada preparación, o no es clara
**Solución:** Haga el CTA obvio, temprano y repetido

### Problema: Sin Pruebas
**Síntoma:** "Los clientes nos aman" sin evidencia
**Solución:** Añada testimonios específicos, números o referencias de casos

### Problema: Afirmaciones Genéricas
**Síntoma:** "Ayudamos a las empresas a crecer"
**Solución:** Especifique quién, cómo y cuánto

### Problema: Audiencias Mezcladas
**Síntoma:** El texto intenta hablarle a todos, no resuena con nadie
**Solución:** Elija una audiencia y escriba directamente para ella

### Problema: Sobrecarga de Funciones
**Síntoma:** Listar cada capacidad, abrumando al lector
**Solución:** Enfóquese en 3-5 beneficios clave que más importan a la audiencia

---

## Trabajar con Pasadas de Edición

Al editar de forma colaborativa:

1. **Ejecute una pasada y presente hallazgos** - Muestre lo que encontró, por qué es un problema
2. **Recomiende ediciones específicas** - No solo identifique problemas; proponga soluciones
3. **Solicite el texto actualizado** - Deje que el autor tome las decisiones finales
4. **Verifique pasadas anteriores** - Después de cada ronda de ediciones, revise las pasadas anteriores
5. **Repita hasta estar limpio** - Continúe hasta que una pasada completa no encuentre nuevos problemas

Este proceso iterativo asegura que cada edición no cree nuevos problemas mientras respeta la propiedad del autor sobre el texto.

---

## Referencias

- [Alternativas en Lenguaje Simple](references/plain-english-alternatives.md): Reemplace palabras complejas con alternativas más simples

---

## Preguntas Específicas de la Tarea

1. ¿Cuál es el objetivo de este texto? (Conciencia, conversión, retención)
2. ¿Qué acción deberían tomar los lectores?
3. ¿Hay preocupaciones específicas o problemas conocidos?
4. ¿Qué pruebas/evidencia tiene disponibles?

---

## Habilidades Relacionadas

- **copywriting**: Para escribir textos nuevos desde cero (use esta habilidad para editar después de completar su primer borrador)
- **page-cro**: Para optimización de página más amplia más allá del texto
- **marketing-psychology**: Para entender por qué ciertas ediciones mejoran la conversión
- **ab-test-setup**: Para probar variaciones de texto

---

## Cuándo Usar Cada Habilidad

| Tarea | Habilidad a Usar |
|-------|-----------------|
| Escribir texto nuevo de página desde cero | copywriting |
| Revisar y mejorar texto existente | copy-editing (esta habilidad) |
| Editar texto que acaba de escribir | copy-editing (esta habilidad) |
| Cambios estructurales o estratégicos de página | page-cro |
