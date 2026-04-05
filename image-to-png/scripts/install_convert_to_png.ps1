<#
.SYNOPSIS
    Installer for "In PNG umwandeln" — image-to-PNG converter.

.DESCRIPTION
    Sets up a "Send To" shortcut so you can right-click image files
    and send them to "In PNG umwandeln" for quick PNG conversion.

.PARAMETER Uninstall
    Remove the Send To shortcut.

.EXAMPLE
    .\install_convert_to_png.ps1
    .\install_convert_to_png.ps1 -Uninstall
#>

param(
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

$SkillDir = Split-Path -Parent $PSScriptRoot
$ScriptsDir = Join-Path $SkillDir "scripts"
$ConverterCmd = Join-Path $ScriptsDir "convert_to_png.cmd"
$ConverterPy = Join-Path $ScriptsDir "convert_to_png.py"
$PromptCmd = Join-Path $ScriptsDir "build_image_prompt.cmd"
$PromptPy = Join-Path $ScriptsDir "build_image_prompt.py"
$SendToDir = [System.IO.Path]::Combine($env:APPDATA, "Microsoft", "Windows", "SendTo")
$ShortcutName = "In PNG umwandeln.lnk"
$ShortcutPath = Join-Path $SendToDir $ShortcutName
$PromptShortcutName = "Bilder analysieren (KI-Prompt).lnk"
$PromptShortcutPath = Join-Path $SendToDir $PromptShortcutName

function Install-PillowHeif {
    Write-Host "Pruefe pillow-heif..." -ForegroundColor Cyan
    $check = & C:\Python314\python.exe -c "import pillow_heif; print('ok')" 2>&1
    if ($check -ne "ok") {
        Write-Host "  pillow-heif nicht installiert. HEIC-Konvertierung nutzt ffmpeg als Fallback." -ForegroundColor Yellow
        Write-Host "  Manuell installieren: pip install pillow-heif" -ForegroundColor Yellow
    } else {
        Write-Host "  pillow-heif bereits installiert." -ForegroundColor Green
    }
}

function Install-SendToShortcut {
    Write-Host ""
    Write-Host "=== In PNG umwandeln — Installer ===" -ForegroundColor Cyan
    Write-Host ""

    # Verify converter exists
    if (-not (Test-Path $ConverterCmd)) {
        Write-Error "Konverterskript nicht gefunden: $ConverterCmd"
        return
    }
    if (-not (Test-Path $ConverterPy)) {
        Write-Error "Python-Skript nicht gefunden: $ConverterPy"
        return
    }

    # Install pillow-heif
    Install-PillowHeif

    # Create Send To shortcut
    Write-Host ""
    Write-Host "Erstelle 'Senden an'-Verknuepfung..." -ForegroundColor Cyan

    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $ConverterCmd
    $Shortcut.WorkingDirectory = $ScriptsDir
    $Shortcut.Description = "Bilddateien in PNG-Format umwandeln"
    $Shortcut.IconLocation = "imageres.dll,67"
    $Shortcut.Save()

    if (Test-Path $ShortcutPath) {
        Write-Host "  Verknuepfung erstellt: $ShortcutPath" -ForegroundColor Green
    } else {
        Write-Error "Verknuepfung konnte nicht erstellt werden."
        return
    }

    # Create Send To shortcut for image prompt builder
    Write-Host ""
    Write-Host "Erstelle 'Senden an'-Verknuepfung fuer KI-Prompt..." -ForegroundColor Cyan

    if ((Test-Path $PromptCmd) -and (Test-Path $PromptPy)) {
        $PromptSc = $WshShell.CreateShortcut($PromptShortcutPath)
        $PromptSc.TargetPath = $PromptCmd
        $PromptSc.WorkingDirectory = $ScriptsDir
        $PromptSc.Description = "KI-Analyse-Prompt fuer Bilder erstellen und in Zwischenablage kopieren"
        $PromptSc.IconLocation = "imageres.dll,76"
        $PromptSc.Save()

        if (Test-Path $PromptShortcutPath) {
            Write-Host "  Verknuepfung erstellt: $PromptShortcutPath" -ForegroundColor Green
        } else {
            Write-Host "  Warnung: Prompt-Verknuepfung konnte nicht erstellt werden." -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Prompt-Skripte nicht gefunden — uebersprungen." -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "=== Installation abgeschlossen ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Nutzung:" -ForegroundColor White
    Write-Host "  1. Bilddatei(en) im Explorer markieren" -ForegroundColor Gray
    Write-Host "  2. Rechtsklick -> Weitere Optionen anzeigen -> Senden an -> 'In PNG umwandeln'" -ForegroundColor Gray
    Write-Host "     oder -> 'Bilder analysieren (KI-Prompt)'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Unterstuetzte Formate:" -ForegroundColor White
    Write-Host "  WebP, AVIF, BMP, TIFF, GIF, PSD, TGA, ICO, HEIC/HEIF," -ForegroundColor Gray
    Write-Host "  JPEG2000, PCX, PPM, SGI, QOI, und weitere" -ForegroundColor Gray
    Write-Host ""
}

function Uninstall-SendToShortcut {
    Write-Host ""
    Write-Host "=== In PNG umwandeln — Deinstallation ===" -ForegroundColor Cyan
    Write-Host ""

    if (Test-Path $ShortcutPath) {
        Remove-Item $ShortcutPath -Force
        Write-Host "  'Senden an'-Verknuepfung entfernt: In PNG umwandeln" -ForegroundColor Green
    } else {
        Write-Host "  Keine PNG-Verknuepfung gefunden." -ForegroundColor Yellow
    }

    if (Test-Path $PromptShortcutPath) {
        Remove-Item $PromptShortcutPath -Force
        Write-Host "  'Senden an'-Verknuepfung entfernt: Bilder analysieren (KI-Prompt)" -ForegroundColor Green
    } else {
        Write-Host "  Keine Prompt-Verknuepfung gefunden." -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "=== Deinstallation abgeschlossen ===" -ForegroundColor Green
    Write-Host ""
}

# Main
if ($Uninstall) {
    Uninstall-SendToShortcut
} else {
    Install-SendToShortcut
}
