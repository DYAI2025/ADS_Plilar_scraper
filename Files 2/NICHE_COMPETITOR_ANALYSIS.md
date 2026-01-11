# Nischen-Konkurrenzanalyse - Dokumentation

## Überblick

Die **Nischen-Konkurrenzanalyse** ist eine neue Funktion des ADS Pillar Scrapers, die es ermöglicht:

✅ **Bilinguales Keyword-Matching** (Deutsch & Englisch)
✅ **Konkurrenz-Identifikation** in der Zielregion
✅ **Google-Sichtbarkeits-Schätzung** (SERP Position, Visibility Score)
✅ **Traffic- und Umsatz-Prognosen** (basierend auf Marktdaten)
✅ **Opportunity Scoring** (0-100) zur Bewertung der Nischen-Attraktivität

---

## Features

### 1. Bilinguales Freitextfeld für Zielgruppe/Nische

Der User kann seine Nische in **Deutsch oder Englisch** als Freitext eingeben:

**Beispiele:**
- `Hundeparks mit Agility-Parcours`
- `Coworking Cafés mit schnellem WiFi`
- `Outdoor Spielplätze für Kleinkinder`
- `Dog parks with agility courses`
- `Coworking spaces with fast WiFi`

Das System generiert automatisch **mehrere Suchvariationen** in beiden Sprachen.

### 2. Konkurrenten-Identifikation

Die Analyse findet automatisch:
- **Direkte Konkurrenten** (gleiche Nische, gleicher Standort)
- **Google-Ratings** und Review-Anzahl
- **Geschätzte SERP-Positionen** (Ranking in Google-Suchergebnissen)
- **Domain-Authority** und Competitive Strength

### 3. Google-Sichtbarkeit & Traffic-Schätzung

Für jeden Konkurrenten wird geschätzt:

| Metrik | Berechnung |
|--------|-----------|
| **Visibility Score** | Rating (50%) + Review Count (50%) |
| **Monthly Visitors** | Review Count × 150 (Durchschnitt) |
| **SERP Position** | Basierend auf Competitive Strength |
| **Monthly Revenue** | (Visitors / 1000) × RPM × Position Factor |

### 4. Umsatz-Prognosen (RPM-Szenarien)

Das System berechnet **3 Umsatz-Szenarien**:

| Szenario | RPM | Beschreibung |
|----------|-----|--------------|
| **Konservativ** | €8 | Pessimistisches Szenario |
| **Realistisch** | €15 | Durchschnittlicher AdSense RPM |
| **Optimistisch** | €25 | Beste Nischen mit hoher CTR |

**Formel:**
`Monatlicher Umsatz = (Geschätzte Besucher / 1000) × RPM`

### 5. Opportunity Score (0-100)

Der **Opportunity Score** bewertet die Nischen-Attraktivität:

| Score | Bewertung | Bedeutung |
|-------|-----------|-----------|
| **70-100** | 🟢 Excellent | Wenig Konkurrenz, hohe Chance |
| **50-69** | 🟡 Moderate | Mittlere Konkurrenz, Differenzierung nötig |
| **0-49** | 🔴 High Competition | Starke Konkurrenz, schwierige Nische |

**Berechnung:**
- ✅ Weniger Konkurrenten (+20 Punkte)
- ✅ Niedrigere Durchschnitts-Ratings (+15 Punkte)
- ✅ Geringe Marktsättigung (+20 Punkte)
- ✅ Hohes Suchvolumen (+15 Punkte)

---

## Installation & Setup

### 1. Abhängigkeiten installieren

```bash
cd "Files 2"
pip install requests pandas
```

### 2. Google Places API Key (Optional)

Für **echte Daten** benötigen Sie einen Google Places API Key:

1. Besuchen Sie: https://console.cloud.google.com/
2. Aktivieren Sie "Places API"
3. Erstellen Sie einen API Key
4. Setzen Sie Environment Variable:

```bash
export GOOGLE_PLACES_API_KEY="your-api-key-here"
```

**Ohne API Key:** System nutzt Schätzungen (immer noch sehr nützlich!)

---

## Verwendung

### Methode 1: Interaktiver Modus

```bash
python niche_scraper_workflow.py --interactive
```

Das System fragt Sie nach:
- ✏️ **Ziel-Nische** (Freitext, DE/EN)
- 📍 **Standort** (Stadt/Region)
- 🌐 **Sprache** (de/en/both)
- 📏 **Suchradius** (in km)
- 🔑 **API Key** (optional)

### Methode 2: Command-Line Argumente

```bash
python niche_scraper_workflow.py \
  --niche "Hundeparks mit Agility" \
  --location "Berlin" \
  --language both \
  --radius 10 \
  --output results/
```

**Mit Google API Key:**

```bash
python niche_scraper_workflow.py \
  --niche "Coworking Cafés" \
  --location "München" \
  --api-key "YOUR_API_KEY" \
  --output results/
```

### Methode 3: Python-Integration

```python
from competitor_analysis import NicheCompetitorAnalyzer

# Analyzer erstellen
analyzer = NicheCompetitorAnalyzer(
    google_api_key="YOUR_API_KEY"  # Optional
)

# Analyse durchführen
result = analyzer.analyze_niche_competition(
    target_niche="Hundeparks mit Wasser",
    location="Berlin",
    radius_km=10.0,
    language="both"
)

# Ergebnisse anzeigen
print(f"Opportunity Score: {result.opportunity_score}/100")
print(f"Konkurrenten: {result.total_competitors_found}")
print(f"Umsatzpotenzial: €{result.estimated_monthly_revenue[1]:.2f}/Monat")

# Report exportieren
analyzer.export_analysis_report(result, "analysis_report.txt")
```

---

## Ausgabe-Formate

### 1. CSV-Export

**Datei:** `niche_data_<location>.csv`

Enthält:
- Alle Konkurrenten mit Metriken
- Gescrapete Locations (wenn API Key vorhanden)
- Combined Data für weitere Analysen

**Spalten:**
```
source, name, rating, review_count, estimated_monthly_visitors,
estimated_monthly_revenue, visibility_score, competitive_strength,
serp_position, domain, address, city, latitude, longitude, ...
```

### 2. JSON-Export

**Datei:** `niche_data_<location>.json`

Strukturierte Daten für Weiterverarbeitung:

```json
{
  "source": "competitor_analysis",
  "name": "Hundeparadies Berlin",
  "rating": 4.5,
  "review_count": 234,
  "estimated_monthly_visitors": 35100,
  "estimated_monthly_revenue": 526.50,
  "visibility_score": 85.3,
  "competitive_strength": "High",
  "serp_position": 2
}
```

### 3. Text-Report

**Datei:** `competitor_analysis_<location>.txt`

Detaillierter Analyse-Report mit:
- ✅ Marktübersicht
- ✅ Umsatzpotenzial (3 Szenarien)
- ✅ Opportunity Score
- ✅ Konkurrenten-Liste (Top 10)
- ✅ Empfehlungen

**Beispiel:**

```
======================================================================
NISCHEN-KONKURRENZANALYSE
======================================================================

Ziel-Nische: Hundeparks mit Agility
Standort: Berlin

MARKTÜBERSICHT
----------------------------------------------------------------------
Anzahl Konkurrenten: 12
Durchschn. Rating: 4.2/5.0
Marktsättigung: Medium
Geschätzte monatl. Suchanfragen: 3,400

UMSATZPOTENZIAL (Monatlich)
----------------------------------------------------------------------
Konservativ (RPM €8):  €127.20
Realistisch (RPM €15): €238.50
Optimistisch (RPM €25): €397.50

OPPORTUNITY SCORE: 62.5/100

EMPFEHLUNGEN
----------------------------------------------------------------------
🟡 Moderate opportunity. Focus on differentiation and quality.
Add unique features or filters not available on competitor sites.
Collect 30-50 locations with detailed features for best SERP performance.
```

---

## Integration mit bestehenden Tools

### Mit Enhanced Scrapers

```python
from enhanced_scrapers import UniversalScraper
from competitor_analysis import NicheCompetitorAnalyzer

# 1. Konkurrenzanalyse
analyzer = NicheCompetitorAnalyzer()
comp_analysis = analyzer.analyze_niche_competition(
    target_niche="Parks",
    location="Berlin"
)

# 2. Locations scrapen
scraper_config = {
    "google_api_key": "YOUR_KEY",
    "delay": 1.5
}
scraper = UniversalScraper(scraper_config)
places = scraper.collect_all_data("parks", "Berlin")

# 3. Kombinierte Ausgabe
import pandas as pd
df = pd.DataFrame(places)
df.to_csv("berlin_parks_with_competition.csv")
```

### Mit Data Pipeline

```python
from data_pipeline import PillarPageGenerator, LocationData
from competitor_analysis import NicheCompetitorAnalyzer

# Analyse durchführen
analyzer = NicheCompetitorAnalyzer()
analysis = analyzer.analyze_niche_competition("Parks", "Berlin")

# LocationData aus Konkurrenten erstellen
locations = [
    LocationData(
        id=f"comp_{i}",
        name=comp.name,
        city="Berlin",
        rating=comp.rating,
        review_count=comp.review_count,
        # ... weitere Felder
    )
    for i, comp in enumerate(analysis.competitors[:20])
]

# Pillar Page generieren
generator = PillarPageGenerator()
generator.generate_page(
    data=locations,
    city="Berlin",
    category="Parks",
    output_path="berlin_parks.html",
    canonical_url="https://example.com/berlin-parks"
)
```

---

## Beispiele

### Beispiel 1: Hundeparks in Berlin

```bash
python niche_scraper_workflow.py \
  --niche "Hundeparks" \
  --location "Berlin" \
  --language both
```

**Ergebnis:**
- 12 Konkurrenten gefunden
- Opportunity Score: 62.5/100
- Geschätzter Umsatz: €238.50/Monat (realistisch)
- Empfehlung: Moderate Konkurrenz, Fokus auf Differenzierung

### Beispiel 2: Coworking Cafés in München

```bash
python niche_scraper_workflow.py \
  --niche "Coworking Cafés mit schnellem WiFi" \
  --location "München" \
  --language de
```

**Ergebnis:**
- 8 Konkurrenten gefunden
- Opportunity Score: 71.3/100
- Geschätzter Umsatz: €412.80/Monat (realistisch)
- Empfehlung: Excellent opportunity!

### Beispiel 3: Spielplätze in Hamburg

```bash
python niche_scraper_workflow.py \
  --niche "Outdoor Spielplätze für Kleinkinder" \
  --location "Hamburg" \
  --language both \
  --api-key "YOUR_KEY"
```

**Mit API Key:**
- 23 echte Locations gescraped
- 15 Konkurrenten analysiert
- Vollständige Daten (Phone, Website, Opening Hours)

---

## Best Practices

### 1. Nischen-Auswahl

✅ **Gute Nischen:**
- Spezifisch: "Hundeparks mit Agility-Parcours"
- Lokalisiert: "Berlin Mitte"
- Feature-fokussiert: "mit Wasser", "mit WiFi"

❌ **Schlechte Nischen:**
- Zu breit: "Restaurants"
- Zu generisch: "Sport"
- Keine Lokalisierung: "Parks weltweit"

### 2. Sprach-Einstellungen

- **`both`**: Maximum Coverage (empfohlen für DE)
- **`de`**: Nur deutsche Suchen
- **`en`**: Nur englische Suchen (für internationale Standorte)

### 3. Radius-Optimierung

| Standort-Typ | Empfohlener Radius |
|--------------|-------------------|
| Großstadt (Berlin, München) | 5-10 km |
| Mittelstadt | 15-20 km |
| Kleinstadt | 25-30 km |
| Ländliche Region | 40-50 km |

### 4. API-Nutzung

**Ohne API Key:**
- ✅ Schnelle Marktanalyse
- ✅ Opportunity Scoring
- ✅ Konkurrenz-Schätzungen
- ❌ Keine echten Location-Daten

**Mit API Key:**
- ✅ Echte Google Places Daten
- ✅ Phone, Website, Opening Hours
- ✅ Präzise Ratings & Reviews
- ⚠️ API-Kosten beachten!

---

## FAQ

### Wie genau sind die Umsatz-Schätzungen?

Die Schätzungen basieren auf **realistischen AdSense-RPMs** (€8-€25) und Branchen-Durchschnitten. Sie sind **Richtwerte** und können je nach:
- Nischen-Qualität
- Content-Optimierung
- AdSense-Platzierung
- Saisonalität

um ±30% variieren.

### Brauche ich einen Google API Key?

**Nein!** Der Analyzer funktioniert auch ohne API Key mit **Schätzungen**. Diese sind für erste Marktanalysen völlig ausreichend.

**Aber:** Mit API Key erhalten Sie **echte Daten** und können direkt scrapen.

### Welche Sprachen werden unterstützt?

Aktuell: **Deutsch** und **Englisch**

Das System generiert automatisch bilinguale Suchvariationen für maximale Coverage.

### Wie oft sollte ich die Analyse durchführen?

- **Initial:** Vor Projektstart
- **Monatlich:** Zur Konkurrenz-Überwachung
- **Quartalsweise:** Für Markt-Trends

### Kann ich die Daten in Excel öffnen?

Ja! Die CSV-Exporte lassen sich direkt in Excel, Google Sheets oder LibreOffice öffnen.

---

## Troubleshooting

### Error: "Import error - make sure you're in the 'Files 2' directory"

**Lösung:**
```bash
cd "Files 2"
python niche_scraper_workflow.py --interactive
```

### API Key funktioniert nicht

**Prüfen Sie:**
1. Places API in Google Console aktiviert?
2. API Key korrekt kopiert? (keine Leerzeichen)
3. Billing aktiviert? (Google benötigt Zahlungsmethode)

### Zu wenige Konkurrenten gefunden

**Mögliche Ursachen:**
- Nische zu spezifisch
- Standort zu klein
- Radius zu gering

**Lösungen:**
- Radius erhöhen: `--radius 20`
- Nische verallgemeinern
- Mehrere Städte kombinieren

---

## Erweiterungen & Roadmap

### Geplante Features

- [ ] Mehrsprachigkeit (FR, IT, ES)
- [ ] SERP-Scraping (echte Google-Positionen)
- [ ] Backlink-Analyse (Domain Authority)
- [ ] Sentiment-Analyse (Review-Text-Mining)
- [ ] Automatische Content-Gaps-Erkennung
- [ ] Integration mit SEO-Tools (Ahrefs, SEMrush)

### Beitragen

Feedback und Pull Requests willkommen!

---

## Lizenz & Credits

Teil des **ADS Pillar Scraper** Projekts.

Entwickelt für automatisierte Local SEO und AdSense-Monetarisierung.
