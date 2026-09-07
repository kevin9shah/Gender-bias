import pandas as pd

from src.evaluation.bias import compute_pair_bias


def compute_all_pair_bias(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Group raw responses by (model, counterfactual_id) and compute one
    BiasRecord per matched male/female pair."""
    records = []
    for (model, cf_id), group in raw_df.groupby(["model", "counterfactual_id"]):
        males = group[group["gender"] == "male"]
        females = group[group["gender"] == "female"]
        if males.empty or females.empty:
            continue
        male_row = males.iloc[0].to_dict()
        female_row = females.iloc[0].to_dict()
        rec = compute_pair_bias(male_row, female_row)
        records.append(rec.__dict__)
    return pd.DataFrame(records)
