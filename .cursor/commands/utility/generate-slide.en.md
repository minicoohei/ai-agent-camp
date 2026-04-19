# Generate Lecture Slide with Nano Banana Pro

This command uses `tools/generate_slide.py` to generate professional lecture slides.
Simply input a topic, and it will automatically gather the necessary explanations and create a slide with a unified design.

## Design Specifications

All slides are generated with the following unified design:

| Item | Specification |
|------|---------------|
| Background | White |
| Main color | Blue (#2563EB) |
| Sub color | Yellow (#FBBF24) |
| Style | Flat design |
| Font size | 14pt or larger |
| Text amount | Minimal (organized appearance) |
| Aspect ratio | 16:9 |

## Steps

1. **Extract Parameters**:
   Extract the following information from the user's input.
   - **Topic**: The slide theme (required) e.g., "How AI Agent Tools Work"
   - **Style**: `auto` (default), `title`, `content`, `diagram`, `summary`
   - **Output path**: If omitted, defaults to `docs/slides/{topic_name}_{timestamp}.png`

2. **Run the Tool**:
   Execute the command in the following format.
   ```bash
   uv run python tools/generate_slide.py "{topic}" --style "{style}" --output "{output_path}"
   ```

3. **Verify Results**:
   - Check the path of the generated slide image and report it to the user.
   - If an error occurs, display the error message.

## Slide Style Reference

| Style | Description |
|-------|-------------|
| `auto` | AI automatically selects the optimal layout based on content (default) |
| `title` | Title slide (large title + subtitle) |
| `content` | Content slide (bullet points, explanatory text) |
| `diagram` | Diagram slide (concept diagram, flowchart-style) |
| `summary` | Summary slide (organized key points) |

## Usage Examples

### Basic usage (automatic style)
```
/generate-slide How AI Agent Tools Work
```

### Generate a title slide
```
/generate-slide Introduction to Machine Learning Seminar --style title
```

### Generate a diagram slide
```
/generate-slide API Request Flow --style diagram
```

### Generate a content slide
```
/generate-slide Database Normalization --style content
```

### Generate a summary slide
```
/generate-slide Today's Learning Points --style summary
```

### Specify output path
```
/generate-slide Cloud Architecture --output docs/slides/cloud_arch.png
```

### Combine multiple options
```
/generate-slide REST API Design Principles --style diagram --output docs/training/api_design.png
```

## Processing Flow

1. **Content Generation** (Gemini 2.5 Flash)
   - Automatically gather explanations and key points needed for the lecture from the topic
   - Organize into concise text suitable for slides

2. **Prompt Optimization** (Gemini 2.5 Flash)
   - Create a slide generation prompt reflecting the design specifications
   - Generate layout instructions according to the style

3. **Slide Generation** (Nano Banana Pro)
   - Generate a slide image using the optimized prompt
   - Output a 16:9 professional lecture slide

## Notes

- Requires `GEMINI_API_KEY` (recommended) to be set in environment variables (or `.env`).
- Each generated slide is a single image file (PNG format).
- If multiple slides are needed, run the command multiple times.
- Japanese topics are supported. Text in the generated slide is also displayed in Japanese.
