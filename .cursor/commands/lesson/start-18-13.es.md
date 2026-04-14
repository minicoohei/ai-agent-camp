---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-12"]
level: "intermediate"
tags: ["pm", "ui", "prototype", "html", "tailwind"]
---

# 🎓 Lesson 18-13: Prototipo HTML + Tailwind CSS

| Elemento | Detalles |
|------|------|
| Objetivo | Implementar los diseños Pencil de TaskFlow en HTML + Tailwind CSS y crear un prototipo funcional |
| Duración | ~30 min |
| Habilidades utilizadas | - |
| Requisitos previos | Lesson 18-12 completada, diseño Pencil existente |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

---

## 📍 Que aprenderá

En esta lección, convertirá el diseño del panel de control de PM creado en Pencil en un prototipo HTML funcional. El objetivo es implementar un diseño responsive utilizando Tailwind CSS.

**Puntos de aprendizaje:**
- Prototipado rápido con Tailwind CDN
- Estructura HTML y diseño de componentes
- Uso eficiente de frameworks CSS
- Implementación de diseño responsive

---

## 🚀 Paso 1: Inicialización del proyecto (HTML + Tailwind CDN)

### 1-1. Seleccionar método de configuración

```json
{
  "type": "AskQuestion",
  "question": "Seleccione la estructura del prototipo",
  "hint": "La version CDN se inicia rapidamente. La version de compilacion es mas cercana a produccion.",
  "options": [
    {
      "label": "HTML unico (CDN)",
      "description": "Completado solo con index.html. El mas simple.",
      "value": "single-html"
    },
    {
      "label": "Multi-pagina (CDN)",
      "description": "Multiples archivos HTML. Incluye navegacion entre paginas.",
      "value": "multi-page"
    },
    {
      "label": "Vite + Tailwind (con compilacion)",
      "description": "Con npm y proceso de compilacion. Cercano a produccion.",
      "value": "vite-build"
    },
    {
      "label": "Obtener sugerencia de estructura optima de IA",
      "description": "Recibir sugerencia adaptada a los objetivos del curso.",
      "value": "ai-suggest"
    }
  ]
}
```

### 1-2. Crear estructura del proyecto

```text
output/pm/prototype/
├── index.html          # Pantalla del panel de control
├── tasks.html          # Pantalla de gestion de tareas
├── task-detail.html    # Pantalla de detalle de tarea
├── styles.css          # Estilos personalizados (segun sea necesario)
└── app.js              # Logica JavaScript (cuando se selecciona CRUD)
```

**Comando de ejecución:**
```bash
mkdir -p output/pm/prototype
```

### 1-3. Estructura básica de index.html

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskFlow - PM Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* Custom styles */
  </style>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <h1 class="text-2xl font-bold text-gray-900">TaskFlow</h1>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Dashboard sections will be added here -->
  </main>

  <script src="app.js"></script>
</body>
</html>
```

---

## 📍 Paso 2: Implementación de la pantalla del panel

### 2-1. Seleccionar enfoque de implementación

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el enfoque de implementacion",
  "hint": "La eficiencia depende de cuanto consulte el diseno de Pencil.",
  "options": [
    {
      "label": "Conversion automatica desde diseno Pencil",
      "description": "La IA lee el diseno y lo convierte (usando herramientas)",
      "value": "auto-convert"
    },
    {
      "label": "Implementacion manual seccion por seccion",
      "description": "Codificar a mano consultando las especificaciones de diseno. Alto efecto de aprendizaje.",
      "value": "manual-section"
    },
    {
      "label": "Que la IA genere todo de una vez",
      "description": "Cargar archivo Pencil y generar codigo",
      "value": "ai-generate"
    }
  ]
}
```

### 2-2. Componentes del panel de control

**Elementos obligatorios:**
- Encabezado (información de usuario, navegación)
- Barra lateral (menu)
- Tarjetas de estadísticas (cantidad de tareas, tasa de finalización, etc.)
- Lista de tareas (tareas de hoy)
- Lista de proyectos
- Feed de actividad

### 2-3. Muestras de implementación (por sección)

**Implementación del encabezado:**
```html
<header class="bg-white shadow sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
    <div class="flex items-center">
      <h1 class="text-2xl font-bold text-blue-600">TaskFlow</h1>
    </div>
    <div class="flex items-center gap-4">
      <button class="p-2 hover:bg-gray-100 rounded-lg">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
        </svg>
      </button>
      <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold">
        PM
      </div>
    </div>
  </div>
</header>
```

**Implementación de tarjetas de estadísticas:**
```html
<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
  <!-- Total Tasks Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">Total de tareas</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">24</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
      </div>
    </div>
  </div>

  <!-- Completed Tasks Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">Tareas completadas</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">16</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
    </div>
  </div>

  <!-- In Progress Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">En progreso</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">5</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-yellow-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
      </div>
    </div>
  </div>

  <!-- Completion Rate Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">Tasa de finalizacion</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">67%</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
      </div>
    </div>
  </div>
</div>
```

**Implementación de lista de tareas:**
```html
<div class="bg-white rounded-lg shadow overflow-hidden">
  <div class="px-6 py-4 border-b border-gray-200">
    <h2 class="text-lg font-semibold text-gray-900">Tareas de hoy</h2>
  </div>
  <div class="divide-y divide-gray-200">
    <!-- Task Item -->
    <div class="px-6 py-4 hover:bg-gray-50 transition cursor-pointer flex items-center gap-4">
      <input type="checkbox" class="w-5 h-5 text-blue-600 rounded cursor-pointer">
      <div class="flex-1">
        <p class="font-medium text-gray-900">Implementar autenticacion de usuario</p>
        <p class="text-sm text-gray-600 mt-1">Backend Team</p>
      </div>
      <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">Alta prioridad</span>
      <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full">En progreso</span>
    </div>

    <!-- More task items -->
    <div class="px-6 py-4 hover:bg-gray-50 transition cursor-pointer flex items-center gap-4">
      <input type="checkbox" class="w-5 h-5 text-blue-600 rounded cursor-pointer">
      <div class="flex-1">
        <p class="font-medium text-gray-900">Revision de diseno de base de datos</p>
        <p class="text-sm text-gray-600 mt-1">Database Team</p>
      </div>
      <span class="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">Prioridad media</span>
      <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-full">Sin iniciar</span>
    </div>
  </div>
</div>
```

---

## 📍 Paso 3: Implementación de pantallas CRUD de tareas

### 3-1. Seleccionar nivel de funcionalidad

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el nivel de funcionalidad de la pantalla de tareas",
  "hint": "Sin JavaScript (estatico) es el mas simple. LocalStorage permite guardar.",
  "options": [
    {
      "label": "Solo visualizacion (HTML estatico)",
      "description": "Solo visualizacion HTML y CSS. Sin interaccion.",
      "value": "static-only"
    },
    {
      "label": "Interaccion simple (con JS)",
      "description": "Visualizacion modal, entrada de formulario, etc. Solo en memoria.",
      "value": "js-interaction"
    },
    {
      "label": "CRUD completo (usando LocalStorage)",
      "description": "Toda la funcionalidad Crear/Leer/Actualizar/Eliminar. Guardado en el navegador.",
      "value": "localstorage-crud"
    }
  ]
}
```

### 3-2. tasks.html - Página de lista de tareas

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskFlow - Tasks</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
      <a href="index.html" class="text-2xl font-bold text-blue-600">TaskFlow</a>
      <a href="index.html" class="text-gray-600 hover:text-gray-900">← Volver al panel de control</a>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Title and Action -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Gestion de tareas</h1>
      <button id="newTaskBtn" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        + Nueva tarea
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="flex gap-2 mb-6 border-b border-gray-200">
      <button class="px-4 py-2 text-gray-900 font-medium border-b-2 border-blue-600">Todos</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">En progreso</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">Completado</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">Vencido</button>
    </div>

    <!-- Task Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Nombre de tarea</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Equipo</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Prioridad</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Estado</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Fecha limite</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <!-- Task rows will be generated here -->
          <tr class="hover:bg-gray-50 transition">
            <td class="px-6 py-4"><a href="task-detail.html" class="text-blue-600 hover:underline font-medium">Implementacion autenticacion</a></td>
            <td class="px-6 py-4 text-gray-900">Backend</td>
            <td class="px-6 py-4"><span class="px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full">Alta</span></td>
            <td class="px-6 py-4"><span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full">En progreso</span></td>
            <td class="px-6 py-4 text-gray-900">2024-01-25</td>
            <td class="px-6 py-4 text-right">
              <button class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
              <button class="text-red-600 hover:text-red-900">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>

  <!-- New Task Modal -->
  <div id="taskModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6">
      <h2 class="text-xl font-bold mb-4">Nueva tarea</h2>
      <form>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de tarea</label>
          <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Descripcion</label>
          <textarea class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" rows="3"></textarea>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Prioridad</label>
          <select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option>Baja</option>
            <option>Media</option>
            <option selected>Alta</option>
          </select>
        </div>
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Fecha limite</label>
          <input type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div class="flex gap-3">
          <button type="button" id="closeModalBtn" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
          <button type="submit" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Crear</button>
        </div>
      </form>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
```

### 3-3. task-detail.html - Página de detalle de tarea

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskFlow - Task Detail</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
      <a href="index.html" class="text-2xl font-bold text-blue-600">TaskFlow</a>
      <a href="tasks.html" class="text-gray-600 hover:text-gray-900">← Volver a la lista de tareas</a>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-3 gap-8">
      <!-- Main Content -->
      <div class="col-span-2">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Implementar autenticacion de usuario</h1>
              <p class="text-gray-600 mt-2">ID de tarea: #2401</p>
            </div>
            <button class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Editar</button>
          </div>

          <!-- Description -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-2">Descripcion</h2>
            <p class="text-gray-700">Implementar la autenticacion de usuario. Debe usar OAuth2.0 y soportar inicio de sesion con cuentas de Google, GitHub y Microsoft.</p>
          </div>

          <!-- Details Grid -->
          <div class="grid grid-cols-2 gap-6 mb-6">
            <div>
              <p class="text-sm font-medium text-gray-600">Equipo</p>
              <p class="text-gray-900 mt-1">Backend</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">Responsable</p>
              <p class="text-gray-900 mt-1">Taro Yamada</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">Prioridad</p>
              <span class="inline-block px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full mt-1">Alta</span>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">Estado</p>
              <span class="inline-block px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full mt-1">En progreso</span>
            </div>
          </div>

          <!-- Checklist -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Lista de verificacion</h2>
            <div class="space-y-2">
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-green-600 rounded">
                <span class="ml-3 text-gray-700">Investigacion y diseno de OAuth2.0</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-green-600 rounded">
                <span class="ml-3 text-gray-700">Seleccion de biblioteca de autenticacion</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-blue-600 rounded">
                <span class="ml-3 text-gray-700">Implementacion y pruebas</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-blue-600 rounded">
                <span class="ml-3 text-gray-700">Despliegue a produccion</span>
              </label>
            </div>
          </div>

          <!-- Comments Section -->
          <div>
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Comentarios</h2>
            <div class="space-y-4">
              <div class="border-t pt-4">
                <p class="font-medium text-gray-900">Taro Yamada</p>
                <p class="text-sm text-gray-600">2024-01-20</p>
                <p class="text-gray-700 mt-2">La autenticacion de Google esta completa. A continuacion, trabajando en la autenticacion de GitHub.</p>
              </div>
            </div>
            <div class="mt-4">
              <input type="text" placeholder="Ingrese un comentario..." class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div>
        <div class="bg-white rounded-lg shadow p-6 sticky top-20">
          <h3 class="font-semibold text-gray-900 mb-4">Informacion del proyecto</h3>
          <div class="space-y-4">
            <div>
              <p class="text-sm text-gray-600">Fecha de inicio</p>
              <p class="text-gray-900 font-medium">2024-01-15</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Fecha limite</p>
              <p class="text-gray-900 font-medium">2024-01-25</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Progreso</p>
              <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div class="bg-blue-600 h-2 rounded-full" style="width: 60%"></div>
              </div>
              <p class="text-sm text-gray-600 mt-1">60% Completado</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</body>
</html>
```

---

## 📍 Paso 4: Diseño responsivo y verificación de funcionamiento

### 4-1. Seleccionar método de verificación

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el metodo de verificacion",
  "hint": "La verificacion manual da experiencia real. Las listas de verificacion aseguran que nada se pase por alto.",
  "options": [
    {
      "label": "Verificacion manual en el navegador",
      "description": "Abrir en multiples dispositivos para verificar la apariencia.",
      "value": "manual-browser"
    },
    {
      "label": "Verificar con lista de verificacion responsiva",
      "description": "Verificar siguiendo los elementos de la lista de verificacion proporcionada.",
      "value": "checklist-verification"
    },
    {
      "label": "Obtener revision de codigo de IA",
      "description": "La IA inspecciona HTML y CSS y sugiere mejoras.",
      "value": "ai-review"
    }
  ]
}
```

### 4-2. Lista de verificación responsive

**Pantalla móvil (320px-480px)**
- [ ] La navegación del encabezado esta colapsada
- [ ] Las tarjetas de tareas estan apiladas en una sola columna
- [ ] Los botones son grandes y faciles de tocar (48px x 48px o más)
- [ ] El texto tiene un tamaño legible (16px o más)
- [ ] No se produce desplazamiento horizontal

**Pantalla de tableta (768px-1024px)**
- [ ] Las tarjetas de estadísticas se muestran en 2-3 columnas
- [ ] La barra lateral y el contenido principal se muestran lado a lado
- [ ] Las tablas se muestran en un formato fácil de leer

**Pantalla de escritorio (1024px y superior)**
- [ ] El diseño esta limitado al ancho máximo (max-w-7xl)
- [ ] Las tarjetas de estadísticas se muestran en 4 columnas
- [ ] Los efectos hover funcionan correctamente
- [ ] Todas las funciones se muestran como se esperaba

### 4-3. Clases responsive de Tailwind CSS

```html
<!-- Ejemplo: Usar diferentes cuadriculas para diferentes tamanos de pantalla -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <!-- Movil: 1 col, Tableta: 2 cols, Escritorio: 4 cols -->
</div>
```

**Principales puntos de quiebre de Tailwind:**
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

---

## ⚠️ Solución de problemas

### El CDN de Tailwind no se carga
- Verificar la pestana "Network" en las herramientas de desarrollo del navegador (F12)
- Verificar que el estado del CDN este en el rango 200
- Limpiar cache y recargar (Ctrl+Shift+Delete)

### El diseño se rompe
- Verificar si la clase `max-w-` esta aplicada al elemento padre
- Verificar configuración de padding/margin (`px-`, `py-`, etc.)
- Verificar la profundidad de anidamiento (no excesivamente anidado)

### Diferencias con el diseño de Pencil
- Comparar el archivo de Pencil y la implementación lado a lado
- Verificar que los códigos de color (valores HEX) sean precisos
- Verificar que los tamaños de fuente coincidan (definiciones de tamaño de Tailwind)
- Verificar que la ubicación de elementos (flexbox/grid) coincida con el diseño

### JavaScript no funciona
- Verificar si `app.js` se cargo correctamente (verificar con F12)
- Verificar errores en la consola del navegador (F12 → Console)
- Verificar que los event listeners esten registrados correctamente

---

## ✅ Punto de control

Elementos de verificación de finalización del prototipo:

```json
{
  "type": "AskQuestion",
  "question": "Ha completado todo?",
  "hint": "Verifique todos los elementos a continuacion antes de continuar.",
  "checkpoints": [
    {
      "item": "prototype/index.html existe",
      "checked": false
    },
    {
      "item": "La pantalla del panel de control se muestra",
      "checked": false
    },
    {
      "item": "La pantalla de lista de tareas se muestra",
      "checked": false
    },
    {
      "item": "La pantalla de detalle de tarea se muestra",
      "checked": false
    },
    {
      "item": "Diseno responsivo aplicado (verificado en movil/tableta/escritorio)",
      "checked": false
    },
    {
      "item": "Verificado en el navegador (sin errores)",
      "checked": false
    },
    {
      "item": "La apariencia coincide con el diseno de Pencil",
      "checked": false
    },
    {
      "item": "Las interacciones JavaScript (si se seleccionaron) estan funcionando",
      "checked": false
    }
  ]
}
```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/integration-test-evidence/
└──   (Evidencia de pruebas de integracion)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/integration-test-evidence/

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/integration-test-evidence/
```

> 💡 Texto completo: Ejecute `cat output/pm/integration-test-evidence/` para mostrar el texto completo

---

## ➡️ Siguientes pasos

✅ Después de completar esta lección, proceda a:

**[Lesson 18-14: Pruebas E2E con Playwright](./start-18-14.md)**
- Implementar pruebas automatizadas para el prototipo
- Probar funciones clave como navegación de páginas, entrada de formularios y clics en botones
- Fundamentos de integración CI/CD

---

## 📚 Referencias

- [Documentación oficial de Tailwind CSS](https://tailwindcss.com/docs)
- [MDN - Elementos semánticos HTML](https://developer.mozilla.org/es/docs/Glossary/Semantics)
- [Flexbox & Grid - CSS-Tricks](https://css-tricks.com/)
- [Introducción a la accesibilidad - WAI](https://www.w3.org/WAI/fundamentals/accessibility-intro/)

---

**Created with Claude Code - PM Training Course**
