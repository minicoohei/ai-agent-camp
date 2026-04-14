---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
duration: "~25 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["gas", "clasp", "google", "automation"]
---

# 🎓 Lesson 10-1: GAS Environment Setup with Clasp

## 📍 What You'll Do

**Lesson 10-1: GAS Development Environment Setup**!

| Item | Details |
|------|------|
| Goal | Enable local management and deployment of GAS projects with Clasp |
| Duration | ~25 min |
| Skills used | gas-clasp-ops, clasp CLI |
| Prerequisites | Node.js installed, Google account, Apps Script API enabled, Lesson 0-1 completed |
| Course page | [Module 10: GAS](https://ai-agent.camp/en/course/module-10)  alongside this lesson |

**Session flow:**
1. Install Clasp
2. Create a GAS project and push
3. Deploy and verify operation

By the end of this session, you will be able to edit and deploy GAS from your local machine.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite verification)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Install Clasp and Verify Apps Script API

First, verify that the Google Apps Script API is enabled.
If disabled, clasp login and clasp create will fail.

**Apps Script API Activation Check:**
1. Go to https://script.google.com/home/usersettings
2. Verify that the "Google Apps Script API" toggle is **ON**
3. If OFF, switch to ON

> **Important**: If the Apps Script API is disabled, all operations after `clasp login` (`clasp create`, `clasp push`, etc.) will fail. Be sure to enable it first.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Install Clasp",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please verify Clasp is working.
Run npx -y @google/clasp --version to verify.
```

**Expected result:** The Clasp version number is displayed (e.g., 2.4.2).

---

## 🚀 Step 2: Google Authentication

> **Relationship with gogcli**: You completed gogcli Google OAuth authentication (`gog auth login`) in 4-1, but clasp uses its own credentials. Since gogcli and clasp authentication are managed separately, you need to run `clasp login` here.
>
> - **gogcli authentication**: Saved in `~/.config/gogcli/` -> for Gmail, Calendar, Drive, Sheets API access
> - **clasp authentication**: Saved in `~/.clasprc.json` -> for managing and deploying Apps Script projects

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Google Authentication (clasp login)",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please run npx -y @google/clasp login to log in with your Google account.
A browser will open, so complete the authentication.
After authentication, verify that ~/.clasprc.json has been created.

Note: Google authentication for gogcli was completed in 4-1,
but clasp requires its own authentication. Log in with the same Google account.
```

**Expected result:** After authenticating in the browser, "Authorization successful" is displayed.

---

## 🚀 Step 3: Create a GAS Project

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Create a GAS Project",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please create the following directory and GAS project:

1. Create the ~/ai-agent-camp/gas-example directory
2. Run npx -y @google/clasp create --type standalone in that directory
3. Display the contents of the created .clasp.json and appsscript.json
```

**Expected result:** The script ID is listed in `.clasp.json` and timezone settings are included in `appsscript.json`.

---

## 🚀 Step 4: Create Hello World Script

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Create Hello World Script",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please create a Code.gs file in the gas-example directory with the following content:

function helloWorld() {
  Logger.log("Hello World from GAS!");
  return "Success";
}

function getExecutionInfo() {
  const info = {
    user: Session.getActiveUser().getEmail(),
    timezone: Session.getScriptTimeZone(),
    timestamp: new Date().toISOString()
  };
  Logger.log(JSON.stringify(info));
  return info;
}

Then sync with npx -y @google/clasp push.
```

**Expected result:** "Pushed X files." is displayed and reflected in Google Drive.

---

## 🚀 Step 5: Verify in GAS Editor

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Verify in GAS Editor",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please run npx -y @google/clasp open to open the Google Apps Script editor in the browser.
Run the helloWorld function in the editor and check the logs.
```

**Expected result:** The GAS editor opens and running the helloWorld function displays "Hello World from GAS!" in the log.

---

## ⚠️ Common Issues and Solutions

Use AskQuestion to select the issue, then follow the guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "clasp: command not found"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Push failed: File name contains invalid characters"},
      {"id": "trouble_4", "label": "Script ID is invalid"},
      {"id": "trouble_5", "label": "Apps Script API has not been used / is not enabled"}
    ]
  }]
}
```


### Issue 1: "clasp: command not found"
**Cause:** Clasp is not installed or not added to PATH
**Solution prompt:**
```
Please re-run npx -y @google/clasp --version and check the error. Make sure Node.js and npm are correctly installed.
```

### Issue 2: "Permission denied"
**Cause:** Google authentication is not complete
**Solution prompt:**
```
Please run npx -y @google/clasp logout and then run npx -y @google/clasp login again.
Please provide details of the authentication error.
```

### Issue 3: "Push failed: File name contains invalid characters"
**Cause:** File name contains non-ASCII characters such as Japanese
**Solution prompt:**
```
Please check file names in the gas-example directory and fix them to use only alphanumeric characters and underscores.
```

### Issue 4: "Script ID is invalid"
**Cause:** .clasp.json does not exist or is corrupted
**Solution prompt:**
```
Please delete the .clasp.json file and re-run npx -y @google/clasp create --type standalone.
```

### Issue 5: "Apps Script API has not been used in project / User has not enabled the Apps Script API"
**Cause:** Google Apps Script API is disabled
**Resolution steps**:
1. Go to https://script.google.com/home/usersettings
2. Switch the "Google Apps Script API" toggle to **ON**
3. After the change, redo from `clasp login`

> This setting is per Google account. Once enabled, it can be used for all subsequent GAS projects.

---

## ✅ Checkpoint
- [ ] Clasp is available (verify with npx -y @google/clasp --version)
- [ ] Google authentication is complete (~/.clasp.json exists)
- [ ] GAS project is initialized
- [ ] Code.gs has been created
- [ ] npx -y @google/clasp push succeeds
- [ ] Can execute in the GAS editor


---

## 📋 Deliverable Preview

### Expected Output
```
📁 output/gas/
└── Code.gs  (GAS script)
```

### Verification Commands
```bash
# Check local script files
ls -la output/gas/

# Check the beginning of script contents
head -30 output/gas/Code.gs

# Verify in GAS editor
npx -y @google/clasp open
```

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Please verify the following.
# 1. npx -y @google/clasp --version displays the version
# 2. gas-example/.clasp.json exists
# 3. gas-example/Code.gs exists
# 4. npx -y @google/clasp push succeeds (run in gas-example directory)
# 5. npx -y @google/clasp open opens the GAS editor
```

**Expected result:** All checklist items pass, and you can manage and deploy GAS projects from your local machine.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin a new section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/start-10-2)"},
      {"id": "next_window", "label": "Start in new window (/start-10-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /start-10-2
- next_window → Open new window with /start-10-2
- finish → End
