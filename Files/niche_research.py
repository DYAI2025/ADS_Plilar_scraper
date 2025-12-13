import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote
import re
from collections import Counter
import os
import sys

# Import GooglePlacesScraper for review data
try:
    from enhanced_scrapers import GooglePlacesScraper
except ImportError:
    # Fallback for when running from different directory
    sys.path.insert(0, os.path.dirname(__file__))
    from enhanced_scrapers import GooglePlacesScraper

import pandas as pd
import requests


class KeywordResearch:
    """Research keywords and validate niches"""

    def __init__(self):
        self.session = requests.Session()

    def check_serp_diversity(self, keyword: str) -> Dict:
        """
        Analyze SERP diversity for a keyword
        Returns diversity score and top domains
        """
        # This is a simplified version - in production you'd use SEO APIs
        # like Ahrefs, SEMrush, or custom SERP scraping

        print(f"🔍 Analyzing SERP for: {keyword}")

        # Simulated SERP analysis
        # In real implementation, scrape Google results
        mock_serp = {
            "keyword": keyword,
            "diversity_score": 0.7,  # 0-1, higher = more diverse intents
            "top_domains": [
                "yelp.com",
                "tripadvisor.com",
                "foursquare.com",
                "local-site.de",
            ],
            "intent_types": ["informational", "local", "commercial"],
            "estimated_traffic": 8500,
            "keyword_difficulty": 18,
        }

        return mock_serp

    def generate_keyword_variations(
        self, base_keyword: str, cities: List[str]
    ) -> List[Dict]:
        """Generate keyword variations for multiple cities"""

        patterns = [
            "{keyword} in {city}",
            "{keyword} {city}",
            "best {keyword} in {city}",
            "{keyword} near {city}",
            "{city} {keyword}",
            "{keyword} {city} guide",
            "top {keyword} {city}",
        ]

        keywords = []
        for city in cities:
            for pattern in patterns:
                keyword = pattern.format(keyword=base_keyword, city=city)
                keywords.append(
                    {
                        "keyword": keyword,
                        "city": city,
                        "pattern": pattern,
                        "estimated_volume": self._estimate_volume(keyword),
                        "competition": self._estimate_competition(keyword),
                    }
                )

        return keywords

    def _estimate_volume(self, keyword: str) -> int:
        """Estimate search volume (mock implementation)"""
        base_volume = len(keyword.split()) * 1000
        return max(100, base_volume + (hash(keyword) % 5000))

    def _estimate_competition(self, keyword: str) -> str:
        """Estimate competition level"""
        score = hash(keyword) % 100
        if score < 30:
            return "Low"
        elif score < 70:
            return "Medium"
        else:
            return "High"


class NicheValidator:
    """Validate niche opportunities using live geo data instead of placeholders"""

    def __init__(
        self,
        config_path: str = "quick_config.json",
        data_sources: Optional[List[Path]] = None,
    ):
        self.config = self._load_config(config_path)
        self.data_sources = data_sources or [
            Path("data/babelsberg_locations.csv"),
            Path("data/active.csv"),
            Path("data/collected_data.csv"),
        ]
        self.analytics_df = self._load_geolocation_data()
        self.niches = self._build_dynamic_niches()

    def _load_config(self, config_path: str) -> Dict:
        path = Path(config_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        return {
            "city": "Berlin",
            "category": "Parks",
            "google_api_key": "",
        }

    @staticmethod
    def _normalize_bool(series: pd.Series) -> pd.Series:
        return series.astype(str).str.upper().isin({"TRUE", "1", "JA", "YES", "Y"})

    def _load_geolocation_data(self) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []
        for path in self.data_sources:
            if not path.exists():
                continue
            try:
                df = pd.read_csv(path)
                frames.append(df)
            except Exception as exc:
                print(f"⚠️  Konnte {path} nicht laden: {exc}")

        if not frames:
            return pd.DataFrame()

        df = pd.concat(frames, ignore_index=True, sort=False)
        if "review_count" in df.columns:
            df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce").fillna(0)
        if "rating" in df.columns:
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
        return df

    @staticmethod
    def _feature_to_label(feature_name: str) -> str:
        mapping = {
            "feature_dogs_allowed": "Hundefreundliche Spots",
            "feature_kids_friendly": "Familienfreundliche Orte",
            "feature_parking": "Parkplätze in der Nähe",
            "feature_toilets": "Orte mit Toiletten",
            "feature_water": "Am Wasser",
            "feature_shade": "Schattenplätze",
            "feature_wheelchair_accessible": "Barrierefreie Orte",
            "feature_restaurant": "Gastro & Snacks",
        }
        return mapping.get(feature_name, feature_name.replace("feature_", "").replace("_", " ").title())

    @staticmethod
    def _monetization_bucket(total_reviews: float) -> str:
        if total_reviews >= 10000:
            return "high"
        if total_reviews >= 2500:
            return "medium"
        return "emerging"

    def _extract_tags(self, feature_df: pd.DataFrame) -> List[str]:
        if "tags" not in feature_df.columns:
            return []

        tag_scores: Dict[str, float] = {}
        for _, row in feature_df.iterrows():
            weight = float(row.get("review_count", 0)) or 1.0
            for tag in str(row.get("tags", "")).split(","):
                tag_clean = tag.strip()
                if not tag_clean:
                    continue
                tag_scores[tag_clean] = tag_scores.get(tag_clean, 0.0) + weight

        return [tag for tag, _ in sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)]

    def _build_dynamic_niches(self) -> List[Dict]:
        if self.analytics_df.empty:
            return []

        feature_columns = [col for col in self.analytics_df.columns if col.startswith("feature_")]
        niches: List[Dict] = []

        for feature in feature_columns:
            feature_mask = self._normalize_bool(self.analytics_df[feature])
            feature_df = self.analytics_df[feature_mask]
            if feature_df.empty:
                continue

            total_reviews = float(feature_df.get("review_count", pd.Series([])).sum())
            tags = self._extract_tags(feature_df)
            display_name = self._feature_to_label(feature)
            niche_keywords = [display_name.lower()] + [t.lower() for t in tags[:3]]

            niches.append(
                {
                    "name": display_name,
                    "feature_column": feature,
                    "keywords": niche_keywords,
                    "facets": tags[:5] if tags else [display_name],
                    "cities": [self.config.get("city", "") or "Berlin"],
                    "seasonality": "live",
                    "monetization_potential": self._monetization_bucket(total_reviews),
                    "analytics": {
                        "locations": len(feature_df),
                        "total_reviews": int(total_reviews),
                        "avg_rating": round(feature_df.get("rating", pd.Series([])).mean(), 2),
                    },
                }
            )

        niches.sort(key=lambda n: n["analytics"]["total_reviews"], reverse=True)
        return niches

    def analyze_niche(self, niche_name: str) -> Dict:
        """Analyze a specific niche opportunity based on collected geo data"""

        niche = next(
            (n for n in self.niches if n["name"].lower() == niche_name.lower()), None
        )
        if not niche:
            return {"error": f'Niche "{niche_name}" not found'}

        feature_df = self.analytics_df[
            self._normalize_bool(self.analytics_df[niche["feature_column"]])
        ]

        print(f"📊 Analyzing niche: {niche['name']}")

        researcher = KeywordResearch()
        base_city = niche["cities"][0]
        all_keywords: List[Dict] = []

        for keyword in niche["keywords"][:3]:
            variations = researcher.generate_keyword_variations(keyword, [base_city])
            for entry in variations:
                entry["estimated_volume"] = int(niche["analytics"]["total_reviews"])
                entry["competition"] = (
                    "Low" if niche["analytics"]["total_reviews"] < 2500 else "Medium"
                )
            all_keywords.extend(variations)

        total_volume = sum(kw["estimated_volume"] for kw in all_keywords)
        low_competition_count = sum(
            1 for kw in all_keywords if kw["competition"].lower() == "low"
        )

        opportunity_score = min(
            100,
            (total_volume / 1000)
            + (float(feature_df.get("rating", pd.Series([])).mean()) * 5)
            + (low_competition_count * 2),
        )

        return {
            "niche": niche,
            "keywords": all_keywords,
            "total_estimated_volume": total_volume,
            "low_competition_keywords": low_competition_count,
            "opportunity_score": round(opportunity_score, 1),
            "recommended": opportunity_score > 50,
            "analytics": niche["analytics"],
        }

    def get_niche_recommendations(self) -> List[Dict]:
        """Get all niche recommendations ranked by opportunity"""

        recommendations = []
        for niche in self.niches:
            analysis = self.analyze_niche(niche["name"])
            if "error" not in analysis:
                recommendations.append(analysis)

        # Sort by opportunity score
        recommendations.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return recommendations


def analyze_competition(keyword: str, city: str) -> Dict:
    """Analyze competition for a keyword in a specific city"""

    print(f"🔍 Analyzing competition: '{keyword}' in {city}")

    # Mock competition analysis
    # In production: scrape SERP, analyze domain authority, content quality

    mock_analysis = {
        "keyword": f"{keyword} {city}",
        "serp_features": ["local_pack", "knowledge_panel", "reviews"],
        "top_competitors": [
            {"domain": "yelp.com", "da": 95, "content_quality": "medium"},
            {"domain": "tripadvisor.com", "da": 92, "content_quality": "high"},
            {"domain": "local-guide.de", "da": 35, "content_quality": "low"},
        ],
        "content_gaps": [
            "Keine Filtermöglichkeiten nach Ausstattung",
            "Wenig strukturierte Daten",
            "Schlechte mobile Erfahrung",
        ],
        "opportunity_score": 75,
        "recommended_approach": "Pillar page with filtering and structured data",
    }

    return mock_analysis


def generate_launch_plan(niche: str, city: str, target_keywords: List[str]) -> Dict:
    """Generate a 7-day launch plan"""

    plan = {
        "niche": niche,
        "city": city,
        "target_keywords": target_keywords,
        "timeline": {
            "day_1": {
                "tasks": [
                    "Domain registrieren oder Subdomain einrichten",
                    "WordPress/Static Site Setup",
                    "AdSense Konto anlegen",
                    "Google Search Console einrichten",
                ],
                "deliverables": ["Live Website", "Analytics Setup"],
            },
            "day_2_3": {
                "tasks": [
                    "Datensammlung (20-50 Locations)",
                    "Review-Analyse für Feature-Extraktion",
                    "CSV mit allen Facetten erstellen",
                    "Erste SERP-Positionen checken",
                ],
                "deliverables": ["Vollständige Datenbank", "Feature Matrix"],
            },
            "day_4_5": {
                "tasks": [
                    "Pillar-Seite aus Template generieren",
                    "JSON-LD Schema implementieren",
                    "Interne Verlinkung aufbauen",
                    "Mobile Optimierung testen",
                ],
                "deliverables": ["Launch-bereite Pillar Page"],
            },
            "day_6": {
                "tasks": [
                    "AdSense Auto Ads aktivieren",
                    "ads.txt hochladen",
                    "CMP für DSGVO einrichten",
                    "Site bei Google einreichen",
                ],
                "deliverables": ["Vollständige Monetarisierung"],
            },
            "day_7": {
                "tasks": [
                    "Analytics Tracking einrichten",
                    "Erste Performance-Metriken",
                    "Plan für Skalierung (weitere Städte)",
                    "Content-Pipeline für Updates",
                ],
                "deliverables": ["Monitoring Dashboard", "Skalierungsplan"],
            },
        },
        "kpis": {
            "week_1": "Indexierung + erste Impressions",
            "month_1": "1,000+ Impressions, CTR > 2%",
            "month_3": "10,000+ Impressions, Page RPM > €8",
            "month_6": "50,000+ Impressions, €500+ Revenue",
        },
    }

    return plan


def main():
    """Run niche analysis and generate recommendations"""

    print("🚀 ADS Pillar - Nische Analyse")
    print("=" * 50)

    validator = NicheValidator()

    # Get all recommendations
    recommendations = validator.get_niche_recommendations()

    print(f"\n📈 Top {len(recommendations)} Nischen-Empfehlungen:")
    for i, rec in enumerate(recommendations, 1):
        niche = rec["niche"]
        score = rec["opportunity_score"]
        volume = rec["total_estimated_volume"]

        print(f"\n{i}. {niche['name']} (Score: {score})")
        print(f"   📊 Suchvolumen: {volume:,}")
        print(f"   🎯 Keywords: {', '.join(niche['keywords'][:3])}")
        print(f"   🏙️  Städte: {', '.join(niche['cities'][:3])}")
        print(f"   💰 Potenzial: {niche['monetization_potential'].title()}")

        if i <= 3:  # Show details for top 3
            print(f"   🔍 Facetten: {', '.join(niche['facets'][:5])}")

    # Detailed analysis for top recommendation
    if recommendations:
        top_niche = recommendations[0]
        print(f"\n🔬 Detailanalyse: {top_niche['niche']['name']}")
        print("-" * 40)

        # Show some sample keywords
        sample_keywords = top_niche["keywords"][:5]
        for kw in sample_keywords:
            print(
                f"   • {kw['keyword']} (Vol: {kw['estimated_volume']}, Comp: {kw['competition']})"
            )

        # Generate launch plan
        plan = generate_launch_plan(
            niche=top_niche["niche"]["name"],
            city=top_niche["niche"]["cities"][0],
            target_keywords=[kw["keyword"] for kw in sample_keywords],
        )

        print(f"\n📅 7-Tage Startplan für {plan['niche']} in {plan['city']}:")
        for day, details in plan["timeline"].items():
            print(f"\n   {day.replace('_', ' ').title()}:")
            for task in details["tasks"][:2]:  # Show first 2 tasks
                print(f"     • {task}")

        print(f"\n🎯 KPI-Ziele:")
        for period, goal in plan["kpis"].items():
            print(f"   • {period}: {goal}")

    print(f"\n✨ Nächste Schritte:")
    print(f"   1. Wähle eine Nische aus der obigen Liste")
    print(f"   2. Führe SERP-Analyse für deine Zielstadt durch")
    print(f"   3. Sammle 20-50 Locations und extrahiere Facetten")
    print(f"   4. Generiere Pillar-Seite mit data_pipeline.py")
    print(f"   5. Aktiviere AdSense und starte Monitoring")


class ReviewDemandAnalyzer:
    """
    Analyzes Google Places reviews to extract hidden user demands and content opportunities.

    This class identifies:
    - Top complaints from negative reviews (what users are missing)
    - Top praised features from positive reviews (what users expect)
    - Unmet needs (features mentioned in complaints but not listed by competitors)
    - Content ideas based on review insights
    """

    def __init__(self, api_key: str, delay: float = 1.0):
        """
        Initialize the ReviewDemandAnalyzer.

        Args:
            api_key: Google Places API key
            delay: Delay between API calls (seconds)
        """
        self.scraper = GooglePlacesScraper(api_key=api_key, delay=delay)
        self.api_key = api_key

        # Feature keywords for unmet needs detection (German + English)
        self.feature_keywords = {
            "parking": ["parkplatz", "parken", "parking", "stellplatz"],
            "shade": ["schatten", "schattig", "shade", "shaded", "shady"],
            "toilets": ["toilette", "toiletten", "wc", "toilet", "restroom", "bathroom"],
            "playground": ["spielplatz", "playground", "kinder"],
            "benches": ["bank", "bänke", "bench", "benches", "sitzgelegenheit"],
            "wheelchair_accessible": ["rollstuhl", "barrierefrei", "wheelchair", "accessible", "handicap"],
            "water_fountain": ["wasserbrunnen", "trinkbrunnen", "water fountain", "drinking fountain"],
            "dog_friendly": ["hund", "hunde", "dog", "dogs", "haustier", "pet"],
            "wifi": ["wifi", "wlan", "internet"],
            "outlets": ["steckdose", "steckdosen", "outlet", "outlets", "power"],
        }

    def get_reviews_for_category(self, category: str, city: str,
                                 max_places: int = 30) -> List[Dict]:
        """
        Fetch all reviews for a specific category and city.

        Args:
            category: Category to search (e.g., "parks", "cafes")
            city: City name
            max_places: Maximum number of places to analyze

        Returns:
            List of review dictionaries with structure:
            {
                "place_name": str,
                "place_id": str,
                "rating": float (1-5),
                "text": str,
                "author": str (optional)
            }
        """
        print(f"🔍 Fetching reviews for '{category}' in {city}...")

        # Search for places
        places = self.scraper.search_places(category, city)

        if not places:
            print(f"❌ No places found for '{category}' in {city}")
            return []

        print(f"📍 Found {len(places)} places, enriching with reviews...")

        # Limit to max_places to avoid excessive API calls
        places_to_analyze = places[:max_places]

        all_reviews = []

        for i, place in enumerate(places_to_analyze):
            print(f"   Processing {i+1}/{len(places_to_analyze)}: {place.name}")

            if not place.place_id:
                continue

            # Get detailed reviews for this place
            reviews = self._get_place_reviews(place.place_id)

            for review in reviews:
                review["place_name"] = place.name
                review["place_id"] = place.place_id
                all_reviews.append(review)

            time.sleep(self.scraper.delay)

        print(f"✅ Collected {len(all_reviews)} reviews from {len(places_to_analyze)} places")
        return all_reviews

    def _get_place_reviews(self, place_id: str) -> List[Dict]:
        """
        Get all reviews for a specific place.

        Args:
            place_id: Google Places ID

        Returns:
            List of review dictionaries
        """
        url = f"{self.scraper.base_url}/details/json"
        params = {
            "place_id": place_id,
            "key": self.api_key,
            "fields": "reviews",
            "language": "de",  # Prefer German reviews
        }

        try:
            response = self.scraper.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                return []

            result = data.get("result", {})
            reviews = result.get("reviews", [])

            # Extract relevant fields
            processed_reviews = []
            for review in reviews:
                processed_reviews.append({
                    "rating": review.get("rating", 3),
                    "text": review.get("text", ""),
                    "author": review.get("author_name", "Anonymous"),
                    "time": review.get("time", 0),
                })

            return processed_reviews

        except Exception as e:
            print(f"⚠️  Error fetching reviews for place {place_id}: {e}")
            return []

    def analyze_review_sentiment(self, category: str, city: str,
                                 min_reviews: int = 100,
                                 max_places: int = 30) -> Dict:
        """
        Analyze reviews to identify complaints, praise, and unmet needs.

        Args:
            category: Category to analyze
            city: City name
            min_reviews: Minimum number of reviews needed for analysis
            max_places: Maximum places to analyze

        Returns:
            Dictionary with analysis results:
            {
                "total_reviews_analyzed": int,
                "avg_rating": float,
                "sentiment_score": float,
                "top_complaints": [(phrase, count), ...],
                "top_praise": [(phrase, count), ...],
                "unmet_needs": [(feature, count), ...],
                "complaint_keywords": [(keyword, count), ...],
                "praise_keywords": [(keyword, count), ...]
            }
        """
        # Fetch all reviews
        all_reviews = self.get_reviews_for_category(category, city, max_places)

        if len(all_reviews) < min_reviews:
            print(f"⚠️  Warning: Only {len(all_reviews)} reviews found (min: {min_reviews})")
            print(f"   Analysis may be less accurate with limited data")

        if not all_reviews:
            return {
                "total_reviews_analyzed": 0,
                "avg_rating": 0.0,
                "sentiment_score": 0.0,
                "top_complaints": [],
                "top_praise": [],
                "unmet_needs": [],
                "complaint_keywords": [],
                "praise_keywords": []
            }

        # Categorize reviews by rating
        complaints = [r for r in all_reviews if r["rating"] <= 2]
        praise = [r for r in all_reviews if r["rating"] >= 4]
        neutral = [r for r in all_reviews if 2 < r["rating"] < 4]

        print(f"\n📊 Review Distribution:")
        print(f"   ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ (Praise): {len(praise)} ({len(praise)*100//len(all_reviews)}%)")
        print(f"   ⭐⭐⭐ (Neutral): {len(neutral)} ({len(neutral)*100//len(all_reviews)}%)")
        print(f"   ⭐⭐ / ⭐ (Complaints): {len(complaints)} ({len(complaints)*100//len(all_reviews)}%)")

        # Extract phrases from complaints and praise
        print(f"\n🔍 Extracting patterns from reviews...")
        top_complaints = self._extract_top_phrases([r["text"] for r in complaints], negative=True)
        top_praise = self._extract_top_phrases([r["text"] for r in praise], negative=False)

        # Extract keywords
        complaint_keywords = self._extract_keywords([r["text"] for r in complaints], negative=True)
        praise_keywords = self._extract_keywords([r["text"] for r in praise], negative=False)

        # Find unmet needs
        unmet_needs = self._find_unmet_needs(top_complaints)

        # Calculate sentiment
        avg_rating = sum(r["rating"] for r in all_reviews) / len(all_reviews)
        sentiment_score = avg_rating / 5.0

        return {
            "total_reviews_analyzed": len(all_reviews),
            "avg_rating": round(avg_rating, 2),
            "sentiment_score": round(sentiment_score, 2),
            "top_complaints": top_complaints[:15],
            "top_praise": top_praise[:15],
            "unmet_needs": unmet_needs[:10],
            "complaint_keywords": complaint_keywords[:20],
            "praise_keywords": praise_keywords[:20]
        }

    def _extract_top_phrases(self, texts: List[str], negative: bool = False,
                            max_phrases: int = 50) -> List[Tuple[str, int]]:
        """
        Extract most common 2-4 word phrases from texts.

        Args:
            texts: List of review texts
            negative: If True, focus on negative sentiment phrases
            max_phrases: Maximum number of phrases to return

        Returns:
            List of (phrase, count) tuples sorted by count
        """
        if not texts:
            return []

        # Sentiment indicator keywords
        if negative:
            indicators = [
                "kein", "keine", "fehlt", "fehlen", "vermisse", "vermissen",
                "schlecht", "schade", "leider", "nicht", "wenig", "zu wenig",
                "dreckig", "schmutzig", "kaputt", "defekt",
                "no", "missing", "lack", "poor", "bad", "dirty", "broken"
            ]
        else:
            indicators = [
                "toll", "super", "schön", "gut", "perfekt", "empfehlen",
                "liebe", "beste", "viel", "genug", "sauber", "gepflegt",
                "great", "good", "nice", "perfect", "clean", "well-maintained",
                "excellent", "beautiful", "love", "best"
            ]

        phrases = []

        for text in texts:
            if not text:
                continue

            text_lower = text.lower()

            # Split into sentences
            sentences = re.split(r'[.!?]+', text_lower)

            for sentence in sentences:
                # Check if sentence contains indicator words
                has_indicator = any(ind in sentence for ind in indicators)

                if not has_indicator:
                    continue

                # Clean and tokenize
                sentence = re.sub(r'[^\w\s]', ' ', sentence)
                words = sentence.split()

                # Extract 2-4 word phrases
                for n in [2, 3, 4]:
                    for i in range(len(words) - n + 1):
                        phrase = " ".join(words[i:i+n])

                        # Filter out phrases that are too generic
                        if len(phrase) >= 8 and not self._is_too_generic(phrase):
                            phrases.append(phrase)

        # Count and sort
        phrase_counts = Counter(phrases)
        return phrase_counts.most_common(max_phrases)

    def _extract_keywords(self, texts: List[str], negative: bool = False,
                         max_keywords: int = 30) -> List[Tuple[str, int]]:
        """
        Extract most common single keywords from texts.

        Args:
            texts: List of review texts
            negative: If True, focus on negative context
            max_keywords: Maximum keywords to return

        Returns:
            List of (keyword, count) tuples
        """
        if not texts:
            return []

        # Stop words to ignore (German + English)
        stop_words = {
            "der", "die", "das", "und", "oder", "aber", "ist", "sind", "war", "waren",
            "ein", "eine", "einen", "einem", "eines", "mit", "zu", "auf", "für", "von",
            "in", "im", "am", "an", "bei", "nach", "vor", "über", "unter", "auch",
            "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
            "in", "on", "at", "to", "for", "of", "with", "from", "by", "about",
            "sehr", "viel", "mehr", "wenig", "gut", "schlecht", "nice", "good", "bad"
        }

        all_words = []

        for text in texts:
            if not text:
                continue

            # Clean and tokenize
            text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
            words = text_clean.split()

            # Filter meaningful words
            for word in words:
                if (len(word) >= 4 and  # At least 4 characters
                    word not in stop_words and
                    not word.isdigit()):  # Not a number
                    all_words.append(word)

        # Count and return
        word_counts = Counter(all_words)
        return word_counts.most_common(max_keywords)

    def _is_too_generic(self, phrase: str) -> bool:
        """Check if a phrase is too generic to be useful."""
        generic_patterns = [
            r"^sehr\s+", r"^gut\s+", r"^schlecht\s+",
            r"^very\s+", r"^good\s+", r"^bad\s+",
            r"^das\s+ist", r"^die\s+sind", r"^this\s+is", r"^it\s+is"
        ]

        for pattern in generic_patterns:
            if re.match(pattern, phrase):
                return True

        return False

    def _find_unmet_needs(self, complaints: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Identify features mentioned in complaints (unmet needs).

        Args:
            complaints: List of (phrase, count) tuples from complaints

        Returns:
            List of (feature_name, mention_count) tuples
        """
        feature_mentions = {feature: 0 for feature in self.feature_keywords.keys()}

        # Combine all complaint phrases into one text for analysis
        all_complaint_text = " ".join([phrase for phrase, count in complaints])

        # Check for feature keywords
        for feature, keywords in self.feature_keywords.items():
            for keyword in keywords:
                # Count occurrences in complaints
                pattern = r'\b' + re.escape(keyword) + r'\w*'
                matches = re.findall(pattern, all_complaint_text, re.IGNORECASE)
                feature_mentions[feature] += len(matches)

        # Filter out features with no mentions and sort by count
        unmet_needs = [(feature, count) for feature, count in feature_mentions.items() if count > 0]
        unmet_needs.sort(key=lambda x: x[1], reverse=True)

        return unmet_needs

    def generate_content_ideas(self, category: str, city: str,
                              max_places: int = 30) -> List[Dict]:
        """
        Generate actionable content ideas based on review analysis.

        Args:
            category: Category to analyze
            city: City name
            max_places: Maximum places to analyze

        Returns:
            List of content idea dictionaries with:
            {
                "type": str (e.g., "FAQ Section", "Filter Feature"),
                "title": str,
                "description": str,
                "priority": str ("High", "Medium", "Low"),
                "estimated_impact": str,
                "implementation": str
            }
        """
        print(f"\n🎯 Generating content ideas for '{category}' in {city}...")

        # Get review analysis
        analysis = self.analyze_review_sentiment(category, city, max_places=max_places)

        if analysis["total_reviews_analyzed"] == 0:
            print("❌ No reviews to analyze - cannot generate content ideas")
            return []

        ideas = []

        # Idea 1: FAQ based on top complaints
        if analysis["top_complaints"]:
            top_complaint_phrase, complaint_count = analysis["top_complaints"][0]
            ideas.append({
                "type": "FAQ Section",
                "title": f"FAQ addressing: '{top_complaint_phrase}'",
                "description": f"Create FAQ section answering common concern mentioned in {complaint_count} reviews",
                "priority": "High",
                "estimated_impact": "CTR +15%, Time on Page +25%",
                "implementation": f"Add FAQ Schema.org markup with answers about '{top_complaint_phrase}'. "
                                 f"Place FAQ section prominently on pillar page."
            })

        # Idea 2: Filter feature based on unmet needs
        if analysis["unmet_needs"]:
            unmet_feature, mention_count = analysis["unmet_needs"][0]
            ideas.append({
                "type": "Filter Feature",
                "title": f"Add filter for: '{unmet_feature}'",
                "description": f"{mention_count} users mentioned missing '{unmet_feature}' - add it as a filterable feature",
                "priority": "High",
                "estimated_impact": "Engagement +30%, RPM +1.5x",
                "implementation": f"1. Scrape '{unmet_feature}' data for all locations\n"
                                 f"2. Add '{unmet_feature}' checkbox to pillar_page_skeleton.html\n"
                                 f"3. Update JavaScript filter logic"
            })

        # Idea 3: "Best of" list based on praise
        if analysis["top_praise"]:
            praise_feature, praise_count = analysis["top_praise"][0]
            ideas.append({
                "type": "Curated Content",
                "title": f"Create 'Best {category.title()} with {praise_feature}' list",
                "description": f"{praise_count} users praised '{praise_feature}' - create curated top-10 list",
                "priority": "Medium",
                "estimated_impact": "Social Shares +40%, Backlinks +20%",
                "implementation": f"1. Sort locations by '{praise_feature}' relevance\n"
                                 f"2. Create dedicated section with top 10\n"
                                 f"3. Add rich snippet markup for List schema"
            })

        # Idea 4: Comparison feature for top complaint
        if len(analysis["unmet_needs"]) >= 2:
            feature1, count1 = analysis["unmet_needs"][0]
            feature2, count2 = analysis["unmet_needs"][1]
            ideas.append({
                "type": "Comparison Tool",
                "title": f"Compare {category} by '{feature1}' and '{feature2}'",
                "description": f"Users care about both features - add comparison matrix",
                "priority": "Medium",
                "estimated_impact": "Session Duration +45%, RPM +1.3x",
                "implementation": f"Create interactive table comparing all locations across these features. "
                                 f"Add sortable columns and visual indicators."
            })

        # Idea 5: Address top complaint keyword in meta description
        if analysis["complaint_keywords"]:
            complaint_kw, kw_count = analysis["complaint_keywords"][0]
            ideas.append({
                "type": "SEO Optimization",
                "title": f"Target keyword: '{complaint_kw}' in content",
                "description": f"Mentioned {kw_count} times in complaints - address it for SEO",
                "priority": "Medium",
                "estimated_impact": "Organic CTR +10%, Rankings +5%",
                "implementation": f"1. Add '{complaint_kw}' to title tag and H2 headings\n"
                                 f"2. Create content section addressing '{complaint_kw}' concerns\n"
                                 f"3. Include in meta description"
            })

        return ideas

    def print_analysis_report(self, category: str, city: str, max_places: int = 30):
        """
        Print a comprehensive analysis report to console.

        Args:
            category: Category to analyze
            city: City name
            max_places: Maximum places to analyze
        """
        print(f"\n{'='*70}")
        print(f"📊 REVIEW DEMAND ANALYSIS REPORT")
        print(f"{'='*70}")
        print(f"Category: {category.title()}")
        print(f"Location: {city}")
        print(f"{'='*70}\n")

        # Get analysis
        analysis = self.analyze_review_sentiment(category, city, max_places=max_places)

        if analysis["total_reviews_analyzed"] == 0:
            print("❌ No data available for analysis\n")
            return

        # Summary stats
        print(f"📈 SUMMARY STATISTICS")
        print(f"{'-'*70}")
        print(f"Total Reviews Analyzed: {analysis['total_reviews_analyzed']}")
        print(f"Average Rating: {analysis['avg_rating']:.2f} / 5.0")
        print(f"Sentiment Score: {analysis['sentiment_score']:.2f} (0.0 = very negative, 1.0 = very positive)")
        print()

        # Top complaints
        print(f"🔴 TOP COMPLAINTS (What Users Are Missing)")
        print(f"{'-'*70}")
        for i, (phrase, count) in enumerate(analysis["top_complaints"][:10], 1):
            print(f"  {i:2d}. '{phrase}' ({count} mentions)")
        print()

        # Top praise
        print(f"🟢 TOP PRAISE (What Users Love)")
        print(f"{'-'*70}")
        for i, (phrase, count) in enumerate(analysis["top_praise"][:10], 1):
            print(f"  {i:2d}. '{phrase}' ({count} mentions)")
        print()

        # Unmet needs
        print(f"💡 UNMET NEEDS (Opportunity Features!)")
        print(f"{'-'*70}")
        if analysis["unmet_needs"]:
            for i, (feature, count) in enumerate(analysis["unmet_needs"], 1):
                print(f"  {i:2d}. {feature.upper()} - {count} complaint mentions ⭐⭐⭐")
        else:
            print("  None detected - all needs seem to be met")
        print()

        # Generate content ideas
        ideas = self.generate_content_ideas(category, city, max_places=max_places)

        print(f"🎯 ACTIONABLE CONTENT IDEAS")
        print(f"{'-'*70}")
        for i, idea in enumerate(ideas, 1):
            print(f"\n{i}. [{idea['priority'].upper()}] {idea['type']}: {idea['title']}")
            print(f"   Description: {idea['description']}")
            print(f"   Impact: {idea['estimated_impact']}")
            print(f"   Implementation:")
            for line in idea['implementation'].split('\n'):
                print(f"     • {line.strip()}")

        print(f"\n{'='*70}")
        print(f"✨ Analysis complete! Use these insights to create high-performing pillar pages.")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
