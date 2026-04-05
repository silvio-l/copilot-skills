"""
Build a comprehensive AI image analysis prompt and copy to clipboard.

Usage:
    python build_image_prompt.py image1.webp image2.png ...

Accepts image file paths as arguments, builds a structured prompt for deep
image analysis (general + UI/UX), and copies it to the Windows clipboard.
"""

import sys
import os
import subprocess
import ctypes

# Image extensions accepted by this tool
IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp",
    ".avif", ".avifs", ".heic", ".heif", ".hif", ".psd", ".tga", ".ico",
    ".jp2", ".j2k", ".j2c", ".pcx", ".pbm", ".pgm", ".ppm", ".sgi",
    ".rgb", ".rgba", ".qoi", ".dib", ".icb", ".vda", ".vst", ".svg",
    ".cr2", ".nef", ".arw", ".dng", ".orf", ".rw2",
}

# Extensions that most AI chat interfaces can process directly
AI_NATIVE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}


def get_image_info(filepath):
    """Gather basic image metadata if Pillow is available."""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            w, h = img.size
            fmt = img.format or "unknown"
            mode = img.mode
            return f"{w}×{h}px, {fmt}, {mode}"
    except Exception:
        ext = os.path.splitext(filepath)[1].lower()
        return f"format: {ext}"


def build_prompt(files):
    """Build the analysis prompt referencing all provided images."""
    n = len(files)
    plural = n > 1

    # Image reference block — include full paths so the AI can locate files on disk
    ref_lines = []
    for i, f in enumerate(files, 1):
        info = get_image_info(f)
        ref_lines.append(f"  [{i}] \"{f}\" ({info})")
    ref_block = "\n".join(ref_lines)

    # Core prompt
    prompt = f"""You are an expert visual analyst. I am providing you with {n} image{"s" if plural else ""} for thorough, in-depth analysis.

**Important:** The image{"s are" if plural else " is"} uploaded alongside this prompt. Please analyze the uploaded image{"s" if plural else ""} matching the references below.

## Referenced Images

{ref_block}

## Your Task

Analyze {"each image" if plural else "the image"} **comprehensively and meticulously**. Take your time — depth and completeness matter more than brevity. Cover every aspect below that applies.

### 1. General Image Analysis

For {"each image" if plural else "the image"}, describe:

- **Subject & Content**: What is depicted? Identify all key elements, objects, text, people, icons, or scenes visible.
- **Composition & Layout**: How are elements arranged? Describe visual hierarchy, alignment, spacing, balance, symmetry, and flow.
- **Color Palette**: Extract the dominant and accent colors. Describe the overall color mood (warm/cool/neutral), contrast levels, and color harmony (complementary, analogous, monochromatic, etc.).
- **Typography** (if text is present): Identify font styles (serif, sans-serif, monospace, display), sizes, weights, letter-spacing, line-height, and readability.
- **Visual Style**: Is it photographic, illustrative, flat, skeuomorphic, neumorphic, glassmorphic, minimal, bold, playful, corporate? Describe the overall aesthetic language.
- **Image Quality**: Sharpness, resolution, artifacts, compression quality, noise levels.
- **Mood & Tone**: What feeling or atmosphere does the image convey?

### 2. UI/UX Analysis (if the image shows a user interface)

If {"any image" if plural else "the image"} depicts a user interface (app screen, website, dashboard, dialog, settings, etc.), provide a deep UI/UX analysis:

- **Screen Type & Purpose**: What kind of screen is this? (Login, dashboard, settings, list view, detail view, onboarding, modal, etc.) What is the user supposed to accomplish here?
- **Information Architecture**: How is information structured and grouped? Are there clear sections, cards, or containers? Is the hierarchy logical?
- **Component Inventory**: List all UI components visible (buttons, inputs, toggles, tabs, navigation bars, cards, lists, modals, tooltips, badges, avatars, etc.) and note their styling.
- **Navigation & User Flow**: How does the user navigate? What are the primary and secondary actions? Is the call-to-action clear?
- **Design System Consistency**: Do components look like they belong to a cohesive design system? Are there consistent border radii, shadows, spacing units, color tokens?
- **Spacing & Grid**: Analyze padding, margins, gaps. Is there a visible spacing scale? Does the layout follow a grid system?
- **Color System**: Identify primary, secondary, accent, background, surface, text, and state colors (hover, active, disabled, error, success). Is there a light/dark mode indicator?
- **Typography System**: Heading levels, body text, captions, labels — are they consistent? Is there a clear type scale?
- **Iconography**: Style of icons (outlined, filled, duotone, custom), consistency, sizing.
- **Interactive Elements & States**: Buttons, links, inputs — can you infer hover/active/disabled states from what's visible?
- **Responsiveness Cues**: Any indication of how the layout adapts to different screen sizes?
- **Accessibility**: Contrast ratios (estimate), text sizes, touch target sizes, color-only indicators.
- **Polish & Attention to Detail**: Micro-interactions implied, transitions, shadows, gradients, borders, subtle textures, animation cues.
- **Design Patterns**: Identify known UI patterns (e.g., bottom navigation, hamburger menu, floating action button, infinite scroll, skeleton loading, empty states, pull-to-refresh).
- **Platform Conventions**: Does it follow iOS HIG, Material Design, Windows Fluent, or a custom design language?"""

    if plural:
        prompt += """

### 3. Comparative Analysis

Since multiple images are provided:

- **Commonalities**: What visual patterns, components, colors, or styles are shared across the images?
- **Differences**: Where do they diverge in layout, color, typography, or approach?
- **Consistency Assessment**: Do they appear to belong to the same product/brand/design system?
- **Evolution or Variants**: If they show different screens of the same product, describe the design continuity and any inconsistencies."""

    prompt += """

### Output Format

Structure your response with clear headings for each image (use the reference numbers). Be specific — reference exact positions ("top-left", "below the header"), exact colors where possible (hex values or color names), and exact component names. Quote any visible text. When analyzing UI, think like a senior product designer conducting a design audit.

**Be thorough. Be precise. Miss nothing.**"""

    return prompt


def copy_to_clipboard(text):
    """Copy text to Windows clipboard via PowerShell."""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value $input"],
            input=text,
            encoding="utf-8",
            capture_output=True,
            timeout=10,
        )
        return proc.returncode == 0
    except Exception:
        return False


def show_msgbox(title, message, icon=0x40):
    """Show a Windows MessageBox. icon: 0x40=info, 0x30=warning, 0x10=error."""
    ctypes.windll.user32.MessageBoxW(0, message, title, icon)


def main():
    if len(sys.argv) < 2:
        show_msgbox(
            "Bilder analysieren",
            "Keine Dateien übergeben.\n\n"
            "Nutzung: Bilddateien markieren → Rechtsklick → Senden an → "
            "\"Bilder analysieren (KI-Prompt)\"",
            0x30,
        )
        sys.exit(1)

    files = sys.argv[1:]

    # Filter to existing image files only
    valid = []
    missing = []
    skipped = []
    for f in files:
        if not os.path.isfile(f):
            missing.append(f)
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            skipped.append(f)
            continue
        valid.append(os.path.abspath(f))

    if not valid:
        show_msgbox(
            "Bilder analysieren",
            "Keine gültigen Dateien gefunden.",
            0x10,
        )
        sys.exit(1)

    # Auto-convert non-PNG/JPG images so AI chat can process them
    final_files = []
    converted = []
    convert_failed = []
    for f in valid:
        ext = os.path.splitext(f)[1].lower()
        if ext in AI_NATIVE_EXTENSIONS:
            final_files.append(f)
        else:
            # Import converter from sibling script
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                sys.path.insert(0, script_dir)
                from convert_to_png import convert_file
                name, success, msg = convert_file(f)
                if success and "Übersprungen" not in msg:
                    png_path = os.path.splitext(f)[0] + ".png"
                    if os.path.isfile(png_path):
                        final_files.append(png_path)
                        converted.append((os.path.basename(f), os.path.basename(png_path)))
                    else:
                        final_files.append(f)
                        convert_failed.append(os.path.basename(f))
                elif success:
                    # Was skipped (already PNG/JPG) — use as-is
                    final_files.append(f)
                else:
                    final_files.append(f)
                    convert_failed.append(os.path.basename(f))
            except Exception:
                # Converter not available — use original file
                final_files.append(f)
                convert_failed.append(os.path.basename(f))

    # Build prompt with converted files
    prompt = build_prompt(final_files)

    # Copy to clipboard
    ok = copy_to_clipboard(prompt)

    if ok:
        n = len(final_files)
        names = "\n".join(f"  • {os.path.basename(f)}" for f in final_files)
        msg = (
            f"KI-Analyse-Prompt für {n} Bild{'er' if n > 1 else ''} "
            f"in die Zwischenablage kopiert!\n\n"
            f"Dateien:\n{names}\n\n"
            f"Prompt-Länge: {len(prompt):,} Zeichen\n\n"
            f"Nächste Schritte:\n"
            f"  1. Die oben genannten Dateien im KI-Chat hochladen\n"
            f"  2. Prompt einfügen (Strg+V)"
        )
        if converted:
            conv_list = "\n".join(f"  • {orig} → {png}" for orig, png in converted)
            msg += f"\n\n🔄 Automatisch nach PNG konvertiert:\n{conv_list}"
        if convert_failed:
            msg += f"\n\n⚠ Konvertierung fehlgeschlagen (Original wird referenziert):\n" + "\n".join(f"  • {cf}" for cf in convert_failed)
        if skipped:
            msg += f"\n\n⚠ Übersprungen (kein Bildformat):\n" + "\n".join(f"  • {os.path.basename(s)}" for s in skipped)
        if missing:
            msg += f"\n\n⚠ Nicht gefunden:\n" + "\n".join(f"  • {m}" for m in missing)
        show_msgbox("Bilder analysieren ✓", msg, 0x40)
    else:
        show_msgbox(
            "Bilder analysieren",
            "Fehler beim Kopieren in die Zwischenablage.\n\n"
            "Ist PowerShell verfügbar?",
            0x10,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
