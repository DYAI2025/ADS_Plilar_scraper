#!/usr/bin/env python3
"""
Test suite for ReviewDemandAnalyzer

Tests both unit functionality and integration with Google Places API
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from niche_research import ReviewDemandAnalyzer


class TestReviewDemandAnalyzer:
    """Test ReviewDemandAnalyzer functionality"""

    @pytest.fixture
    def mock_api_key(self):
        """Provide a mock API key for testing"""
        return "AIzaSyDEMO_KEY_FOR_TESTING_1234567890"

    @pytest.fixture
    def analyzer(self, mock_api_key):
        """Create analyzer instance with mock API key"""
        return ReviewDemandAnalyzer(api_key=mock_api_key, delay=0.1)

    @pytest.fixture
    def sample_reviews(self):
        """Sample review data for testing"""
        return [
            {
                "place_name": "Test Park",
                "place_id": "ChIJ_TEST_123",
                "rating": 5,
                "text": "Toller Park mit viel Schatten und schönen Bänken. Sehr gut gepflegt.",
                "author": "User1",
                "time": 1234567890,
            },
            {
                "place_name": "Test Park",
                "place_id": "ChIJ_TEST_123",
                "rating": 1,
                "text": "Keine Parkplätze! Es fehlen Toiletten und zu wenig Schatten.",
                "author": "User2",
                "time": 1234567891,
            },
            {
                "place_name": "Test Park",
                "place_id": "ChIJ_TEST_123",
                "rating": 2,
                "text": "Leider keine Toiletten und schlechte Erreichbarkeit. Vermisse Spielplatz.",
                "author": "User3",
                "time": 1234567892,
            },
            {
                "place_name": "Test Park 2",
                "place_id": "ChIJ_TEST_456",
                "rating": 4,
                "text": "Schöner Spielplatz und genug Parkplätze. Empfehlenswert!",
                "author": "User4",
                "time": 1234567893,
            },
            {
                "place_name": "Test Park 2",
                "place_id": "ChIJ_TEST_456",
                "rating": 1,
                "text": "Kaputte Bänke, keine Toiletten, schlecht",
                "author": "User5",
                "time": 1234567894,
            },
        ]

    def test_initialization(self, mock_api_key):
        """Test analyzer initializes correctly"""
        analyzer = ReviewDemandAnalyzer(api_key=mock_api_key)

        assert analyzer.api_key == mock_api_key
        assert analyzer.scraper is not None
        assert len(analyzer.feature_keywords) > 0
        assert "parking" in analyzer.feature_keywords
        assert "shade" in analyzer.feature_keywords

    def test_extract_top_phrases_complaints(self, analyzer):
        """Test phrase extraction from complaint reviews"""
        complaint_texts = [
            "Keine Parkplätze verfügbar und keine Toiletten",
            "Es fehlen Toiletten und zu wenig Schatten",
            "Leider keine Toiletten vorhanden",
        ]

        phrases = analyzer._extract_top_phrases(complaint_texts, negative=True)

        assert isinstance(phrases, list)
        assert len(phrases) > 0

        # Should find "keine toiletten" as a common phrase
        phrase_texts = [p[0] for p in phrases]
        assert any("toiletten" in p for p in phrase_texts)

    def test_extract_top_phrases_praise(self, analyzer):
        """Test phrase extraction from praise reviews"""
        praise_texts = [
            "Toller Park mit viel Schatten",
            "Schöner Spielplatz und gut gepflegt",
            "Super Park, sehr empfehlenswert",
        ]

        phrases = analyzer._extract_top_phrases(praise_texts, negative=False)

        assert isinstance(phrases, list)
        assert len(phrases) > 0

        # Should find positive phrases
        phrase_texts = [p[0] for p in phrases]
        assert any("spielplatz" in p or "park" in p for p in phrase_texts)

    def test_extract_keywords(self, analyzer):
        """Test keyword extraction from reviews"""
        texts = [
            "Die Parkplätze sind immer voll und die Toiletten schmutzig",
            "Parkplatz ist zu klein, mehr Parkplätze nötig",
        ]

        keywords = analyzer._extract_keywords(texts, negative=True)

        assert isinstance(keywords, list)
        assert len(keywords) > 0

        # "parkplatz" or "parkplätze" should be top keywords
        keyword_texts = [kw[0] for kw in keywords]
        assert any("park" in kw for kw in keyword_texts)

    def test_is_too_generic(self, analyzer):
        """Test generic phrase filtering"""
        assert analyzer._is_too_generic("sehr gut") == True
        assert analyzer._is_too_generic("das ist toll") == True
        assert analyzer._is_too_generic("keine parkplätze") == False
        assert analyzer._is_too_generic("toller spielplatz") == False
        
        # Test None and empty string handling
        assert analyzer._is_too_generic(None) == True
        assert analyzer._is_too_generic("") == True
        assert analyzer._is_too_generic("   ") == True

    def test_find_unmet_needs(self, analyzer):
        """Test unmet needs detection from complaints"""
        complaints = [
            ("keine parkplätze", 10),
            ("fehlen toiletten", 8),
            ("zu wenig schatten", 5),
            ("keine spielplatz", 3),
        ]

        unmet_needs = analyzer._find_unmet_needs(complaints)

        assert isinstance(unmet_needs, list)
        # Should find parking, toilets, shade, playground
        feature_names = [feature for feature, count in unmet_needs]

        assert "parking" in feature_names
        assert "toilets" in feature_names
        assert "shade" in feature_names

    def test_analyze_review_sentiment_with_mock_data(self, analyzer, sample_reviews):
        """Test sentiment analysis with mocked review data"""

        # Mock the get_reviews_for_category method
        with patch.object(
            analyzer, "get_reviews_for_category", return_value=sample_reviews
        ):
            analysis = analyzer.analyze_review_sentiment(
                category="parks",
                city="Berlin",
                min_reviews=1,  # Low threshold for testing
                max_places=2,
            )

            assert analysis is not None
            assert analysis["total_reviews_analyzed"] == 5
            assert 0 < analysis["avg_rating"] < 5
            assert 0 < analysis["sentiment_score"] < 1

            # Should have found some complaints
            assert len(analysis["top_complaints"]) > 0

            # Should have found some praise
            assert len(analysis["top_praise"]) > 0

            # Should have detected unmet needs
            # (parking, toilets mentioned in complaints)
            unmet_features = [f for f, count in analysis["unmet_needs"]]
            assert "toilets" in unmet_features or "parking" in unmet_features

    def test_generate_content_ideas_with_mock_data(self, analyzer, sample_reviews):
        """Test content idea generation"""

        with patch.object(
            analyzer, "get_reviews_for_category", return_value=sample_reviews
        ):
            ideas = analyzer.generate_content_ideas(
                category="parks", city="Berlin", max_places=2
            )

            assert isinstance(ideas, list)
            assert len(ideas) > 0

            # Check idea structure
            for idea in ideas:
                assert "type" in idea
                assert "title" in idea
                assert "description" in idea
                assert "priority" in idea
                assert "estimated_impact" in idea
                assert "implementation" in idea

            # Should generate high priority ideas
            priorities = [idea["priority"] for idea in ideas]
            assert "High" in priorities

    def test_get_place_reviews_api_error(self, analyzer):
        """Test handling of API errors when fetching reviews"""

        # Mock API to return error status
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ZERO_RESULTS"}
        mock_response.raise_for_status = Mock()

        with patch.object(analyzer.scraper.session, "get", return_value=mock_response):
            reviews = analyzer._get_place_reviews("invalid_place_id")

            assert reviews == []

    def test_empty_reviews_handling(self, analyzer):
        """Test analyzer handles empty review lists gracefully"""

        with patch.object(analyzer, "get_reviews_for_category", return_value=[]):
            analysis = analyzer.analyze_review_sentiment(
                category="parks", city="Berlin", min_reviews=1, max_places=5
            )

            assert analysis["total_reviews_analyzed"] == 0
            assert analysis["top_complaints"] == []
            assert analysis["top_praise"] == []
            assert analysis["unmet_needs"] == []

    def test_phrase_extraction_handles_empty_text(self, analyzer):
        """Test phrase extraction with empty or None texts"""
        phrases = analyzer._extract_top_phrases([], negative=True)
        assert phrases == []

        phrases = analyzer._extract_top_phrases(["", None, "  "], negative=False)
        assert phrases == []

    def test_keyword_extraction_handles_empty_text(self, analyzer):
        """Test keyword extraction with empty texts"""
        keywords = analyzer._extract_keywords([], negative=True)
        assert keywords == []

        keywords = analyzer._extract_keywords(["", None], negative=False)
        assert keywords == []

    def test_feature_keywords_completeness(self, analyzer):
        """Test that all important features are in keyword dictionary"""
        required_features = [
            "parking",
            "shade",
            "toilets",
            "playground",
            "benches",
            "wheelchair_accessible",
            "water_fountain",
            "dog_friendly",
            "wifi",
            "outlets",
        ]

        for feature in required_features:
            assert feature in analyzer.feature_keywords
            assert len(analyzer.feature_keywords[feature]) > 0


class TestReviewDemandAnalyzerIntegration:
    """Integration tests that require real API key (skip if not available)"""

    @pytest.fixture
    def real_api_key(self):
        """Get real API key from environment"""
        return os.getenv("GOOGLE_PLACES_API_KEY")

    @pytest.fixture
    def skip_if_no_api_key(self, real_api_key):
        """Skip test if no real API key available"""
        if not real_api_key:
            pytest.skip("GOOGLE_PLACES_API_KEY not set - skipping integration test")
        return real_api_key

    def test_real_api_integration(self, skip_if_no_api_key):
        """Test with real Google Places API (requires API key)"""
        api_key = skip_if_no_api_key

        analyzer = ReviewDemandAnalyzer(api_key=api_key, delay=1.5)

        # Use a small city and low max_places to minimize API quota usage
        analysis = analyzer.analyze_review_sentiment(
            category="parks",
            city="Potsdam",  # Smaller city = fewer results
            min_reviews=10,  # Low threshold
            max_places=5,  # Only analyze 5 places
        )

        assert analysis is not None
        assert analysis["total_reviews_analyzed"] >= 0

        # If reviews were found, check structure
        if analysis["total_reviews_analyzed"] > 0:
            assert 0 <= analysis["avg_rating"] <= 5
            assert 0 <= analysis["sentiment_score"] <= 1

            print(f"\n✅ Real API Integration Test Results:")
            print(f"   Reviews analyzed: {analysis['total_reviews_analyzed']}")
            print(f"   Avg rating: {analysis['avg_rating']:.2f}")
            print(f"   Top complaints: {len(analysis['top_complaints'])}")
            print(f"   Unmet needs: {len(analysis['unmet_needs'])}")


def test_cli_import():
    """Test that CLI script can be imported without errors"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        import analyze_demand

        assert hasattr(analyze_demand, "main")
    except ImportError as e:
        pytest.fail(f"Failed to import CLI script: {e}")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
