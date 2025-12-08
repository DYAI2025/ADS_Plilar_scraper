import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

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


if __name__ == "__main__":
    main()
