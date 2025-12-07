#!/usr/bin/env python3
"""
Generate AI-SEO optimized Babelsberg site
Optimized for ChatGPT, Perplexity, Claude, and other AI search engines
"""

import csv
import html
import json
from datetime import datetime
from pathlib import Path

# Configuration - AI SEO optimized
config = {
    "site_name": "Park Babelsberg & Schloss Potsdam",
    "domain": "https://babelsberger.info",
    "city": "Potsdam",
    "category": "Parks & Attraktionen",
    "adsense_id": "pub-1712273263687132",
    "ga_id": "G-K409QD2YSJ",
    "year": "2025",
    "last_updated": datetime.now().strftime("%Y-%m-%d")
}

def load_locations(csv_path):
    """Load location data from CSV"""
    locations = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            locations.append(row)
    return locations


def generate_faq_schema(locations):
    """Generate FAQ Schema for AI crawlers"""
    faq_items = [
        {
            "question": "Welche Attraktionen gibt es im Park Babelsberg?",
            "answer": f"Der Park Babelsberg bietet {len(locations)} Hauptattraktionen: Schloss Babelsberg (UNESCO Welterbe), Flatowturm (Aussichtsturm), Matrosenhaus, Gerichtslaube und mehrere Liegewiesen am Wasser. Alle Orte sind mit GPS-Koordinaten und detaillierten Informationen zu Barrierefreiheit, Toiletten und Kinderfreundlichkeit dokumentiert."
        },
        {
            "question": "Gibt es Toiletten im Park Babelsberg?",
            "answer": "Ja, Toiletten befinden sich vor dem Schloss Babelsberg und beim Spielplatz. Nutzen Sie unseren Filter 'Toiletten' um alle Orte mit WC-Zugang zu finden."
        },
        {
            "question": "Ist der Park Babelsberg barrierefrei?",
            "answer": "Der Uferweg Nord am Tiefen See ist weitgehend barrierefrei mit festem Belag. Viele Hauptwege sind für Rollstuhlfahrer geeignet. Nutzen Sie unseren 'Barrierefrei'-Filter für spezifische Locations."
        },
        {
            "question": "Sind Hunde im Park Babelsberg erlaubt?",
            "answer": "Ja, Hunde sind erlaubt, müssen aber an der Leine geführt werden. Bitte Hundekotbeutel mitführen und die Parkordnung beachten."
        },
        {
            "question": "Gibt es Parkplätze am Park Babelsberg?",
            "answer": "Ja, der Hauptparkplatz befindet sich an der Albert-Einstein-Straße (kostenpflichtig). Von dort sind es ca. 5-10 Minuten Fußweg zum Schloss und den Hauptattraktionen."
        },
        {
            "question": "Ist der Park Babelsberg kinderfreundlich?",
            "answer": "Sehr! Es gibt einen gut ausgestatteten Spielplatz mit modernen Geräten, weitläufige Liegewiesen zum Toben und schattige Picknickbereiche. Nutzen Sie unseren 'Kinderfreundlich'-Filter."
        },
        {
            "question": "Wo kann man im Park Babelsberg fotografieren?",
            "answer": "Top Fotospots: Schloss Babelsberg (beste Zeit: Abendlicht), Flatowturm (Panorama), Zypressen-Allee, Uferweg mit Blick über den Tiefen See und die Steintreppe am Wasser. Nutzen Sie unseren 'Fotografie'-Filter."
        },
        {
            "question": "Was kostet der Eintritt in den Park Babelsberg?",
            "answer": "Der Park ist frei zugänglich (kostenfrei). Nur das Schloss-Innere kostet Eintritt. Parkgebühren fallen am Parkplatz an."
        }
    ]

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"]
                }
            }
            for item in faq_items
        ]
    }


def generate_breadcrumb_schema():
    """Generate BreadcrumbList for AI understanding"""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Potsdam",
                "item": "https://babelsberger.info"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Parks & Schlösser",
                "item": "https://babelsberger.info"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": "Park Babelsberg",
                "item": "https://babelsberger.info"
            }
        ]
    }


def generate_organization_schema():
    """Generate Organization schema for brand recognition"""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Babelsberger.info",
        "url": "https://babelsberger.info",
        "description": "Ihr Guide für Park Babelsberg, Schloss Babelsberg und Neuer Schlossgarten in Potsdam. Detaillierte Informationen zu Attraktionen, Barrierefreiheit, Kinderfreundlichkeit und mehr.",
        "sameAs": []
    }


def convert_bool(value):
    """Convert CSV boolean to Python boolean"""
    if not value or value == '':
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.upper() == 'TRUE'
    return bool(value)


def prepare_location_data(locations):
    """Prepare locations for JavaScript with AI-friendly structure"""
    js_data = []
    for loc in locations:
        def sanitize(value):
            if value is None:
                return ""
            return html.escape(str(value))

        item = {
            "name": sanitize(loc['name']),
            "address": sanitize(loc.get('address', '')),
            "city": sanitize(loc['city']),
            "rating": float(loc['rating']) if loc.get('rating') else 0,
            "review_count": int(loc.get('review_count', 0)),
            "description": sanitize(loc.get('description_de', '')),
            "tags": sanitize(loc.get('tags', '')),
            "image": sanitize(loc.get('main_image', '')),
            "opening_hours": sanitize(loc.get('opening_hours', '')),
            "website": sanitize(loc.get('website', '')),
            "latitude": float(loc['latitude']),
            "longitude": float(loc['longitude']),
            "feature_shade": convert_bool(loc.get('feature_shade')),
            "feature_water": convert_bool(loc.get('feature_water')),
            "feature_benches": convert_bool(loc.get('feature_benches')),
            "feature_parking": convert_bool(loc.get('feature_parking')),
            "feature_toilets": convert_bool(loc.get('feature_toilets')),
            "feature_wheelchair_accessible": convert_bool(loc.get('feature_wheelchair_accessible')),
            "feature_kids_friendly": convert_bool(loc.get('feature_kids_friendly')),
            "feature_dogs_allowed": convert_bool(loc.get('feature_dogs_allowed')),
            "feature_fee": convert_bool(loc.get('feature_fee')),
            "feature_seasonal": convert_bool(loc.get('feature_seasonal')),
            "feature_fkk": convert_bool(loc.get('feature_fkk')),
            "feature_restaurant": convert_bool(loc.get('feature_restaurant')),
            "feature_photography": convert_bool(loc.get('feature_photography')),
            "feature_historic": convert_bool(loc.get('feature_historic')),
        }
        js_data.append(item)
    return js_data


def generate_ai_summary(locations):
    """Generate AI-friendly summary with key facts"""
    total_locations = len(locations)

    # Count features
    with_toilets = sum(1 for loc in locations if convert_bool(loc.get('feature_toilets')))
    wheelchair = sum(1 for loc in locations if convert_bool(loc.get('feature_wheelchair_accessible')))
    kids_friendly = sum(1 for loc in locations if convert_bool(loc.get('feature_kids_friendly')))
    dogs_allowed = sum(1 for loc in locations if convert_bool(loc.get('feature_dogs_allowed')))
    free_entry = sum(1 for loc in locations if convert_bool(loc.get('feature_fee')) == False)

    return {
        "total_locations": total_locations,
        "with_toilets": with_toilets,
        "wheelchair_accessible": wheelchair,
        "kids_friendly": kids_friendly,
        "dogs_allowed": dogs_allowed,
        "free_entry": free_entry,
        "last_updated": config["last_updated"],
        "coverage": "Park Babelsberg, Schloss Babelsberg, Neuer Schlossgarten"
    }


def generate_statistics_grid(summary):
    """Generate information-dense statistics grid"""
    stats_html = f"""
    <div class="stats-grid">
      <div class="stat-card">
        <div class="number">{summary['total_locations']}</div>
        <div class="label">Attraktionen</div>
        <div class="detail">Vollständig dokumentiert</div>
      </div>
      <div class="stat-card">
        <div class="number">{summary['with_toilets']}</div>
        <div class="label">Mit Toiletten</div>
        <div class="detail">{round(summary['with_toilets']/summary['total_locations']*100)}% der Locations</div>
      </div>
      <div class="stat-card">
        <div class="number">{summary['wheelchair_accessible']}</div>
        <div class="label">Barrierefrei</div>
        <div class="detail">Rollstuhlgeeignet</div>
      </div>
      <div class="stat-card">
        <div class="number">{summary['kids_friendly']}</div>
        <div class="label">Kinderfreundlich</div>
        <div class="detail">Geeignet für Familien</div>
      </div>
      <div class="stat-card">
        <div class="number">{summary['dogs_allowed']}</div>
        <div class="label">Hunde erlaubt</div>
        <div class="detail">Leinenpflicht beachten</div>
      </div>
      <div class="stat-card">
        <div class="number">{summary['free_entry']}</div>
        <div class="label">Kostenfrei</div>
        <div class="detail">Ohne Eintrittsgebühr</div>
      </div>
    </div>
    """
    return stats_html


def generate_accessibility_guide(summary):
    """Generate comprehensive accessibility information section"""
    accessibility_html = f"""
    <div class="accessibility-guide">
      <h2>Barrierefreiheit & Zugänglichkeit</h2>
      <p class="intro">Der Park Babelsberg ist grundsätzlich öffentlich zugänglich. {summary['wheelchair_accessible']} von {summary['total_locations']} dokumentierten Locations sind als barrierefrei markiert. Hier finden Sie detaillierte Informationen zur Zugänglichkeit:</p>

      <div class="accessibility-grid">
        <div class="access-item">
          <h3>Rollstuhlfahrer & Mobilitätshilfen</h3>
          <ul>
            <li>Uferweg Nord am Tiefen See: Fester Belag, weitgehend eben</li>
            <li>Hauptwege zum Schloss: Asphaltiert und gut befahrbar</li>
            <li>Einige Nebenwege: Kies oder Naturbelag (eingeschränkt nutzbar)</li>
            <li>Steigungen: Teilweise vorhanden, besonders im südlichen Parkbereich</li>
            <li>Nutzen Sie den "Barrierefrei"-Filter oben für geeignete Locations</li>
          </ul>
        </div>

        <div class="access-item">
          <h3>Toiletten & Sanitäranlagen</h3>
          <ul>
            <li>{summary['with_toilets']} Locations mit Toiletten dokumentiert</li>
            <li>Hauptstandorte: Vor dem Schloss Babelsberg, beim Spielplatz</li>
            <li>Barrierefreie WCs verfügbar (nach Verfügbarkeit)</li>
            <li>Öffnungszeiten beachten: Saisonal unterschiedlich</li>
            <li>Filter "Toiletten" zeigt alle Standorte mit WC-Zugang</li>
          </ul>
        </div>

        <div class="access-item">
          <h3>Familien & Kinder</h3>
          <ul>
            <li>{summary['kids_friendly']} kinderfreundliche Locations</li>
            <li>Moderner Spielplatz mit altersgerechten Geräten</li>
            <li>Weitläufige Liegewiesen zum Spielen und Toben</li>
            <li>Picknickbereiche mit Sitzgelegenheiten</li>
            <li>Kinderwagen: Hauptwege gut geeignet, Nebenwege teilweise schwierig</li>
          </ul>
        </div>

        <div class="access-item">
          <h3>Anreise & Parkplätze</h3>
          <ul>
            <li>Hauptparkplatz: Albert-Einstein-Straße (kostenpflichtig)</li>
            <li>Fußweg zum Schloss: 5-10 Minuten vom Parkplatz</li>
            <li>ÖPNV: Bus-Haltestellen in der Nähe</li>
            <li>Fahrradstellplätze vorhanden</li>
            <li>Begrenzte Behindertenparkplätze (nach Verfügbarkeit)</li>
          </ul>
        </div>
      </div>
    </div>
    """
    return accessibility_html


def generate_feature_table(locations):
    """Generate comprehensive feature comparison table"""
    rows = []
    for loc in locations:
        toilets = "✓" if convert_bool(loc.get('feature_toilets')) else "—"
        wheelchair = "✓" if convert_bool(loc.get('feature_wheelchair_accessible')) else "—"
        kids = "✓" if convert_bool(loc.get('feature_kids_friendly')) else "—"
        dogs = "✓" if convert_bool(loc.get('feature_dogs_allowed')) else "—"
        parking = "✓" if convert_bool(loc.get('feature_parking')) else "—"
        free = "✓" if not convert_bool(loc.get('feature_fee')) else "—"
        restaurant = "✓" if convert_bool(loc.get('feature_restaurant')) else "—"
        historic = "✓" if convert_bool(loc.get('feature_historic')) else "—"

        row = f"""
        <tr>
          <td><strong>{loc['name']}</strong></td>
          <td class="{'check' if toilets == '✓' else 'no-check'}">{toilets}</td>
          <td class="{'check' if wheelchair == '✓' else 'no-check'}">{wheelchair}</td>
          <td class="{'check' if kids == '✓' else 'no-check'}">{kids}</td>
          <td class="{'check' if dogs == '✓' else 'no-check'}">{dogs}</td>
          <td class="{'check' if parking == '✓' else 'no-check'}">{parking}</td>
          <td class="{'check' if free == '✓' else 'no-check'}">{free}</td>
          <td class="{'check' if restaurant == '✓' else 'no-check'}">{restaurant}</td>
          <td class="{'check' if historic == '✓' else 'no-check'}">{historic}</td>
        </tr>
        """
        rows.append(row)

    table_html = f"""
    <div class="feature-table">
      <h2>Übersicht aller Ausstattungsmerkmale</h2>
      <p style="margin-bottom: 20px; color: var(--text-light);">Alle {len(locations)} Locations im direkten Vergleich. Filtern Sie oben nach Ihren Wünschen oder nutzen Sie diese Tabelle zur Orientierung.</p>
      <table>
        <thead>
          <tr>
            <th>Location</th>
            <th>Toiletten</th>
            <th>Barrierefrei</th>
            <th>Kinder</th>
            <th>Hunde</th>
            <th>Parkplatz</th>
            <th>Kostenfrei</th>
            <th>Gastronomie</th>
            <th>Historisch</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </div>
    """
    return table_html


def generate_html(locations, output_path):
    """Generate AI-SEO optimized HTML"""

    js_data = prepare_location_data(locations)
    faq_schema = generate_faq_schema(locations)
    breadcrumb_schema = generate_breadcrumb_schema()
    org_schema = generate_organization_schema()
    summary = generate_ai_summary(locations)
    stats_grid = generate_statistics_grid(summary)
    accessibility_guide = generate_accessibility_guide(summary)
    feature_table = generate_feature_table(locations)

    # AI-optimized meta description
    meta_description = f"Park Babelsberg & Schloss Potsdam Guide {config['year']}: {summary['total_locations']} Attraktionen mit Filtern für Toiletten ({summary['with_toilets']}), Barrierefreiheit ({summary['wheelchair_accessible']}), Kinderfreundlich ({summary['kids_friendly']}). Aktualisiert {summary['last_updated']}."

    # AI-friendly keywords
    meta_keywords = "Park Babelsberg 2025, Schloss Babelsberg Potsdam, UNESCO Welterbe, barrierefrei, Toiletten, kinderfreundlich, Hunde erlaubt, FKK, Fotospots, Neuer Schlossgarten, Ausflugsziele Potsdam"

    # AI-optimized title
    page_title = f"Park Babelsberg Guide {config['year']} – {summary['total_locations']} Attraktionen mit Filter | Potsdam UNESCO Welterbe"

    html = f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">

  <!-- AI-Optimized Title & Meta -->
  <title>{page_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="keywords" content="{meta_keywords}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="author" content="Babelsberger.info">
  <meta name="date" content="{config['last_updated']}" scheme="YYYY-MM-DD">
  <link rel="canonical" href="{config['domain']}/">

  <!-- Open Graph / Social Media -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{config['domain']}/">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:image" content="{config['domain']}/images/park-babelsberg/hero.webp">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Babelsberger.info">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{meta_description}">
  <meta name="twitter:image" content="{config['domain']}/images/park-babelsberg/hero.webp">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/favicon.png">

  <!-- AI Summary Meta (for ChatGPT, Perplexity, etc.) -->
  <meta name="summary" content="Interaktiver Guide für Park Babelsberg mit {summary['total_locations']} detaillierten Locations. Filter: Toiletten, Barrierefreiheit, Kinderfreundlich, Hunde erlaubt, FKK. Letzte Aktualisierung: {summary['last_updated']}.">
  <meta name="coverage" content="Park Babelsberg, Schloss Babelsberg, Neuer Schlossgarten, Potsdam, Brandenburg, Deutschland">
  <meta name="category" content="Travel, Tourism, Parks, UNESCO World Heritage, Local Guide">

  <!-- Multiple Schema.org Types for AI Understanding -->
  <script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(org_schema, ensure_ascii=False, indent=2)}
  </script>

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={config['ga_id']}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{config['ga_id']}');
  </script>

  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{config['adsense_id']}"
          crossorigin="anonymous"></script>

  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    :root {{
      --primary: #2c5f2d;
      --secondary: #97c05c;
      --accent: #ffa500;
      --text: #1a1a1a;
      --text-light: #666;
      --bg: #f9fafb;
      --card-bg: #ffffff;
      --border: #e5e7eb;
      --shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.7;
      color: var(--text);
      background: var(--bg);
    }}

    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {{
      font-family: Georgia, 'Times New Roman', Times, serif;
      font-weight: 600;
      letter-spacing: -0.02em;
      line-height: 1.3;
    }}

    /* Header */
    header {{
      background: linear-gradient(135deg, var(--primary) 0%, #1a4d1b 100%);
      color: white;
      padding: 60px 20px;
      text-align: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}

    header h1 {{
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 12px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }}

    header p {{
      font-size: 1.2rem;
      opacity: 0.95;
      max-width: 700px;
      margin: 0 auto 20px;
    }}

    /* AI Summary Badge */
    .ai-summary {{
      background: rgba(255,255,255,0.2);
      padding: 15px 25px;
      border-radius: 8px;
      display: inline-block;
      margin-top: 15px;
      backdrop-filter: blur(10px);
    }}

    .ai-summary strong {{
      font-size: 1.1rem;
    }}

    /* Container */
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }}

    /* Filters */
    .filters {{
      background: var(--card-bg);
      border-radius: 12px;
      padding: 24px;
      margin: 30px 0;
      box-shadow: var(--shadow);
      border: 2px solid var(--border);
    }}

    .filters h2 {{
      font-size: 1.5rem;
      margin-bottom: 16px;
      color: var(--primary);
    }}

    .filter-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
    }}

    .filter-grid label {{
      display: flex;
      align-items: center;
      padding: 10px;
      background: var(--bg);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      border: 2px solid transparent;
    }}

    .filter-grid label:hover {{
      background: #e8f5e9;
      border-color: var(--secondary);
    }}

    .filter-grid input[type="checkbox"] {{
      margin-right: 8px;
      width: 18px;
      height: 18px;
      cursor: pointer;
    }}

    /* Stats */
    .stats {{
      text-align: center;
      padding: 20px;
      background: white;
      border-radius: 8px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
    }}

    .stats strong {{
      font-size: 2rem;
      color: var(--primary);
    }}

    /* Location Cards */
    .location-card {{
      background: var(--card-bg);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
      border-left: 4px solid var(--secondary);
      transition: transform 0.2s, box-shadow 0.2s;
    }}

    .location-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }}

    .location-card h3 {{
      font-size: 1.5rem;
      margin-bottom: 8px;
      color: var(--primary);
    }}

    .location-card .address {{
      color: var(--text-light);
      margin-bottom: 12px;
    }}

    .location-card .rating {{
      margin-bottom: 12px;
      font-weight: 500;
    }}

    .location-card .description {{
      margin: 16px 0;
      line-height: 1.7;
      color: var(--text);
    }}

    /* Feature Badges */
    .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 16px 0;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 0.875rem;
      font-weight: 500;
      white-space: nowrap;
    }}

    .badge.shade {{ background: #dcfce7; color: #166534; }}
    .badge.water {{ background: #dbeafe; color: #1e40af; }}
    .badge.benches {{ background: #fef3c7; color: #92400e; }}
    .badge.parking {{ background: #e5e7eb; color: #374151; }}
    .badge.toilets {{ background: #fce7f3; color: #be185d; }}
    .badge.wheelchair {{ background: #f0f9ff; color: #0369a1; }}
    .badge.kids {{ background: #fef7cd; color: #a16207; }}
    .badge.dogs {{ background: #ecfccb; color: #365314; }}
    .badge.free {{ background: #dcfce7; color: #166534; }}
    .badge.restaurant {{ background: #ffedd5; color: #9a3412; }}
    .badge.photography {{ background: #e0e7ff; color: #3730a3; }}
    .badge.historic {{ background: #fce7f3; color: #9f1239; }}

    /* Links */
    .location-card a {{
      display: inline-block;
      margin-top: 12px;
      color: var(--primary);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.2s;
    }}

    .location-card a:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}

    /* Last Updated Badge */
    .last-updated {{
      text-align: center;
      padding: 10px;
      background: #fef3c7;
      border-radius: 8px;
      margin: 20px 0;
      font-weight: 500;
      color: #92400e;
    }}

    /* Statistics Grid */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin: 30px 0;
    }}

    .stat-card {{
      background: var(--card-bg);
      border-radius: 12px;
      padding: 24px;
      text-align: center;
      box-shadow: var(--shadow);
      border-top: 4px solid var(--secondary);
    }}

    .stat-card .number {{
      font-size: 3rem;
      font-weight: 700;
      color: var(--primary);
      line-height: 1;
      margin-bottom: 8px;
      font-family: Georgia, serif;
    }}

    .stat-card .label {{
      font-size: 0.95rem;
      color: var(--text-light);
      font-weight: 500;
    }}

    .stat-card .detail {{
      font-size: 0.85rem;
      color: var(--text-light);
      margin-top: 8px;
    }}

    /* Accessibility Guide */
    .accessibility-guide {{
      background: #f0f9ff;
      border-radius: 12px;
      padding: 32px;
      margin: 30px 0;
      border-left: 4px solid var(--primary);
    }}

    .accessibility-guide h2 {{
      font-size: 1.8rem;
      margin-bottom: 16px;
      color: var(--primary);
    }}

    .accessibility-guide .intro {{
      color: var(--text);
      margin-bottom: 24px;
      line-height: 1.8;
      font-size: 1.05rem;
    }}

    .accessibility-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}

    .access-item {{
      background: white;
      padding: 20px;
      border-radius: 8px;
      border-left: 3px solid var(--secondary);
    }}

    .access-item h3 {{
      font-size: 1.2rem;
      margin-bottom: 12px;
      color: var(--primary);
    }}

    .access-item ul {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}

    .access-item li {{
      padding: 6px 0;
      padding-left: 20px;
      position: relative;
      line-height: 1.6;
    }}

    .access-item li:before {{
      content: "•";
      position: absolute;
      left: 0;
      color: var(--secondary);
      font-weight: bold;
      font-size: 1.2em;
    }}

    /* Feature Comparison Table */
    .feature-table {{
      background: var(--card-bg);
      border-radius: 12px;
      padding: 24px;
      margin: 30px 0;
      box-shadow: var(--shadow);
      overflow-x: auto;
    }}

    .feature-table h2 {{
      font-size: 1.8rem;
      margin-bottom: 20px;
      color: var(--primary);
    }}

    .feature-table table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }}

    .feature-table th {{
      background: var(--primary);
      color: white;
      padding: 12px 8px;
      text-align: left;
      font-weight: 600;
      white-space: nowrap;
    }}

    .feature-table td {{
      padding: 10px 8px;
      border-bottom: 1px solid var(--border);
    }}

    .feature-table tr:hover {{
      background: #f0f9ff;
    }}

    .feature-table .check {{
      color: #166534;
      font-weight: bold;
      text-align: center;
    }}

    .feature-table .no-check {{
      color: #9ca3af;
      text-align: center;
    }}

    /* Footer */
    footer {{
      background: var(--card-bg);
      padding: 40px 20px;
      margin-top: 60px;
      border-top: 3px solid var(--secondary);
    }}

    footer h2 {{
      font-size: 1.8rem;
      margin-bottom: 24px;
      color: var(--primary);
    }}

    footer h3 {{
      font-size: 1.2rem;
      margin: 20px 0 8px;
      color: var(--primary);
    }}

    footer p {{
      color: var(--text-light);
      line-height: 1.7;
      margin-bottom: 16px;
    }}

    .footer-bottom {{
      text-align: center;
      padding-top: 32px;
      margin-top: 32px;
      border-top: 1px solid var(--border);
      color: var(--text-light);
      font-size: 0.9rem;
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      header h1 {{
        font-size: 1.8rem;
      }}

      header p {{
        font-size: 1rem;
      }}

      .filter-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Ad Containers */
    .ad-container {{
      margin: 30px 0;
      padding: 20px;
      background: #f8f9fa;
      border-radius: 8px;
      text-align: center;
    }}
  </style>
</head>
<body>
<header>
  <h1>Park Babelsberg & Schloss Potsdam</h1>
  <p>UNESCO Welterbe • {summary['total_locations']} Attraktionen • Interaktive Filter</p>
  <div class="ai-summary">
    <strong>Live Daten:</strong> {summary['with_toilets']} mit Toiletten • {summary['wheelchair_accessible']} barrierefrei • {summary['kids_friendly']} kinderfreundlich
  </div>
</header>

<main class="container">
  <div class="last-updated">
    Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y')} • Alle Informationen geprüft
  </div>

  {stats_grid}

  <!-- Top Ad -->
  <div class="ad-container">
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-{config['adsense_id']}"
         data-ad-slot="1234567890"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  <div class="filters">
    <h2>Finden Sie genau das, was Sie suchen:</h2>
    <div class="filter-grid" id="filterGrid"></div>
  </div>

  <div class="stats" id="stats">
    Zeige <strong id="count">{len(locations)}</strong> von {len(locations)} Orten
  </div>

  {feature_table}

  <div id="locationList"></div>

  <!-- Bottom Ad -->
  <div class="ad-container">
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-{config['adsense_id']}"
         data-ad-slot="0987654321"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  {accessibility_guide}
</main>

<footer class="container">
  <h2>Häufig gestellte Fragen (FAQ)</h2>

  <h3>Welche Attraktionen gibt es im Park Babelsberg?</h3>
  <p>Der Park Babelsberg bietet {len(locations)} Hauptattraktionen: Schloss Babelsberg (UNESCO Welterbe), Flatowturm (Aussichtsturm), Matrosenhaus, Gerichtslaube und mehrere Liegewiesen am Wasser. Alle Orte sind mit GPS-Koordinaten und detaillierten Informationen zu Barrierefreiheit, Toiletten und Kinderfreundlichkeit dokumentiert.</p>

  <h3>Gibt es Toiletten im Park Babelsberg?</h3>
  <p>Ja, Toiletten befinden sich vor dem Schloss Babelsberg und beim Spielplatz. Nutzen Sie unseren Filter "Toiletten" um alle Orte mit WC-Zugang zu finden. Stand {config['last_updated']}: {summary['with_toilets']} Locations mit Toiletten.</p>

  <h3>Ist der Park Babelsberg barrierefrei?</h3>
  <p>Der Uferweg Nord am Tiefen See ist weitgehend barrierefrei mit festem Belag. Viele Hauptwege sind für Rollstuhlfahrer geeignet. {summary['wheelchair_accessible']} von {summary['total_locations']} Locations sind als barrierefrei markiert. Nutzen Sie unseren "Barrierefrei"-Filter.</p>

  <h3>Sind Hunde im Park Babelsberg erlaubt?</h3>
  <p>Ja, Hunde sind erlaubt ({summary['dogs_allowed']} Locations hundefreundlich), müssen aber an der Leine geführt werden. Bitte Hundekotbeutel mitführen und die Parkordnung beachten.</p>

  <h3>Gibt es Parkplätze am Park Babelsberg?</h3>
  <p>Ja, der Hauptparkplatz befindet sich an der Albert-Einstein-Straße (kostenpflichtig). Von dort sind es ca. 5-10 Minuten Fußweg zum Schloss und den Hauptattraktionen.</p>

  <h3>Ist der Park Babelsberg kinderfreundlich?</h3>
  <p>Sehr! {summary['kids_friendly']} von {summary['total_locations']} Locations sind kinderfreundlich. Es gibt einen gut ausgestatteten Spielplatz mit modernen Geräten, weitläufige Liegewiesen zum Toben und schattige Picknickbereiche.</p>

  <h3>Wo kann man im Park Babelsberg fotografieren?</h3>
  <p>Top Fotospots: Schloss Babelsberg (beste Zeit: Abendlicht), Flatowturm (Panorama), Zypressen-Allee, Uferweg mit Blick über den Tiefen See und die Steintreppe am Wasser. Nutzen Sie unseren "Fotografie"-Filter für alle Spots.</p>

  <h3>Was kostet der Eintritt in den Park Babelsberg?</h3>
  <p>Der Park ist frei zugänglich (kostenfrei). {summary['free_entry']} von {summary['total_locations']} Attraktionen sind kostenlos. Nur das Schloss-Innere kostet Eintritt. Parkgebühren fallen am Parkplatz an.</p>

  <div class="footer-bottom">
    <p>&copy; {datetime.now().year} Babelsberger.info | <a href="/impressum.html">Impressum</a> | <a href="/datenschutz.html">Datenschutz</a></p>
    <p>Letzte Aktualisierung: {config['last_updated']} • {summary['total_locations']} Attraktionen • Park Babelsberg, Schloss Babelsberg, Neuer Schlossgarten</p>
  </div>
</footer>

<script>
const LOCATIONS = {json.dumps(js_data, ensure_ascii=False, indent=2)};

const FILTERS = [
  {{ id: 'shade', label: 'Schatten', field: 'feature_shade' }},
  {{ id: 'water', label: 'Wasser', field: 'feature_water' }},
  {{ id: 'benches', label: 'Sitzbänke', field: 'feature_benches' }},
  {{ id: 'parking', label: 'Parkplatz', field: 'feature_parking' }},
  {{ id: 'toilets', label: 'Toiletten', field: 'feature_toilets' }},
  {{ id: 'wheelchair', label: 'Barrierefrei', field: 'feature_wheelchair_accessible' }},
  {{ id: 'kids', label: 'Kinderfreundlich', field: 'feature_kids_friendly' }},
  {{ id: 'dogs', label: 'Hunde erlaubt', field: 'feature_dogs_allowed' }},
  {{ id: 'free', label: 'Kostenfrei', field: 'feature_fee', inverse: true }},
  {{ id: 'restaurant', label: 'Restaurant/Café', field: 'feature_restaurant' }},
  {{ id: 'photography', label: 'Fotografie', field: 'feature_photography' }},
  {{ id: 'historic', label: 'Historisch', field: 'feature_historic' }},
];

// Render filters
const filterGrid = document.getElementById('filterGrid');
filterGrid.innerHTML = FILTERS.map(f => `
  <label>
    <input type="checkbox" id="filter_${{f.id}}" data-field="${{f.field}}" data-inverse="${{f.inverse || false}}">
    <span>${{f.label}}</span>
  </label>
`).join('');

// Render locations
function renderLocations(locations) {{
  const list = document.getElementById('locationList');

  if (locations.length === 0) {{
    list.innerHTML = '<div class="stats"><p>Keine Orte gefunden mit den gewählten Filtern. Bitte passen Sie Ihre Suche an.</p></div>';
    return;
  }}

  list.innerHTML = locations.map((loc, idx) => {{
    const badges = [];

    if (loc.feature_shade) badges.push('<span class="badge shade">Schatten</span>');
    if (loc.feature_water) badges.push('<span class="badge water">Wasser</span>');
    if (loc.feature_benches) badges.push('<span class="badge benches">Sitzbänke</span>');
    if (loc.feature_parking) badges.push('<span class="badge parking">Parkplatz</span>');
    if (loc.feature_toilets) badges.push('<span class="badge toilets">Toiletten</span>');
    if (loc.feature_wheelchair_accessible) badges.push('<span class="badge wheelchair">Barrierefrei</span>');
    if (loc.feature_kids_friendly) badges.push('<span class="badge kids">Kinderfreundlich</span>');
    if (loc.feature_dogs_allowed) badges.push('<span class="badge dogs">Hunde erlaubt</span>');
    if (loc.feature_fee === false) badges.push('<span class="badge free">Kostenfrei</span>');
    if (loc.feature_restaurant) badges.push('<span class="badge restaurant">Restaurant</span>');
    if (loc.feature_photography) badges.push('<span class="badge photography">Fotografie</span>');
    if (loc.feature_historic) badges.push('<span class="badge historic">Historisch</span>');

    return `
      <article class="location-card">
        <h3>${{loc.name}}</h3>
        <div class="address">${{loc.address}}, ${{loc.city}}</div>
        ${{loc.rating ? `<div class="rating">Bewertung: ${{loc.rating.toFixed(1)}}/5.0 (${{loc.review_count}} Bewertungen)</div>` : ''}}
        ${{loc.opening_hours ? `<div style="margin-bottom: 12px;"><strong>Öffnungszeiten:</strong> ${{loc.opening_hours}}</div>` : ''}}
        ${{loc.description ? `<div class="description">${{loc.description}}</div>` : ''}}
        <div class="badges">${{badges.join('')}}</div>
        ${{loc.website ? `<a href="${{loc.website}}" target="_blank" rel="noopener">Mehr Informationen</a>` : ''}}
      </article>
      ${{idx > 0 && idx % 5 === 0 ? `
        <div class="ad-container">
          <ins class="adsbygoogle"
               style="display:block"
               data-ad-client="ca-{config['adsense_id']}"
               data-ad-slot="5555555555"
               data-ad-format="fluid"></ins>
          <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>
      ` : ''}}
    `;
  }}).join('');

  document.getElementById('count').textContent = locations.length;
}}

// Apply filters
function applyFilters() {{
  let filtered = LOCATIONS;

  FILTERS.forEach(f => {{
    const checkbox = document.getElementById(`filter_${{f.id}}`);
    if (checkbox && checkbox.checked) {{
      filtered = filtered.filter(loc => {{
        if (f.inverse) {{
          return loc[f.field] === false;
        }} else {{
          return loc[f.field] === true;
        }}
      }});
    }}
  }});

  renderLocations(filtered);

  // Track filter usage
  if (typeof gtag !== 'undefined') {{
    const activeFilterNames = FILTERS
      .filter(f => document.getElementById(`filter_${{f.id}}`).checked)
      .map(f => f.id);

    gtag('event', 'filter_applied', {{
      'filters': activeFilterNames.join(','),
      'result_count': filtered.length
    }});
  }}
}}

// Add event listeners
document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {{
  checkbox.addEventListener('change', applyFilters);
}});

// Initial render
renderLocations(LOCATIONS);
</script>
</body>
</html>
"""

    # Write HTML file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding='utf-8')

    print(f"Generated AI-optimized: {output_path}")
    print(f"Total locations: {len(locations)}")
    print(f"AI SEO Features:")
    print(f"   - FAQPage Schema with {len(faq_schema['mainEntity'])} questions")
    print(f"   - BreadcrumbList Schema")
    print(f"   - Organization Schema")
    print(f"   - AI-friendly meta tags")
    print(f"   - Last updated: {config['last_updated']}")

    return output_path


def main():
    # Paths
    csv_path = Path(__file__).parent / "data" / "babelsberg_locations.csv"
    output_path = Path(__file__).parent / "generated" / "index.html"

    print("Generating AI-SEO optimized Babelsberg site...")
    print(f"Reading data from: {csv_path}")

    # Load and generate
    locations = load_locations(csv_path)
    html_path = generate_html(locations, output_path)

    print(f"\nAI-optimized site generated!")
    print(f"Open: file://{html_path.absolute()}")
    print(f"\nReady for deployment to: {config['domain']}")
    print(f"\nOptimized for: ChatGPT, Perplexity, Claude, Google AI")


if __name__ == "__main__":
    main()
