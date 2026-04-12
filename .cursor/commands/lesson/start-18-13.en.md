---
description: "When the user says /start-18-13 — Module 18 Lesson 18-13: PM - HTML + Tailwind CSS Prototype Implementation"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-12"]
level: "intermediate"
tags: ["pm", "ui", "prototype", "html", "tailwind"]
---

# 🎓 Lesson 18-13: HTML + Tailwind CSS Prototype

| Item | Details |
|------|------|
| Goal | Implement TaskFlow's Pencil designs in HTML + Tailwind CSS and create a working prototype |
| Duration | ~30 min |
| Skills Used | - |
| Prerequisites | Lesson 18-12 completed, Pencil design exists |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

---

## 📍 What You'll Learn

In this lesson, you will convert the PM dashboard design created in Pencil into a working HTML prototype. The goal is to implement a responsive design using Tailwind CSS.

**Learning Points:**
- Rapid prototyping with Tailwind CDN
- HTML structure and component design
- Efficient use of CSS frameworks
- Responsive design implementation

---

## 🚀 Step 1: Project Initialization (HTML + Tailwind CDN)

### 1-1. Select Configuration Method

```json
{
  "type": "AskQuestion",
  "question": "Select the prototype structure",
  "hint": "CDN version starts quickly. Build version is closer to production.",
  "options": [
    {
      "label": "Single HTML (CDN)",
      "description": "Completed with just index.html. Simplest.",
      "value": "single-html"
    },
    {
      "label": "Multi-page (CDN)",
      "description": "Multiple HTML files. Includes page navigation.",
      "value": "multi-page"
    },
    {
      "label": "Vite + Tailwind (with build)",
      "description": "With npm and build process. Close to production.",
      "value": "vite-build"
    },
    {
      "label": "Get AI to suggest optimal structure",
      "description": "Receive suggestion tailored to course objectives.",
      "value": "ai-suggest"
    }
  ]
}
```

### 1-2. Create Project Structure

```text
output/pm/prototype/
├── index.html          # Dashboard screen
├── tasks.html          # Task management screen
├── task-detail.html    # Task detail screen
├── styles.css          # Custom styles (as needed)
└── app.js              # JavaScript logic (when CRUD selected)
```

**Execution Command:**
```bash
mkdir -p output/pm/prototype
```

### 1-3. Basic Structure of index.html

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

## 📍 Step 2: Implementing the Dashboard Screen

### 2-1. Select Implementation Approach

```json
{
  "type": "AskQuestion",
  "question": "Select the implementation approach",
  "hint": "Efficiency depends on how much you reference the Pencil design.",
  "options": [
    {
      "label": "Auto-convert from Pencil design",
      "description": "AI reads design and converts (using tools)",
      "value": "auto-convert"
    },
    {
      "label": "Manual implementation section by section",
      "description": "Code by hand while referencing design specs. High learning effect.",
      "value": "manual-section"
    },
    {
      "label": "Have AI generate all at once",
      "description": "Upload Pencil file and generate code",
      "value": "ai-generate"
    }
  ]
}
```

### 2-2. Dashboard Components

**Required Elements:**
- Header (user info, navigation)
- Sidebar (menu)
- Statistics cards (task count, completion rate, etc.)
- Task list (today's tasks)
- Project list
- Activity feed

### 2-3. Implementation Samples (Per Section)

**Header Implementation:**
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

**Statistics Card Implementation:**
```html
<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
  <!-- Total Tasks Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">Total Tasks</p>
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
        <p class="text-gray-600 text-sm font-medium">Completed Tasks</p>
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
        <p class="text-gray-600 text-sm font-medium">In Progress</p>
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
        <p class="text-gray-600 text-sm font-medium">Completion Rate</p>
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

**Task List Implementation:**
```html
<div class="bg-white rounded-lg shadow overflow-hidden">
  <div class="px-6 py-4 border-b border-gray-200">
    <h2 class="text-lg font-semibold text-gray-900">Today's Tasks</h2>
  </div>
  <div class="divide-y divide-gray-200">
    <!-- Task Item -->
    <div class="px-6 py-4 hover:bg-gray-50 transition cursor-pointer flex items-center gap-4">
      <input type="checkbox" class="w-5 h-5 text-blue-600 rounded cursor-pointer">
      <div class="flex-1">
        <p class="font-medium text-gray-900">Implement User Authentication</p>
        <p class="text-sm text-gray-600 mt-1">Backend Team</p>
      </div>
      <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">High Priority</span>
      <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full">In Progress</span>
    </div>

    <!-- More task items -->
    <div class="px-6 py-4 hover:bg-gray-50 transition cursor-pointer flex items-center gap-4">
      <input type="checkbox" class="w-5 h-5 text-blue-600 rounded cursor-pointer">
      <div class="flex-1">
        <p class="font-medium text-gray-900">Database Design Review</p>
        <p class="text-sm text-gray-600 mt-1">Database Team</p>
      </div>
      <span class="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">Medium Priority</span>
      <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-full">Not Started</span>
    </div>
  </div>
</div>
```

---

## 📍 Step 3: Implementing Task CRUD Screens

### 3-1. Select Feature Level

```json
{
  "type": "AskQuestion",
  "question": "Select the task screen functionality level",
  "hint": "No JavaScript (static) is simplest. LocalStorage allows saving.",
  "options": [
    {
      "label": "Display only (static HTML)",
      "description": "HTML display and CSS only. No interaction.",
      "value": "static-only"
    },
    {
      "label": "Simple interaction (with JS)",
      "description": "Modal display, form input, etc. In-memory only.",
      "value": "js-interaction"
    },
    {
      "label": "Full CRUD (using LocalStorage)",
      "description": "All Create/Read/Update/Delete functionality. Saved in browser.",
      "value": "localstorage-crud"
    }
  ]
}
```

### 3-2. tasks.html - Task List Page

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
      <a href="index.html" class="text-gray-600 hover:text-gray-900">← Back to Dashboard</a>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Title and Action -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Task Management</h1>
      <button id="newTaskBtn" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        + New Task
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="flex gap-2 mb-6 border-b border-gray-200">
      <button class="px-4 py-2 text-gray-900 font-medium border-b-2 border-blue-600">All</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">In Progress</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">Completed</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">Overdue</button>
    </div>

    <!-- Task Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Task Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Team</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Priority</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Due Date</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <!-- Task rows will be generated here -->
          <tr class="hover:bg-gray-50 transition">
            <td class="px-6 py-4"><a href="task-detail.html" class="text-blue-600 hover:underline font-medium">User Auth Implementation</a></td>
            <td class="px-6 py-4 text-gray-900">Backend</td>
            <td class="px-6 py-4"><span class="px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full">High</span></td>
            <td class="px-6 py-4"><span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full">In Progress</span></td>
            <td class="px-6 py-4 text-gray-900">2024-01-25</td>
            <td class="px-6 py-4 text-right">
              <button class="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
              <button class="text-red-600 hover:text-red-900">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>

  <!-- New Task Modal -->
  <div id="taskModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6">
      <h2 class="text-xl font-bold mb-4">New Task</h2>
      <form>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Task Name</label>
          <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" rows="3"></textarea>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option>Low</option>
            <option>Medium</option>
            <option selected>High</option>
          </select>
        </div>
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
          <input type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div class="flex gap-3">
          <button type="button" id="closeModalBtn" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</button>
          <button type="submit" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Create</button>
        </div>
      </form>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
```

### 3-3. task-detail.html - Task Detail Page

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
      <a href="tasks.html" class="text-gray-600 hover:text-gray-900">← Back to Task List</a>
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
              <h1 class="text-3xl font-bold text-gray-900">Implement User Authentication</h1>
              <p class="text-gray-600 mt-2">Task ID: #2401</p>
            </div>
            <button class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Edit</button>
          </div>

          <!-- Description -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-2">Description</h2>
            <p class="text-gray-700">Implement user authentication. Must use OAuth2.0 and support login with Google, GitHub, and Microsoft accounts.</p>
          </div>

          <!-- Details Grid -->
          <div class="grid grid-cols-2 gap-6 mb-6">
            <div>
              <p class="text-sm font-medium text-gray-600">Team</p>
              <p class="text-gray-900 mt-1">Backend</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">Assignee</p>
              <p class="text-gray-900 mt-1">Taro Yamada</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">Priority</p>
              <span class="inline-block px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full mt-1">High</span>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">Status</p>
              <span class="inline-block px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full mt-1">In Progress</span>
            </div>
          </div>

          <!-- Checklist -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Checklist</h2>
            <div class="space-y-2">
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-green-600 rounded">
                <span class="ml-3 text-gray-700">OAuth2.0 Research and Design</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-green-600 rounded">
                <span class="ml-3 text-gray-700">Authentication Library Selection</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-blue-600 rounded">
                <span class="ml-3 text-gray-700">Implementation and Testing</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-blue-600 rounded">
                <span class="ml-3 text-gray-700">Deploy to Production</span>
              </label>
            </div>
          </div>

          <!-- Comments Section -->
          <div>
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Comments</h2>
            <div class="space-y-4">
              <div class="border-t pt-4">
                <p class="font-medium text-gray-900">Taro Yamada</p>
                <p class="text-sm text-gray-600">2024-01-20</p>
                <p class="text-gray-700 mt-2">Google auth is complete. Next, working on GitHub auth.</p>
              </div>
            </div>
            <div class="mt-4">
              <input type="text" placeholder="Enter a comment..." class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div>
        <div class="bg-white rounded-lg shadow p-6 sticky top-20">
          <h3 class="font-semibold text-gray-900 mb-4">Project Information</h3>
          <div class="space-y-4">
            <div>
              <p class="text-sm text-gray-600">Start Date</p>
              <p class="text-gray-900 font-medium">2024-01-15</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Due Date</p>
              <p class="text-gray-900 font-medium">2024-01-25</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Progress</p>
              <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div class="bg-blue-600 h-2 rounded-full" style="width: 60%"></div>
              </div>
              <p class="text-sm text-gray-600 mt-1">60% Complete</p>
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

## 📍 Step 4: Responsive Design and Operation Check

### 4-1. Select Verification Method

```json
{
  "type": "AskQuestion",
  "question": "Select the verification method",
  "hint": "Manual verification gives real experience. Checklists ensure nothing is missed.",
  "options": [
    {
      "label": "Manual verification in browser",
      "description": "Open on multiple devices to check appearance.",
      "value": "manual-browser"
    },
    {
      "label": "Verify with responsive checklist",
      "description": "Verify along provided checklist items.",
      "value": "checklist-verification"
    },
    {
      "label": "Get AI code review",
      "description": "AI inspects HTML and CSS and suggests improvements.",
      "value": "ai-review"
    }
  ]
}
```

### 4-2. Responsive Verification Checklist

**Mobile Display (320px-480px)**
- [ ] Header navigation is collapsed
- [ ] Task cards are stacked in a single column
- [ ] Buttons are large and easy to tap (48px x 48px or larger)
- [ ] Text is a readable size (16px or larger)
- [ ] No horizontal scrolling occurs

**Tablet Display (768px-1024px)**
- [ ] Statistics cards are displayed in 2-3 columns
- [ ] Sidebar and main content are displayed side by side
- [ ] Tables are displayed in an easy-to-read format

**Desktop Display (1024px and above)**
- [ ] Layout is constrained to max width (max-w-7xl)
- [ ] Statistics cards are displayed in 4 columns
- [ ] Hover effects are working correctly
- [ ] All features are displayed as expected

### 4-3. Tailwind CSS Responsive Classes

```html
<!-- Example: Use different grids for different screen sizes -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <!-- Mobile: 1 col, Tablet: 2 cols, Desktop: 4 cols -->
</div>
```

**Main Tailwind Breakpoints:**
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

---

## ⚠️ Troubleshooting

### Tailwind CDN Does Not Load
- Check the "Network" tab in browser developer tools (F12)
- Verify CDN status is in the 200 range
- Clear cache and reload (Ctrl+Shift+Delete)

### Layout Is Broken
- Check if `max-w-` class is applied to the parent element
- Check padding/margin settings (`px-`, `py-`, etc.)
- Check nesting depth (not overly nested)

### Differences from Pencil Design
- Compare Pencil file and implementation side by side
- Verify color codes (HEX values) are accurate
- Verify font sizes match (Tailwind size definitions)
- Verify element placement (flexbox/grid) matches design

### JavaScript Does Not Work
- Check if `app.js` is loaded correctly (verify with F12)
- Check for errors in browser console (F12 → Console)
- Verify event listeners are registered correctly

---

## ✅ Checkpoint

Prototype completion verification items:

```json
{
  "type": "AskQuestion",
  "question": "Have you completed everything?",
  "hint": "Please check all items below before proceeding.",
  "checkpoints": [
    {
      "item": "prototype/index.html exists",
      "checked": false
    },
    {
      "item": "Dashboard screen is displayed",
      "checked": false
    },
    {
      "item": "Task list screen is displayed",
      "checked": false
    },
    {
      "item": "Task detail screen is displayed",
      "checked": false
    },
    {
      "item": "Responsive design applied (verified on mobile/tablet/desktop)",
      "checked": false
    },
    {
      "item": "Verified in browser (no errors)",
      "checked": false
    },
    {
      "item": "Appearance matches Pencil design",
      "checked": false
    },
    {
      "item": "JavaScript interactions (if selected) are working",
      "checked": false
    }
  ]
}
```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/integration-test-evidence/
└──   (Integration Test Evidence)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/integration-test-evidence/

# Check the beginning (first 30 lines)
head -30 output/pm/integration-test-evidence/
```

> 💡 Full text: Run `cat output/pm/integration-test-evidence/` to display the full text

---

## ➡️ Next Steps

✅ After completing this lesson, proceed to:

**[Lesson 18-14: Playwright E2E Testing](./start-18-14.md)**
- Implement automated testing for the prototype
- Test key features such as page navigation, form input, and button clicks
- Basics of CI/CD integration

---

## 📚 References

- [Tailwind CSS Official Documentation](https://tailwindcss.com/docs)
- [MDN - HTML Semantic Elements](https://developer.mozilla.org/en-US/docs/Glossary/Semantics)
- [Flexbox & Grid - CSS-Tricks](https://css-tricks.com/)
- [Introduction to Accessibility - WAI](https://www.w3.org/WAI/fundamentals/accessibility-intro/)

---

**Created with Claude Code - PM Training Course**
