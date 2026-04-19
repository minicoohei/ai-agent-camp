# Tools Index - Tool List

A list and overview of the tools available in this project.

## Tools by Category

### Project Analysis
- **project_overview**: Visualizes project structure in PlantUML/Mermaid/WBS format and summarizes modules, features, and missing parts.

### Screenshot Analysis & Processing
- **screenshot_analyzer**: Integrated screenshot analysis tool.
  - `analyze` mode: Error detection, cause identification, NextStep suggestions
  - `tutorial` mode: Operation step analysis and step-annotated tutorial generation
- **annotate_screenshot**: Adds annotations such as red borders, arrows, and callouts to screenshots (overlays without modifying the original image).
- **video_frame_reader**: Extracts keyframes from videos + performs Gemini analysis.

### Ad & Banner Generation
- **banner_creator**: Generates banners/creatives for various SNS and advertising platforms.
  - Supports X, Facebook, Instagram, PR Times, YouTube, LINE, and web ads
  - Fine-grained control over tone, color scheme, font style, and priority
  - Simultaneous generation of post copy text (post text, hashtags, CTA)
  - Supports reference image specification and web search retrieval

### Slide & Diagram Generation
- **generate_aitutor_slide**: Generates AI BRAIN PARTNERS training slide images based on 17 reference slide types.
- **generate_slide**: Generates lecture slide images from topics (simple design with white background/blue main/yellow accent).
- **generate_diagram**: Generates infographic/diagram images from topics or text.
- **generate_plantuml_diagram**: Generates Visio-style modern flowchart images from PlantUML files.
- **pptx_template**: Extracts format from PPTX into YAML templates and generates new slides with only text replaced.

### Learning Support & Guides
- **guide_action**: Analyzes the current situation from SpecStory history and presents background explanations and next actions.
- **tutor_generate**: Extracts learning gaps from SpecStory history and generates beginner-friendly learning content (HTML).

### Setup & Utilities
- **google_api_setup**: Sets up Google API OAuth authentication for MCP (supports Gmail, Calendar, Drive, Sheets).
- **gmail_account_setup**: Configures OAuth authentication for multiple Gmail accounts and automatically registers them in GitHub Secrets.
- **google_account_setup**: Configures Calendar/Drive OAuth authentication for multiple Google accounts and automatically registers them in GitHub Secrets. Can reuse the same client ID as for Gmail.
- **bigquery_auth**: Sets up BigQuery authentication per GCP project. Safely manages multiple projects using gcloud configuration profiles.
- **notebooklm_cli**: Creates/retrieves/lists recently viewed notebooks using the NotebookLM Enterprise API.
- **bootcamp_utils**: Common utilities (Gemini API client initialization, HTML template generation, etc.). Used internally.

## Command List

| Command | Corresponding Tool | Description |
|---------|-------------------|-------------|
| `/overview` | project_overview | Visualize project structure |
| `/screenshot-analyzer` | screenshot_analyzer | Screenshot analysis (error/tutorial) |
| `/annotate-screenshot` | annotate_screenshot | Add annotations to images |
| `/video-frame-reader` | video_frame_reader | Video keyframe extraction + Gemini analysis |
| `/create-banner` | banner_creator | Ad banner/creative generation |
| `/generate-aitutor-slide` | generate_aitutor_slide | Training slide generation |
| `/generate-slide` | generate_slide | General-purpose slide generation |
| `/generate-diagram` | generate_diagram | Diagram generation |
| `/generate-plantuml-diagram` | generate_plantuml_diagram | PlantUML diagram generation |
| `/pptx-template` | pptx_template | PPTX template extraction & generation |
| `/guide` | guide_action | Next action suggestions |
| `/tutor` | tutor_generate | Learning content generation |
| `/setup-google-api` | google_api_setup | Google API authentication setup |
| `/gmail-account-setup` | gmail_account_setup | Gmail OAuth authentication & Secrets registration |
| `/google-account-setup` | google_account_setup | Calendar/Drive OAuth authentication & Secrets registration |
| `/bigquery-auth` | bigquery_auth | BigQuery authentication (per project) |
| `/notebooklm` | notebooklm_cli | NotebookLM notebook creation/retrieval/listing |
