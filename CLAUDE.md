# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ADS Pillar Scraper** is a programmatic SEO toolkit for generating static pillar pages (location directories) with Google AdSense monetization. The system scrapes data from Google Places API and other sources, enriches it with features extracted from reviews, and generates SEO-optimized HTML pages.

**Target**: Create automated, monetizable directory sites for local search intents (e.g., "parks in Berlin", "restaurants in Munich")

## Core Architecture

The project follows a **data pipeline architecture** with these key stages:

```
Niche Research → Data Collection → Enrichment → Page Generation → Deployment
```

### Key Modules

**Data Collection Layer** (`Files/` and `Files 2/` contain active implementations):
- `enhanced_scrapers.py`: Multi-source data scrapers
  - `GooglePlacesScraper`: Google Places API integration with pagination
  - `WebScraper`: Directory site scraping (BeautifulSoup-based)
  - `UniversalScraper`: Combines multiple sources with deduplication
  - `SmartFeatureExtractor`: Extracts feature flags from review text

- `data_pipeline.py`: Core data processing
  - `LocationData`: Dataclass with 15+ feature flags (shade, benches, parking, etc.)
  - `DataEnrichment`: Keyword-based feature extraction from German/English text
  - `PillarPageGenerator`: Jinja2-based HTML generation with AdSense integration
  - `DataScraper`: Google Places API wrapper with retry logic

**Research & Planning**:
- `niche_research.py`: Niche validation and keyword research
  - `NicheValidator`: Pre-configured profitable niches with RPM estimates
  - `KeywordResearch`: SERP analysis and keyword variation generation
  - Opportunity scoring based on traffic, competition, and monetization

**User Interfaces**:
- `gui_app.py`: Tkinter GUI for non-technical users
  - Revenue calculator (RPM scenarios: 8€, 15€, 25€)
  - CSV import/export
  - Project configuration management
  - Falls back to stub implementations if dependencies missing

- `quick_start.py`: CLI wizard for initial setup and demo data generation

**Setup & Infrastructure**:
- `run_setup.sh`: Automated virtualenv setup with all dependencies
- `setup.py`: Package installer with console entry points (`ads-pillar-gui`, `ads-pillar-quick`, `ads-pillar-niche`)
- `verify_imports.py`: Dependency verification script

### Critical Implementation Details

**Dual Directory Structure**: The repo has both `Files/` and `Files 2/` directories containing module implementations. `Files 2/` has the complete `data_pipeline.py`, while `Files/` contains other core modules. The GUI imports attempt to find modules from the working directory.

**Graceful Degradation**: `gui_app.py` uses try/except imports with fallback stub classes. If `data_pipeline`, `niche_research`, or other modules fail to import, the GUI shows a warning but doesn't crash.

**Feature Extraction**: The system uses keyword matching against German/English terms to extract boolean features from review text (e.g., "schatten" → `feature_shade: True`). See `DataEnrichment.FEATURE_KEYWORDS` in `data_pipeline.py`.

**Template System**: `pillar_page_skeleton.html` is a Jinja2 template with:
- Client-side JavaScript filtering (by features like "shade", "parking")
- Schema.org JSON-LD for local business markup
- AdSense Auto Ads + manual placement slots
- Mobile-responsive design with sticky ad units

## Development Commands

### Setup
```bash
# Full automated setup (recommended)
./run_setup.sh

# Manual setup
pip install -r requirements.txt
pip install -e .  # Install as package with entry points

# Verify all dependencies loaded
python3 verify_imports.py
```

### Testing
```bash
# Run full test suite (both /tests and Files/tests)
pytest

# Run specific test directory
pytest Files/tests/ -v

# Run system health check
cd Files && python3 test_system.py

# Run single test file
pytest tests/test_pipeline_end_to_end.py -v
```

**Test Structure**:
- `tests/` (root): End-to-end integration tests
- `Files/tests/`: Module-specific unit tests
- `Files 2/tests/`: Additional test coverage
- Tests gracefully skip GUI tests when tkinter unavailable (CI/CD environments)

### Linting & Formatting
```bash
# Check formatting
black --check Files/*.py *.py

# Auto-format all Python files
black Files/*.py *.py

# Lint with flake8 (critical errors only)
flake8 Files/*.py *.py --count --select=E9,F63,F7,F82 --show-source

# Run pre-commit hooks
pre-commit run --all-files
```

**Code Style**: Project uses Black formatter with 120 char line length. Pre-commit hooks enforce Black, flake8, isort, and trailing whitespace checks.

### Running the Application

```bash
# Interactive setup wizard (creates demo data)
python Files/quick_start.py

# Launch GUI
python Files/gui_app.py
# or if installed as package:
ads-pillar-gui

# CLI niche research
python Files/niche_research.py
# or:
ads-pillar-niche
```

### Data Pipeline Usage

```python
from Files.enhanced_scrapers import GooglePlacesScraper, UniversalScraper
from Files.data_pipeline import PillarPageGenerator

# Scrape locations
scraper = GooglePlacesScraper(api_key="YOUR_API_KEY")
locations = scraper.search_places("parks", "Berlin")

# Generate HTML page
generator = PillarPageGenerator(
    template_path="Files/pillar_page_skeleton.html",
    config={
        "site_name": "Berlin Parks Guide",
        "adsense_id": "ca-pub-XXXXXXXX",
        "ga_id": "GA_MEASUREMENT_ID"
    }
)
generator.generate_page(
    locations=locations,
    output_path="generated/index.html"
)
```

## Configuration

**Project Config** (`project_config.json`):
```json
{
  "site_name": "Park Babelsberg Guide",
  "domain": "https://www.babelsberger.info",
  "city": "Potsdam",
  "category": "Parks",
  "adsense_id": "pub-XXXXXXXXXX",
  "ga_id": "G-XXXXXXXXXX"
}
```

**API Keys**: Set environment variables or pass to scrapers:
- `GOOGLE_PLACES_API_KEY`: For GooglePlacesScraper
- Store in `.env` file (NOT committed - already in .gitignore)

## CI/CD

**Workflows** (`.github/workflows/`):
- `test.yml`: Full test suite on Python 3.8-3.12, lint checks
- `ci.yml`: Quick pytest run on push/PR
- `claude.yml`: Claude Code integration for issue/PR assistance
- `claude-code-review.yml`: Automated code review on PRs

**Claude Code Integration**:
- Uses `CLAUDE_CODE_OAUTH_TOKEN` secret for authentication
- Triggered by `@claude` mentions in issues/PRs
- **Troubleshooting**: If Claude only works in this repo, see [docs/CLAUDE_REPOSITORY_ACCESS.md](docs/CLAUDE_REPOSITORY_ACCESS.md)

**Pre-commit Hooks** (`.pre-commit-config.yaml`):
- Black formatting
- Flake8 linting (120 char line, ignoring E203, W503)
- Trailing whitespace, EOF fixer
- YAML/JSON validation
- Import sorting (isort with Black profile)

## Common Pitfalls

1. **Import Errors**: If you see "Missing Dependencies" in GUI:
   - Run `pip install -r requirements.txt`
   - Specifically check for `beautifulsoup4` and `lxml`
   - Run `python3 verify_imports.py` to diagnose

2. **Module Not Found**: The codebase has modules in both `Files/` and `Files 2/`:
   - Always run scripts from their containing directory or install package with `pip install -e .`
   - `data_pipeline.py` is in `Files 2/`, not `Files/`

3. **Tkinter Unavailable**: Tests skip GUI tests gracefully in headless environments
   - This is expected in CI/CD - 2 tests will be skipped
   - On local dev, install `python3-tk` package

4. **Directory Structure**: Generated output goes to:
   - `generated/`: Generated HTML pages from PillarPageGenerator
   - `generated_site/`: Full site structure with assets
   - `data/`: CSV data files from scrapers

5. **Python Version**: Project supports Python 3.8-3.12 (tested in CI)
   - Use Python 3.11+ for best compatibility with all dependencies

6. **Claude Code Access**: If Claude only works in this repository:
   - See [docs/CLAUDE_REPOSITORY_ACCESS.md](docs/CLAUDE_REPOSITORY_ACCESS.md) for solution
   - Issue: OAuth token needs expanded repository permissions
   - Fix: Update GitHub App installation settings

## Working with Tests

When modifying code:
1. Run `pytest` to ensure all tests pass
2. Add tests for new features in `Files/tests/` or `tests/`
3. Use `conftest.py` for shared fixtures
4. GUI tests should handle missing tkinter gracefully (see `test_gui_revenue.py` for pattern)

When tests fail:
1. Check `python3 verify_imports.py` for dependency issues
2. Run `cd Files && python3 test_system.py` for system diagnostics
3. Check if running from correct directory (some imports are path-sensitive)

## AdSense & SEO Notes

- **AdSense Integration**: Template includes Auto Ads + manual slots
  - Policy compliance checklist: `Files/adsense_policy_checklist.md`
  - Always include `ads.txt` file on deployed site

- **Schema.org Markup**: Each location gets LocalBusiness JSON-LD for rich snippets

- **Performance**: Generated pages are static HTML with client-side filtering
  - No database or server-side processing required
  - Can be deployed to any static host (Netlify, Cloudflare Pages, etc.)
