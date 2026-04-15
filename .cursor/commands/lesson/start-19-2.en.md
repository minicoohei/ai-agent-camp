---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module19-outlook-windows"
duration: "About 35 min"
prerequisites: ["start-19-1"]
level: "intermediate"
tags: ["outlook", "microsoft365", "rules", "folders", "categories"]
---

# 🎓 Lesson 19-2: Folders, Rules & Categories

## 📍 What You'll Do in This Session

Welcome to **Lesson 19-2: Folders, Rules & Categories**!

| Item | Details |
|------|---------|
| Goal | Automate email organization using Outlook folders, rules, and categories |
| Duration | About 35 min |
| Skills Used | Outlook rule configuration, category management, m365 CLI |
| Prerequisites | Lesson 19-1 completed (m365 CLI authentication set up) |
| Course Page | Refer to [Module 19: Outlook](https://ai-agent.camp/en/course/module-19) in parallel |

> **💡 Tool Info**: This lesson uses m365 CLI. It works with Cursor IDE and Claude Code (CLI/Desktop). In some environments like Codex CLI, you may see a `request_user_input is not supported` error. If so, refer to the "Alternative Workflow" section.

**Session Flow:**
1. Learn folder design that keeps the inbox lean
2. Configure rule conditions and actions (move, assign categories, etc.)
3. Understand cross-cutting tagging with categories
4. After applying organization rules, automate email listing and sending with m365 CLI
5. Record and save configuration results to output/outlook/

By the end of this session, you'll be able to organize your inbox using Outlook folders, rules, and categories, and automate tasks with m365 CLI.

> **💡 Hint**: If the AI response stops midway, type "continue" or "please go on" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first confirm everything is set up.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session Check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's go"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Check prerequisites)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Folder Design — Don't Let the Inbox Overflow

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Folder Design Basics",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please explain best practices for Outlook folder design. Cover the following:

1. Basic folder design principles:
   - Aim for Inbox Zero
   - Keep hierarchy to 2 levels max (too deep becomes unmanageable)
   - Action-based vs. project-based organization

2. Recommended folder structure example:
   - 📁 01_Action Required (emails needing response)
   - 📁 02_Waiting (awaiting reply/approval)
   - 📁 03_Reference (read-only/informational)
   - 📁 04_Projects/ (project-specific subfolders)
   - 📁 05_Archive/ (monthly/yearly)

3. List folders with m365 CLI:
   m365 outlook mail folder list
```

**Expected result**: You understand folder design principles and have reviewed your current folder structure.

---

## 🚀 Step 2: Rule Conditions and Actions (Move, Categorize)

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Rule Conditions and Actions",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please explain how to set up Outlook rules. Cover the following:

1. Basic rule structure:
   - Condition: When the rule triggers
   - Action: What happens when conditions are met
   - Exception: When to skip the rule

2. Common conditions:
   - Filter by sender (from)
   - Subject contains keyword
   - Recipient (to/cc) — when you're CC'd
   - By domain (@company.com etc.)

3. Common actions:
   - Move to specific folder
   - Assign category
   - Change importance level
   - Add flag
   - Show notification

4. Practice: Create the following rules in Outlook
   - Rule 1: Internal emails (@your-domain) → Assign "Internal" category
   - Rule 2: Newsletters → Move to "03_Reference" folder
   - Rule 3: Emails from your manager → Set importance to "High"

5. Record configuration in output/outlook/rules-config.json
```

**Expected result**: Three rules are created in Outlook with automatic sorting based on conditions.

---

## 🚀 Step 3: Cross-Cutting Tagging with Categories

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Cross-Cutting Tagging with Categories",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Set up cross-cutting tagging using Outlook's category feature.

Steps:
1. Basic category concepts:
   - Folders = one email can only be in one folder
   - Categories = one email can have multiple tags
   - Use folders for "location", categories for "nature"

2. Category design example:
   - 🔴 Urgent (Red): Needs action today
   - 🟡 This Week (Yellow): Needs action this week
   - 🟢 Info (Green): Read-only
   - 🔵 Project A (Blue): Project A related
   - 🟣 Project B (Purple): Project B related

3. Check categories with m365 CLI:
   m365 outlook mail list --top 10 --query "categories/any(c:c eq 'Urgent')"

4. Design combined rules for categories and folders
5. Record configuration in output/outlook/categories-config.json
```

**Expected result**: Categories are set up and combined with folders for efficient email management.

---

## 🚀 Step 4: Automating Email Listing and Sending with m365 CLI

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Automating with m365 CLI",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Use m365 CLI to automate email listing and sending after organization.

Steps:
1. mkdir -p output/outlook

2. Get email lists by folder:
   # Inbox email list
   m365 outlook mail list --top 20 --output json > output/outlook/inbox-list.json

   # List mail folders
   m365 outlook mail folder list --output json

3. Filtered retrieval:
   # Unread emails only
   m365 outlook mail list --filter "isRead eq false" --output json

   # Emails with specific category
   m365 outlook mail list --filter "categories/any(c:c eq 'Urgent')" --output json

4. Automate email sending:
   m365 outlook mail send \
     --to "colleague@example.com" \
     --subject "Weekly Report" \
     --bodyContents "Please find this week's report attached." \
     --bodyContentType Text

5. Save results to output/outlook/automation-result.json
```

**Expected result**: Email listing and sending are automated with m365 CLI, results saved in output/outlook/.

---

## 🚀 Step 5: Verifying Configuration and Record Keeping

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Verifying Configuration and Record Keeping",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Verify configuration results so far and create a summary.

Steps:
1. Display the folder structure you created
2. Review rule list with conditions and actions for each rule
3. Review category design and operational rules
4. Create a summary in output/outlook/summary.md covering:
   - Folder structure
   - Rule configuration (condition → action)
   - Category design
   - m365 CLI automation command list
5. Suggest 3 improvement points for ongoing operations
```

**Expected result**: A configuration summary for folders, rules, and categories is saved in output/outlook/.

---

## ⚠️ Common Troubleshooting

AskUserQuestion (AskQuestion) lets you select the issue for guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "m365 CLI authentication expired"},
      {"id": "trouble_2", "label": "Rules not working as expected"},
      {"id": "trouble_3", "label": "Categories not showing"},
      {"id": "trouble_4", "label": "Email sending error"}
    ]
  }]
}
```


### Trouble 1: "m365 CLI authentication expired"
**Cause**: Access token has expired
**Solution prompt**:
```
Re-authenticate with the m365 login command.
Use m365 status to check the current authentication state.
If the token has expired, browser-based re-authentication is required.
```

### Trouble 2: "Rules not working as expected"
**Cause**: Incorrect rule conditions or rule priority issues
**Solution prompt**:
```
Review the conditions and actions in Outlook's rule settings.
Rules are applied from top to bottom, so check their priority order.
Verify whether the "Stop processing more rules" option is enabled.
```

### Trouble 3: "Categories not showing"
**Cause**: Categories not created or filter query is incorrect
**Solution prompt**:
```
Check if categories are created in Outlook Settings → Category Management.
Verify the m365 CLI filter syntax is correct.
Category names must be specified as exact matches.
```

### Trouble 4: "Email sending error"
**Cause**: Insufficient permissions or invalid send parameters
**Solution prompt**:
```
Verify that Mail.Send permission is granted to m365 CLI.
Check that a valid email address is specified in the --to parameter.
--bodyContentType can be either Text or HTML.
```

---

## ✅ Checkpoint
- [ ] Understood folder design principles and reviewed folder structure
- [ ] Configured rule conditions and actions for automatic sorting
- [ ] Understood cross-cutting tagging with categories
- [ ] Automated email listing and sending with m365 CLI
- [ ] Configuration results saved in output/outlook/


---

## 📋 Deliverables Preview

### Expected Output
```
📁 output/outlook/
├── inbox-list.json            ← Inbox email list
├── rules-config.json          ← Rule configuration record
├── categories-config.json     ← Category configuration record
├── automation-result.json     ← m365 CLI automation results
└── summary.md                 ← Configuration summary
```
> Format: JSON / Markdown

### Verification Commands
```bash
# Check output files
ls -lh output/outlook/

# Check email list
cat output/outlook/inbox-list.json | jq '.[:3]'

# Check summary
cat output/outlook/summary.md
```

> 💡 **Claude Code**: `Read output/outlook/summary.md` for in-chat preview
> 💡 **Cursor**: Click the file in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor's chat to check completion status:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

AskUserQuestion (AskQuestion) lets you choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose your next action",
    "options": [
      {"id": "next_module", "label": "Proceed to Module 20 (/start-20-1)"},
      {"id": "review_module", "label": "Review Module 19"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_module → /start-20-1 for Module 20
- review_module → Review each lesson in Module 19
- finish → End session
