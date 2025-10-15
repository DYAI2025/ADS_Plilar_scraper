"""End-to-end test for the quick_start module.

This verifies that we can go from a prepared configuration to
actual generated artefacts (CSV + HTML) without any manual input.
"""

from pathlib import Path

import pandas as pd

from quick_start import create_sample_data, generate_quick_page


def test_quick_start_end_to_end(tmp_path, monkeypatch):
    # Run the quick-start helpers inside an isolated working directory
    monkeypatch.chdir(tmp_path)

    config = {
        "city": "Berlin",
        "category": "Parks",
        "domain": "example.com",
        "niche_config": {"rpm_estimate": "8-15"},
    }

    csv_path = create_sample_data(config)
    html_path = generate_quick_page(config, csv_path)

    csv_file = Path(csv_path)
    html_file = Path(html_path)

    assert csv_file.exists(), "Expected sample CSV file to be created"
    assert html_file.exists(), "Expected demo HTML file to be generated"

    df = pd.read_csv(csv_file)
    assert not df.empty, "Sample CSV should contain at least one row"
    assert set(df.columns) >= {"name", "address", "city"}

    html_content = html_file.read_text(encoding="utf-8")
    assert "Berlin" in html_content
    assert "Parks" in html_content
    assert "Demo-Seite" in html_content
