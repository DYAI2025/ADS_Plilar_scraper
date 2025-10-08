# 🚀 ADS Pillar – Programmatic SEO Toolkit

> **ADS Pillar** bündelt Recherche, Datenaufbereitung und statische Site-Generierung in einem Workflow, um kuratierte Verzeichnisse für lokale Orte zu bauen und mit Google AdSense zu monetarisieren.

## Inhaltsverzeichnis
- [Projektüberblick](#projektüberblick)
- [Systemarchitektur](#systemarchitektur)
- [Kernfunktionen](#kernfunktionen)
  - [1. Orte analysieren & Daten beschaffen](#1-orte-analysieren--daten-beschaffen)
  - [2. Websites erstellen & anreichern](#2-websites-erstellen--anreichern)
  - [3. Release vorbereiten & hosten](#3-release-vorbereiten--hosten)
- [Quick Start](#quick-start)
- [Tests & Qualitätssicherung](#tests--qualitätssicherung)
- [Best Practices & Monetarisierung](#best-practices--monetarisierung)
- [Skalierungsfahrplan](#skalierungsfahrplan)
- [Ressourcen & Support](#ressourcen--support)
- [Mitwirken & Lizenz](#mitwirken--lizenz)

## Projektüberblick
- **Ziel**: Automatisiertes Erstellen von Pillar Pages für lokale Suchintentionen.
- **Monetarisierung**: Google AdSense (Auto Ads + individuelle Slots).
- **Output**: Host-fertige statische Websites (HTML, CSV-Daten, JSON-LD).

## Systemarchitektur
```mermaid
flowchart LR
    A[Nischenanalyse\n`niche_research.py`] --> B[Datenbeschaffung\n`enhanced_scrapers.py`]
    B --> C[Datenaufbereitung\n`data_pipeline.py`]
    C --> D[Seitengenerierung\n`pillar_page_skeleton.html`\n`PillarPageGenerator`]
    D --> E[Release Paket\n`generated/`]
    E --> F[Hosting\nCDN / Static Hosting]
    A -->|Insights| C
    B -->|CSV & JSON| C
```

## Kernfunktionen

### 1. Orte analysieren & Daten beschaffen
| Datei/Tool | Zweck | Highlights |
|------------|-------|------------|
| `niche_research.py` | Identifiziert lukrative Nischen & Keywords | Opportunity-Score, RPM-Schätzungen, Facettenvorschläge |
| `enhanced_scrapers.py` | Aggregiert Daten aus Google Places & anderen Quellen | Session-Reuse, Feature-Extraktion aus Reviews, Retry-Handling |
| `DataEnrichment` (in `data_pipeline.py`) | Wandelt Texte in strukturierte Merkmals-Flags um | Keyword-Mapping für Schatten, Wasser, Hunde, Gebühren etc. |

**Ablauf:**
1. Nische identifizieren → Keyword-Cluster mit Suchintentionen ableiten.
2. API-Keys (z. B. Google Places) hinterlegen.
3. Scraper starten – Daten werden als CSV/JSON gespeichert.

### 2. Websites erstellen & anreichern
| Datei/Tool | Zweck | Besonderheiten |
|------------|-------|----------------|
| `pillar_page_skeleton.html` | Responsives HTML-Template mit AdSense-Slots | Schema.org JSON-LD, Sticky Ads, Filter-UI |
| `data_pipeline.py` | Transformiert Location-Daten in Seiten | `PillarPageGenerator` erzeugt HTML inkl. JSON-Daten-Embed |
| `quick_start.py` | CLI-Assistent für Demo-Daten & Seiten | Erstellt Sample-CSV, Demo-HTML und Next-Step-Guides |
| `gui_app.py` | Tkinter-GUI für nicht-technische User | Revenue-Rechner, Datenimport, Seitenexport |

**Output-Formate:**
- `generated/` – fertige HTML-Seiten (Host-ready).
- `data/` – CSV-Dateien für weitere Bearbeitung oder QA.
- `project_overview.json` – Projekt-Metadaten.

### 3. Release vorbereiten & hosten
| Datei/Tool | Zweck | Inhalt |
|------------|-------|--------|
| `run_setup.sh` | Automatisiertes Setup (venv, Requirements) | Erstellt Virtualenv, installiert `requirements.txt` |
| `adsense_policy_checklist.md` | Compliance-Check vor Livegang | Policy-Hinweise & DSGVO-To-Dos |
| `Standard_Pillarpage.md` | Content-Richtlinien | Aufbau, Module, interne Verlinkung |
| `generated_site/` | Beispiel-Deployment-Struktur | Index-Seite, Assets, robots.txt |

**Release Steps:**
1. `./run_setup.sh` – Umgebung aufsetzen.
2. `python data_pipeline.py` – Daten laden und Seite generieren.
3. Ergebnis aus `generated/` auf Hosting-Anbieter (z. B. Netlify, Cloudflare Pages) deployen.
4. `ads.txt`, `robots.txt`, `sitemap.xml` hochladen.

## Quick Start
1. **Repo klonen & Setup**
   ```bash
   ./run_setup.sh
   ```
2. **Demo-Projekt anlegen**
   ```bash
   python quick_start.py
   ```
   - erzeugt `quick_config.json`
   - legt Beispieldaten in `data/` an
   - erstellt Demo-HTML in `generated/`
3. **Eigene Daten nutzen**
   ```python
   from data_pipeline import DataScraper, PillarPageGenerator
   ```
   - `DataScraper.scrape_google_places("parks", "Berlin", API_KEY)`
   - `PillarPageGenerator.generate_page(...)
4. **GUI starten (optional)**
   ```bash
   python gui_app.py
   ```

## Tests & Qualitätssicherung
| Testtyp | Datei | Beschreibung |
|---------|-------|--------------|
| Smoke-Test | `test_hello_world.py` | Prüft Pytest-Setup |
| End-to-End | `tests/test_quick_start_flow.py` | Erstellt Demo-Daten & HTML komplett durch Quick-Start-Helfer |
| Regression | `tests/test_pillar_page_regression.py` | Validiert dynamische Inhalte und Schema.org im generierten HTML |
| Setup/Dependencies | `tests/test_requirements_and_setup.py` | Stellt sicher, dass Setup-Skript & Requirements vollständig sind |
| GUI/Business-Logik | `tests/test_gui_revenue.py` | Testet Revenue-Berechnungen der GUI |

Ausführen:
```bash
cd Files
pytest
```

## Best Practices & Monetarisierung
- **AdSense**: Slots nicht zu dicht platzieren, invalid traffic vermeiden.
- **SEO**: Einzigartige Texte für jede Stadt/Kategorie, schnelle Ladezeiten (<2 s).
- **Tracking**: Google Analytics 4 + Search Console einbinden.
- **Content-Aktualität**: Regelmäßige Aktualisierung der CSV-Daten (API oder Scraper).

### Revenue-Szenarien
| Pageviews/Monat | RPM 8 € | RPM 15 € | RPM 25 € |
|-----------------|---------|----------|----------|
| 50.000 | 400 € | 750 € | 1.250 € |
| 100.000 | 800 € | 1.500 € | 2.500 € |
| 250.000 | 2.000 € | 3.750 € | 6.250 € |

## Skalierungsfahrplan
1. **MVP (Monat 1)** – eine Stadt, eine Kategorie, 20–50 Orte.
2. **Horizontal (Monat 2–3)** – weitere Städte, Template-Reuse, interne Verlinkung.
3. **Vertikal (Monat 4–6)** – neue Kategorien pro Stadt, thematische Silo-Struktur.
4. **Automation (Monat 6+)** – API-Updates, Multi-Language, White-Label.

## Ressourcen & Support
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

## 🔧 Troubleshooting

### Import Errors / GUI Shows "Missing Dependencies" Warning

If you see import errors or the GUI warns about missing modules:

```bash
pip install -r requirements.txt
```

Or use the automated setup:

```bash
bash run_setup.sh
```

### Missing beautifulsoup4

This is a common issue if you're running an older version. Install it with:

```bash
pip install beautifulsoup4 lxml
```

### Python Module Not Found Errors

Make sure you're running from the correct directory:

```bash
cd Files
python3 gui_app.py
```

Or install the package properly from the root directory:

```bash
pip install -e .
```

### Verify All Dependencies

Run the verification script to check all imports:

```bash
python3 verify_imports.py
```

### System Test

Check the complete system status:

```bash
cd Files && python3 test_system.py
```

This will show you exactly which components are missing or need attention.

---

## Mitwirken & Lizenz
1. Repo forken, Feature-Branch erstellen.
2. Änderungen + Tests (`pytest`) durchführen.
3. Pull Request mit Beschreibung erstellen.

Lizenz: **MIT** – kommerzielle Nutzung auf eigene Verantwortung.
