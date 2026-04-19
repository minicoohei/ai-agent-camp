# PDF Page Editor

A command to edit (modify/delete) text in PDFs.
Uses an interactive AskQuestion format for page and text selection.

## Execution Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **PDF file path**: The PDF to edit (required)
- **Edit content**: What text to change and how (optional, can be confirmed later)

---

### Step 2: PDF Analysis

```bash
uv run python tools/pdf_page_editor.py analyze "{pdf_file_path}"
```

- A workspace is created (`{pdf_name}_workspace/`)
- Text elements on each page are analyzed
- Retrieve the page list from `analysis.yaml`

---

### Step 3: Page Selection (AskQuestion)

**Use the ask_question tool to select a page:**

```yaml
title: "Select a page to edit"
questions:
  - id: "page_select"
    prompt: "Which page would you like to edit?"
    options:
      # Dynamically generated from analysis.yaml
      # Example:
      - id: "page_1"
        label: "Page 1 - {first 20 characters of the first text element}..."
      - id: "page_2"
        label: "Page 2 - {first 20 characters of the first text element}..."
      # ... for all pages
    allow_multiple: false
```

> **Implementation hint**: Retrieve the first text element from each page in `analysis.yaml`
> and include the first ~20 characters in the label to help users identify pages.

---

### Step 4: Display Text List

```bash
uv run python tools/pdf_page_editor.py show {workspace} {page_number}
```

- Displays all text elements on that page as a **numbered list**
- Example:
  ```
  Text elements on page 3:
  [1] New Standards for AI Data Analysis
  [2] Company XYZ Inc.
  [3] December 2024
  [4] Table of Contents
  ...
  ```

---

### Step 5: Text Selection (AskQuestion)

**Use the ask_question tool to confirm the selection method:**

```yaml
title: "Select text to edit"
questions:
  - id: "text_select_method"
    prompt: "Choose your text selection method"
    options:
      - id: "by_number"
        label: "Select by number (specify a number from the list above)"
      - id: "by_input"
        label: "Enter text directly"
    allow_multiple: false
```

#### If selecting by number

**Follow up with ask_question to select the text number:**

```yaml
title: "Select text number"
questions:
  - id: "text_number"
    prompt: "Choose the number of the text to edit"
    options:
      # Dynamically generated from the list displayed in Step 4
      - id: "text_1"
        label: "[1] New Standards for AI Data Analysis"
      - id: "text_2"
        label: "[2] Company XYZ Inc."
      # ... for all text elements
    allow_multiple: false
```

#### If entering text directly

Ask the user to input the target text.

---

### Step 6: Edit Type Selection (AskQuestion)

**Use the ask_question tool to select the edit type:**

```yaml
title: "Select edit type"
questions:
  - id: "edit_type"
    prompt: "What kind of edit would you like to perform?"
    options:
      - id: "replace"
        label: "Text replacement (change to different text)"
      - id: "delete"
        label: "Text deletion (remove the text)"
      - id: "prompt"
        label: "Free-form description (instruct AI to edit)"
    allow_multiple: false
```

#### Additional input by edit type

- **Replacement**: Ask for the new text
- **Deletion**: Confirmation only (no additional input needed)
- **Free-form**: Ask for editing instructions

---

### Step 7: Execute Edit

```bash
# Text replacement
uv run python tools/pdf_page_editor.py edit {workspace} {page_number} --replace "{old_text}" "{new_text}"

# Text deletion
uv run python tools/pdf_page_editor.py edit {workspace} {page_number} --delete "{text_to_delete}"

# Free-form description
uv run python tools/pdf_page_editor.py edit {workspace} {page_number} --prompt "{editing_instructions}"
```

---

### Step 8: Display Results

After editing is complete, display the following to the user:

```
✅ Edit complete

Original image: {workspace}/pages/page_{number:03d}.png
Edited image: {workspace}/edited/page_{number:03d}_edited.png
```

- Use the `open` command to open the image if needed

---

### Step 9: Next Action Selection (AskQuestion)

**Use the ask_question tool to confirm the next action:**

```yaml
title: "Next action"
questions:
  - id: "next_action"
    prompt: "What would you like to do next?"
    options:
      - id: "same_page"
        label: "Edit different text on the same page"
      - id: "other_page"
        label: "Edit a different page"
      - id: "rebuild"
        label: "Finish editing and rebuild the PDF"
      - id: "exit"
        label: "End editing (no rebuild)"
    allow_multiple: false
```

#### Transitions by action

- **Edit different text on the same page**: -> Return to Step 4
- **Edit a different page**: -> Return to Step 3
- **Finish editing and rebuild the PDF**: -> Go to Step 10
- **End editing (no rebuild)**: -> Done

---

### Step 10: PDF Rebuild (Optional)

```bash
uv run python tools/pdf_page_editor.py rebuild {workspace}
```

- A new PDF containing edited pages is generated
- Output: `{workspace}/{pdf_name}_edited.pdf`

---

## Flow Diagram

```
PDF Analysis -> [AskQuestion] Page Selection
                    |
               Display Text List
                    |
          [AskQuestion] Text Selection Method
               |              |
          By Number      Direct Input
               |              |
        [AskQuestion]    Text Input
         Number Select
               |              |
          [AskQuestion] Edit Type Selection
                    |
               Execute Edit
                    |
              Display Results
                    |
          [AskQuestion] Next Action
           |      |       |        |
        Same    Other   Rebuild   Exit
        Page    Page
           |      |       |
         Step4  Step3  Step10
```

---

## Usage Example

```
/pdf-editor docs/presentation.pdf
```

-> PDF Analysis -> [AskQuestion] Page Selection -> Display Text List -> [AskQuestion] Text Selection -> [AskQuestion] Edit Type -> Execute Edit -> [AskQuestion] Next Action

---

## Workspace Structure

```
{pdf_name}_workspace/
├── pages/           # Extracted page images
│   ├── page_001.png
│   └── ...
├── edited/          # Edited images
│   ├── page_001_edited.png
│   └── ...
├── analysis.yaml    # Analysis results (text elements)
└── {pdf_name}_edited.pdf  # Final output
```

---

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY`
- Image editing is AI-generated, so fonts and layout may change slightly
- Dependencies: `pdf2image`, `img2pdf`, `tqdm`, `PyYAML`, `Pillow`, `google-genai`
