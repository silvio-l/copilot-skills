#!/usr/bin/env python3
"""
convert_to_png.py — Convert image files to PNG format.

Supports: WebP, AVIF, BMP, TIFF, GIF, PSD, TGA, ICO, JPEG2000,
          PCX, PPM, SGI, QOI, HEIC/HEIF, and more.

Usage:
    python convert_to_png.py file1.webp file2.avif ...
    python convert_to_png.py "C:\\path\\to\\image.heic"

Output: PNG file in the same directory with the same base name.
Already-PNG and JPG/JPEG files are skipped.
"""

import sys
import os
import subprocess
import ctypes
from pathlib import Path

SKIP_EXTENSIONS = {".png", ".jpg", ".jpeg"}

PILLOW_SUPPORTED = {
    ".webp", ".avif", ".avifs", ".bmp", ".dib", ".tiff", ".tif",
    ".gif", ".psd", ".tga", ".icb", ".vda", ".vst", ".ico",
    ".jp2", ".j2k", ".j2c", ".jpc", ".jpf", ".jpx",
    ".pcx", ".pbm", ".pgm", ".ppm", ".pnm", ".pfm",
    ".sgi", ".bw", ".rgb", ".rgba", ".qoi",
    ".eps", ".ps", ".dds", ".cur", ".dcx", ".fli", ".flc",
    ".gbr", ".icns", ".im", ".msp", ".ras", ".xbm", ".xpm",
    ".emf", ".wmf",
}

HEIF_EXTENSIONS = {".heic", ".heif", ".hif"}

FFMPEG_FALLBACK_EXTENSIONS = {".raw", ".cr2", ".nef", ".arw", ".dng", ".orf", ".rw2"}


def show_toast(title: str, message: str):
    """Show a Windows toast notification via PowerShell."""
    try:
        ps_script = f"""
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $textNodes = $template.GetElementsByTagName('text')
        $textNodes.Item(0).AppendChild($template.CreateTextNode('{title}')) > $null
        $textNodes.Item(1).AppendChild($template.CreateTextNode('{message}')) > $null
        $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Image Converter').Show($toast)
        """
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, timeout=5,
        )
    except Exception:
        pass


def show_msgbox(title: str, message: str):
    """Show a simple Windows MessageBox as fallback notification."""
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
    except Exception:
        pass


def convert_with_pillow(src: Path, dst: Path) -> bool:
    """Convert using Pillow."""
    from PIL import Image
    img = Image.open(src)
    if img.mode in ("RGBA", "LA", "PA"):
        img.save(dst, "PNG")
    elif img.mode == "P":
        img = img.convert("RGBA")
        img.save(dst, "PNG")
    else:
        img = img.convert("RGB")
        img.save(dst, "PNG")
    return True


def convert_with_heif(src: Path, dst: Path) -> bool:
    """Convert HEIC/HEIF using pillow-heif."""
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
        return convert_with_pillow(src, dst)
    except ImportError:
        return convert_with_ffmpeg(src, dst)


def convert_with_ffmpeg(src: Path, dst: Path) -> bool:
    """Convert using ffmpeg as fallback."""
    ffmpeg = "ffmpeg"
    result = subprocess.run(
        [ffmpeg, "-y", "-i", str(src), str(dst)],
        capture_output=True, timeout=60,
    )
    return result.returncode == 0 and dst.exists()


def convert_file(src_path: str) -> tuple[str, bool, str]:
    """
    Convert a single file to PNG.
    Returns (filename, success, message).
    """
    src = Path(src_path).resolve()

    if not src.exists():
        return (src.name, False, "Datei nicht gefunden")

    ext = src.suffix.lower()

    if ext in SKIP_EXTENSIONS:
        return (src.name, True, "Übersprungen (bereits PNG/JPG)")

    dst = src.with_suffix(".png")

    if dst.exists() and dst != src:
        base = src.stem
        counter = 1
        while dst.exists():
            dst = src.parent / f"{base}_{counter}.png"
            counter += 1

    try:
        if ext in HEIF_EXTENSIONS:
            success = convert_with_heif(src, dst)
        elif ext in PILLOW_SUPPORTED:
            success = convert_with_pillow(src, dst)
        elif ext in FFMPEG_FALLBACK_EXTENSIONS:
            success = convert_with_ffmpeg(src, dst)
        else:
            # Try Pillow first, then ffmpeg
            try:
                success = convert_with_pillow(src, dst)
            except Exception:
                success = convert_with_ffmpeg(src, dst)

        if success and dst.exists():
            size_kb = dst.stat().st_size / 1024
            return (src.name, True, f"→ {dst.name} ({size_kb:.0f} KB)")
        else:
            return (src.name, False, "Konvertierung fehlgeschlagen")

    except Exception as e:
        if dst.exists():
            dst.unlink()
        return (src.name, False, str(e))


def main():
    if len(sys.argv) < 2:
        show_msgbox("In PNG umwandeln", "Keine Dateien ausgewählt.\n\nBitte Bilddateien per Rechtsklick → Senden an → 'In PNG umwandeln' senden.")
        sys.exit(1)

    files = sys.argv[1:]
    results = []

    for f in files:
        name, success, msg = convert_file(f)
        results.append((name, success, msg))

    ok = sum(1 for _, s, _ in results if s)
    fail = sum(1 for _, s, m in results if not s and "Übersprungen" not in m)
    skip = sum(1 for _, _, m in results if "Übersprungen" in m)

    lines = []
    for name, success, msg in results:
        icon = "✅" if success else "❌"
        lines.append(f"{icon} {name}: {msg}")

    summary_parts = []
    if ok - skip > 0:
        summary_parts.append(f"{ok - skip} konvertiert")
    if skip > 0:
        summary_parts.append(f"{skip} übersprungen")
    if fail > 0:
        summary_parts.append(f"{fail} fehlgeschlagen")

    title = "In PNG umwandeln"
    detail = "\n".join(lines)
    summary = " | ".join(summary_parts)

    if len(files) <= 3:
        show_msgbox(title, f"{summary}\n\n{detail}")
    else:
        show_msgbox(title, f"{summary}\n\n{detail[:500]}{'...' if len(detail) > 500 else ''}")


if __name__ == "__main__":
    main()
