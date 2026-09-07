import numpy as np


def stability_profile(bias_values: list[float]) -> dict:
    """Bias magnitude, variability, and directional consistency across
    prompt variants for one (model, scenario, metric) group."""
    arr = np.array([b for b in bias_values if b is not None], dtype=float)
    n = len(arr)
    if n == 0:
        return {"n": 0, "bias_magnitude": None, "bias_variability": None, "directional_consistency": None}

    magnitude = float(abs(np.mean(arr)))
    variability = float(np.std(arr, ddof=1)) if n > 1 else 0.0

    favor_male = int(np.sum(arr > 0))
    favor_female = int(np.sum(arr < 0))
    directional_consistency = max(favor_male, favor_female) / n

    return {
        "n": n,
        "bias_magnitude": magnitude,
        "bias_variability": variability,
        "directional_consistency": directional_consistency,
        "favor_male_count": favor_male,
        "favor_female_count": favor_female,
    }
