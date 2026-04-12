---
name: banner-creator
description: "A skill for generating banners/creatives for various SNS and advertising platforms. Supports X, Facebook, Instagram, PRTimes, YouTube, LINE, and web ads. Triggered by requests like 'create a banner', 'generate ad image', 'SNS image', 'creative production', etc."
triggers:
  - banner-creator
  - create a banner
  - generate ad image
  - SNS image
  - creative production
  - banner creation
  - ad banner
  - banner
  - バナーを作って
  - 広告画像を生成
---

# Banner Creator - Ad Banner/Creative Generation

Generates banners/creatives for various SNS and advertising platforms.

## Features

1. **Platform-specific presets**: X, Facebook, Instagram, PRTimes, YouTube, LINE, web ads
2. **Tone & style settings**: Professional, pop, elegant, and more
3. **Reference image search**: Retrieves reference images via web search from keywords
4. **Copy text generation**: Simultaneously generates post text, hashtags, and CTAs

## Platform-Specific Sizes

| Platform | Size | Aspect Ratio |
|----------|------|--------------|
| x_post | 1200x675 | 16:9 |
| x_card | 800x418 | 1.91:1 |
| facebook | 1200x630 | 1.91:1 |
| facebook_story | 1080x1920 | 9:16 |
| instagram_feed | 1080x1080 | 1:1 |
| instagram_story | 1080x1920 | 9:16 |
| prtimes | 1200x630 | 1.91:1 |
| youtube | 1280x720 | 16:9 |
| line | 1040x1040 | 1:1 |
| web_horizontal | 1200x628 | 1.91:1 |
| web_vertical | 300x600 | 1:2 |

## Usage

```bash
# Basic usage
python scripts/banner_creator.py --platform x_post --message "Catchphrase"

# With copy text generation
python scripts/banner_creator.py --platform instagram_feed --message "New product launch" --with-copy

# With reference image search
python scripts/banner_creator.py --platform facebook --message "Sale" --search-ref "EC sale banner"

# Full options
python scripts/banner_creator.py \
  --platform x_post \
  --message "Main message" \
  --sub-copy "Sub copy" \
  --cta "Sign up now" \
  --tone professional \
  --color-scheme cool \
  --font-style bold \
  --priority ctr \
  --brand-name "Company Name" \
  --session "campaign_name" \
  --with-copy \
  --variants 3
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --platform | Yes | - | Target platform (see table above) |
| --message | Yes | - | Main headline/catchphrase |
| --sub-copy | No | - | Sub-headline or details |
| --cta | No | - | Call-to-action text |
| --tone | No | professional | Tone: professional, casual, pop, elegant, urgent, minimal, tech, natural |
| --color-scheme | No | auto | Color: warm, cool, mono, pastel, vivid, dark, or HEX code |
| --font-style | No | auto | Font: gothic, mincho, handwritten, bold, script, geometric |
| --priority | No | ctr | Focus: ctr, brand, info, emotion, product, event |
| --brand-name | No | - | Brand/company name to display |
| --reference | No | - | Local path or URL to reference image |
| --search-ref | No | - | Keywords to search for reference images |
| --session | No | - | Session name for organizing output |
| --with-copy | No | false | Generate copy text along with image |
| --variants | No | 1 | Number of variations to generate |
| --output | No | auto | Output file path |

## Output

- **Image**: `docs/generated/banners/{date}_{session}/{filename}.png`
- **Copy text** (when --with-copy): Saved as `{filename}_copy.md`
  - 3 post text variations
  - Hashtag suggestions
  - CTA phrases

## Examples

### X Post Banner
```bash
python scripts/banner_creator.py \
  --platform x_post \
  --message "Work Style Reform in the AI Era" \
  --sub-copy "Free Webinar" \
  --cta "Sign up now" \
  --tone professional \
  --with-copy
```

### Instagram Feed with Reference Search
```bash
python scripts/banner_creator.py \
  --platform instagram_feed \
  --message "Summer Collection" \
  --tone pop \
  --color-scheme vivid \
  --search-ref "fashion summer sale instagram"
```

### PRTimes Press Release Image
```bash
python scripts/banner_creator.py \
  --platform prtimes \
  --message "New Service Release Announcement" \
  --brand-name "Company Inc." \
  --tone professional \
  --priority info
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv, requests

## Overview

A skill for automatically generating banners/creatives for various SNS and advertising platforms (X, Facebook, Instagram, PRTimes, YouTube, LINE, web ads) using the Gemini Image Generation API. Supports platform-specific presets, reference image search, and simultaneous copy text generation.

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` as environment variable |
| Image generation failed | Possible Gemini API rate limit. Wait a few seconds and retry |
| Unknown platform | Specify correct preset name for `--platform` (x_post, instagram_feed, etc.) |

## Success Criteria

- [ ] Image is generated at the correct size for the specified platform
- [ ] Output file is saved under `docs/generated/banners/`
- [ ] When `--with-copy` is specified, copy text `.md` file is also generated
