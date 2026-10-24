import re

from sentiment_radar.models import (
    AggregatedSentimentRadar,
    ScoredPost,
    SentimentClass,
    SocialPost,
)

BULLISH_KEYWORDS = [
    "buy", "long", "moon", "breakout", "accumulate", "bullish", "growth",
    "profit", "earnings beat", "undervalued", "rally", "solid", "call", "all-in"
]

BEARISH_KEYWORDS = [
    "sell", "short", "dump", "crash", "overvalued", "bearish", "loss",
    "earnings miss", "scam", "drop", "downside", "puts", "recession", "bankrupt"
]


def score_text_sentiment(text: str) -> tuple[SentimentClass, float, list[str]]:
    """Analyzes text for bullish/bearish lexical markers and calculates sentiment score (-1 to +1)."""
    text_lower = text.lower()
    words = set(re.findall(r"\b\w+\b", text_lower))

    found_bullish = [w for w in BULLISH_KEYWORDS if w in words or w in text_lower]
    found_bearish = [w for w in BEARISH_KEYWORDS if w in words or w in text_lower]

    bull_count = len(found_bullish)
    bear_count = len(found_bearish)

    total_matches = bull_count + bear_count

    if total_matches == 0:
        return SentimentClass.NEUTRAL, 0.0, []

    score = (bull_count - bear_count) / total_matches

    if score > 0.2:
        return SentimentClass.BULLISH, round(score, 2), found_bullish
    elif score < -0.2:
        return SentimentClass.BEARISH, round(score, 2), found_bearish
    else:
        return SentimentClass.NEUTRAL, round(score, 2), found_bullish + found_bearish


def analyze_posts(posts: list[SocialPost]) -> AggregatedSentimentRadar:
    if not posts:
        raise ValueError("Cannot analyze empty posts collection.")

    scored: list[ScoredPost] = []
    bull_keys: set[str] = set()
    bear_keys: set[str] = set()
    total_reach = sum(p.upvotes_or_likes for p in posts)
    keyword = posts[0].target_keyword

    for post in posts:
        sentiment, score, themes = score_text_sentiment(post.text)
        scored.append(
            ScoredPost(
                post=post,
                sentiment=sentiment,
                confidence_score=min(1.0, 0.5 + 0.1 * len(themes)),
                sentiment_score=score,
                key_themes=themes,
            )
        )
        if sentiment == SentimentClass.BULLISH:
            bull_keys.update(themes)
        elif sentiment == SentimentClass.BEARISH:
            bear_keys.update(themes)

    total = len(scored)
    bull_count = sum(1 for s in scored if s.sentiment == SentimentClass.BULLISH)
    bear_count = sum(1 for s in scored if s.sentiment == SentimentClass.BEARISH)
    neutral_count = total - bull_count - bear_count

    avg_score = sum(s.sentiment_score for s in scored) / total

    if avg_score > 0.15:
        overall = SentimentClass.BULLISH
    elif avg_score < -0.15:
        overall = SentimentClass.BEARISH
    else:
        overall = SentimentClass.NEUTRAL

    return AggregatedSentimentRadar(
        keyword=keyword,
        total_posts=total,
        bullish_percentage=round((bull_count / total) * 100, 1),
        bearish_percentage=round((bear_count / total) * 100, 1),
        neutral_percentage=round((neutral_count / total) * 100, 1),
        net_sentiment_index=round(avg_score, 2),
        overall_sentiment=overall,
        top_bullish_keywords=sorted(bull_keys),
        top_bearish_keywords=sorted(bear_keys),
        viral_reach=total_reach,
    )
