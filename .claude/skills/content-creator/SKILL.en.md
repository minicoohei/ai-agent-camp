---
name: content-creator
description: "A marketing content creation skill. Creates X/Instagram posts, Note/Medium articles, banner images, video scripts, and more. Triggered by requests like 'create a post', 'create a banner', 'write an article', 'create copy', etc. References product-context.md to maintain brand consistency."
triggers:
  - create a post
  - content creation
  - create a banner
  - write an article
  - create copy
  - SNS post
  - create tweet
  - Instagram post
  - Note article
  - Medium article
  - 投稿作って
  - コンテンツ作成
---

# Content Creator

A skill for creating marketing content. Generates brand-consistent content based on product context.

## Prerequisites

`marketing/product-context.md` must exist. If not, prompt creation with the `marketing-planner` skill first.

## Content Types

### 1. SNS Posts (X / Instagram)

**Input**: Theme or prompt
**Output**: Post text + hashtags + (if needed) image prompt

Format -> `references/post-formats.md`

#### X (Twitter)
- Within 280 characters (approximately 140 characters for Japanese)
- Thread format also supported (3-7 tweets)
- CTA should be clear

#### Instagram
- Caption: within 2200 characters, first 125 characters are critical
- Hashtags: 20-30 (in order of relevance)
- Reels/Stories scripts also supported

### 2. Articles (Note / Medium / Blog)

**Input**: Theme, target audience, purpose
**Output**: Structure proposal -> Body text -> Meta information

Process:
1. Outline proposal (H2/H3 structure)
2. Body writing after approval
3. SEO meta (title, description, OGP) generation

### 3. Banner Images

**Input**: Use case, text, style
**Output**: Gemini image generation prompt -> Generation -> Review

Size guide:
- X: 1200x675px
- Instagram Feed: 1080x1080px
- Instagram Stories: 1080x1920px
- Note/Medium OGP: 1200x630px

### 4. Video Scripts

**Input**: Theme, duration, platform
**Output**: Script (lines + screen directions)

- Short (15-60 sec): Hook -> Main topic -> CTA
- Long (5-15 min): Intro -> Sections -> Summary -> CTA

### 5. Email

**Input**: Purpose, target audience, sequence position
**Output**: Subject line + Body + CTA

Details -> `references/email-templates.md`

## Content Quality Check

Always verify after generation:
- [ ] Matches brand voice in product-context.md
- [ ] Appropriate for target persona
- [ ] CTA is clear
- [ ] Meets platform constraints (character count, image size, etc.)
- [ ] Does not use words to avoid

## Batch Generation

Handles requests like "Create a week's worth of posts":
1. Reference content-calendar.md (if available)
2. Generate theme variations
3. Optimize for day of week/time of day
4. Batch output -> save to `marketing/drafts/`

## Related Skills

- `marketing-planner` -- Context document creation
- `post-publisher` -- Publishing created content
- Source skills: `copywriting`, `copy-editing`, `social-content`, `email-sequence`
