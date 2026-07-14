---
nonInteractiveMode: deferred
---

# Create Banner - Ad Banner/Creative Generation

This command uses `tools/banner_creator.py` to generate banners/creatives for various SNS and advertising platforms.

## Important: Pre-Execution Checklist

**Before executing this command, you must use the `ask_question` tool to confirm the following information.**

## Step 1: Gather Information with ask_question

Use the `ask_question` tool to ask the following questions:

```json
{
  "title": "Ad Banner/Creative Creation",
  "questions": [
    {
      "id": "platform",
      "prompt": "Which platform is this banner for?",
      "options": [
        {"id": "x_post", "label": "X (Twitter) - Timeline post (1200x675)"},
        {"id": "x_card", "label": "X (Twitter) - Card display (800x418)"},
        {"id": "facebook", "label": "Facebook - Link post (1200x630)"},
        {"id": "facebook_story", "label": "Facebook - Stories (1080x1920)"},
        {"id": "instagram_feed", "label": "Instagram - Feed post (1080x1080)"},
        {"id": "instagram_story", "label": "Instagram - Stories (1080x1920)"},
        {"id": "prtimes", "label": "PR Times - Press release (1200x630)"},
        {"id": "youtube", "label": "YouTube - Thumbnail (1280x720)"},
        {"id": "line", "label": "LINE - Rich message (1040x1040)"},
        {"id": "web_horizontal", "label": "Web ad - Horizontal (1200x628)"},
        {"id": "web_vertical", "label": "Web ad - Vertical (300x600)"},
        {"id": "custom", "label": "Custom size"}
      ],
      "allow_multiple": false
    },
    {
      "id": "tone",
      "prompt": "Select the tone/mood for the banner",
      "options": [
        {"id": "professional", "label": "Professional - Business-oriented, trustworthy"},
        {"id": "casual", "label": "Casual - Approachable, friendly"},
        {"id": "pop", "label": "Pop - Bright, fun, youth-oriented"},
        {"id": "elegant", "label": "Elegant - Luxurious, sophisticated"},
        {"id": "urgent", "label": "Urgent - Sale, limited time, act now"},
        {"id": "minimal", "label": "Minimal - Simple, leveraging whitespace"},
        {"id": "tech", "label": "Tech - Advanced, digital feel"},
        {"id": "natural", "label": "Natural - Nature, organic"}
      ],
      "allow_multiple": false
    },
    {
      "id": "color_scheme",
      "prompt": "Select the color direction",
      "options": [
        {"id": "brand", "label": "Specify brand colors (enter later)"},
        {"id": "warm", "label": "Warm tones - Red, orange, yellow"},
        {"id": "cool", "label": "Cool tones - Blue, green, purple"},
        {"id": "mono", "label": "Monotone - Black, white, gray"},
        {"id": "pastel", "label": "Pastel - Light, soft colors"},
        {"id": "vivid", "label": "Vivid - Bright primary colors"},
        {"id": "dark", "label": "Dark - Black-based, luxurious feel"},
        {"id": "auto", "label": "Let AI decide"}
      ],
      "allow_multiple": false
    },
    {
      "id": "font_style",
      "prompt": "Select the font style",
      "options": [
        {"id": "gothic", "label": "Gothic - Readable, modern"},
        {"id": "mincho", "label": "Mincho (Serif) - Traditional, luxurious"},
        {"id": "handwritten", "label": "Handwritten - Approachable, unique"},
        {"id": "bold", "label": "Bold/Impact - Strong, eye-catching"},
        {"id": "script", "label": "Script - Elegant, feminine"},
        {"id": "geometric", "label": "Geometric - Futuristic, tech-oriented"},
        {"id": "auto", "label": "Let AI decide"}
      ],
      "allow_multiple": false
    },
    {
      "id": "priority",
      "prompt": "What is most important for this banner?",
      "options": [
        {"id": "ctr", "label": "Click-through rate (CTR) - Eye-catching, call to action"},
        {"id": "brand", "label": "Brand awareness - Emphasize logo/company name"},
        {"id": "info", "label": "Information delivery - Convey content accurately"},
        {"id": "emotion", "label": "Emotional appeal - Evoke empathy, emotion"},
        {"id": "product", "label": "Product appeal - Showcase products attractively"},
        {"id": "event", "label": "Event announcement - Clearly show date/location"}
      ],
      "allow_multiple": false
    },
    {
      "id": "reference_type",
      "prompt": "How would you like to specify a reference image?",
      "options": [
        {"id": "search", "label": "Search by keyword (reference competitor/similar creatives)"},
        {"id": "url", "label": "Specify image URL directly"},
        {"id": "local", "label": "Specify local file"},
        {"id": "none", "label": "No reference image (generate from text)"}
      ],
      "allow_multiple": false
    }
  ]
}
```

## Step 2: Gather Additional Information

Based on the answers above, request the following additional information via text input:

1. **Main message/catchphrase**: Text to display on the banner
2. **Sub-copy (optional)**: Supplementary information, details
3. **CTA (call to action)**: e.g., "Sign up now", "Learn more"
4. **Brand name/logo (optional)**: Company or service name to display
5. **Brand colors (when "brand" is selected for color_scheme)**: HEX code e.g., #FF5733
6. **Custom size (when "custom" is selected)**: width x height e.g., 1200x800
7. **Reference image search keywords/URL/path (depending on reference_type selection)**
8. **Session name**: Output folder name (e.g., summer_sale_campaign)

## Step 3: Run the Tool

Using the collected information, execute the following command (can also be delegated to the media-generator sub-agent):

```bash
uv run python tools/banner_creator.py \
  --platform "{platform}" \
  --message "{main_message}" \
  --tone "{tone}" \
  --color-scheme "{color_scheme}" \
  --font-style "{font_style}" \
  --priority "{priority}" \
  --session "{session_name}" \
  --with-copy
```

### Optional Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--platform` | Platform (required) | `x_post`, `instagram_feed` |
| `--message` | Main message (required) | `"Summer sale now on"` |
| `--tone` | Tone | `professional`, `pop` |
| `--color-scheme` | Color scheme | `warm`, `cool`, `#FF5733` |
| `--font-style` | Font | `gothic`, `bold` |
| `--priority` | Focus point | `ctr`, `brand` |
| `--sub-copy` | Sub-copy | `"Up to 50% OFF"` |
| `--cta` | CTA text | `"Check it out now"` |
| `--brand-name` | Brand name | `"MyCompany"` |
| `--reference` | Reference image path/URL | `./ref.png` or URL |
| `--search-ref` | Search for reference images | `"SaaS ad banner"` |
| `--session` | Session name | `"summer_campaign"` |
| `--with-copy` | Also generate post copy | Flag |
| `--variants` | Number of variants | `3` |
| `--output` | Output destination | `./output/banner.png` |

## Step 4: Report Results

After generation is complete, report the following:

1. **Path of the generated banner image**
2. **Generated copy text** (when --with-copy is specified)
   - 3 post text variations
   - Hashtag suggestions
   - CTA phrases
3. **Variants** (when --variants is specified)

## Usage Examples

### X post banner
```bash
uv run python tools/banner_creator.py \
  --platform x_post \
  --message "Work Reform in the AI Era" \
  --sub-copy "Free Webinar" \
  --cta "Sign up now" \
  --tone professional \
  --color-scheme cool \
  --font-style bold \
  --priority ctr \
  --session "webinar_promotion" \
  --with-copy
```

### Instagram feed (with reference image search)
```bash
uv run python tools/banner_creator.py \
  --platform instagram_feed \
  --message "New Product Launch" \
  --tone pop \
  --color-scheme vivid \
  --search-ref "cosmetics new product Instagram ad" \
  --with-copy
```

### PR Times press release image
```bash
uv run python tools/banner_creator.py \
  --platform prtimes \
  --message "Company X Announces New Service" \
  --brand-name "Company X" \
  --tone professional \
  --color-scheme "#1E40AF" \
  --font-style gothic \
  --priority info
```

## Notes

- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` to be set in environment variables
- Generated images are saved to `docs/generated/banners/{date}_{session_name}/`
- The `--with-copy` option also generates post text simultaneously
- Browser tools are used for reference image retrieval via web search
