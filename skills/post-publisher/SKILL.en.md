---
name: post-publisher
description: "Content posting and distribution skill. Posts to X via Typefully, uploads images, and schedules posts. Triggered by requests like 'publish this', 'schedule a post', 'create a Typefully draft', etc."
triggers:
  - publish this
  - post this
  - schedule post
  - Typefully
  - create draft
  - distribute
  - publish
  - schedule post
---

# Post Publisher

Publish and schedule pre-made content to various platforms.

## Supported Platforms

| Platform | Method | Status |
|----------|--------|--------|
| X (Twitter) | Typefully API | ✅ Supported |
| X Threads | Typefully API | ✅ Supported |
| LinkedIn | Typefully API | ✅ Supported |
| Instagram | Manual / Meta API (to be implemented) | 🔧 Planned |
| TikTok | Manual / TikTok API (to be implemented) | 🔧 Planned |
| Note | Manual / API (research needed) | 🔧 Planned |
| Medium | Medium API | 🔧 Planned |

## Typefully API

### Authentication
Environment variable: `TYPEFULLY_API_KEY`

### Endpoints

#### Create Draft
```bash
curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Post text",
    "threadify": false,
    "schedule-date": "2025-01-15T09:00:00Z",
    "auto_retweet_enabled": false,
    "auto_plug_enabled": false
  }'
```

#### Thread Posting
Separate tweets within `content` using `\n\n\n\n` (4 newlines).
```json
{
  "content": "1/🧵 Hook\n\n\n\n2/ Main point\n\n\n\n3/ CTA",
  "threadify": true
}
```

#### Scheduled Posting
- `schedule-date`: ISO 8601 format (UTC)
- `schedule-date: "next-free-slot"` to auto-place at the next available slot

#### Immediate Posting (No Draft)
```json
{
  "content": "Text",
  "schedule-date": "next-free-slot"
}
```

### Posts with Images

The Typefully API does not support direct image uploads. Workflow:
1. Upload image to catbox.moe
2. Post text-only to Typefully draft
3. Attach image URL as a comment (manual attachment may be required)

## Posting Workflow

### Single Post
1. Load content from `marketing/drafts/` (or generate with content-creator)
2. Confirm platform
3. Create draft or schedule via Typefully API
4. Send confirmation message

### Batch Posting
1. Load multiple content pieces from `marketing/drafts/`
2. Distribute schedule (optimize time slots)
3. Batch API calls
4. Send results summary

### Optimal Posting Times (Japan Market)
| Day | X | Instagram | TikTok |
|-----|---|-----------|--------|
| Weekdays | 7-8am, 12pm, 6-9pm | 12pm, 6-9pm | 6-10pm |
| Weekends | 9-11am, 2-4pm | 10am-12pm, 3-5pm | 12-10pm |

## Logging

Record posting results in `marketing/post-log.md`:
```markdown
| Date/Time | Platform | Content Summary | URL | Status |
```

## Related Skills

- `marketing-planner` — Strategy planning
- `content-creator` — Content creation
