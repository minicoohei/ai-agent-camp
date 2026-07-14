---
nonInteractiveMode: compliant
---

# Screenshot Analyzer - Integrated Screenshot Analysis Tool

This command uses `tools/screenshot_analyzer.py` to analyze screenshots, perform error diagnosis, and generate operation tutorials.

## Features

- **Analyze mode**: Detects errors in images and presents causes and solutions (NextStep).
- **Tutorial mode**: Analyzes operation steps in images and generates step-by-step annotated tutorials.
- **Annotation addition**: Automatically adds annotations such as red borders and arrows to error locations or operation steps.

## Execution Steps

1. **Extract parameters**:
   Extract the following information from the user's input.
   - **Input image path**: The screenshot to analyze (required)
   - **Mode**: `analyze` (error analysis) or `tutorial` (operation steps) (optional, default: `analyze`)
   - **Output path**: Defaults to `docs/bootcamp/screenshots/{mode}_{timestamp}.html` when omitted

2. **Run the tool**:
   Execute the command in the following format.

   ```bash
   # Error analysis mode (default)
   uv run python tools/screenshot_analyzer.py "{input_image_path}" --mode analyze

   # Operation tutorial mode
   uv run python tools/screenshot_analyzer.py "{input_image_path}" --mode tutorial
   ```

3. **Verify results**:
   - Confirm the path of the generated HTML file and report it to the user.
   - Provide instructions on how to open it with Live Server.
   - Display error messages if any errors occur.

## Usage Examples

### Error analysis (Analyze mode)
```
/screenshot-analyzer error.png
```
or
```
/screenshot-analyzer error.png --mode analyze
```

### Operation tutorial generation (Tutorial mode)
```
/screenshot-analyzer menu.png --mode tutorial
```

### Run without annotations
```
/screenshot-analyzer error.png --no-annotate
```

### Specify output destination
```
/screenshot-analyzer error.png --output docs/report/error_analysis.html
```

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` to run.
- In Tutorial mode, annotated images are generated for each step, so processing may take time.
- The original image file is not modified (annotated images are saved as separate files).
