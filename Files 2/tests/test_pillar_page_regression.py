"""Regression tests for the pillar page generator."""

from pathlib import Path

from data_pipeline import LocationData, PillarPageGenerator


def build_sample_location(identifier: str, name: str) -> LocationData:
    return LocationData(
        id=identifier,
        name=name,
        street="Musterstraße 1",
        city="Berlin",
        region="Berlin",
        country="Deutschland",
        postcode="10115",
        latitude=52.52,
        longitude=13.405,
        url="https://example.com",
        phone="+49 30 123456",
        email="info@example.com",
        opening_hours="Mo-So 08:00-20:00",
        rating=4.5,
        review_count=120,
        feature_shade=True,
        feature_benches=False,
        feature_water=True,
        feature_parking=False,
        feature_toilets=True,
        feature_wheelchair_accessible=True,
        feature_kids_friendly=True,
        feature_dogs_allowed=False,
        feature_fee=False,
        feature_seasonal=False,
        tags="park,outdoor",
    )


def test_generate_page_inserts_dynamic_content(tmp_path):
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"

    output_file = tmp_path / "berlin_parks.html"

    generator = PillarPageGenerator(str(template_path))
    generator.generate_page(
        data=[
            build_sample_location("park_1", "Tiergarten"),
            build_sample_location("park_2", "Volkspark Friedrichshain"),
        ],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/berlin-parks",
    )

    html = output_file.read_text(encoding="utf-8")

    assert "Tiergarten" in html
    assert "Volkspark Friedrichshain" in html
    assert "https://example.com/berlin-parks" in html
    assert "ListItem" in html  # schema.org data present
