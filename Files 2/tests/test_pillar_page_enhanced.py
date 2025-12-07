"""Enhanced tests for the improved pillar page generator."""

from pathlib import Path
import json
import re

from data_pipeline import LocationData, PillarPageGenerator


def build_sample_location(identifier: str, name: str) -> LocationData:
    """Create a sample location with all features."""
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


def test_schema_org_injection(tmp_path):
    """Test that Schema.org JSON-LD is correctly injected into the page."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_schema.html"

    config = {
        "adsense_id": "pub-1234567890123456",
        "ga_id": "G-TEST123456",
    }

    generator = PillarPageGenerator(str(template_path), config=config)
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

    # Check Schema.org is present
    assert "ItemList" in html
    assert "LocalBusiness" in html

    # Extract and validate Schema.org JSON
    schema_match = re.search(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        html,
        re.DOTALL
    )
    assert schema_match, "Schema.org JSON-LD not found in HTML"

    schema_json = json.loads(schema_match.group(1))
    assert schema_json["@type"] == "ItemList"
    assert schema_json["name"] == "Parks in Berlin"
    assert len(schema_json["itemListElement"]) == 2
    assert schema_json["itemListElement"][0]["item"]["name"] == "Tiergarten"
    assert schema_json["itemListElement"][1]["item"]["name"] == "Volkspark Friedrichshain"


def test_adsense_id_replacement(tmp_path):
    """Test that AdSense IDs are correctly replaced."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_adsense.html"

    config = {
        "adsense_id": "pub-9876543210987654",
    }

    generator = PillarPageGenerator(str(template_path), config=config)
    generator.generate_page(
        data=[build_sample_location("park_1", "Test Park")],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/test",
    )

    html = output_file.read_text(encoding="utf-8")

    # Check that placeholder is replaced
    assert "ca-pub-XXXXXXXXXXXXXXXX" not in html, "AdSense placeholder not replaced"
    assert "ca-pub-9876543210987654" in html, "AdSense ID not found in HTML"

    # Count occurrences (should be multiple ad units)
    adsense_count = html.count("ca-pub-9876543210987654")
    assert adsense_count >= 5, f"Expected at least 5 AdSense units, found {adsense_count}"


def test_google_analytics_integration(tmp_path):
    """Test that Google Analytics is correctly integrated."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_ga.html"

    config = {
        "ga_id": "G-TESTANALYTICS",
    }

    generator = PillarPageGenerator(str(template_path), config=config)
    generator.generate_page(
        data=[build_sample_location("park_1", "Test Park")],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/test",
    )

    html = output_file.read_text(encoding="utf-8")

    # Check GA integration
    assert "G-TESTANALYTICS" in html, "GA ID not found in HTML"
    assert "gtag/js?id=G-TESTANALYTICS" in html, "GA script tag not found"
    assert "gtag('config', 'G-TESTANALYTICS')" in html, "GA config not found"
    assert "window.dataLayer" in html, "dataLayer not found"


def test_google_analytics_optional(tmp_path):
    """Test that page generation works without GA ID."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_no_ga.html"

    # No GA ID in config
    config = {}

    generator = PillarPageGenerator(str(template_path), config=config)
    generator.generate_page(
        data=[build_sample_location("park_1", "Test Park")],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/test",
    )

    html = output_file.read_text(encoding="utf-8")

    # GA should not be present
    assert "gtag/js" not in html, "GA script should not be present without ga_id"


def test_validation_empty_data(tmp_path):
    """Test that validation catches empty data."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_empty.html"

    generator = PillarPageGenerator(str(template_path))

    try:
        generator.generate_page(
            data=[],  # Empty data
            city="Berlin",
            category="Parks",
            output_path=str(output_file),
            canonical_url="https://example.com/test",
        )
        assert False, "Should have raised ValueError for empty data"
    except ValueError as e:
        assert "No location data provided" in str(e)


def test_validation_missing_city(tmp_path):
    """Test that validation catches missing city."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_no_city.html"

    generator = PillarPageGenerator(str(template_path))

    try:
        generator.generate_page(
            data=[build_sample_location("park_1", "Test Park")],
            city="",  # Empty city
            category="Parks",
            output_path=str(output_file),
            canonical_url="https://example.com/test",
        )
        assert False, "Should have raised ValueError for missing city"
    except ValueError as e:
        assert "City and category are required" in str(e)


def test_validation_missing_template(tmp_path):
    """Test that validation catches missing template."""
    output_file = tmp_path / "test_no_template.html"

    generator = PillarPageGenerator(template_path="nonexistent.html")

    try:
        generator.generate_page(
            data=[build_sample_location("park_1", "Test Park")],
            city="Berlin",
            category="Parks",
            output_path=str(output_file),
            canonical_url="https://example.com/test",
        )
        assert False, "Should have raised FileNotFoundError for missing template"
    except FileNotFoundError as e:
        assert "Template not found" in str(e)


def test_output_directory_creation(tmp_path):
    """Test that output directory is automatically created."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"

    # Use nested path that doesn't exist yet
    output_file = tmp_path / "nested" / "dirs" / "test.html"
    assert not output_file.parent.exists()

    generator = PillarPageGenerator(str(template_path))
    generator.generate_page(
        data=[build_sample_location("park_1", "Test Park")],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/test",
    )

    # Directory should now exist
    assert output_file.parent.exists()
    assert output_file.exists()


def test_config_with_pub_prefix(tmp_path):
    """Test that 'pub-' prefix in config is handled correctly."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_prefix.html"

    # Config with 'pub-' prefix (like in project_config.json)
    config = {
        "adsense_id": "pub-1234567890123456",
    }

    generator = PillarPageGenerator(str(template_path), config=config)
    generator.generate_page(
        data=[build_sample_location("park_1", "Test Park")],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/test",
    )

    html = output_file.read_text(encoding="utf-8")

    # Should have correct format
    assert "ca-pub-1234567890123456" in html


def test_backward_compatibility_no_config(tmp_path):
    """Test that generator works without config (backward compatibility)."""
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "pillar_page_skeleton.html"
    output_file = tmp_path / "test_no_config.html"

    # Old style: no config parameter
    generator = PillarPageGenerator(str(template_path))
    generator.generate_page(
        data=[build_sample_location("park_1", "Test Park")],
        city="Berlin",
        category="Parks",
        output_path=str(output_file),
        canonical_url="https://example.com/test",
    )

    html = output_file.read_text(encoding="utf-8")

    # Should work, but with placeholder AdSense ID
    assert "ca-pub-XXXXXXXXXXXXXXXX" in html
    # Should have location data
    assert "Test Park" in html
    # Should not have GA
    assert "gtag/js" not in html
