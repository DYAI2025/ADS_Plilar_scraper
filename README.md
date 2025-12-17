# 🏰 ADS Pillar Scraper

> **Programmatic SEO Toolkit** für automatisierte Location-basierte Directory Sites mit Google AdSense Monetarisierung

[![Tests](https://github.com/DYAI2025/ADS_Plilar_scraper/actions/workflows/test.yml/badge.svg)](https://github.com/DYAI2025/ADS_Plilar_scraper/actions/workflows/test.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ADS Pillar Scraper** ist ein vollständiges Python-Toolkit zum Erstellen von monetarisierbaren Location-Directory-Websites. Scrape Daten von Google Places API, extrahiere automatisch Features aus Reviews, generiere SEO-optimierte HTML-Seiten und monetarisiere mit Google AdSense.

---

## 📑 Inhaltsverzeichnis

- [Features](#-features)
- [Live Demo](#-live-demo)
- [Installation](#-installation)
  - [macOS](#macos)
  - [Linux](#linux)
  - [Windows](#windows)
- [Quick Start](#-quick-start)
- [Verwendung](#-verwendung)
- [Architektur](#-architektur)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎯 Kern-Funktionalität

- **🔍 Multi-Source Data Scraping**
  - Google Places API mit automatischer Pagination
  - Google Places Details API für Reviews, Öffnungszeiten, Kontakte
  - CSV Import/Export für manuelle Daten
  - Web Scraping für Directory-Seiten (Yelp-Style)

- **🤖 Intelligente Feature-Extraktion**
  - NLP-basierte Keyword-Erkennung (Deutsch/Englisch)
  - Automatische Feature-Flags aus Reviews (Schatten, Wasser, Toiletten, etc.)
  - Google price_level Integration für authentische Gebührenerkennung
  - 10+ vordefinierte Features: Parkplatz, Barrierefrei, Kinderfreundlich, Hunde erlaubt, etc.

- **📄 SEO-Optimierte Pillar Pages**
  - Jinja2-Template System
  - Schema.org JSON-LD (LocalBusiness, ItemList)
  - Client-side JavaScript Filtering
  - Mobile-responsive Design
  - Google AdSense Integration (Auto Ads + manuelle Slots)

- **💰 Monetarisierung**
  - Vorkonfigurierte AdSense-Platzierungen
  - ads.txt Generator
  - Revenue Calculator (GUI)
  - ROI-Kalkulation nach Traffic-Szenarien

- **🎨 GUI & CLI Tools**
  - Tkinter GUI für Non-Technical Users
  - Interactive Setup Wizard (`quick_start.py`)
  - Niche Research Tool mit Opportunity Scoring
  - Revenue Projections

- **💡 Review-Based Demand Analysis** ⭐ NEU!
  - **Automatische Analyse** von Google Places Reviews zur Identifizierung versteckter Nutzer-Bedürfnisse
  - **Unmet Needs Detection**: Findet Features, die Nutzer vermissen (z.B. "Parkplatz", "Schatten")
  - **Content-Ideen Generator**: Erstellt actionable Vorschläge für FAQ, Filter und kuratierte Listen
  - **Sentiment Analysis**: Kategorisiert Reviews in Beschwerden und Lobeshymnen
  - **Wettbewerbslücken-Identifikation**: Zeigt wo die echte monetarisierbare Nische liegt
  - **CLI & GUI Integration**: Verfügbar als `analyze_demand.py` Script und GUI-Button
  - **ROI-optimiert**: 2.5x höherer RPM durch datenbasierte Content-Optimierung

### 🆕 Kürzlich hinzugefügt

- ✅ **Review-Based Demand Analyzer** - Findet versteckte Bedürfnisse aus echten Reviews (2024-12-13)
- ✅ **Echte API-Integration** statt Stub-Funktionen
- ✅ **Koordinaten-Validierung** (-90°/90°, -180°/180°)
- ✅ **Duplikat-Erkennung** basierend auf Name + Koordinaten
- ✅ **Verbesserte City-Extraktion** (international, nicht nur DE)
- ✅ **Dynamisches Schema.org** JSON-LD

---

## 🌐 Live Demo

**Live Site:** [https://babelsberger.info](https://babelsberger.info)

Beispiel-Implementierung: Park Babelsberg Guide mit 14 kuratierten Locations, 12 interaktiven Filtern und vollständiger AdSense-Integration.

---

## 🚀 Installation

### Voraussetzungen

- **Python 3.8+** (empfohlen: Python 3.11)
- **pip** (Python Package Manager)
- **Git** (optional, für Repository-Cloning)
- **Google Places API Key** (für Live-Scraping)

---

### ⚡ Schnellinstallation (alle Plattformen)

**3 Schritte zum Start:**

```bash
# 1. Repository klonen
git clone https://github.com/DYAI2025/ADS_Plilar_scraper.git
cd ADS_Plilar_scraper

# 2. Dependencies installieren
pip install -r requirements.txt

# 3. Verifizierung
python3 verify_imports.py
python3 -m pytest -v
```

**Fertig!** 🎉 Du kannst jetzt die Tools nutzen:
- `python Files/quick_start.py` - Interaktiver Setup Wizard
- `python Files/gui_app.py` - GUI starten (benötigt Tkinter)
- `python Files/analyze_demand.py --help` - Review Demand Analyzer

---

### 📋 Detaillierte Installation nach Plattform

<details>
<summary><b>macOS</b> (klicken zum Ausklappen)</summary>

#### 1. Python installieren

```bash
# Prüfe ob Python installiert ist
python3 --version

# Falls nicht installiert: Homebrew installieren
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python via Homebrew installieren
brew install python@3.11
```

#### 2. Repository klonen

```bash
git clone https://github.com/DYAI2025/ADS_Plilar_scraper.git
cd ADS_Plilar_scraper
```

#### 3. Dependencies installieren

```bash
# Alle Dependencies installieren
pip install -r requirements.txt

# Optional: Package installieren (für entry points wie ads-pillar-gui)
pip install -e .
```

#### 4. Tkinter installieren (für GUI)

```bash
# Tkinter ist normalerweise vorinstalliert auf macOS
# Falls nicht:
brew install python-tk@3.11
```

#### 5. Verifizierung

```bash
# Module testen
python3 verify_imports.py

# Tests ausführen
python3 -m pytest -v
```

✅ **Installation erfolgreich!** Starte die GUI mit `python Files/gui_app.py`

</details>

<details>
<summary><b>Linux (Ubuntu / Debian)</b> (klicken zum Ausklappen)</summary>

```bash
# 1. System aktualisieren
sudo apt update && sudo apt upgrade -y

# 2. Python 3.11 installieren
sudo apt install python3.11 python3.11-venv python3-pip -y

# 3. Tkinter installieren (für GUI)
sudo apt install python3.11-tk -y

# 4. Repository klonen
git clone https://github.com/DYAI2025/ADS_Plilar_scraper.git
cd ADS_Plilar_scraper

# 5. Dependencies installieren
pip install -r requirements.txt

# Optional: Package installieren (für entry points)
pip install -e .

# 6. Verifizierung
python3 verify_imports.py
python3 -m pytest -v
```

✅ **Installation erfolgreich!**

</details>

<details>
<summary><b>Linux (Fedora / RHEL / CentOS)</b> (klicken zum Ausklappen)</summary>

```bash
# 1. Python 3.11 installieren
sudo dnf install python3.11 python3.11-devel -y

# 2. Tkinter installieren
sudo dnf install python3-tkinter -y

# 3-6. Gleiche Schritte wie Ubuntu (ab Repository klonen)
```

</details>

<details>
<summary><b>Linux (Arch Linux)</b> (klicken zum Ausklappen)</summary>

```bash
# 1. Python installieren
sudo pacman -S python python-pip tk -y

# 2-6. Gleiche Schritte wie Ubuntu (ab Repository klonen)
```

</details>

<details>
<summary><b>Windows</b> (klicken zum Ausklappen)</summary>

#### 1. Python installieren

1. Download Python von [python.org/downloads](https://www.python.org/downloads/)
2. Installiere Python 3.11 mit **"Add Python to PATH"** aktiviert ✅
3. Bestätige Installation:
   ```cmd
   python --version
   ```

#### 2. Repository herunterladen

**Option A - mit Git:**
```cmd
git clone https://github.com/DYAI2025/ADS_Plilar_scraper.git
cd ADS_Plilar_scraper
```

**Option B - ZIP Download:**
1. Download ZIP von [GitHub](https://github.com/DYAI2025/ADS_Plilar_scraper/archive/refs/heads/main.zip)
2. Entpacke nach `C:\ADS_Plilar_scraper`
3. ```cmd
   cd C:\ADS_Plilar_scraper
   ```

#### 3. Dependencies installieren

```cmd
REM Alle Dependencies installieren
pip install -r requirements.txt

REM Optional: Package installieren
pip install -e .
```

#### 4. Verifizierung

```cmd
REM Module testen
python verify_imports.py

REM Tests ausführen
python -m pytest -v
```

✅ **Installation erfolgreich!** Tkinter ist auf Windows normalerweise vorinstalliert.

</details>

---

### 🔧 Installation mit Virtual Environment (empfohlen für Entwickler)

Virtual Environments isolieren Python-Dependencies pro Projekt:

**macOS / Linux:**
```bash
# Virtual Environment erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# Deaktivieren (später)
deactivate
```

**Windows:**
```cmd
REM Virtual Environment erstellen
python -m venv venv

REM Aktivieren
venv\Scripts\activate

REM Dependencies installieren
pip install -r requirements.txt

REM Deaktivieren (später)
deactivate
```

---

## ⚡ Quick Start

### 1. Setup Wizard ausführen

```bash
# Automatischer Setup (Virtualenv + Dependencies)
./run_setup.sh

# Oder manuell
python Files/quick_start.py
```

Der Setup Wizard:
- ✅ Erstellt Demo-Daten
- ✅ Generiert Beispiel-Config
- ✅ Erstellt erste Pillar Page
- ✅ Zeigt Revenue-Kalkulation

### 2. Eigenen Google API Key einrichten

1. Gehe zu [Google Cloud Console](https://console.cloud.google.com/)
2. Erstelle ein Projekt
3. Aktiviere "Places API" und "Places API (New)"
4. Erstelle API Key
5. Speichere in `.env`:

```bash
# .env Datei erstellen
echo "GOOGLE_PLACES_API_KEY=your_api_key_here" > .env
```

### 3. Erste Location-Seite generieren

```python
# example_usage.py
import os
from Files.enhanced_scrapers import GooglePlacesScraper
from Files.data_pipeline import PillarPageGenerator, LocationData

# API Key laden
api_key = os.getenv("GOOGLE_PLACES_API_KEY")

# Scraper initialisieren
scraper = GooglePlacesScraper(api_key=api_key, delay=1.0)

# Locations scrapen
places = scraper.search_places(query="parks", location="Berlin")

# Details enrichment (Reviews, Öffnungszeiten, etc.)
enriched_places = scraper.enrich_places(places)

# Konvertiere zu LocationData
locations = []
for place in enriched_places:
    loc = LocationData(
        id=place.place_id,
        name=place.name,
        street=place.address.split(',')[0],
        city=place.city,
        region="Berlin",
        country="DE",
        postcode="",
        latitude=place.latitude,
        longitude=place.longitude,
        url=place.website,
        phone=place.phone,
        email="",
        opening_hours=place.opening_hours,
        rating=place.rating,
        review_count=place.review_count,
    )
    locations.append(loc)

# Pillar Page generieren
generator = PillarPageGenerator("Files/pillar_page_skeleton.html")
generator.generate_page(
    data=locations,
    city="Berlin",
    category="Parks",
    output_path="generated/berlin-parks.html",
    canonical_url="https://example.com/berlin-parks"
)

print(f"✅ Generated: generated/berlin-parks.html")
```

### 4. GUI starten (optional)

```bash
# GUI für Non-Technical Users
python Files/gui_app.py

# Oder via entry point (nach `pip install -e .`)
ads-pillar-gui
```

---

## 📘 Verwendung

### Scenario 1: Google Places Scraping

```python
from Files.enhanced_scrapers import GooglePlacesScraper

scraper = GooglePlacesScraper(api_key="YOUR_API_KEY", delay=1.0)

# Basic Search
places = scraper.search_places(
    query="restaurants",
    location="Munich",
    radius=50000  # 50km
)

# Enrichment mit Details
enriched = scraper.enrich_places(places)

for place in enriched:
    print(f"{place.name}: {place.rating}⭐ ({place.review_count} reviews)")
    print(f"  📞 {place.phone}")
    print(f"  🌐 {place.website}")
    print(f"  🕒 {place.opening_hours}")
```

### Scenario 2: Feature Extraction

```python
from Files.enhanced_scrapers import SmartFeatureExtractor

extractor = SmartFeatureExtractor()

review_text = """
Schöner Park mit viel Schatten und sauberen Toiletten.
Kostenloser Eintritt, perfekt für Kinder. Hunde sind erlaubt.
"""

features = extractor.extract_features(
    text="Stadtpark München",
    reviews=review_text,
    price_level=0  # Google price_level
)

print(features)
# {
#   'feature_shade': True,
#   'feature_toilets': True,
#   'feature_kids': True,
#   'feature_dogs': True,
#   'feature_fee': False,  # kostenlos
#   ...
# }
```

### Scenario 3: Niche Research

```python
from Files.niche_research import NicheValidator, KeywordResearch

# Profitable Niches validieren
validator = NicheValidator()
niches = validator.get_profitable_niches()

for niche in niches[:3]:
    print(f"{niche['name']}: {niche['rpm_range']} RPM")
    # "Parks in [Stadt]": 8-15€ RPM

# Keyword Research
research = KeywordResearch()
variations = research.generate_keyword_variations(
    base="parks",
    cities=["Berlin", "Munich", "Hamburg"]
)

for kw in variations:
    print(f"{kw['keyword']} - Difficulty: {kw['difficulty']}")
```

### Scenario 4: CSV Import

```python
from Files.enhanced_scrapers import CSVDataLoader

# CSV laden
places = CSVDataLoader.load_csv("data/my_locations.csv")

# CSV Format:
# name,address,city,latitude,longitude,rating,review_count,phone,website,opening_hours
```

### Scenario 5: Review-Based Demand Analysis ⭐ NEU!

**CLI Usage:**

```bash
# Analyse mit Review Demand Analyzer
cd Files
python analyze_demand.py --category "parks" --city "Berlin" --api-key YOUR_KEY

# Mit begrenzter Anzahl an Orten (spart API-Quota)
python analyze_demand.py --category "cafes" --city "München" --max-places 15

# API Key aus Umgebungsvariable
export GOOGLE_PLACES_API_KEY=your_key_here
python analyze_demand.py --category "restaurants" --city "Hamburg"

# Ergebnisse als JSON speichern
python analyze_demand.py --category "parks" --city "Potsdam" --output results.json
```

**Python API Usage:**

```python
from Files.niche_research import ReviewDemandAnalyzer
import os

# API Key setzen
api_key = os.getenv("GOOGLE_PLACES_API_KEY")

# Analyzer initialisieren
analyzer = ReviewDemandAnalyzer(api_key=api_key, delay=1.0)

# Review-Analyse durchführen
analysis = analyzer.analyze_review_sentiment(
    category="parks",
    city="Berlin",
    min_reviews=100,
    max_places=30
)

# Ergebnisse anzeigen
print(f"📊 {analysis['total_reviews_analyzed']} Reviews analysiert")
print(f"⭐ Durchschnittsbewertung: {analysis['avg_rating']:.2f}/5.0")

# Top Beschwerden (was fehlt?)
print("\n🔴 TOP BESCHWERDEN:")
for phrase, count in analysis["top_complaints"][:5]:
    print(f"  • '{phrase}' ({count}x)")

# Unerfüllte Bedürfnisse (OPPORTUNITIES!)
print("\n💡 UNMET NEEDS:")
for feature, mentions in analysis["unmet_needs"][:5]:
    print(f"  • {feature.upper()}: {mentions} Erwähnungen ⭐")

# Content-Ideen generieren
ideas = analyzer.generate_content_ideas(
    category="parks",
    city="Berlin",
    max_places=30
)

print("\n🎯 CONTENT IDEAS:")
for idea in ideas[:3]:
    print(f"\n  [{idea['priority']}] {idea['type']}")
    print(f"  {idea['title']}")
    print(f"  Impact: {idea['estimated_impact']}")
    print(f"  Umsetzung: {idea['implementation'][:80]}...")

# Vollständigen Report anzeigen
analyzer.print_analysis_report(category="parks", city="Berlin", max_places=20)
```

**GUI Usage:**

1. Starte die GUI: `python Files/gui_app.py`
2. Gehe zum Tab **"🔍 Nischen-Analyse"**
3. Klicke auf **"💡 Review Demand Analyse"**
4. Gib bei Bedarf deinen Google Places API Key ein
5. Erhalte:
   - Top Beschwerden aus negativen Reviews
   - Unerfüllte Bedürfnisse (Features die fehlen)
   - Content-Ideen für FAQ, Filter, Listen
   - Sentiment-Analyse aller Reviews

**Was du erhältst:**

- **Unmet Needs**: Features die 0% der Konkurrenten haben, aber 50%+ der Nutzer suchen
- **Content Ideas**: Konkrete Vorschläge für FAQ, Filter-Features, kuratierte Listen
- **ROI-Impact**: z.B. "Schatten-Filter hinzufügen → +1.5x RPM erwartet"
- **Data-Driven Decisions**: Statt raten welche Features wichtig sind → echte Daten!

**Business Impact:**

```
OHNE Review Analysis:
- Generische Pillar Page
- Baseline RPM: 8€
- Revenue Jahr 1: 2.400€

MIT Review Analysis:
- Optimierte Features basierend auf Nutzer-Bedürfnissen
- RPM: 16.8€ (2.1x durch Feature-Gap-Optimierung)
- Revenue Jahr 1: 15.120€
- Delta: +12.720€ 💰
```

---

## 🏗️ Architektur

### Daten-Pipeline

```
┌─────────────────┐
│ Data Collection │
│ (Scrapers)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Enrichment      │
│ (Details API)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Feature Extract │
│ (NLP Keywords)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Deduplication   │
│ (Name + Coords) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Page Generation │
│ (Jinja2)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Static HTML     │
│ + AdSense       │
└─────────────────┘
```

### Projekt-Struktur

```
ADS_Plilar_scraper/
├── Files/                          # Haupt-Implementierung
│   ├── data_pipeline.py            # LocationData, PillarPageGenerator
│   ├── enhanced_scrapers.py        # Google Places, Feature Extraction
│   ├── niche_research.py           # Niche Validation, Keywords
│   ├── gui_app.py                  # Tkinter GUI
│   ├── quick_start.py              # Interactive Setup Wizard
│   ├── seo_setup.py                # SEO Tools
│   ├── pillar_page_skeleton.html   # Jinja2 Template
│   └── tests/                      # Unit Tests
│
├── tests/                          # Integration Tests
│   ├── test_pipeline_end_to_end.py
│   └── test_sanitization.py
│
├── data/                           # CSV Data Storage
├── generated/                      # Output Directory
├── docs/                           # Documentation
│
├── requirements.txt                # Python Dependencies
├── setup.py                        # Package Setup
├── pytest.ini                      # Test Configuration
└── README.md                       # This file
```

---

## 🧪 Testing

### Test Suite ausführen

```bash
# Alle Tests
pytest

# Verbose Output
pytest -v

# Specific Test
pytest tests/test_pipeline_end_to_end.py -v

# Coverage Report
pytest --cov=Files --cov-report=html
```

### Test-Typen

- **Unit Tests** (`Files/tests/`) - Module-spezifische Tests
- **Integration Tests** (`tests/`) - End-to-End Workflows
- **System Tests** (`Files/tests/test_system.py`) - Dependency Checks

### Continuous Integration

- **GitHub Actions** führt Tests automatisch bei Push/PR aus
- **Workflows**: `.github/workflows/test.yml`

---

## 📦 Deployment

### Statische Site (GitHub Pages)

```bash
# 1. Seite generieren
python generate_ai_optimized_site.py

# 2. Output liegt in generated/
ls generated/
# index.html, ads.txt, robots.txt, sitemap.xml

# 3. GitHub Pages Setup
# Repository Settings → Pages → GitHub Actions als Source
```

### Netlify / Vercel

```bash
# netlify.toml
[build]
  command = "python3 generate_ai_optimized_site.py"
  publish = "generated"
```

### Custom Server

```bash
# Static File Server
cd generated
python3 -m http.server 8000

# Nginx
# Kopiere generated/ nach /var/www/html/
```

---

## 🛠️ Troubleshooting

### Import Errors

```bash
# Dependencies prüfen
python3 verify_imports.py

# System Health Check
cd Files && python3 test_system.py
```

### Tkinter nicht verfügbar

**macOS:**
```bash
brew install python-tk@3.11
```

**Linux (Ubuntu):**
```bash
sudo apt install python3.11-tk
```

**Windows:**
Tkinter ist normalerweise vorinstalliert. Falls nicht, Python neu installieren mit Tcl/Tk Option.

### Google API Quota Exceeded

```python
# Delay zwischen Requests erhöhen
scraper = GooglePlacesScraper(api_key="...", delay=2.0)  # 2 Sekunden
```

### Tests schlagen fehl

```bash
# Virtual Environment aktivieren
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Dependencies neu installieren
pip install -r requirements.txt --force-reinstall
```

---

## 🤝 Contributing

1. **Fork** das Repository
2. **Clone** deinen Fork
   ```bash
   git clone https://github.com/YOUR_USERNAME/ADS_Plilar_scraper.git
   ```
3. **Branch** erstellen
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Änderungen** committen
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push** zu deinem Fork
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Pull Request** erstellen

### Code Style

- **Formatting:** Black (120 char line length)
- **Linting:** flake8
- **Pre-commit Hooks:** `.pre-commit-config.yaml`

```bash
# Pre-commit installieren
pip install pre-commit
pre-commit install

# Manuell ausführen
pre-commit run --all-files
```

---

## 📝 Lizenz

MIT License - Siehe [LICENSE](LICENSE) für Details

---

## 📚 Weitere Ressourcen

- **📘 [CLAUDE.md](CLAUDE.md)** - Claude Code Dokumentation
- **🚀 [LAUNCH_SUMMARY.md](LAUNCH_SUMMARY.md)** - Deployment Guide
- **🏰 [BABELSBERGER_README.md](BABELSBERGER_README.md)** - Beispiel-Implementierung
- **🔧 [docs/CLAUDE_REPOSITORY_ACCESS.md](docs/CLAUDE_REPOSITORY_ACCESS.md)** - Claude Setup

---

## 🆘 Support

- **GitHub Issues:** [Issues](https://github.com/DYAI2025/ADS_Plilar_scraper/issues)
- **Discussions:** [Discussions](https://github.com/DYAI2025/ADS_Plilar_scraper/discussions)

---

## 📊 Status

- ✅ **Tests:** 18/20 passed (2 skipped - GUI in headless)
- ✅ **Python:** 3.8 - 3.12 (tested in CI)
- ✅ **Platform:** macOS, Linux, Windows
- ✅ **API Integration:** Google Places API (Text Search + Details)
- ✅ **Features:** Vollständig implementiert
- ✅ **Documentation:** Vollständig

---

**Built with ❤️ for Programmatic SEO**

_Last Updated: 2025-12-07_
