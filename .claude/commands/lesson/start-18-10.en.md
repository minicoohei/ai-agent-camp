---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-9", "output/pm/api-spec.yaml"]
level: "intermediate"
tags: ["pm", "wbs", "gantt", "schedule"]
---

# 🎓 Lesson 18-10: WBS & Gantt Chart

| Item | Details |
|------|------|
| Goal | Create a WBS for the TaskFlow project and generate a Gantt chart with PlantUML |
| Duration | ~25 min |
| Skills Used | pm-toolkit skill |
| Prerequisites | Lesson 18-9 completed, all design documents up to this point are available |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

---

## 📍 Learning Objectives

In this lesson, you will learn the following:

- How to create a **WBS (Work Breakdown Structure)**
- Task decomposition and hierarchical structuring of the project
- Key estimation methods for effort
- PlantUML Gantt chart generation and utilization
- Critical path analysis

---

## 🚀 Step 1: Creating the WBS

A Work Breakdown Structure (WBS) is a method for decomposing a project into smaller, manageable tasks. Visualize the overall structure of the TaskFlow project.

### 📊 TaskFlow WBS Structure

```text
TaskFlow Project
├── 1. Planning Phase
│   ├── 1.1 Requirements Definition
│   ├── 1.2 Competitive Analysis
│   └── 1.3 Project Plan
├── 2. Design Phase
│   ├── 2.1 System Design
│   ├── 2.2 UI/UX Design
│   ├── 2.3 Database Design
│   └── 2.4 API Specification Design
├── 3. Implementation Phase
│   ├── 3.1 Backend Development
│   ├── 3.2 Frontend Development
│   ├── 3.3 Integration
│   └── 3.4 Test Environment Setup
├── 4. Testing Phase
│   ├── 4.1 Unit Testing
│   ├── 4.2 Integration Testing
│   ├── 4.3 UAT
│   └── 4.4 Production Environment Testing
└── 5. Deployment & Operations Phase
    ├── 5.1 Production Environment Setup
    ├── 5.2 Deployment
    ├── 5.3 Operations Start
    └── 5.4 User Support Setup
```

### ❓ Select WBS Granularity

```json
{
  "type": "AskQuestion",
  "id": "wbs-granularity",
  "question": "Select the WBS granularity",
  "description": "Select the WBS decomposition level based on the project's scale and complexity",
  "options": [
    {
      "value": "level2",
      "label": "Major items only (Level 2)",
      "description": "5 main phases only. For small projects",
      "recommended": false
    },
    {
      "value": "level3",
      "label": "Up to mid-level items (Level 3)",
      "description": "Major tasks for each phase. Recommended level",
      "recommended": true
    },
    {
      "value": "level4",
      "label": "Detailed (Level 4)",
      "description": "Further subdivided. For complex projects",
      "recommended": false
    },
    {
      "value": "ai-suggest",
      "label": "Get AI to suggest optimal granularity",
      "description": "Automatic determination from project scale"
    }
  ],
  "default": "level3"
}
```

---

## 💼 Step 2: Effort Estimation

Estimate the effort required for each WBS task. Accurate effort estimation is key to project success.

### 📌 Key Estimation Methods

| Method | Features | Application Scenario |
|------|------|---------|
| **Analogous Estimation** | Estimate from past similar projects | When extensive experience exists |
| **Three-point Estimation** | Calculate from optimistic/most likely/pessimistic values | When uncertainty is high |
| **Function Point Method** | Calculate by function complexity | Software development |
| **Bottom-up Estimation** | Accumulate from detailed tasks | After detailed design |

### ❓ Select Estimation Method

```json
{
  "type": "AskQuestion",
  "id": "estimation-method",
  "question": "Select the estimation method",
  "description": "Select the appropriate estimation method based on project characteristics",
  "options": [
    {
      "value": "analogy",
      "label": "Analogous Estimation",
      "description": "Estimated from past similar projects. For quick estimation"
    },
    {
      "value": "three-point",
      "label": "3-Point Estimation (Optimistic/Most Likely/Pessimistic)",
      "description": "PERT method. Precise estimation considering uncertainty"
    },
    {
      "value": "function-point",
      "label": "Function Point Analysis",
      "description": "Quantification by feature complexity. Optimal for software development"
    },
    {
      "value": "ai-estimate",
      "label": "Get AI estimation",
      "description": "Automatic estimation by analyzing WBS"
    }
  ],
  "default": "three-point"
}
```

### 📋 TaskFlow Effort Estimation Example (Three-point Estimation)

| WBS Code | Task | Optimistic (days) | Most Likely (days) | Pessimistic (days) | Expected (days) |
|-----------|--------|----------|----------|----------|-----------|
| 1.1 | Requirements Definition | 2 | 3 | 5 | 3.2 |
| 1.2 | Competitive Analysis | 1 | 2 | 4 | 2.2 |
| 1.3 | Project Planning | 1 | 2 | 3 | 2.0 |
| 2.1 | System Design | 3 | 5 | 8 | 5.2 |
| 2.2 | UI/UX Design | 2 | 4 | 7 | 4.2 |
| 2.3 | DB Design | 2 | 3 | 5 | 3.2 |
| 2.4 | API Spec Design | 2 | 3 | 5 | 3.2 |
| 3.1 | Backend Development | 8 | 12 | 18 | 12.3 |
| 3.2 | Frontend Development | 6 | 10 | 15 | 10.2 |
| 3.3 | Integration | 2 | 4 | 7 | 4.2 |
| 3.4 | Test Environment Setup | 1 | 2 | 3 | 2.0 |
| 4.1 | Unit Testing | 3 | 5 | 8 | 5.2 |
| 4.2 | Integration Testing | 2 | 4 | 6 | 4.0 |
| 4.3 | UAT | 2 | 3 | 5 | 3.2 |
| 4.4 | Production Environment Testing | 1 | 2 | 3 | 2.0 |
| 5.1 | Production Environment Preparation | 1 | 2 | 4 | 2.2 |
| 5.2 | Deployment | 1 | 2 | 3 | 2.0 |
| 5.3 | Operations Launch | 1 | 2 | 3 | 2.0 |
| 5.4 | Support Setup | 1 | 1 | 2 | 1.2 |

**Total Planned Effort: 73.7 person-days**

---

## 📅 Step 3: Generating PlantUML Gantt Charts

Gantt charts visualize project schedules, task dependencies, and progress.

### ❓ Select Gantt Chart Display Period

```json
{
  "type": "AskQuestion",
  "id": "gantt-period",
  "question": "Select the Gantt chart display period",
  "description": "Select the display period based on the project duration",
  "options": [
    {
      "value": "1month",
      "label": "1 month",
      "description": "Detailed daily display"
    },
    {
      "value": "3months",
      "label": "3 months",
      "description": "Recommended. Typical project duration"
    },
    {
      "value": "6months",
      "label": "6 months",
      "description": "For large-scale projects"
    },
    {
      "value": "custom",
      "label": "Custom",
      "description": "Specify any period"
    }
  ],
  "default": "3months"
}
```

### 📊 PlantUML Gantt Chart Example

```plantuml
@startgantt
title TaskFlow Project Gantt Chart
dateFormat YYYY-MM-DD
projectScale monthly
axisFormat %Y-%m

section Planning
Requirements Definition :crit, wbs-1-1, 2024-04-01, 3d
Competitive Analysis   :crit, wbs-1-2, after wbs-1-1, 2d
Project Plan           :crit, wbs-1-3, after wbs-1-2, 2d

section Design
System Design          :des1, wbs-2-1, after wbs-1-3, 5d
UI/UX Design           :des1, wbs-2-2, after wbs-1-3, 4d
DB Design              :des2, wbs-2-3, after wbs-2-1, 3d
API Spec Design        :des2, wbs-2-4, after wbs-2-1, 3d
Design Review          :milestone, des-review, after wbs-2-4, 1d

section Implementation
Backend Development    :impl1, wbs-3-1, after des-review, 12d
Frontend Development   :impl1, wbs-3-2, after des-review, 10d
Integration            :impl2, wbs-3-3, after wbs-3-1, 4d
Test Environment Setup :impl2, wbs-3-4, after wbs-3-1, 2d

section Testing
Unit Testing           :test1, wbs-4-1, after wbs-3-3, 5d
Integration Testing    :test1, wbs-4-2, after wbs-4-1, 4d
UAT              :test2, wbs-4-3, after wbs-4-2, 3d
Production Env Testing :test2, wbs-4-4, after wbs-4-3, 2d
Testing Complete       :milestone, test-complete, after wbs-4-4, 1d

section Deployment & Operations
Production Env Setup   :deploy1, wbs-5-1, after test-complete, 2d
Deployment             :deploy1, wbs-5-2, after wbs-5-1, 2d
Operations Start       :deploy2, wbs-5-3, after wbs-5-2, 2d
Support Setup          :deploy2, wbs-5-4, after wbs-5-3, 1d
Release                :crit, milestone, after wbs-5-4, 1d

@endgantt
```

### 🎯 Key PlantUML Gantt Syntax Elements

```markdown
- **dateFormat**: Date format (YYYY-MM-DD, etc.)
- **projectScale**: Display unit (daily/weekly/monthly)
- **section**: Section (phase) name
- **Task definition**: `Task name :type, id, start, duration`
  - type: `crit` (critical), `milestone`, `active` (in progress)
  - start: `2024-04-01` or `after id`
  - duration: `5d` (5 days), `1w` (1 week)
- **Milestone**: Displayed with `milestone` type
```

---

## 🔍 Step 4: Critical Path Analysis

The critical path is the longest path to project completion and the set of tasks with the greatest impact from delays.

### ❓ Perform Critical Path Analysis

```json
{
  "type": "AskQuestion",
  "id": "critical-path",
  "question": "Perform critical path analysis?",
  "description": "Manage project delay risk by identifying the critical path",
  "options": [
    {
      "value": "ai-analyze",
      "label": "Yes, have AI analyze",
      "description": "Automatic analysis from WBS and effort estimates. Recommended"
    },
    {
      "value": "manual",
      "label": "Verify myself",
      "description": "Manually identify by checking WBS and dependencies"
    },
    {
      "value": "skip",
      "label": "Skip",
      "description": "Skip critical path analysis"
    }
  ],
  "default": "ai-analyze"
}
```

### 📍 TaskFlow Critical Path Example

**Longest Path (approximately 55 days total effort):**
```text
Requirements Definition (3.2 days)
→ Competitive Analysis (2.2 days)
→ Project Plan (2.0 days)
→ System Design (5.2 days)
→ API Spec Design (3.2 days)
→ Backend Development (12.3 days)
→ Integration (4.2 days)
→ Unit Testing (5.2 days)
→ Integration Testing (4.0 days)
→ UAT (3.2 days)
→ Production Env Testing (2.0 days)
→ Production Env Setup (2.2 days)
→ Deployment (2.0 days)
→ Operations Start (2.0 days)
→ Support Setup (1.2 days)
```

### ⚠️ Risk Area Identification

| Risk Area | Factor | Countermeasure |
|-----------|------|------|
| Backend Development | Longest implementation task (12.3 days) | Early start, secure resources |
| Integration | Unexpected interactions | Conduct early integration testing |
| Database Design | Possibility of requirement changes | Prioritize requirement finalization |

---

## 📝 Deliverables Checklist

### ✅ Output Files

1. **output/pm/wbs.md** - WBS structure and detailed description
2. **output/pm/gantt-chart.puml** - PlantUML Gantt chart

### ✅ Checkpoint

```markdown
□ WBS decomposed to Level 3 or higher
□ Effort estimates set for all tasks
□ Gantt chart generated
□ 3 or more milestones set
□ wbs.md file generated
□ gantt-chart.puml file generated
□ Critical path identified (optional)
□ Risk areas identified (optional)
```

---

## 🔧 Troubleshooting

### ❓ Do not know the WBS decomposition granularity

**Solution:**
- Recommend starting with Level 3 (mid-level items)
- 20-30 tasks is a manageable range
- 3-5 WBS items per phase is a guideline

### ❓ No basis for effort estimation

**Solution:**
- Refer to past similar task performance
- Consider team member skill levels
- Absorb uncertainty with three-point estimation
- Secure a buffer (10-20%)

### ❓ Do not understand PlantUML Gantt syntax

**Solution:**
- Refer to [PlantUML Gantt official documentation](https://plantuml.com/gantt-diagram)
- Express dependencies with the `after` keyword
- Display major milestones with `milestone`
- Highlight critical tasks with `crit`

### ❓ Cannot understand the concept of critical path

**Solution:**
- Learn the basics of CPM (Critical Path Method)
- Calculate "earliest start date" and "latest start date" for each task
- Tasks with zero slack (float) form the critical path
- Manage them as a priority since they have the greatest delay impact

---

## 🎬 Next Steps

### ➡️ Next Lesson

**[Lesson 18-11: Notion Integration](./start-18-11.md)**

Through Notion integration, share the WBS and Gantt chart with the entire team and manage progress in real-time.

### 📚 Related Resources

- [Module 18: PM & System Definition](https://ai-agent.camp/en/course/module-18)
- [PlantUML Gantt Official Documentation](https://plantuml.com/gantt-diagram)

---

## 📌 Key Points

🎯 **WBS clarifies "what to do"**
- Ambiguous tasks lead to problems later
- Each task should be independent and comprehensive (MECE principle)

⏱️ **Be conservative with effort estimates**
- Add a 20-30% buffer to initial estimates
- If uncertainty decreases during implementation, the buffer can be reduced

📊 **The Gantt chart is a living document**
- Update regularly even after the project starts
- Regularly check discrepancies between actual and planned (progress rate, remaining effort)

🚨 **Tasks outside the critical path have flexibility**
- Effectively utilize buffer (slack) for resource adjustment
- However, note that when slack is consumed, the critical path may change

---

**When this lesson is complete, proceed to Lesson 18-11.**
