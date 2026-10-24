from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SocialPlatform(str, Enum):
    REDDIT = "Reddit"
    TWITTER = "Twitter/X"
    DISCORD = "Discord"
    FORUM = "Online Forum"


class SentimentClass(str, Enum):
    BULLISH = "BULLISH / POSITIVE"
    BEARISH = "BEARISH / NEGATIVE"
    NEUTRAL = "NEUTRAL"


class SocialPost(BaseModel):
    post_id: str
    platform: SocialPlatform
    author: str
    text: str
    target_keyword: str
    upvotes_or_likes: int = 0
    created_at: datetime = Field(default_factory=datetime.now)


class ScoredPost(BaseModel):
    post: SocialPost
    sentiment: SentimentClass
    confidence_score: float = Field(ge=0.0, le=1.0)
    sentiment_score: float = Field(
        ge=-1.0, le=1.0, description="-1.0 extreme negative, +1.0 extreme positive"
    )
    key_themes: list[str]


class AggregatedSentimentRadar(BaseModel):
    keyword: str
    total_posts: int
    bullish_percentage: float
    bearish_percentage: float
    neutral_percentage: float
    net_sentiment_index: float = Field(ge=-1.0, le=1.0, description="Overall market consensus score")
    overall_sentiment: SentimentClass
    top_bullish_keywords: list[str]
    top_bearish_keywords: list[str]
    viral_reach: int
