#!/usr/bin/env python3
"""
Nischen-Konkurrenzanalyse für ADS Pillar
Analysiert Konkurrenten in der Umgebung und schätzt Google-Sichtbarkeit, Traffic und Umsätze
"""

import requests
import re
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import logging
from urllib.parse import quote_plus
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CompetitorData:
    """Data structure for competitor analysis"""

    name: str
    domain: str
    distance_km: float
    rating: float
    review_count: int
    estimated_monthly_visitors: int
    estimated_serp_position: int
    estimated_monthly_revenue: float
    visibility_score: float  # 0-100
    competitive_strength: str  # "Low", "Medium", "High"
    found_via_keywords: List[str] = field(default_factory=list)


@dataclass
class NicheAnalysisResult:
    """Complete niche analysis result"""

    target_niche: str
    target_location: str
    total_competitors_found: int
    avg_competitor_rating: float
    market_saturation: str  # "Low", "Medium", "High"
    opportunity_score: float  # 0-100
    estimated_monthly_searches: int
    estimated_monthly_revenue: Tuple[float, float, float]  # (min, avg, max)
    competitors: List[CompetitorData]
    recommendations: List[str]


class NicheCompetitorAnalyzer:
    """
    Analysiert Nischen-Konkurrenz basierend auf Nutzereingaben
    Unterstützt bilinguale Suche (Deutsch/Englisch)
    """

    # Bilingual search patterns for niche identification
    SEARCH_PATTERNS_DE = [
        "{niche} {location}",
        "beste {niche} {location}",
        "{niche} in {location}",
        "{niche} {location} guide",
        "{niche} {location} finden",
        "top {niche} {location}",
        "{location} {niche}",
    ]

    SEARCH_PATTERNS_EN = [
        "{niche} {location}",
        "best {niche} {location}",
        "{niche} in {location}",
        "{niche} near {location}",
        "top {niche} {location}",
        "{location} {niche} guide",
    ]

    def __init__(self, google_api_key: Optional[str] = None, delay: float = 1.5):
        """
        Initialize analyzer

        Args:
            google_api_key: Google Places API key (optional, for enhanced data)
            delay: Delay between API requests in seconds
        """
        self.google_api_key = google_api_key
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def analyze_niche_competition(
        self,
        target_niche: str,
        location: str,
        radius_km: float = 10.0,
        language: str = "both",  # "de", "en", or "both"
    ) -> NicheAnalysisResult:
        """
        Hauptfunktion für Nischen-Konkurrenzanalyse

        Args:
            target_niche: Freitext-Nischenbeschreibung (z.B. "Hundeparks", "Coworking Cafés")
            location: Stadt/Region (z.B. "Berlin", "München")
            radius_km: Suchradius in Kilometern
            language: Suchsprache ("de", "en", "both")

        Returns:
            NicheAnalysisResult mit vollständiger Konkurrenz-Analyse
        """
        logger.info(f"🔍 Analyzing niche: '{target_niche}' in {location}")

        # Generate search keywords bilingual
        search_keywords = self._generate_search_keywords(
            target_niche, location, language
        )
        logger.info(f"Generated {len(search_keywords)} search variations")

        # Find competitors via multiple sources
        competitors = []
        if self.google_api_key:
            competitors.extend(
                self._find_competitors_google_places(
                    search_keywords, location, radius_km
                )
            )
        else:
            logger.warning(
                "No Google API key provided - using estimation-based analysis"
            )
            competitors.extend(
                self._find_competitors_estimated(search_keywords, location)
            )

        # Deduplicate competitors
        unique_competitors = self._deduplicate_competitors(competitors)
        logger.info(f"Found {len(unique_competitors)} unique competitors")

        # Calculate market metrics
        market_saturation = self._calculate_market_saturation(
            len(unique_competitors), radius_km
        )
        avg_rating = (
            sum(c.rating for c in unique_competitors) / len(unique_competitors)
            if unique_competitors
            else 0.0
        )

        # Estimate search volume and revenue potential
        monthly_searches = self._estimate_search_volume(target_niche, location)
        revenue_estimates = self._estimate_revenue_potential(
            monthly_searches, len(unique_competitors), market_saturation
        )

        # Calculate opportunity score
        opportunity_score = self._calculate_opportunity_score(
            len(unique_competitors),
            avg_rating,
            market_saturation,
            monthly_searches,
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            opportunity_score, market_saturation, len(unique_competitors)
        )

        return NicheAnalysisResult(
            target_niche=target_niche,
            target_location=location,
            total_competitors_found=len(unique_competitors),
            avg_competitor_rating=round(avg_rating, 2),
            market_saturation=market_saturation,
            opportunity_score=round(opportunity_score, 1),
            estimated_monthly_searches=monthly_searches,
            estimated_monthly_revenue=revenue_estimates,
            competitors=unique_competitors,
            recommendations=recommendations,
        )

    def _generate_search_keywords(
        self, niche: str, location: str, language: str = "both"
    ) -> List[str]:
        """Generate bilingual search keyword variations"""
        keywords = []

        patterns = []
        if language in ["de", "both"]:
            patterns.extend(self.SEARCH_PATTERNS_DE)
        if language in ["en", "both"]:
            patterns.extend(self.SEARCH_PATTERNS_EN)

        for pattern in patterns:
            keyword = pattern.format(niche=niche, location=location)
            keywords.append(keyword)

        return list(set(keywords))  # Remove duplicates

    def _find_competitors_google_places(
        self, keywords: List[str], location: str, radius_km: float
    ) -> List[CompetitorData]:
        """Find competitors using Google Places API"""
        competitors = []
        base_url = "https://maps.googleapis.com/maps/api/place"

        # Use first 3 keywords to avoid excessive API calls
        for keyword in keywords[:3]:
            try:
                url = f"{base_url}/textsearch/json"
                params = {
                    "query": keyword,
                    "key": self.google_api_key,
                }

                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") != "OK":
                    logger.warning(f"API status: {data.get('status')} for '{keyword}'")
                    continue

                for idx, place in enumerate(data.get("results", [])[:10]):
                    competitor = self._parse_competitor_from_place(
                        place, keyword, idx + 1
                    )
                    if competitor:
                        competitors.append(competitor)

                time.sleep(self.delay)

            except Exception as e:
                logger.error(f"Error searching for '{keyword}': {e}")
                continue

        return competitors

    def _find_competitors_estimated(
        self, keywords: List[str], location: str
    ) -> List[CompetitorData]:
        """Estimate competitors without API (fallback method)"""
        competitors = []

        # Generate realistic dummy data based on niche
        num_competitors = self._estimate_competitor_count(keywords[0] if keywords else "")

        for i in range(num_competitors):
            competitor = CompetitorData(
                name=f"Competitor {i+1}",
                domain=f"example-{i+1}.com",
                distance_km=round((i + 1) * 0.8, 1),
                rating=round(3.5 + (hash(f"{i}") % 15) / 10, 1),
                review_count=50 + (hash(f"{i}") % 200),
                estimated_monthly_visitors=500 + (hash(f"{i}") % 2000),
                estimated_serp_position=i + 1,
                estimated_monthly_revenue=round(
                    (10 + (hash(f"{i}") % 50)) * ((num_competitors - i) / num_competitors),
                    2,
                ),
                visibility_score=round(
                    80 - (i * 5) + (hash(f"{i}") % 10), 1
                ),
                competitive_strength=self._classify_strength(i + 1),
                found_via_keywords=[keywords[0] if keywords else ""],
            )
            competitors.append(competitor)

        return competitors

    def _parse_competitor_from_place(
        self, place_data: Dict, keyword: str, position: int
    ) -> Optional[CompetitorData]:
        """Parse competitor data from Google Places result"""
        try:
            name = place_data.get("name", "")
            rating = place_data.get("rating", 0.0)
            review_count = place_data.get("user_ratings_total", 0)

            # Estimate metrics based on rating and review count
            visibility_score = min(
                100, (rating / 5.0 * 50) + (min(review_count, 200) / 200 * 50)
            )
            monthly_visitors = self._estimate_visitors_from_reviews(review_count)
            monthly_revenue = self._estimate_revenue_from_traffic(monthly_visitors, position)

            return CompetitorData(
                name=name,
                domain=self._extract_domain_from_place(place_data),
                distance_km=0.0,  # Would need geocoding
                rating=rating,
                review_count=review_count,
                estimated_monthly_visitors=monthly_visitors,
                estimated_serp_position=position,
                estimated_monthly_revenue=monthly_revenue,
                visibility_score=round(visibility_score, 1),
                competitive_strength=self._classify_strength(position),
                found_via_keywords=[keyword],
            )

        except Exception as e:
            logger.error(f"Error parsing competitor: {e}")
            return None

    def _deduplicate_competitors(
        self, competitors: List[CompetitorData]
    ) -> List[CompetitorData]:
        """Remove duplicate competitors"""
        seen_names = set()
        unique = []

        for comp in competitors:
            name_key = comp.name.lower().strip()
            if name_key not in seen_names:
                seen_names.add(name_key)
                unique.append(comp)

        return unique

    def _estimate_search_volume(self, niche: str, location: str) -> int:
        """Estimate monthly search volume for niche + location"""
        # Realistic estimation based on word count and location size
        base_volume = 500

        # Major cities get more searches
        major_cities = ["berlin", "münchen", "hamburg", "köln", "frankfurt"]
        if any(city in location.lower() for city in major_cities):
            base_volume *= 3

        # Niche complexity affects volume
        niche_words = len(niche.split())
        volume = int(base_volume * (1.5 ** (niche_words - 1)))

        # Add some variance
        volume += (hash(f"{niche}{location}") % 1000)

        return max(100, min(50000, volume))

    def _estimate_revenue_potential(
        self, monthly_searches: int, competitor_count: int, saturation: str
    ) -> Tuple[float, float, float]:
        """
        Estimate monthly revenue potential (min, avg, max)

        Based on:
        - Monthly searches (traffic potential)
        - Competitor count (market share)
        - Market saturation (difficulty)
        - Typical AdSense RPM: €8-€25
        """
        # Estimate your potential share
        if saturation == "Low":
            traffic_share = 0.3
        elif saturation == "Medium":
            traffic_share = 0.15
        else:  # High
            traffic_share = 0.08

        # Account for competitors
        if competitor_count > 0:
            traffic_share /= math.log(competitor_count + 2)

        estimated_monthly_visitors = int(monthly_searches * traffic_share)

        # RPM scenarios (conservative, realistic, optimistic)
        rpm_min, rpm_avg, rpm_max = 8.0, 15.0, 25.0

        # Revenue = (Visitors / 1000) * RPM
        revenue_min = (estimated_monthly_visitors / 1000) * rpm_min
        revenue_avg = (estimated_monthly_visitors / 1000) * rpm_avg
        revenue_max = (estimated_monthly_visitors / 1000) * rpm_max

        return (
            round(revenue_min, 2),
            round(revenue_avg, 2),
            round(revenue_max, 2),
        )

    def _calculate_market_saturation(
        self, competitor_count: int, radius_km: float
    ) -> str:
        """Calculate market saturation level"""
        density = competitor_count / (radius_km * radius_km)

        if density < 0.5:
            return "Low"
        elif density < 1.5:
            return "Medium"
        else:
            return "High"

    def _calculate_opportunity_score(
        self,
        competitor_count: int,
        avg_rating: float,
        saturation: str,
        monthly_searches: int,
    ) -> float:
        """
        Calculate overall opportunity score (0-100)

        Higher score = better opportunity
        """
        score = 50.0  # Base score

        # Fewer competitors = higher score
        if competitor_count < 5:
            score += 20
        elif competitor_count < 10:
            score += 10
        else:
            score -= 10

        # Lower avg rating = opportunity to outrank
        if avg_rating < 3.5:
            score += 15
        elif avg_rating < 4.0:
            score += 5

        # Market saturation
        if saturation == "Low":
            score += 20
        elif saturation == "Medium":
            score += 5
        else:
            score -= 15

        # Search volume
        if monthly_searches > 5000:
            score += 15
        elif monthly_searches > 1000:
            score += 10
        elif monthly_searches < 200:
            score -= 10

        return max(0, min(100, score))

    def _generate_recommendations(
        self, opportunity_score: float, saturation: str, competitor_count: int
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if opportunity_score >= 70:
            recommendations.append(
                "🟢 Excellent opportunity! Low competition and good search volume."
            )
            recommendations.append(
                "Launch a comprehensive pillar page with detailed filters and features."
            )
        elif opportunity_score >= 50:
            recommendations.append(
                "🟡 Moderate opportunity. Focus on differentiation and quality."
            )
            recommendations.append(
                "Add unique features or filters not available on competitor sites."
            )
        else:
            recommendations.append(
                "🔴 High competition. Consider targeting a sub-niche or different location."
            )
            recommendations.append(
                "Focus on long-tail keywords and very specific user intents."
            )

        if saturation == "High":
            recommendations.append(
                "Consider expanding to nearby cities with lower competition."
            )

        if competitor_count < 3:
            recommendations.append(
                "Very few competitors - you could dominate this niche quickly!"
            )

        recommendations.append(
            "Collect 30-50 locations with detailed features for best SERP performance."
        )

        return recommendations

    def _estimate_competitor_count(self, keyword: str) -> int:
        """Estimate realistic competitor count based on keyword"""
        # Hash-based but realistic
        base = 5 + (hash(keyword) % 15)
        return base

    def _estimate_visitors_from_reviews(self, review_count: int) -> int:
        """Estimate monthly visitors from review count"""
        # Rough estimate: 1 review per 100-200 visitors
        return review_count * 150

    def _estimate_revenue_from_traffic(self, visitors: int, position: int) -> float:
        """Estimate monthly revenue from traffic and SERP position"""
        # RPM typically €8-€25, lower positions get less traffic
        base_rpm = 15.0
        position_factor = max(0.1, 1.0 - (position - 1) * 0.1)
        revenue = (visitors / 1000) * base_rpm * position_factor
        return round(revenue, 2)

    def _classify_strength(self, position: int) -> str:
        """Classify competitive strength based on SERP position"""
        if position <= 3:
            return "High"
        elif position <= 7:
            return "Medium"
        else:
            return "Low"

    def _extract_domain_from_place(self, place_data: Dict) -> str:
        """Extract domain from place data"""
        # In real implementation, would check for website field
        return f"{place_data.get('name', 'unknown').lower().replace(' ', '-')}.example.com"

    def export_analysis_report(
        self, analysis: NicheAnalysisResult, output_path: str = "niche_analysis_report.txt"
    ) -> None:
        """Export detailed analysis report to text file"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write(f"NISCHEN-KONKURRENZANALYSE\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Ziel-Nische: {analysis.target_niche}\n")
            f.write(f"Standort: {analysis.target_location}\n\n")

            f.write(f"MARKTÜBERSICHT\n")
            f.write("-" * 70 + "\n")
            f.write(f"Anzahl Konkurrenten: {analysis.total_competitors_found}\n")
            f.write(f"Durchschn. Rating: {analysis.avg_competitor_rating}/5.0\n")
            f.write(f"Marktsättigung: {analysis.market_saturation}\n")
            f.write(
                f"Geschätzte monatl. Suchanfragen: {analysis.estimated_monthly_searches:,}\n\n"
            )

            f.write(f"UMSATZPOTENZIAL (Monatlich)\n")
            f.write("-" * 70 + "\n")
            f.write(
                f"Konservativ (RPM €8):  €{analysis.estimated_monthly_revenue[0]:,.2f}\n"
            )
            f.write(
                f"Realistisch (RPM €15): €{analysis.estimated_monthly_revenue[1]:,.2f}\n"
            )
            f.write(
                f"Optimistisch (RPM €25): €{analysis.estimated_monthly_revenue[2]:,.2f}\n\n"
            )

            f.write(f"OPPORTUNITY SCORE: {analysis.opportunity_score}/100\n\n")

            f.write(f"EMPFEHLUNGEN\n")
            f.write("-" * 70 + "\n")
            for rec in analysis.recommendations:
                f.write(f"{rec}\n")
            f.write("\n")

            f.write(f"TOP KONKURRENTEN\n")
            f.write("-" * 70 + "\n")
            for i, comp in enumerate(analysis.competitors[:10], 1):
                f.write(f"\n{i}. {comp.name}\n")
                f.write(f"   Rating: {comp.rating}/5.0 ({comp.review_count} Reviews)\n")
                f.write(f"   SERP Position: #{comp.estimated_serp_position}\n")
                f.write(
                    f"   Geschätzte Besucher/Monat: {comp.estimated_monthly_visitors:,}\n"
                )
                f.write(
                    f"   Geschätzter Umsatz/Monat: €{comp.estimated_monthly_revenue:,.2f}\n"
                )
                f.write(f"   Sichtbarkeit: {comp.visibility_score}/100\n")
                f.write(f"   Konkurrenzkraft: {comp.competitive_strength}\n")

        logger.info(f"✅ Report exported to {output_path}")


# Example usage and CLI interface
def main():
    """Example usage of NicheCompetitorAnalyzer"""
    print("=" * 70)
    print("NISCHEN-KONKURRENZANALYSE - ADS Pillar")
    print("=" * 70)

    # Example 1: Hundeparks in Berlin
    analyzer = NicheCompetitorAnalyzer()

    print("\n📊 Beispiel 1: Hundeparks in Berlin")
    print("-" * 70)
    result = analyzer.analyze_niche_competition(
        target_niche="Hundeparks",
        location="Berlin",
        radius_km=10.0,
        language="both",
    )

    print(f"\nZiel-Nische: {result.target_niche}")
    print(f"Standort: {result.target_location}")
    print(f"Konkurrenten gefunden: {result.total_competitors_found}")
    print(f"Marktsättigung: {result.market_saturation}")
    print(f"Opportunity Score: {result.opportunity_score}/100")
    print(
        f"Geschätzte monatl. Suchen: {result.estimated_monthly_searches:,}"
    )
    print(
        f"\nUmsatzpotenzial (monatlich):\n"
        f"  Min:  €{result.estimated_monthly_revenue[0]:,.2f}\n"
        f"  Avg:  €{result.estimated_monthly_revenue[1]:,.2f}\n"
        f"  Max:  €{result.estimated_monthly_revenue[2]:,.2f}"
    )

    print(f"\n📋 Empfehlungen:")
    for rec in result.recommendations:
        print(f"  • {rec}")

    print(f"\n🏆 Top 5 Konkurrenten:")
    for i, comp in enumerate(result.competitors[:5], 1):
        print(
            f"  {i}. {comp.name} - Rating: {comp.rating}/5.0, "
            f"Sichtbarkeit: {comp.visibility_score}/100"
        )

    # Export report
    analyzer.export_analysis_report(result, "niche_analysis_hundeparks_berlin.txt")

    print("\n" + "=" * 70)
    print("✅ Analyse abgeschlossen!")
    print("=" * 70)


if __name__ == "__main__":
    main()
