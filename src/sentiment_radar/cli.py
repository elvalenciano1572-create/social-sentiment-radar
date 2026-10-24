import argparse
import sys

from sentiment_radar.analyzer import analyze_posts
from sentiment_radar.feed import get_mock_social_feed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Autonomous real-time social sentiment analytics engine."
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        default="NVDA",
        help="Target ticker or brand keyword to scan (default: NVDA)",
    )
    args = parser.parse_args(argv)

    print("=" * 68)
    print("   SOCIAL SENTIMENT RADAR: REAL-TIME CONVERSATION ANALYTICS")
    print("=" * 68)

    posts = get_mock_social_feed(args.keyword)
    print(f"[*] Ingested {len(posts)} social posts across Twitter/X, Reddit, & Forums.")
    print(f"[*] Analyzing sentiment velocity and lexical markers for: [{args.keyword.upper()}]...")

    radar = analyze_posts(posts)

    print("\n--- RADAR SYNTHESIS REPORT ---")
    print(f"Target Symbol:        {radar.keyword}")
    print(f"Consensus Verdict:    [{radar.overall_sentiment.value}]")
    print(f"Net Sentiment Index:  {radar.net_sentiment_index:+.2f} (scale -1.0 to +1.0)")
    print(f"Viral Reach / Likes:  {radar.viral_reach:,} engagements")
    print("\nDistribution Breakdown:")
    print(f"  + Bullish: {radar.bullish_percentage}%")
    print(f"  - Bearish: {radar.bearish_percentage}%")
    print(f"  = Neutral: {radar.neutral_percentage}%")

    print("\nDominant Bullish Keywords:")
    print("  " + (", ".join(radar.top_bullish_keywords) if radar.top_bullish_keywords else "None"))

    print("Dominant Bearish Keywords:")
    print("  " + (", ".join(radar.top_bearish_keywords) if radar.top_bearish_keywords else "None"))

    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
