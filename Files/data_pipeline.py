import pandas as pd
import json
import html
import re
import time
from dataclasses import dataclass
from typing import Dict, List

import requests


@dataclass
class LocationData:
    """Data structure for a single location"""

    id: str
    name: str
    street: str
    city: str
    region: str
    country: str
    postcode: str
    latitude: float
    longitude: float
    url: str
    phone: str
    email: str
    opening_hours: str
    rating: float
    review_count: int
    # Feature flags
    feature_shade: bool = False
    feature_benches: bool = False
    feature_water: bool = False
    feature_parking: bool = False
    feature_toilets: bool = False
    feature_wheelchair_accessible: bool = False
    feature_kids_friendly: bool = False
    feature_dogs_allowed: bool = False
    feature_fee: bool = True  # True = costs money, False = free
    feature_seasonal: bool = False
    tags: str = ""


class DataEnrichment:
    """Extract features from reviews and descriptions"""

    FEATURE_KEYWORDS = {
        "shade": [
            "schatten",
            "schattig",
            "bäume",
            "überdacht",
            "shadow",
            "shaded",
            "trees",
        ],
        "benches": [
            "bank",
            "bänke",
            "sitzbank",
            "sitzen",
            "bench",
            "benches",
            "seating",
        ],
        "water": [
            "wasser",
            "brunnen",
            "teich",
            "see",
            "bach",
            "water",
            "fountain",
            "pond",
        ],
        "parking": ["parkplatz", "parken", "parking", "stellplatz", "garage"],
        "toilets": [
            "toilette",
            "wc",
            "klo",
            "sanitär",
            "toilet",
            "restroom",
            "bathroom",
        ],
        "wheelchair": [
            "rollstuhl",
            "barriere",
            "wheelchair",
            "accessible",
            "handicap",
            "disabled",
        ],
        "kids": [
            "kinder",
            "spielplatz",
            "familie",
            "kids",
            "children",
            "family",
            "playground",
        ],
        "dogs": ["hund", "hunde", "dog", "dogs", "pet", "tier", "erlaubt"],
        "fee": ["kostenlos", "gratis", "free", "frei", "umsonst", "ohne kosten"],
        "seasonal": [
            "saisonal",
            "winter",
            "sommer",
            "geschlossen",
            "seasonal",
            "closed",
        ],
    }

    @classmethod
    def extract_features_from_text(cls, text: str) -> Dict[str, bool]:
        """Extract feature flags from review text"""
        text_lower = text.lower()
        features = {}

        for feature, keywords in cls.FEATURE_KEYWORDS.items():
            features[f"feature_{feature}"] = any(
                keyword in text_lower for keyword in keywords
            )

        # Special logic for fee (free is opposite of fee)
        if features.get("feature_fee", False):
            features["feature_fee"] = False  # Found "free" keywords = no fee
        else:
            features["feature_fee"] = True  # Default: assume fee

        return features


class DataScraper:
    """Base class for data scraping from various sources"""

    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )

    def scrape_google_places(
        self, query: str, location: str, api_key: str
    ) -> List[Dict]:
        """
        Scrape Google Places API (requires API key)
        Example: scrape_google_places("parks", "Berlin", "YOUR_API_KEY")
        """
        if not api_key or api_key == "YOUR_API_KEY":
            print("⚠️  Google Places API key required")
            return []

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{query} in {location}",
            "key": api_key,
            "fields": "name,formatted_address,geometry,rating,user_ratings_total,place_id",
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            places = []
            for place in data.get("results", []):
                places.append(
                    {
                        "name": place.get("name", ""),
                        "address": place.get("formatted_address", ""),
                        "rating": place.get("rating", 0),
                        "review_count": place.get("user_ratings_total", 0),
                        "lat": place.get("geometry", {})
                        .get("location", {})
                        .get("lat", 0),
                        "lng": place.get("geometry", {})
                        .get("location", {})
                        .get("lng", 0),
                        "place_id": place.get("place_id", ""),
                    }
                )

            time.sleep(self.delay)
            return places

        except Exception as e:
            print(f"❌ Error scraping Google Places: {e}")
            return []

    def get_place_details(self, place_id: str, api_key: str) -> Dict:
        """Get detailed information for a place"""
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "key": api_key,
            "fields": "name,formatted_address,international_phone_number,website,opening_hours,reviews,rating,user_ratings_total",
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            result = data.get("result", {})
            reviews_text = " ".join(
                [review.get("text", "") for review in result.get("reviews", [])]
            )

            return {
                "phone": result.get("international_phone_number", ""),
                "website": result.get("website", ""),
                "opening_hours": str(
                    result.get("opening_hours", {}).get("weekday_text", [])
                ),
                "reviews_text": reviews_text,
            }

        except Exception as e:
            print(f"❌ Error getting place details: {e}")
            return {}


class PillarPageGenerator:
    """Generate pillar pages from data"""

    def __init__(self, template_path: str = "pillar_page_skeleton.html"):
        self.template_path = template_path

    @staticmethod
    def _sanitize_text(value: str) -> str:
        """Escape user-provided text to keep generated pages authentic and safe."""
        if value is None:
            return ""
        return html.escape(str(value))

    def generate_page(
        self,
        data: List[LocationData],
        city: str,
        category: str,
        output_path: str,
        canonical_url: str,
    ) -> None:
        """Generate a complete pillar page"""

        # Read template
        with open(self.template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # Generate JSON data for JavaScript
        json_data = []
        schema_items = []

        for i, location in enumerate(data):
            safe_name = self._sanitize_text(location.name)
            safe_street = self._sanitize_text(location.street)
            safe_city = self._sanitize_text(location.city)

            json_data.append(
                {
                    "name": safe_name,
                    "street": safe_street,
                    "city": safe_city,
                    "rating": location.rating,
                    "feature_shade": location.feature_shade,
                    "feature_water": location.feature_water,
                    "feature_benches": location.feature_benches,
                    "feature_parking": location.feature_parking,
                    "feature_toilets": location.feature_toilets,
                    "feature_wheelchair_accessible": location.feature_wheelchair_accessible,
                    "feature_kids_friendly": location.feature_kids_friendly,
                    "feature_dogs_allowed": location.feature_dogs_allowed,
                    "feature_fee": location.feature_fee,
                    "feature_seasonal": location.feature_seasonal,
                    "url": self._sanitize_text(location.url),
                }
            )

            # Generate schema.org data
            schema_items.append(
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "item": {
                        "@type": "LocalBusiness",
                        "name": safe_name,
                        "address": {
                            "@type": "PostalAddress",
                            "streetAddress": safe_street,
                            "addressLocality": safe_city,
                            "postalCode": self._sanitize_text(location.postcode),
                            "addressCountry": self._sanitize_text(location.country),
                        },
                        "geo": {
                            "@type": "GeoCoordinates",
                            "latitude": location.latitude,
                            "longitude": location.longitude,
                        },
                        "url": self._sanitize_text(location.url),
                        "telephone": self._sanitize_text(location.phone),
                        "aggregateRating": (
                            {
                                "@type": "AggregateRating",
                                "ratingValue": location.rating,
                                "reviewCount": location.review_count,
                            }
                            if location.rating > 0
                            else None
                        ),
                    },
                }
        )

        # Replace placeholders
        page_content = template.replace("{{CITY}}", self._sanitize_text(city))
        page_content = page_content.replace("{{CATEGORY}}", self._sanitize_text(category))
        page_content = page_content.replace(
            "{{CANONICAL_URL}}", self._sanitize_text(canonical_url)
        )

        # Insert JSON data (already sanitized) into template
        json_string = json.dumps(json_data, ensure_ascii=False, indent=2)
        page_content = page_content.replace(
            "/* DATA_PLACEHOLDER */",
            f"const DATA = {json_string};"
        )

        # Update schema.org
        schema_string = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": f"{category} in {city}",
                "itemListElement": schema_items,
            },
            ensure_ascii=False,
            indent=2,
        )

        # Write output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_content)

        print(f"✅ Generated pillar page: {output_path}")


def example_usage():
    """Example of how to use the system"""

    # 1. Initialize scraper
    scraper = DataScraper(delay=1.0)

    # 2. Sample data (in real scenario, you'd scrape this)
    sample_data = [
        LocationData(
            id="park_001",
            name="Muster Park",
            street="Musterstraße 123",
            city="Berlin",
            region="Berlin",
            country="Deutschland",
            postcode="10115",
            latitude=52.5200,
            longitude=13.4050,
            url="https://example.com",
            phone="+49 30 123456",
            email="info@park.de",
            opening_hours="Mo-So 06:00-22:00",
            rating=4.2,
            review_count=156,
            feature_shade=True,
            feature_benches=True,
            feature_water=True,
            feature_parking=False,
            feature_toilets=True,
            feature_wheelchair_accessible=True,
            feature_kids_friendly=True,
            feature_dogs_allowed=True,
            feature_fee=False,
            feature_seasonal=False,
            tags="park,outdoor,recreation",
        )
    ]

    # 3. Generate pillar page
    generator = PillarPageGenerator("pillar_page_skeleton.html")
    generator.generate_page(
        data=sample_data,
        city="Berlin",
        category="Parks",
        output_path="berlin_parks.html",
        canonical_url="https://yourdomain.com/berlin-parks",
    )

    print("🎉 Example completed! Check berlin_parks.html")


if __name__ == "__main__":
    example_usage()
