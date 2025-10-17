#!/usr/bin/env python3
"""
ADS Pillar - SEO & Analytics Setup Script
Automatisiert die technischen Setup-Schritte für eine neue Pillar-Site
"""

import json
import os
from pathlib import Path
from typing import Dict, List
import xml.etree.ElementTree as ET
from datetime import datetime


class SEOSetup:
    """Handle SEO-related setup tasks"""

    def __init__(self, domain: str, site_name: str):
        self.domain = domain
        self.site_name = site_name

    def generate_robots_txt(self) -> str:
        """Generate robots.txt for SEO"""
        return f"""User-agent: *
Allow: /

# Sitemap location
Sitemap: https://{self.domain}/sitemap.xml

# Block admin/private areas if applicable
Disallow: /admin/
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/plugins/

# Allow all static assets
Allow: /wp-content/uploads/
Allow: *.css
Allow: *.js
Allow: *.png
Allow: *.jpg
Allow: *.jpeg
Allow: *.gif
Allow: *.webp

# Block search/filter parameters to avoid duplicate content
Disallow: /*?*
Disallow: /*&*
"""

    def generate_sitemap(self, pages: List[Dict]) -> str:
        """Generate XML sitemap"""

        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        urlset.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")

        for page in pages:
            url = ET.SubElement(urlset, "url")

            loc = ET.SubElement(url, "loc")
            loc.text = f"https://{self.domain}{page['path']}"

            lastmod = ET.SubElement(url, "lastmod")
            lastmod.text = page.get("lastmod", datetime.now().strftime("%Y-%m-%d"))

            changefreq = ET.SubElement(url, "changefreq")
            changefreq.text = page.get("changefreq", "weekly")

            priority = ET.SubElement(url, "priority")
            priority.text = str(page.get("priority", 0.8))

        return ET.tostring(urlset, encoding="unicode", xml_declaration=True)

    def generate_meta_tags(self, page_data: Dict) -> str:
        """Generate meta tags for a page"""

        city = page_data.get("city", "")
        category = page_data.get("category", "")
        count = page_data.get("location_count", 0)

        title = f"{category} in {city} | {self.site_name}"
        description = f"Finde die besten {category} in {city}. {count}+ Orte mit detaillierten Informationen zu Ausstattung, Bewertungen und Öffnungszeiten."

        return f"""
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{category}, {city}, Verzeichnis, Bewertungen, Ausstattung">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://{self.domain}{page_data.get('path', '')}">
    <meta property="og:site_name" content="{self.site_name}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    
    <!-- Geo Tags -->
    <meta name="geo.region" content="DE-{page_data.get('region_code', 'BE')}">
    <meta name="geo.placename" content="{city}">
    <meta name="ICBM" content="{page_data.get('lat', '')}, {page_data.get('lon', '')}">"""


class AnalyticsSetup:
    """Handle analytics and tracking setup"""

    def generate_gtag_code(self, ga_id: str, adsense_id: str) -> str:
        """Generate Google Analytics + AdSense tracking code"""

        return f"""
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{ga_id}', {{
    // Enhanced measurement for better insights
    'enhanced_measurement': true,
    // Track file downloads
    'track_file_downloads': true,
    // Track outbound clicks
    'track_outbound_clicks': true
  }});
  
  // Custom events for filter usage
  function trackFilterUsage(filterName) {{
    gtag('event', 'filter_used', {{
      'event_category': 'engagement',
      'event_label': filterName,
      'page_title': document.title
    }});
  }}
  
  // Track AdSense performance
  gtag('config', '{adsense_id}', {{
    'send_page_view': false
  }});
</script>

<!-- AdSense Auto ads -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_id}"
        crossorigin="anonymous"></script>
<script>
  // Enhanced AdSense tracking
  (adsbygoogle = window.adsbygoogle || []).push({{
    google_ad_client: "{adsense_id}",
    enable_page_level_ads: true,
    overlays: {{bottom: true}}
  }});
</script>"""

    def generate_schema_markup(
        self, location_data: List[Dict], city: str, category: str
    ) -> str:
        """Generate JSON-LD schema markup"""

        # Main ItemList schema
        schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": f"{category} in {city}",
            "description": f"Kuratierte Liste der besten {category} in {city} mit detaillierten Informationen.",
            "numberOfItems": len(location_data),
            "itemListElement": [],
        }

        for i, location in enumerate(location_data):
            item = {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "LocalBusiness",
                    "name": location.get("name", ""),
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": location.get("street", ""),
                        "addressLocality": location.get("city", ""),
                        "postalCode": location.get("postcode", ""),
                        "addressCountry": "DE",
                    },
                    "geo": {
                        "@type": "GeoCoordinates",
                        "latitude": location.get("latitude", 0),
                        "longitude": location.get("longitude", 0),
                    },
                },
            }

            # Add optional fields if available
            if location.get("url"):
                item["item"]["url"] = location["url"]
            if location.get("phone"):
                item["item"]["telephone"] = location["phone"]
            if location.get("rating", 0) > 0:
                item["item"]["aggregateRating"] = {
                    "@type": "AggregateRating",
                    "ratingValue": location["rating"],
                    "reviewCount": location.get("review_count", 1),
                }

            schema["itemListElement"].append(item)

        return json.dumps(schema, ensure_ascii=False, indent=2)


class ProjectSetup:
    """Main project setup coordinator"""

    def __init__(self, project_config: Dict):
        self.config = project_config
        self.seo = SEOSetup(project_config["domain"], project_config["site_name"])
        self.analytics = AnalyticsSetup()

    def create_project_structure(self, base_path: str = "."):
        """Create complete project file structure"""

        base = Path(base_path)

        # Create directory structure
        directories = [
            "assets/css",
            "assets/js",
            "assets/images",
            "data",
            "templates",
            "generated",
            "logs",
        ]

        for directory in directories:
            (base / directory).mkdir(parents=True, exist_ok=True)

        print(f"✅ Created project structure in {base.absolute()}")

    def generate_config_files(self, output_dir: str = "."):
        """Generate all configuration files"""

        output_path = Path(output_dir)

        # 1. robots.txt
        robots_content = self.seo.generate_robots_txt()
        with open(output_path / "robots.txt", "w") as f:
            f.write(robots_content)

        # 2. ads.txt (if AdSense ID provided)
        if self.config.get("adsense_id"):
            ads_content = (
                f"google.com, {self.config['adsense_id']}, DIRECT, f08c47fec0942fa0\n"
            )
            with open(output_path / "ads.txt", "w") as f:
                f.write(ads_content)

        # 3. Sample sitemap structure
        sample_pages = [
            {"path": "/", "priority": 1.0, "changefreq": "weekly"},
            {
                "path": f"/{self.config.get('main_category', 'places')}/",
                "priority": 0.9,
            },
            {"path": "/about/", "priority": 0.3, "changefreq": "monthly"},
            {"path": "/contact/", "priority": 0.3, "changefreq": "monthly"},
        ]

        sitemap_content = self.seo.generate_sitemap(sample_pages)
        with open(output_path / "sitemap.xml", "w") as f:
            f.write(sitemap_content)

        # 4. Analytics configuration
        if self.config.get("ga_id") and self.config.get("adsense_id"):
            analytics_code = self.analytics.generate_gtag_code(
                self.config["ga_id"], self.config["adsense_id"]
            )
            with open(output_path / "analytics_snippet.html", "w") as f:
                f.write(analytics_code)

        # 5. Project configuration
        config_file = {
            "project": self.config,
            "setup_date": datetime.now().isoformat(),
            "next_steps": [
                "Add location data to data/ directory",
                "Customize pillar_page_skeleton.html",
                "Test AdSense ad placements",
                "Submit sitemap to Google Search Console",
                "Set up Google Analytics goals",
                "Configure DSGVO-compliant cookie consent",
            ],
        }

        with open(output_path / "project_config.json", "w") as f:
            json.dump(config_file, f, indent=2, ensure_ascii=False)

        print(f"✅ Generated configuration files in {output_path.absolute()}")

    def create_deployment_script(self, output_dir: str = "."):
        """Create deployment script for going live"""

        script_content = f"""#!/bin/bash
# ADS Pillar - Deployment Script
# Automated deployment for {self.config['site_name']}

set -e

echo "🚀 Deploying {self.config['site_name']}..."

# 1. Build checks
echo "📋 Pre-deployment checks..."
if [ ! -f "robots.txt" ]; then
    echo "❌ robots.txt missing"
    exit 1
fi

if [ ! -f "ads.txt" ]; then
    echo "❌ ads.txt missing"
    exit 1
fi

if [ ! -f "sitemap.xml" ]; then
    echo "❌ sitemap.xml missing"
    exit 1
fi

# 2. Upload to server (adjust for your hosting)
echo "📤 Uploading files..."
# rsync -avz --exclude='.git' . user@yourserver.com:/var/www/html/

# 3. Set permissions
echo "🔒 Setting permissions..."
# ssh user@yourserver.com "chmod -R 644 /var/www/html/*.html"
# ssh user@yourserver.com "chmod -R 644 /var/www/html/*.txt"

# 4. Submit sitemap to Google
echo "🗺️  Submitting sitemap..."
curl -X POST "https://www.google.com/ping?sitemap=https://{self.config['domain']}/sitemap.xml"

# 5. Ping search engines
echo "📡 Notifying search engines..."
curl -X POST "https://www.bing.com/ping?sitemap=https://{self.config['domain']}/sitemap.xml"

echo "✅ Deployment completed!"
echo "🔗 Visit: https://{self.config['domain']}"
echo "📊 Analytics: https://analytics.google.com"
echo "💰 AdSense: https://www.google.com/adsense"

echo ""
echo "📝 Next steps:"
echo "1. Submit site to Google Search Console"
echo "2. Set up Google Analytics goals"
echo "3. Monitor AdSense policy compliance"
echo "4. Track keyword rankings"
"""

        script_path = Path(output_dir) / "deploy.sh"
        with open(script_path, "w") as f:
            f.write(script_content)

        # Make executable
        script_path.chmod(0o755)

        print(f"✅ Created deployment script: {script_path.absolute()}")


def main():
    """Setup a new ADS Pillar project"""

    print("🏗️  ADS Pillar - Project Setup")
    print("=" * 50)

    # Example configuration
    project_config = {
        "site_name": "Local Places Guide",
        "domain": "your-domain.com",
        "main_category": "parks",
        "target_city": "Berlin",
        "ga_id": "GA_MEASUREMENT_ID",  # Replace with real GA4 ID
        "adsense_id": "ca-pub-XXXXXXXXXXXXXXXX",  # Replace with real AdSense ID
        "language": "de",
        "country": "DE",
    }

    # Initialize setup
    setup = ProjectSetup(project_config)

    # Run setup steps
    setup.create_project_structure()
    setup.generate_config_files()
    setup.create_deployment_script()

    print("\n🎉 Setup completed!")
    print("\n📋 Generated files:")
    print("   • robots.txt - SEO crawling rules")
    print("   • ads.txt - AdSense authorization")
    print("   • sitemap.xml - Search engine sitemap")
    print("   • analytics_snippet.html - Tracking code")
    print("   • project_config.json - Project settings")
    print("   • deploy.sh - Deployment script")

    print("\n🔧 Customize these files:")
    print(f"   • Replace 'your-domain.com' with {project_config['domain']}")
    print(f"   • Add real Google Analytics ID")
    print(f"   • Add real AdSense Publisher ID")
    print(f"   • Update deployment script for your hosting")

    print("\n🚀 Next steps:")
    print("   1. Run niche_research.py to validate your niche")
    print("   2. Collect location data with data_pipeline.py")
    print("   3. Generate pillar pages from templates")
    print("   4. Test everything locally")
    print("   5. Deploy with ./deploy.sh")


if __name__ == "__main__":
    main()
