#!/usr/bin/env python3
"""
Integrierter Workflow: Nischen-Analyse + Scraping + Konkurrenz-Analyse
Kombiniert alle ADS Pillar Tools für vollständige Markt- und Datenanalyse
"""

import pandas as pd
import json
import sys
from pathlib import Path

# Import project modules
try:
    from competitor_analysis import NicheCompetitorAnalyzer, NicheAnalysisResult
    from enhanced_scrapers import UniversalScraper, GooglePlacesScraper
except ImportError:
    print("⚠️  Import error - make sure you're in the 'Files 2' directory")
    sys.exit(1)


class IntegratedNichePipeline:
    """
    Vollständiger Pipeline für Nischen-Analyse und Daten-Scraping

    Workflow:
    1. Nischen-Konkurrenzanalyse (bilingual DE/EN)
    2. Scraping von Locations (Google Places API)
    3. Anreicherung mit Features
    4. Export als CSV + Analyse-Report
    """

    def __init__(self, google_api_key: str = None):
        """
        Initialize pipeline

        Args:
            google_api_key: Google Places API key (optional)
        """
        self.google_api_key = google_api_key
        self.competitor_analyzer = NicheCompetitorAnalyzer(
            google_api_key=google_api_key
        )

    def run_complete_analysis(
        self,
        target_niche: str,
        location: str,
        output_dir: str = "output",
        language: str = "both",
        radius_km: float = 10.0,
    ) -> dict:
        """
        Führe vollständige Nischen-Analyse und Daten-Scraping aus

        Args:
            target_niche: Freitext-Nischenbeschreibung (z.B. "Hundeparks mit Agility-Parcours")
            location: Stadt/Region (z.B. "Berlin")
            output_dir: Ausgabe-Verzeichnis
            language: Suchsprache ("de", "en", "both")
            radius_km: Suchradius in km

        Returns:
            Dictionary mit allen Ergebnissen
        """
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        print("=" * 80)
        print(f"🚀 INTEGRIERTE NISCHEN-ANALYSE: {target_niche} in {location}")
        print("=" * 80)

        # Step 1: Competitor Analysis
        print(f"\n📊 Schritt 1: Konkurrenzanalyse...")
        print("-" * 80)
        competitor_analysis = self.competitor_analyzer.analyze_niche_competition(
            target_niche=target_niche,
            location=location,
            radius_km=radius_km,
            language=language,
        )

        self._print_competitor_summary(competitor_analysis)

        # Export competitor report
        report_path = f"{output_dir}/competitor_analysis_{location.lower().replace(' ', '_')}.txt"
        self.competitor_analyzer.export_analysis_report(
            competitor_analysis, report_path
        )
        print(f"\n✅ Konkurrenz-Report exportiert: {report_path}")

        # Step 2: Scrape Locations (if API key available)
        scraped_places = []
        if self.google_api_key:
            print(f"\n🔍 Schritt 2: Location-Scraping...")
            print("-" * 80)
            scraped_places = self._scrape_locations(target_niche, location)
            print(f"✅ {len(scraped_places)} Locations gescraped")
        else:
            print(f"\n⚠️  Schritt 2 übersprungen (kein Google API Key)")

        # Step 3: Combine data and export
        print(f"\n💾 Schritt 3: Daten-Export...")
        print("-" * 80)
        combined_data = self._combine_data(competitor_analysis, scraped_places)

        # Export as CSV
        csv_path = f"{output_dir}/niche_data_{location.lower().replace(' ', '_')}.csv"
        df = pd.DataFrame(combined_data)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"✅ CSV exportiert: {csv_path} ({len(combined_data)} Einträge)")

        # Export as JSON
        json_path = f"{output_dir}/niche_data_{location.lower().replace(' ', '_')}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON exportiert: {json_path}")

        # Step 4: Summary Report
        print(f"\n📈 ZUSAMMENFASSUNG")
        print("=" * 80)
        self._print_final_summary(competitor_analysis, len(scraped_places))

        return {
            "competitor_analysis": competitor_analysis,
            "scraped_places": scraped_places,
            "combined_data": combined_data,
            "files": {
                "competitor_report": report_path,
                "csv": csv_path,
                "json": json_path,
            },
        }

    def _scrape_locations(self, niche: str, location: str) -> list:
        """Scrape locations using Google Places API"""
        scraper = GooglePlacesScraper(api_key=self.google_api_key, delay=1.5)
        places = scraper.search_places(query=niche, location=location)

        # Enrich with details
        if places:
            print(f"   Anreicherung mit Details...")
            places = scraper.enrich_places(places[:20])  # Limit to 20 for API quota

        return places

    def _combine_data(
        self, competitor_analysis: NicheAnalysisResult, scraped_places: list
    ) -> list:
        """Combine competitor analysis and scraped data"""
        combined = []

        # Add competitor data
        for comp in competitor_analysis.competitors:
            combined.append(
                {
                    "source": "competitor_analysis",
                    "name": comp.name,
                    "rating": comp.rating,
                    "review_count": comp.review_count,
                    "estimated_monthly_visitors": comp.estimated_monthly_visitors,
                    "estimated_monthly_revenue": comp.estimated_monthly_revenue,
                    "visibility_score": comp.visibility_score,
                    "competitive_strength": comp.competitive_strength,
                    "serp_position": comp.estimated_serp_position,
                    "domain": comp.domain,
                }
            )

        # Add scraped places
        for place in scraped_places:
            combined.append(
                {
                    "source": "google_places",
                    "name": place.name,
                    "address": place.address,
                    "city": place.city,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                    "rating": place.rating,
                    "review_count": place.review_count,
                    "phone": place.phone,
                    "website": place.website,
                    "opening_hours": place.opening_hours,
                    "price_level": place.price_level,
                }
            )

        return combined

    def _print_competitor_summary(self, analysis: NicheAnalysisResult):
        """Print competitor analysis summary"""
        print(f"   Konkurrenten gefunden: {analysis.total_competitors_found}")
        print(f"   Marktsättigung: {analysis.market_saturation}")
        print(f"   Opportunity Score: {analysis.opportunity_score}/100")
        print(
            f"   Monatliche Suchen (geschätzt): {analysis.estimated_monthly_searches:,}"
        )
        print(f"\n   💰 Umsatzpotenzial (monatlich):")
        print(
            f"      Konservativ: €{analysis.estimated_monthly_revenue[0]:,.2f}"
        )
        print(
            f"      Realistisch:  €{analysis.estimated_monthly_revenue[1]:,.2f}"
        )
        print(
            f"      Optimistisch: €{analysis.estimated_monthly_revenue[2]:,.2f}"
        )

    def _print_final_summary(
        self, competitor_analysis: NicheAnalysisResult, scraped_count: int
    ):
        """Print final summary"""
        print(f"Nische: {competitor_analysis.target_niche}")
        print(f"Standort: {competitor_analysis.target_location}")
        print(f"Konkurrenten analysiert: {competitor_analysis.total_competitors_found}")
        print(f"Locations gescraped: {scraped_count}")
        print(f"Opportunity Score: {competitor_analysis.opportunity_score}/100")
        print(f"\n🎯 Empfehlungen:")
        for rec in competitor_analysis.recommendations:
            print(f"   • {rec}")


def interactive_mode():
    """Interactive CLI mode"""
    print("=" * 80)
    print("🎯 INTEGRIERTE NISCHEN-ANALYSE - ADS Pillar")
    print("=" * 80)

    # Get user input
    print("\n📋 Bitte geben Sie folgende Informationen ein:\n")

    target_niche = input(
        "Ziel-Nische (Freitext, DE/EN):\n"
        "Beispiele: 'Hundeparks', 'Coworking Cafés', 'Outdoor Spielplätze'\n"
        "> "
    ).strip()

    location = input(
        "\nStandort (Stadt/Region):\n"
        "Beispiele: 'Berlin', 'München', 'Hamburg'\n"
        "> "
    ).strip()

    language = input(
        "\nSuchsprache (de/en/both) [both]: "
    ).strip().lower() or "both"

    radius = input("\nSuchradius in km [10]: ").strip()
    radius_km = float(radius) if radius else 10.0

    api_key = input(
        "\nGoogle Places API Key (optional, Enter für Skip): "
    ).strip() or None

    output_dir = input("\nAusgabe-Verzeichnis [output]: ").strip() or "output"

    # Run analysis
    pipeline = IntegratedNichePipeline(google_api_key=api_key)

    try:
        result = pipeline.run_complete_analysis(
            target_niche=target_niche,
            location=location,
            output_dir=output_dir,
            language=language,
            radius_km=radius_km,
        )

        print(f"\n✨ Analyse erfolgreich abgeschlossen!")
        print(f"\n📂 Ausgabe-Dateien:")
        for file_type, file_path in result["files"].items():
            print(f"   • {file_type}: {file_path}")

    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback

        traceback.print_exc()


def example_usage():
    """Example with predefined parameters"""
    print("🔧 Running example analysis...\n")

    # Example: Hundeparks in Berlin
    pipeline = IntegratedNichePipeline()

    result = pipeline.run_complete_analysis(
        target_niche="Hundeparks mit Agility-Parcours",
        location="Berlin",
        output_dir="example_output",
        language="both",
        radius_km=10.0,
    )

    print(f"\n✨ Beispiel-Analyse abgeschlossen!")
    print(f"   Ergebnisse in: example_output/")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Integrierte Nischen-Analyse und Location-Scraping"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interaktiver Modus (fragt Nutzer-Eingaben ab)",
    )
    parser.add_argument(
        "--niche", "-n", type=str, help="Ziel-Nische (Freitext)"
    )
    parser.add_argument("--location", "-l", type=str, help="Stadt/Region")
    parser.add_argument(
        "--api-key", "-k", type=str, help="Google Places API Key"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="both",
        choices=["de", "en", "both"],
        help="Suchsprache",
    )
    parser.add_argument(
        "--radius", "-r", type=float, default=10.0, help="Suchradius in km"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output",
        help="Ausgabe-Verzeichnis",
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.niche and args.location:
        pipeline = IntegratedNichePipeline(google_api_key=args.api_key)
        result = pipeline.run_complete_analysis(
            target_niche=args.niche,
            location=args.location,
            output_dir=args.output,
            language=args.language,
            radius_km=args.radius,
        )
        print(f"\n✨ Analyse abgeschlossen! Ergebnisse in: {args.output}/")
    else:
        # Run example
        example_usage()
