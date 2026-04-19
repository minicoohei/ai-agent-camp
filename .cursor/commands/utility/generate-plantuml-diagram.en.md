# Generate PlantUML Diagram with Nano Banana Pro

This command uses `tools/generate_plantuml_diagram.py` to generate modern Visio Flowchart-template-style flowchart images from PlantUML files.

## Design Specifications

### Layout

- The overall flow follows a vertical (top-down) direction
- Each "participant" defined in the PlantUML gets its own vertical swimlane
- Swimlane borders are light gray (#CCCCCC), background is white
- Each step is placed within the swimlane of its corresponding participant

### Shape Styles

| Shape Type | Style |
|-----------|---------|
| General process | Rounded rectangle (white, border #4A90E2, light shadow) |
| Internal process (self-call) | Light blue (#E8F1FF) rounded rectangle |
| Receive/input (from another participant) | Light green (#E9F7EC) rounded rectangle |
| Conditional branch (alt/else/opt) | Diamond (border #7B61FF) |

### Arrows (Flow Lines)

- All straight lines or 90-degree angled lines, color is dark gray (#555555)
- Arrow heads are clear and highly visible
- Conditional branches split left and right from the bottom of the diamond, with alt/else labels

### Icons

- Small flat icons placed in the upper-left corner of shapes to indicate the nature of the process
- Icon line width is 1.5-2px for consistency
- Appropriate icons are automatically assigned based on participant names and process content

### Color Palette

| Element | Color |
|---------|-------|
| Background | Light gray (#F7F7F7) |
| General process | White |
| Internal process | Light blue (#E8F1FF) |
| Receive/input | Light green (#E9F7EC) |
| Branch labels | Dark gray (#444444) |

### Font

- Sans-serif (Segoe UI, Helvetica, Noto Sans, etc.)
- Text inside shapes: approximately 18px
- Labels (alt, else, opt): 14px

### Spacing

- Vertical distance between shapes is uniform at 40-60px
- Swimlanes are aligned with equal widths
- Overall margins are maintained, with shapes horizontally aligned for a neat arrangement

### Overall Aesthetic

- Modern, simple UI-style design
- Minimal decorations, focused on readability
- Very light shadows, avoiding excessive 3D effects
- Clear balance and alignment of overall shapes

## Steps

1. **Extract Parameters**:
   Extract the following information from the user's input.
   - **PlantUML file path**: The PlantUML file to convert (required)
   - **Aspect ratio**: `auto` (default), `16:9`, `1:1`, `4:3`, `3:4`, `9:16`
   - **Output path**: If omitted, defaults to `docs/diagrams/{filename}_{timestamp}.png`

2. **Run the Tool**:
   Execute the command in the following format.
   ```bash
   uv run python tools/generate_plantuml_diagram.py "{plantuml_file_path}" --aspect_ratio "{aspect_ratio}" --output "{output_path}"
   ```

3. **Verify Results**:
   - Check the path of the generated diagram image and report it to the user.
   - If an error occurs, display the error message.

## Parameter Reference

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `plantuml_path` | Yes | - | Path to the PlantUML file (.puml) |
| `--output`, `-o` | - | Auto-generated | Output image path |
| `--aspect_ratio`, `-a` | - | `auto` | Aspect ratio (auto determines from PlantUML structure) |

## Automatic Aspect Ratio Detection

When `auto` is specified, the following rules apply:

| Condition | Aspect Ratio |
|-----------|-------------|
| 5 or more participants | `21:9` (landscape) |
| 3-4 participants | `16:9` |
| Long sequence (20+ steps) | `9:16` (portrait) |
| Other | `16:9` |

## Usage Examples

### Basic usage (automatic aspect ratio)
```
/generate-plantuml-diagram work/06.Porimu/sequence.puml
```

### Specify aspect ratio
```
/generate-plantuml-diagram work/project/flow.puml --aspect_ratio 16:9
```

### Specify output path
```
/generate-plantuml-diagram sequence.puml --output docs/diagrams/my_flow.png
```

### Combine multiple options
```
/generate-plantuml-diagram work/api_flow.puml --aspect_ratio 9:16 --output docs/api_sequence.png
```

## Processing Flow

1. **Read PlantUML**
   - Read PlantUML code from the file
   - Analyze the structure of participants, messages, branches, etc.

2. **Generate Prompt** (Gemini 2.5 Flash)
   - Analyze the PlantUML structure and create a prompt reflecting the design specifications
   - Specify swimlanes, shape types, and color coding

3. **Generate Diagram** (Nano Banana Pro)
   - Generate a flowchart image using the optimized prompt
   - Output a modern, professional Visio-style diagram

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` to be set in environment variables (or `.env`).
- The generated diagram is a single image file (PNG format).
- Complex PlantUML diagrams (many participants, many steps) may take longer to generate.
- Japanese labels are supported. Text in the generated diagram is also displayed in Japanese.
