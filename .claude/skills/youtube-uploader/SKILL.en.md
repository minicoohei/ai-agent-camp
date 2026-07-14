---
name: youtube-uploader
description: "Video upload skill using YouTube Data API v3. Supports automatic Shorts detection, UTM link auto-insertion, and scheduled publishing. Triggered by 'Post to YouTube', 'Upload video', 'Post Shorts', etc."
status: draft
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

## Implementation Status

> **Draft:** The upload script is not included. No execution command is provided until the implementation is added.

## Planned Features

- **Automatic Shorts Detection**: Vertical (h>w) and 60 seconds or less -> automatically treated as Shorts
- **UTM Link Auto-insertion**: If description doesn't contain ai-agent.camp link, auto-added
- **Resumable Upload**: Stable upload in 10MB chunks
- **Log Saving**: `output/gtm/youtube/upload_YYYYMMDD_HHMMSS.json`

## Dependencies

- `google-api-python-client`, `google-auth` (for upload)
- `ffprobe` (for Shorts detection, optional)
