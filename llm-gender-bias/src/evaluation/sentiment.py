from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def sentiment_score(text: str | None) -> float:
    """VADER compound sentiment score in [-1, 1]. 0.0 for empty text."""
    if not text or not isinstance(text, str):
        return 0.0
    return _analyzer.polarity_scores(text)["compound"]
