#!/usr/bin/env python3
"""
CLI tool for Review-Based Demand Analysis

Usage:
    python analyze_demand.py --category "parks" --city "Berlin" --api-key YOUR_KEY
    python analyze_demand.py --category "cafes" --city "München" --api-key YOUR_KEY --max-places 20
"""

import argparse
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from niche_research import ReviewDemandAnalyzer


def _print_detailed_report(analysis: Dict[str, Any], ideas: List[Dict[str, Any]], category: str, city: str):
    """
    Print a detailed analysis report using pre-computed analysis and ideas.
    This avoids redundant API calls when results are already available.
    """
    print(f"\n{'='*70}")
    print(f"📊 REVIEW DEMAND ANALYSIS REPORT")
    print(f"{'='*70}")
    print(f"Category: {category.title()}")
    print(f"Location: {city}")
    print(f"{'='*70}\n")

    if analysis["total_reviews_analyzed"] == 0:
        print("❌ No data available for analysis\n")
        return

    # Summary stats
    print(f"📈 SUMMARY STATISTICS")
    print(f"{'-'*70}")
    print(f"Total Reviews Analyzed: {analysis['total_reviews_analyzed']}")
    print(f"Average Rating: {analysis['avg_rating']:.2f} / 5.0")
    print(f"Sentiment Score: {analysis['sentiment_score']:.2f} (0.0 = very negative, 1.0 = very positive)")
    print()

    # Top complaints
    print(f"🔴 TOP COMPLAINTS (What Users Are Missing)")
    print(f"{'-'*70}")
    for i, (phrase, count) in enumerate(analysis["top_complaints"][:10], 1):
        print(f"  {i:2d}. '{phrase}' ({count} mentions)")
    print()

    # Top praise
    print(f"🟢 TOP PRAISE (What Users Love)")
    print(f"{'-'*70}")
    for i, (phrase, count) in enumerate(analysis["top_praise"][:10], 1):
        print(f"  {i:2d}. '{phrase}' ({count} mentions)")
    print()

    # Unmet needs
    print(f"💡 UNMET NEEDS (Opportunity Features!)")
    print(f"{'-'*70}")
    if analysis["unmet_needs"]:
        for i, (feature, count) in enumerate(analysis["unmet_needs"], 1):
            print(f"  {i:2d}. {feature.upper()} - {count} complaint mentions ⭐⭐⭐")
    else:
        print("  None detected - all needs seem to be met")
    print()

    # Content ideas
    print(f"🎯 ACTIONABLE CONTENT IDEAS")
    print(f"{'-'*70}")
    for i, idea in enumerate(ideas, 1):
        print(f"\n{i}. [{idea['priority'].upper()}] {idea['type']}: {idea['title']}")
        print(f"   Description: {idea['description']}")
        print(f"   Impact: {idea['estimated_impact']}")
        print(f"   Implementation:")
        for line in idea['implementation'].split('\n'):
            print(f"     • {line.strip()}")

    print(f"\n{'='*70}")
    print(f"✨ Analysis complete! Use these insights to create high-performing pillar pages.")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Google Places reviews to find hidden user demands and content opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze parks in Berlin
  python analyze_demand.py --category "parks" --city "Berlin" --api-key YOUR_API_KEY

  # Analyze cafes in München with limited API calls
  python analyze_demand.py --category "cafes" --city "München" --api-key YOUR_API_KEY --max-places 15

  # Use API key from environment variable
  export GOOGLE_PLACES_API_KEY=your_key_here
  python analyze_demand.py --category "restaurants" --city "Hamburg"

  # Save results to JSON file
  python analyze_demand.py --category "parks" --city "Potsdam" --output results.json
        """,
    )

    parser.add_argument(
        "--category",
        required=True,
        help="Category to analyze (e.g., 'parks', 'cafes', 'restaurants')",
    )

    parser.add_argument(
        "--city",
        required=True,
        help="City to analyze (e.g., 'Berlin', 'München', 'Hamburg')",
    )

    parser.add_argument(
        "--api-key",
        help="Google Places API key (or set GOOGLE_PLACES_API_KEY environment variable)",
    )

    parser.add_argument(
        "--max-places",
        type=int,
        default=30,
        help="Maximum number of places to analyze (default: 30, affects API quota usage)",
    )

    parser.add_argument(
        "--min-reviews",
        type=int,
        default=100,
        help="Minimum number of reviews needed for reliable analysis (default: 100)",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between API calls in seconds (default: 1.0)",
    )

    parser.add_argument("--output", "-o", help="Save results to JSON file (optional)")

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress detailed output, only show summary",
    )

    args = parser.parse_args()

    # Get API key from args or environment
    api_key = args.api_key or os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        print("❌ Error: Google Places API key required!")
        print(
            "   Provide via --api-key or set GOOGLE_PLACES_API_KEY environment variable"
        )
        print("\n   Example:")
        print("   export GOOGLE_PLACES_API_KEY=your_key_here")
        print("   python analyze_demand.py --category parks --city Berlin")
        sys.exit(1)

    # Validate API key format (basic check)
    if len(api_key) < 20:
        print("⚠️  Warning: API key seems too short, it may be invalid")

    if not args.quiet:
        print("\n" + "=" * 70)
        print("🚀 REVIEW-BASED DEMAND ANALYZER")
        print("=" * 70)
        print(f"Category: {args.category}")
        print(f"City: {args.city}")
        print(f"Max Places: {args.max_places}")
        print(f"Min Reviews: {args.min_reviews}")
        print("=" * 70 + "\n")

    # Initialize analyzer
    try:
        analyzer = ReviewDemandAnalyzer(api_key=api_key, delay=args.delay)
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        sys.exit(1)

    # Run analysis
    try:
        # Always run analysis once and cache results to avoid redundant API calls
        try:
            analysis = analyzer.analyze_review_sentiment(
                category=args.category,
                city=args.city,
                min_reviews=args.min_reviews,
                max_places=args.max_places,
            )
        except Exception as e:
            print(f"\n❌ Error during sentiment analysis: {e}")
            raise

        try:
            ideas = analyzer.generate_content_ideas(
                category=args.category, city=args.city, max_places=args.max_places
            )
        except Exception as e:
            print(f"\n❌ Error generating content ideas: {e}")
            raise
        
        # Display results based on quiet mode
        if args.quiet:
            # Print summary only
            print(f"\n📊 ANALYSIS SUMMARY")
            print(f"   Reviews Analyzed: {analysis['total_reviews_analyzed']}")
            print(f"   Avg Rating: {analysis['avg_rating']:.2f}/5.0")
            print(
                f"   Top Complaint: {analysis['top_complaints'][0][0] if analysis['top_complaints'] else 'N/A'}"
            )
            print(
                f"   Top Unmet Need: {analysis['unmet_needs'][0][0] if analysis['unmet_needs'] else 'N/A'}"
            )
            print(f"   Content Ideas Generated: {len(ideas)}\n")

        else:
            # Print full detailed report using cached data
            _print_detailed_report(analysis, ideas, args.category, args.city)

        # Save to JSON if requested (reusing cached results)
        if args.output:

            output_data = {
                "category": args.category,
                "city": args.city,
                "analysis": analysis,
                "content_ideas": ideas,
                "parameters": {
                    "max_places": args.max_places,
                    "min_reviews": args.min_reviews,
                },
            }

            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            print(f"💾 Results saved to: {output_path}")

        print("\n✅ Analysis complete!\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
