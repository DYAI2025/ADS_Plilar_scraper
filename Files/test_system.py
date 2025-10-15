#!/usr/bin/env python3
"""ADS Pillar System - Funktionstest.

Dieses Modul dient sowohl als pytest-Suite als auch als manuell ausführbarer
Systemcheck. Die Helper-Funktionen behalten die bestehende Konsolen-Ausgabe bei,
werden in den Tests aber über aussagekräftige Asserts ausgewertet.
"""

from __future__ import annotations

import importlib.util
import os
from typing import Iterable, Tuple


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

def check_dependencies():
    """Test important Python dependencies"""
    required_modules = [
        'pandas', 'requests', 'tkinter', 
        'json', 'csv', 'datetime',
        'bs4',
        'PIL',
        'jinja2',
        'yaml'
    ]
    
    missing = []
    for module in modules:
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'bs4':
                from bs4 import BeautifulSoup
            elif module == 'PIL':
                from PIL import Image
            elif module == 'yaml':
                import yaml
            else:
                __import__(module)
            print(f"✅ {module} verfügbar")
        except ImportError:
            print(f"❌ {module} FEHLT")
            missing.append(module)
    return len(missing) == 0, tuple(missing)


def test_system_health():
    """End-to-end Systemcheck innerhalb von pytest."""
    print("🧪 ADS Pillar System - Funktionstest")
    print("=" * 50)

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
        assert check_file_exists(filename, desc), f"{filename} fehlt"

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
            assert check_python_import(module_name, filepath), f"Import von {module_name} fehlgeschlagen"
        else:
            raise AssertionError(f"Datei {filepath} fehlt für Import-Test")

    deps_ok, missing_deps = check_dependencies([
        "pandas",
        "requests",
        "bs4",
        "tkinter",
        "json",
        "csv",
        "datetime",
    ])
    assert deps_ok, f"Fehlende Dependencies: {', '.join(missing_deps)}"


def test_system_completeness():
    """pytest entry point."""

    assert run_system_completeness(), "System not fully configured"

def main():
    """Hauptfunktion für Systemtest"""
    try:
        return run_system_completeness()
    except KeyboardInterrupt:
        print("\n\n👋 Test abgebrochen.")
        return False
    except Exception as e:
        print(f"\n❌ Test-Fehler: {e}")
        return False

if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
