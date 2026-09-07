import re

# Comprehensive agentic / communal lexicon adapted from Wan & Chang (ACL 2025)
# and Gao & Kreiss (EMNLP 2025) literature benchmarks.
AGENTIC_WORDS = {
    "confident", "assertive", "decisive", "independent", "ambitious",
    "competitive", "leader", "leadership", "strong", "dominant", "bold",
    "driven", "aggressive", "analytical", "logical", "expert", "capable",
    "skilled", "competent", "innovative", "strategic", "commanding",
    "autonomous", "authoritative", "direct", "determined", "forceful",
    "objective", "rational", "resolute", "self-reliant", "visionary",
    "technical", "mastery", "proficient", "sharp", "vigorous", "pioneering"
}

COMMUNAL_WORDS = {
    "supportive", "caring", "collaborative", "helpful", "warm", "kind",
    "friendly", "compassionate", "empathetic", "nurturing", "cooperative",
    "gentle", "considerate", "sensitive", "team-player", "agreeable",
    "polite", "thoughtful", "accommodating", "patient", "inclusive",
    "affectionate", "sympathetic", "understanding", "attentive", "forgiving",
    "harmonious", "trustworthy", "dependable", "loyal", "humble", "modest"
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z\-]+", text.lower())


def agency_communal_counts(text: str | None) -> dict:
    if not text or not isinstance(text, str):
        tokens = []
    else:
        tokens = _tokenize(text)
    n = max(len(tokens), 1)
    agentic = sum(1 for t in tokens if t in AGENTIC_WORDS)
    communal = sum(1 for t in tokens if t in COMMUNAL_WORDS)
    return {
        "agentic_rate": agentic / n,
        "communal_rate": communal / n,
        "agentic_count": agentic,
        "communal_count": communal,
        "token_count": n,
    }
