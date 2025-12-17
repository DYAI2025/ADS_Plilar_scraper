#!/usr/bin/env python3
"""
ADS Pillar Scraper - One-Click GUI Starter
Plattformunabhängiger GUI-Start mit automatischer Setup-Prüfung
"""

import os
import sys
import subprocess
from pathlib import Path


def print_colored(text, color='white'):
    """Print colored text (works cross-platform with fallback)"""
    colors = {
        'red': '\033[0;31m',
        'green': '\033[0;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[0;34m',
        'white': '\033[0m',
    }

    # Nur Farben auf Unix-Systemen, Windows CMD hat Probleme damit
    if os.name != 'nt':
        print(f"{colors.get(color, colors['white'])}{text}\033[0m")
    else:
        # Windows: Entferne Emoji und nutze einfachen Text
        text = text.replace('✅', '[OK]').replace('❌', '[FEHLER]') \
                   .replace('⚠️', '[WARNUNG]').replace('📋', '').replace('📦', '') \
                   .replace('🖼️', '').replace('📁', '').replace('🎨', '').replace('🚀', '')
        print(text)


def check_python_version():
    """Prüfe Python-Version"""
    print_colored("📋 Prüfe Python-Installation...", 'blue')

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored(f"❌ Python {version.major}.{version.minor} ist zu alt!", 'red')
        print_colored("   Bitte installieren Sie Python 3.8+", 'yellow')
        return False

    print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} gefunden", 'green')
    return True


def check_dependencies():
    """Prüfe und installiere Dependencies"""
    print_colored("📦 Prüfe Dependencies...", 'blue')

    try:
        import pandas
        import jinja2
        import yaml
        print_colored("✅ Dependencies vorhanden", 'green')
        return True
    except ImportError:
        print_colored("⚠️  Dependencies nicht installiert - Installation wird gestartet...", 'yellow')
        print()

        requirements_file = Path("requirements.txt")
        if not requirements_file.exists():
            print_colored("❌ requirements.txt nicht gefunden!", 'red')
            return False

        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
            ])
            print_colored("✅ Dependencies installiert", 'green')
            return True
        except subprocess.CalledProcessError:
            print_colored("❌ Fehler bei Installation der Dependencies!", 'red')
            return False


def check_tkinter():
    """Prüfe Tkinter-Verfügbarkeit"""
    print_colored("🖼️  Prüfe GUI-Unterstützung (Tkinter)...", 'blue')

    try:
        import tkinter
        print_colored("✅ GUI-Unterstützung verfügbar", 'green')
        return True
    except ImportError:
        print_colored("❌ Tkinter ist nicht installiert!", 'red')
        print()
        print_colored("Installations-Anleitung:", 'yellow')
        if sys.platform == 'darwin':
            print_colored("  macOS:   brew install python-tk@3.11", 'yellow')
        elif sys.platform.startswith('linux'):
            print_colored("  Ubuntu:  sudo apt install python3-tk", 'yellow')
            print_colored("  Fedora:  sudo dnf install python3-tkinter", 'yellow')
        elif sys.platform == 'win32':
            print_colored("  Windows: Python neu installieren mit Tcl/Tk Option", 'yellow')
        return False


def create_directories():
    """Erstelle notwendige Arbeitsverzeichnisse"""
    print_colored("📁 Erstelle Arbeitsverzeichnisse...", 'blue')

    Path("data").mkdir(exist_ok=True)
    Path("generated").mkdir(exist_ok=True)

    print_colored("✅ Verzeichnisse bereit", 'green')


def find_gui_script():
    """Finde gui_app.py"""
    candidates = [
        Path("Files/gui_app.py"),
        Path("gui_app.py"),
        Path("Files 2/gui_app.py"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def start_gui():
    """Starte die GUI"""
    print()
    print_colored("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'green')
    print_colored("🎨 GUI wird gestartet...", 'green')
    print_colored("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'green')
    print()

    gui_script = find_gui_script()
    if not gui_script:
        print_colored("❌ gui_app.py nicht gefunden!", 'red')
        return False

    # Wechsle ins richtige Verzeichnis
    original_dir = Path.cwd()
    if gui_script.parent.name in ['Files', 'Files 2']:
        os.chdir(gui_script.parent)

    try:
        # Starte GUI
        subprocess.run([sys.executable, gui_script.name])
        return True
    except KeyboardInterrupt:
        print()
        print_colored("⚠️  GUI wurde durch Nutzer abgebrochen", 'yellow')
        return True
    except Exception as e:
        print_colored(f"❌ Fehler beim Starten der GUI: {str(e)}", 'red')
        return False
    finally:
        os.chdir(original_dir)


def main():
    """Hauptfunktion"""
    print()
    print_colored("🚀 ADS Pillar Scraper - GUI wird gestartet...", 'blue')
    print()

    # Prüfungen durchführen
    checks = [
        check_python_version,
        check_dependencies,
        check_tkinter,
    ]

    for check in checks:
        if not check():
            print()
            print_colored("❌ Setup fehlgeschlagen. Bitte beheben Sie die Fehler oben.", 'red')
            input("\nDrücken Sie Enter zum Beenden...")
            sys.exit(1)
        print()

    # Verzeichnisse erstellen
    create_directories()
    print()

    # GUI starten
    if start_gui():
        print()
        print_colored("👋 GUI wurde beendet. Bis bald!", 'blue')
        sys.exit(0)
    else:
        print()
        print_colored("❌ GUI konnte nicht gestartet werden", 'red')
        input("\nDrücken Sie Enter zum Beenden...")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_colored("⚠️  Abgebrochen durch Nutzer", 'yellow')
        sys.exit(0)
