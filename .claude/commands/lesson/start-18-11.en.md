---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-10", "output/pm/wbs.md", "output/pm/requirements-spec.md"]
level: "intermediate"
tags: ["pm", "notion", "tracker", "collaboration"]
---

# 🎓 Lesson 18-11: Notion Integration

| Item | Details |
|------|------|
| Goal | Create a requirements tracker DB in Notion and manage TaskFlow requirements in a database |
| Duration | ~25 min |
| Skills Used | notion-db skill |
| Prerequisites | Lesson 18-10 completed, output/pm/requirements-spec.md exists. Notion API key is configured |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

---

## 📍 Step 1: Verifying Notion API Connection

### 🚀 Content

Check the Notion API connection status and configure the API key as needed.

```json
{
  "type": "AskQuestion",
  "question": "What is the status of your Notion API setup?",
  "options": [
    {
      "label": "Already set up",
      "value": "ready",
      "description": "Notion API key is set in environment variables"
    },
    {
      "label": "Setting up now",
      "value": "setup_now",
      "description": "Getting and setting up API key now"
    },
    {
      "label": "Want to skip Notion integration",
      "value": "skip",
      "description": "Use a markdown-based tracker as alternative"
    },
    {
      "label": "Having trouble",
      "value": "troubleshoot",
      "description": "There are issues with the connection settings"
    }
  ],
  "conditional": {
    "setup_now": "🔧 How to get Notion API key\n\n1. Log in to the Notion website (https://www.notion.so)\n2. Settings → Developer → My integrations → New integration\n3. Name: Enter 'TaskFlow PM Tracker'\n4. Capabilities: Select Read content, Update content, Insert content\n5. Associated workspace: Select target workspace\n6. Click Show API key\n7. Set the following environment variables:\n   - NOTION_API_KEY=YOUR_NOTION_SECRET_HERE\n   - NOTION_DATABASE_ID=xxxxxxxx... (set after creating DB)",
    "skip": "✅ If skipping Notion\n\nUse the following alternative:\n- Markdown-format requirements tracker\n- Type: output/pm/requirement-tracker.md\n- Manual updates required\n\nHowever, this lesson's checkpoints will not be implemented.",
    "troubleshoot": "⚠️ Troubleshooting\n\n[Error] \"NOTION_API_KEY not found\"\n→ Environment variable is not set. Refer to the API key setup method above.\n\n[Error] \"Unauthorized\"\n→ Check if the API key is correct. Retrieve it again from show API key.\n\n[Error] \"Rate limit exceeded\"\n→ Wait 15 seconds and try again.\n\nSee docs/setup-guides/ for details"
  }
}
```

### ⚠️ Verification Items

- [ ] Notion API key is set in environment variables
- [ ] Notion API key has been verified as valid
- [ ] Permissions exist for the target workspace
- [ ] API library can be installed in Node.js environment

---

## 📍 Step 2: Creating Requirements Tracker DB

### 🚀 Content

Create a requirements management database in Notion. Select the column configuration.

```json
{
  "type": "AskQuestion",
  "question": "Select the tracker column configuration",
  "options": [
    {
      "label": "Simple (5 columns)",
      "value": "simple",
      "description": "Basic info only: ID / Name / Category / Status / Priority"
    },
    {
      "label": "Standard (8 columns)",
      "value": "standard",
      "description": "Simple + Assignee / Related Use Cases / Notes"
    },
    {
      "label": "Detailed (12 columns)",
      "value": "detailed",
      "description": "Standard + Test Case ID / Planned Completion Date / Related Documents / Tech Stack"
    },
    {
      "label": "Custom",
      "value": "custom",
      "description": "Freely combine columns"
    }
  ]
}
```

### 📋 Database Schema

#### Simple Configuration (5 Columns)

| Column | Type | Description | Required |
|---------|----|----|------|
| Requirement ID | Text | REQ-001, REQ-002, etc. | Yes |
| Requirement Name | Title | Name of the requirement | Yes |
| Category | Select | Functional / Non-functional / Other | Yes |
| Status | Select | Not Started / Designing / Implementing / Testing / Completed | Yes |
| Priority | Select | Must / Should / Could / Won't | Yes |

#### Standard Configuration (8 Columns)

In addition to the simple configuration:

| Column | Type | Description | Required |
|---------|----|----|------|
| Assignee | People | Person responsible for this task | No |
| Related Use Cases | Relation | Link to UC-XXX | No |
| Notes | Text | Additional information and memos | No |

#### Detailed Configuration (12 Columns)

In addition to the standard configuration:

| Column | Type | Description | Required |
|---------|----|----|------|
| Test Case ID | Text | TC-001, etc. | No |
| Target Completion Date | Date | Target completion date | No |
| Related Documents | URL | Specifications and links | No |
| Tech Stack | Multi-select | React / Node.js, etc. | No |

### 🚀 Execution Steps

```bash
# 1. Create DB with notion-db skill
/notion-db create \
  --db-name "TaskFlow Requirements Tracker" \
  --workspace-name "TaskFlow PM" \
  --icon "📋" \
  --columns-template "standard"

# Output example:
# ✓ Database created
# Database ID: abc123def456...
# URL: https://notion.so/abc123def456...
# Set NOTION_DATABASE_ID environment variable
```

### ✅ Success Verification

- [ ] Database has been created in Notion
- [ ] URL: `https://notion.so/{DATABASE_ID}` is accessible
- [ ] All columns have been created correctly
- [ ] Environment variable `NOTION_DATABASE_ID` is set

---

## 📍 Step 3: Importing Requirements Data

### 🚀 Content

Extract requirements from requirements-spec.md and import them into the Notion DB.

```json
{
  "type": "AskQuestion",
  "question": "Select the data import method",
  "options": [
    {
      "label": "Auto-extract from requirements-spec.md",
      "value": "auto_extract",
      "description": "Automatically parse and import requirements from existing specification (recommended)"
    },
    {
      "label": "Manually one by one",
      "value": "manual",
      "description": "Add one at a time via form input"
    },
    {
      "label": "Bulk import with sample data",
      "value": "sample",
      "description": "Bulk import 15 sample requirements for testing"
    }
  ]
}
```

### 📋 Auto-extraction Procedure

```bash
# 1. Load requirements-spec.md
/notion-db import \
  --source-file "output/pm/requirements-spec.md" \
  --database-id "${NOTION_DATABASE_ID}" \
  --parse-mode "markdown" \
  --map-config '{
    "title": "requirement_name",
    "id": "requirement_id",
    "category": "category_field",
    "priority": "priority_field",
    "status": "initial_status:Not Started"
  }'

# 2. Verify import results
# Import count: 10-15 items
# Success count: XX items
# Error count: 0 items
```

### 📋 Sample Data Example

```markdown
| Req ID | Requirement Name | Category | Status | Priority | Related Use Cases | Notes |
|--------|--------|---------|----------|--------|---------------|------|
| REQ-001 | User Registration | Functional | Not Started | Must | UC-01 | Includes email verification |
| REQ-002 | Login | Functional | Not Started | Must | UC-02 | Password reset feature |
| REQ-003 | Dashboard Display | Functional | Not Started | Must | UC-05 | No real-time updates needed |
| REQ-004 | Task List Display | Functional | Not Started | Must | UC-06 | Includes filtering |
| REQ-005 | Task Create/Edit | Functional | Not Started | Must | UC-07 | Multiple priority levels |
| REQ-006 | Task Delete | Functional | Not Started | Should | UC-08 | Soft delete |
| REQ-007 | Notifications | Functional | Not Started | Should | UC-09 | Email/push support |
| REQ-008 | Deadline Alert | Functional | Not Started | Should | UC-10 | Notify 24 hours before |
| REQ-009 | Responsive Design | Non-functional | Not Started | Must | UC-11 | Mobile/Tablet/Desktop |
| REQ-010 | Page Load Time | Non-functional | Not Started | Should | N/A | Under 3 seconds |
| REQ-011 | Security (Encryption) | Non-functional | Not Started | Must | N/A | SSL/TLS required |
| REQ-012 | Database Optimization | Non-functional | Not Started | Could | N/A | Index configuration |
```

### ✅ Import Verification

- [ ] 10 or more requirements have been imported into the Notion DB
- [ ] All required fields (ID/Name/Category/Status) have been filled in
- [ ] Priority is appropriately set (Must: 40-50%, Should: 30-40%, Could: 10-20%)
- [ ] Viewing, searching, and filtering are possible in Notion

---

## 📍 Step 4: Markdown Export

### 🚀 Content

Export the Notion DB contents in markdown format and create documentation.

```json
{
  "type": "AskQuestion",
  "question": "Select the export format",
  "options": [
    {
      "label": "Markdown table format",
      "value": "markdown_table",
      "description": "Export in Markdown table format (recommended)"
    },
    {
      "label": "CSV",
      "value": "csv",
      "description": "Export as CSV file"
    },
    {
      "label": "JSON",
      "value": "json",
      "description": "Export as structured JSON"
    },
    {
      "label": "All",
      "value": "all",
      "description": "Generate in all 3 formats: Markdown + CSV + JSON"
    }
  ]
}
```

### 🚀 Execute Export

```bash
# 1. Export Notion DB
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "markdown" \
  --output-file "output/pm/notion-export.md" \
  --include-metadata true \
  --include-stats true

# 2. Also export in CSV format (recommended)
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "csv" \
  --output-file "output/pm/notion-export.csv"

# 3. Export in JSON format
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "json" \
  --output-file "output/pm/notion-export.json"
```

### 📋 Export Format Example

```markdown
# TaskFlow Requirements Tracker - Export

**Export date/time**: 2024-01-15 14:30:00 JST
**Database ID**: abc123def456...
**URL**: https://notion.so/abc123def456...

## 📊 Statistics

| Item | Count |
|------|------|
| Total Requirements | 15 |
| Not Started | 15 |
| In Design | 0 |
| In Development | 0 |
| In Testing | 0 |
| Completed | 0 |

### By Priority

| Priority | Count | Percentage |
|--------|------|------|
| Must | 7 | 46.7% |
| Should | 6 | 40.0% |
| Could | 2 | 13.3% |
| Won't | 0 | 0.0% |

### By Category

| Category | Count | Percentage |
|---------|------|------|
| Functional | 12 | 80% |
| Non-functional | 3 | 20% |

## 📋 Requirements List

| Req ID | Requirement Name | Category | Status | Priority | Related UC | Notes |
|--------|--------|---------|----------|--------|--------|------|
| REQ-001 | User Registration | Functional | Not Started | Must | UC-01 | Includes email verification |
| REQ-002 | Login | Functional | Not Started | Must | UC-02 | Password reset feature |
| ... | ... | ... | ... | ... | ... | ... |

---

**Generated by TaskFlow PM Training Platform**
```

### ✅ Export Verification

- [ ] output/pm/notion-export.md file has been generated
- [ ] Statistics are included (requirement count, status distribution, priority distribution)
- [ ] All requirements are displayed in table format
- [ ] Table format is correct (readable by Markdown parsers)
- [ ] CSV has also been exported if needed

---

## 🎯 DeliverablesChecklist

### Required Files and Data

```json
{
  "type": "AskQuestion",
  "question": "Are the following deliverables complete? Check all that apply",
  "options": [
    {
      "label": "✓ Notion setup (API connection verified)",
      "value": "step1_done"
    },
    {
      "label": "✓ Requirements tracker DB created",
      "value": "step2_done"
    },
    {
      "label": "✓ Requirements data imported (10+ items)",
      "value": "step3_done"
    },
    {
      "label": "✓ Markdown export completed",
      "value": "step4_done"
    },
    {
      "label": "✓ output/pm/notion-export.md file generated",
      "value": "export_done"
    }
  ]
}
```

### ✅ Success Criteria

- **Notion API Connection**: Environment variables `NOTION_API_KEY` and `NOTION_DATABASE_ID` are correctly set
- **DB Creation**: Requirements tracker DB is visible and accessible in the Notion dashboard
- **Data Import**: At least 10, ideally 15 requirements exist in the DB
- **Status Distribution**: All set to "Not Started" in initial state
- **Priority Distribution**: Must 40-50%, Should 30-40%, Could 10-20% approximately
- **Export Complete**: output/pm/notion-export.md has been generated, containing statistics and a full requirements list

---

## ⚠️ Troubleshooting

### Error: "NOTION_API_KEY not found"

```text
Cause: Environment variable is not set
Solution:
1. Get Notion API key (https://www.notion.so/settings/integrations)
2. Run the following:
   export NOTION_API_KEY="YOUR_NOTION_SECRET_HERE"          # Mac/Linux/WSL
3. Run again
```

### Error: "Unauthorized - Invalid API key"

```text
Cause: API key is invalid or expired
Solution:
1. Generate a new API key from Notion settings
2. Update environment variable
3. Run again
```

### Error: "Database not found"

```text
Cause: NOTION_DATABASE_ID is incorrect, or DB access permission is missing
Solution:
1. Verify the correct ID from the Notion DB URL
   Extract ID from https://notion.so/[32-character ID]
2. Fix environment variable
3. Verify the integration has access to the DB
```

### Error: "Rate limit exceeded"

```text
Cause: API request frequency is too high
Solution:
1. Wait 15 seconds
2. Run again
3. Use the --delay flag when importing large data
```

### Error: "Markdown parse failure"

```text
Cause: requirements-spec.md format is incorrect
Solution:
1. Check the format of requirements-spec.md
2. Import manually one at a time (manual mode)
3. Or try with sample data
```

### Files Are Not Generated

```text
Cause: output/pm/ directory does not exist, or insufficient permissions
Solution:
1. Create directory: mkdir -p output/pm
2. Check permissions: ls -la output/
3. Run again
```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── test-cases.md  (Test Cases List)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/test-cases.md

# Check the beginning (first 30 lines)
head -30 output/pm/test-cases.md
```

> 💡 Full text: Run `cat output/pm/test-cases.md` to display the full text

---

## ➡️ Next Steps

### 🎓 Lesson 18-12: UI Design

**Phase Progress**: Phase B (Requirements Definition & Design) complete!

The next lesson proceeds to Phase C (Design & Implementation).

- Create TaskFlow UI prototypes
- Wireframe design
- Design system definition
- Frontend implementation preparation

**Duration**: ~30 min
**Skills Used**: figma-design / wireframe skill

---

## 📚 Reference Resources

### Notion API Documentation
- [Notion API Documentation](https://developers.notion.com/)
- [Database API Reference](https://developers.notion.com/reference/database)
- [Query Database](https://developers.notion.com/reference/post-database-query)

### TaskFlow PM Module
- Module 18: System Requirements Definition (Planning → Requirements → Design → Implementation → Testing → Summary)

### Related Lessons
- Lesson 18-10: Requirements Specification Creation (Requirements Analysis)
- Lesson 18-12: UI Design (Design & Implementation Phase)
- Lesson 18-13: Implementation Plan Creation (Implementation Phase)

---

**Created**: 2024-01-15
**Last Updated**: 2024-01-15
**Module**: 14-PM-System Definition
**Level**: Intermediate
