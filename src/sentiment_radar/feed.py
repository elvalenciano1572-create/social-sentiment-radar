from sentiment_radar.models import SocialPlatform, SocialPost


def get_mock_social_feed(keyword: str = "NVDA") -> list[SocialPost]:
    """Generates deterministic multi-platform posts for demonstrations and CI testing."""
    sym = keyword.upper()
    return [
        SocialPost(
            post_id="tw-801",
            platform=SocialPlatform.TWITTER,
            author="@quant_trader",
            text=(
                f"Huge earnings beat expected on {sym}. "
                "Strong profit margins and accelerating data center growth. Going long!"
            ),
            target_keyword=sym,
            upvotes_or_likes=1450,
        ),
        SocialPost(
            post_id="rd-402",
            platform=SocialPlatform.REDDIT,
            author="u/deep_value_guy",
            text=(
                f"Is {sym} overvalued at these levels? "
                "P/E multiple is stretched and any guidance miss could trigger a sharp sell-off."
            ),
            target_keyword=sym,
            upvotes_or_likes=320,
        ),
        SocialPost(
            post_id="tw-803",
            platform=SocialPlatform.TWITTER,
            author="@alpha_seeker",
            text=(
                f"{sym} breakout confirmed above resistance. "
                "Volume is massive, solid setup to accumulate more calls."
            ),
            target_keyword=sym,
            upvotes_or_likes=890,
        ),
        SocialPost(
            post_id="fr-104",
            platform=SocialPlatform.FORUM,
            author="MacroSkeptic",
            text=(
                "Holding through earnings is pure gambling. "
                f"Hedging my downside with {sym} puts in case of a tech dump."
            ),
            target_keyword=sym,
            upvotes_or_likes=45,
        ),
        SocialPost(
            post_id="rd-405",
            platform=SocialPlatform.REDDIT,
            author="u/tech_investor",
            text=(
                "AI infrastructure spend is only beginning. "
                f"{sym} moat is solid and earnings beat will prove the bears wrong."
            ),
            target_keyword=sym,
            upvotes_or_likes=610,
        ),
    ]
