import pytest

from sentiment_radar.analyzer import analyze_posts, score_text_sentiment
from sentiment_radar.cli import main
from sentiment_radar.feed import get_mock_social_feed
from sentiment_radar.models import SentimentClass


def test_lexical_scoring():
    # Bullish text
    sent, score, themes = score_text_sentiment(
        "Massive growth and solid earnings beat. Going long to the moon!"
    )
    assert sent == SentimentClass.BULLISH
    assert score > 0
    assert "growth" in themes

    # Bearish text
    sent_b, score_b, themes_b = score_text_sentiment(
        "Major recession risk, crash incoming, sell all positions."
    )
    assert sent_b == SentimentClass.BEARISH
    assert score_b < 0
    assert "crash" in themes_b

    # Neutral text
    sent_n, score_n, _ = score_text_sentiment("The quarterly meeting is scheduled for Tuesday.")
    assert sent_n == SentimentClass.NEUTRAL
    assert score_n == 0.0


def test_analyze_posts_aggregation():
    posts = get_mock_social_feed("NVDA")
    assert len(posts) == 5

    radar = analyze_posts(posts)
    assert radar.keyword == "NVDA"
    assert radar.total_posts == 5
    assert radar.bullish_percentage > 0
    assert radar.bearish_percentage > 0
    assert radar.viral_reach > 1000
    assert -1.0 <= radar.net_sentiment_index <= 1.0


def test_empty_posts_validation():
    with pytest.raises(ValueError, match="Cannot analyze empty"):
        analyze_posts([])


def test_cli_execution(capsys):
    exit_code = main(["TSLA"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "SOCIAL SENTIMENT RADAR" in captured.out
    assert "RADAR SYNTHESIS REPORT" in captured.out
