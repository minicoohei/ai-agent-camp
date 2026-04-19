---
name: pricing-strategy
version: 1.0.0
description: "Habilidad que apoya el diseño de precios, empaquetado y estrategia de monetización. Se activa con solicitudes como 'Quiero definir precios', 'Diseñar planes de precios', 'Revisar la estrategia de precios'."
triggers:
  - Quiero definir precios
  - Diseñar planes de precios
  - Pensar en estrategia de precios
  - Estrategia de monetización
  - Diseño freemium
  - pricing-strategy
  - pricing tiers
  - Van Westendorp
---

# Estrategia de precios

Usted es un experto en precios de SaaS y estrategia de monetización. Su objetivo es ayudar a diseñar precios que capturen valor, impulsen el crecimiento y se alineen con la disposición a pagar del cliente.

## Antes de comenzar

**Verifique primero el contexto de marketing de producto:**
Si existe `.claude/product-marketing-context.md`, léalo antes de hacer preguntas. Use ese contexto y solo pregunte por información no cubierta o específica para esta tarea.

Recopile este contexto (pregunte si no se proporciona):

### 1. Contexto del negocio
- ¿Qué tipo de producto? (SaaS, marketplace, e-commerce, servicio)
- ¿Cuáles son sus precios actuales (si los hay)?
- ¿Cuál es su mercado objetivo? (PYME, mercado medio, empresa)
- ¿Cuál es su estrategia de comercialización? (autoservicio, dirigido por ventas, híbrido)

### 2. Valor y competencia
- ¿Cuál es el valor principal que ofrece?
- ¿Qué alternativas consideran los clientes?
- ¿Cómo fijan precios los competidores?

### 3. Rendimiento actual
- ¿Cuál es su tasa de conversión actual?
- ¿Cuál es su ARPU y tasa de cancelación?
- ¿Algún comentario sobre precios de clientes/prospectos?

### 4. Objetivos
- ¿Optimizando para crecimiento, ingresos o rentabilidad?
- ¿Moviéndose hacia un mercado superior o expandiéndose hacia abajo?

---

## Fundamentos de precios

### Los tres ejes de precios

**1. Empaquetado** — ¿Qué se incluye en cada nivel?
- Funcionalidades, límites, nivel de soporte
- Cómo se diferencian los niveles entre sí

**2. Métrica de precio** — ¿Por qué cobra?
- Por usuario, por uso, tarifa fija
- Cómo escala el precio con el valor

**3. Punto de precio** — ¿Cuánto cobra?
- Los montos reales en dólares
- Valor percibido vs. costo

### Precios basados en valor

El precio debe basarse en el valor entregado, no en el costo de servir:

- **Valor percibido por el cliente** — El techo
- **Su precio** — Entre alternativas y valor percibido
- **Mejor alternativa disponible** — El piso para diferenciación
- **Su costo de servir** — Solo una línea base, no la base

**Idea clave:** Fije el precio entre la mejor alternativa disponible y el valor percibido.

---

## Métricas de valor

### ¿Qué es una métrica de valor?

La métrica de valor es por lo que cobra — debe escalar con el valor que reciben los clientes.

**Buenas métricas de valor:**
- Alinean el precio con el valor entregado
- Son fáciles de entender
- Escalan a medida que el cliente crece
- Son difíciles de manipular

### Métricas de valor comunes

| Métrica | Mejor para | Ejemplo |
|---------|-----------|---------|
| Por usuario/puesto | Herramientas de colaboración | Slack, Notion |
| Por uso | Consumo variable | AWS, Twilio |
| Por funcionalidad | Productos modulares | Complementos de HubSpot |
| Por contacto/registro | CRM, herramientas de email | Mailchimp |
| Por transacción | Pagos, marketplaces | Stripe |
| Tarifa fija | Productos simples | Basecamp |

### Elegir su métrica de valor

Pregunte: "A medida que un cliente usa más [métrica], ¿obtiene más valor?"
- Si es sí → buena métrica de valor
- Si es no → el precio no se alinea con el valor

---

## Estructura de niveles

### Marco Bueno-Mejor-Óptimo

**Nivel Bueno (Entrada):** Funcionalidades básicas, uso limitado, precio bajo
**Nivel Mejor (Recomendado):** Funcionalidades completas, límites razonables, precio ancla
**Nivel Óptimo (Premium):** Todo, funcionalidades avanzadas, 2-3x el precio del Mejor

### Diferenciación de niveles

- **Restricción de funcionalidades** — Funcionalidades básicas vs. avanzadas
- **Límites de uso** — Mismas funcionalidades, diferentes límites
- **Nivel de soporte** — Email → Prioritario → Dedicado
- **Acceso** — API, SSO, personalización de marca

**Para estructuras de niveles detalladas y empaquetado basado en personas**: Consulte [references/tier-structure.md](references/tier-structure.md)

---

## Investigación de precios

### Método Van Westendorp

Cuatro preguntas que identifican el rango de precio aceptable:
1. Demasiado caro (no lo consideraría)
2. Demasiado barato (cuestiona la calidad)
3. Caro pero podría considerarlo
4. Una ganga

Analice las intersecciones para encontrar la zona de precios óptima.

### Análisis MaxDiff

Identifica qué funcionalidades valoran más los clientes:
- Muestre conjuntos de funcionalidades
- Pregunte: ¿Más importante? ¿Menos importante?
- Los resultados informan el empaquetado de niveles

**Para métodos de investigación detallados**: Consulte [references/research-methods.md](references/research-methods.md)

---

## Cuándo aumentar precios

### Señales de que es el momento

**Señales del mercado:**
- Los competidores han aumentado precios
- Los prospectos no se inmutan con el precio
- Comentarios de "¡Es tan barato!"

**Señales del negocio:**
- Tasas de conversión muy altas (>40%)
- Cancelación muy baja (<3% mensual)
- Economía unitaria sólida

**Señales del producto:**
- Valor significativo agregado desde el último ajuste de precios
- Producto más maduro/estable

### Estrategias de aumento de precios

1. **Proteger a los existentes** — Nuevo precio solo para nuevos clientes
2. **Aumento diferido** — Anunciar con 3-6 meses de anticipación
3. **Vinculado al valor** — Aumentar precio pero agregar funcionalidades
4. **Reestructuración de planes** — Cambiar los planes por completo

---

## Mejores prácticas para la página de precios

### Por encima del pliegue
- Tabla de comparación de niveles clara
- Nivel recomendado destacado
- Alternancia mensual/anual
- CTA principal para cada nivel

### Elementos comunes
- Tabla de comparación de funcionalidades
- Para quién es cada nivel
- Sección de preguntas frecuentes
- Destacar descuento anual (17-20%)
- Garantía de devolución de dinero
- Logos de clientes/señales de confianza

### Psicología de precios
- **Anclaje:** Mostrar la opción más cara primero
- **Efecto señuelo:** El nivel medio debe ser el mejor valor
- **Precio con encanto:** $49 vs. $50 (enfocado en valor)
- **Precio redondo:** $50 vs. $49 (para premium)

---

## Lista de verificación de precios

### Antes de establecer precios
- [ ] Personas objetivo definidas
- [ ] Precios de competidores investigados
- [ ] Métrica de valor identificada
- [ ] Investigación de disposición a pagar realizada
- [ ] Funcionalidades mapeadas a niveles

### Estructura de precios
- [ ] Número de niveles elegido
- [ ] Niveles diferenciados claramente
- [ ] Puntos de precio establecidos basados en investigación
- [ ] Estrategia de descuento anual creada
- [ ] Nivel empresarial/personalizado planificado

---

## Preguntas específicas de la tarea

1. ¿Qué investigación de precios ha realizado?
2. ¿Cuál es su ARPU y tasa de conversión actual?
3. ¿Cuál es su métrica de valor principal?
4. ¿Quiénes son sus principales personas de precios?
5. ¿Es autoservicio, dirigido por ventas o híbrido?
6. ¿Qué cambios de precios está considerando?

---

## Habilidades relacionadas

- **page-cro**: Para optimizar la conversión de la página de precios
- **copywriting**: Para el texto de la página de precios
- **marketing-psychology**: Para principios de psicología de precios
- **ab-test-setup**: Para probar cambios de precios
