#!/usr/bin/env python3
"""Verify all module imports work correctly"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Files"))

def test_imports():
    print("🧪 Testing all module imports...")
    print("=" * 50)
    success = True
    
    try:
        from data_pipeline import DataScraper, PillarPageGenerator, LocationData, DataEnrichment
        print("✅ data_pipeline imports successfully")
        print(f"   - DataScraper: {DataScraper}")
        print(f"   - PillarPageGenerator: {PillarPageGenerator}")
        print(f"   - LocationData: {LocationData}")
        print(f"   - DataEnrichment: {DataEnrichment}")
    except Exception as e:
        print(f"❌ data_pipeline import failed: {e}")
        success = False
    
    try:
        from niche_research import NicheValidator, KeywordResearch
        print("✅ niche_research imports successfully")
        print(f"   - NicheValidator: {NicheValidator}")
        print(f"   - KeywordResearch: {KeywordResearch}")
    except Exception as e:
        print(f"❌ niche_research import failed: {e}")
        success = False
    
    try:
        from enhanced_scrapers import UniversalScraper, GooglePlacesScraper
        print("✅ enhanced_scrapers imports successfully")
        print(f"   - UniversalScraper: {UniversalScraper}")
        print(f"   - GooglePlacesScraper: {GooglePlacesScraper}")
    except Exception as e:
        print(f"❌ enhanced_scrapers import failed: {e}")
        success = False
    
    try:
        import gui_app
        print("✅ gui_app imports successfully")
        if hasattr(gui_app, 'MODULES_AVAILABLE'):
            if gui_app.MODULES_AVAILABLE:
                print("   ✅ GUI using REAL modules (not stubs)")
            else:
                print("   ❌ GUI fell back to STUB classes")
                success = False
    except Exception as e:
        print(f"❌ gui_app import failed: {e}")
        success = False
    
    print()
    if success:
        print("🎉 All imports successful!")
        return True
    else:
        print("❌ Some imports failed. Install dependencies with:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
