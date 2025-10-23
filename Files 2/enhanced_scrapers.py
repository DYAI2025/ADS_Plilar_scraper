#!/usr/bin/env python3
"""
Enhanced Data Scrapers for ADS Pillar
Unterstützt multiple Datenquellen und automatische Feature-Extraktion
"""

import requests
import pandas as pd
import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapedLocation:
    """Standardized location data structure"""
    name: str
    address: str
    city: str
    latitude: float = 0.0
    longitude: float = 0.0
    rating: float = 0.0
    review_count: int = 0
    phone: str = ""
    website: str = ""
    opening_hours: str = ""
    price_level: int = 0
    categories: List[str] = None
    reviews_text: str = ""
    photos: List[str] = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = []
        if self.photos is None:
            self.photos = []

class GooglePlacesScraper:
    """Enhanced Google Places API scraper"""
    
    def __init__(self, api_key: str, delay: float = 1.0):
        self.api_key = api_key
        self.delay = delay
        self.session = requests.Session()
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    def search_places(self, query: str, location: str, radius: int = 50000) -> List[ScrapedLocation]:
        """Search for places using text search"""
        
        url = f"{self.base_url}/textsearch/json"
        params = {
            'query': f"{query} in {location}",
            'key': self.api_key,
            'radius': radius
        }
        
        all_places = []
        next_page_token = None
        
        while True:
            if next_page_token:
                params['pagetoken'] = next_page_token
                time.sleep(2)  # Required delay for page token
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data['status'] != 'OK':
                    logger.warning(f"API returned status: {data['status']}")
                    break
                
                # Process results
                for place in data.get('results', []):
                    location_obj = self._parse_place_basic(place)
                    if location_obj:
                        all_places.append(location_obj)
                
                # Check for next page
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                    
                logger.info(f"Found {len(data.get('results', []))} places, continuing...")
                
            except Exception as e:
                logger.error(f"Error searching places: {e}")
                break
                
            time.sleep(self.delay)
        
        logger.info(f"Total places found: {len(all_places)}")
        return all_places
    
    def enrich_places(self, places: List[ScrapedLocation]) -> List[ScrapedLocation]:
        """Enrich places with detailed information"""
        
        enriched_places = []
        
        for i, place in enumerate(places):
            logger.info(f"Enriching place {i+1}/{len(places)}: {place.name}")
            
            try:
                # Get place details (would need place_id from search)
                # This is a simplified version
                enriched_place = place
                enriched_places.append(enriched_place)
                
            except Exception as e:
                logger.error(f"Error enriching place {place.name}: {e}")
                enriched_places.append(place)  # Add original if enrichment fails
            
            time.sleep(self.delay)
        
        return enriched_places
    
    def _parse_place_basic(self, place_data: Dict) -> Optional[ScrapedLocation]:
        """Parse basic place data from API response"""
        
        try:
            geometry = place_data.get('geometry', {})
            location = geometry.get('location', {})
            
            return ScrapedLocation(
                name=place_data.get('name', ''),
                address=place_data.get('formatted_address', ''),
                city=self._extract_city_from_address(place_data.get('formatted_address', '')),
                latitude=location.get('lat', 0.0),
                longitude=location.get('lng', 0.0),
                rating=place_data.get('rating', 0.0),
                review_count=place_data.get('user_ratings_total', 0),
                price_level=place_data.get('price_level', 0),
                categories=place_data.get('types', [])
            )
            
        except Exception as e:
            logger.error(f"Error parsing place data: {e}")
            return None
    
    def _extract_city_from_address(self, address: str) -> str:
        """Extract city name from formatted address"""
        if not address:
            return ""
        
        # Simple regex for German addresses
        city_match = re.search(r'\d{5}\s+([^,]+)', address)
        if city_match:
            return city_match.group(1).strip()
        
        return ""

class WebScraper:
    """Generic web scraper for location data"""
    
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_yelp_style(self, base_url: str, search_params: Dict) -> List[ScrapedLocation]:
        """Scrape Yelp-style directory sites"""
        
        places = []
        page = 1
        max_pages = 10
        
        while page <= max_pages:
            try:
                params = search_params.copy()
                params['start'] = (page - 1) * 10  # Typical pagination
                
                response = self.session.get(base_url, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_places = self._extract_yelp_places(soup)
                
                if not page_places:
                    break
                
                places.extend(page_places)
                logger.info(f"Scraped page {page}: {len(page_places)} places")
                
                page += 1
                time.sleep(self.delay)
                
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                break
        
        return places
    
    def _extract_yelp_places(self, soup: BeautifulSoup) -> List[ScrapedLocation]:
        """Extract places from Yelp-style HTML"""
        
        places = []
        
        # This would need to be adapted for specific websites
        # Generic selectors for common directory sites
        business_cards = soup.find_all(['div', 'article'], class_=re.compile(r'business|listing|card'))
        
        for card in business_cards:
            try:
                place = self._parse_business_card(card)
                if place:
                    places.append(place)
            except Exception as e:
                logger.warning(f"Error parsing business card: {e}")
                continue
        
        return places
    
    def _parse_business_card(self, card: BeautifulSoup) -> Optional[ScrapedLocation]:
        """Parse individual business card HTML"""
        
        try:
            # Extract name
            name_elem = card.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'name|title'))
            name = name_elem.get_text().strip() if name_elem else ""
            
            # Extract address
            address_elem = card.find(['div', 'span'], class_=re.compile(r'address|location'))
            address = address_elem.get_text().strip() if address_elem else ""
            
            # Extract rating
            rating_elem = card.find(['div', 'span'], class_=re.compile(r'rating|stars'))
            rating = self._extract_rating(rating_elem) if rating_elem else 0.0
            
            if name and address:
                return ScrapedLocation(
                    name=name,
                    address=address,
                    city=self._extract_city_from_address(address),
                    rating=rating
                )
            
        except Exception as e:
            logger.error(f"Error parsing business card: {e}")
        
        return None
    
    def _extract_rating(self, rating_elem) -> float:
        """Extract numerical rating from HTML element"""
        
        if not rating_elem:
            return 0.0
        
        text = rating_elem.get_text()
        
        # Look for patterns like "4.5 stars", "Rating: 4.2", etc.
        rating_match = re.search(r'(\d+\.?\d*)', text)
        if rating_match:
            return float(rating_match.group(1))
        
        return 0.0

class CSVDataLoader:
    """Load and validate CSV data"""
    
    @staticmethod
    def load_csv(filepath: str) -> List[ScrapedLocation]:
        """Load locations from CSV file"""
        
        try:
            df = pd.read_csv(filepath)
            places = []
            
            for _, row in df.iterrows():
                place = ScrapedLocation(
                    name=row.get('name', ''),
                    address=row.get('address', ''),
                    city=row.get('city', ''),
                    latitude=float(row.get('latitude', 0.0)),
                    longitude=float(row.get('longitude', 0.0)),
                    rating=float(row.get('rating', 0.0)),
                    review_count=int(row.get('review_count', 0)),
                    phone=row.get('phone', ''),
                    website=row.get('website', ''),
                    opening_hours=row.get('opening_hours', '')
                )
                places.append(place)
            
            logger.info(f"Loaded {len(places)} places from CSV")
            return places
            
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return []

class SmartFeatureExtractor:
    """Advanced feature extraction from text data"""
    
    FEATURE_PATTERNS = {
        'shade': [
            r'schatten\w*', r'schattig', r'bäume', r'baum', r'überdacht',
            r'shadow\w*', r'shade\w*', r'tree\w*', r'covered'
        ],
        'water': [
            r'wasser', r'brunnen', r'teich', r'see\b', r'bach', r'fluss',
            r'water', r'fountain', r'pond', r'lake', r'river', r'stream'
        ],
        'parking': [
            r'parkplatz', r'parken', r'stellplatz', r'garage',
            r'parking', r'park\s', r'lot\b'
        ],
        'toilets': [
            r'toilette\w*', r'wc\b', r'klo\b', r'sanitär',
            r'toilet\w*', r'restroom\w*', r'bathroom\w*', r'washroom\w*'
        ],
        'wheelchair': [
            r'rollstuhl', r'barriere\w*', r'behinderten\w*',
            r'wheelchair', r'accessible', r'handicap\w*', r'disabled'
        ],
        'dogs': [
            r'hund\w*', r'tier\w*', r'haustier\w*',
            r'dog\w*', r'pet\w*', r'animal\w*'
        ],
        'kids': [
            r'kind\w*', r'spielplatz', r'familie\w*', r'baby\w*',
            r'kid\w*', r'child\w*', r'family', r'playground', r'baby'
        ],
        'free': [
            r'kostenlos', r'gratis', r'frei\b', r'umsonst', r'ohne\s+kosten',
            r'free\b', r'no\s+charge', r'no\s+fee', r'complimentary'
        ]
    }
    
    @classmethod
    def extract_features(cls, text: str, reviews: str = "") -> Dict[str, bool]:
        """Extract boolean features from text and reviews"""
        
        combined_text = f"{text} {reviews}".lower()
        features = {}
        
        for feature_name, patterns in cls.FEATURE_PATTERNS.items():
            feature_found = False
            
            for pattern in patterns:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    feature_found = True
                    break
            
            # Map to standard feature names
            feature_key = f"feature_{feature_name}"
            if feature_name == 'free':
                feature_key = 'feature_fee'
                feature_found = not feature_found  # Invert for fee
            
            features[feature_key] = feature_found
        
        return features
    
    @classmethod
    def analyze_sentiment(cls, reviews: str) -> Dict[str, float]:
        """Basic sentiment analysis of reviews"""
        
        if not reviews:
            return {'sentiment_score': 0.5, 'confidence': 0.0}
        
        # Simple keyword-based sentiment
        positive_words = [
            'gut', 'toll', 'schön', 'empfehlen', 'perfekt', 'ausgezeichnet',
            'good', 'great', 'nice', 'recommend', 'perfect', 'excellent'
        ]
        
        negative_words = [
            'schlecht', 'schrecklich', 'nicht empfehlen', 'katastrophe',
            'bad', 'terrible', 'awful', 'horrible', 'worst'
        ]
        
        text_lower = reviews.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = len(reviews.split())
        
        if total_words == 0:
            return {'sentiment_score': 0.5, 'confidence': 0.0}
        
        sentiment_score = 0.5 + (positive_count - negative_count) / (total_words * 2)
        sentiment_score = max(0.0, min(1.0, sentiment_score))
        
        confidence = (positive_count + negative_count) / total_words
        confidence = min(1.0, confidence)
        
        return {
            'sentiment_score': sentiment_score,
            'confidence': confidence
        }

class UniversalScraper:
    """Main scraper class that combines all data sources"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Initialize scrapers based on config
        if config.get('google_api_key'):
            self.google_scraper = GooglePlacesScraper(
                api_key=config['google_api_key'],
                delay=config.get('delay', 1.0)
            )
        else:
            self.google_scraper = None
        
        self.web_scraper = WebScraper(delay=config.get('delay', 2.0))
        self.feature_extractor = SmartFeatureExtractor()
    
    def collect_all_data(self, query: str, location: str) -> List[Dict]:
        """Collect data from all available sources"""
        
        all_places = []
        
        # Google Places API
        if self.google_scraper:
            logger.info("Collecting from Google Places API...")
            google_places = self.google_scraper.search_places(query, location)
            all_places.extend(google_places)
        
        # CSV files (if specified)
        csv_files = self.config.get('csv_files', [])
        for csv_file in csv_files:
            logger.info(f"Loading from CSV: {csv_file}")
            csv_places = CSVDataLoader.load_csv(csv_file)
            all_places.extend(csv_places)
        
        # Deduplicate based on name and address
        unique_places = self._deduplicate_places(all_places)
        
        # Extract features for all places
        enriched_places = []
        for place in unique_places:
            features = self.feature_extractor.extract_features(
                f"{place.name} {place.address}",
                place.reviews_text
            )
            
            # Convert to dictionary format
            place_dict = {
                'name': place.name,
                'address': place.address,
                'city': place.city,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'rating': place.rating,
                'review_count': place.review_count,
                'phone': place.phone,
                'website': place.website,
                'opening_hours': place.opening_hours,
                **features
            }
            
            enriched_places.append(place_dict)
        
        logger.info(f"Collected and processed {len(enriched_places)} unique places")
        return enriched_places
    
    def _deduplicate_places(self, places: List[ScrapedLocation]) -> List[ScrapedLocation]:
        """Remove duplicate places based on name and address similarity"""
        
        unique_places = []
        seen = set()
        
        for place in places:
            # Create a normalized key for deduplication
            key = f"{place.name.lower().strip()}_{place.address.lower().strip()}"
            key = re.sub(r'\s+', ' ', key)  # Normalize whitespace
            
            if key not in seen:
                seen.add(key)
                unique_places.append(place)
            else:
                logger.debug(f"Duplicate found: {place.name}")
        
        logger.info(f"Removed {len(places) - len(unique_places)} duplicates")
        return unique_places

# Example usage and testing
def main():
    """Test the enhanced scrapers"""
    
    # Configuration
    config = {
        'google_api_key': 'YOUR_API_KEY_HERE',  # Replace with real key
        'delay': 1.0,
        'csv_files': ['data/sample_data.csv']  # Optional CSV files
    }
    
    # Initialize scraper
    scraper = UniversalScraper(config)
    
    # Collect data
    places = scraper.collect_all_data(
        query="parks",
        location="Berlin"
    )
    
    # Save results
    if places:
        df = pd.DataFrame(places)
        df.to_csv('data/scraped_places.csv', index=False)
        print(f"✅ Saved {len(places)} places to scraped_places.csv")
        
        # Show sample features
        print("\n📊 Sample feature extraction:")
        for place in places[:3]:
            print(f"\n{place['name']}:")
            features = {k: v for k, v in place.items() if k.startswith('feature_')}
            for feature, value in features.items():
                if value:
                    print(f"  ✓ {feature.replace('feature_', '').title()}")
    
    else:
        print("❌ No places found. Check API key and query.")

if __name__ == "__main__":
    main()
