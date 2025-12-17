"""End-to-end test for the quick_start module.

This verifies that quick_start now REFUSES to create fake data
and instead creates templates and requires real data.
"""

from pathlib import Path

import pandas as pd
import pytest

from quick_start import create_sample_data, generate_quick_page


def test_quick_start_end_to_end(tmp_path, monkeypatch, capsys):
    """Test that quick_start creates TEMPLATES, not fake data."""
    # Run the quick-start helpers inside an isolated working directory
    monkeypatch.chdir(tmp_path)

    config = {
        "city": "Berlin",
        "category": "Parks",
        "domain": "example.com",
        "niche_config": {"rpm_estimate": "8-15"},
    }

    # create_sample_data should now return None and create a template
    csv_path = create_sample_data(config)

    # Verify return value is None (no fake data created)
    assert csv_path is None, "create_sample_data should return None (no fake data)"

    # Verify template CSV was created instead
    template_path = Path("data/berlin_parks_TEMPLATE.csv")
    assert template_path.exists(), "Expected template CSV to be created"

    # Verify template contains placeholder text
    df = pd.read_csv(template_path)
    assert not df.empty, "Template CSV should contain at least one row"
    assert "[BITTE ECHTE DATEN HINZUFÜGEN]" in df['name'].values[0], \
        "Template should contain placeholder text"

    # Verify console output shows warning
    captured = capsys.readouterr()
    assert "KEINE FAKE-DATEN" in captured.out, "Should warn about no fake data"
    assert "Google Places API" in captured.out, "Should suggest using API"

    # Verify generate_quick_page returns None without valid data
    html_path = generate_quick_page(config, None)
    assert html_path is None, "generate_quick_page should return None without data"

    # Verify it also fails with template data
    html_path = generate_quick_page(config, str(template_path))
    assert html_path is None, "generate_quick_page should reject template placeholders"

    captured = capsys.readouterr()
    assert "CSV enthält noch Platzhalter" in captured.out, \
        "Should detect and reject placeholder data"
