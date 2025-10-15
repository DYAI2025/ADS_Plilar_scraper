"""Integration and regression tests for the ADS Pillar toolkit."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES_DIR = PROJECT_ROOT / "Files"

# Ensure the "Files" folder is on sys.path for module imports.
import sys

if str(FILES_DIR) not in sys.path:
    sys.path.insert(0, str(FILES_DIR))

from data_pipeline import DataEnrichment, LocationData, PillarPageGenerator


@pytest.fixture(scope="module")
def sample_location() -> LocationData:
    """Provide a deterministic location instance for the tests."""

    return LocationData(
        id="sample-park-berlin",
        name="Musterpark",
        street="Parkstraße 1",
        city="Berlin",
        region="Berlin",
        country="DE",
        postcode="10115",
        latitude=52.52,
        longitude=13.405,
        url="https://example.com/musterpark",
        phone="+49-30-1234567",
        email="info@example.com",
        opening_hours="Mo-Fr 08:00-20:00",
        rating=4.6,
        review_count=128,
        feature_shade=True,
        feature_benches=True,
        feature_water=False,
        feature_parking=True,
        feature_toilets=True,
        feature_wheelchair_accessible=True,
        feature_kids_friendly=True,
        feature_dogs_allowed=False,
        feature_fee=False,
        feature_seasonal=False,
        tags="familienfreundlich"
    )


def _load_generated_data(html_content: str) -> list[dict]:
    """Extract the DATA array from the generated HTML for assertions."""

    match = re.search(r"const DATA = (\[.*?\]);", html_content, re.DOTALL)
    assert match, "DATA array not embedded in HTML output"
    return json.loads(match.group(1))


def test_generate_page_end_to_end(tmp_path: Path, sample_location: LocationData) -> None:
    """Generate a pillar page and verify the artefacts."""

    template_path = FILES_DIR / "pillar_page_skeleton.html"
    assert template_path.exists(), "Template fehlt für End-to-End-Test"

    output_path = tmp_path / "berlin-parks.html"
    generator = PillarPageGenerator(str(template_path))
    generator.generate_page(
        data=[sample_location],
        city="Berlin",
        category="Parks",
        output_path=str(output_path),
        canonical_url="https://example.com/berlin-parks",
    )

    content = output_path.read_text(encoding="utf-8")
    assert "Musterpark" in content
    assert "Berlin" in content

    data_payload = _load_generated_data(content)
    assert data_payload[0]["name"] == "Musterpark"
    assert data_payload[0]["feature_shade"] is True
    assert data_payload[0]["feature_dogs_allowed"] is False


def test_feature_extraction_regression() -> None:
    """Regression test ensuring keyword-based feature extraction stays stable."""

    review_text = (
        "Schöner Park mit viel Schatten und sauberen Toiletten. "
        "Kostenloser Eintritt, perfekt für Kinder und Hunde sind erlaubt."
    )

    features = DataEnrichment.extract_features_from_text(review_text)

    assert features["feature_shade"] is True
    assert features["feature_toilets"] is True
    assert features["feature_kids"] is True
    assert features["feature_dogs"] is True
    # "Kostenlos" sollte bedeuten, dass keine Gebühr verlangt wird.
    assert features["feature_fee"] is False
