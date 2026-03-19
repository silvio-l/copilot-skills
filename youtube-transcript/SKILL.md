---
name: youtube-transcript
description: >
  Fetch and analyze YouTube video transcripts. Use this skill when the user
  asks to analyze a YouTube video, get a transcript, summarize a video, or
  extract information from a YouTube URL. Works with any video that has
  captions (manual or auto-generated). No API key required.
---

# YouTube Transcript Analysis Skill

## Overview

This skill fetches transcripts (subtitles/captions) from YouTube videos using
the `youtube-transcript-api` Python library. It works with both manually
created and auto-generated (ASR) subtitles. No API key or authentication
is required.

## Prerequisites

The `youtube-transcript-api` package must be installed:

```powershell
pip install youtube-transcript-api
```

If the package is not installed, install it before proceeding. Use the direct
Python path if the shim doesn't work: `C:\Python314\python.exe -m pip install youtube-transcript-api`

## Extracting the Video ID

YouTube URLs come in several formats. Extract the video ID:

| URL Format | Video ID |
|---|---|
| `https://www.youtube.com/watch?v=dQw4w9WgXcQ` | `dQw4w9WgXcQ` |
| `https://youtu.be/dQw4w9WgXcQ` | `dQw4w9WgXcQ` |
| `https://www.youtube.com/embed/dQw4w9WgXcQ` | `dQw4w9WgXcQ` |
| `https://www.youtube.com/v/dQw4w9WgXcQ` | `dQw4w9WgXcQ` |
| `https://www.youtube.com/shorts/dQw4w9WgXcQ` | `dQw4w9WgXcQ` |

The video ID is always 11 characters (letters, digits, hyphens, underscores).

## Usage

### Step 1: List Available Transcripts

Always list available transcripts first to know what languages are available:

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list("VIDEO_ID")

for t in transcript_list:
    print(f"{t.language} ({t.language_code}) [auto={t.is_generated}]")
```

### Step 2: Fetch Transcript

Fetch with language preference (tries each in order, falls back):

```python
# Fetch with language preference
transcript = ytt_api.fetch("VIDEO_ID", languages=["de", "en"])

# Or fetch default (usually English or video's language)
transcript = ytt_api.fetch("VIDEO_ID")

# Get plain text (no timestamps)
full_text = " ".join([snippet.text for snippet in transcript])
print(full_text)
```

### Step 3: Fetch with Timestamps

For detailed analysis with timing information:

```python
transcript = ytt_api.fetch("VIDEO_ID")
for snippet in transcript:
    start = snippet.start  # seconds (float)
    duration = snippet.duration  # seconds (float)
    text = snippet.text
    minutes = int(start // 60)
    seconds = int(start % 60)
    print(f"[{minutes:02d}:{seconds:02d}] {text}")
```

### Translation

If a transcript is translatable, you can translate it:

```python
transcript_list = ytt_api.list("VIDEO_ID")
en_transcript = transcript_list.find_transcript(["en"])

if en_transcript.is_translatable:
    de_transcript = en_transcript.translate("de")
    translated = de_transcript.fetch()
    text = " ".join([s.text for s in translated])
```

## Complete Analysis Script

Use this all-in-one script for quick analysis. Pipe the video ID via stdin
or pass it as argument in the Python code:

```python
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url_or_id):
    """Extract YouTube video ID from various URL formats or return as-is."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

def fetch_transcript(video_id, languages=None):
    """Fetch transcript and return metadata + full text."""
    ytt_api = YouTubeTranscriptApi()

    # List available transcripts
    transcript_list = ytt_api.list(video_id)
    available = []
    for t in transcript_list:
        available.append({
            "language": t.language,
            "code": t.language_code,
            "auto": t.is_generated,
            "translatable": t.is_translatable,
        })

    # Fetch transcript
    if languages:
        transcript = ytt_api.fetch(video_id, languages=languages)
    else:
        transcript = ytt_api.fetch(video_id)

    # Build output
    segments = []
    for snippet in transcript:
        segments.append({
            "start": snippet.start,
            "duration": snippet.duration,
            "text": snippet.text,
        })

    full_text = " ".join([s["text"] for s in segments])

    return {
        "video_id": video_id,
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
        "available_transcripts": available,
        "segment_count": len(segments),
        "char_count": len(full_text),
        "word_count": len(full_text.split()),
        "segments": segments,
        "full_text": full_text,
    }

# --- Main ---
if __name__ == "__main__":
    video_input = sys.argv[1] if len(sys.argv) > 1 else input("YouTube URL or ID: ")
    video_id = extract_video_id(video_input.strip())
    if not video_id:
        print(f"Error: Could not extract video ID from: {video_input}")
        sys.exit(1)

    langs = None
    if len(sys.argv) > 2:
        langs = sys.argv[2].split(",")

    result = fetch_transcript(video_id, langs)

    print(f"Video ID: {result['video_id']}")
    print(f"Language: {result['language']} ({result['language_code']})")
    print(f"Auto-generated: {result['is_generated']}")
    print(f"Segments: {result['segment_count']}")
    print(f"Words: {result['word_count']} | Chars: {result['char_count']}")
    print(f"\nAvailable transcripts:")
    for a in result['available_transcripts']:
        print(f"  - {a['language']} ({a['code']}) [auto={a['auto']}]")
    print(f"\n--- FULL TRANSCRIPT ---\n")
    print(result['full_text'])
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|---|---|---|
| `TranscriptsDisabled` | Video has no captions | Cannot be resolved — the uploader disabled captions |
| `NoTranscriptFound` | Requested language unavailable | List available languages first, use fallback |
| `VideoUnavailable` | Video is private/deleted/region-blocked | Cannot be resolved |
| `TooManyRequests` | Rate limited by YouTube | Wait and retry, or use a proxy |
| `InvalidVideoId` | Malformed video ID | Check URL parsing |

## Workflow for the Agent

When a user asks to analyze a YouTube video:

1. **Extract the video ID** from the URL using regex
2. **Run the analysis script** (write it to a temp file, execute with Python)
3. **Read the full transcript** output
4. **Analyze/summarize** the transcript as requested
5. **Clean up** the temp script file

### Important Notes

- Always use `C:\Python314\python.exe` as the Python executable if `python` doesn't work
- The transcript text may contain auto-generated artifacts (repeated words, missing punctuation)
- Auto-generated transcripts have no punctuation — consider adding it for readability
- Some videos have multiple language tracks — prefer manual over auto-generated
- Very long videos produce large transcripts — consider chunking for analysis
- The library does NOT download the video, only the text captions
