# 🚀 One-Click GUI Start Guide

Starten Sie die ADS Pillar Scraper GUI mit nur einem Klick!

---

## 📋 Schnellstart

### **macOS / Linux:**
```bash
./start_gui.sh
```

### **Windows:**
```cmd
start_gui.bat
```
oder doppelklicken Sie auf `start_gui.bat` im Datei-Explorer

### **Plattformunabhängig (Python):**
```bash
python3 start_gui.py
```

---

## ✨ Was die Scripts machen

Die One-Click-Start-Scripts führen automatisch folgende Schritte aus:

1. ✅ **Python-Version prüfen** (Python 3.8+ erforderlich)
2. ✅ **Dependencies installieren** (falls noch nicht vorhanden)
3. ✅ **Tkinter (GUI) prüfen** (GUI-Bibliothek)
4. ✅ **Arbeitsverzeichnisse erstellen** (data/, generated/)
5. ✅ **GUI starten** (Files/gui_app.py)

**Kein manuelles Setup mehr nötig!** 🎉

---

## 🎨 GUI Verbesserungen

Die neue verbesserte GUI bietet:

### 1. **Größeres Fenster**
- **1400x900 Pixel** (vorher 1200x800)
- Minimum-Größe: 1200x750
- Bessere Übersichtlichkeit für alle Tabs

### 2. **Auto-Save Dialog** ⭐ NEU!
- **Automatische Speicher-Abfrage** beim Tab-Wechsel
- Verhindert Datenverlust

**So funktioniert's:**
```
1. Sie bearbeiten die Projekt-Konfiguration (Tab "🚀 Projekt Setup")
2. Sie wechseln zu einem anderen Tab
3. Dialog erscheint automatisch:

   ┌─────────────────────────────────────────┐
   │  Konfiguration speichern?               │
   ├─────────────────────────────────────────┤
   │  Sie haben die Projekt-Konfiguration    │
   │  geändert.                               │
   │                                          │
   │  Möchten Sie die Änderungen speichern?  │
   │                                          │
   │  • JA = Speichern und fortfahren         │
   │  • NEIN = Änderungen verwerfen           │
   │  • ABBRECHEN = Zurück zum Setup-Tab      │
   └─────────────────────────────────────────┘
```

**Sie KÖNNEN NICHT weitergehen ohne zu:**
- ✅ Speichern (JA)
- ❌ Verwerfen (NEIN)
- ⬅️ Zurückgehen (ABBRECHEN)

### 3. **Explizite API-Benennung** 🔑
- **"Google Places API"** statt nur "API Key"
- Klare Beschreibung: "Google Places API Key (erforderlich für Live-Scraping)"
- **Klickbarer Link** zur Google Cloud Console
- **Show/Hide Button** (👁️) für API Key Sichtbarkeit

**Neue API-Sektion:**
```
╔══════════════════════════════════════════════════╗
║ 🔑 Google Places API Konfiguration              ║
╠══════════════════════════════════════════════════╣
║ Google Places API Key (erforderlich für Live-Scraping)
║
║ ➜ API Key erstellen:                            ║
║   https://console.cloud.google.com/apis/credentials [KLICK]
║
║ API Key: [**********************************] [👁️]
║
║ Search Query: [parks                       ]    ║
╚══════════════════════════════════════════════════╝
```

### 4. **Verbesserte Konfigurationsspeicherung**
- **Automatisches Speichern** nach `project_config.json`
- Kein File-Dialog mehr (schneller Workflow)
- **Statusanzeige**: "✅ Konfiguration gespeichert"

---

## 📝 Detaillierte Anleitung

### Erster Start

1. **Start-Script ausführen:**
   ```bash
   ./start_gui.sh          # macOS/Linux
   start_gui.bat           # Windows
   python3 start_gui.py    # Plattformunabhängig
   ```

2. **Automatische Prüfungen:**
   ```
   🚀 ADS Pillar Scraper - GUI wird gestartet...

   📋 Prüfe Python-Installation...
   ✅ Python 3.11.14 gefunden

   📦 Prüfe Dependencies...
   ✅ Dependencies vorhanden

   🖼️  Prüfe GUI-Unterstützung (Tkinter)...
   ✅ GUI-Unterstützung verfügbar

   📁 Erstelle Arbeitsverzeichnisse...
   ✅ Verzeichnisse bereit

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎨 GUI wird gestartet...
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

3. **GUI öffnet sich automatisch!** ✅

### Tab "🚀 Projekt Setup"

**Pflichtfelder ausfüllen:**
- **Website Name**: z.B. "Berlin Parks Guide"
- **Domain**: z.B. "berlin-parks.de"
- **Stadt**: z.B. "Berlin"
- **Kategorie**: z.B. "Parks"
- **AdSense ID**: z.B. "ca-pub-1234567890123456" (optional)
- **Google Analytics ID**: z.B. "G-XXXXXXXXXX" (optional)

**Speichern:**
- Button "💾 Konfiguration speichern" klicken
- ODER: Zu anderem Tab wechseln → Auto-Save Dialog

### Tab "📊 Daten sammeln"

**NEUE verbesserte API-Sektion:**

1. **Google Places API Key eingeben:**
   - Klicken Sie auf den blauen Link zur Google Cloud Console
   - Erstellen Sie einen API Key (falls noch nicht vorhanden)
   - Kopieren Sie den Key
   - Fügen Sie ihn in das API Key Feld ein
   - **👁️ Button** zum Anzeigen/Verstecken des Keys

2. **Search Query:**
   - Standard: "parks"
   - Anpassen nach Bedarf (z.B. "cafes", "restaurants")

3. **Daten scrapen:**
   - Button "🔍 Daten sammeln" klicken
   - API wird abgefragt
   - Echte Daten werden geladen!

---

## 🛠️ Fehlerbehebung

### "Python ist nicht installiert"
```bash
# macOS:
brew install python@3.11

# Linux:
sudo apt install python3.11

# Windows:
# Download von python.org
# Wichtig: "Add Python to PATH" aktivieren!
```

### "Tkinter ist nicht installiert"
```bash
# macOS:
brew install python-tk@3.11

# Ubuntu/Debian:
sudo apt install python3-tk

# Fedora:
sudo dnf install python3-tkinter

# Windows:
# Python neu installieren mit Tcl/Tk Option
```

### "Dependencies nicht installiert"
```bash
pip install -r requirements.txt
```

### GUI startet nicht
```bash
# Manuelle Prüfung:
python3 verify_imports.py

# GUI direkt starten:
python3 Files/gui_app.py
```

---

## 📊 Workflow-Beispiel

### Kompletter Workflow mit One-Click-Start:

```bash
# 1. GUI starten
./start_gui.sh

# 2. Tab "🚀 Projekt Setup"
#    - Website Name: "Berlin Parks Guide"
#    - Domain: "berlin-parks.de"
#    - Stadt: "Berlin"
#    - Kategorie: "Parks"
#    - [💾 Speichern] klicken

# 3. Tab wechseln → "📊 Daten sammeln"
#    ┌─────────────────────────────────┐
#    │ Konfiguration speichern?        │  ← AUTO-SAVE DIALOG!
#    │ [JA] [NEIN] [ABBRECHEN]         │
#    └─────────────────────────────────┘
#    → [JA] klicken

# 4. In "📊 Daten sammeln" Tab:
#    - Google Places API Key eingeben
#    - Search Query: "parks"
#    - [🔍 Daten sammeln] klicken
#    → Echte Daten werden geladen!

# 5. Tab "🏗️ Seiten generieren"
#    - [🏗️ Pillar Page generieren] klicken
#    → HTML wird erstellt!

# 6. Fertig! 🎉
#    → Datei: generated/berlin_parks.html
```

---

## ⚙️ Technische Details

### start_gui.sh (macOS/Linux)
- Bash-Script mit Farb-Output
- Prüft Python, Dependencies, Tkinter
- Erstellt Verzeichnisse
- Startet GUI aus richtigem Pfad

### start_gui.bat (Windows)
- Windows Batch-Script
- Gleiche Funktionalität wie .sh
- CMD-kompatible Output-Formatierung

### start_gui.py (Plattformunabhängig)
- Python-Script (funktioniert überall)
- Fallback für Farben auf Windows
- subprocess für Dependency-Installation
- Intelligente GUI-Pfad-Erkennung

---

## 🎯 Zusammenfassung

**Vorher (alt):**
```bash
# 1. Python prüfen
python3 --version

# 2. Dependencies installieren
pip install -r requirements.txt

# 3. Tkinter prüfen
python3 -c "import tkinter"

# 4. Verzeichnisse erstellen
mkdir -p data generated

# 5. GUI starten
cd Files
python3 gui_app.py
```

**Nachher (neu):**
```bash
./start_gui.sh
```

**Eine Zeile statt 5+ Befehle!** 🚀

---

## 📚 Weitere Ressourcen

- **GUI_IMPROVEMENTS.py** - Detaillierte Code-Änderungen
- **README.md** - Vollständige Projekt-Dokumentation
- **CLAUDE.md** - Entwickler-Dokumentation
- **PLACEHOLDER_REMOVAL_SUMMARY.md** - Änderungen an Fake-Daten-Logik
- **VERIFICATION_REPORT.md** - Repository-Verifikation

---

**✅ GUI ist jetzt professioneller, benutzerfreundlicher und sicherer!**

_Last Updated: 2025-12-16_
