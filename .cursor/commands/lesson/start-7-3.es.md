---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-2"]
duration: "~25 min"
level: "intermediate"
tags: ["agent", "testing", "iteration"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 7-3: Pruebas e iteración

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-3: Pruebas e iteración**!

| Elemento | Contenido |
|------|------|
| Objetivo | Verificar el skill de actas de reunion con 3 tipos de pruebas y ejecutar un ciclo de mejora |
| Duración | ~25 min |
| Habilidades utilizadas | meeting-notes-summarizer (creado en Lesson 7-2) |
| Requisitos previos | Lesson 7-2 completada (SKILL.md creado) |

**Flujo de la sesion:**
1. Ejecutar pruebas de activación
2. Pruebas funcionales (3 tipos de datos de ejemplo)
3. Comparación de rendimiento (con/sin skill)
4. Diagnosticar 5 patrones típicos de problemas
5. Practicar el ciclo de mejora

Al final de está sesion, podrá evaluar objetivamente la calidad del skill y ejecutar ciclos de mejora.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificación de preparación

Primero verifiquemos que todo esté listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Está listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar URL de la página del curso https://ai-agent.camp/es/course/module-7)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Ejecutar pruebas de activación

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Ejecutar pruebas de activacion",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**
Entrada:
```
Pruebe la precision de activacion del skill meeting-notes-summarizer.
Ingrese cada frase una por una y verifique si el skill se activa correctamente.

[Frases que DEBEN activar (5)]

1. "Resume las actas de la reunion"
2. "Organiza las notas de la reunion"
3. "Extrae los elementos de accion"
4. "Estructura las notas de la reunion"
5. "Resume los puntos clave de esta reunion"

→ Esperado: El skill meeting-notes-summarizer debe activarse para todas las frases

[Frases que NO deben activar (3)]

1. "Resume el correo electronico"
2. "Busca mensajes de Slack"
3. "Crea un informe"

→ Esperado: El skill no debe activarse para estas frases

[Como registrar los resultados]
Registre los resultados en el siguiente formato:

| Frase | Esperado | Real | Resultado |
|-------|----------|------|-----------|
| Resume las actas de la reunion | Se activa | ? | OK/NG |
| Organiza las notas de la reunion | Se activa | ? | OK/NG |
| Extrae los elementos de accion | Se activa | ? | OK/NG |
| Estructura las notas de la reunion | Se activa | ? | OK/NG |
| Resume los puntos clave | Se activa | ? | OK/NG |
| Resume el correo electronico | No se activa | ? | OK/NG |
| Busca mensajes de Slack | No se activa | ? | OK/NG |
| Crea un informe | No se activa | ? | OK/NG |

Verifique cuantos de 8 funcionaron correctamente.
Criterio de aprobacion: 8/8 (todos correctos)
```

**Resultado esperado**: Todas las activaciones correctas activan el skill, y las incorrectas no lo activan.

---

## 🚀 Step 2: Pruebas funcionales (3 tipos de datos de ejemplo)

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Pruebas funcionales (3 tipos de datos de ejemplo)",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**
Entrada:
```
Pruebe el skill meeting-notes-summarizer con 3 tipos de datos de ejemplo.
Ingrese cada ejemplo y verifique la calidad de la salida.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Ejemplo 1: Reunion corta (3 personas, 5 min)]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resume las siguientes actas de reunion:

Asistentes: Tanaka, Sato, Suzuki
Fecha: 10 de febrero de 2026, 10:00
Agenda: Confirmar el calendario de lanzamiento de la proxima semana
Tanaka: El lanzamiento el 2/17 esta bien?
Sato: Las pruebas se completaran para el 2/14.
Suzuki: Actualizare la documentacion el 2/15.
Conclusion: Lanzamiento confirmado para el 2/17. Sato se encarga de las pruebas, Suzuki de la documentacion.

→ Puntos de verificacion:
  - Se extrajeron correctamente los asistentes?
  - Se reconocio correctamente la fecha/hora?
  - Se extrajeron 2 elementos de accion? (Sato: completar pruebas, Suzuki: actualizar documentacion)
  - Se establecieron correctamente las fechas limite? (2/14, 2/15)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Ejemplo 2: Reunion regular (5 personas, 30 min)]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resume las siguientes actas de reunion:

Asistentes: Yamada (PM), Takahashi (Dev), Ito (Diseno), Watanabe (QA), Kobayashi (Ventas)
Fecha: 10 de febrero de 2026, 14:00-14:30
Ubicacion: Sala de reuniones A / Zoom hibrido

[Agenda 1: Revision de ventas Q1]
Kobayashi: Las ventas de Q1 se espera que cierren al 120% del objetivo. Los contratos del plan empresarial fueron particularmente buenos.
Yamada: Excelentes resultados. Cual deberia ser el objetivo de Q2?
Kobayashi: Propongo 130% interanual. Podemos esperar el efecto de los lanzamientos de nuevas funciones.
Yamada: Entendido. Procedamos con el objetivo de Q2 al 130%.

[Agenda 2: Informe de progreso de nuevas funciones]
Takahashi: La funcion de dashboard puede lanzarse segun lo programado para el 2/28. Hubo un retraso de 1 dia en la parte de integracion de API, pero lo recuperamos.
Ito: La revision de UI está completa. Se necesita una correccion para soporte movil. La correccion estara lista para el 2/12.
Watanabe: Los casos de prueba estan al 80%. El 20% restante estara listo para el 2/20. Las pruebas de regresion estan incluidas.
Yamada: Por favor priorice la correccion movil. Las pruebas pueden venir despues.

[Agenda 3: Estructura de soporte al cliente]
Watanabe: Los tickets de soporte del mes pasado aumentaron un 30% respecto al mes anterior. Muchos pueden resolverse actualizando las FAQ.
Yamada: Quien se encargara de la actualizacion de FAQ?
Watanabe: Yo me encargo. Actualizare las 10 FAQ principales para el 2/17.
Kobayashi: Compartire una lista de preguntas frecuentes del equipo de ventas. La enviare para el 2/13.

[Decisiones]
1. Objetivo de ventas Q2 es 130% interanual
2. La funcion de dashboard se lanza el 2/28
3. La correccion de UI movil tiene maxima prioridad
4. Actualizacion de FAQ por Watanabe, completada para el 2/17

[Proxima reunion]
17 de febrero de 2026, 14:00, misma ubicacion

→ Puntos de verificacion:
  - Se reconocieron correctamente los 5 asistentes y sus roles?
  - Se estructuraron los 3 puntos de agenda?
  - Se extrajeron las 4 decisiones?
  - Se extrajeron los elementos de accion con responsables y fechas limite?
    - Ito: Correccion de UI movil (para el 2/12)
    - Watanabe: Completar casos de prueba (para el 2/20)
    - Watanabe: Actualizacion de FAQ (para el 2/17)
    - Kobayashi: Compartir lista de preguntas frecuentes (para el 2/13)
  - Se registro la proxima reunion?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Ejemplo 3: Taller con idiomas mixtos]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resume las siguientes actas de reunion:

Asistentes: Nakamura (Tech Lead), Matsumoto (Backend), Kimura (Frontend), Garcia (DevOps)
Fecha: 10 de febrero de 2026, 16:00-16:45
Formato: Taller tecnico

Nakamura: Hoy discutiremos la mejora del pipeline de CI/CD. El build time actual es demasiado largo, asi que propongamos mejoras.
Garcia: El average build time actual es de unos 12 minutos. Queremos un objetivo de menos de 5 minutos. Introducir Docker layer caching deberia reducirlo significativamente.
Matsumoto: Los unit tests de Backend representan el 60% del tiempo total. La ejecucion en paralelo deberia reducirlo a la mitad.
Kimura: En el lado de Frontend, migrar de webpack a Vite puede reducir el build time de 3 minutos a 30 segundos. El PoC ya está completado.
Nakamura: Excelente. Establezcamos prioridades.
Garcia: Mi propuesta: Fase 1 para Docker layer caching, Fase 2 para ejecucion de pruebas en paralelo, Fase 3 para migracion a Vite. Que les parece ese orden?
Nakamura: De acuerdo. Cual es el esfuerzo estimado para cada fase?
Garcia: La Fase 1 son 2 dias, yo me encargo. Puede estar lista para el 2/14.
Matsumoto: La Fase 2 toma 3 dias. Se necesita configurar pytest-xdist y cambios en la configuracion de CI. Lista para el 2/19.
Kimura: Por favor permita 1 semana para la Fase 3. Hay que manejar breaking changes. Enviare el PR para el 2/24.
Nakamura: Entendido. Revisemos el progreso en checkpoints semanales. El KPI es una reduccion del 50% en el build time.

[Decisiones]
1. Mejora del pipeline de CI/CD en 3 fases
2. KPI: Reduccion del 50% en build time (12 min → menos de 6 min)
3. Checkpoint semanal para revision de progreso

→ Puntos de verificacion:
  - Se manejan correctamente los terminos tecnicos en ingles (CI/CD, Docker layer caching, parallel execution, etc.)?
  - Se estructuraron las 3 fases?
  - Se extrajeron los elementos de accion con responsables y fechas limite?
    - Garcia: Introducir Docker layer caching (para el 2/14)
    - Matsumoto: Introducir ejecucion de pruebas en paralelo (para el 2/19)
    - Kimura: Enviar PR de migracion a Vite (para el 2/24)
  - Se documento el KPI?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para los 3 ejemplos, verifique que las siguientes secciones de salida esten presentes:
1. Informacion basica de la reunion (fecha/hora, asistentes, ubicacion)
2. Agenda y resumen de la discusion
3. Lista de decisiones
4. Elementos de accion (con responsables y fechas limite)
5. Proxima reunion (si corresponde)
```

**Resultado esperado**: Los 3 ejemplos producen actas de reunion estructuradas con todas las secciones requeridas.

---

## 🚀 Step 3: Comparación de rendimiento (con/sin skill)

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Comparacion de rendimiento (con/sin skill)",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**
Entrada:
```
Compare la calidad de salida con y sin el skill.
Ejecute los mismos datos de actas de reunion en 2 patrones.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Datos de actas de reunion para comparacion]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(Use los mismos datos del Ejemplo 2 del Step 2)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Patron A: Ejecutar SIN skill]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Primero, desactive temporalmente el skill meeting-notes-summarizer.
Metodo: Renombre temporalmente el directorio skills/meeting-notes-summarizer/.

mv skills/meeting-notes-summarizer skills/_meeting-notes-summarizer_disabled

Luego haga una solicitud generica:
"Resume el contenido de la reunion anterior"

Guarde la salida en output/test-without-skill.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Patron B: Ejecutar CON skill]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reactive el skill.

mv skills/_meeting-notes-summarizer_disabled skills/meeting-notes-summarizer

Use los mismos datos y solicite:
"Resume las actas de la reunion anterior"

Guarde la salida en output/test-with-skill.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Criterios de comparacion]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Compare con los siguientes 5 criterios y evalue la efectividad del skill:

| Criterio | Sin skill | Con skill | Veredicto |
|----------|-----------|-----------|-----------|
| Completitud de estructura (todas las secciones presentes?) | ? | ? | Cual es mejor |
| Precision de extraccion de elementos de accion (con responsable/fecha) | ? | ? | Cual es mejor |
| Consistencia de formato (mismo formato cada vez?) | ? | ? | Cual es mejor |
| Cobertura de informacion (sin omisiones?) | ? | ? | Cual es mejor |
| Tiempo de ejecucion (percibido) | ? | ? | Cual es mas rapido |

Si "con skill" es mejor en al menos 3 de 5 criterios, el skill esta funcionando efectivamente.
```

**Resultado esperado**: La version con skill muestra superioridad en completitud de estructura, precision de extraccion de elementos de accion y consistencia de formato.

---

## 🚀 Step 4: Diagnosticar 5 patrones típicos de problemas

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Diagnosticar 5 patrones tipicos de problemas",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**
Entrada:
```
Revise 5 patrones comunes de problemas en el desarrollo de skills y diagnostique si alguno aplica a su skill.

[Patron 1: Undertriggering (activacion insuficiente)]
Sintoma: El skill no se activa cuando deberia
Causa: Frases de activacion insuficientes en la description de SKILL.md
Solucion: Agregar las frases faltantes a la description

[Patron 2: Overtriggering (activacion excesiva)]
Sintoma: El skill se activa en contextos no relacionados
Causa: La description es demasiado amplia
Solucion: Limitar la description a lenguaje especifico de reuniones

[Patron 3: Salida incompleta]
Sintoma: Faltan elementos de accion o asistentes, secciones incompletas
Causa: Instrucciones insuficientes en el cuerpo de SKILL.md
Solucion: Agregar un checklist de salida a SKILL.md

[Patron 4: Desbordamiento de contexto]
Sintoma: SKILL.md es demasiado largo y el rendimiento se degrada
Causa: El cuerpo excede 5,000 palabras
Solucion: Mover detalles a references/, mantener SKILL.md conciso

[Patron 5: Error de carga de recursos]
Sintoma: No se pueden leer archivos de scripts/ o references/
Causa: Error en la especificacion de rutas o archivo no creado
Solucion: Verificar y corregir las rutas de referencia

Registre los patrones que apliquen a su skill. Los corregira en Step 5.
```

**Resultado esperado**: Comprension de los 5 patrones de problemas e identificacion de problemas en su propio skill.

---

## 🚀 Step 5: Practicar el ciclo de mejora

Use AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Practicar el ciclo de mejora",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Guía tras la selección:**
Entrada:
```
Basandose en los resultados de los Steps 1-4, practique el ciclo de mejora.
Siga estos pasos para ejecutar al menos un ciclo de mejora.

■ Paso A: Identificar el area mas debil
■ Paso B: Modificar SKILL.md
■ Paso C: Re-ejecutar las pruebas relacionadas con la correccion
■ Paso D: Comparar resultados antes y despues

Guarde el informe de mejora en output/skill-improvement-report.md.

El ciclo de mejora es una repeticion de "Identificar → Corregir → Probar → Comparar".
Este proceso iterativo mejora continuamente la calidad del skill.
```

**Resultado esperado**: Completar al menos un ciclo de mejora y registrar la comparación de calidad de salida antes/después.

---

## ⚠️ Problemas comunes y soluciones

Use AskQuestion para seleccionar el problema y siga la guía.

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No hay datos de ejemplo para pruebas"},
      {"id": "trouble_2", "label": "No se como activar/desactivar el skill"},
      {"id": "trouble_3", "label": "La salida no cambia despues de la mejora"},
      {"id": "trouble_4", "label": "No se como registrar los resultados de las pruebas"}
    ]
  }]
}
```

### Problema 1: No hay datos de ejemplo para pruebas
**Causa**: No puede preparar datos de actas de reunion para pruebas
**Prompt de solución**:
```
El Step 2 tiene 3 tipos de datos de ejemplo preparados en linea.
Uselos tal cual:
- Ejemplo 1: Reunion corta (3 personas, 5 min)
- Ejemplo 2: Reunion regular (5 personas, 30 min)
- Ejemplo 3: Taller con idiomas mixtos
```

### Problema 2: No se cómo activar/desactivar el skill
**Causa**: No conoce cómo desactivar/activar skills
**Prompt de solución**:
```
Puede desactivar un skill renombrando la carpeta del skill dentro de skills/.

Desactivar (ocultar temporalmente renombrando):
mv skills/meeting-notes-summarizer skills/_meeting-notes-summarizer_disabled

Activar (restaurar el nombre original):
mv skills/_meeting-notes-summarizer_disabled skills/meeting-notes-summarizer

Nota: Siempre reactive despues de las pruebas.
```

### Problema 3: La salida no cambia después de la mejora
**Causa**: Los cambios en SKILL.md pueden estar en cache
**Prompt de solución**:
```
Intente los siguientes pasos:
1. Reinicie el editor (Cursor)
2. Vuelva a guardar el archivo SKILL.md (Ctrl+S / Cmd+S)
3. Pruebe nuevamente en una nueva sesion de chat
4. Si aun no cambia, verifique que los cambios de SKILL.md se guardaron correctamente:
   cat skills/meeting-notes-summarizer/SKILL.md
```

### Problema 4: No se cómo registrar los resultados de las pruebas
**Causa**: No está claro dónde ni en que formato guardar los resultados
**Prompt de solución**:
```
Guarde en formato Markdown en el directorio output/.

mkdir -p output

Ubicaciones de guardado de resultados:
- Resultados de pruebas de activacion: output/trigger-test-results.md
- Resultados de pruebas funcionales: output/functional-test-results.md
- Comparacion de rendimiento: output/performance-comparison.md
- Informe de mejora: output/skill-improvement-report.md
```

---

## ✅ Punto de control
- [ ] Verifico el comportamiento correcto de activación/no activación en las pruebas
- [ ] Ejecuto pruebas con 3 tipos de datos de ejemplo
- [ ] Comparo el rendimiento con/sin skill
- [ ] Comprendio los 5 patrones de problemas
- [ ] Ejecuto al menos 1 ciclo de mejora
- [ ] Comparo la salida antes/después


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 skills/{skill_name}/
├── SKILL.md  (definicion del skill)
├── scripts/    (scripts de ejecucion)
└── tests/      (archivos de prueba)
```

### Comandos de verificación
```bash
# Verificar la estructura del directorio del skill
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Verificar el inicio de SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat de Cursor para verificar la finalización:

```
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Determinacion de aprobado/no aprobado con los elementos faltantes listados.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar una nueva sección.

Use AskQuestion para elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-7-4)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-7-4
- finish → Finalizar
