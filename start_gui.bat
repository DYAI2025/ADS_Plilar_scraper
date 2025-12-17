@echo off
REM ADS Pillar Scraper - One-Click GUI Start (Windows)
REM Startet automatisch die GUI mit allen benötigten Services

echo.
echo ========================================
echo  ADS Pillar Scraper - GUI Start
echo ========================================
echo.

REM Prüfe Python Installation
echo [1/4] Pruefe Python-Installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FEHLER] Python ist nicht installiert!
    echo Bitte installieren Sie Python 3.8+ von https://python.org
    echo Wichtig: "Add Python to PATH" aktivieren!
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% gefunden
echo.

REM Prüfe Dependencies
echo [2/4] Pruefe Dependencies...
python -c "import pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNUNG] Dependencies nicht installiert - Installation wird gestartet...
    echo.

    if exist requirements.txt (
        pip install -r requirements.txt -q
        echo [OK] Dependencies installiert
    ) else (
        echo [FEHLER] requirements.txt nicht gefunden!
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependencies vorhanden
)
echo.

REM Prüfe Tkinter (normalerweise vorinstalliert auf Windows)
echo [3/4] Pruefe GUI-Unterstuetzung...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [FEHLER] Tkinter ist nicht verfügbar!
    echo Bitte installieren Sie Python neu mit Tcl/Tk Option.
    pause
    exit /b 1
)
echo [OK] GUI-Unterstuetzung verfuegbar
echo.

REM Erstelle Arbeitsverzeichnisse
echo [4/4] Erstelle Arbeitsverzeichnisse...
if not exist "data" mkdir data
if not exist "generated" mkdir generated
echo [OK] Verzeichnisse bereit
echo.

REM Starte GUI
echo ========================================
echo  GUI wird gestartet...
echo ========================================
echo.

REM Wechsle ins Files-Verzeichnis falls nötig
if exist "Files\gui_app.py" (
    cd Files
    python gui_app.py
) else if exist "gui_app.py" (
    python gui_app.py
) else (
    echo [FEHLER] gui_app.py nicht gefunden!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  GUI wurde beendet. Bis bald!
echo ========================================
pause
