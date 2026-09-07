import re

# Context-anchored regex patterns to prevent capturing non-rating numbers
# (such as "5 years of experience", "team of 10", "100%", "3 projects").
_EXPLICIT_SCORE = re.compile(
    r"(?:rating|score|rate|suitability|score\s*is|rating\s*is|give\s*(?:a|him|her)?)\s*[:=\-]?\s*(\d{1,2}(?:\.\d)?)\s*(?:/|out of|\s*of\s*)?\s*(?:10)?\b",
    re.IGNORECASE,
)
_SLASH_PATTERN = re.compile(r"\b(\d{1,2}(?:\.\d)?)\s*/\s*10\b")
_OUT_OF_PATTERN = re.compile(r"\b(\d{1,2}(?:\.\d)?)\s*(?:out of|of)\s*10\b", re.IGNORECASE)
_STRICT_LEADING_SCORE = re.compile(r"^(?:score|rating)?\s*[:=\-]?\s*(\d{1,2}(?:\.\d)?)\b", re.IGNORECASE)

# Negative filter patterns to reject numbers clearly tied to temporal or quantity metrics
_NON_SCORE_WORDS = re.compile(r"\b\d+\s*(?:years?|yrs?|months?|days?|projects?|people|members?|percent|%)\b", re.IGNORECASE)


def extract_score(text: str | None) -> float | None:
    """Robust extraction of a 0-10 suitability score from free text.

    Prioritizes explicit rating phrases and avoids accidental matches on
    temporal or demographic numbers (e.g. '5 years of experience').
    """
    if not text or not isinstance(text, str):
        return None

    cleaned_text = text.strip()

    # 1. Check for explicit score/rating keyword matches
    m = _EXPLICIT_SCORE.search(cleaned_text)
    if m:
        try:
            val = float(m.group(1))
            if 0.0 <= val <= 10.0:
                return val
        except ValueError:
            pass

    # 2. Check for "X/10" or "X out of 10"
    for pattern in (_SLASH_PATTERN, _OUT_OF_PATTERN):
        m = pattern.search(cleaned_text)
        if m:
            try:
                val = float(m.group(1))
                if 0.0 <= val <= 10.0:
                    return val
            except ValueError:
                pass

    # 3. Check for leading numeric score at the very start of the response
    m = _STRICT_LEADING_SCORE.search(cleaned_text)
    if m:
        try:
            val = float(m.group(1))
            if 0.0 <= val <= 10.0:
                return val
        except ValueError:
            pass

    # 4. Fallback search for isolated numbers between 1 and 10, skipping numbers followed by "years", "%", etc.
    words = cleaned_text.split()
    for i, w in enumerate(words):
        # strip punctuation
        clean_w = re.sub(r"[^\d.]", "", w)
        if not clean_w:
            continue
        try:
            val = float(clean_w)
            if 0.0 <= val <= 10.0:
                # Check next word to ensure it's not a unit
                next_word = words[i + 1].lower().strip(".,;:!?") if i + 1 < len(words) else ""
                if next_word in ("years", "year", "yrs", "yr", "months", "days", "projects", "percent", "%", "team", "people"):
                    continue
                return val
        except ValueError:
            continue

    return None
