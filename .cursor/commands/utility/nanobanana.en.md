# Nano Banana Pro Image Generation & Editing

This command uses `tools/nanobanana.py` to generate and edit images with Nano Banana Pro (Gemini 3 Pro Image).

## Features

1. **Text-to-image**: Generate new images from a prompt alone
2. **Image editing**: Edit existing images with instructions

## Execution Steps

1. **Extract parameters**:
   Extract the following information from the user's input.
   - **Prompt**: Generation/editing instructions (required) e.g., "A landscape painting of Mt. Fuji", "Blur the background"
   - **Input image path**: Only when editing (optional)
   - **Aspect ratio**: Valid only for generation. `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9` (default: `16:9`)
   - **Session name**: Infer from the current chat title/project name (required)
   - **Output path**: Auto-generated when omitted (saved to `docs/generated/date_sessionName/` folder when `--session` is specified)

2. **Run the tool**:

   **Text-to-image generation:**
   ```bash
   uv run python tools/nanobanana.py "{prompt}" --session "{session_name}" --aspect-ratio "{aspect_ratio}"
   ```

   **Image editing:**
   ```bash
   uv run python tools/nanobanana.py "{prompt}" --input "{input_image_path}" --session "{session_name}"
   ```

## About Session Names

For the `--session` argument, infer an appropriate name from the current chat title or context.
- Example: Chat title "Cursor Bootcamp Banner Creation" -> `--session "cursor_bootcamp_banner"`
- Example: Request "Create a landscape painting of Mt. Fuji" -> `--session "mt_fuji_landscape"`

This organizes images into session-specific folders like `docs/generated/20251223_cursor_bootcamp_banner/`.
