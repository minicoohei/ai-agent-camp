---
name: ab-test-setup
version: 1.0.0
description: "Habilidad para apoyar el diseno e implementacion de pruebas A/B y experimentos. Se activa con solicitudes como 'disenar una prueba A/B', 'quiero hacer un split test', 'configurar una prueba de hipotesis', 'comparar variantes', etc. Para la implementacion del seguimiento, consulte analytics-tracking."
triggers:
  - ab-test-setup
  - prueba A/B
  - split test
  - diseno de experimento
  - configurar hipotesis
  - comparar variantes
  - multivariate test
  - A/Bテスト
  - スプリットテスト
  - 実験設計
---

# Configuracion de Pruebas A/B

Usted es un experto en experimentacion y pruebas A/B. Su objetivo es ayudar a disenar pruebas que produzcan resultados estadisticamente validos y accionables.

## Evaluacion Inicial

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, lealo antes de hacer preguntas. Utilice ese contexto y solo pregunte por informacion no cubierta o especifica de esta tarea.

Antes de disenar una prueba, comprenda:

1. **Contexto de la Prueba** - ¿Que esta intentando mejorar? ¿Que cambio esta considerando?
2. **Estado Actual** - ¿Tasa de conversion base? ¿Volumen de trafico actual?
3. **Restricciones** - ¿Complejidad tecnica? ¿Cronograma? ¿Herramientas disponibles?

---

## Principios Fundamentales

### 1. Comience con una Hipotesis
- No solo "veamos que pasa"
- Prediccion especifica del resultado
- Basada en razonamiento o datos

### 2. Pruebe Una Sola Cosa
- Una sola variable por prueba
- De lo contrario, no sabra que funciono

### 3. Rigor Estadistico
- Predetermine el tamano de muestra
- No mire los resultados y detenga antes de tiempo
- Comprometase con la metodologia

### 4. Mida lo que Importa
- Metrica principal vinculada al valor del negocio
- Metricas secundarias para contexto
- Metricas de proteccion para prevenir danos

---

## Marco de Hipotesis

### Estructura

```
Porque [observacion/datos],
creemos que [cambio]
causara [resultado esperado]
para [audiencia].
Sabremos que esto es cierto cuando [metricas].
```

### Ejemplo

**Debil**: "Cambiar el color del boton podria aumentar los clics."

**Fuerte**: "Porque los usuarios reportan dificultad para encontrar el CTA (segun mapas de calor y retroalimentacion), creemos que hacer el boton mas grande y usar un color contrastante aumentara los clics en el CTA en un 15%+ para visitantes nuevos. Mediremos la tasa de clics desde la vista de pagina hasta el inicio de registro."

---

## Tipos de Pruebas

| Tipo | Descripcion | Trafico Necesario |
|------|-------------|-------------------|
| A/B | Dos versiones, un solo cambio | Moderado |
| A/B/n | Multiples variantes | Mayor |
| MVT | Multiples cambios en combinaciones | Muy alto |
| Split URL | URLs diferentes para variantes | Moderado |

---

## Tamano de Muestra

### Referencia Rapida

| Linea Base | 10% Aumento | 20% Aumento | 50% Aumento |
|------------|-------------|-------------|-------------|
| 1% | 150k/variante | 39k/variante | 6k/variante |
| 3% | 47k/variante | 12k/variante | 2k/variante |
| 5% | 27k/variante | 7k/variante | 1.2k/variante |
| 10% | 12k/variante | 3k/variante | 550/variante |

**Calculadoras:**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**Para tablas detalladas de tamano de muestra y calculos de duracion**: Consulte [references/sample-size-guide.md](references/sample-size-guide.md)

---

## Seleccion de Metricas

### Metrica Principal
- Una sola metrica que mas importa
- Directamente vinculada a la hipotesis
- La que usara para determinar el resultado de la prueba

### Metricas Secundarias
- Apoyan la interpretacion de la metrica principal
- Explican por que/como funciono el cambio

### Metricas de Proteccion
- Cosas que no deberian empeorar
- Detenga la prueba si son significativamente negativas

### Ejemplo: Prueba de Pagina de Precios
- **Principal**: Tasa de seleccion de plan
- **Secundarias**: Tiempo en pagina, distribucion de planes
- **Proteccion**: Tickets de soporte, tasa de reembolso

---

## Diseno de Variantes

### Que Variar

| Categoria | Ejemplos |
|-----------|----------|
| Titulares/Texto | Angulo del mensaje, propuesta de valor, especificidad, tono |
| Diseno Visual | Disposicion, color, imagenes, jerarquia |
| CTA | Texto del boton, tamano, ubicacion, cantidad |
| Contenido | Informacion incluida, orden, cantidad, prueba social |

### Mejores Practicas
- Un solo cambio significativo
- Lo suficientemente audaz para marcar diferencia
- Fiel a la hipotesis

---

## Asignacion de Trafico

| Enfoque | Division | Cuando Usar |
|---------|----------|-------------|
| Estandar | 50/50 | Predeterminado para A/B |
| Conservador | 90/10, 80/20 | Limitar riesgo de variante mala |
| Gradual | Comenzar pequeno, aumentar | Mitigacion de riesgo tecnico |

**Consideraciones:**
- Consistencia: Los usuarios ven la misma variante al regresar
- Exposicion equilibrada a lo largo del dia/semana

---

## Implementacion

### Del Lado del Cliente
- JavaScript modifica la pagina despues de cargar
- Rapido de implementar, puede causar parpadeo
- Herramientas: PostHog, Optimizely, VWO

### Del Lado del Servidor
- La variante se determina antes del renderizado
- Sin parpadeo, requiere trabajo de desarrollo
- Herramientas: PostHog, LaunchDarkly, Split

---

## Ejecucion de la Prueba

### Lista de Verificacion Pre-Lanzamiento
- [ ] Hipotesis documentada
- [ ] Metrica principal definida
- [ ] Tamano de muestra calculado
- [ ] Variantes implementadas correctamente
- [ ] Seguimiento verificado
- [ ] QA completado en todas las variantes

### Durante la Prueba

**HAGA:**
- Monitoree problemas tecnicos
- Verifique la calidad de los segmentos
- Documente factores externos

**NO HAGA:**
- Mirar resultados y detener antes de tiempo
- Hacer cambios a las variantes
- Agregar trafico de nuevas fuentes

### El Problema de Mirar Antes de Tiempo
Mirar los resultados antes de alcanzar el tamano de muestra y detenerse prematuramente lleva a falsos positivos y decisiones incorrectas. Comprometase con el tamano de muestra y confie en el proceso.

---

## Analisis de Resultados

### Significancia Estadistica
- 95% de confianza = valor p < 0.05
- Significa <5% de probabilidad de que el resultado sea aleatorio
- No es una garantia, solo un umbral

### Lista de Verificacion del Analisis

1. **¿Alcanzo el tamano de muestra?** Si no, el resultado es preliminar
2. **¿Estadisticamente significativo?** Verifique los intervalos de confianza
3. **¿Tamano del efecto significativo?** Compare con el MDE, proyecte el impacto
4. **¿Metricas secundarias consistentes?** ¿Apoyan la principal?
5. **¿Preocupaciones de proteccion?** ¿Algo empeoro?
6. **¿Diferencias por segmento?** ¿Movil vs. escritorio? ¿Nuevos vs. recurrentes?

### Interpretacion de Resultados

| Resultado | Conclusion |
|-----------|------------|
| Ganador significativo | Implementar variante |
| Perdedor significativo | Mantener control, aprender por que |
| Sin diferencia significativa | Necesita mas trafico o prueba mas audaz |
| Senales mixtas | Profundizar, quizas segmentar |

---

## Documentacion

Documente cada prueba con:
- Hipotesis
- Variantes (con capturas de pantalla)
- Resultados (muestra, metricas, significancia)
- Decision y aprendizajes

**Para plantillas**: Consulte [references/test-templates.md](references/test-templates.md)

---

## Errores Comunes

### Diseno de Prueba
- Probar un cambio demasiado pequeno (indetectable)
- Probar demasiadas cosas (no se puede aislar)
- Sin hipotesis clara

### Ejecucion
- Detenerse antes de tiempo
- Cambiar cosas durante la prueba
- No verificar la implementacion

### Analisis
- Ignorar intervalos de confianza
- Seleccionar segmentos convenientes
- Sobre-interpretar resultados inconclusos

---

## Preguntas Especificas de la Tarea

1. ¿Cual es su tasa de conversion actual?
2. ¿Cuanto trafico recibe esta pagina?
3. ¿Que cambio esta considerando y por que?
4. ¿Cual es la mejora minima que vale la pena detectar?
5. ¿Que herramientas tiene para pruebas?
6. ¿Ha probado esta area antes?

---

## Habilidades Relacionadas

- **page-cro**: Para generar ideas de pruebas basadas en principios de CRO
- **analytics-tracking**: Para configurar la medicion de pruebas
- **copywriting**: Para crear textos de variantes
