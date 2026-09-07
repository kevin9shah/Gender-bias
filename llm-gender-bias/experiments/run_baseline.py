"""Baseline evaluation: single fixed prompt (variant 0) per scenario,
mirroring the classic "one prompt per scenario" evaluation design that the
stability experiment (run_stability.py) then stress-tests.
"""
import sys

import pandas as pd
import yaml

sys.path.insert(0, ".")

from src.evaluation.pairing import compute_all_pair_bias
from src.statistics.significance import paired_significance


def main():
    with open("configs/experiment.yaml") as f:
        cfg = yaml.safe_load(f)
    run_id = cfg["run_id"]

    import os
    os.makedirs("results/metrics", exist_ok=True)
    raw = pd.read_csv(f"results/raw/responses_{run_id}.csv")
    pairs = compute_all_pair_bias(raw)
    pairs.to_csv(f"results/metrics/pair_bias_{run_id}.csv", index=False)

    baseline_pairs = pairs[pairs["prompt_variant"] == 0].copy()

    parse_rate = (
        raw.assign(parsed=raw["response"].notna())
        .groupby("model")["parsed"].mean()
        .rename("parse_attempt_rate")
    )

    rows = []
    for (model, domain), group in baseline_pairs.groupby(["model", "domain"]):
        decision_stats = paired_significance(group["decision_bias"].dropna().tolist())
        sentiment_stats = paired_significance(group["sentiment_bias"].tolist())
        n_scenarios = group["scenario_id"].nunique()
        n_decision_parsed = group["decision_bias"].notna().sum()

        rows.append({
            "model": model,
            "domain": domain,
            "n_scenarios": n_scenarios,
            "n_decision_pairs_parsed": n_decision_parsed,
            "decision_parse_rate": n_decision_parsed / len(group) if len(group) else 0,
            "mean_decision_bias": decision_stats.get("mean"),
            "decision_bias_ci_low": decision_stats.get("ci_low"),
            "decision_bias_ci_high": decision_stats.get("ci_high"),
            "decision_bias_t_p": decision_stats.get("t_test_p"),
            "decision_bias_wilcoxon_p": decision_stats.get("wilcoxon_p"),
            "decision_bias_cohens_d": decision_stats.get("cohens_d"),
            "decision_bias_significant": decision_stats.get("significant_at_0.05"),
            "mean_sentiment_bias": sentiment_stats.get("mean"),
            "sentiment_bias_t_p": sentiment_stats.get("t_test_p"),
            "mean_agentic_bias": group["agentic_bias"].mean(),
            "mean_communal_bias": group["communal_bias"].mean(),
            "mean_semantic_divergence": group["semantic_divergence"].mean(),
        })

    result = pd.DataFrame(rows).sort_values(["domain", "model"])
    result.to_csv(f"results/metrics/baseline_{run_id}.csv", index=False)
    parse_rate.to_csv(f"results/metrics/parse_rate_{run_id}.csv")

    print(result.to_string(index=False))
    print(f"\n[baseline] wrote results/metrics/baseline_{run_id}.csv")


if __name__ == "__main__":
    main()
