---
name: lp-designer
description: "LP/HP creation workflow. Guides the full flow from hearing → messaging → wireframe → Pencil design → HTML implementation → Vercel deploy. Triggered by requests like 'create an LP', 'landing page creation', 'HP design', 'web page production', etc."
triggers:
  - create an LP
  - create a landing page
  - I want to make an HP
  - homepage production
  - create a web page
  - lp-designer
  - landing page
---

# LP/HP Designer - Landing Page & Homepage Production Skill

An integrated workflow skill for producing LP (Landing Page) / HP (Homepage) from scratch.
Complete in 6 phases from hearing via AskQuestionTool to Vercel deployment.

## Trigger Phrases

- "Create an LP", "Create a landing page"
- "I want to make an HP", "Homepage production"
- "Create a web page", "I want to make a site"
- "Design with Pencil and implement"

## Prerequisites

- ai-agent-camp is open in Cursor IDE
- Pencil MCP is enabled (for .pen file operations)
- Node.js 18+ is installed (for Vercel deployment)
- Gemini API key is configured (for diagram-generator)

## Workflow Overview

```
Phase 1: Hearing (AskQuestion)
    | Service overview, target, messaging axis
Phase 2: Messaging Organization
    | Persona, benefits, copy
Phase 3: WF Creation
    | ASCII WF + Visual WF
Phase 4: Pencil Design
    | .pen design file
Phase 5: Code Implementation
    | HTML/CSS(Tailwind)/JS
Phase 6: Vercel Deploy
    | Public URL
```

---

## Phase 1: Hearing (AskQuestion)

First, use AskQuestionTool to structurally collect requirements for the LP/HP to be created.

### Step 1-1: Project Type Confirmation

```json
{
  "title": "LP/HP Production Hearing",
  "questions": [{
    "id": "project_type",
    "prompt": "What type of page do you want to create?",
    "options": [
      {"id": "lp", "label": "LP (Landing Page) - Focused on a single CTA"},
      {"id": "hp", "label": "HP (Homepage) - Multiple sections with navigation"},
      {"id": "product", "label": "Product Page - Feature-focused"},
      {"id": "event", "label": "Event/Campaign Page"}
    ]
  }]
}
```

### Step 1-2: Service/Product Information

```json
{
  "title": "Service Information",
  "questions": [
    {
      "id": "service_category",
      "prompt": "Select the service category",
      "options": [
        {"id": "saas", "label": "SaaS / Web Service"},
        {"id": "ec", "label": "E-commerce / Retail"},
        {"id": "consulting", "label": "Consulting / Professional Services"},
        {"id": "education", "label": "Education / School"},
        {"id": "event", "label": "Event / Seminar"},
        {"id": "portfolio", "label": "Portfolio / Personal"},
        {"id": "other", "label": "Other"}
      ]
    },
    {
      "id": "design_tone",
      "prompt": "Select the design tone",
      "options": [
        {"id": "professional", "label": "Professional / Trustworthy"},
        {"id": "modern", "label": "Modern / Stylish"},
        {"id": "playful", "label": "Pop / Friendly"},
        {"id": "luxury", "label": "Luxury / Elegant"},
        {"id": "minimal", "label": "Minimal / Simple"},
        {"id": "tech", "label": "Tech / Advanced"}
      ]
    }
  ]
}
```

### Step 1-3: Additional Hearing (Free Input)

After AskQuestion, confirm the following via free input:

- **Service name**: Official name
- **Tagline ideas**: If any (otherwise generate)
- **Target**: Who is the page for
- **Key selling points**: About 3
- **Reference sites**: URLs if any
- **CTA purpose**: Inquiry / Sign up / Request materials / Purchase, etc.

---

## Phase 2: Messaging Organization

Generate the following document based on Phase 1 hearing results.

### Output: `output/lp-brief.md`

```markdown
# LP Brief

## Persona
- Name: {e.g.: John Smith}
- Age: {e.g.: 35}
- Occupation: {e.g.: Marketing Manager}
- Challenge: {e.g.: LP creation takes too long}

## Messaging Axis (3 Benefits)
1. {Main benefit}
2. {Sub benefit 1}
3. {Sub benefit 2}

## Copy
- Headline: {e.g.: Create LPs 10x Faster with AI}
- Subheadline: {e.g.: AI supports everything from hearing to deployment}
- CTA text: {e.g.: Start for Free}

## Section Structure
1. Hero (Headline + CTA)
2. Pain Points (Problem statement)
3. Solution (Solution introduction)
4. Features (Features / highlights 3-4 items)
5. Social Proof (Results / Testimonials)
6. Pricing / Plan (Pricing/plans) *Optional
7. FAQ (Frequently asked questions)
8. Final CTA (Final action)
```

---

## Phase 3: WF (Wireframe) Creation

### Step 3-1: ASCII Wireframe

Design the structure of each section in text-based format:

```
+----------------------------------+
|           HEADER / NAV           |
+----------------------------------+
|                                  |
|     [Hero Image / Video]         |
|                                  |
|     Headline (H1)               |
|     Subheadline                  |
|     [ CTA Button ]              |
|                                  |
+----------------------------------+
|     Pain Points Section          |
|   +------+ +------+ +------+    |
|   |Pain 1| |Pain 2| |Pain 3|    |
|   +------+ +------+ +------+    |
+----------------------------------+
|     Solution Section             |
|   [Image]  Description text      |
+----------------------------------+
|     Features Section             |
|   +-------+ +-------+           |
|   |Feat 1 | |Feat 2 |           |
|   +-------+ +-------+           |
|   +-------+ +-------+           |
|   |Feat 3 | |Feat 4 |           |
|   +-------+ +-------+           |
+----------------------------------+
|     Social Proof                 |
|     ***** Testimonials           |
+----------------------------------+
|     FAQ                          |
|     Q1 / A1                      |
|     Q2 / A2                      |
+----------------------------------+
|     Final CTA                    |
|     [ CTA Button ]              |
+----------------------------------+
|           FOOTER                 |
+----------------------------------+
```

### Step 3-2: Visual WF Generation

Generate a visual wireframe using diagram-generator:

```bash
uv run python tools/generate_diagram.py --topic "LP wireframe: {section structure}" --style minimalist
```

Output: `output/images/lp-wireframe.png`

---

## Phase 4: Pencil Design

Create .pen design files using Pencil MCP.
Since .pen files are encrypted, always use Pencil MCP tools instead of Read/Grep.

### Step 4-0: Open Pencil Editor

First check the current editor state. Create a new file if none is open.

```
# 1) Check editor state
CallMcpTool: user-pencil / get_editor_state
  arguments: {}

# -> Returns error if no file is open
# -> Returns node list if a file is already open

# 2-A) Create a new document
CallMcpTool: user-pencil / open_document
  arguments: { "filePathOrTemplate": "new" }

# 2-B) Open an existing .pen file
CallMcpTool: user-pencil / open_document
  arguments: { "filePathOrTemplate": "path/to/design.pen" }

# 3) After opening, check node structure again with get_editor_state
CallMcpTool: user-pencil / get_editor_state
  arguments: {}
```

**Important**: `open_document` is an operation to open the target file within the Pencil app.
`user-pencil` must be enabled in Cursor's MCP settings.

### Step 4-1: Get LP Design Guidelines

Retrieve LP-specific design rules (section structure, hero design, footer design, etc.):

```
CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "landing-page" }
```

These guidelines include:
- Recommended section structure for SaaS/LP (Hero -> Features -> Social Proof -> Pricing -> FAQ -> CTA -> Footer)
- Hero section best practices
- Content-before-visual ordering principle
- Page container creation examples with batch_design

### Step 4-2: Get Style Guide

Retrieve a style guide matching the design tone:

```
# 1) Check available tags
CallMcpTool: user-pencil / get_style_guide_tags
  arguments: {}

# -> Returns tags like minimal, modern, clean, warm, tech, brutalist, etc.

# 2) Select tags matching the hearing result tone
CallMcpTool: user-pencil / get_style_guide
  arguments: { "tags": ["minimal", "clean", "whitespace", "website"] }
```

The style guide includes:
- Color system (background, text, accent colors)
- Typography (font, size, weight)
- Spacing, border-radius, shadow values
- Component patterns (buttons, cards, nav, etc.)

### Step 4-3: Create Page Container

Create a frame wrapping the entire LP with `batch_design`:

```
# batch_design operations are written in script format
CallMcpTool: user-pencil / batch_design
  arguments: {
    "operations": "page=I(document, {type: \"frame\", name: \"Landing Page\", placeholder: true, layout: \"vertical\", width: 1440, height: \"fit_content(4000)\", fill: \"#FFFFFF\", clip: true})"
  }
```

**batch_design operation basic syntax:**

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Insert | `foo=I("parentId", {...})` | Insert child into parent node |
| Copy | `bar=C("nodeId", "parentId", {...})` | Copy a node |
| Update | `U("nodeId", {...})` | Update properties |
| Replace | `R("nodeId", {...})` | Replace a node |
| Delete | `D("nodeId")` | Delete a node |
| Move | `M("nodeId", "parentId", index)` | Move a node |
| Image | `G("nodeId", "ai", "prompt")` | AI image generation |

**Important rules:**
- Always set `placeholder: true` on frames in progress, set to `false` when complete
- Always set `fill` on text (default is transparent and invisible)
- Maximum 25 operations per batch_design call
- `x`, `y` are ignored for flexbox children (use `fill_container` / `fit_content`)
- There is no image node type. Apply images to frames with `G()`

### Step 4-4: Create Sections Sequentially

Create the following sections 1-2 at a time using `batch_design`:

1. **Header**: Logo + nav links + CTA button (horizontal layout `space_between`)
2. **Hero Section**: Badge, headline, subheadline, CTA button (center-aligned)
3. **Features**: Section header + 3-column cards (icon + title + description)
4. **How It Works**: Numbered 3-step process (circled numbers + title + description)
5. **Stats/Social Proof**: Dark background stats + customer testimonial cards
6. **Final CTA**: Accent color background + headline + CTA button
7. **Footer**: Dark background + link columns + copyright

Example of creating each section (Hero):

```
CallMcpTool: user-pencil / batch_design
  arguments: {
    "operations": "hero=I(\"pageId\", {type: \"frame\", name: \"Hero\", layout: \"vertical\", width: \"fill_container\", height: \"fit_content(600)\", padding: [100, 120], gap: 32, alignItems: \"center\", fill: \"#FFFFFF\"})\nheadline=I(hero, {type: \"text\", content: \"Main Copy\", fontFamily: \"Outfit\", fontSize: 56, fontWeight: \"700\", fill: \"#1A1918\", letterSpacing: -1, textAlign: \"center\", lineHeight: 1.2, textGrowth: \"fixed-width\", width: 800})\nsubline=I(hero, {type: \"text\", content: \"Subheadline description\", fontFamily: \"Outfit\", fontSize: 18, fill: \"#6D6C6A\", textAlign: \"center\"})"
  }
```

### Step 4-5: Design Review & Fine-tuning

After adding each section, visually confirm with screenshots:

```
# Review entire page
CallMcpTool: user-pencil / get_screenshot
  arguments: { "nodeId": "pageId" }

# Zoom in on specific section
CallMcpTool: user-pencil / get_screenshot
  arguments: { "nodeId": "heroId" }

# Check layout structure numerically (effective for detecting misalignment)
CallMcpTool: user-pencil / snapshot_layout
  arguments: { "parentId": "pageId", "maxDepth": 3 }
```

Fix issues with `batch_design` `U()`.
Once all sections are complete, release the placeholder:

```
CallMcpTool: user-pencil / batch_design
  arguments: { "operations": "U(\"pageId\", {placeholder: false})" }
```

---

## Phase 5: Code Implementation

Convert the Pencil design into working HTML/CSS/JS.

### Step 5-1: Get Coding Guidelines

```
CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "code" }

CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "tailwind" }
```

### Step 5-2: Project Structure

```
lp-project/
├── index.html          # Main HTML
├── css/
│   └── style.css       # Custom CSS (using Tailwind CDN)
├── js/
│   └── main.js         # Interactions
├── images/             # Image assets
└── package.json        # For Vercel deployment
```

### Step 5-3: Implementation Points

- **Tailwind CSS CDN**: Use immediately with `<script src="https://cdn.tailwindcss.com"></script>`
- **Responsive**: Implement mobile-first (sm: / md: / lg: breakpoints)
- **Animations**: Intersection Observer for elements fading in on scroll
- **Forms**: External service integration like Formspree or Netlify Forms

### Step 5-4: Browser Check

Check display using cursor-ide-browser MCP:

```
CallMcpTool: cursor-ide-browser / browser_navigate
  arguments: { "url": "file:///path/to/lp-project/index.html" }
```

---

## Phase 6: Vercel Deploy

### Step 6-1: Install Vercel CLI

```bash
npm i -g vercel
```

### Step 6-2: Preview Deploy

```bash
vercel lp-project
```

Login and project configuration are required the first time.

### Step 6-3: Production Deploy

```bash
vercel --prod
```

### Step 6-4: Custom Domain (Optional)

```bash
vercel domains add your-domain.com
```

---

## 3 Levels of Experience

This skill can be used at three levels:

### Stage 1: Text-Based LP (Beginner)
- Hearing with AskQuestion
- Structure design with ASCII WF
- Generate HTML/CSS directly (without Pencil)
- Check locally

### Stage 2: HP Production (Intermediate)
- Multi-page structure (top + sub-pages)
- Navigation implementation
- Visual WF with diagram-generator
- Responsive support

### Stage 3: Pencil Design → LP (Advanced)
- Create professional designs with Pencil MCP
- Design-to-code conversion
- Animations & interactions
- Publish with Vercel deploy

---

## Related Skills

- **diagram-generator**: WF and structure diagram generation
- **nanobanana**: Hero image and OGP image generation
- **banner-creator**: Banner creation for social media announcements
- **screenshot-annotator**: Adding annotations for design review
