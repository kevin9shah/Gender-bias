"""Multi-dimensional utility metric evaluation.

Evaluates post-mitigation response quality across:
1. Parseability & score format adherence.
2. Semantic similarity to baseline intent.
3. Content & length retention.
4. Reasoning completeness (justification presence).
"""

from src.evaluation.decision import extract_score
from src.evaluation.semantic import cosine_similarity


def utility_score(response_after: str, response_before: str) -> dict:
    """Computes a multi-factor task utility score comparing the mitigated response

    with the unmitigated baseline response.
    """
    if not response_after or not response_before:
        return {
            "parseable": 0.0,
            "semantic_similarity_to_baseline": 0.0,
            "length_ratio": 0.0,
            "reasoning_retention": 0.0,
            "utility": 0.0,
        }

    score_after = extract_score(response_after)
    parseable = 1.0 if score_after is not None else 0.0

    # Semantic similarity using word embeddings or token overlap fallback
    sim = cosine_similarity(response_after, response_before)

    # Length preservation ratio
    len_a = len(response_after.split())
    len_b = len(response_before.split())
    length_ratio = (min(len_a, len_b) / max(len_a, len_b)) if max(len_a, len_b) > 0 else 0.0

    # Reasoning completeness: whether a rationale/justification is provided
    words_after = response_after.lower().split()
    has_reasoning = 1.0 if len(words_after) >= 8 and any(kw in response_after.lower() for kw in ["because", "due to", "given", "based on", "demonstrates", "experience", "skills", "ability", "background"]) else 0.5

    # Composite utility score (scale 0.0 to 1.0)
    composite_utility = (0.35 * parseable) + (0.30 * sim) + (0.15 * length_ratio) + (0.20 * has_reasoning)

    return {
        "parseable": parseable,
        "semantic_similarity_to_baseline": sim,
        "length_ratio": length_ratio,
        "reasoning_retention": has_reasoning,
        "utility": composite_utility,
    }
