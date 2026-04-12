---
name: marketing-planner
description: "Marketing plan formulation and product marketing context creation skill. Triggered by 'marketing plan', 'positioning', 'persona creation', 'competitive analysis', etc. Generates product-marketing-context.md to serve as the foundation for other marketing skills."
triggers:
  - marketing plan
  - marketing planning
  - positioning
  - persona
  - competitive analysis
  - content strategy
  - target setting
  - product marketing context
---

# Marketing Planner

Creates the marketing foundation document for your product and builds the base for all marketing initiatives.

## Output File

`marketing/product-context.md` -- A shared context referenced by other skills (content-creator, post-publisher, etc.).

## Workflow

### Step 1: Check Existing Context

Check if `marketing/product-context.md` exists.
- **If it exists**: Load it and check which sections need updating
- **If it doesn't exist**: Proceed to the new creation flow

### Step 2: Information Gathering

Fill in the following sections through conversation. Don't ask everything at once.

1. **Product Overview** -- One-line description, category, business model, pricing
2. **Target** -- User segments, personas, primary use cases
3. **Challenges & Pain Points** -- Problems users face, shortcomings of existing solutions
4. **Competitors** -- Direct/indirect competitors, differentiation points
5. **Brand Voice** -- Tone, style, words to use/avoid
6. **Goals** -- Business goals, KPIs, conversion actions

Detailed framework -> `references/context-template.md`

### Step 3: Context Document Generation

Generate `marketing/product-context.md` from the collected information.

### Step 4: Channel Strategy (Optional)

Propose the optimal channel mix based on the context.
Details -> `references/channel-strategy.md`

### Step 5: Content Calendar (Optional)

Output a monthly/weekly content posting plan to `marketing/content-calendar.md`.

## Related Skills

- `content-creator` -- Creates content referencing the context
- `post-publisher` -- Publishes created content to each platform
- Original skills: `product-marketing-context`, `content-strategy`, `marketing-ideas`, `launch-strategy`
