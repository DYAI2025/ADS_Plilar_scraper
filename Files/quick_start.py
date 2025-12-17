#!/usr/bin/env python3
"""
ADS Pillar - Simple Starter
Ein-Klick-Lösung für dein erstes ADS Pillar Projekt
"""

import os
import sys
import json


def simple_setup():
    """Einfacher interaktiver Setup"""

    print("🚀 ADS Pillar - Einfacher Start")
    print("=" * 40)
    print()

    # Sammle grundlegende Informationen
    print("📋 Lass uns dein erstes Projekt konfigurieren:")
    print()

    city = input("🏙️  In welcher Stadt? (z.B. Berlin): ").strip() or "Berlin"
    category = (
        input("📍 Welche Kategorie? (z.B. Parks, Cafés, Spielplätze): ").strip()
        or "Parks"
    )
    domain = (
        input("🌐 Deine Domain? (z.B. meine-stadt.de): ").strip() or "meine-website.de"
    )

    print()
    print("🔧 Optional - für erweiterte Funktionen:")
    google_api_key = input("🗺️  Google Places API Key (Enter = überspringen): ").strip()
    adsense_id = input("💰 AdSense Publisher ID (Enter = später): ").strip()

    # Wähle automatisch passende Nische
    niche_suggestions = {
        "parks": {
            "facets": [
                "shade",
                "benches",
                "water",
                "parking",
                "toilets",
                "wheelchair",
                "kids",
                "dogs",
            ],
            "keywords": ["park", "grünanlage", "erholung", "outdoor"],
            "rpm_estimate": "8-15",
        },
        "cafés": {
            "facets": ["wifi", "power_outlets", "quiet", "workspace", "parking"],
            "keywords": ["café", "kaffee", "arbeitsplatz", "wifi"],
            "rpm_estimate": "12-20",
        },
        "spielplätze": {
            "facets": ["age_group", "shade", "parking", "toilets", "fence"],
            "keywords": ["spielplatz", "kinder", "familie", "outdoor"],
            "rpm_estimate": "10-18",
        },
    }

    # Erkenne Nische automatisch
    category_lower = category.lower()
    selected_niche = None
    for niche_key in niche_suggestions:
        if niche_key in category_lower or any(
            keyword in category_lower
            for keyword in niche_suggestions[niche_key]["keywords"]
        ):
            selected_niche = niche_suggestions[niche_key]
            break

    if not selected_niche:
        selected_niche = niche_suggestions["parks"]  # Default

    print()
    print("✨ Erkannte Nische-Eigenschaften:")
    print(f"   📊 Geschätzter RPM: €{selected_niche['rpm_estimate']}")
    print(f"   🏷️  Facetten: {', '.join(selected_niche['facets'][:5])}")
    print()

    # Erstelle Projekt-Konfiguration
    config = {
        "project_name": f"{category} in {city}",
        "city": city,
        "category": category,
        "domain": domain,
        "google_api_key": google_api_key,
        "adsense_id": adsense_id or "ca-pub-XXXXXXXXXXXXXXXX",
        "niche_config": selected_niche,
    }

    # Speichere Konfiguration
    with open("quick_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("💾 Konfiguration gespeichert!")
    print()

    return config


def create_sample_data(config):
    """
    ⚠️ WARNUNG: KEINE FAKE-DATEN MEHR!

    Diese Funktion zeigt eine Anleitung, wie echte Daten gesammelt werden.
    Fake/Placeholder-Daten werden NICHT mehr erstellt.

    Um echte Daten zu sammeln, verwenden Sie:
    1. Google Places API (empfohlen)
    2. CSV-Import von echten Quellen
    3. Manual curation
    """

    city = config["city"]
    category = config["category"]

    print("\n" + "=" * 60)
    print("⚠️  KEINE FAKE-DATEN: Echte Daten erforderlich!")
    print("=" * 60)
    print()
    print("📋 Um echte Daten zu sammeln, haben Sie folgende Optionen:")
    print()
    print("1️⃣  Google Places API (Empfohlen):")
    print("   python Files/enhanced_scrapers.py --query '{category}' --location '{city}'")
    print("   Benötigt: GOOGLE_PLACES_API_KEY")
    print()
    print("2️⃣  CSV-Import:")
    print("   Erstellen Sie eine CSV mit echten Daten:")
    print("   - name, address, city, latitude, longitude, rating, review_count")
    print("   - Speichern als: data/{city.lower()}_{category.lower()}.csv")
    print()
    print("3️⃣  GUI verwenden:")
    print("   python Files/gui_app.py")
    print("   → Tab 'Daten sammeln' → API Key eingeben → Scrapen")
    print()
    print("❌ Fake/Placeholder-Daten werden NICHT mehr generiert!")
    print()

    # Erstelle leere CSV mit korrekter Struktur als Template
    import pandas as pd

    template_data = {
        'name': ['[BITTE ECHTE DATEN HINZUFÜGEN]'],
        'address': ['[ERSETZEN SIE DIES]'],
        'city': [city],
        'latitude': [0.0],
        'longitude': [0.0],
        'rating': [0.0],
        'review_count': [0],
        'phone': [''],
        'website': [''],
        'opening_hours': [''],
        'feature_shade': [False],
        'feature_benches': [False],
        'feature_water': [False],
        'feature_parking': [False],
        'feature_toilets': [False],
        'feature_wheelchair_accessible': [False],
        'feature_kids_friendly': [False],
        'feature_dogs_allowed': [False],
        'feature_fee': [False],
    }

    df = pd.DataFrame(template_data)

    os.makedirs("data", exist_ok=True)
    filename = f"data/{city.lower()}_{category.lower()}_TEMPLATE.csv"
    df.to_csv(filename, index=False)

    print(f"✅ CSV-Template erstellt: {filename}")
    print(f"   → Öffnen Sie diese Datei und fügen Sie ECHTE Daten hinzu!")
    print()

    return None  # Kein valider Dateiname, da nur Template


def generate_quick_page(config, data_file=None):
    """
    Generiere Seite mit echten Daten - KEINE Platzhalter mehr!

    Diese Funktion verwendet jetzt die echte PillarPageGenerator Klasse.
    """

    city = config["city"]
    category = config["category"]
    domain = config["domain"]

    print("\n" + "=" * 60)
    print("📄 Seiten-Generierung")
    print("=" * 60)
    print()

    # Prüfe ob Datendatei existiert
    if not data_file or not os.path.exists(data_file):
        print("❌ Keine gültige Datendatei vorhanden!")
        print()
        print("💡 Um eine Seite zu generieren, benötigen Sie ECHTE Daten:")
        print("   1. Sammeln Sie Daten via Google Places API")
        print("   2. Oder erstellen Sie eine CSV mit echten Orten")
        print("   3. Dann rufen Sie erneut generate_quick_page(config, 'data.csv') auf")
        print()
        print("❌ KEINE Platzhalter-Seiten werden mehr erstellt!")
        print()
        return None

    # Verwende echte PillarPageGenerator
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from data_pipeline import PillarPageGenerator, LocationData
        import pandas as pd

        # Lade echte Daten
        df = pd.read_csv(data_file)

        # Validiere dass es echte Daten sind
        if len(df) == 0:
            print("❌ CSV-Datei ist leer!")
            return None

        # Prüfe auf Platzhalter
        if df['name'].str.contains('BITTE ECHTE DATEN|ERSETZEN SIE', case=False).any():
            print("❌ CSV enthält noch Platzhalter!")
            print("   Bitte ersetzen Sie die Template-Einträge mit echten Daten.")
            return None

        # Konvertiere zu LocationData
        locations = []
        for _, row in df.iterrows():
            loc = LocationData(
                id=row.get('id', str(row.name)),
                name=row['name'],
                street=row.get('address', row.get('street', '')),
                city=row['city'],
                region=row.get('region', ''),
                country=row.get('country', 'Deutschland'),
                postcode=row.get('postcode', ''),
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                url=row.get('website', row.get('url', '')),
                phone=row.get('phone', ''),
                email=row.get('email', ''),
                opening_hours=row.get('opening_hours', ''),
                rating=float(row.get('rating', 0.0)),
                review_count=int(row.get('review_count', 0)),
            )
            locations.append(loc)

        # Generiere mit echtem Generator
        template_path = os.path.join(os.path.dirname(__file__), 'pillar_page_skeleton.html')
        page_config = {
            'site_name': f"{category} in {city}",
            'adsense_id': config.get('adsense_id', ''),
            'ga_id': config.get('ga_id', ''),
        }
        generator = PillarPageGenerator(template_path=template_path, config=page_config)

        os.makedirs("generated", exist_ok=True)
        output_file = f"generated/{city.lower()}_{category.lower()}.html"

        generator.generate_page(
            data=locations,
            city=city,
            category=category,
            output_path=output_file,
            canonical_url=f"https://{domain}/{city.lower()}-{category.lower()}"
        )

        print(f"✅ Echte Seite generiert: {output_file}")
        print(f"   → {len(locations)} echte Orte verarbeitet")
        return output_file

    except Exception as e:
        print(f"❌ Fehler bei Seiten-Generierung: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def show_next_steps(config, html_file):
    """Zeige die nächsten Schritte"""

    print()
    print("🎉 Dein ADS Pillar Demo ist bereit!")
    print("=" * 40)
    print()
    print("📁 Generierte Dateien:")
    print(f"   • {html_file} - Demo-Website")
    print("   • quick_config.json - Projekt-Konfiguration")
    print(
        f"   • data/{config['city'].lower()}_{config['category'].lower()}_sample.csv - Beispieldaten"
    )
    print()

    print("👀 Demo ansehen:")
    print(f"   open {html_file}")
    print()

    print("🚀 Nächste Schritte für ECHTES Projekt:")
    print()
    print("1️⃣  ECHTE DATEN sammeln:")
    if config.get("google_api_key"):
        print("   ✅ Google API Key vorhanden - führe aus:")
        print("   python3 enhanced_scrapers.py")
    else:
        print("   📝 Google Places API Key besorgen (kostenlos):")
        print("   https://console.cloud.google.com/")
        print("   Oder CSV mit echten Orten erstellen")
    print()

    print("2️⃣  ADSENSE einrichten:")
    if config.get("adsense_id") and "XXXX" not in config["adsense_id"]:
        print("   ✅ AdSense ID vorhanden")
    else:
        print("   💰 AdSense Konto erstellen:")
        print("   https://www.google.com/adsense/")
    print()

    print("3️⃣  WEBSITE live schalten:")
    print("   🌐 Domain/Hosting besorgen")
    print("   📤 HTML-Dateien hochladen")
    print("   🔍 Google Search Console konfigurieren")
    print()

    print("4️⃣  ERWEITERTE FEATURES nutzen:")
    print("   🖥️  GUI starten: python3 gui_app.py")
    print("   🔧 Vollsetup: ./run_setup.sh")
    print("   📊 Nischen-Analyse: python3 niche_research.py")
    print()

    print("💰 REVENUE-POTENZIAL für dein Projekt:")
    niche_config = config.get("niche_config", {})
    rpm_estimate = niche_config.get("rpm_estimate", "10-15")
    print(f"   📊 Geschätzter RPM: €{rpm_estimate}")
    print(
        f"   📈 Bei 25K Pageviews/Monat: €{int(rpm_estimate.split('-')[0]) * 25}€ - €{int(rpm_estimate.split('-')[1]) * 25}€"
    )
    print(
        f"   📈 Bei 50K Pageviews/Monat: €{int(rpm_estimate.split('-')[0]) * 50}€ - €{int(rpm_estimate.split('-')[1]) * 50}€"
    )
    print()

    print("❓ HILFE & SUPPORT:")
    print("   📖 README.md lesen")
    print("   ✅ adsense_policy_checklist.md beachten")
    print("   🚀 launch_checklist.md für Go-Live")


def main():
    """Hauptfunktion für einfachen Start"""

    try:
        # Setup
        config = simple_setup()

        # Erstelle Beispieldaten
        data_file = create_sample_data(config)

        # Generiere Demo-Seite
        html_file = generate_quick_page(config, data_file)

        # Zeige nächste Schritte
        show_next_steps(config, html_file)

        # Öffne Demo automatisch (wenn möglich)
        try:
            import webbrowser

            print("🌐 Öffne Demo im Browser...")
            webbrowser.open(f"file://{os.path.abspath(html_file)}")
        except Exception:
            pass

        print()
        print("✨ Happy Building! 🚀")

    except KeyboardInterrupt:
        print("\n\n👋 Setup abgebrochen. Bis später!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        print("\n🔧 Versuche stattdessen:")
        print("   python3 gui_app.py    # GUI-Version")
        print("   ./run_setup.sh        # Vollständiges Setup")
        sys.exit(1)


if __name__ == "__main__":
    main()
