"""Benchmark and Response Quality Auditor.

Audits benchmark outputs before and after mitigation to evaluate:
1. Parse Success Rate (Score extraction reliability)
2. Hallucination / Generation Error Rate
3. Length and Structure Coherence
4. Anomaly and Error Flagging
"""

from typing import Any
import pandas as pd
from src.evaluation.decision import extract_score


def audit_response_quality(responses_df: pd.DataFrame) -> dict[str, Any]:
    """Audits a dataframe of LLM responses and produces quality diagnostics."""
    total = len(responses_df)
    if total == 0:
        return {
            "total_responses": 0,
            "parse_success_rate": 0.0,
            "error_rate": 0.0,
            "average_word_count": 0.0,
            "flagged_anomalies": 0,
        }

    has_response = responses_df["response"].notna()
    responses = responses_df["response"].fillna("").astype(str)

    # 1. Error rate (generation crashes or API error flags)
    error_flags = responses.str.contains(r"\[GENERATION_ERROR", regex=True)
    error_count = int(error_flags.sum())

    # 2. Parse success rate
    scores = responses.apply(extract_score)
    parsed_count = int(scores.notna().sum())

    # 3. Word counts & brevity
    word_counts = responses.apply(lambda x: len(x.split()))
    avg_words = float(word_counts.mean())
    too_short = int((word_counts < 4).sum())

    # 4. Out of bounds or corrupted format
    flagged = error_count + too_short + (total - parsed_count)

    return {
        "total_responses": total,
        "valid_responses": int(has_response.sum()),
        "parsed_scores_count": parsed_count,
        "parse_success_rate": float(parsed_count / total),
        "error_count": error_count,
        "error_rate": float(error_count / total),
        "too_short_count": too_short,
        "average_word_count": avg_words,
        "flagged_anomalies": flagged,
        "quality_score": float(max(0.0, 1.0 - (flagged / total))),
    }


def compare_mitigation_quality(raw_df: pd.DataFrame, mitigation_df: pd.DataFrame) -> dict[str, Any]:
    """Compares response quality before vs after mitigation."""
    initial_audit = audit_response_quality(raw_df)
    post_audit = audit_response_quality(
        pd.DataFrame({"response": mitigation_df["response_after"]})
        if "response_after" in mitigation_df.columns
        else pd.DataFrame()
    )

    return {
        "initial_quality": initial_audit,
        "post_mitigation_quality": post_audit,
        "quality_delta": post_audit.get("quality_score", 0.0) - initial_audit.get("quality_score", 0.0),
        "parse_rate_delta": post_audit.get("parse_success_rate", 0.0) - initial_audit.get("parse_success_rate", 0.0),
    }
