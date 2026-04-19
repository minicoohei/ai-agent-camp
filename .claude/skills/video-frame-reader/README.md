# video-frame-reader

A Claude Code skill that extracts keyframes from video files and analyzes their content using AI.

## Features

- **Smart Keyframe Extraction**: Automatically removes duplicate/similar frames using correlation-based similarity detection
- **Token Optimization**: Compresses and resizes images to minimize API token consumption
- **Cost Estimation**: Calculates estimated costs for Opus, Sonnet, and Haiku models before analysis
- **Subagent Analysis**: Uses Haiku model for cost-efficient frame analysis

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- ffmpeg (for video frame extraction)
- Python 3 with Pillow and numpy

## Installation

1. Clone this repository to your Claude skills directory:

```bash
git clone https://github.com/YOUR_USERNAME/video-frame-reader.git ~/skills/video-frame-reader
```

2. Install Python dependencies:

```bash
# uv で依存関係をインストール
uv add Pillow numpy
```

## Usage

Simply provide a video file to Claude Code:

```
User: /path/to/video.mp4 - analyze this screen recording
```

Claude will:
1. Extract keyframes from the video
2. Show you the estimated token count and cost
3. Ask for confirmation before analysis
4. Analyze the frames using a Haiku subagent

## Options

The extraction script supports several options:

| Option | Default | Description |
|--------|---------|-------------|
| `-t, --threshold` | 0.85 | Similarity threshold (higher = more frames kept) |
| `-q, --quality` | 30 | JPEG quality (1-100) |
| `-s, --scale` | 0.3 | Resize scale |
| `-o, --output` | `<video>_keyframes/` | Output directory |

### Example: More Aggressive Token Reduction

```bash
python3 extract_keyframes.py video.mp4 -t 0.75 -q 20 -s 0.2
```

## How It Works

1. **Frame Extraction**: Uses ffmpeg to extract all frames from the video
2. **Duplicate Removal**: Calculates normalized cross-correlation between consecutive frames, keeping only frames that differ significantly
3. **Compression**: Resizes and compresses frames to JPEG with configurable quality
4. **Token Calculation**: Estimates tokens based on image dimensions (1M pixels ≈ 1300 tokens)
5. **Cost Estimation**: Calculates costs for different Claude models

## File Structure

```
video-frame-reader/
├── README.md              # This file
├── SKILL.md               # Claude Code skill definition
├── .gitignore
└── scripts/
    └── extract_keyframes.py   # Keyframe extraction script
```

## License

MIT License
