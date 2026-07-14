---
nonInteractiveMode: compliant
---

# Overview - Project Structure Visualization

This command uses `tools/project_overview.py` to leverage serena MCP for visualizing project structure and extracting missing features or unimplemented parts.

## Features

- Symbolically explore the codebase with serena MCP
- Visualize project structure in PlantUML format (displayed as SVG images)
- **Display file list and function/class list**
- Extract missing features and unimplemented parts
- Output reports in HTML format
- **Ask for clarification when information is insufficient**

## Design Philosophy

- **serena MCP utilization**: Accurate structure analysis through symbolic exploration
- **Visualization focus**: Display structure diagrams as SVG images via the PlantUML official server
- **File/function listing**: Display descriptions and key functions for each file
- **Missing feature identification**: Clearly distinguish between implemented and missing features

## Execution Steps

1. **Extract parameters**:
   Extract the following information from the user's input.
   - **Target directory**: The directory to analyze (optional, default: project root)
   - **Output format**: plantuml / wbs / all (optional, default: all)
   - **Output path**: Defaults to `docs/bootcamp/overview/overview_{timestamp}.html` when omitted

2. **Handling insufficient information**:
   If required information is missing, ask the user as follows:
   ```
   To generate the project overview, please provide the following:
   
   1. Which directory would you like to analyze? (e.g., src/, scripts/)
   2. Do you have a preferred output format? (plantuml / wbs / all)
   ```

3. **Run the tool**:
   Execute the command in the following format.
   ```bash
   uv run python tools/project_overview.py --directory "{target_directory}" --format "{output_format}" --output "{output_path}"
   ```

4. **Verify results**:
   - Confirm the path of the generated HTML file and report it to the user.
   - Provide instructions on how to open it with Live Server.
   - Display error messages if any errors occur.

## Usage Examples

### Basic usage (analyze the entire project)
```
/overview
```

### Analyze a specific directory
```
/overview --directory src/
```

### Specify output format (WBS mind map only)
```
/overview --format wbs
```

### Combine multiple options
```
/overview --directory scripts/ --format plantuml --output docs/bootcamp/overview/scripts_overview.html
```

## Processing Flow

1. **Explore codebase with serena MCP**: Symbolically analyze the project structure
2. **Analyze with Gemini API**: Extract file list, function list, and descriptions
3. **Visualize structure**: Generate component diagrams and mind maps with PlantUML
4. **Generate HTML report**: Output a report in an easy-to-understand format

## Output Contents

- **File list and functions**: Path, description, and key functions/classes for each file
- **Project structure diagram**: Component diagram in PlantUML format (SVG image)
- **Mind map (WBS)**: Hierarchical diagram in PlantUML format (SVG image)
- **Module list**: Roles and relationships of each module
- **Implemented features**: List of currently implemented features
- **Missing features**: List of unimplemented or missing features
- **Recommendations**: Recommendations for project improvement

## About serena MCP

serena MCP is an MCP (Model Context Protocol) that enables symbolic exploration of codebases.

- Clearly understand project structure
- Understand what each file does
- Confirm which features have been completed

## Notes

- Run in an environment where serena MCP is available
- Analysis may take time for large projects
- Connection to the PlantUML official server (plantuml.com) is required
