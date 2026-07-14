---
nonInteractiveMode: compliant
---

# Annotate Screenshot with Nano Banana Pro

This command uses `tools/annotate_screenshot.py` to add manual-style annotations (red boxes, arrows, callouts, text) to screenshots.

## Key Principle

**The original screenshot is never modified.**

- No pixels of the input image are altered
- Annotations are added as overlays on top of the original image
- Output is always saved as a separate file
- Designed for manual/documentation use, preserving the actual screen content exactly

## Steps

1. **Extract Parameters**:
   Extract the following information from the user's input.
   - **Input image path**: The screenshot to annotate (required)
   - **Annotation instructions**: What to add and where (required) e.g., "Surround the Save button with a red box"
   - **Text label**: Text to display on arrows or callouts (optional)
   - **Style**: `red_box` (default), `arrow`, `callout`, `highlight`, `circle`, `number`
   - **Output path**: If omitted, defaults to `{original_filename}_annotated.png`

2. **Run the Tool**:
   Execute the command in the following format.
   ```bash
   uv run python tools/annotate_screenshot.py "{input_image_path}" "{annotation_instructions}" --style "{style}" --text "{text_label}" --output "{output_path}"
   ```

3. **Verify Results**:
   - Check the path of the generated annotated image and report it to the user.
   - **Clearly state that the original image has not been modified.**
   - If an error occurs, display the error message.

## Style Reference

| Style | Description |
|-------|-------------|
| `red_box` | Surround the element with a red rectangle and add an arrow (default) |
| `arrow` | Point to the element with a red arrow |
| `callout` | Add a callout (comment balloon) |
| `highlight` | Add a semi-transparent highlighter-style highlight |
| `circle` | Surround the element with a red circle |
| `number` | Add numbered markers (for showing step order) |

## Usage Examples

### Basic usage (red box + arrow)
```
/annotate-screenshot docs/manual_screenshots/login.png Surround the "Login" button with a red box and add an arrow
```

### With text label
```
/annotate-screenshot settings.png The "Settings" icon in the upper right --text "Click here"
```

### Callout style
```
/annotate-screenshot dashboard.png The menu bar --style callout --text "Operate from this area"
```

### Highlighter-style highlight
```
/annotate-screenshot form.png The input field --style highlight
```

### Specify output path
```
/annotate-screenshot original.png The "Submit" button --output docs/manual_screenshots/step3_annotated.png
```

### Add multiple annotations in sequence (numbered markers)
```
/annotate-screenshot workflow.png The first input field --style number --text "1"
/annotate-screenshot workflow_annotated.png The next dropdown --style number --text "2" --output workflow_step2.png
```

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` to be set in environment variables (or `.env`).
- If the output file path is the same as the input file path, an error will occur for safety.
- This tool uses Nano Banana Pro (Gemini 3 Pro Image Preview). The prompt strongly instructs it to preserve the original image, but due to the nature of AI generation, minor differences may occur. If strict pixel-perfect accuracy is required, consider using the legacy `src/gemini_annotate.py` (Pillow drawing version).
