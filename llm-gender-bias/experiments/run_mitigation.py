"""Mitigation experiments: apply 3 interventions to the top-K highest-|bias|
scenarios found in the baseline run, then re-evaluate bias (O5)."""
import sys

import pandas as pd
import yaml

sys.path.insert(0, ".")

from src.evaluation.bias import compute_pair_bias
from src.mitigation.strategies import STRATEGIES
from src.models.registry import load_models
from src.storage.store import ResponseStore, now_iso


def select_top_k_scenarios(pairs: pd.DataFrame, k: int) -> list[str]:
    variant0 = pairs[pairs["prompt_variant"] == 0].copy()
    variant0["abs_bias"] = variant0["decision_bias"].abs()
    ranked = (
        variant0.groupby("scenario_id")["abs_bias"].mean()
        .sort_values(ascending=False)
    )
    return ranked.head(k).index.tolist()


def main():
    with open("configs/experiment.yaml") as f:
        cfg = yaml.safe_load(f)
    run_id = cfg["run_id"]
    top_k = cfg["mitigation"]["top_k_scenarios"]

    import os
    os.makedirs("results/metrics", exist_ok=True)
    os.makedirs("results/raw", exist_ok=True)
    pairs = pd.read_csv(f"results/metrics/pair_bias_{run_id}.csv")
    raw = pd.read_csv(f"results/raw/responses_{run_id}.csv")
    top_scenarios = select_top_k_scenarios(pairs, top_k)
    print(f"[mitigation] top-{top_k} scenarios by |baseline bias|: {top_scenarios}")

    print("[mitigation] loading models ...")
    models = load_models()
    per_model_max_tokens = {
        spec["slot"]: spec.get("max_new_tokens", cfg["generation"]["max_new_tokens"])
        for spec in cfg["models"]
    }

    out_path = f"results/raw/mitigation_{run_id}.csv"
    store = ResponseStore(out_path)
    metric_rows = []

    v0 = raw[raw["prompt_variant"] == 0]

    for slot, model in models.items():
        for scenario_id in top_scenarios:
            sub = v0[(v0["model"] == slot) & (v0["scenario_id"] == scenario_id)]
            male_row = sub[sub["gender"] == "male"]
            female_row = sub[sub["gender"] == "female"]
            if male_row.empty or female_row.empty:
                continue
            male_row, female_row = male_row.iloc[0], female_row.iloc[0]

            baseline_bias_rec = compute_pair_bias(male_row.to_dict(), female_row.to_dict())

            male_resp = str(male_row["response"]) if pd.notna(male_row["response"]) else ""
            female_resp = str(female_row["response"]) if pd.notna(female_row["response"]) else ""
            mnt = per_model_max_tokens[slot]
            for strat_name, strat_fn in STRATEGIES.items():
                kwargs_m = dict(
                    counterfactual_prompt=female_row["prompt"],
                    baseline_response=male_resp,
                    max_new_tokens=mnt,
                )
                kwargs_f = dict(
                    counterfactual_prompt=male_row["prompt"],
                    baseline_response=female_resp,
                    max_new_tokens=mnt,
                )
                male_after = strat_fn(model, male_row["prompt"], **kwargs_m)
                female_after = strat_fn(model, female_row["prompt"], **kwargs_f)

                for gender, prompt_text, response_text in (
                    ("male", male_row["prompt"], male_after),
                    ("female", female_row["prompt"], female_after),
                ):
                    store.write({
                        "model": slot, "model_version": model.version, "family": model.family,
                        "domain": male_row["domain"], "scenario_id": scenario_id,
                        "prompt_id": f"{scenario_id}_MIT_{strat_name}_{gender[0].upper()}",
                        "prompt_variant": 0,
                        "counterfactual_id": f"{scenario_id}_MIT_{strat_name}",
                        "experiment": f"mitigation_{strat_name}", "gender": gender,
                        "name": "", "temperature": cfg["generation"]["temperature"],
                        "timestamp": now_iso(), "prompt": prompt_text, "response": response_text,
                    })

                after_rec = compute_pair_bias(
                    {**male_row.to_dict(), "response": male_after},
                    {**female_row.to_dict(), "response": female_after},
                )

                bias_before = baseline_bias_rec.decision_bias
                bias_after = after_rec.decision_bias
                bias_reduction = (
                    abs(bias_before) - abs(bias_after)
                    if bias_before is not None and bias_after is not None else None
                )

                metric_rows.append({
                    "model": slot, "domain": male_row["domain"], "scenario_id": scenario_id,
                    "strategy": strat_name,
                    "decision_bias_before": bias_before, "decision_bias_after": bias_after,
                    "bias_reduction": bias_reduction,
                    "sentiment_bias_before": baseline_bias_rec.sentiment_bias,
                    "sentiment_bias_after": after_rec.sentiment_bias,
                    "semantic_divergence_after": after_rec.semantic_divergence,
                    "male_response_before": male_row["response"], "male_response_after": male_after,
                    "female_response_before": female_row["response"], "female_response_after": female_after,
                })
            print(f"[mitigation] {slot} / {scenario_id} done")

    store.close()
    metrics_df = pd.DataFrame(metric_rows)
    metrics_df.to_csv(f"results/metrics/mitigation_{run_id}.csv", index=False)
    print(f"[mitigation] wrote results/metrics/mitigation_{run_id}.csv ({len(metrics_df)} rows)")


if __name__ == "__main__":
    main()
