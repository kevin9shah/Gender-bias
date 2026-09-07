"""Fairness-utility trade-off: for each mitigation strategy, combine bias
reduction (fairness) with the proxy utility metric (O6)."""
import sys

import pandas as pd
import yaml

sys.path.insert(0, ".")

from src.evaluation.utility import utility_score
from src.statistics.significance import paired_significance


def main():
    with open("configs/experiment.yaml") as f:
        cfg = yaml.safe_load(f)
    run_id = cfg["run_id"]

    import os
    os.makedirs("results/metrics", exist_ok=True)
    mit = pd.read_csv(f"results/metrics/mitigation_{run_id}.csv")

    util_rows = []
    for _, row in mit.iterrows():
        u_male = utility_score(str(row["male_response_after"]), str(row["male_response_before"]))
        u_female = utility_score(str(row["female_response_after"]), str(row["female_response_before"]))
        util_rows.append({
            "model": row["model"], "domain": row["domain"], "scenario_id": row["scenario_id"],
            "strategy": row["strategy"],
            "bias_before": row["decision_bias_before"], "bias_after": row["decision_bias_after"],
            "bias_reduction": row["bias_reduction"],
            "utility_male": u_male["utility"], "utility_female": u_female["utility"],
            "utility": (u_male["utility"] + u_female["utility"]) / 2,
        })
    detail = pd.DataFrame(util_rows)
    detail.to_csv(f"results/metrics/fairness_utility_detail_{run_id}.csv", index=False)

    summary_rows = []
    for strategy, group in detail.groupby("strategy"):
        reduction_stats = paired_significance(group["bias_reduction"].dropna().tolist())
        summary_rows.append({
            "strategy": strategy,
            "n": len(group),
            "mean_bias_reduction": reduction_stats.get("mean"),
            "bias_reduction_ci_low": reduction_stats.get("ci_low"),
            "bias_reduction_ci_high": reduction_stats.get("ci_high"),
            "bias_reduction_significant": reduction_stats.get("significant_at_0.05"),
            "mean_utility": group["utility"].mean(),
            "mean_abs_bias_before": group["bias_before"].abs().mean(),
            "mean_abs_bias_after": group["bias_after"].abs().mean(),
        })
    summary = pd.DataFrame(summary_rows).sort_values("mean_bias_reduction", ascending=False)
    summary.to_csv(f"results/metrics/fairness_utility_{run_id}.csv", index=False)

    print(summary.to_string(index=False))
    print(f"\n[fairness_utility] wrote results/metrics/fairness_utility_{run_id}.csv")


if __name__ == "__main__":
    main()
