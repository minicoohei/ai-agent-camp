# Generate Diagram with Nano Banana Pro

This command uses `.cursor/tools/generate_diagram.py` to generate diagrams and infographics based on a specified theme.
You can also paste long text or entire paragraphs to visualize them.

## Steps

1.  **Extract Parameters**:
    Extract the following information from the user's input.
    - **Theme/Content**: The content or text to visualize (required)
    - **Style**: `colorful_infographic` (default), `sketch`, `photorealistic`, `minimalist`, `claymation`, `pixel_art`
    - **Aspect ratio**: `16:9` (default), `1:1`, `4:3`, `3:4`, `9:16`, `21:9`

2.  **Run the Tool**:
    Execute the command in the following format. For long text, enclose the entire text in quotes or pass it as-is (the tool will concatenate it).
    ```bash
    python .cursor/tools/generate_diagram.py "{theme/content}" --style "{style}" --aspect_ratio "{aspect_ratio}"
    ```

3.  **Verify Results**:
    - Check the path of the generated image and report it to the user.
    - If an error occurs, display the error message.

## Usage Examples

- Basic usage:
  `/generate-diagram How photosynthesis works`

- Visualizing long text:
  `/generate-diagram "Gemini 3 Pro is a new AI model with reasoning capabilities. It generates responses through a thinking process, enabling it to handle complex tasks. It also offers Nano Banana Pro, an image generation model..." --style minimalist`

- Generating from a file (when an Agent reads the file and passes it as an argument):
  The Agent reads the file content and passes it as an argument, or directly executes `python .cursor/tools/generate_diagram.py --file path/to/file.txt`.
