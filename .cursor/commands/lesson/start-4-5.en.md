---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "drive"]
---

# 🎓 Lesson 4-5: Google Drive Operations

## 📍 What You'll Do

**Lesson 4-5: Google Drive Operations** !

| Item | Details |
|------|---------|
| Goal | List, download, and upload files on Drive using gogcli |
| Duration | ~25 min |
| Skills Used | gogcli drive |
| Prerequisites | gogcli authentication setup completed (start-4-1 done) |

**Session flow:**
1. List and search files in Drive
2. Download files
3. Upload files

By the end of this session, you will be able to operate Google Drive files using gogcli.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. The response may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → `gog auth list`  to check auth status)
(different_lesson → Show module list)

---

## 🚀 Step 1: List and Search Files in Drive

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: File list and search",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:

Let's list the files in Google Drive:

```bash
# Root folder file list (latest 10)
gog drive ls --account your-email@gmail.com --max 10

# Search by file name
gog drive ls --account your-email@gmail.com --query "name contains 'minutes'"

# Filter by MIME type (spreadsheets only)
gog drive ls --account your-email@gmail.com --query "mimeType='application/vnd.google-apps.spreadsheet'"

# Google Docs only
gog drive ls --account your-email@gmail.com --query "mimeType='application/vnd.google-apps.document'"

# PDF files only
gog drive ls --account your-email@gmail.com --query "mimeType='application/pdf'"

# File list in a specific folder
gog drive ls --account your-email@gmail.com --query "'<folder-ID>' in parents"

# Recently modified files
gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-01'" --max 10
```

**Main MIME types:**

| Google Format | MIME Type |
|-----------|-----------|
| Google Docs | `application/vnd.google-apps.document` |
| Google Sheets | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Folder | `application/vnd.google-apps.folder` |

**Expected result**: File IDs, file names, MIME types, and last modified dates are listed.

---

## 🚀 Step 2: Download Files

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: File download",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:

Download using the file IDs obtained in Step 1:

```bash
# Download regular files (PDF, images, etc.)
gog drive download <file-ID> --account your-email@gmail.com --out ./downloads/filename.pdf

# Google Docs → Convert to PDF and download
gog drive download <file-ID> --account your-email@gmail.com --format pdf --out ./downloads/document.pdf

# Google Sheets → Convert to CSV and download
gog drive download <file-ID> --account your-email@gmail.com --format csv --out ./downloads/sheet.csv

# Google Sheets → Convert to Excel and download
gog drive download <file-ID> --account your-email@gmail.com --format xlsx --out ./downloads/sheet.xlsx

# Google Slides → Convert to PPTX and download
gog drive download <file-ID> --account your-email@gmail.com --format pptx --out ./downloads/slides.pptx
```

**Export format list:**

| Google Format | Exportable Formats |
|-----------|---------------------|
| Google Docs | PDF, DOCX, TXT, HTML, EPUB |
| Google Sheets | CSV, XLSX, PDF, TSV |
| Google Slides | PPTX, PDF, TXT |

**Expected result**: Files are downloaded to the specified output location.

> **💡 Hint**: Google format files (Docs/Sheets/Slides) cannot be downloaded directly, so you need to specify the conversion format with `--format`.

---

## 🚀 Step 3: Upload Files

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: File upload",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:

Upload local files to Google Drive:

```bash
# Create test file
echo "This is a gogcli upload test." > /tmp/test-upload.txt

# Upload file (to root folder)
gog drive upload /tmp/test-upload.txt --account your-email@gmail.com

# Upload to a specific folder
gog drive upload /tmp/test-upload.txt --account your-email@gmail.com --parent <folder-ID>

# Upload multiple files (ask AI)
# Enter the following prompt in Cursor:
```

**Advanced: Batch upload using AI**
```text
Please upload all PNG files in the output/ folder to a specific Google Drive folder.
Account: your-email@gmail.com
Folder ID: <folder-ID>
Please use the gogcli drive upload command.
```

**Expected result**: Files are uploaded to Google Drive and file IDs are returned. You can verify on the Google Drive web page.

---

## ⚠️ Common Issues and Solutions

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "File list is empty"},
      {"id": "trouble_2", "label": "Download results in error"},
      {"id": "trouble_3", "label": "Upload fails"},
      {"id": "trouble_4", "label": "Do not know how to find folder ID"}
    ]
  }]
}
```

### Issue 1: "File list is empty"
**Cause**: Query conditions are too strict, or viewing a drive without access permissions
**Solution prompt**:
```text
First try gog drive ls --account <email> --max 5 without any conditions.
Files in shared drives may not be displayed by default.
```

### Issue 2: "Download results in error"
**Cause**: --format not specified for Google format files
**Solution prompt**:
```text
For Google Docs/Sheets/Slides, you need to specify the conversion format with --format.
Example: --format pdf (PDF conversion)
Example: --format csv (CSV conversion)
```

### Issue 3: "Upload fails"
**Cause**: File path is incorrect, or file size is too large
**Solution prompt**:
```text
Verify that the file path is correct: ls -la <file-path>
Large files (hundreds of MB or more) may time out.
```

### Issue 4: "Do not know how to find folder ID"
**Cause**: Does not know how to get the folder ID
**Solution prompt**:
```text
Method 1: Get folder list with gog drive ls (items with MIME type folder)
gog drive ls --account <email> --query "mimeType='application/vnd.google-apps.folder'"

Method 2: Open the folder in the Google Drive web page. The end of the URL is the folder ID.
https://drive.google.com/drive/folders/<this-is-the-folder-ID>
```

---

## ✅ Checkpoint
- [ ] Was able to list files in Drive
- [ ] Was able to search by file name and MIME type
- [ ] Was able to download files (including Google format conversion downloads)
- [ ] Was able to upload files


---

## 📋 Output Preview

The deliverable for this lesson is terminal output.

### Expected Output
```text
┌─────────────────────────────────────┐
│  Command execution result              │
│  Status: ✅ Success                     │
│  Items processed: N                     │
└─────────────────────────────────────┘
```

> Tip: To save output to a file, append ` > output/result.txt` to the end of the command

---

## ✅ Completion Check
Paste the following into Codex chat to verify completion:

```text
Run the following gogcli commands to verify that Drive operations work correctly:
1. gog drive ls --account <your-email> --max 5
2. Select one item from the results above and download with gog drive download
3. Verify that the downloaded file exists (ls -la)
Confirm that everything works correctly.
```

**Expected result**: File listing and download complete without errors.

---

## 🎉 Next Steps

Google Drive operations are now complete! In the next lesson, you will learn Google Sheets operations.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/start-4-6)"},
      {"id": "next_window", "label": "Start in new window (/start-4-6)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /start-4-6（Google Sheets Operations)
- next_window → Open new window with /start-4-6
- finish → End
