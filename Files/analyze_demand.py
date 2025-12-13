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

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from niche_research import ReviewDemandAnalyzer


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
        # Store analysis results to avoid redundant API calls
        analysis = None
        ideas = None

        if args.quiet:
            # Quick analysis without detailed report
            analysis = analyzer.analyze_review_sentiment(
                category=args.category,
                city=args.city,
                min_reviews=args.min_reviews,
                max_places=args.max_places,
            )

            ideas = analyzer.generate_content_ideas(
                category=args.category, city=args.city, max_places=args.max_places
            )

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
            # Full detailed report
            analyzer.print_analysis_report(
                category=args.category, city=args.city, max_places=args.max_places
            )

        # Save to JSON if requested
        if args.output:
            # Reuse analysis results if already computed, otherwise compute them
            if analysis is None:
                analysis = analyzer.analyze_review_sentiment(
                    category=args.category,
                    city=args.city,
                    min_reviews=args.min_reviews,
                    max_places=args.max_places,
                )

            if ideas is None:
                ideas = analyzer.generate_content_ideas(
                    category=args.category, city=args.city, max_places=args.max_places
                )

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
