@echo off
:: In PNG umwandeln — Send To wrapper
:: Calls convert_to_png.py with all dropped files
:: Hidden window via pythonw to avoid console flash

setlocal
set "SCRIPT_DIR=%~dp0"
set "CONVERTER=%SCRIPT_DIR%convert_to_png.py"

:: Use pythonw for no-console, fall back to python
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw "%CONVERTER%" %*
) else (
    start "" python "%CONVERTER%" %*
)
