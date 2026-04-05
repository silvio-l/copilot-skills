@echo off
:: Bilder analysieren (KI-Prompt) — Send To wrapper
:: Calls build_image_prompt.py with all dropped files
:: Hidden window via pythonw/pyw to avoid console flash

setlocal
set "SCRIPT_DIR=%~dp0"
set "PROMPTER=%SCRIPT_DIR%build_image_prompt.py"

:: Try pythonw first (no console), then pyw launcher, then python
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw "%PROMPTER%" %*
    goto :eof
)
where pyw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pyw -3 "%PROMPTER%" %*
    goto :eof
)
where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python "%PROMPTER%" %*
    goto :eof
)
where py >nul 2>&1
if %errorlevel% equ 0 (
    start "" py -3 "%PROMPTER%" %*
    goto :eof
)
echo Python nicht gefunden. Bitte Python installieren.
pause
