---
nonInteractiveMode: compliant
---

# Slide Forge — Building Slides from an Outline

Creates a well-formatted, self-contained HTML slide deck (16:9) from an outline or research findings. Applies a shared template (header/footer) to every slide, and builds one message per slide. The output defaults to self-contained HTML (with no dependency on external CDNs — JS/CSS libraries loaded from another server on the internet — external images, or external fonts), so the file displays correctly just by opening it, even with no internet connection.

This skill is named as a general-purpose command rather than one dedicated to a specific project. If a `slide-forge` command with the same name already exists under a different definition in the environment, check for its presence when installing; if it doesn't exist, add this one as-is, and if it does exist, treat the contents of this file as authoritative and overwrite/merge it.

## Capabilities

- Takes an outline file (follow the project's convention, e.g. `outline/proposal.md`) and/or research findings (follow the project's convention, e.g. `research/<theme>/findings.md`) as input, and generates self-contained HTML slides with no external dependencies
- Fixes the shared header, footer, colors, and fonts across every page up front, to prevent inconsistencies in appearance
- Never uses unsourced figures or facts
- Embeds images in the HTML as base64 data URIs, creating no external references

## When to Use / Not Use

**Use when**: you want to turn research findings into a proposal deck, turn an outline into HTML for projection, unify the look of existing notes, mass-produce multilingual slide versions, want a lightweight internal deck, or want to build a proposal deck that includes photos/chart images.

**Don't use (consider another approach)**:
- A PPTX that needs elaborate animations or slide transitions (only if explicitly requested, consider a separate PPTX conversion)
- A single standalone diagram or infographic (→ the `diagram-generator` skill is a better fit)
- Cases where you want to directly edit an existing PowerPoint/Google Slides template as-is
- Interactive dashboards or filterable reports that handle large volumes of data (→ the `interactive-dashboard-builder` skill is a better fit)
- Stages where sourced facts/figures aren't ready yet (→ if a fact-checking skill such as `ycp-research-factcheck` exists in the environment, complete it with that first; otherwise, verify sources yourself before using this)
- A large number of slides (roughly 50+) or a long deck spanning multiple sections (→ a single file becomes bloated and hard to maintain, so split files by chapter or reduce the slide count before using this)

## Execution Steps

1. **Extract parameters and confirm the storage destination**
   Extract the following from the user's request.
   - Deal/project name (required; used in the file name)
   - Whether an outline file exists, and its path (follow the project's convention, e.g. `outline/proposal.md`)
   - Whether research findings/sourced data exist, and their path (follow the project's convention, e.g. `research/<theme>/findings.md`)
   - Output destination (if the project has no established convention, confirm this with the user here; otherwise the default is `output/slides/<project name/theme name>.html`)

2. **Confirm the outline**
   If an outline file exists, read its contents. If not, either gather the information from the user, or, if an outline-creation skill such as `ycp-proposal-outline` exists in the environment, use it to organize the chapter structure and key messages first before proceeding. When using figures or facts, check whether sourced research findings exist (if not, tell the user that "numbers without a source can't be used," and, if a fact-checking skill such as `ycp-research-factcheck` exists in the environment, point them to it).

3. **Define the shared template**
   Fix the following within a single file's CSS.
   - Size: fixed 16:9 (1280×720)
   - Shared header: chapter label + title
   - Shared footer: project name, page number
   - Colors: limit to two colors plus grayscale shades. Default to navy (#1F3A5F) as the main color and orange (#E8833A) as the accent color, with body text in gray (#333333/#666666). Prefer brand colors if known
   - Font: system fonts only (loading external fonts is prohibited). Default the body font size to 18px or larger
   - Source notation: for any slide that cites figures or facts, note the source (media name and date, or a footnote number) in small text of roughly 8px directly below the relevant content
   - Images: when used, embed them in the HTML as base64 data URIs (external file references and external URLs are prohibited). Compress the image before embedding if the file would become excessively large

4. **Build slides one message at a time**
   - Make the title line the key message (a single declarative sentence). Don't use descriptive headings like "About X"
     - Bad example: "About Market Trends"
     - Good example: "The Domestic Market Will Grow 1.5x Over the Next Three Years"
   - Keep the body to at most 4 bullet points (each bullet roughly no more than 40 full-width Japanese characters, or the equivalent length in English), or a single diagram
   - For any slide requiring a diagram, reserve a diagram area in the center (a placeholder is fine; set alt text)

5. **Save**
   Save it as self-contained HTML with no dependency on external CDNs, external images, or external fonts, following the project's convention (or, if none, `output/slides/<project name/theme name>.html`). Make it something that can be projected as-is just by opening it in a browser.

6. **When producing multilingual versions**
   Finish and review the default-language version first, then generate multilingual versions by pouring translated text into the same template. Name each language's file `<same name>_<language code>.html` (e.g. `_ja.html` / `_en.html`). Since text length varies by language, re-check the body's bullet-point character limit for each language and adjust the wording if anything overflows (do not change the layout itself).

7. **Self-review**
   Double-click the saved HTML file to open it in the default browser, actually check the display slide by slide, and go through the checklist below. Fix any issues before reporting completion.

## Examples

```
/slide-forge Turn outline/proposal.md into slides
/slide-forge Use research/market-trends/findings.md to build a proposal deck
/slide-forge Make slides on the theme "AI Agent Adoption Proposal"
```

## Checklist (Before Submission)

- [ ] Is each slide one message (no two or more claims mixed together)?
- [ ] Skimming only the titles, does the overall story hold together? (How to check: read the title line of every slide aloud in order from top to bottom, and confirm the narrative doesn't suddenly jump around or repeat itself)
- [ ] Are the header, footer, margins, and colors consistent across every slide?
- [ ] Does it use only sourced figures/facts, and is the source noted on the slide (as a footnote or in the footer)?
- [ ] Is it self-contained HTML (no remaining references to external CDNs, external images, or external fonts)?
- [ ] Does it display correctly at 16:9 (1280×720) without breaking?
- [ ] Is the body font size large enough to read at projection distance (guideline: body text 18px or larger, each bullet roughly 40 full-width Japanese characters or fewer, or the equivalent in English)?
- [ ] Is there sufficient contrast between the background color and the text color (no light gray text on a light background)?
- [ ] Are you avoiding distinguishing meaning by color alone (e.g., red = NG / green = OK also indicated by a symbol or label, not color alone)?
- [ ] Do diagram placeholders/images have alt text set?
- [ ] Does the save location/file name follow the project's convention (or, if none, `output/slides/<name>.html`)?
- [ ] No typos, and no errors in number digits or units (yen/dollars, percent, etc.)?
- [ ] When producing multilingual versions, does any language have text overflowing, awkward line-break positions, or broken fonts?

## Notes
- Always keep the output under `output/slides/`. Normalize the file name to alphanumerics, hyphens, and underscores only, and reject inputs containing `..`, a leading slash, or control characters (to prevent writing to unintended locations).

- Only consider PPTX output when the user explicitly requests it (HTML is the default)
- Don't jump straight into building slides without an outline or sourced data in hand. Line up the inputs and storage conventions first in steps 1–2
- A single standalone diagram or a PPTX requiring elaborate animation is out of scope for this command
