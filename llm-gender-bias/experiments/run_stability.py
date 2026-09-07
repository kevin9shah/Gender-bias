"""Bias stability analysis: for each (model, scenario), compute bias
magnitude, variability, and directional consistency across all 8 prompt
variants (O3)."""
import sys

import pandas as pd
import yaml

sys.path.insert(0, ".")

from src.statistics.stability import stability_profile


def main():
    with open("configs/experiment.yaml") as f:
        cfg = yaml.safe_load(f)
    run_id = cfg["run_id"]

    import os
    os.makedirs("results/metrics", exist_ok=True)
    pairs = pd.read_csv(f"results/metrics/pair_bias_{run_id}.csv")

    scenario_rows = []
    for (model, scenario_id, domain), group in pairs.groupby(["model", "scenario_id", "domain"]):
        profile = stability_profile(group["decision_bias"].dropna().tolist())
        scenario_rows.append({
            "model": model,
            "domain": domain,
            "scenario_id": scenario_id,
            **profile,
        })
    scenario_df = pd.DataFrame(scenario_rows)
    scenario_df.to_csv(f"results/metrics/stability_by_scenario_{run_id}.csv", index=False)

    model_domain_rows = []
    for (model, domain), group in scenario_df.groupby(["model", "domain"]):
        model_domain_rows.append({
            "model": model,
            "domain": domain,
            "mean_bias_magnitude": group["bias_magnitude"].mean(),
            "mean_bias_variability": group["bias_variability"].mean(),
            "mean_directional_consistency": group["directional_consistency"].mean(),
        })
    model_df = pd.DataFrame(model_domain_rows).sort_values(["domain", "model"])
    model_df.to_csv(f"results/metrics/stability_{run_id}.csv", index=False)

    print(model_df.to_string(index=False))
    print(f"\n[stability] wrote results/metrics/stability_{run_id}.csv")


if __name__ == "__main__":
    main()
