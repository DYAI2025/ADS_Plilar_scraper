# ADS Pillar Toolkit

> **Programmatic-SEO Baukasten für lokale Verzeichnisse mit AdSense-Monetarisierung.**
> Von der Nischenanalyse über Datenerfassung bis zur fertigen, hostbaren Website.

---

## 📚 Inhaltsverzeichnis

1. [Systemüberblick](#-systemüberblick)
2. [Funktionsmatrix](#-funktionsmatrix)
3. [Architektur & Datenfluss](#-architektur--datenfluss)
4. [Kernmodule im Detail](#-kernmodule-im-detail)
5. [Projektstruktur](#-projektstruktur)
6. [End-to-End Workflow](#-end-to-end-workflow)
7. [Tests & Qualitätssicherung](#-tests--qualitätssicherung)
8. [Monetarisierung & KPIs](#-monetarisierung--kpis)
9. [Compliance & Risiken](#-compliance--risiken)
10. [Skalierungsfahrplan](#-skalierungsfahrplan)
11. [Support & Beitrag](#-support--beitrag)
12. [Lizenz](#-lizenz)

---

## 🎯 Systemüberblick

ADS Pillar automatisiert komplette Location-Verzeichnisse:

- **Analyse** – Identifiziere lukrative Städte & Kategorien (`niche_research.py`).
- **Datenaufbereitung** – Scrape, anreichern und normalisieren von Locations (`data_pipeline.py`, `enhanced_scrapers.py`).
- **Website-Generierung** – Erzeuge statische Pillar-Pages inklusive JSON-LD & Filter-UI (`pillar_page_skeleton.html`).
- **Launch** – Bereite AdSense, SEO-Assets und Host-ready Deliverables vor (`seo_setup.py`, `ads.txt`, `run_setup.sh`).

> Ziel: Innerhalb weniger Minuten von einer Idee zur produktionsreifen Microsite gelangen.

---

## 🧭 Funktionsmatrix

| Use Case | Modul(e) | Output |
| --- | --- | --- |
| **Nischen recherchieren** | `niche_research.py`, `revenue_model.csv` | Keyword-Ideen, Opportunity-Score, RPM-Schätzung |
| **Locations beschaffen** | `enhanced_scrapers.py`, `directory_facets_template.csv` | Rohdaten (CSV/JSON) aus Google Places & Web-Scrapes |
| **Daten anreichern** | `data_pipeline.py` (\`DataEnrichment\`) | Feature-Flags (Schatten, Hunde erlaubt, Gebühren etc.) |
| **Website bauen** | `data_pipeline.py` (\`PillarPageGenerator\`), `pillar_page_skeleton.html` | Fertige HTML-Seite inkl. Filterlogik & Schema.org |
| **SEO & Monetarisierung** | `seo_setup.py`, `ads.txt`, `adsense_policy_checklist.md` | robots.txt, Sitemaps, AdSense-Konfiguration |
| **Go-Live automatisieren** | `quick_start.py`, `run_setup.sh`, `generated_site/` | Hostbare Artefakte, Demo-Seiten, Projekt-Konfig |
| **GUI-Prototyp** | `gui_app.py`, `ads-pillar-gui/` | Desktop-Oberfläche für nicht-technische Anwender |

---

## 🏗 Architektur & Datenfluss

```mermaid
graph TD
    A[Nischenanalyse\n`niche_research.py`] --> B[Dataset-Aufbau\n`enhanced_scrapers.py`]
    B --> C[Datenanreicherung\n`DataEnrichment`]
    C --> D[Pillar-Seite\n`PillarPageGenerator`]
    D --> E[Deployment-Paket\n`generated_site/`]
    D --> F[SEO Assets\n`seo_setup.py`]
    F --> G[Host Ready\n(Netlify, Vercel, S3)]
```

### Datenlebenszyklus

1. **Input** – Keywords, Städte, optionale Google Places API Keys.
2. **Scraping** – API- und HTML-Scrapes sammeln Grunddaten.
3. **Enrichment** – Keyword-gestützte Feature-Erkennung aus Reviews & Beschreibungen.
4. **Transformation** – Normalisierung in `LocationData`-Objekte.
5. **Generation** – Rendering des Templates mit Facetten-Filtern, Ads-Slots & JSON-LD.
6. **Export** – Ablage in `generated/` (HTML), `data/` (CSV/JSON) & `generated_site/` (Release-Paket).

---

## 🔍 Kernmodule im Detail

### Analyse & Strategie
- **`niche_research.py`** – Scoring-Modell für Städte/Kategorien, nutzt Markt- & RPM-Daten.
- **`Standard_Pillarpage.md`** – Content-Richtlinien für konsistente Pillar-Struktur.
- **`revenue_model.csv`** – Projektion von Umsätzen bei verschiedenen RPM/Pageview-Szenarien.

### Datenerhebung & Aufbereitung
- **`enhanced_scrapers.py`** – API-Wrapper (Google Places) + HTML-Scraper (BeautifulSoup) mit Rate-Limitierung.
- **`csv_to_data_json.py`** – Konvertiert CSV-Dumps in strukturierte JSON-Datasets.
- **`data_pipeline.py`**
  - `DataScraper` – generischer HTTP-Client.
  - `DataEnrichment` – Feature-Mapping auf Basis von Keyword-Listen.
  - `LocationData` – Dataclass mit über 20 Feldern.
  - `PillarPageGenerator` – Template-Renderer für komplette Seiten.

### Website-Generierung & Delivery
- **`pillar_page_skeleton.html`** – Responsive Template inkl. Ad-Slots, Filter, JSON-LD.
- **`generated_site/`** – Beispiel-Ausgabe (Product Ready) als Referenz für Hosting.
- **`seo_setup.py`** – Erzeugt robots.txt, sitemaps, favicon, OpenGraph.
- **`ads.txt` / `adsense_policy_checklist.md`** – Monetarisierungsgrundlagen.

### Tooling & Onboarding
- **`quick_start.py`** – Interaktives CLI für erste Projekte (Konfig, Beispieldaten, HTML-Demo).
- **`gui_app.py`** – Thin Wrapper auf die GUI-Implementierung in `Files/gui_app.py`.
- **`START_HERE.md`** – Schritt-für-Schritt Setup-Anleitung.

---

## 🗂 Projektstruktur

```text
ADS_Plilar_scraper/
├─ Files/                 # Hauptcode & Dokumentation
│  ├─ data_pipeline.py
│  ├─ enhanced_scrapers.py
│  ├─ niche_research.py
│  ├─ pillar_page_skeleton.html
│  ├─ README.md (dieses Dokument)
│  └─ ...
├─ gui_app.py             # Wrapper für Files/gui_app.py
├─ requirements.txt       # Python-Abhängigkeiten
├─ data/                  # Arbeitsdaten & CSV-Exports
├─ generated/             # Generierte Artefakte (HTML, Assets)
├─ templates/             # Zusätzliche HTML/Email-Templates
└─ tests/                 # Pytest-Suite (End-to-End & Regression)
```

---

## ⚙️ End-to-End Workflow

1. **Virtuelle Umgebung vorbereiten**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Nischen-Research durchführen**
   ```bash
   python Files/niche_research.py
   ```
   Liefert Opportunity-Scores, Keyword-Cluster und RPM-Range.
3. **Daten einsammeln**
   ```python
   from Files.data_pipeline import DataScraper
   scraper = DataScraper()
   parks = scraper.scrape_google_places("parks", "Berlin", api_key="YOUR_KEY")
   ```
4. **Feature-Anreicherung & Normalisierung**
   ```python
   from Files.data_pipeline import DataEnrichment
   enriched = [DataEnrichment.extract_features_from_text(p["reviews"]) for p in parks]
   ```
5. **Pillar-Seite generieren**
   ```python
   from Files.data_pipeline import PillarPageGenerator, LocationData
   generator = PillarPageGenerator("Files/pillar_page_skeleton.html")
   generator.generate_page(locations, "Berlin", "Parks", "generated/berlin-parks.html", "https://domain.com/berlin-parks")
   ```
6. **SEO & Hosting vorbereiten**
   ```bash
   python Files/seo_setup.py
   sh run_setup.sh
   ```
7. **AdSense integrieren**
   - Publisher-ID in Template ersetzen.
   - `ads.txt` im Root des Deployments bereitstellen.
   - Auto-Ads oder manuelle Slots aktivieren.

> 💡 Schnelleinstieg: `python Files/quick_start.py` erstellt Beispiel-Daten & HTML in einem Durchgang.

---

## ✅ Tests & Qualitätssicherung

| Testtyp | Befehl | Beschreibung |
| --- | --- | --- |
| **Smoke-Test** | `pytest Files/test_hello_world.py` | Prüft die Test-Infrastruktur.
| **System-Check** | `pytest Files/test_system.py` oder `python Files/test_system.py` | Validiert Projektdokumente, Module & Dependencies.
| **End-to-End** | `pytest tests/test_pipeline_end_to_end.py::test_generate_page_end_to_end` | Erstellt eine Demo-Seite und prüft das eingebettete JSON.
| **Regression** | `pytest tests/test_pipeline_end_to_end.py::test_feature_extraction_regression` | Sicherstellt stabile Feature-Extraktion aus Review-Texten.

Alle Tests auf einmal starten:
```bash
pytest
```

Die End-to-End-Suite generiert echte HTML-Ausgaben und verifiziert, dass Feature-Flags korrekt in die `const DATA`-Struktur eingebettet werden – damit bleibt der Release-Prozess HostReady.

---

## 💰 Monetarisierung & KPIs

### Revenue-Modell (Page RPM × Pageviews)

| Pageviews/Monat | RPM 8€ | RPM 15€ | RPM 25€ |
| --------------- | ------ | ------- | ------- |
| 50.000          | 400€   | 750€    | 1.250€  |
| 100.000         | 800€   | 1.500€  | 2.500€  |
| 250.000         | 2.000€ | 3.750€  | 6.250€  |

**Praxiswerte:**
- Monat 1: 10.000 Pageviews → ~80€ (8€ RPM)
- Monat 3: 50.000 Pageviews → ~600€ (12€ RPM)
- Monat 6: 150.000 Pageviews → ~2.250€ (15€ RPM)

### Monitoring-Dashboard

- **Täglich:** Pageviews, Page RPM, Ad Impressions, Invalid Traffic.
- **Wöchentlich:** Keyword-Rankings, CTR, Session Duration, Bounce Rate.
- **Monatlich:** A/B-Tests für Ad-Positionen, Content-Aktualisierung, neue Städte/Kategorien.

---

## ⚠️ Compliance & Risiken

### AdSense Policies
- Keine Aufforderungen zum Klicken auf Ads.
- Klare Kennzeichnung & Platzierung von Anzeigen.
- DSGVO-konformes Consent-Management für EU-Traffic.

### SEO Stolperfallen
- Duplicate Content vermeiden (unique city/category copy).
- Keyword Stuffing verhindern, natürliche Sprache bevorzugen.
- Ladezeiten trotz Ads optimieren (Lazy Loading, Minification).
- Mobile First UX priorisieren.

### Traffic-Qualität
- Fokus auf organischen Google Search Traffic.
- Kein bezahlter oder künstlicher Traffic → Risiko für AdSense-Ban.
- Beobachte Bounce Rate & Session Duration (<30s kritisch).

---

## 📈 Skalierungsfahrplan

| Phase | Zeitraum | Fokus |
| --- | --- | --- |
| **MVP** | Monat 1 | Eine Stadt, eine Kategorie, 20-50 Locations, erste Ads live |
| **Horizontal** | Monat 2-3 | Rollout in weitere Städte mit identischem Template |
| **Vertikal** | Monat 4-6 | Neue Kategorien in bestehenden Städten, interne Verlinkung |
| **Automation** | Monat 6+ | API-basierte Updates, Multi-Language, White-Label-Angebote |

---

## 🤝 Support & Beitrag

- **Ressourcen:**
  - [AdSense Help Center](https://support.google.com/adsense)
  - [Google Search Central](https://developers.google.com/search)
  - [Schema.org LocalBusiness](https://schema.org/LocalBusiness)
- **Community-Tools:**
  - [Google Places API](https://developers.google.com/maps/documentation/places/web-service)
  - [Ahrefs API](https://ahrefs.com/api)
  - [PageSpeed Insights](https://pagespeed.web.dev/)

### Mitmachen
1. Repository forken & Feature-Branch erstellen.
2. Tests hinzufügen/aktualisieren (`pytest`).
3. Pull Request mit klarer Beschreibung eröffnen.

---

## 📄 Lizenz

MIT License – freie Nutzung für kommerzielle Projekte auf eigene Verantwortung.

> 💡 **Pro-Tipp:** Eine sauber optimierte Pillar-Seite in einer mittelgroßen Stadt kann bereits vierstellige Monatsumsätze erzielen. Skalierung gelingt durch konsequente Datenqualität, saubere Templates und wiederholbare Prozesse.
