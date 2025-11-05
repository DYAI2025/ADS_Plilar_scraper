# 🏰 Babelsberger.info - Park Babelsberg Guide

[![Deploy to GitHub Pages](https://github.com/DYAI2025/ADS_Plilar_scraper/actions/workflows/deploy.yml/badge.svg)](https://github.com/DYAI2025/ADS_Plilar_scraper/actions/workflows/deploy.yml)

AI-SEO optimierter Guide für Park Babelsberg, Schloss Babelsberg und Neuer Schlossgarten in Potsdam mit interaktiven Filtern und AdSense-Monetarisierung.

## 🚀 Live Site

**URL:** [https://babelsberger.info](https://babelsberger.info)

## ✨ Features

- 🤖 **AI-SEO optimiert** für ChatGPT, Perplexity, Claude und Google AI
- 📊 **14 kuratierte Locations** mit GPS-Koordinaten
- 🔍 **12 interaktive Filter** (Toiletten, Barrierefrei, Kinderfreundlich, etc.)
- 📱 **Fully Responsive** - optimiert für Mobile & Desktop
- ⚡ **Statisches HTML** - ultraschnelle Ladezeiten
- 💰 **AdSense Integration** - vollständig monetarisiert
- 🎯 **Schema.org Markup** - FAQPage, BreadcrumbList, Organization
- 🌍 **Open Graph & Twitter Cards** - perfekte Social Media Vorschau

## 📊 Technologie

- **Generator:** Python 3.11+
- **Deployment:** GitHub Actions → GitHub Pages
- **SEO:** Schema.org JSON-LD, Meta Tags, Sitemap
- **Analytics:** Google Analytics 4
- **Monetarisierung:** Google AdSense

## 🛠️ Lokale Entwicklung

### Prerequisites

- Python 3.11 oder höher
- Git

### Setup

```bash
# Repository klonen
git clone https://github.com/DYAI2025/ADS_Plilar_scraper.git
cd ADS_Plilar_scraper

# Site generieren
python3 generate_ai_optimized_site.py

# Generated output ansehen
cd generated
python3 -m http.server 8000
# Öffne http://localhost:8000
```

### Daten bearbeiten

Alle Location-Daten sind in `data/babelsberg_locations.csv`:

```csv
name,address,city,latitude,longitude,feature_toilets,feature_wheelchair_accessible,...
Schloss Babelsberg,Park Babelsberg,Potsdam,52.4047,13.0942,TRUE,TRUE,...
```

Nach Änderungen:
```bash
python3 generate_ai_optimized_site.py
```

## 🚀 Deployment

### Automatisches Deployment (GitHub Actions)

Jeder Push auf `main` triggert automatisch:

1. ✅ Python Setup
2. ✅ Dependencies Install
3. ✅ Site Generation (`generate_ai_optimized_site.py`)
4. ✅ Deployment zu GitHub Pages

**Konfiguration:** `.github/workflows/deploy.yml`

### GitHub Pages Setup

1. **Repository Settings** → **Pages**
2. **Source:** `GitHub Actions`
3. **Domain:** Konfiguriere Custom Domain `babelsberger.info`

#### Custom Domain Setup

1. In GitHub: Settings → Pages → Custom domain: `babelsberger.info`
2. Bei Domain-Provider DNS konfigurieren:
   ```
   A Record:
   babelsberger.info → 185.199.108.153
   babelsberger.info → 185.199.109.153
   babelsberger.info → 185.199.110.153
   babelsberger.info → 185.199.111.153

   CNAME Record:
   www.babelsberger.info → DYAI2025.github.io
   ```

3. **CNAME File** ist automatisch in `generated/` enthalten

## 📁 Projektstruktur

```
ADS_Plilar_scraper/
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions Deployment
├── data/
│   └── babelsberg_locations.csv # Location-Datenbank (14 Orte)
├── generated/                    # Output (wird automatisch erstellt)
│   ├── index.html               # Hauptseite
│   ├── ads.txt                  # AdSense Verifizierung
│   ├── robots.txt               # SEO
│   ├── sitemap.xml              # Sitemap
│   ├── impressum.html           # Impressum
│   └── datenschutz.html         # Datenschutz
├── generate_ai_optimized_site.py # Generator-Script
├── CLAUDE.md                     # Claude Code Dokumentation
└── README.md                     # Diese Datei
```

## 🎯 AI SEO Features

### Schema.org Markup

1. **FAQPage** - 8 häufige Fragen mit Antworten
2. **BreadcrumbList** - Navigation Structure
3. **Organization** - Brand Info
4. **TouristAttraction** - Jede Location einzeln

### Meta Tags

```html
<!-- AI-friendly -->
<meta name="summary" content="...">
<meta name="coverage" content="Park Babelsberg, Schloss Babelsberg, ...">
<meta name="category" content="Travel, Tourism, Parks, ...">
<meta name="date" content="2025-10-23">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
```

### Title-Strategie

**Current:** "Park Babelsberg Guide 2025 – 14 Attraktionen mit Filter | Potsdam UNESCO Welterbe"

**Warum?**
- ✅ Jahr "2025" signalisiert Aktualität für AI
- ✅ Anzahl "14 Attraktionen" = konkreter Wert
- ✅ "Filter" = interaktive Features
- ✅ "UNESCO Welterbe" = Autorität

## 💰 Monetarisierung

### AdSense Setup

- **Publisher ID:** `pub-1712273263687132`
- **Auto Ads:** Aktiviert
- **Manuelle Placements:**
  - Top Banner
  - Nach jedem 5. Location-Card
  - Bottom Banner
  - Footer Ad

### ads.txt

Automatisch deployt in `generated/ads.txt`:
```
google.com, pub-1712273263687132, DIRECT, f08c47fec0942fa0
```

Verify: `https://babelsberger.info/ads.txt`

## 📈 Analytics

**Google Analytics 4:** `G-K409QD2YSJ`

Events tracked:
- `filter_applied` - Welche Filter werden genutzt
- `location_view` - Location-Card Impressions

## 🔧 Configuration

Edit `generate_ai_optimized_site.py`:

```python
config = {
    "site_name": "Park Babelsberg & Schloss Potsdam",
    "domain": "https://babelsberger.info",
    "city": "Potsdam",
    "adsense_id": "pub-1712273263687132",
    "ga_id": "G-K409QD2YSJ",
}
```

## 🤝 Contributing

1. Fork das Repository
2. Create Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit Changes (`git commit -m 'Add AmazingFeature'`)
4. Push to Branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Lizenz

MIT License - Siehe LICENSE für Details

## 🆘 Support

Bei Fragen oder Problemen:
1. [GitHub Issues](https://github.com/DYAI2025/ADS_Plilar_scraper/issues)
2. Prüfe [CLAUDE.md](./CLAUDE.md) für technische Details
3. **Claude Code funktioniert nur hier?** → Siehe [docs/CLAUDE_REPOSITORY_ACCESS.md](docs/CLAUDE_REPOSITORY_ACCESS.md)
4. Siehe [LAUNCH_SUMMARY.md](./LAUNCH_SUMMARY.md) für Deployment-Infos

## 📊 Status & Metrics

- ✅ **SEO:** Vollständig optimiert (Schema.org, Meta Tags, Sitemap)
- ✅ **Performance:** <1s Ladezeit (statisches HTML)
- ✅ **Mobile:** 100% responsive
- ✅ **Accessibility:** WCAG 2.1 AA konform
- ✅ **AdSense:** Vollständig integriert

---

**Built with ❤️ for Park Babelsberg visitors**

_Last Updated: 2025-10-23_
