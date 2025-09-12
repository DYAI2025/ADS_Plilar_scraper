# ADS Pillar - README

## 🎯 Über das Projekt

**ADS Pillar** ist ein System für Programmatic-SEO mit AdSense-Monetarisierung. Das Konzept: Du erstellst kuratierte Verzeichnisse für lokale Orte/Dienstleistungen, optimierst sie für Suchmaschinen und monetarisierst über Google AdSense.

### Kernprinzip

- **Syntaktisch gleiche Suchanfragen** ("Parks in Berlin", "Parks München", etc.)
- **Semantisch unterschiedliche Intentionen** (Schatten, Spielplätze, Hunde, Sport)
- **Eine Pillar-Seite** bedient alle Intentionen mit Filtern
- **AdSense-Anzeigen** monetarisieren den Traffic

## 📁 Datei-Übersicht

### Vorlagen & Templates

- `pillar_page_skeleton.html` - HTML-Template für Pillar-Seiten
- `directory_facets_template.csv` - Datenstruktur für Locations
- `ads.txt` - AdSense-Autorisierung

### Python-Tools

- `data_pipeline.py` - Datensammlung und Seiten-Generierung
- `niche_research.py` - Nischen-Analyse und Keyword-Research
- `seo_setup.py` - SEO und Analytics Setup

### Dokumentation

- `adsense_policy_checklist.md` - AdSense-Compliance Guide
- `revenue_model.csv` - Umsatz-Szenarien nach Pageviews/RPM

## 🚀 Quick Start (5 Minuten)

### 1. Nische analysieren

```bash
python niche_research.py
```

Gibt dir Top-Nischen mit Opportunity-Score und Keywords.

### 2. Projekt aufsetzen

```bash
python seo_setup.py
```

Erstellt alle SEO-Files (robots.txt, sitemap.xml, etc.).

### 3. Daten sammeln

```python
# In data_pipeline.py anpassen:
scraper = DataScraper()
places = scraper.scrape_google_places("parks", "Berlin", "YOUR_API_KEY")
```

### 4. Seite generieren

```python
generator = PillarPageGenerator("pillar_page_skeleton.html")
generator.generate_page(data, "Berlin", "Parks", "berlin_parks.html", "https://domain.com/berlin-parks")
```

### 5. AdSense aktivieren

- AdSense-Konto erstellen
- Publisher-ID in HTML einsetzen
- `ads.txt` hochladen
- Auto-Ads aktivieren

## 💰 Revenue Model

Basiert auf **Page-RPM × Pageviews**:

| Pageviews/Monat | RPM 8€ | RPM 15€ | RPM 25€ |
| --------------- | ------ | ------- | ------- |
| 50.000          | 400€   | 750€    | 1.250€  |
| 100.000         | 800€   | 1.500€  | 2.500€  |
| 250.000         | 2.000€ | 3.750€  | 6.250€  |

**Realistic Ziele:**

- Monat 1: 10.000 Pageviews, 8€ RPM = 80€
- Monat 3: 50.000 Pageviews, 12€ RPM = 600€
- Monat 6: 150.000 Pageviews, 15€ RPM = 2.250€

## 🎯 Bewährte Nischen

### 1. Hundeparks

- **Keywords:** "hundepark berlin", "dog park munich"
- **Facetten:** Zaun, Wasser, Schatten, Größe, Agility
- **RPM:** 12-20€ (Haustier-Nische zahlt gut)

### 2. Arbeitsplätze & Cafés

- **Keywords:** "laptop cafe", "coworking", "wifi arbeitsplatz"
- **Facetten:** WIFI, Steckdosen, Lärmpegel, Öffnungszeiten
- **RPM:** 15-25€ (Business-Audience)

### 3. Sauna & Wellness

- **Keywords:** "sauna berlin", "kaltwasser spot"
- **Facetten:** Außenbereich, Ruheraum, Preise, Aufguss
- **RPM:** 18-30€ (Premium-Nische)

## 🔧 Technischer Stack

### Frontend

- Pure HTML/CSS/JavaScript (kein Framework nötig)
- Client-side Filtering für Interaktivität
- Mobile-first Design
- Schema.org JSON-LD für SEO

### Backend/Data

- Python für Scraping und Generierung
- CSV für Datenmanagement
- Google Places API (optional)
- Static Site Generation

### SEO & Analytics

- Google Search Console
- Google Analytics 4
- AdSense Auto Ads
- XML Sitemaps

## 📊 Monitoring & KPIs

### Tägliche Metriken

- **Pageviews** - Traffic-Entwicklung
- **Page RPM** - Monetarisierung pro 1000 Views
- **Ad Impressions** - Anzeigen-Performance
- **Invalid Traffic** - Compliance-Risiko

### Wöchentliche Reviews

- **Keyword Rankings** - SEO-Performance
- **Click-through Rate** - SERP-Performance
- **Session Duration** - User Engagement
- **Bounce Rate** - Content-Qualität

### Monatliche Optimierung

- **A/B Test Ad Positions** - RPM optimieren
- **Content Updates** - Aktualität sicherstellen
- **New Cities/Keywords** - Skalierung
- **Competitor Analysis** - Marktposition

## ⚠️ Wichtige Warnungen

### AdSense Compliance

- **Niemals** zum Klicken auf Anzeigen auffordern
- **Keine** irreführenden Ad-Platzierungen
- **DSGVO-konformes** Cookie-Management (EU)
- **Regelmäßige** Policy-Updates beachten

### SEO Risiken

- **Duplicate Content** bei Programmatic-Skalierung
- **Keyword Stuffing** vermeiden
- **Page Speed** trotz Ads optimieren
- **Mobile Usability** priorisieren

### Traffic Quality

- **Organischer Traffic** aus Google Search bevorzugen
- **Künstlicher Traffic** führt zu AdSense-Ban
- **High Bounce Rate** schadet Rankings
- **Session Duration** unter 30s problematisch

## 🔄 Skalierungs-Strategie

### Phase 1: MVP (Monat 1)

- 1 Stadt, 1 Kategorie
- 20-50 Locations
- 1 Pillar-Seite
- AdSense aktiviert

### Phase 2: Horizontal (Monat 2-3)

- 3-5 weitere Städte
- Gleiche Kategorie
- Template-basierte Generierung
- Interne Verlinkung

### Phase 3: Vertikal (Monat 4-6)

- Neue Kategorien in bestehenden Städten
- Cross-Verlinkung zwischen Kategorien
- Spezialisierte Landing Pages
- Premium-Content für höhere RPM

### Phase 4: Automation (Monat 6+)

- API-basierte Datenaktualisierung
- Automated Content Generation
- Multi-Language Expansion
- White-Label für andere Betreiber

## 📞 Support & Community

### Offizielle Ressourcen

- [AdSense Help Center](https://support.google.com/adsense)
- [Google Search Central](https://developers.google.com/search)
- [Schema.org Documentation](https://schema.org/LocalBusiness)

### Tools & APIs

- [Google Places API](https://developers.google.com/maps/documentation/places/web-service)
- [Ahrefs API](https://ahrefs.com/api) - Keyword Research
- [PageSpeed Insights](https://pagespeed.web.dev/) - Performance
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

## 🤝 Beitragen

1. Fork das Repository
2. Feature-Branch erstellen
3. Tests schreiben für neue Features
4. Pull Request mit Beschreibung erstellen

## 📄 Lizenz

MIT License - Nutze es kommerziell, aber auf eigene Verantwortung.

---

**💡 Pro-Tipp:** Start small, think big. Eine gut optimierte Pillar-Seite für eine Stadt kann bereits 1.000€+/Monat generieren. Skalierung folgt dann natürlich.

**🎯 Ziel:** Aufbau eines passiven Einkommens durch datengetriebene, SEO-optimierte Verzeichnisse mit minimaler laufender Pflege.
