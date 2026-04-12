---
description: "When the user says /start-18-12 — Module 18 Lesson 18-12: PM - UI Design (Pencil MCP)"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-11", "output/pm/wireframes.md"]
level: "intermediate"
tags: ["pm", "ui", "design", "pencil-mcp"]
---

# 🎓 Lesson 18-12: UI Design (Pencil MCP)

| Item | Details |
|------|------|
| Goal | Design TaskFlow's main screens (dashboard, task list, task details) using Pencil MCP |
| Duration | ~30 min |
| Skills Used | Pencil MCP |
| Prerequisites | Lesson 18-11 completed, output/pm/wireframes.md exists. Pencil MCP is connected to Cursor |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

> **💡 Tool Info**: This lesson uses Pencil MCP. It is available in the current workspace, Claude Code (CLI/desktop), and other environments. In some environments such as Codex CLI, you may encounter a `request_user_input is not supported` error. In that case, refer to the "Alternative Workflow" section.

## 📍 Step 1: Defining the Design System

First, create a design file in the project using Pencil MCP:
```bash
mkdir -p output/pm/ui-design
open_document("output/pm/ui-design/taskflow-ui.pen")
```
> **Save location**: `output/pm/ui-design/taskflow-ui.pen`

Define the foundational color palette, typography, spacing, and shadow styles for the design. These are elements used consistently across all screens.

```json
{
  "type": "AskQuestion",
  "question": "Select the design tone for TaskFlow",
  "options": [
    {
      "label": "Professional (blue)",
      "value": "professional",
      "description": "Business-oriented. Emphasizes trust and stability. Primary: blue (#0066CC), secondary: gray"
    },
    {
      "label": "Modern (purple)",
      "value": "modern",
      "description": "Advanced and refined. Emphasizes innovation. Primary: purple (#7C3AED), secondary: indigo"
    },
    {
      "label": "Friendly (green)",
      "value": "friendly",
      "description": "Approachable and calm. Emphasizes user-friendliness. Primary: green (#10B981), secondary: emerald"
    },
    {
      "label": "Custom",
      "value": "custom",
      "description": "Specify your own color palette"
    }
  ],
  "required": true,
  "hint": "Select based on your project positioning to determine the overall design tone"
}
```

### 🚀 Design System Definition Task

Based on the selected tone, define the following elements:

#### Color Palette
- **Primary Color**: Used for main actions and important elements
- **Secondary Color**: Used for support elements and secondary actions
- **Accent Color**: Used for status expressions such as warnings, success, and information
- **Background Colors**: Main background, sub-background (for containers)
- **Text Colors**: Body text, headings, supplementary text

#### Typography
- **Headings**: Font size 28px/24px/20px, weight Bold/SemiBold
- **Body**: Font size 16px/14px, weight Regular
- **Supplementary**: Font size 12px, weight Regular, opacity 70%
- **Recommended fonts**: Inter, Segoe UI, or SF Pro Display

#### Spacing Rules
- **Base unit**: 4px
- **Standard spacing**: 8px, 12px, 16px, 24px, 32px
- **Within components**: 12px - 16px
- **Between sections**: 24px - 32px
- **Page margins**: 16px (mobile) / 24px (desktop)

#### Border and Border Radius
- **Border Radius**: 4px (small) / 8px (medium) / 16px (large)
- **Border Color**: neutral-200 / neutral-300
- **Border Width**: 1px standard

#### Shadow Styles
- **Soft Shadow**: `0 1px 3px rgba(0,0,0,0.1)`
- **Medium Shadow**: `0 4px 12px rgba(0,0,0,0.15)`
- **Elevated Shadow**: `0 10px 30px rgba(0,0,0,0.2)`

---

## 📍 Step 2: Designing the Dashboard Screen

Design the dashboard, the main screen of TaskFlow. As the first screen users see, it needs to be intuitive with a clear information structure.

```json
{
  "type": "AskQuestion",
  "question": "Select the dashboard layout",
  "options": [
    {
      "label": "Card layout (statistics + task list)",
      "value": "card_layout",
      "description": "Statistics cards + task list. Balanced and most common"
    },
    {
      "label": "Kanban layout (status columns)",
      "value": "kanban_layout",
      "description": "Display tasks in columns by status. Visual progress management is easy"
    },
    {
      "label": "Timeline layout",
      "value": "timeline_layout",
      "description": "Display tasks chronologically. For schedule management"
    },
    {
      "label": "Get AI suggestions",
      "value": "ai_suggest",
      "description": "Suggest optimal layout based on project scale and purpose"
    }
  ],
  "required": true,
  "hint": "Select considering the number of tasks and management style of the project"
}
```

### 🚀 Dashboard Design Elements

#### Header Area (Height: 56px / 64px)
- Logo/brand name (left)
- Page title "Dashboard"
- User menu/notifications (right)
- Device support: Compact display on smartphones

#### Sidebar (Width: 256px / 200px)
- Navigation menu
  - Dashboard (current)
  - Task list
  - Projects
  - Team
  - Settings
- Collapsible function (mobile support)

#### Main Content Area
**Statistics Cards (Grid: 4 columns → 2 columns → 1 column)**
- Today's tasks: 🎯 Value + bar
- Completion rate: 📊 Percentage + circle progress
- Overdue tasks: ⚠️ Value + warning color
- Team activity: 👥 Activity count

**"Today's Tasks" Section (Height: 320px)**
- Filter/sort controls (top)
- Task list (scrollable)
  - Priority indicator
  - Task title
  - Assignee avatar
  - Due date display
  - Status badge
- "View all" button

**Recent Activity Section (Height: 240px)**
- Timeline view
- Activity items
  - Action type icon
  - Performer information
  - Timestamp (relative time)

---

## 📍 Step 3: Designing Task List/Detail Screens

Design the core screens for task management. They need to efficiently display large amounts of task information, allowing users to quickly access the information they need.

```json
{
  "type": "AskQuestion",
  "question": "Select the task list display format",
  "options": [
    {
      "label": "Table view",
      "value": "table_view",
      "description": "Table format. Display many columns at once. For large datasets"
    },
    {
      "label": "Card view",
      "value": "card_view",
      "description": "Card format. Visual task information. Limited information display"
    },
    {
      "label": "Kanban view",
      "value": "kanban_view",
      "description": "Columns by status. Status changes via drag and drop"
    },
    {
      "label": "List + card toggle",
      "value": "hybrid_view",
      "description": "Display list view and detail panel side by side. Flexible and feature-rich"
    }
  ],
  "required": true,
  "hint": "Select considering how users want to manage their tasks"
}
```

### 🚀 Task List Screen Design

#### Top Operation Bar (Height: 56px)
- Title "Task List"
- Search box
  - Placeholder: "Search tasks"
  - Search icon
- Filter button
  - Status
  - Priority
  - Assignee
  - Due date
- Sort menu
  - Date (newest/oldest)
  - Priority
  - Name (A-Z)
- Create new button (Primary Button)

#### Filter/Sort Panel (Expanded)
- Tabs: Filter / Sort
- Checkbox list
- Reset button
- Apply button

#### Task List Elements (depending on selected format)

**For table view:**
- Column headers: ☑️ | Task Name | Priority | Assignee | Due Date | Status | Actions
- Row height: 48px
- Hover effect: Background color change + action menu display
- Selection: Checkbox
- ↑↓ icons on sortable columns

**For card view:**
- Grid layout (3 columns → 2 columns → 1 column)
- Card contents:
  - Task name (bold)
  - Description (1-2 lines)
  - Tags/labels
  - Priority badge
  - Assignee avatar
  - Due date/time
  - Status badge
  - On hover: Quick actions (edit, delete, share)

**For kanban view:**
- Status columns (Unassigned / Planned / In Progress / Review / Completed)
- Each column header: Status name + task count
- Drag and drop area
- Card display (same as card view)
- "Add new" button (bottom of column)

**For list + card toggle:**
- Left panel: Task list (narrow display)
- Right panel: Selected task detail display
- Resizer (panel width adjustment)
- Real-time update when selecting items in the left panel

#### Pagination (Bottom)
- Page info display (e.g., 1-25 of 127)
- Page count selection
- Previous / Next buttons

---

### 📍 Task Detail Screen Design

#### Layout
- **Full page display**: Uses the entire browser (large screens)
- **Modal/side panel**: Displayed over the existing list (small to medium screens)

#### Header Section (Height: 72px)
- Task name (editable)
- Priority badge
- Status dropdown
- "×" close button / back button

#### Main Content (Scrollable)

**Basic Information Section**
- Task name
- Description/notes (Markdown supported)
- Priority selector
- Status
- Assignee
- Due date/time

**Detailed Information Section**
- Project
- Labels/tags
- Estimated effort
- Completion rate
- Parent task (if any)
- Related tasks

**Attachments Section**
- Upload area
- File list

**Activity/Comments Section**
- Timeline view
- Comment input field
- Existing comment display

#### Sidebar (Right)
- Checklist (subtasks)
- Assignee information
- Time tracking
- Related links

#### Bottom Action Bar
- Delete button
- Cancel button
- Save button (Primary)

---

## 📍 Step 4: Design Review

Verify that the created design meets requirements and is of high quality.

```json
{
  "type": "AskQuestion",
  "question": "Select the design review perspective",
  "options": [
    {
      "label": "UI consistency",
      "value": "consistency",
      "description": "Check consistency of colors, typography, and component shapes"
    },
    {
      "label": "Accessibility",
      "value": "accessibility",
      "description": "Check color blindness support, contrast ratio, and keyboard operation"
    },
    {
      "label": "Usability",
      "value": "usability",
      "description": "Check ease of operation, information findability, and task flow efficiency"
    },
    {
      "label": "All",
      "value": "all",
      "description": "Check all 3 perspectives above (most recommended)"
    }
  ],
  "required": true,
  "hint": "Selecting 'All' is recommended for higher quality"
}
```

### 🚀 UI Consistency Checklist

- [ ] Color palette is consistent across all screens
  - Primary Color usage (buttons, emphasis elements)
  - Secondary Color usage (backgrounds, auxiliary elements)
  - Warning/error/success colors are standardized
- [ ] Font specifications are consistent
  - Headings are always Bold/SemiBold
  - Body text is always Regular
  - Standard sizes 28/24/20/16/14/12px are used
- [ ] Spacing (margin/padding) is in multiples of 4px
  - Within components: 12px / 16px
  - Between sections: 24px / 32px
- [ ] Component shapes are consistent
  - Buttons: Same height (44px / 40px), same border-radius (8px)
  - Cards: Same border-radius (8px), same shadow
  - Input fields: Same height (40px), same border style
- [ ] Icons are consistent
  - Same icon set (Material Icons / Heroicons, etc.)
  - Same size (16px / 20px / 24px)
  - Same stroke weight

### ⚠️ Accessibility Checklist

- [ ] Contrast ratio meets WCAG AA standards
  - Text: Minimum 4.5:1 (normal text) / 3:1 (large text)
  - Graphic elements: Minimum 3:1
  - Especially check background and text color combinations
- [ ] Information is not conveyed by color alone
  - Priority: Color + icon + text
  - Status: Color + badge + label
  - Errors: Color + icon + message text
- [ ] Focus states are clearly visible
  - Button hover/focus states are visible
  - Focus indicators are clear (outline, etc.)
- [ ] Text sizes are sufficient
  - Body: Minimum 14px
  - Captions: Minimum 12px (should be avoided though)
- [ ] Interactive element target sizes are sufficient
  - Buttons: Minimum 44px x 44px (touch target)
  - Links: Minimum 16px height

### ✅ Usability Checklist

- [ ] Main user tasks can be performed efficiently
  - Task search: Within 3 clicks
  - Task creation: Within 4 steps
  - Task editing: Direct inline editing possible
  - Status change: One-click (kanban)
- [ ] Information hierarchy is clear
  - Most important information (task name, status) is easily visible
  - Secondary information (due date, assignee) is appropriately sized
  - Supplementary information (creation date, etc.) is inconspicuous
- [ ] Action (button) placement is logical
  - Primary actions (save, create) are at bottom-right or prominent position
  - Destructive actions (delete) use warning color + confirmation dialog
  - Secondary actions (cancel) are on the left side
- [ ] Error handling is clear
  - Validation errors are displayed directly below the input field
  - Error messages are specific and include solutions
  - Expressed with color + icon + text
- [ ] Responsive feedback is immediate
  - Button click: Visual change (color, animation)
  - Data submission: Loading state display
  - Error: Warning display (within 300ms)
- [ ] Consistency with wireframes
  - Dashboard layout matches wireframes.md
  - Task list layout meets specifications
  - All required elements (filter, search, etc.) are included

---

## ✅ Deliverables

Files and formats created in this lesson:

### .pen Files (Managed by Pencil MCP)
- `dashboard.pen` - Dashboard screen design
- `task-list.pen` - Task list screen design
- `task-detail.pen` - Task detail screen design
- `design-system.pen` - Design system (colors, typography, components)

### Documents (Reference)
- `output/pm/design-system.md` - Design system specification
  - Color palette definition (HEX/RGB codes)
  - Typography rules
  - Spacing rules
  - Component design specifications
  - Accessibility guidelines

---

## 🚀 Implementation Steps

### 1. Verify Pencil MCP Connection
```bash
cursor /pencil status
```
- Status: Connected
- Version: 1.0+

### 2. Create the Design System
```bash
cursor /pencil create-system \
  --name "TaskFlow" \
  --primary "#0066CC" \
  --secondary "#F3F4F6" \
  --accent "#EF4444"
```

### 3. Create Each Screen Design
- Dashboard: `/pencil design-screen dashboard --layout card_layout`
- Task list: `/pencil design-screen task-list --layout table_view`
- Task detail: `/pencil design-screen task-detail --layout full-page`

### 4. Component Design (Reusable Elements)
- Button（Primary / Secondary / Danger）
- Input Field
- Card
- Badge
- Avatar
- Dialog / Modal
- Dropdown
- Tabs

### 5. Export
```bash
cursor /pencil export --format png --output output/pm/designs/
cursor /pencil export --format figma --output output/pm/designs/figma-link
```

---

## 🔄 Alternative Workflow (for non-GUI environments)

In environments where Pencil MCP is not available (Claude Code, Codex CLI, SSH, etc.), create UI mockups directly with HTML + Tailwind CSS.

1. Refer to `output/pm/wireframes.md` to check design requirements
2. Write the Step 1 design system definition in Markdown at `output/pm/design-system.md`
3. Implement each screen (dashboard, task list, task detail) with HTML + Tailwind CSS CDN:
   ```bash
   mkdir -p output/pm/designs
   ```
4. Create `output/pm/designs/dashboard.html`, `task-list.html`, `task-detail.html`
5. Take screenshots with Playwright and save as PNG:
   ```bash
   npx playwright screenshot output/pm/designs/dashboard.html output/pm/designs/dashboard.png
   ```
6. The Step 4 design review checklist can be applied as-is

> HTML files will be the deliverables instead of .pen files. You can proceed directly to Lesson 18-13.

---

## ⚠️ Common Troubleshooting

### Pencil MCP Is Not Connected
**Cause**: Cursor extension is not loaded

**Solution**:
1. Check MCP in Cursor settings: Settings > Extensions > Pencil MCP
2. Restart: `cursor restart`
3. Connection test: `cursor /pencil status`

### Not Sure How to Edit the Design
**Reference steps**:
1. Right-click the relevant component in Pencil
2. Select "Edit"
3. Adjust color/size/placement in the properties panel
4. Verify in preview
5. Save（Ctrl+S）

### How to Choose a Color Palette
**Decision criteria**:
- **Professional**: For B2B/enterprise, financial, business management tools
- **Modern**: SaaS, startups, innovation-focused
- **Friendly**: Consumer-facing, learning/education, healthcare
- **Custom**: When existing brand colors are available

### Differences from Wireframes
**Check points**:
- Open `output/pm/wireframes.md`
- Check if each section layout matches the design
- If there are discrepancies, prioritize wireframes for corrections

### Component Reuse
**Recommended method**:
1. Open "Library" in Pencil
2. Drag pre-made components (buttons, cards, etc.)
3. Use the same components across multiple screens
4. All screens auto-update when components are updated

---

## 📍 Checkpoint

Once the following are completed, this lesson is complete:

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "title": "Design system defined",
      "description": "Color palette, typography, and spacing rules are saved in .pen",
      "verification": "cursor /pencil list-components | grep 'design-system'"
    },
    {
      "title": "Dashboard screen design completed",
      "description": "Header, sidebar, statistics cards, task list, and activity section are included",
      "verification": "ls output/pm/designs/dashboard.png"
    },
    {
      "title": "Task list screen design completed",
      "description": "Filter, sort, task display (selected format), and pagination are included",
      "verification": "ls output/pm/designs/task-list.png"
    },
    {
      "title": "Task detail screen design completed",
      "description": "Task information, activity/comments, sidebar, and actions are included",
      "verification": "ls output/pm/designs/task-detail.png"
    },
    {
      "title": ".pen files saved",
      "description": "dashboard.pen, task-list.pen, task-detail.pen, design-system.pen are all saved in Pencil MCP",
      "verification": "cursor /pencil list-files | wc -l >= 4"
    }
  ]
}
```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/ui-design/
├── taskflow-ui.pen       ← Pencil design file (main)
├── dashboard.png         ← Dashboard screen screenshot
├── task-list.png         ← Task list screen screenshot
└── task-detail.png       ← Task detail screen screenshot
```

### Verification Commands
```bash
# Check .pen files and screenshots
ls -lh output/pm/ui-design/

# Open images (macOS: open / Linux: xdg-open)
open output/pm/ui-design/
```

> 💡 **Claude Code**: `Read output/pm/ui-design/dashboard.png` for in-chat preview
> 💡 **Cursor**: Click on the image in the file explorer to preview
> 💡 **.pen files**: You can check contents with Pencil MCP's `batch_get` or `get_screenshot`

---

## ➡️ Next Steps

After completing this lesson, proceed to **Lesson 18-13: HTML + Tailwind CSS Prototype**.

Convert the designs created with Pencil MCP into actual code:

- Create HTML structure
- Styling with Tailwind CSS
- Responsive design (mobile / tablet / desktop)
- Interaction implementation (hover, click, animation)

**Start**: `cursor /lesson start-18-13`

---

## 📚 References

- [Pencil MCP Documentation](https://pencil.dev/docs)
- [Design System Best Practices](https://www.designsystems.com/)
- [WCAG 2.1 Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Tailwind CSS Component Collection](https://tailwindui.com/)
- [Material Design 3 Guidelines](https://m3.material.io/)
