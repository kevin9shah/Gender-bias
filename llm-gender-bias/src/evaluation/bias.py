from dataclasses import dataclass

import pandas as pd

from src.evaluation.decision import extract_score
from src.evaluation.lexical import agency_communal_counts
from src.evaluation.semantic import cosine_divergence
from src.evaluation.sentiment import sentiment_score


@dataclass
class BiasRecord:
    model: str
    domain: str
    scenario_id: str
    counterfactual_id: str
    prompt_variant: int
    male_score: float | None
    female_score: float | None
    decision_bias: float | None  # male - female, None if either unparseable
    male_sentiment: float
    female_sentiment: float
    sentiment_bias: float
    male_agentic_rate: float
    female_agentic_rate: float
    agentic_bias: float
    male_communal_rate: float
    female_communal_rate: float
    communal_bias: float
    semantic_divergence: float
    male_response: str
    female_response: str


def compute_pair_bias(male_row: dict, female_row: dict) -> BiasRecord:
    raw_m, raw_f = male_row["response"], female_row["response"]
    male_text = str(raw_m) if (raw_m is not None and pd.notna(raw_m)) else ""
    female_text = str(raw_f) if (raw_f is not None and pd.notna(raw_f)) else ""

    male_score = extract_score(male_text)
    female_score = extract_score(female_text)
    decision_bias = (
        male_score - female_score if male_score is not None and female_score is not None else None
    )

    male_sent = sentiment_score(male_text)
    female_sent = sentiment_score(female_text)

    male_lex = agency_communal_counts(male_text)
    female_lex = agency_communal_counts(female_text)

    divergence = cosine_divergence(male_text, female_text)

    return BiasRecord(
        model=male_row["model"],
        domain=male_row["domain"],
        scenario_id=male_row["scenario_id"],
        counterfactual_id=male_row["counterfactual_id"],
        prompt_variant=int(male_row["prompt_variant"]),
        male_score=male_score,
        female_score=female_score,
        decision_bias=decision_bias,
        male_sentiment=male_sent,
        female_sentiment=female_sent,
        sentiment_bias=male_sent - female_sent,
        male_agentic_rate=male_lex["agentic_rate"],
        female_agentic_rate=female_lex["agentic_rate"],
        agentic_bias=male_lex["agentic_rate"] - female_lex["agentic_rate"],
        male_communal_rate=male_lex["communal_rate"],
        female_communal_rate=female_lex["communal_rate"],
        communal_bias=male_lex["communal_rate"] - female_lex["communal_rate"],
        semantic_divergence=divergence,
        male_response=male_text,
        female_response=female_text,
    )
