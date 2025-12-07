from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES_DIR = PROJECT_ROOT / "Files"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(FILES_DIR) not in sys.path:
    sys.path.insert(0, str(FILES_DIR))

from data_pipeline import LocationData, PillarPageGenerator
from generate_ai_optimized_site import prepare_location_data


def test_prepare_location_data_sanitizes_script_payload() -> None:
    malicious_location = {
        "name": "Park</script><script>alert('xss')</script>",
        "address": "<b>Street 1</b>",
        "city": "Berlin",
        "rating": "4.2",
        "review_count": "10",
        "description_de": "Toller Ort <script>evil()</script>",
        "tags": "familienfreundlich",
        "main_image": "https://example.com/image.png",
        "opening_hours": "Immer",
        "website": "https://example.com",
        "latitude": "52.52",
        "longitude": "13.4",
        "feature_shade": "TRUE",
        "feature_water": "FALSE",
        "feature_benches": "TRUE",
        "feature_parking": "TRUE",
        "feature_toilets": "TRUE",
        "feature_wheelchair_accessible": "FALSE",
        "feature_kids_friendly": "FALSE",
        "feature_dogs_allowed": "FALSE",
        "feature_fee": "FALSE",
        "feature_seasonal": "FALSE",
        "feature_fkk": "FALSE",
        "feature_restaurant": "FALSE",
        "feature_photography": "FALSE",
        "feature_historic": "FALSE",
    }

    sanitized = prepare_location_data([malicious_location])[0]

    assert "<script" not in sanitized["name"].lower()
    assert "&lt;/script&gt;" in sanitized["name"]
    assert sanitized["description"].startswith("Toller Ort")


def test_pillar_page_generator_escapes_template_values(tmp_path: Path) -> None:
    template = tmp_path / "template.html"
    template.write_text(
        """
        <html>
        <head></head>
        <body>
        <h1>{{CITY}} - {{CATEGORY}}</h1>
        <script>const DATA = [
        ];</script>
        <a href="{{CANONICAL_URL}}">link</a>
        </body>
        </html>
        """,
        encoding="utf-8",
    )

    generator = PillarPageGenerator(str(template))
    output_path = tmp_path / "output.html"

    generator.generate_page(
        data=[
            LocationData(
                id="loc-1",
                name="Test<script>alert('bad')</script>",
                street="<b>Main</b> Street",
                city="Berlin",
                region="Berlin",
                country="DE",
                postcode="10115",
                latitude=52.5,
                longitude=13.4,
                url="https://example.com/<script>hack</script>",
                phone="<script>call()</script>",
                email="user@example.com",
                opening_hours="Täglich",
                rating=4.8,
                review_count=12,
                feature_shade=True,
                feature_benches=True,
                feature_water=False,
                feature_parking=True,
                feature_toilets=False,
                feature_wheelchair_accessible=False,
                feature_kids_friendly=False,
                feature_dogs_allowed=False,
                feature_fee=False,
                feature_seasonal=False,
            )
        ],
        city="Berlin<script>alert('city')</script>",
        category="Parks<script>bad()</script>",
        output_path=str(output_path),
        canonical_url="https://example.com/<script>malicious</script>",
    )

    content = output_path.read_text(encoding="utf-8")

    assert "<script>alert('city')</script>" not in content
    assert "Parks&lt;script&gt;bad()&lt;/script&gt;" in content
    assert "<script>hack</script>" not in content
