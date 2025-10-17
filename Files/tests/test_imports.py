"""Test that all core modules can be imported"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_data_pipeline_import():
    """Test data_pipeline module imports successfully"""
    from data_pipeline import (
        DataScraper,
        PillarPageGenerator,
        LocationData,
        DataEnrichment,
    )

    assert DataScraper is not None
    assert PillarPageGenerator is not None
    assert LocationData is not None
    assert DataEnrichment is not None


def test_niche_research_import():
    """Test niche_research module imports successfully"""
    from niche_research import NicheValidator, KeywordResearch

    assert NicheValidator is not None
    assert KeywordResearch is not None


def test_enhanced_scrapers_import():
    """Test enhanced_scrapers module imports successfully"""
    from enhanced_scrapers import UniversalScraper, GooglePlacesScraper, WebScraper

    assert UniversalScraper is not None
    assert GooglePlacesScraper is not None
    assert WebScraper is not None


def test_gui_app_import():
    """Test gui_app module imports successfully"""
    try:
        import tkinter  # noqa: F401
    except ModuleNotFoundError:
        pytest.skip(
            "Tkinter not available (system package required: apt install python3-tk)"
        )

    try:
        import gui_app

        assert hasattr(gui_app, "ADSPillarGUI")
        assert gui_app.MODULES_AVAILABLE, "GUI should load real modules, not stubs"
        assert gui_app.NICHE_AVAILABLE, "GUI should load niche_research, not stubs"
    except ModuleNotFoundError as e:
        if "tkinter" in str(e) or "_tkinter" in str(e):
            pytest.skip(
                "Tkinter not available (system package required: apt install python3-tk)"
            )
        else:
            raise


def test_beautifulsoup_available():
    """Test that beautifulsoup4 is available"""
    from bs4 import BeautifulSoup

    assert BeautifulSoup is not None


def test_all_required_dependencies():
    """Test that all required dependencies are available"""
    import pandas
    import jinja2
    import yaml
    import requests
    import lxml
    from PIL import Image

    assert pandas is not None
    assert jinja2 is not None
    assert yaml is not None
    assert requests is not None
    assert lxml is not None
    assert Image is not None
