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
    category = input(
        "📍 Welche Kategorie? (z.B. Parks, Cafés, Spielplätze): "
    ).strip() or "Parks"
    domain = input(
        "🌐 Deine Domain? (z.B. meine-stadt.de): "
    ).strip() or "meine-website.de"
    
    print()
    print("🔧 Optional - für erweiterte Funktionen:")
    google_api_key = input(
        "🗺️  Google Places API Key (Enter = überspringen): "
    ).strip()
    adsense_id = input("💰 AdSense Publisher ID (Enter = später): ").strip()
    
    # Wähle automatisch passende Nische
    niche_suggestions = {
        'parks': {
            'facets': [
                'shade', 'benches', 'water', 'parking',
                'toilets', 'wheelchair', 'kids', 'dogs'
            ],
            'keywords': ['park', 'grünanlage', 'erholung', 'outdoor'],
            'rpm_estimate': '8-15'
        },
        'cafés': {
            'facets': [
                'wifi', 'power_outlets', 'quiet', 'workspace', 'parking'
            ],
            'keywords': ['café', 'kaffee', 'arbeitsplatz', 'wifi'],
            'rpm_estimate': '12-20'
        },
        'spielplätze': {
            'facets': ['age_group', 'shade', 'parking', 'toilets', 'fence'],
            'keywords': ['spielplatz', 'kinder', 'familie', 'outdoor'],
            'rpm_estimate': '10-18'
        }
    }
    
    # Erkenne Nische automatisch
    category_lower = category.lower()
    selected_niche = None
    for niche_key in niche_suggestions:
        if (niche_key in category_lower or
                any(keyword in category_lower
                    for keyword in niche_suggestions[niche_key]['keywords'])):
            selected_niche = niche_suggestions[niche_key]
            break
    
    if not selected_niche:
        selected_niche = niche_suggestions['parks']  # Default
    
    print()
    print("✨ Erkannte Nische-Eigenschaften:")
    print(f"   📊 Geschätzter RPM: €{selected_niche['rpm_estimate']}")
    print(f"   🏷️  Facetten: {', '.join(selected_niche['facets'][:5])}")
    print()
    
    # Erstelle Projekt-Konfiguration
    config = {
        'project_name': f"{category} in {city}",
        'city': city,
        'category': category,
        'domain': domain,
        'google_api_key': google_api_key,
        'adsense_id': adsense_id or "ca-pub-XXXXXXXXXXXXXXXX",
        'niche_config': selected_niche
    }
    
    # Speichere Konfiguration
    with open('quick_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("💾 Konfiguration gespeichert!")
    print()
    
    return config


def create_sample_data(config):
    """Erstelle Beispieldaten für die gewählte Nische"""
    
    city = config['city']
    category = config['category']
    
    # Beispieldaten je nach Kategorie
    if 'park' in category.lower():
        sample_places = [
            {
                'name': f'Stadtpark {city}',
                'address': f'Parkstraße 1, {city}',
                'city': city,
                'latitude': 52.5200,
                'longitude': 13.4050,
                'rating': 4.2,
                'review_count': 156,
                'feature_shade': True,
                'feature_benches': True,
                'feature_water': True,
                'feature_parking': False,
                'feature_toilets': True,
                'feature_wheelchair': True,
                'feature_kids': True,
                'feature_dogs': True,
                'feature_fee': False
            },
            {
                'name': f'Volkspark {city}',
                'address': f'Volksstraße 15, {city}',
                'city': city,
                'latitude': 52.5300,
                'longitude': 13.4150,
                'rating': 4.0,
                'review_count': 89,
                'feature_shade': True,
                'feature_benches': True,
                'feature_water': False,
                'feature_parking': True,
                'feature_toilets': False,
                'feature_wheelchair': False,
                'feature_kids': True,
                'feature_dogs': True,
                'feature_fee': False
            }
        ]
    elif 'café' in category.lower():
        sample_places = [
            {
                'name': f'Café Central {city}',
                'address': f'Hauptstraße 10, {city}',
                'city': city,
                'latitude': 52.5200,
                'longitude': 13.4050,
                'rating': 4.5,
                'review_count': 234,
                'feature_wifi': True,
                'feature_power_outlets': True,
                'feature_quiet': False,
                'feature_workspace': True,
                'feature_parking': True,
                'feature_wheelchair': True,
                'feature_fee': True
            }
        ]
    else:
        # Generic sample
        sample_places = [
            {
                'name': f'{category} Beispiel',
                'address': f'Musterstraße 1, {city}',
                'city': city,
                'latitude': 52.5200,
                'longitude': 13.4050,
                'rating': 4.0,
                'review_count': 100
            }
        ]
    
    # Speichere als CSV
    import pandas as pd
    df = pd.DataFrame(sample_places)
    
    os.makedirs('data', exist_ok=True)
    filename = f"data/{city.lower()}_{category.lower()}_sample.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Beispieldaten erstellt: {filename}")
    return filename


def generate_quick_page(config, _unused_data_file=None):
    """Generiere eine einfache Demo-Seite"""
    
    city = config['city']
    category = config['category']
    domain = config['domain']
    
    # Einfaches HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{category} in {city} | Lokaler Guide</title>
    <meta name="description" content="Finde die besten {category} in {city}. Kuratierte Auswahl mit Bewertungen und Details.">
    <style>
        body {{ font-family: system-ui, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        .subtitle {{ color: #666; margin-bottom: 30px; }}
        .place {{ border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
        .place h3 {{ margin-top: 0; color: #2c5aa0; }}
        .rating {{ color: #f39c12; font-weight: bold; }}
        .features {{ margin-top: 10px; }}
        .feature {{ display: inline-block; background: #e8f4fd; color: #2c5aa0; padding: 4px 8px; border-radius: 4px; margin: 2px; font-size: 12px; }}
        .header-stats {{ background: #f8f9fa; padding: 15px; border-radius: 6px; margin: 20px 0; }}
        .cta {{ background: #2c5aa0; color: white; padding: 15px; text-align: center; border-radius: 6px; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 40px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{category} in {city}</h1>
            <p class="subtitle">Kuratierte Auswahl der besten {category} mit Bewertungen und Ausstattungsmerkmalen</p>
            
            <div class="header-stats">
                <strong>📊 Aktuelle Statistiken:</strong><br>
                📍 2 Orte gelistet | ⭐ Durchschnitt: 4.1/5 | 📝 245 Bewertungen
            </div>
            
            <div class="cta">
                🚀 <strong>Demo-Version</strong> - Zeigt Beispieldaten für "{category}" in {city}
            </div>
        </header>
        
        <main>
            <div class="place">
                <h3>🌳 Stadtpark {city}</h3>
                <p><strong>📍 Adresse:</strong> Parkstraße 1, {city}</p>
                <p><strong class="rating">⭐ 4.2/5</strong> (156 Bewertungen)</p>
                <div class="features">
                    <span class="feature">🌳 Schatten</span>
                    <span class="feature">🪑 Sitzbänke</span>
                    <span class="feature">💧 Wasser</span>
                    <span class="feature">🚻 Toiletten</span>
                    <span class="feature">♿ Barrierefrei</span>
                    <span class="feature">👶 Kinderfreundlich</span>
                    <span class="feature">🐕 Hunde erlaubt</span>
                    <span class="feature">💰 Kostenfrei</span>
                </div>
            </div>
            
            <div class="place">
                <h3>🌲 Volkspark {city}</h3>
                <p><strong>📍 Adresse:</strong> Volksstraße 15, {city}</p>
                <p><strong class="rating">⭐ 4.0/5</strong> (89 Bewertungen)</p>
                <div class="features">
                    <span class="feature">🌳 Schatten</span>
                    <span class="feature">🪑 Sitzbänke</span>
                    <span class="feature">🚗 Parkplatz</span>
                    <span class="feature">👶 Kinderfreundlich</span>
                    <span class="feature">🐕 Hunde erlaubt</span>
                    <span class="feature">💰 Kostenfrei</span>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            <p><strong>💡 Das ist eine Demo-Seite</strong></p>
            <p>Echte Daten können über Google Places API oder CSV-Upload hinzugefügt werden.</p>
            <p>Mit AdSense-Integration geschätzter Umsatz: <strong>€50-200/Monat</strong> bei 10-50K Pageviews</p>
            <hr>
            <p>Erstellt mit ADS Pillar System | Domain: {domain}</p>
        </footer>
    </div>
</body>
</html>"""
    
    # Speichere HTML
    os.makedirs('generated', exist_ok=True)
    output_file = f"generated/{city.lower()}_{category.lower()}_demo.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Demo-Seite erstellt: {output_file}")
    return output_file

def show_next_steps(config, html_file):
    """Zeige die nächsten Schritte"""
    
    print()
    print("🎉 Dein ADS Pillar Demo ist bereit!")
    print("=" * 40)
    print()
    print("📁 Generierte Dateien:")
    print(f"   • {html_file} - Demo-Website")
    print("   • quick_config.json - Projekt-Konfiguration")
    print(f"   • data/{config['city'].lower()}_{config['category'].lower()}_sample.csv - Beispieldaten")
    print()
    
    print("👀 Demo ansehen:")
    print(f"   open {html_file}")
    print()
    
    print("🚀 Nächste Schritte für ECHTES Projekt:")
    print()
    print("1️⃣  ECHTE DATEN sammeln:")
    if config.get('google_api_key'):
        print("   ✅ Google API Key vorhanden - führe aus:")
        print("   python3 enhanced_scrapers.py")
    else:
        print("   📝 Google Places API Key besorgen (kostenlos):")
        print("   https://console.cloud.google.com/")
        print("   Oder CSV mit echten Orten erstellen")
    print()
    
    print("2️⃣  ADSENSE einrichten:")
    if config.get('adsense_id') and 'XXXX' not in config['adsense_id']:
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
    niche_config = config.get('niche_config', {})
    rpm_estimate = niche_config.get('rpm_estimate', '10-15')
    print(f"   📊 Geschätzter RPM: €{rpm_estimate}")
    print(f"   📈 Bei 25K Pageviews/Monat: €{int(rpm_estimate.split('-')[0]) * 25}€ - €{int(rpm_estimate.split('-')[1]) * 25}€")
    print(f"   📈 Bei 50K Pageviews/Monat: €{int(rpm_estimate.split('-')[0]) * 50}€ - €{int(rpm_estimate.split('-')[1]) * 50}€")
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
