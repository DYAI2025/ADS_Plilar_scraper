#!/usr/bin/env python3
"""
ADS Pillar System - Funktionstest
Testet alle Hauptkomponenten des Systems
"""

import os
import sys
import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES_DIR = PROJECT_ROOT / "Files"


def _resolve_path(relative_path: str) -> Path | None:
    """Return the first matching path within the known project folders."""

    for base in (PROJECT_ROOT, FILES_DIR):
        candidate = base / relative_path
        if candidate.exists():
            return candidate
    return None

def check_file_exists(filepath, description):
    """Test if file exists"""

    resolved = _resolve_path(filepath)
    if resolved:
        print(f"✅ {description}")
        return True

    print(f"❌ {description} - FEHLT: {filepath}")
    return False

def check_python_import(module_name, filepath):
    """Test if Python module is importable"""
    try:
        resolved = _resolve_path(filepath)
        if not resolved:
            raise FileNotFoundError(filepath)

        spec = importlib.util.spec_from_file_location(module_name, resolved)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ {module_name}.py - Import erfolgreich")
        return True
    except Exception as e:
        print(f"❌ {module_name}.py - Import-Fehler: {str(e)[:50]}...")
        return False

def check_dependencies():
    """Teste wichtige Python-Dependencies"""
    required_modules = [
        'pandas', 'requests', 'tkinter', 
        'json', 'csv', 'datetime'
    ]
    
    missing = []
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
            else:
                __import__(module)
            print(f"✅ {module} verfügbar")
        except ImportError:
            print(f"❌ {module} FEHLT")
            missing.append(module)
    
    return len(missing) == 0, missing

def run_system_completeness():
    """Teste Vollständigkeit des Systems"""
    
    print("🧪 ADS Pillar System - Funktionstest")
    print("=" * 50)
    print()
    
    # Teste Kern-Dateien
    print("📁 Kern-System Dateien:")
    core_files = [
        ('gui_app.py', 'GUI Hauptanwendung'),
        ('data_pipeline.py', 'Datenverarbeitung & Generator'),
        ('enhanced_scrapers.py', 'Multi-Source Datensammlung'),
        ('niche_research.py', 'Nischen-Analyse Tools'),
        ('quick_start.py', 'Ein-Klick Starter'),
    ]
    
    core_ok = True
    for filename, desc in core_files:
        if not check_file_exists(filename, desc):
            core_ok = False
    print()
    
    # Teste Template-Dateien
    print("🌐 Templates & Assets:")
    template_files = [
        ('pillar_page_skeleton.html', 'Haupt-HTML-Template'),
        ('ads.txt', 'AdSense Ads.txt'),
        ('README.md', 'Haupt-Dokumentation'),
        ('START_HERE.md', 'Schnellstart-Guide'),
    ]
    
    templates_ok = True
    for filename, desc in template_files:
        if not check_file_exists(filename, desc):
            templates_ok = False
    print()
    
    # Teste Setup-Dateien
    print("🔧 Setup & Konfiguration:")
    setup_files = [
        ('run_setup.sh', 'Automatisches Setup Script'),
        ('adsense_policy_checklist.md', 'AdSense Compliance Guide'),
        ('revenue_model.csv', 'Revenue-Berechnungsmodell'),
    ]
    
    setup_ok = True
    for filename, desc in setup_files:
        if not check_file_exists(filename, desc):
            setup_ok = False
    print()
    
    # Teste Python-Module Imports
    print("🐍 Python Module Tests:")
    python_modules = [
        ('gui_app', 'gui_app.py'),
        ('data_pipeline', 'data_pipeline.py'),
        ('enhanced_scrapers', 'enhanced_scrapers.py'),
        ('niche_research', 'niche_research.py'),
    ]
    
    imports_ok = True
    for module_name, filepath in python_modules:
        if not check_python_import(module_name, filepath):
            imports_ok = False
    print()
    
    # Teste Dependencies
    print("📦 Python Dependencies:")
    deps_ok, missing_deps = check_dependencies()
    print()
    
    # Teste Verzeichnisstruktur
    print("📂 Verzeichnisstruktur:")
    expected_dirs = ['data', 'generated', 'templates']
    dirs_ok = True

    for dirname in expected_dirs:
        resolved = _resolve_path(dirname)
        if not resolved:
            # create under project root to keep predictable structure
            created = PROJECT_ROOT / dirname
            created.mkdir(exist_ok=True)
            print(f"✅ {dirname}/ - Erstellt")
        else:
            print(f"✅ {dirname}/ - Vorhanden")
    print()
    
    # Gesamtergebnis
    print("📊 SYSTEM-STATUS:")
    print("-" * 30)
    
    overall_score = 0
    total_tests = 5
    
    if core_ok:
        print("✅ Kern-System: Vollständig")
        overall_score += 1
    else:
        print("❌ Kern-System: Unvollständig")
    
    if templates_ok:
        print("✅ Templates: Vollständig")
        overall_score += 1
    else:
        print("❌ Templates: Unvollständig")
    
    if setup_ok:
        print("✅ Setup-Dateien: Vollständig")
        overall_score += 1
    else:
        print("❌ Setup-Dateien: Unvollständig")
    
    if imports_ok:
        print("✅ Python-Module: Alle importierbar")
        overall_score += 1
    else:
        print("❌ Python-Module: Import-Probleme")
    
    if deps_ok:
        print("✅ Dependencies: Alle verfügbar")
        overall_score += 1
    else:
        print(f"❌ Dependencies: {len(missing_deps)} fehlen: {', '.join(missing_deps)}")
    
    print()
    score_percent = (overall_score / total_tests) * 100
    
    if score_percent == 100:
        print("🎉 SYSTEM BEREIT! (100%)")
        print("   → Starte mit: python3 quick_start.py")
        print("   → Oder GUI: python3 gui_app.py")
    elif score_percent >= 80:
        print(f"⚠️  SYSTEM MEIST BEREIT ({score_percent:.0f}%)")
        print("   → Behebe die Warnungen und starte dann")
    else:
        print(f"🚨 SYSTEM NICHT BEREIT ({score_percent:.0f}%)")
        print("   → Installiere fehlende Komponenten")
        
        if missing_deps:
            print("\n📦 Installiere Dependencies:")
            print("   pip3 install " + " ".join(missing_deps))
    
    return score_percent >= 80


def test_system_completeness():
    """Pytest entry point."""

    assert run_system_completeness(), "System nicht vollständig eingerichtet"

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

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
