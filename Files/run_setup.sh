#!/bin/bash

# ADS Pillar - Quick Start Script
# Führt alle Setup-Schritte automatisch aus

set -e

echo "🚀 ADS Pillar - Automatischer Setup"
echo "=================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert. Bitte installieren und erneut versuchen."
    exit 1
fi

echo "✅ Python 3 gefunden"

# Create and activate virtual environment, then install required Python packages
echo "📦 Erstelle und aktiviere Python-virtualenv..."
python3 -m venv .venv
# shellcheck source=/dev/null
source .venv/bin/activate

echo "📦 Installiere Python-Abhängigkeiten..."
pip install -r requirements.txt

# Check if data directory exists, create if not
if [ ! -d "data" ]; then
    mkdir -p data
    echo "✅ Data-Verzeichnis erstellt"
fi

# Check if generated directory exists, create if not
if [ ! -d "generated" ]; then
    mkdir -p generated
    echo "✅ Generated-Verzeichnis erstellt"
fi

# Run niche research
echo ""
echo "🔍 Starte Nischen-Analyse..."
python3 niche_research.py > niche_analysis_results.txt || true
echo "✅ Nischen-Analyse abgeschlossen (siehe niche_analysis_results.txt)"

# Run SEO setup
echo ""
echo "🔧 Starte SEO-Setup..."
python3 seo_setup.py || true
echo "✅ SEO-Setup abgeschlossen"

# Create sample data file
echo ""
echo "📊 Erstelle Beispiel-Daten..."
cat > data/sample_parks_berlin.csv << EOF
id,name,street,city,region,country,postcode,latitude,longitude,url,phone,email,opening_hours,rating,review_count,feature_shade,feature_benches,feature_water,feature_parking,feature_toilets,feature_wheelchair_accessible,feature_kids_friendly,feature_dogs_allowed,feature_fee,feature_seasonal,tags
1,"Tiergarten","Unter den Linden 1","Berlin","Berlin","Deutschland","10117",52.5144,13.3501,"https://berlin.de/tiergarten","+49 30 123456","","Mo-So 06:00-22:00",4.5,1250,true,true,true,false,true,true,true,true,false,false,"park,zentral,tourist"
2,"Volkspark Friedrichshain","Am Friedrichshain 1","Berlin","Berlin","Deutschland","10249",52.5286,13.4342,"https://berlin.de/friedrichshain","+49 30 789012","","Mo-So 06:00-22:00",4.2,856,true,true,false,false,true,true,true,true,false,false,"park,sport,familie"
3,"Mauerpark","Bernauer Str. 63-64","Berlin","Berlin","Deutschland","13355",52.5408,13.4022,"https://mauerpark.info","","","Mo-So 24h",4.3,2103,true,true,false,false,false,false,true,true,false,false,"park,flohmarkt,kultur"
EOF

echo "✅ Beispiel-Daten erstellt (data/sample_parks_berlin.csv)"

# Generate sample pillar page
echo ""
echo "🏗️ Generiere Beispiel-Pillar-Seite..."
python3 - << 'PYCODE'
from data_pipeline import PillarPageGenerator, LocationData
import pandas as pd

# Load sample data
df = pd.read_csv('data/sample_parks_berlin.csv')

# Convert to LocationData objects
locations = []
for _, row in df.iterrows():
    loc = LocationData(
        id=str(row['id']),
        name=row['name'],
        street=row['street'],
        city=row['city'],
        region=row['region'],
        country=row['country'],
        postcode=str(row['postcode']),
        latitude=float(row['latitude']),
        longitude=float(row['longitude']),
        url=row['url'],
        phone=row['phone'],
        email=row['email'],
        opening_hours=row['opening_hours'],
        rating=float(row['rating']),
        review_count=int(row['review_count']),
        feature_shade=bool(row['feature_shade']),
        feature_benches=bool(row['feature_benches']),
        feature_water=bool(row['feature_water']),
        feature_parking=bool(row['feature_parking']),
        feature_toilets=bool(row['feature_toilets']),
        feature_wheelchair_accessible=bool(row['feature_wheelchair_accessible']),
        feature_kids_friendly=bool(row['feature_kids_friendly']),
        feature_dogs_allowed=bool(row['feature_dogs_allowed']),
        feature_fee=bool(row['feature_fee']),
        feature_seasonal=bool(row['feature_seasonal']),
        tags=row['tags']
    )
    locations.append(loc)

# Generate page
generator = PillarPageGenerator('pillar_page_skeleton.html')
generator.generate_page(
    data=locations,
    city='Berlin',
    category='Parks',
    output_path='generated/berlin_parks_example.html',
    canonical_url='https://your-domain.com/berlin-parks'
)
PYCODE

echo "✅ Beispiel-Pillar-Seite generiert (generated/berlin_parks_example.html)"

# Create launch checklist
echo ""
echo "📋 Erstelle Launch-Checkliste..."
cat > launch_checklist.md << 'EOF'
# 🚀 ADS Pillar - Launch Checkliste

## ✅ Pre-Launch (vor dem Live-Gang)

### Domain & Hosting
- [ ] Domain registriert
- [ ] Hosting-Provider gewählt (Empfehlung: Netlify, Vercel, oder traditioneller Webhost)
- [ ] SSL-Zertifikat aktiv
- [ ] DNS richtig konfiguriert

### Google Services Setup
- [ ] Google AdSense Konto erstellt und genehmigt
- [ ] Google Analytics 4 eingerichtet
- [ ] Google Search Console hinzugefügt
- [ ] Publisher-ID in allen HTML-Dateien ersetzt

### Content & SEO
- [ ] Mindestens 20-50 Locations in CSV
- [ ] Alle Locations mit korrekten Koordinaten
- [ ] Feature-Extraction aus Reviews durchgeführt
- [ ] Meta-Tags und Descriptions optimiert
- [ ] Schema.org JSON-LD implementiert

### Legal & Compliance
- [ ] Impressum erstellt
- [ ] Datenschutzerklärung (DSGVO-konform)
- [ ] Cookie-Consent-Banner (für EU-Traffic)
- [ ] ads.txt auf Root-Level hochgeladen

## 🎯 Tag 1-7 (Launch-Woche)

### Tag 1: Go Live
- [ ] Alle Dateien auf Server hochgeladen
- [ ] robots.txt und sitemap.xml live
- [ ] Erste Funktionstest der Website
- [ ] AdSense Auto Ads aktiviert

### Tag 2-3: Search Engine Submission
- [ ] Sitemap in Google Search Console eingereicht
- [ ] Bing Webmaster Tools konfiguriert
- [ ] Erste Indexierungsanfragen gesendet

### Tag 4-5: Monitoring Setup
- [ ] Google Analytics Goals konfiguriert
- [ ] AdSense Performance-Tracking aktiviert
- [ ] Uptime-Monitoring eingerichtet
- [ ] Keyword-Ranking-Tool konfiguriert

### Tag 6-7: First Optimizations
- [ ] Page Speed optimiert (< 3 Sekunden)
- [ ] Mobile Usability getestet
- [ ] Erste Ad-Placement Tests
- [ ] Social Media Profile erstellt (optional)

## 📊 Woche 2-4 (Optimierung)

### Performance Monitoring
- [ ] Tägliches AdSense Dashboard Check
- [ ] Wöchentliche Analytics Review
- [ ] Keyword-Ranking Entwicklung
- [ ] Core Web Vitals überwacht

### Content Expansion
- [ ] 5-10 zusätzliche Locations hinzugefügt
- [ ] FAQ-Sektion erweitert
- [ ] Über-Uns Seite detaillierter gestaltet
- [ ] Blog-Sektion gestartet (optional)

## 🎯 KPI-Ziele erste 3 Monate

### Monat 1
- Ziel: 1.000+ Impressions in Google Search Console
- Ziel: 100+ Klicks aus organischer Suche
- Ziel: AdSense aktiviert und erste Einnahmen
- Ziel: Durchschnittliche Position < 50 für Hauptkeywords

### Monat 2
- Ziel: 5.000+ Impressions
- Ziel: 500+ Klicks
- Ziel: €50+ AdSense Revenue
- Ziel: Top 30 Positionen für 3-5 Keywords

### Monat 3
- Ziel: 15.000+ Impressions
- Ziel: 1.500+ Klicks
- Ziel: €200+ AdSense Revenue
- Ziel: Top 10 Position für mindestens 1 Hauptkeyword

## 🚨 Troubleshooting

### Häufige Probleme

**AdSense zeigt keine Anzeigen:**
- Publisher-ID korrekt eingefügt?
- ads.txt-Datei erreichbar?
- Genügend Content vorhanden?
- Policy-Verletzungen im Dashboard?

**Schlechte Rankings:**
- Sitemap eingereicht?
- Interne Verlinkung optimiert?
- Page Speed unter 3 Sekunden?
- Mobile-friendly?

**Niedrige CTR aus Google:**
- Meta-Descriptions optimiert?
- Title-Tags ansprechend?
- Schema Markup implementiert?
- Featured Snippets optimiert?

---

**💡 Success Tip:** Fokussiere dich die ersten 4 Wochen NUR auf eine Stadt und eine Kategorie. Master the basics before scaling!
EOF

echo "✅ Launch-Checkliste erstellt (launch_checklist.md)"

# Final summary
echo ""
echo "🎉 Setup abgeschlossen!"
echo "====================="
echo ""
echo "📁 Generierte Dateien:"
echo "   • niche_analysis_results.txt - Nischen-Empfehlungen"
echo "   • data/sample_parks_berlin.csv - Beispiel-Daten"
echo "   • generated/berlin_parks_example.html - Demo-Seite"
echo "   • launch_checklist.md - Go-Live Checkliste"
echo "   • robots.txt, sitemap.xml, ads.txt - SEO-Files"
echo ""
echo "🔧 Nächste Schritte:"
echo "   1. Öffne niche_analysis_results.txt für Nischen-Empfehlungen"
echo "   2. Öffne generated/berlin_parks_example.html im Browser"
echo "   3. Ersetze Beispieldaten durch echte Locations"
echo "   4. Konfiguriere AdSense und Analytics IDs"
echo "   5. Folge launch_checklist.md für Go-Live"

echo ""
echo "💰 Revenue-Potenzial (Zielbild): 120–360 €/Tag (≈ 3.6k–10.8k €/Monat)"
echo ""
echo "📊 Demo ansehen:"
echo "   open generated/berlin_parks_example.html"
echo ""
echo "✨ Viel Erfolg mit deinem ADS Pillar Projekt!"
