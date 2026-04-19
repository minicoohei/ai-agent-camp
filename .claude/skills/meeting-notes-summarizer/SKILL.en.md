---
name: meeting-notes-summarizer
description: "Skill for automatically generating structured meeting minutes from meeting text and notes. Triggered by requests like 'summarize the meeting minutes', 'organize meeting notes', 'extract action items', etc."
triggers:
  - summarize the meeting minutes
  - organize meeting notes
  - extract action items
  - summarize meeting notes
  - list the decisions
  - meeting-notes-summarizer
  - organize the key points of this meeting
---

# meeting-notes-summarizer - Automated Meeting Minutes Generation Skill

Reads meeting notes, transcriptions, and chat logs, then formats them into structured Markdown meeting minutes. When the input has missing information, it is explicitly noted as `Not specified`, `To be confirmed`, or `Deadline TBD` rather than guessing.

## When to Use

Use when you receive the following requests:

- Create meeting minutes from meeting text or notes
- Extract decisions and action items
- Structure and organize meeting notes for readability
- Format meeting notes in Markdown

Representative trigger phrases:

- "Summarize the meeting minutes"
- "Organize meeting notes"
- "Extract action items"
- "Summarize the meeting notes"
- "Structure the meeting notes"
- "Organize the key points of this meeting"
- "Summarize the key points of this meeting"
- "List the decisions"

## Workflow

Follow these steps. Always execute at least one round of self-review and improvement loop after the initial generation.

### Step 1: Receive the Input Text

- Receive meeting notes, audio transcriptions, chat logs, or bullet-point notes
- Determine the input format and separate date/time, participants, speaker labels, and discussion content
- Don't over-supplement missing information; handle it as `Not specified` or `To be confirmed` in subsequent sections

### Step 2: Extract Participants

- Extract participant candidates from participant lists, speaker names, and utterance labels
- Unify name variations as the same person
- If participants are not explicitly stated, note `Participants unknown`

### Step 3: Identify Agenda Items

- Organize major topics chronologically or by discussion point
- Briefly summarize the discussion content for each topic
- If there is excessive chat or noise, retain only utterances related to the main topic

### Step 4: Extract Decisions

- Extract confirmed items from expressions like "decided", "agreed", "approved", "determined"
- Add a one-line note about the background or rationale for each decision
- If no decisions are found, explicitly note `No decisions made`

### Step 5: Extract Action Items

- Extract tasks from expressions like "will do", "will handle", "will confirm", "by next meeting"
- Associate each task with an assignee, deadline, and priority
- If the assignee is unknown, note `To be confirmed`; if the deadline is unknown, note `Deadline TBD`

### Step 6: Generate Initial Draft

- Read `references/output-template.md` and create the initial draft following the same order and heading structure
- Don't leave unknown items blank; use `Not specified`, `To be confirmed`, `Deadline TBD` explicitly
- At this stage, prioritize filling all required sections without omission over perfection

### Step 7: Perform Self-Review

- Self-check the initial draft against the following checklist
- Evaluate each item as `OK` / `Needs fix` / `Needs confirmation` with a one-line rationale

Self-review checklist:

1. Are all participants reflected in the body or participant section?
2. Are the agenda items or major topics organized without excess or deficiency?
3. Are decisions clear, and is `No decisions made` explicitly noted when applicable?
4. Does each action item have an assignee, deadline, and priority? Is `To be confirmed` / `Deadline TBD` inserted when missing?
5. Does the discussion notes section retain important context such as background, concerns, and pending items?
6. Is the next meeting schedule or its absence explicitly stated?
7. Does the output follow the heading order and primary language of `references/output-template.md`?

### Step 8: Run Improvement Loop

- Revise the draft based on self-review results
- Limit improvements to a maximum of 2 rounds, briefly recording "what was fixed" each round
- Stop improvement when any of the following are met:
  - All checklist items are `OK`
  - 2 rounds of improvement have been completed
  - The diff from the previous version is minimal with little room for further improvement
- Issues unresolved after 2 rounds are noted as `Remaining issues` in the final output

### Step 9: Format Final Output with Diff

- Read `references/output-template.md` and format following the same order and heading structure
- Return output in Markdown
- Before the final version, summarize changes from the initial draft as a `diff`
- Show the diff in at least 3 categories: `Added`, `Modified`, `Needs confirmation`
- If file output is needed, save to `output/` or the `outputs/` of the current repository

## Output Format

The output follows the template in `references/output-template.md`. At minimum, include these sections:

- Basic Information
- Agenda
- Decisions
- Action Items
- Discussion Notes
- Next Meeting

Action items are organized in table format with columns for assignee, task, deadline, and priority.

When using Iterative Refinement, the following may be added before the template body:

- `## Self-Review Results`
- `## Revision Diff`
- `## Remaining Issues` (only when needed)

## Iterative Refinement Prompt Structure

Process internally in this order:

1. Initial draft generation
   - "Create a Markdown meeting minutes draft conforming to the template from the input text. Don't guess missing information; state it explicitly"
2. Self-review
   - "Evaluate the draft against the 7-item checklist, returning `OK` / `Needs fix` / `Needs confirmation` with rationale"
3. Improved version generation
   - "Update the meeting minutes targeting only items marked `Needs fix` or `Needs confirmation` in the review, listing what was modified"
4. Final confirmation
   - "Display the diff between the initial draft and improved version as `Added` / `Modified` / `Needs confirmation`, then output the final version"

## Edge Case Handling

### No Action Items

- Note `No action items for this meeting` in the `Action Items` section
- Don't treat meetings with only decisions as an error

### Unknown Participants

- If partially inferable from utterance content, add `(estimated)`
- If completely unknown, note `Participants: Unknown (not specified in text)`

### Mixed Languages

- Output in the primary language of the input text
- Preserve proper nouns, product names, and technical terms in their original language
- When Japanese and English are mixed, use Japanese as the primary language

### Input Text Too Short

- Create meeting minutes with the minimum identifiable information
- Explicitly note missing elements as `Not specified`

### Chat Log Format

- Parse timestamps and speakers
- Exclude casual chat and duplicate posts, extracting the essence of discussion
- If threads exist, organize by topic before integrating into the overall minutes
