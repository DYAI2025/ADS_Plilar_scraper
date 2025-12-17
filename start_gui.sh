#!/bin/bash
#
# ADS Pillar Scraper - One-Click GUI Start
# Startet automatisch die GUI mit allen benötigten Services
#

set -e  # Exit on error

echo "🚀 ADS Pillar Scraper - GUI wird gestartet..."
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Prüfe Python Installation
echo -e "${BLUE}📋 Prüfe Python-Installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 ist nicht installiert!${NC}"
    echo -e "${YELLOW}   Bitte installieren Sie Python 3.8+ von https://python.org${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION gefunden${NC}"

# Prüfe ob Dependencies installiert sind
echo -e "${BLUE}📦 Prüfe Dependencies...${NC}"
if ! python3 -c "import pandas" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Dependencies nicht installiert - Installation wird gestartet...${NC}"
    echo ""

    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt -q
        echo -e "${GREEN}✅ Dependencies installiert${NC}"
    else
        echo -e "${RED}❌ requirements.txt nicht gefunden!${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Dependencies vorhanden${NC}"
fi

# Prüfe ob Tkinter verfügbar ist
echo -e "${BLUE}🖼️  Prüfe GUI-Unterstützung (Tkinter)...${NC}"
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${RED}❌ Tkinter ist nicht installiert!${NC}"
    echo ""
    echo -e "${YELLOW}Installation-Anleitung:${NC}"
    echo -e "${YELLOW}  macOS:   brew install python-tk@3.11${NC}"
    echo -e "${YELLOW}  Ubuntu:  sudo apt install python3-tk${NC}"
    echo -e "${YELLOW}  Fedora:  sudo dnf install python3-tkinter${NC}"
    exit 1
fi
echo -e "${GREEN}✅ GUI-Unterstützung verfügbar${NC}"

# Erstelle notwendige Verzeichnisse
echo -e "${BLUE}📁 Erstelle Arbeitsverzeichnisse...${NC}"
mkdir -p data generated

# Wechsle ins Files-Verzeichnis
cd Files 2>/dev/null || cd "$(dirname "$0")/Files" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Starte aus Root-Verzeichnis${NC}"
}

# Starte GUI
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎨 GUI wird gestartet...${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Prüfe ob gui_app.py existiert
if [ -f "gui_app.py" ]; then
    python3 gui_app.py
elif [ -f "Files/gui_app.py" ]; then
    python3 Files/gui_app.py
else
    echo -e "${RED}❌ gui_app.py nicht gefunden!${NC}"
    exit 1
fi

# Cleanup bei Exit
echo ""
echo -e "${BLUE}👋 GUI wurde beendet. Bis bald!${NC}"
