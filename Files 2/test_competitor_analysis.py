#!/usr/bin/env python3
"""
Quick Test Script für Nischen-Konkurrenzanalyse
Demonstriert alle Features mit Beispiel-Daten
"""

from competitor_analysis import NicheCompetitorAnalyzer

def test_basic_analysis():
    """Test 1: Basis-Analyse ohne API Key"""
    print("=" * 80)
    print("TEST 1: Basis-Analyse (ohne API Key)")
    print("=" * 80)

    analyzer = NicheCompetitorAnalyzer()

    result = analyzer.analyze_niche_competition(
        target_niche="Hundeparks mit Agility-Parcours",
        location="Berlin",
        radius_km=10.0,
        language="both"
    )

    print(f"\n✅ Analyse abgeschlossen!")
    print(f"   Nische: {result.target_niche}")
    print(f"   Standort: {result.target_location}")
    print(f"   Konkurrenten: {result.total_competitors_found}")
    print(f"   Marktsättigung: {result.market_saturation}")
    print(f"   Opportunity Score: {result.opportunity_score}/100")
    print(f"   Monatliche Suchen (geschätzt): {result.estimated_monthly_searches:,}")

    print(f"\n💰 Umsatzpotenzial (monatlich):")
    print(f"   Konservativ: €{result.estimated_monthly_revenue[0]:,.2f}")
    print(f"   Realistisch:  €{result.estimated_monthly_revenue[1]:,.2f}")
    print(f"   Optimistisch: €{result.estimated_monthly_revenue[2]:,.2f}")

    print(f"\n📊 Top 5 Konkurrenten:")
    for i, comp in enumerate(result.competitors[:5], 1):
        print(f"   {i}. {comp.name}")
        print(f"      Rating: {comp.rating}/5.0 ({comp.review_count} Reviews)")
        print(f"      Sichtbarkeit: {comp.visibility_score}/100")
        print(f"      Monatl. Umsatz: €{comp.estimated_monthly_revenue:,.2f}")

    print(f"\n🎯 Empfehlungen:")
    for rec in result.recommendations:
        print(f"   • {rec}")

    # Export report
    analyzer.export_analysis_report(result, "test_report_hundeparks_berlin.txt")
    print(f"\n✅ Report exportiert: test_report_hundeparks_berlin.txt")

    return result


def test_multiple_niches():
    """Test 2: Vergleich mehrerer Nischen"""
    print("\n\n" + "=" * 80)
    print("TEST 2: Vergleich mehrerer Nischen")
    print("=" * 80)

    analyzer = NicheCompetitorAnalyzer()

    niches = [
        ("Hundeparks", "Berlin"),
        ("Coworking Cafés", "München"),
        ("Outdoor Spielplätze", "Hamburg"),
        ("Fotospots", "Dresden"),
    ]

    results = []
    for niche, location in niches:
        result = analyzer.analyze_niche_competition(
            target_niche=niche,
            location=location,
            radius_km=10.0,
            language="both"
        )
        results.append((niche, location, result))

    # Sort by opportunity score
    results.sort(key=lambda x: x[2].opportunity_score, reverse=True)

    print(f"\n🏆 Nischen-Ranking (nach Opportunity Score):\n")
    for i, (niche, location, result) in enumerate(results, 1):
        print(f"{i}. {niche} in {location}")
        print(f"   Opportunity Score: {result.opportunity_score}/100")
        print(f"   Konkurrenten: {result.total_competitors_found}")
        print(f"   Marktsättigung: {result.market_saturation}")
        print(f"   Umsatz (realistisch): €{result.estimated_monthly_revenue[1]:,.2f}/Monat")
        print()

    print(f"🎯 Empfehlung: Fokus auf #{1} - {results[0][0]} in {results[0][1]}")


def test_bilingual_search():
    """Test 3: Bilinguale Suche (DE + EN)"""
    print("\n\n" + "=" * 80)
    print("TEST 3: Bilinguale Suche (Deutsch + Englisch)")
    print("=" * 80)

    analyzer = NicheCompetitorAnalyzer()

    # Generate keywords
    keywords_both = analyzer._generate_search_keywords(
        "Dog parks", "Berlin", language="both"
    )
    keywords_de = analyzer._generate_search_keywords(
        "Hundeparks", "Berlin", language="de"
    )
    keywords_en = analyzer._generate_search_keywords(
        "Dog parks", "Berlin", language="en"
    )

    print(f"\n📝 Generierte Keywords:")
    print(f"   Both (DE+EN): {len(keywords_both)} Keywords")
    print(f"   Nur Deutsch:  {len(keywords_de)} Keywords")
    print(f"   Nur Englisch: {len(keywords_en)} Keywords")

    print(f"\n🔍 Beispiel-Keywords (both):")
    for kw in keywords_both[:8]:
        print(f"   • {kw}")


def test_export_formats():
    """Test 4: Export in verschiedenen Formaten"""
    print("\n\n" + "=" * 80)
    print("TEST 4: Export-Formate testen")
    print("=" * 80)

    analyzer = NicheCompetitorAnalyzer()

    result = analyzer.analyze_niche_competition(
        target_niche="Sauna & Kaltwasser",
        location="München",
        radius_km=15.0,
        language="de"
    )

    # Export text report
    analyzer.export_analysis_report(result, "test_export_sauna_muenchen.txt")
    print(f"✅ Text-Report exportiert: test_export_sauna_muenchen.txt")

    # Export as JSON (manual)
    import json
    json_data = {
        "target_niche": result.target_niche,
        "target_location": result.target_location,
        "total_competitors": result.total_competitors_found,
        "opportunity_score": result.opportunity_score,
        "market_saturation": result.market_saturation,
        "estimated_monthly_searches": result.estimated_monthly_searches,
        "revenue_estimates": {
            "conservative": result.estimated_monthly_revenue[0],
            "realistic": result.estimated_monthly_revenue[1],
            "optimistic": result.estimated_monthly_revenue[2],
        },
        "top_competitors": [
            {
                "name": comp.name,
                "rating": comp.rating,
                "review_count": comp.review_count,
                "visibility_score": comp.visibility_score,
                "estimated_revenue": comp.estimated_monthly_revenue,
            }
            for comp in result.competitors[:10]
        ],
    }

    with open("test_export_sauna_muenchen.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON exportiert: test_export_sauna_muenchen.json")

    # Export as CSV (manual)
    import csv
    with open("test_export_sauna_muenchen.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "rating", "review_count", "visibility_score",
            "estimated_monthly_visitors", "estimated_monthly_revenue",
            "competitive_strength", "serp_position"
        ])
        writer.writeheader()
        for comp in result.competitors:
            writer.writerow({
                "name": comp.name,
                "rating": comp.rating,
                "review_count": comp.review_count,
                "visibility_score": comp.visibility_score,
                "estimated_monthly_visitors": comp.estimated_monthly_visitors,
                "estimated_monthly_revenue": comp.estimated_monthly_revenue,
                "competitive_strength": comp.competitive_strength,
                "serp_position": comp.estimated_serp_position,
            })

    print(f"✅ CSV exportiert: test_export_sauna_muenchen.csv")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "NISCHEN-KONKURRENZANALYSE - TEST SUITE" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")

    # Run all tests
    test_basic_analysis()
    test_multiple_niches()
    test_bilingual_search()
    test_export_formats()

    print("\n\n" + "=" * 80)
    print("✅ ALLE TESTS ABGESCHLOSSEN!")
    print("=" * 80)
    print("\nGenerierte Dateien:")
    print("   • test_report_hundeparks_berlin.txt")
    print("   • test_export_sauna_muenchen.txt")
    print("   • test_export_sauna_muenchen.json")
    print("   • test_export_sauna_muenchen.csv")
    print("\n🎯 Nächste Schritte:")
    print("   1. Prüfe die generierten Reports")
    print("   2. Teste mit eigenem Google API Key")
    print("   3. Nutze niche_scraper_workflow.py für vollständigen Workflow")
    print("\n")


if __name__ == "__main__":
    main()
