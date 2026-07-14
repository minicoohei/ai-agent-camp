---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-4"]
duration: "~30 min"
level: "intermediate"
tags: ["notion", "mcp", "files", "attachments"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 12-5: Notion and Slack Integration

## 📍 What You'll Do

**Lesson 12-5** !

| Item | Details |
|------|------|
| Goal | Identify **file blocks, attachments, and exportable URLs** on Notion, enabling the agent to **verify content and display it clearly to the user** |
| Duration | ~30 min |
| Skills used | Notion MCP (page/block retrieval), official API as needed |
| Prerequisites | `/start-12-4` completed, with access to the target page |
| Course page | [Module 12: Notion](https://ai-agent.camp/en/course/module-12)  alongside this lesson |

**Session flow:**
1. Identify blocks containing **files / PDFs / images** from the target page's block list
2. Choose the **retrievable format** (text extraction, temporary URL, local save) available via the MCP or API in use
3. Do not paste binary directly in chat; return as **file name, type, summary, and reference link**

By the end of this session, you will be able to reproduce the flow: "Where is the file -> How to retrieve it -> How to present it to the user".

> **Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume.

> **Secret information**: Do not paste download URLs or tokens raw in logs or chat.

---

## 🎯 Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Do you have a Notion page with file attachments ready?",
    "options": [
      {"id": "ready", "label": "Ready"},
      {"id": "need_page", "label": "I want to create a test page"},
      {"id": "skip_practice", "label": "Just review the procedure"}
    ]
  }]
}
```

---

## 🚀 Step 1: Identify File Blocks

The agent performs the following:

1. Confirm the **page URL or page ID** from the user
2. Traverse blocks with MCP / `retrieve block children` etc., and list blocks corresponding to `type: file` or embeds
3. Return a short list of "file name, block type" to the user

**Prompt examples for the user:**
```text
Please list all file attachments in this Notion page,
and add a brief note for each on how to retrieve it (via MCP or open in browser).
Page: <URL>
```

---

## 🚀 Step 2: Retrieve and Verify Locally

1. Follow the MCP tool instructions to attempt **file content retrieval** or **saving to the user's local machine**
2. If the tool returns binary only, report just the **file size and hash**, leaving the opening procedure to the user
3. If convertible to text/Markdown, extract only the **first few hundred characters** and headings

---

## 🚀 Step 3: "Display" in Chat

**Required rules:**
- Images: When possible, show `![](URL)` or file paths **briefly** (avoid large base64)
- PDF: Summary at page count/table of contents level only (full-text OCR only when user explicitly requests)
- Include "which file" and "how far it was read" in the **completion report**

---

## ✅ Completion Criteria

- [ ] Can explain the retrieval path for at least one file attachment
- [ ] Converted to a readable format in chat (summary/links)
- [ ] Did not paste URLs containing secrets directly in public chat
