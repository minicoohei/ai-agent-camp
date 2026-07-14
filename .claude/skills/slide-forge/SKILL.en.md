---
name: slide-forge
version: 1.1.0
description: "A skill that assembles a well-formatted proposal slide deck (self-contained HTML, 16:9) from an outline or research findings. Use it for requests like \"turn this into slides,\" \"build a proposal deck,\" \"make a slide deck,\" or \"slide forge.\""
triggers:
  - turn this into slides
  - build a proposal deck
  - make a slide deck
  - put this together into a deck
  - slide forge
  - make slides
  - turn this into a slide deck
  - create a presentation
---

# Slide Forge — Forging Slides from an Outline

A skill that turns an outline or research findings into a self-contained HTML slide deck ready to project or share as-is. Rather than designing each slide individually, the key is to **pour content into a shared template**, which automatically keeps the overall look and feel consistent.

## Overview

- The default output format is **self-contained HTML (16:9, 1280×720)**. It has no dependency on external CDNs (JS/CSS libraries loaded from another server on the internet), external images, or external fonts — meaning the file displays correctly just by opening it, even in an environment with no internet connection
- Strictly one message per slide, to prevent overcrowding
- Define the header (chapter label + title) and footer (project name, page number) shared across all pages first, then pour in the content

## About the Skill Name

This skill is named as a general-purpose skill rather than one dedicated to a specific project. If a skill with the same name `slide-forge` already exists under a different definition in the environment, check for its presence when installing; if it doesn't exist, add this one as-is, and if it does exist, treat the contents of this SKILL.md as authoritative and overwrite/merge it (to avoid ambiguous trigger routing caused by duplicate registrations).

Note: the slide-forge covered in this repo's course lesson03 ("module29-slide-forge") is a **different** thing — the external OSS `github.com/minicoohei/slide-forge` (a Python CLI that generates editable PPTX and other formats). This skill is a lightweight variant that quickly builds a self-contained HTML deck from an outline; typing `/slide-forge` triggers this skill (not the lesson's Python CLI). When you need editable PPTX or multi-format output, follow the lesson's steps.

## Use Cases

Concrete scenarios where this skill is effective:

1. **Research findings → proposal deck**: When you want to format research/analysis results (sourced facts and figures) into proposal slides for decision-makers
2. **Outline → HTML for projection**: When an outline (chapter structure, key messages) already exists and you want to turn it into slides with a consistent look
3. **Unifying the look of existing notes/documents**: When you want to reorganize inconsistently formatted notes or bullet lists into slides using a unified template
4. **Mass-producing multilingual slide versions**: When you want to create multiple slide sets in different languages from the same outline and template
5. **Lightweight internal decks**: When you want slides that can be shown immediately on the spot without opening PowerPoint
6. **Proposal decks with photos/chart images**: When you want to include product photos or chart images (images are embedded in the HTML as base64 data URIs, with no external references created)

**Cases where this is not a good fit (out of scope)**:
- A PPTX that needs elaborate animations or slide-transition effects (→ if explicitly requested, consider a separate PPTX conversion; HTML is the default)
- A single standalone diagram or infographic (→ the `diagram-generator` skill is a better fit)
- Cases where you want to directly edit an existing PowerPoint/Google Slides template as-is
- Interactive dashboards or filterable reports that handle large volumes of data (→ the `interactive-dashboard-builder` skill is a better fit)
- Stages where sourced facts/figures aren't ready yet (→ if a fact-checking skill such as `ycp-research-factcheck` exists in the environment, complete research/fact-checking with it first; otherwise, verify sources yourself before using this skill)
- A large number of slides (roughly 50+) or a long deck spanning multiple sections (→ a single file becomes bloated and hard to maintain, so split files by chapter or reduce the slide count before using this skill)

## Workflow

1. **Confirm inputs and storage conventions**
   First, confirm the deal/project name (used in the file name) with the user. If an outline file exists (follow the project's convention, e.g. `outline/proposal.md`), use it. If not, either gather the information on the spot, or, if an outline-creation skill such as `ycp-proposal-outline` exists in the environment, use it to build the outline first before proceeding. When using figures or facts, reference sourced research findings (follow the project's convention, e.g. `research/<theme>/findings.md`). For projects with no established storage convention, confirm the output destination to be used in step 4 with the user at this point
2. **Define the shared template** (self-contained within a single file's CSS)
   - Fixed 16:9 (1280×720); one section = one slide
   - Common to every slide: header at the top (chapter label + title) / footer at the bottom (project name, page number)
   - Limit the color palette to two colors plus grayscale shades. Unless otherwise specified, default to navy (#1F3A5F) as the main color and orange (#E8833A) as the accent color, with body text in gray (#333333/#666666). If the project's brand colors are known, prefer those instead
   - Use system fonts (loading external fonts is prohibited). Default the body font size to 18px or larger
   - For any slide that cites figures or facts, note the source (media name and date, or a footnote number) in small text of roughly 8px directly below the relevant content
   - When using images, embed them in the HTML as base64 data URIs (external file references and external URLs are prohibited). If embedding would make the file excessively large, compress the image before embedding
3. **Build one message per slide**
   - The title line = the key message (a single declarative sentence). Descriptive headings like "About X" are prohibited
     - Bad example: "About Market Trends"
     - Good example: "The Domestic Market Will Grow 1.5x Over the Next Three Years"
   - Keep the body to at most 4 bullet points (each bullet should be roughly no more than 40 full-width Japanese characters, or the equivalent length in English), or a single diagram. Don't overcrowd
   - For any slide requiring a diagram, reserve a diagram area in the center (a placeholder is acceptable; structure it so an image can be inserted later, and set alt text)
4. **Produce the output**
   Save it as self-contained HTML (with no dependency on external CDNs, external images, or external fonts) following the project's convention (or, if none exists, `output/slides/<project name/theme name>.html`). Make it something that can be projected as-is just by opening it in a browser. When producing multilingual versions, finish and review the default-language version first, then save each language as `<same name>_<language code>.html` (e.g. `_ja.html` / `_en.html`), keeping the template (colors, layout) shared and swapping only the wording. Since text length varies by language, re-check the body's character limit for each language and adjust the wording if anything overflows (do not change the layout itself)
5. **Self-review**
   Double-click the saved HTML file to open it in the default browser, actually check the display slide by slide, and be sure to go through the "Checklist" below before submission

## Checklist (Before Submission)

- [ ] Is each slide **one message** (no two or more claims mixed on a single slide)?
- [ ] **Skimming only the titles**, does the overall story hold together? (How to check: read the title line of every slide aloud in order from top to bottom, and confirm the narrative doesn't suddenly jump around or repeat itself)
- [ ] Are the **header, footer, margins, and colors consistent** across every slide?
- [ ] Does it use **only sourced figures/facts**, and is the source noted on the slide (as a footnote or in the footer)?
- [ ] Is it **self-contained HTML** (no remaining references to external CDNs, external images, or external fonts)?
- [ ] Does it display correctly at **16:9 (1280×720)** without breaking (no text overflow or elements spilling out)?
- [ ] Is the **body font size large enough to read at projection distance** (guideline: body text 18px or larger, each bullet roughly 40 full-width Japanese characters or fewer, or the equivalent in English)?
- [ ] Is there **sufficient contrast between the background color and the text color** (no light gray text on a light background)?
- [ ] Are you **avoiding distinguishing meaning by color alone** (e.g., red = NG / green = OK also indicated by a symbol or label, not color alone)?
- [ ] Do diagram placeholders/images have **alt text** set?
- [ ] Does the save location/file name follow the **project's convention** (or, if none, `output/slides/<name>.html`)?
- [ ] No typos, and no errors in number digits or units (yen/dollars, percent, etc.)?
- [ ] When producing multilingual versions, does any language have **text overflowing, awkward line-break positions, or broken fonts**?

## Notes
- Always keep the output under `output/slides/`. Normalize the file name to alphanumerics, hyphens, and underscores only, and reject inputs containing `..`, a leading slash, or control characters (to prevent writing to unintended locations).

- Only consider PPTX output **when explicitly requested** (HTML is the default)
- Use only figures/facts that appear in sourced research findings. Don't add unsourced numbers as decoration
- Don't start building slides without an outline or sourced data in hand. Gather the inputs first (don't skip step 1 of the Workflow)
