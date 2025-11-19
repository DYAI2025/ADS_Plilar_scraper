#!/usr/bin/env python3
"""ADS Pillar System - Funktionstest.

Dieses Modul dient sowohl als pytest-Suite als auch als manuell ausführbarer
Systemcheck. Die Helper-Funktionen behalten die bestehende Konsolen-Ausgabe bei,
werden in den Tests aber über aussagekräftige Asserts ausgewertet.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Iterable, Tuple

# Determine the Files directory - works whether running from root or Files/
TEST_DIR = Path(__file__).resolve().parent
FILES_DIR = TEST_DIR.parent
PROJECT_ROOT = FILES_DIR.parent


def check_file_exists(filepath: str, description: str) -> bool:
    """Prüfe, ob eine Datei existiert und gib Diagnosen aus."""
    if os.path.exists(filepath):
        print(f"✅ {description}")
        return True
    print(f"❌ {description} - FEHLT: {filepath}")
    return False


def check_python_import(module_name: str, filepath: str) -> bool:
    """Prüfe, ob sich ein Modul von einem Pfad importieren lässt."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None or spec.loader is None:
            raise ImportError("Spec konnte nicht erstellt werden")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[call-arg]
        print(f"✅ {module_name}.py - Import erfolgreich")
        return True
    except Exception as exc:  # pragma: no cover - detaillierte Ausgabe
        print(f"❌ {module_name}.py - Import-Fehler: {exc}")
        return False


def test_dependencies():
    """Teste wichtige Python-Dependencies"""
    required_modules = [
        "pandas",
        "requests",
        "tkinter",
        "json",
        "csv",
        "datetime",
        "bs4",
        "PIL",
        "jinja2",
        "yaml",
    ]

    missing = []
    for module in required_modules:
        try:
            if module == "tkinter":
                import tkinter  # noqa: F401
            elif module == "bs4":
                from bs4 import BeautifulSoup  # noqa: F401
            elif module == "PIL":
                from PIL import Image  # noqa: F401
            elif module == "yaml":
                import yaml  # noqa: F401
            else:
                __import__(module)
            print(f"✅ {module} verfügbar")
        except ImportError:
            # tkinter is allowed to be missing in headless environments
            if module == "tkinter":
                print(f"⚠️  {module} nicht verfügbar (akzeptiert in headless Umgebung)")
            else:
                print(f"❌ {module} FEHLT")
                missing.append(module)
    return len(missing) == 0, tuple(missing)


def test_system_health():
    """End-to-end Systemcheck innerhalb von pytest."""
    print("🧪 ADS Pillar System - Funktionstest")
    print("=" * 50)

    # Change to Files directory for file checks
    original_dir = os.getcwd()
    os.chdir(FILES_DIR)
    
    try:
        core_files = [
            ("gui_app.py", "GUI Hauptanwendung"),
            ("data_pipeline.py", "Datenverarbeitung & Generator"),
            ("enhanced_scrapers.py", "Multi-Source Datensammlung"),
            ("niche_research.py", "Nischen-Analyse Tools"),
            ("quick_start.py", "Ein-Klick Starter"),
        ]
        for filename, desc in core_files:
            assert check_file_exists(filename, desc), f"{filename} fehlt"

        template_files = [
            ("pillar_page_skeleton.html", "Haupt-HTML-Template"),
            ("ads.txt", "AdSense Ads.txt"),
            ("README.md", "Haupt-Dokumentation"),
            ("START_HERE.md", "Schnellstart-Guide"),
        ]
        for filename, desc in template_files:
            if not check_file_exists(filename, desc):
                templates_ok = False
        print()
        
        # Teste Setup-Dateien
        print("🔧 Setup & Konfiguration:")

        setup_files = [
            ("run_setup.sh", "Automatisches Setup Script"),
            ("adsense_policy_checklist.md", "AdSense Compliance Guide"),
            ("revenue_model.csv", "Revenue-Berechnungsmodell"),
        ]
        for filename, desc in setup_files:
            if not check_file_exists(filename, desc):
                setup_ok = False
        print()
        
        # Teste Python-Module Imports
        print("🐍 Python Module Tests:")
        python_modules = [
            ("gui_app", "gui_app.py"),
            ("data_pipeline", "data_pipeline.py"),
            ("enhanced_scrapers", "enhanced_scrapers.py"),
            ("niche_research", "niche_research.py"),
        ]
        for module_name, filepath in python_modules:
            if os.path.exists(filepath):
                # gui_app may fail in headless environment without tkinter
                # but that's expected and acceptable
                if module_name == "gui_app":
                    try:
                        import tkinter  # noqa: F401

                        assert check_python_import(
                            module_name, filepath
                        ), f"Import von {module_name} fehlgeschlagen"
                    except ImportError:
                        print(
                            f"⚠️  gui_app.py - Übersprungen (tkinter nicht verfügbar in headless Umgebung)"
                        )
                else:
                    assert check_python_import(
                        module_name, filepath
                    ), f"Import von {module_name} fehlgeschlagen"
            else:
                raise AssertionError(f"Datei {filepath} fehlt für Import-Test")

        deps_ok, missing_deps = test_dependencies()
        assert deps_ok, f"Fehlende Dependencies: {', '.join(missing_deps)}"

        for dirname in ("data", "generated", "templates"):
            os.makedirs(dirname, exist_ok=True)
            assert os.path.exists(
                dirname
            ), f"Verzeichnis {dirname} konnte nicht angelegt werden"
            print(f"✅ {dirname}/ - vorhanden")
    
    finally:
        # Restore original directory
        os.chdir(original_dir)

def test_system_completeness():
    """pytest entry point that runs the full system health check."""
    test_system_health()

def main():
    """Hauptfunktion für Systemtest"""
    try:
        test_system_health()
        return True
    except KeyboardInterrupt:
        print("\n\n👋 Test abgebrochen.")
        return False
    except Exception as e:
        print(f"\n❌ Test-Fehler: {e}")
        return False

if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(0 if main() else 1)
