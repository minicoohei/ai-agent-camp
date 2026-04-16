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

## Typefully API v2

### Authentication
Environment variable: `TYPEFULLY_API_KEY`
Header: `Authorization: Bearer $TYPEFULLY_API_KEY`

### Retrieving social_set_id (required)

All v2 endpoints require a social_set_id. Fetch it first.

```bash
curl -X GET "https://api.typefully.com/v2/social-sets" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY"
# Copy the id from the response and save to an env var
export TYPEFULLY_SOCIAL_SET_ID="the-id-you-got"
```

### Endpoints

#### Create Draft (single X post)
```bash
curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [{"text": "Post text"}]
      }
    },
    "publish_at": "2025-01-15T09:00:00Z"
  }'
```

#### Thread Posting
Arrange multiple entries in the `posts` array (v1's `\n\n\n\n` + `threadify` are deprecated).
```json
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [
        {"text": "1/🧵 Hook"},
        {"text": "2/ Main point"},
        {"text": "3/ CTA"}
      ]
    }
  }
}
```

#### Scheduled Posting
- `publish_at`: ISO 8601 format (UTC)
- `publish_at: "next-free-slot"` to auto-place at the next available slot

#### X and Threads Simultaneous Posting
```json
{
  "platforms": {
    "x":       {"enabled": true, "posts": [{"text": "Text"}]},
    "threads": {"enabled": true, "posts": [{"text": "Text"}]}
  },
  "publish_at": "next-free-slot"
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
