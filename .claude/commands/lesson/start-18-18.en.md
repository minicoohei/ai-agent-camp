---
description: "When the user says /start-18-18 — Module 18 Lesson 18-18: PM - Meeting Design & Minutes Analysis"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-17"]
level: "intermediate"
tags: ["pm", "meeting", "minutes", "spec-change"]
---

# 🎓 Lesson 18-18: Meeting Design & Minutes Analysis

| Item | Details |
|------|------|
| Goal | Design meeting structures for the TaskFlow project and auto-extract spec changes from sample minutes using AI |
| Duration | ~25 min |
| Skills Used | pm-toolkit skill |
| Prerequisites | Lesson 18-17 completed |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 📍 Step 1: Designing Meeting Types and Purposes

In project management, an appropriate meeting structure greatly affects the efficiency of information flow and decision-making. For the TaskFlow project, you need to design a meeting structure appropriate to the project scale.

### Basic Meeting Classification

**Regular meetings (Weekly/Bi-weekly)**
- Standup meeting: Progress reports and issue sharing (15 min)
- Sprint planning meeting: Task selection for the next sprint (60 min)
- Sprint retrospective: Reflection on results and improvement planning (45 min)

**Review meetings (As-needed)**
- Design review: Specification discussion and approval (90 min)
- Code review: Quality assurance and knowledge sharing (60 min)
- Business review: Stakeholder reporting (120 min)

**Retrospective meetings (Sprint end)**
- Retrospective workshop: Cross-team learning and improvement discovery (60 min)
- Risk retrospective: Project risk assessment (45 min)

**Ad-hoc meetings**
- Emergency response meeting: Discussion for production incidents (30 min)
- Customer request meeting: Discussion of new requirements (60 min)

```json
{
  "type": "AskQuestion",
  "question": "How do you want to design the meeting structure scale for the TaskFlow project?",
  "options": [
    {
      "id": "small_team",
      "label": "Small team (3-5 people) - 3 types of meetings",
      "meetings": [
        "Daily Standup",
        "Sprint Planning & Review",
        "Design Review"
      ],
      "frequency": "lightweight"
    },
    {
      "id": "medium_team",
      "label": "Medium team (6-15 people) - 6 types of meetings",
      "meetings": [
        "Daily Standup",
        "Sprint Planning",
        "Sprint Review",
        "Sprint Retrospective",
        "Design Review",
        "Business Review"
      ],
      "frequency": "standard"
    },
    {
      "id": "large_org",
      "label": "Large organization (16+ people) - 7+ types of meetings",
      "meetings": [
        "Daily Standup",
        "Sprint Planning",
        "Sprint Review",
        "Sprint Retrospective",
        "Design Review",
        "Code Review",
        "Business Review",
        "Risk Review",
        "Executive Steering"
      ],
      "frequency": "comprehensive"
    }
  ],
  "context": "Meeting structure scale is determined by team composition, project complexity, and number of stakeholders. Excessive meetings reduce productivity, so aim for a minimal yet effective configuration."
}
```

## 🚀 Step 2: Creating Meeting Structure Diagrams with PlantUML

Create structure diagrams with PlantUML to visually express the meeting structure, relationships, and flow.

```json
{
  "type": "AskQuestion",
  "question": "Which style do you want for the meeting structure diagram?",
  "options": [
    {
      "id": "org_chart",
      "label": "Org chart type (meeting hierarchy and subordination)",
      "focus": "hierarchy",
      "best_for": "Decision-making flow, clarification of responsibility distribution"
    },
    {
      "id": "flow_chart",
      "label": "Flow type (meeting flow along a timeline)",
      "focus": "timeline",
      "best_for": "Sprint cycle, decision-making process"
    },
    {
      "id": "matrix",
      "label": "Matrix type (correspondence table of meetings, attendees, and outputs)",
      "focus": "relationship",
      "best_for": "Attendee role distribution, scope of responsibility"
    }
  ],
  "context": "The diagram style choice is determined by the presentation audience (executives or field staff) and information readability."
}
```

### PlantUML Diagram Example (Flow type)

```plantuml
@startuml TaskFlow_MeetingStructure
!define ACCENT_COLOR #FF6B6B
!define PRIMARY_COLOR #4ECDC4
!define SUCCESS_COLOR #95E1D3

skinparam defaultFontName "Courier New"
skinparam defaultFontSize 12
skinparam backgroundColor #FFFACD
skinparam classBorderColor #333
skinparam classBackgroundColor #FFF
skinparam arrowColor #333

rectangle "Sprint Cycle (2 weeks)" #E8F8F5 {
  node "Monday\nSprint Planning\n(10:00-11:00)" as planning #PRIMARY_COLOR
  node "Daily\nStandup\n(09:30-10:00)" as standup #4ECDC4
  node "Wednesday\nDesign Review\n(14:00-15:30)" as design #FF9999
  node "Friday\nSprint Review\n(15:00-16:30)" as review #ACCENT_COLOR
  node "Friday\nRetro\n(16:30-17:30)" as retro #95E1D3

  planning --> standup: attend
  standup --> design: issues found
  design --> review: design approved
  review --> retro: feedback
  retro --> planning: improvements
}

rectangle "Ad-hoc Meetings" #FFE8E8 {
  node "Customer Request\nMeeting" as customer #FF6B6B
  node "Emergency\nResponse" as emergency #DD3C51
}

note right of planning
  Attendees: Team Lead, Dev, PM
  Output: Sprint Goal, Task Board
end note

note right of design
  Attendees: Architect, Senior Dev
  Output: Design Approval, Issues
end note

@enduml
```

This diagram includes the following elements:

- **Main cycle**: Regular meetings within a 2-week sprint cycle
- **Attendees**: List of attendees for each meeting
- **Outputs**: Deliverables generated from meetings
- **Dependencies**: Flow where decisions from previous meetings affect subsequent ones

Generate the file: **output/pm/meeting-structure.puml**

## ⚠️ Step 3: Loading Sample Meeting Minutes

Use the following sample meeting minutes as analysis targets.

Meeting minutes typically contain the following information:

- **Meeting information**: Date/time, location, attendees
- **Agenda**: List of discussion items
- **Decisions**: Agreed policies and specifications
- **Action items**: Follow-up tasks, owners, deadlines
- **Issues/Risks**: Identified problems
- **Next meeting schedule**: Follow-up

Partial example of sample meeting minutes:

```markdown
# Meeting Minutes

## Meeting Information
- Date/Time: 2024-02-09 10:00-11:30
- Location: Zoom / Meeting Room A
- Attendees: PM (Tanaka), Dev Lead (Sato), Architect (Suzuki), QA (Ando)

## Agenda
1. Sprint #5 progress report
2. Task creation screen UI specification
3. API response time optimization strategy
4. Pre-production release test plan

## Decisions
- Task creation screen: Add "Priority" field (dropdown: Low/Medium/High/Urgent)
- API response time target: Set to 500ms or less at P95
- Production release: Scheduled for mid-March

## Specification Changes
- Add priority field to Task Creation API (enum: low, medium, high, urgent)
- Implement filter functionality in Task List API (filter by status, assignee, priority)
- UI: Add "Priority" display to task detail screen

## Action Items
| Item | Assignee | Deadline |
|------|------|------|
| Create priority field specification | Suzuki | 2024-02-12 |
| Update API schema | Sato | 2024-02-13 |
| Update UI screen design document | Tanaka | 2024-02-14 |
| Design test cases | Ando | 2024-02-16 |

## Risks/Issues
- API response time optimization has high technical complexity -> Extend response period by 1 week
- Impact assessment needed for DB index additions
```

```json
{
  "type": "AskQuestion",
  "question": "At what level of depth do you want to perform meeting minutes analysis?",
  "options": [
    {
      "id": "spec_changes_only",
      "label": "Extract specification changes only",
      "extraction_target": [
        "API schema changes",
        "UI requirement changes",
        "DB schema changes",
        "New feature additions"
      ]
    },
    {
      "id": "all_decisions",
      "label": "Extract all decisions (specifications + policies + approvals)",
      "extraction_target": [
        "Specification changes",
        "Technical decisions",
        "Resource allocation decisions",
        "Release schedule finalization"
      ]
    },
    {
      "id": "comprehensive",
      "label": "Complete analysis including action items",
      "extraction_target": [
        "Specification changes",
        "All decisions",
        "Action items (assignee + deadline)",
        "Risk/issue registration",
        "Stakeholder agreement level"
      ]
    }
  ],
  "context": "The depth of analysis is determined by project scale and tracking systems. For medium or larger projects, action item management through complete analysis is important."
}
```

## ✅ Step 4: AI-based Auto-extraction of Spec Changes

Automatically extract sections corresponding to specification changes from meeting minutes and generate them as a structured report.

Information to extract:

- **Change content**: Which component (API/UI/DB) changes
- **Impact scope**: Which features or modules are affected
- **Change reason**: Why this change is needed (business requirement or technical reason)
- **Response priority**: Priority for implementing this change (Critical/High/Medium/Low)
- **Estimated effort**: Work required for implementation (hours or Story Points)
- **Response deadline**: When it needs to be addressed

Output format for automatic extraction results (Markdown):

```markdown
# Specification Change Extraction Report

Generated: 2024-02-10 15:45 JST
Source: meeting-minutes-sample.md (2024-02-09)
Analysis target: Extracted 3 specification changes from 4 decisions

## Specification Change List

### Change #1: Addition of Task Priority Field

| Item | Details |
|------|------|
| **Change Content** | Add priority field to Task Creation API (enum: low/medium/high/urgent) |
| **Impact Scope** | - API: POST /tasks, GET /tasks, PUT /tasks/{id}<br>- DB: Add priority column to tasks table<br>- UI: Add dropdown to task creation/edit screens<br>- Test: Add test cases for priority filter |
| **Change Reason** | Business requirement. Task prioritization enables teams to prioritize work based on importance. Customer request. |
| **Response Priority** | **High** |
| **Estimated Effort** | 8 Story Points (API 3 days + UI 2 days + Test 2 days) |
| **Response Deadline** | 2024-02-16 |
| **Design Lead** | Suzuki |
| **Implementation Lead** | Sato Team |

Related action items:
- [ ] Detailed specification (deadline: 2024-02-12)
- [ ] Update API schema (deadline: 2024-02-13)
- [ ] Update screen design document (deadline: 2024-02-14)
- [ ] Design test cases (deadline: 2024-02-16)

### Change #2: Implementation of Task List Filter Feature

| Item | Details |
|------|------|
| **Change Content** | Add query parameter-based filter to GET /tasks API<br>Supported filters: status, assignee, priority |
| **Impact Scope** | - API: Extension of GET /tasks endpoint<br>- DB: Index optimization (performance improvement)<br>- Frontend: Filter UI implementation |
| **Change Reason** | Usability improvement. Users can efficiently search for needed tasks from a large list. |
| **Response Priority** | **High** |
| **Estimated Effort** | 13 Story Points (API 3 days + Frontend 2 days + DB optimization 1 day + Test 2 days) |
| **Response Deadline** | 2024-02-23 |
| **Design Lead** | Suzuki |
| **Implementation Lead** | Sato, Tanaka |

Risk: Impact assessment needed for DB index additions on existing data

### Change #3: API Response Time Target Setting

| Item | Details |
|------|------|
| **Change Content** | Set non-functional requirements for API response time<br>P95: 500ms or less, P99: 1000ms or less |
| **Impact Scope** | - API: Optimization of all endpoints<br>- Infrastructure: Introduction of caching strategy<br>- Test: Performance test automation |
| **Change Reason** | Technical necessity. User experience improvement. Essential condition for SLA achievement. |
| **Response Priority** | **Critical** |
| **Estimated Effort** | 21 Story Points (Investigation/analysis 2 days + Implementation 4 days + Test 2 days + Production verification 1 day) |
| **Response Deadline** | 2024-03-01 (before production release) |
| **Design Lead** | Suzuki |
| **Implementation Lead** | Sato (Backend), Infrastructure Team |

## Summary

- **Extracted specification changes**: 3
- **Critical**: 1
- **High**: 2
- **Total estimated effort**: 42 Story Points
- **Risk count**: 1 (DB index verification)
- **Next follow-up**: 2024-02-13 Progress review meeting

## Auto-extraction Confidence

- AI confidence for all extracted items: 95%
- Manual review recommended: DB index impact assessment for Change #2
- Review responsible: Infrastructure Lead (Yamada)
```

Generate the file: **output/pm/spec-changes.md**


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── retrospective.md  (retrospective report)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/retrospective.md

# Check the beginning (first 30 lines)
head -30 output/pm/retrospective.md
```

> 💡 Full text: Run `cat output/pm/retrospective.md` to display the full text

## ➡️ Completion and Next Steps

Verify that the following deliverables are complete and placed in output/pm/.

**Files to generate:**

1. **meeting-structure.puml** - Meeting structure diagram in PlantUML format
   - Display regular meetings within the sprint cycle
   - Document attendees and outputs for each meeting
   - Display ad-hoc meetings in a separate section

2. **spec-changes.md** - Specification change extraction report
   - Table format including change content, impact scope, and reasons
   - Priority and risk assessment
   - Mapping to action items

**Completion criteria:**
- PlantUML diagram renders correctly (no errors)
- At least 3 specification changes are extracted
- Priority and estimated effort are specified for each change
- AI extraction confidence is 90% or higher

**Next Lesson**: Proceed to marimo dashboard creation with `/start-18-19`

The meeting design and AI meeting minutes analysis skills acquired in this lesson are important practices for visualizing project decision-making and preventing missed change requirements. Structured meeting management and automated information extraction significantly improve PM efficiency and accuracy.
