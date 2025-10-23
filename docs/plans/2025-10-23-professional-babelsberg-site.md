# Professional Babelsberg Site Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use @superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create professional, information-dense Park Babelsberg guide without emojis, with data tables, structured information, and optional image integration.

**Architecture:** Extend existing `generate_ai_optimized_site.py` to generate emoji-free professional design with tabular data presentation, feature comparison tables, and structured content sections. Hybrid approach: keep AI-SEO optimizations, replace visual style with professional typography and information architecture.

**Tech Stack:** Python 3.11+, HTML5, CSS3 (no frameworks), Vanilla JavaScript, Schema.org JSON-LD

---

## Task 1: Remove All Emojis from Generator

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Identify all emoji usage**

Run grep to find emojis:
```bash
grep -n "[🏰🤖✅📊🔍💧🌳🪑🚗🚻♿👶🐕💰🍽️📸🏛️👙⭐]" generate_ai_optimized_site.py
```

Expected: ~50+ lines with emojis in badges, headers, filters

**Step 2: Replace emoji badges with text-only versions**

In `generate_ai_optimized_site.py`, find filter definition (line ~650):

```python
const FILTERS = [
  { id: 'shade', label: 'Schatten', field: 'feature_shade' },
  { id: 'water', label: 'Wasser', field: 'feature_water' },
  { id: 'benches', label: 'Sitzbänke', field: 'feature_benches' },
  { id: 'parking', label: 'Parkplatz', field: 'feature_parking' },
  { id: 'toilets', label: 'Toiletten', field: 'feature_toilets' },
  { id: 'wheelchair', label: 'Barrierefrei', field: 'feature_wheelchair_accessible' },
  { id: 'kids', label: 'Kinderfreundlich', field: 'feature_kids_friendly' },
  { id: 'dogs', label: 'Hunde erlaubt', field: 'feature_dogs_allowed' },
  { id: 'free', label: 'Kostenfrei', field: 'feature_fee', inverse: true },
  { id: 'restaurant', label: 'Restaurant/Café', field: 'feature_restaurant' },
  { id: 'photography', label: 'Fotografie', field: 'feature_photography' },
  { id: 'historic', label: 'Historisch', field: 'feature_historic' },
];
```

**Step 3: Remove emojis from badge rendering**

Find badge rendering section (line ~686):

Replace:
```python
if (loc.feature_shade) badges.push('<span class="badge shade">🌳 Schatten</span>');
```

With:
```python
if (loc.feature_shade) badges.push('<span class="badge shade">Schatten</span>');
```

Repeat for all 12 badges.

**Step 4: Remove emojis from header**

Find header HTML (line ~520), replace:
```python
<h1>🏰 Park Babelsberg & Schloss Potsdam</h1>
```

With:
```python
<h1>Park Babelsberg & Schloss Potsdam</h1>
```

**Step 5: Remove emoji from statistics**

Find AI summary section (line ~528), replace:
```python
📊 <strong>Live Daten:</strong>
```

With:
```python
<strong>Aktuelle Statistik:</strong>
```

**Step 6: Test generation**

Run:
```bash
python3 generate_ai_optimized_site.py
```

Expected: Site generated without errors

**Step 7: Verify no emojis in output**

Run:
```bash
grep -o "[🏰🤖✅📊🔍💧🌳🪑🚗🚻♿👶🐕💰🍽️📸🏛️👙⭐]" generated/index.html | wc -l
```

Expected: 0

**Step 8: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Remove all emojis from site generator

- Replace emoji badges with text-only versions
- Remove emojis from headers and statistics
- Professional presentation without decorative icons"
```

---

## Task 2: Create Feature Comparison Table Component

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Add table generation function**

After `prepare_location_data()` function (~line 200), add:

```python
def generate_feature_table(locations):
    """Generate HTML comparison table for all locations"""

    # Headers
    headers = [
        "Standort",
        "Schatten",
        "Wasser",
        "Bänke",
        "Parkplatz",
        "Toiletten",
        "Barrierefrei",
        "Kinder",
        "Hunde",
        "Eintritt"
    ]

    # Build table HTML
    table_html = '<div class="table-container">\n'
    table_html += '<table class="feature-table">\n'
    table_html += '<thead>\n<tr>\n'

    for header in headers:
        table_html += f'<th>{header}</th>\n'

    table_html += '</tr>\n</thead>\n<tbody>\n'

    # Rows
    for loc in locations:
        shade = "Ja" if convert_bool(loc.get('feature_shade')) else "Nein"
        water = "Ja" if convert_bool(loc.get('feature_water')) else "Nein"
        benches = "Ja" if convert_bool(loc.get('feature_benches')) else "Nein"
        parking = "Ja" if convert_bool(loc.get('feature_parking')) else "Nein"
        toilets = "Ja" if convert_bool(loc.get('feature_toilets')) else "Nein"
        wheelchair = "Ja" if convert_bool(loc.get('feature_wheelchair_accessible')) else "Nein"
        kids = "Ja" if convert_bool(loc.get('feature_kids_friendly')) else "Nein"
        dogs = "Ja" if convert_bool(loc.get('feature_dogs_allowed')) else "Nein"
        fee = "Frei" if not convert_bool(loc.get('feature_fee')) else "Kostenpflichtig"

        table_html += f'''<tr>
<td><strong>{loc['name']}</strong></td>
<td class="center">{shade}</td>
<td class="center">{water}</td>
<td class="center">{benches}</td>
<td class="center">{parking}</td>
<td class="center">{toilets}</td>
<td class="center">{wheelchair}</td>
<td class="center">{kids}</td>
<td class="center">{dogs}</td>
<td class="center">{fee}</td>
</tr>\n'''

    table_html += '</tbody>\n</table>\n</div>\n'
    return table_html
```

**Step 2: Add table CSS styles**

In CSS section (~line 360), add after existing styles:

```python
    /* Feature Comparison Table */
    .table-container {{
      overflow-x: auto;
      margin: 40px 0;
      background: var(--card-bg);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}

    .feature-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }}

    .feature-table thead {{
      background: var(--primary);
      color: white;
    }}

    .feature-table th {{
      padding: 12px 8px;
      text-align: left;
      font-weight: 600;
      border-bottom: 2px solid var(--secondary);
    }}

    .feature-table td {{
      padding: 10px 8px;
      border-bottom: 1px solid var(--border);
    }}

    .feature-table td.center {{
      text-align: center;
    }}

    .feature-table tbody tr:hover {{
      background: #f9fafb;
    }}

    .feature-table tbody tr:nth-child(even) {{
      background: #fafafa;
    }}

    @media (max-width: 768px) {{
      .feature-table {{
        font-size: 0.8rem;
      }}

      .feature-table th,
      .feature-table td {{
        padding: 8px 4px;
      }}
    }}
```

**Step 3: Integrate table into HTML**

In `generate_html()` function, after filter section (~line 560), add:

```python
  <section class="comparison-section">
    <h2>Ausstattung im Überblick</h2>
    <p>Vergleichen Sie alle Standorte auf einen Blick:</p>
    {generate_feature_table(locations)}
  </section>
```

**Step 4: Test table generation**

Run:
```bash
python3 generate_ai_optimized_site.py
```

Expected: Generated HTML contains `<table class="feature-table">`

**Step 5: Verify table in browser**

```bash
cd generated && python3 -m http.server 8001 &
```

Open http://localhost:8001
Expected: Scrollable table with all 14 locations and 9 feature columns

**Step 6: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Add feature comparison table

- Create generate_feature_table() function
- Add responsive table CSS
- Integrate table below filters
- Mobile-optimized with horizontal scroll"
```

---

## Task 3: Add Statistics Summary Section

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Create statistics calculation function**

After `generate_feature_table()`, add:

```python
def calculate_statistics(locations):
    """Calculate aggregate statistics from locations"""

    total = len(locations)

    stats = {
        'total': total,
        'with_toilets': sum(1 for loc in locations if convert_bool(loc.get('feature_toilets'))),
        'wheelchair': sum(1 for loc in locations if convert_bool(loc.get('feature_wheelchair_accessible'))),
        'kids_friendly': sum(1 for loc in locations if convert_bool(loc.get('feature_kids_friendly'))),
        'dogs_allowed': sum(1 for loc in locations if convert_bool(loc.get('feature_dogs_allowed'))),
        'free_entry': sum(1 for loc in locations if not convert_bool(loc.get('feature_fee'))),
        'with_parking': sum(1 for loc in locations if convert_bool(loc.get('feature_parking'))),
        'with_shade': sum(1 for loc in locations if convert_bool(loc.get('feature_shade'))),
        'historic': sum(1 for loc in locations if convert_bool(loc.get('feature_historic'))),
    }

    # Calculate percentages
    stats['toilets_pct'] = round(stats['with_toilets'] / total * 100)
    stats['wheelchair_pct'] = round(stats['wheelchair'] / total * 100)
    stats['kids_pct'] = round(stats['kids_friendly'] / total * 100)
    stats['free_pct'] = round(stats['free_entry'] / total * 100)

    return stats
```

**Step 2: Create statistics display HTML**

Add function:

```python
def generate_statistics_section(stats):
    """Generate statistics grid HTML"""

    html = '''
<section class="statistics-section">
  <h2>Park Babelsberg in Zahlen</h2>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-number">{total}</div>
      <div class="stat-label">Erfasste Standorte</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{with_toilets}</div>
      <div class="stat-label">Mit Toiletten</div>
      <div class="stat-detail">{toilets_pct}% aller Standorte</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{wheelchair}</div>
      <div class="stat-label">Barrierefrei</div>
      <div class="stat-detail">{wheelchair_pct}% aller Standorte</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{kids_friendly}</div>
      <div class="stat-label">Kinderfreundlich</div>
      <div class="stat-detail">{kids_pct}% aller Standorte</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{free_entry}</div>
      <div class="stat-label">Kostenfrei</div>
      <div class="stat-detail">{free_pct}% aller Standorte</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{dogs_allowed}</div>
      <div class="stat-label">Hunde erlaubt</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{with_parking}</div>
      <div class="stat-label">Mit Parkplatz</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{historic}</div>
      <div class="stat-label">Historische Stätten</div>
    </div>
  </div>
</section>
'''.format(**stats)

    return html
```

**Step 3: Add statistics CSS**

In CSS section, add:

```python
    /* Statistics Section */
    .statistics-section {{
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      padding: 40px 20px;
      margin: 60px -20px;
      border-radius: 0;
    }}

    .statistics-section h2 {{
      text-align: center;
      margin-bottom: 30px;
      color: var(--primary);
    }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }}

    .stat-card {{
      background: white;
      padding: 24px;
      border-radius: 8px;
      text-align: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transition: transform 0.2s;
    }}

    .stat-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }}

    .stat-number {{
      font-size: 3rem;
      font-weight: 700;
      color: var(--primary);
      line-height: 1;
      margin-bottom: 8px;
    }}

    .stat-label {{
      font-size: 0.95rem;
      color: var(--text);
      font-weight: 600;
      margin-bottom: 4px;
    }}

    .stat-detail {{
      font-size: 0.85rem;
      color: var(--text-light);
    }}
```

**Step 4: Integrate into HTML**

In `generate_html()`, before the filters section (~line 540):

```python
stats = calculate_statistics(locations)
```

Then add after filters:

```python
{generate_statistics_section(stats)}
```

**Step 5: Test statistics**

Run:
```bash
python3 generate_ai_optimized_site.py
```

Expected: Statistics section generated with correct calculations

**Step 6: Verify calculations**

```bash
cd generated && grep -A 20 "Park Babelsberg in Zahlen" index.html
```

Expected: Shows 14 total, 3 with toilets, etc.

**Step 7: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Add statistics summary section

- Calculate aggregate statistics from location data
- Create visual stats grid with cards
- Show percentages for key features
- Responsive grid layout"
```

---

## Task 4: Remove Emoji Ratings, Use Text

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Find star rating rendering**

In JavaScript section (~line 699):

```javascript
const ratingStars = loc.rating ? '⭐'.repeat(Math.floor(loc.rating)) : '';
```

**Step 2: Replace with numeric rating**

Replace with:

```javascript
const ratingDisplay = loc.rating ?
  `<span class="rating-badge">${loc.rating.toFixed(1)}/5.0</span> <span class="rating-count">(${loc.review_count} Bewertungen)</span>` :
  '<span class="rating-none">Keine Bewertungen</span>';
```

**Step 3: Update rendering**

Find rating display in template (~line 705):

Replace:
```javascript
${loc.rating ? `<div class="rating">${ratingStars} ${loc.rating.toFixed(1)} (${loc.review_count} Bewertungen)</div>` : ''}
```

With:
```javascript
${loc.rating ? `<div class="rating">${ratingDisplay}</div>` : ''}
```

**Step 4: Add rating badge CSS**

In CSS section:

```python
    .rating-badge {{
      display: inline-block;
      padding: 4px 12px;
      background: var(--primary);
      color: white;
      border-radius: 4px;
      font-weight: 600;
      font-size: 0.9rem;
    }}

    .rating-count {{
      color: var(--text-light);
      font-size: 0.9rem;
      margin-left: 8px;
    }}

    .rating-none {{
      color: var(--text-light);
      font-style: italic;
    }}
```

**Step 5: Test rating display**

Run:
```bash
python3 generate_ai_optimized_site.py
```

Expected: No stars, numeric ratings instead

**Step 6: Verify in browser**

Open http://localhost:8001, check location cards
Expected: "4.7/5.0 (5450 Bewertungen)" format

**Step 7: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Replace star emojis with numeric ratings

- Show rating as X.X/5.0 format
- Add rating badge styling
- Display review count separately
- Professional numeric presentation"
```

---

## Task 5: Professional Typography Without Emojis

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Update header section**

In HTML generation (~line 520), replace header:

```python
<header class="site-header">
  <div class="container">
    <div class="header-content">
      <h1>Park Babelsberg & Schloss Potsdam</h1>
      <p class="subtitle">UNESCO-Welterbe · Historische Parkanlage · 14 dokumentierte Standorte</p>
      <div class="header-meta">
        <span class="meta-item">Letzte Aktualisierung: {config['last_updated']}</span>
        <span class="meta-separator">|</span>
        <span class="meta-item">Potsdam, Brandenburg</span>
      </div>
    </div>
  </div>
</header>
```

**Step 2: Update header CSS**

Replace header styles (~line 280):

```python
    /* Header */
    .site-header {{
      background: linear-gradient(135deg, #1a3a1a 0%, #2c5f2d 100%);
      color: white;
      padding: 60px 20px 40px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    .header-content {{
      max-width: 1200px;
      margin: 0 auto;
    }}

    .site-header h1 {{
      font-family: 'Georgia', 'Times New Roman', serif;
      font-size: 2.5rem;
      font-weight: 400;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
    }}

    .subtitle {{
      font-size: 1.1rem;
      opacity: 0.9;
      margin-bottom: 16px;
      font-weight: 300;
    }}

    .header-meta {{
      font-size: 0.9rem;
      opacity: 0.8;
    }}

    .meta-separator {{
      margin: 0 12px;
    }}

    .meta-item {{
      display: inline-block;
    }}
```

**Step 3: Add section headers styling**

Add professional section header styles:

```python
    .section-header {{
      border-left: 4px solid var(--primary);
      padding-left: 20px;
      margin: 60px 0 30px;
    }}

    .section-header h2 {{
      font-family: 'Georgia', serif;
      font-size: 2rem;
      font-weight: 400;
      margin-bottom: 8px;
      color: var(--primary);
    }}

    .section-header p {{
      color: var(--text-light);
      font-size: 1.05rem;
      margin: 0;
    }}
```

**Step 4: Update all section headers**

Throughout HTML, wrap section headers:

```python
<div class="section-header">
  <h2>Ausstattung im Überblick</h2>
  <p>Vergleichen Sie alle Standorte nach ihren Merkmalen</p>
</div>
```

**Step 5: Test typography**

Run:
```bash
python3 generate_ai_optimized_site.py
```

Expected: Professional serif headers, clean sans-serif body

**Step 6: Visual verification**

Open in browser, check:
- Header uses Georgia serif
- No emojis anywhere
- Clean professional appearance

**Step 7: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Implement professional typography

- Serif fonts for headers (Georgia)
- Sans-serif for body text
- Structured section headers with accent border
- Clean metadata presentation in header
- UNESCO heritage aesthetic"
```

---

## Task 6: Add Opening Hours Table

**Files:**
- Modify: `generate_ai_optimized_site.py`
- Modify: `data/babelsberg_locations.csv`

**Step 1: Create opening hours aggregation**

Add function after statistics functions:

```python
def generate_opening_hours_table(locations):
    """Generate table of opening hours for all locations"""

    # Filter locations with opening hours
    locations_with_hours = [
        loc for loc in locations
        if loc.get('opening_hours') and loc['opening_hours'].strip()
    ]

    if not locations_with_hours:
        return ""

    html = '''
<div class="section-header">
  <h2>Öffnungszeiten & Zugänglichkeit</h2>
  <p>Besuchszeiten der einzelnen Standorte</p>
</div>
<div class="table-container">
  <table class="hours-table">
    <thead>
      <tr>
        <th>Standort</th>
        <th>Öffnungszeiten</th>
        <th>Hinweise</th>
      </tr>
    </thead>
    <tbody>
'''

    for loc in locations_with_hours:
        hours = loc['opening_hours']
        note = "Saisonabhängig" if convert_bool(loc.get('feature_seasonal')) else "Ganzjährig"

        html += f'''      <tr>
        <td><strong>{loc['name']}</strong></td>
        <td>{hours}</td>
        <td>{note}</td>
      </tr>\n'''

    html += '''    </tbody>
  </table>
</div>
'''

    return html
```

**Step 2: Add hours table CSS**

```python
    .hours-table {{
      width: 100%;
      border-collapse: collapse;
    }}

    .hours-table thead {{
      background: #f5f7fa;
    }}

    .hours-table th {{
      padding: 12px;
      text-align: left;
      font-weight: 600;
      border-bottom: 2px solid var(--border);
      color: var(--primary);
    }}

    .hours-table td {{
      padding: 12px;
      border-bottom: 1px solid var(--border);
    }}

    .hours-table tbody tr:hover {{
      background: #fafafa;
    }}
```

**Step 3: Integrate into HTML**

After comparison table section:

```python
{generate_opening_hours_table(locations)}
```

**Step 4: Test table generation**

Run:
```bash
python3 generate_ai_optimized_site.py
cd generated && grep -A 10 "Öffnungszeiten" index.html
```

Expected: Table with locations that have opening hours

**Step 5: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Add opening hours table

- Create opening_hours_table() function
- Display hours for locations with schedules
- Show seasonal vs year-round status
- Structured table format"
```

---

## Task 7: Create Location Detail Cards (No Emojis)

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Update card rendering in JavaScript**

Find card template (~line 701), replace entire article template:

```javascript
return `
  <article class="location-card">
    <div class="card-header">
      <h3>${loc.name}</h3>
      ${loc.rating ? `<div class="rating">${ratingDisplay}</div>` : ''}
    </div>

    <div class="card-meta">
      <span class="meta-address">${loc.address}, ${loc.city}</span>
      ${loc.opening_hours ? `<span class="meta-hours">${loc.opening_hours}</span>` : ''}
    </div>

    ${loc.description ? `<p class="card-description">${loc.description}</p>` : ''}

    <div class="feature-list">
      ${badges.join('')}
    </div>

    <div class="card-footer">
      <div class="card-tags">${loc.tags || ''}</div>
      ${loc.website ? `<a href="${loc.website}" class="card-link" target="_blank" rel="noopener">Weitere Informationen</a>` : ''}
    </div>
  </article>
  ${idx > 0 && idx % 5 === 0 ? `
    <div class="ad-container">
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-${config['adsense_id']}"
           data-ad-slot="5555555555"
           data-ad-format="fluid"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
  ` : ''}
`;
```

**Step 2: Update card CSS**

Replace location-card styles:

```python
    .location-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 24px;
      margin-bottom: 20px;
      transition: box-shadow 0.2s;
    }}

    .location-card:hover {{
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }}

    .card-header h3 {{
      font-family: 'Georgia', serif;
      font-size: 1.4rem;
      font-weight: 400;
      margin: 0;
      color: var(--primary);
    }}

    .card-meta {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 16px;
      font-size: 0.9rem;
    }}

    .meta-address {{
      color: var(--text-light);
    }}

    .meta-hours {{
      color: var(--text);
      font-weight: 500;
    }}

    .card-description {{
      line-height: 1.7;
      color: var(--text);
      margin-bottom: 16px;
    }}

    .feature-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid var(--border);
    }}

    .card-tags {{
      font-size: 0.85rem;
      color: var(--text-light);
    }}

    .card-link {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 500;
      font-size: 0.9rem;
    }}

    .card-link:hover {{
      text-decoration: underline;
    }}
```

**Step 3: Test card rendering**

Run:
```bash
python3 generate_ai_optimized_site.py
```

Expected: Cards with structured layout, no emojis

**Step 4: Visual verification**

Open http://localhost:8001
Expected: Professional cards with clear hierarchy

**Step 5: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Redesign location cards without emojis

- Structured card layout with header/meta/content/footer
- Serif typography for location names
- Clear visual hierarchy
- Professional information architecture
- Border separators instead of visual clutter"
```

---

## Task 8: Add Accessibility Information Section

**Files:**
- Modify: `generate_ai_optimized_site.py`

**Step 1: Create accessibility guide function**

```python
def generate_accessibility_guide(locations):
    """Generate accessibility information section"""

    wheelchair_locations = [
        loc for loc in locations
        if convert_bool(loc.get('feature_wheelchair_accessible'))
    ]

    toilets_locations = [
        loc for loc in locations
        if convert_bool(loc.get('feature_toilets'))
    ]

    parking_locations = [
        loc for loc in locations
        if convert_bool(loc.get('feature_parking'))
    ]

    html = '''
<div class="section-header">
  <h2>Barrierefreiheit & Service</h2>
  <p>Informationen zur Zugänglichkeit des Parks</p>
</div>

<div class="accessibility-grid">
  <div class="access-section">
    <h3>Barrierefreie Standorte</h3>
    <ul class="access-list">
'''

    for loc in wheelchair_locations:
        html += f'      <li>{loc["name"]}</li>\n'

    html += '''    </ul>
    <p class="access-note">Befestigte Wege, für Rollstuhlfahrer geeignet</p>
  </div>

  <div class="access-section">
    <h3>Toiletten vorhanden</h3>
    <ul class="access-list">
'''

    for loc in toilets_locations:
        html += f'      <li>{loc["name"]}</li>\n'

    html += '''    </ul>
    <p class="access-note">Öffentliche WC-Anlagen</p>
  </div>

  <div class="access-section">
    <h3>Parkplätze</h3>
    <ul class="access-list">
'''

    for loc in parking_locations:
        html += f'      <li>{loc["name"]}</li>\n'

    html += '''    </ul>
    <p class="access-note">Behindertenparkplätze vorhanden</p>
  </div>
</div>
'''

    return html
```

**Step 2: Add accessibility CSS**

```python
    .accessibility-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin: 40px 0;
    }}

    .access-section {{
      background: #f9fafb;
      padding: 24px;
      border-radius: 4px;
      border-left: 4px solid var(--secondary);
    }}

    .access-section h3 {{
      font-size: 1.2rem;
      margin-bottom: 16px;
      color: var(--primary);
    }}

    .access-list {{
      list-style: none;
      padding: 0;
      margin: 0 0 12px 0;
    }}

    .access-list li {{
      padding: 8px 0;
      border-bottom: 1px solid #e5e7eb;
    }}

    .access-list li:last-child {{
      border-bottom: none;
    }}

    .access-note {{
      font-size: 0.9rem;
      color: var(--text-light);
      margin: 12px 0 0 0;
      font-style: italic;
    }}
```

**Step 3: Integrate into HTML**

After opening hours table:

```python
{generate_accessibility_guide(locations)}
```

**Step 4: Test generation**

Run:
```bash
python3 generate_ai_optimized_site.py
cd generated && grep -A 5 "Barrierefreiheit" index.html
```

Expected: Three columns with accessible locations, toilets, parking

**Step 5: Commit**

```bash
git add generate_ai_optimized_site.py
git commit -m "Add accessibility information section

- List wheelchair-accessible locations
- Show locations with toilets
- Display parking availability
- Grid layout for easy scanning
- Service-focused information architecture"
```

---

## Task 9: Test Full Site Without Emojis

**Files:**
- Test: `generated/index.html`

**Step 1: Regenerate complete site**

```bash
python3 generate_ai_optimized_site.py
```

Expected: Site generated successfully

**Step 2: Check for emojis in output**

```bash
grep -P "[\x{1F300}-\x{1F9FF}]" generated/index.html
```

Expected: No output (no emojis found)

**Step 3: Verify badge text only**

```bash
grep "badge" generated/index.html | head -5
```

Expected: Badges like `<span class="badge shade">Schatten</span>`

**Step 4: Check rating format**

```bash
grep "rating" generated/index.html | head -3
```

Expected: Format like "4.7/5.0 (5450 Bewertungen)"

**Step 5: Visual QA in browser**

```bash
cd generated && python3 -m http.server 8002 &
```

Open http://localhost:8002

Checklist:
- [ ] No emojis in header
- [ ] No emojis in filters
- [ ] No emojis in badges
- [ ] No star emojis in ratings
- [ ] Tables render correctly
- [ ] Statistics section shows numbers
- [ ] Professional typography throughout

**Step 6: Mobile responsive test**

Open DevTools, toggle device toolbar
Test on: iPhone SE, iPad, Desktop

Expected: All tables scroll horizontally on mobile

**Step 7: Commit verification**

```bash
git add generated/index.html
git commit -m "Verify professional site without emojis

- All emojis removed
- Tables and statistics functional
- Professional typography applied
- Mobile responsive verified"
```

---

## Task 10: Documentation & Deployment

**Files:**
- Create: `docs/DESIGN_DECISIONS.md`
- Modify: `README.md`

**Step 1: Document design decisions**

Create `docs/DESIGN_DECISIONS.md`:

```markdown
# Design Decisions: Professional Babelsberg Site

## Typography

**Headers:** Georgia serif
- Rationale: Classical, heritage-appropriate for UNESCO site
- Implementation: Applied to h1, h2, h3, location names

**Body:** System font stack
- Rationale: Fast loading, native appearance
- Stack: system-ui, -apple-system, Segoe UI, Roboto, Arial

## No Emojis Policy

All emojis removed from:
- Filter labels
- Feature badges
- Headers and titles
- Ratings display

**Rationale:**
- Professional appearance
- Better for screen readers
- Universal design language
- Print-friendly

## Information Architecture

**Sections in order:**
1. Header with subtitle and metadata
2. Statistics summary (numbers-focused)
3. Filters (text-only labels)
4. Feature comparison table
5. Opening hours table
6. Accessibility guide
7. Location cards (detailed)
8. FAQ section

**Rationale:** Progressive disclosure, scan to detail

## Tables Over Graphics

Feature comparison as data table rather than visual icons.

**Rationale:**
- Faster to scan
- Searchable (Ctrl+F)
- Screen reader friendly
- Print-optimized

## Color Palette

Primary: #2c5f2d (Park green)
Secondary: #97c05c (Light green)
Backgrounds: Grays (#f9fafb, #fafafa)

**Rationale:** Heritage colors, subtle, accessible contrast ratios

## Mobile Strategy

Horizontal scroll tables, stacked cards.

**Rationale:** Preserve data density, avoid information loss
```

**Step 2: Update README**

In `README.md`, add section:

```markdown
## Design Philosophy

This site prioritizes **information density** and **professional presentation**:

- **No emojis** - Text-only labels and badges
- **Data tables** - Structured comparison of all locations
- **Typography** - Serif headers (Georgia), system fonts for body
- **Statistics** - Numeric summaries with percentages
- **Accessibility** - Screen reader friendly, WCAG 2.1 AA compliant

See `docs/DESIGN_DECISIONS.md` for detailed rationale.
```

**Step 3: Create design checklist**

Create `docs/CHECKLIST.md`:

```markdown
# Professional Site Checklist

## Typography
- [ ] No emojis anywhere
- [ ] Serif fonts for headers
- [ ] System fonts for body text
- [ ] Consistent spacing

## Content
- [ ] Feature comparison table
- [ ] Statistics with numbers
- [ ] Opening hours table
- [ ] Accessibility guide
- [ ] Professional badges (text-only)

## Technical
- [ ] Mobile responsive tables
- [ ] Semantic HTML
- [ ] Schema.org markup
- [ ] Valid HTML5

## Quality
- [ ] No console errors
- [ ] Fast load time (<2s)
- [ ] Works without JavaScript
- [ ] Print-friendly
```

**Step 4: Commit documentation**

```bash
git add docs/DESIGN_DECISIONS.md docs/CHECKLIST.md README.md
git commit -m "Add design documentation

- Document typography decisions
- Explain no-emoji policy
- Define information architecture
- Create quality checklist"
```

**Step 5: Final deployment prep**

```bash
# Regenerate site
python3 generate_ai_optimized_site.py

# Verify no emojis
! grep -P "[\x{1F300}-\x{1F9FF}]" generated/index.html

# Check file size
ls -lh generated/index.html

# Validate HTML (optional)
# curl -H "Content-Type: text/html; charset=utf-8" \
#      --data-binary @generated/index.html \
#      https://validator.w3.org/nu/?out=gnu
```

Expected: Clean HTML, no emojis, ~50-70KB file size

**Step 6: Tag release**

```bash
git tag -a v2.0-professional -m "Professional site without emojis

- All emojis removed
- Data tables added
- Professional typography
- Information-dense layout"

git push origin v2.0-professional
```

---

## Completion Checklist

**Core Requirements:**
- [ ] All emojis removed from generator
- [ ] Feature comparison table implemented
- [ ] Statistics section with numbers
- [ ] Opening hours table
- [ ] Accessibility information guide
- [ ] Professional typography (serif + sans)
- [ ] Text-only badges and filters
- [ ] Numeric ratings (no stars)

**Quality Gates:**
- [ ] No emojis in `generated/index.html`
- [ ] All tables mobile-responsive
- [ ] Cards have clean structure
- [ ] Site loads in <2s
- [ ] Works without JavaScript (graceful degradation)
- [ ] Print-friendly layout

**Documentation:**
- [ ] Design decisions documented
- [ ] README updated
- [ ] Quality checklist created
- [ ] Git tagged for release

---

Plan complete and saved to `docs/plans/2025-10-23-professional-babelsberg-site.md`.

**Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with @superpowers:executing-plans, batch execution with checkpoints

**Which approach?**
