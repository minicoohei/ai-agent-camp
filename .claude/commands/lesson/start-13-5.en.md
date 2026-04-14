---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-4"]
duration: "~15 min"
level: "intermediate"
tags: ["lp", "vercel", "deploy", "hosting"]
---

# 🎓 Lesson 13-5: Vercel Deploy

## 📍 What You'll Do

Welcome to **Lesson 13-5: Vercel Deploy**!

| Item | Details |
|------|---------|
| Goal | Deploy the created Landing Page/Website to Vercel and obtain a public URL |
| Duration | ~15 min |
| Skills Used | lp-designer, Vercel CLI |
| Prerequisites | Lesson 13-4 complete (`output/lp-project/` exists). If not complete, a sample project will be generated as a fallback |
| Course Page | Refer to [Module 13: Landing Page/Website Design](https://ai-agent.camp/en/course/module-13) in parallel |

> **⚠️ Note for non-interactive environments (Codex, CI, etc.)**: `vercel login` requires browser authentication and cannot be run in non-interactive environments. In that case, use token authentication via the `VERCEL_TOKEN` environment variable, or skip the deploy step.

**Session flow:**
1. Check project existence (generate sample if missing)
2. Install and authenticate Vercel CLI
3. Preview deploy
4. Verify in browser
5. Production deploy

By the end of this session, the Landing Page will be published at a URL accessible worldwide.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

First, let's confirm everything is ready.

**AskQuestion settings:**
```json
{
  "title": "🎯 Pre-Session Check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Proceed to Step 0)
(check_prereq → Check Node.js, npm existence + Lesson 13-4 completion)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🔍 Step 0: Check Project Existence

Verify that the 13-4 deliverable (`output/lp-project/`) exists.

**Verification steps:**
```bash
# Check if output/lp-project directory exists
ls output/lp-project/index.html 2>/dev/null && echo "OK: Project exists" || echo "NOT FOUND: Project not found"
```

**Fallback if project doesn't exist:**

If `output/lp-project/` doesn't exist, either complete 13-4 first, or use the following minimal sample project as an alternative.

```bash
# Generate sample project
mkdir -p output/lp-project
cat > output/lp-project/index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sample LP - Vercel Deploy Practice</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <header class="bg-blue-600 text-white py-16 text-center">
    <h1 class="text-4xl font-bold mb-4">Sample LP</h1>
    <p class="text-xl">This is a practice page for Vercel deployment</p>
  </header>
  <main class="max-w-3xl mx-auto py-12 px-4">
    <section class="bg-white rounded-lg shadow p-8 mb-8">
      <h2 class="text-2xl font-bold mb-4">About This Page</h2>
      <p class="text-gray-700">This is a sample page auto-generated for 13-5 Vercel deploy practice. Complete 13-4 to deploy your actual Landing Page.</p>
    </section>
  </main>
  <footer class="bg-gray-800 text-gray-400 py-6 text-center">
    <p>&copy; 2026 AI Agent Training</p>
  </footer>
</body>
</html>
HTMLEOF
echo "Sample project generated in output/lp-project/"
```

> **Recommended**: Ideally, use the Landing Page created in 13-4 (`/start-13-4`). The sample is for deployment procedure practice.

**Expected result**: `output/lp-project/index.html` exists.

---

## 🚀 Step 1: Install and Authenticate Vercel CLI

Install and log in to Vercel CLI.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Vercel CLI Setup",
  "questions": [{
    "id": "vercel_status",
    "prompt": "What is the Vercel CLI status?",
    "options": [
      {"id": "not_installed", "label": "Not installed yet"},
      {"id": "installed", "label": "Installed (already logged in)"},
      {"id": "installed_no_login", "label": "Installed (not logged in)"},
      {"id": "no_account", "label": "I don't have a Vercel account"}
    ]
  }]
}
```

**Post-selection instructions (not_installed)**:
Input:
```text
Install and log in to Vercel CLI.

Steps:
1. Install
   npm i -g vercel

2. Verify version
   vercel --version

3. Log in (Method A: Browser authentication - interactive environments only)
   vercel login

   A browser will open - log in with your Vercel account.
   If you don't have an account, create one free at https://vercel.com/signup.

4. Verify login
   vercel whoami
```

**Post-selection instructions (installed_no_login)**:

> **⚠️ For non-interactive environments (Codex, CI, SSH, etc.)**: `vercel login` requires a browser and cannot be run. Use "Method B: Token authentication" below.

Input:
```text
■ Method A: Browser authentication (local environment)
  vercel login
  → A browser will open for authentication

■ Method B: Token authentication (non-interactive environments / CI)
  1. Go to https://vercel.com/account/tokens
  2. Click "Create Token" to generate a token (any name, e.g., "aiagent-deploy")
  3. Set as environment variable:
     export VERCEL_TOKEN="your-generated-token"

  4. Persist in .env (optional):
     Open the .env file directly in a text editor and add VERCEL_TOKEN=your-generated-token.

     > **Security note**: Appending via command like `echo 'VERCEL_TOKEN=...' >> .env` risks leaving the token in shell history. Direct editing with a text editor is recommended.

  5. Deploy with token authentication:
     vercel --token "$VERCEL_TOKEN"
     vercel --prod --token "$VERCEL_TOKEN"

■ Verify login:
  vercel whoami
  # For token auth: vercel whoami --token "$VERCEL_TOKEN"
```

**Post-selection instructions (no_account)**:
```text
Create a Vercel account:

1. Go to https://vercel.com/signup
2. Register with your GitHub account or email (free plan)
3. After registration, run vercel login in the terminal
   (For non-interactive environments, generate a token at https://vercel.com/account/tokens)
```

**Expected result**: Vercel CLI is installed and authenticated.

---

## 🚀 Step 2: Preview Deploy

First, deploy to a preview environment for verification.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Preview Deploy",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Deploy the Landing Page project to Vercel as a preview.

■ Method A: Interactive (local environment)
1. Navigate to the project directory
   cd output/lp-project

2. Run Vercel deploy
   vercel

   Set the following interactively:
   - Set up and deploy? → Y
   - Which scope? → Select your account
   - Link to existing project? → N
   - Project name? → my-lp (any name)
   - In which directory is your code located? → ./
   - Override settings? → N

3. After deployment completes, a preview URL will be displayed
   Example: https://my-lp-xxxxx.vercel.app

■ Method B: Non-interactive mode (CI/Codex environments, or token auth)
1. Navigate to the project directory
   cd output/lp-project

2. Deploy with --yes flag to skip prompts
   vercel --yes --token "$VERCEL_TOKEN"

   ※ If VERCEL_TOKEN is not set, refer to Step 1's token authentication instructions

3. After deployment completes, a preview URL will be displayed

Record the displayed preview URL.
```

> **⚠️ If you get a `~/.vercel` not found error**: It will be auto-created on the first deploy. If the error persists, run `mkdir -p ~/.vercel`.

**Expected result**: A preview URL is obtained.

---

## 🚀 Step 3: Verify in Browser

Check the preview URL in a browser.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Preview Verification",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Open the preview URL in a browser and verify.

Verification items:
1. Does the page display correctly?
2. Are images and fonts loaded?
3. Does responsive layout work correctly? (Try resizing the browser)
4. Do animations work?
5. Do links and buttons function?

Verify with cursor-ide-browser MCP:
Navigate to the preview URL with browser_navigate,
and take a screenshot with browser_snapshot.

If there are issues, fix the code and redeploy with vercel.
```

**Expected result**: The Landing Page displays correctly in the preview environment.

---

## 🚀 Step 4: Production Deploy

If everything looks good, deploy to production.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Production Deploy",
  "questions": [{
    "id": "deploy_action",
    "prompt": "Deploy to production?",
    "options": [
      {"id": "deploy_prod", "label": "Deploy to production"},
      {"id": "fix_first", "label": "Fix first, then deploy to production"},
      {"id": "skip_prod", "label": "Preview only, finish here"},
      {"id": "custom_domain", "label": "I also want to set up a custom domain"}
    ]
  }]
}
```

**Post-selection instructions (deploy_prod)**:
Input:
```text
Deploy to production.

Steps:
1. Run production deploy
   cd output/lp-project
   vercel --prod
   # For token auth: vercel --prod --token "$VERCEL_TOKEN"

2. A production URL will be displayed
   Example: https://my-lp.vercel.app

3. Final verification on production URL
   - Page load speed
   - OGP image (preview when sharing on social media)
   - Mobile display

Record the production URL.
```

**Post-selection instructions (custom_domain)**:

> **Note**: Custom domain setup is optional. Only proceed if you own a custom domain. Publishing with Vercel's free subdomain (*.vercel.app) is also possible.

Input:
```text
Set up a custom domain (only if you own a custom domain).

Steps:
1. Add domain
   vercel domains add your-domain.com

2. DNS settings (configure on your domain provider's side)
   - Type: CNAME
   - Name: @ or www
   - Value: cname.vercel-dns.com

3. SSL certificate (auto-issued)
   Vercel will automatically issue a Let's Encrypt certificate.

4. Verify settings
   vercel domains inspect your-domain.com
```

**Expected result**: The Landing Page is published at a production URL.

---

## ⚠️ Common Issues and Solutions

In Codex, you typically present choices in chat so the user can select their issue and get guidance instantly.

**AskQuestion settings example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "vercel command not found"},
      {"id": "trouble_2", "label": "Cannot log in"},
      {"id": "trouble_3", "label": "Deploy errors"},
      {"id": "trouble_4", "label": "Page is blank white"}
    ]
  }]
}
```

### Issue 1: vercel command not found
**Solution**: Install globally with `npm i -g vercel`. If that doesn't work, try running with `npx vercel`.

### Issue 2: Cannot log in
**Solution**: Try token-based login with `vercel login --token <token>`. You can generate a token at https://vercel.com/account/tokens.

### Issue 3: Deploy errors
**Solution**: Check the error message. Common causes:
- File size limit exceeded → Compress images
- package.json syntax error → Check JSON format
- Build error → Re-verify it works locally

### Issue 4: Page is blank white
**Solution**: Check the root directory setting for the deploy target. Verify you specified `./` for `In which directory is your code located?` when running the `vercel` command.

---

## ✅ Checkpoint
- [ ] Deployable project exists at `output/lp-project/`
- [ ] Vercel CLI is installed
- [ ] Logged in to Vercel (browser auth or token auth)
- [ ] Preview deploy succeeded
- [ ] Landing Page displays correctly at preview URL
- [ ] Production deploy is complete (optional)


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/lp/
├── index.html  (Landing Page)
├── style.css
└── assets/
```

### Verification Commands
```bash
# File list
ls -lh output/lp/

# Open in browser (macOS: open / Linux: xdg-open)
open output/lp/index.html
```

> 💡 Check HTML structure: `head -30 output/lp/index.html`

---

## ✅ Completion Check
Enter the following in the Codex chat to verify completion:

```bash
Display the current deploy list with vercel ls,
and check the URL, status, and creation date of the latest deploy.
# For token auth: vercel ls --token "$VERCEL_TOKEN"
```

**Expected result**: Deploy list and URLs are displayed.

---

## 🎉 Congratulations!

You have completed all lessons in Module 13!

### Skills Acquired
1. **Value Proposition Design**: Persona definition, benefit organization, copywriting
2. **Wireframe**: ASCII WF, visual WF, information architecture
3. **Pencil Design**: Professional-quality design creation using MCP
4. **Frontend Implementation**: Landing Page building with HTML/CSS(Tailwind)/JS
5. **Deployment**: Instant publishing with Vercel

### 3-Stage Experience Summary
- **Stage 1**: Text → HTML direct Landing Page creation (13-1, 13-2, 13-4)
- **Stage 2**: More complex website building (practiced in applied exercises)
- **Stage 3**: Pencil → Code conversion (13-3 → 13-4)

---

## ➡️ Next Steps

All sections are now complete. Select what to do next.

In Codex, you can typically select from choices in chat.

**AskQuestion settings example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-14-1)"},
      {"id": "course_top", "label": "Open course top (ai-agent.camp)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-1 in a new window
- course_top → Open https://ai-agent.camp/en/course in browser
- finish → End
