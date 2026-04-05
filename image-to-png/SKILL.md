---
name: image-to-png
description: >
  MUST USE for image format conversion to PNG or AI image analysis prompts. Invoke when user asks to:
  convert images (WebP, AVIF, HEIC, BMP, TIFF, GIF, PSD, RAW) to PNG, batch convert, install/troubleshoot
  Windows "Send To" converter, build AI prompts for deep image/UI/screenshot analysis, or handle non-standard
  image formats. Triggers on: image conversion, WebP/AVIF/HEIC, "Senden an", AI image prompt, UI review from images.
  German: 'Bild umwandeln', 'Bilder konvertieren', 'In PNG umwandeln', 'Bilder analysieren', 'KI-Prompt für Bilder'.
  Provides Python conversion script and AI prompt builder with Windows Send To integration.
  Auto-converts non-PNG/JPG before prompt building so AI can process all images.
---

# Image-to-PNG Converter & AI Image Analysis Prompt Builder

Converts image files to PNG format and builds comprehensive AI analysis prompts — both via Windows "Send To" integration.

## What's Included

```
image-to-png/
├── SKILL.md              (this file)
└── scripts/
    ├── convert_to_png.py           (PNG converter — Python + Pillow)
    ├── convert_to_png.cmd          (Send To wrapper for converter)
    ├── build_image_prompt.py       (AI prompt builder)
    ├── build_image_prompt.cmd      (Send To wrapper for prompt builder)
    └── install_convert_to_png.ps1  (installer/uninstaller for both)
```

## Supported Formats

| Format | Extensions | Engine |
|--------|-----------|--------|
| WebP | `.webp` | Pillow |
| AVIF | `.avif`, `.avifs` | Pillow |
| BMP | `.bmp`, `.dib` | Pillow |
| TIFF | `.tiff`, `.tif` | Pillow |
| GIF | `.gif` | Pillow |
| PSD | `.psd` | Pillow |
| TGA | `.tga`, `.icb`, `.vda`, `.vst` | Pillow |
| ICO | `.ico` | Pillow |
| JPEG2000 | `.jp2`, `.j2k`, `.j2c` | Pillow |
| HEIC/HEIF | `.heic`, `.heif`, `.hif` | pillow-heif (oder ffmpeg) |
| RAW | `.cr2`, `.nef`, `.arw`, `.dng` | ffmpeg |
| QOI | `.qoi` | Pillow |
| PCX | `.pcx` | Pillow |
| PPM | `.pbm`, `.pgm`, `.ppm` | Pillow |
| SGI | `.sgi`, `.rgb`, `.rgba` | Pillow |

PNG and JPG/JPEG files are automatically skipped (not reconverted).

## Installation

Run the installer script:

```powershell
& "C:\Users\silvi\.copilot\skills\image-to-png\scripts\install_convert_to_png.ps1"
```

This creates two "Send To" shortcuts. After installation:

### In PNG umwandeln
1. Select image file(s) in Explorer
2. Right-click → "Weitere Optionen anzeigen" → "Senden an" → "In PNG umwandeln"
3. PNG files appear in the same directory

### Bilder analysieren (KI-Prompt)
1. Select image file(s) in Explorer
2. Right-click → "Weitere Optionen anzeigen" → "Senden an" → "Bilder analysieren (KI-Prompt)"
3. A comprehensive AI analysis prompt is copied to your clipboard
4. Paste (Ctrl+V) into any AI chat — the prompt references all selected images and instructs the AI to deeply analyze them (composition, colors, UI/UX, design patterns, etc.)

## Uninstallation

```powershell
& "C:\Users\silvi\.copilot\skills\image-to-png\scripts\install_convert_to_png.ps1" -Uninstall
```

## Direct Usage (CLI)

### PNG Conversion
```bash
python "C:\Users\silvi\.copilot\skills\image-to-png\scripts\convert_to_png.py" file1.webp file2.avif
```

### AI Analysis Prompt
```bash
python "C:\Users\silvi\.copilot\skills\image-to-png\scripts\build_image_prompt.py" screenshot1.png mockup.webp
```
The prompt is copied to clipboard and ready to paste into any AI chat.

## Dependencies

- **Python 3.x** with **Pillow** (required — already installed)
- **pillow-heif** (optional — for HEIC/HEIF, installer tries to set up)
- **ffmpeg** (optional fallback — already installed on this system)

## Troubleshooting

If the "Send To" entry doesn't appear:
1. Check that the shortcut exists: `Get-ChildItem "$env:APPDATA\Microsoft\Windows\SendTo" | Where-Object { $_.Name -like "*PNG*" }`
2. Re-run the installer
3. On Windows 11: Use "Weitere Optionen anzeigen" (Shift+F10) to see the classic context menu with "Send To"

If HEIC conversion fails:
1. Try installing `pillow-heif`: `pip install pillow-heif`
2. Or ensure ffmpeg is in PATH: `where.exe ffmpeg`

If the conversion window flashes briefly:
- This is expected — the script runs and shows a result dialog
- If no dialog appears, check that Python is in PATH
