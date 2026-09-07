import numpy as np
from scipy import stats


def paired_significance(diffs: list[float], n_boot: int = 2000, seed: int = 42) -> dict:
    """Paired-sample significance test suite on a list of per-pair bias values.

    Returns mean, SD, 95% bootstrap CI, paired t-test p, Wilcoxon p, and
    Cohen's d for paired samples. Falls back gracefully on tiny samples.
    """
    arr = np.array([d for d in diffs if d is not None], dtype=float)
    n = len(arr)
    if n == 0:
        return {"n": 0}

    mean = float(np.mean(arr))
    sd = float(np.std(arr, ddof=1)) if n > 1 else 0.0

    if n > 1 and sd > 0:
        t_p = float(stats.ttest_1samp(arr, 0.0).pvalue)
        cohens_d = mean / sd
    else:
        t_p, cohens_d = 1.0, 0.0

    if n > 1 and np.any(arr != 0):
        try:
            wilcoxon_p = float(stats.wilcoxon(arr).pvalue)
        except ValueError:
            wilcoxon_p = 1.0
    else:
        wilcoxon_p = 1.0

    rng = np.random.default_rng(seed)
    if n > 1:
        boot_means = [np.mean(rng.choice(arr, size=n, replace=True)) for _ in range(n_boot)]
        ci_low, ci_high = float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))
    else:
        ci_low, ci_high = mean, mean

    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "t_test_p": t_p,
        "wilcoxon_p": wilcoxon_p,
        "cohens_d": cohens_d,
        "significant_at_0.05": (t_p < 0.05) if n > 1 else False,
    }


def holm_bonferroni_correction(p_values: list[float], alpha: float = 0.05) -> list[dict]:
    """Applies Holm-Bonferroni step-down procedure to control Family-Wise Error Rate (FWER)."""
    m = len(p_values)
    if m == 0:
        return []

    # Sort p-values with their original indices
    indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
    results = [None] * m

    for rank, (orig_idx, p_val) in enumerate(indexed_p):
        threshold = alpha / (m - rank)
        is_sig = p_val <= threshold
        adjusted_p = min(p_val * (m - rank), 1.0)
        results[orig_idx] = {
            "p_value": p_val,
            "adjusted_p": adjusted_p,
            "threshold": threshold,
            "significant": is_sig,
        }
    return results


def benjamini_hochberg_fdr(p_values: list[float], q: float = 0.05) -> list[dict]:
    """Applies Benjamini-Hochberg step-up procedure to control False Discovery Rate (FDR)."""
    m = len(p_values)
    if m == 0:
        return []

    indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
    results = [None] * m

    for rank, (orig_idx, p_val) in enumerate(indexed_p, start=1):
        threshold = (rank / m) * q
        adjusted_p = min((p_val * m) / rank, 1.0)
        results[orig_idx] = {
            "p_value": p_val,
            "adjusted_p": adjusted_p,
            "critical_value": threshold,
            "significant": p_val <= threshold,
        }
    return results
