# Video Frame Reader - Video Keyframe Extraction

This command extracts keyframes from videos, optionally performs frame analysis with Gemini Vision, and outputs results as JSON.

## Prerequisites
- `ffmpeg` installed
- Python3 + `Pillow` + `numpy`
- Gemini API key (if performing analysis)

## Execution Steps

1. **Extract parameters**:
   Extract the following information from the user's input.
   - **Video file path** (required)
   - **Output directory** (optional; defaults to `{video_name}_keyframes`)
   - **threshold** (optional, default: 0.85)
   - **quality** (optional, default: 30)
   - **scale** (optional, default: 0.3)
   - **intent** (optional, analysis perspective)
   - **max-frames** (optional, maximum frames for analysis; default: 12)

2. **First-time venv setup** (if not already done):
   ```bash
   cd .cursor/skills/video-frame-reader
   python3 -m venv venv          
   source venv/bin/activate      # macOS/Linux/WSL
   pip install Pillow numpy --quiet
   ```

3. **Extraction + Analysis**:
   ```bash
   uv run python tools/video_frame_analyzer.py "{video_path}" -o "{output_directory}" -t {threshold} -q {quality} -s {scale} --intent "{intent}" --max-frames {max_frames}
   ```

4. **Verify results**:
   - Confirm that the JSON output contains both `extraction` and `analysis`
   - Add `--no-analyze` to skip analysis
   - Display any `error` as-is

## Usage Examples

### Basic
```
/video-frame-reader /path/to/video.mp4
```

### Stronger token reduction
```
/video-frame-reader /path/to/video.mp4 -t 0.75 -q 20 -s 0.2
```

### Specify analysis perspective
```
/video-frame-reader /path/to/video.mp4 --intent "Check if screen transitions after button clicks look natural"
```
