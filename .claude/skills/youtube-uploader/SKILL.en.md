---
name: youtube-uploader
description: "Video upload skill using YouTube Data API v3. Supports automatic Shorts detection, UTM link auto-insertion, and scheduled publishing. Triggered by 'Post to YouTube', 'Upload video', 'Post Shorts', etc."
triggers:
  - Post to YouTube
  - Upload video
  - Post Shorts
  - Publish YouTube video
  - Set scheduled post
  - youtube-uploader
  - YouTube upload
---

# YouTube Uploader Skill

Video upload via YouTube Data API v3. Supports automatic Shorts detection and UTM link auto-insertion.

## Trigger Words
- YouTube, YouTube post, video upload, Shorts post, YouTube Shorts

## Usage

```bash
# Basic upload (dry-run)
python scripts/gtm/upload_youtube.py --file video.mp4 --title "Title" --description "Description" --dry-run

# Shorts post
python scripts/gtm/upload_youtube.py --file short.mp4 --title "AI Tips" --shorts --dry-run

# Scheduled post
python scripts/gtm/upload_youtube.py --file video.mp4 --title "..." --schedule "2026-03-20T09:00:00Z" --dry-run

# With tags
python scripts/gtm/upload_youtube.py --file video.mp4 --title "..." --tags "AI,agent,no-code" --dry-run
```

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--file` | Yes | - | Video file path |
| `--title` | Yes | - | Video title |
| `--description` | No | - | Description (UTM link auto-added) |
| `--tags` | No | - | Comma-separated tags |
| `--category` | No | 27 | Category ID (27=Education) |
| `--privacy` | No | private | private/unlisted/public |
| `--shorts` | No | false | Force Shorts mode |
| `--language` | No | ja | Video language |
| `--schedule` | No | - | Scheduled post (ISO 8601) |
| `--credentials` | No | env | YouTube auth JSON path |
| `--dry-run` | No | false | Don't upload |

## Features

- **Automatic Shorts Detection**: Vertical (h>w) and 60 seconds or less -> automatically treated as Shorts
- **UTM Link Auto-insertion**: If description doesn't contain ai-agent.camp link, auto-added
- **Resumable Upload**: Stable upload in 10MB chunks
- **Log Saving**: `output/gtm/youtube/upload_YYYYMMDD_HHMMSS.json`

## Dependencies

- `google-api-python-client`, `google-auth` (for upload)
- `ffprobe` (for Shorts detection, optional)
