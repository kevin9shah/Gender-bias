# Implementation Plan — Review-1 Build

Companion to `architecture.md`. This file tracks *what gets built, in what
order, and to what percentage* — so it doubles as the honest scope statement
for the panel.

## Target: ~70–80% of full project (per `task.md` phases)

| Phase (task.md) | Review-1 status |
|---|---|
| 1. Literature & Problem Formulation | Done (pre-existing, `task.md`) |
| 2. Dataset & Experimental Design | **Implemented** — custom counterfactual dataset, 8 prompt variants/domain. Public benchmarks (CrowS-Pairs/BBQ/BOLD) **not yet integrated** — Project-II item. |
| 3. Framework Development | **Implemented** — prompt generator, model interface, response storage, evaluation engine (all 4 planned metric families except stereotype-association classifier, which is approximated via the lexical agency/communal module for now). |
| 4. Baseline Evaluation | **Implemented** — run across 4 model slots × 4 domains. |
| 5. Bias Stability Analysis | **Implemented** — 8 prompt variants (design calls for up to 20; reduced for CPU runtime, configurable). |
| 6. Mitigation Experiments | **Implemented**, scoped to top-K highest-bias scenarios (not the full scenario set) to keep runtime bounded. |
| 7. Fairness–Utility Analysis | **Implemented** with a declared proxy utility metric (see architecture.md §4.8) — not yet a validated task-quality measure. |
| 8. Statistical Analysis | **Implemented** — paired t-test, Wilcoxon, Cohen's d, bootstrap CI. Multiple-comparison correction **not yet implemented**. |
| 9. Dashboard | **Implemented**, static-read Streamlit app, 4 tabs. Bias heatmaps done; no live "Run Mitigation" button yet (reads precomputed results only — documented as deliberate for demo reliability). |
| 10. Paper & Final Evaluation | Not started — Project-II. |

Real hosted APIs are connected for all four slots (Gemini official API;
GPT-OSS-20B, Llama-3.3-70B, Qwen3-32B via Groq) — see architecture.md §2. The
one declared gap is `gpt_family` using OpenAI's open-weight GPT-OSS model
rather than proprietary GPT-4/5 (no OpenAI key available for this review). A
local-weights fallback (`src/models/local_hf.py`) exists if API
quota/connectivity fails during the run.

## Build order (this session)

1. `configs/experiment.yaml` — all tunable knobs (scenario counts, variant
   count, models, max_new_tokens, mitigation top-K).
2. `src/data/scenarios.py` — scenario bank (12 base scenarios × 4 domains:
   recruitment, career_recommendation, leadership, occupation_association).
3. `src/prompting/templates.py`, `generator.py` — name pairs, 8 prompt
   variants per domain, counterfactual pair generator.
4. `src/models/base.py`, `local_hf.py`, `registry.py` — unified interface over
   4 local HF models.
5. `src/storage/store.py` — CSV-backed response store.
6. `src/evaluation/{decision,sentiment,lexical,semantic,bias,utility}.py`.
7. `src/statistics/{significance,stability}.py`.
8. `src/mitigation/strategies.py`.
9. `experiments/run_baseline.py` → `results/raw/`, `results/metrics/baseline.csv`
10. `experiments/run_stability.py` → `results/metrics/stability.csv`
11. `experiments/run_mitigation.py` → `results/metrics/mitigation.csv`
12. `experiments/run_fairness_utility.py` → `results/metrics/fairness_utility.csv`
13. `dashboard/app.py` — Streamlit, 4 tabs, reads the CSVs above.
14. Execute the full pipeline once, verify non-degenerate results, fix bugs.
15. Smoke-test the dashboard (`streamlit run dashboard/app.py`).

## What a critical reviewer should be told, unprompted

- Sample sizes are modest (~12 scenarios × 4 domains × 2 genders × 8 variants
  × 4 models ≈ 768 baseline/stability generations). Statistical power is
  limited; p-values should be read as illustrative of the *method*, not as
  publication-grade evidence. This is stated explicitly in the dashboard and
  in results write-ups.
- Even with real hosted models, free-form generation won't always follow the
  requested "score 1-10 + justification" format. The decision extractor
  (`extract_score`) will fail to parse some responses; the parse-failure rate
  is itself reported as a diagnostic in the baseline output, not hidden.
- Stereotype-association is approximated via an agentic/communal word-count
  lexicon, not a trained classifier — flagged as a simplification versus the
  literature's more sophisticated approaches (e.g. Wan & Chang's full
  agency-bias benchmark).
- Mitigation is tested on a subset of scenarios (top-K by baseline |bias|),
  not the full dataset, purely for runtime reasons on CPU.

## Explicitly out of scope for Review-1 (next iteration)

- Public benchmark integration (CrowS-Pairs, BBQ, BOLD).
- Real commercial model APIs.
- Full 20-variant stability sweep at full scenario count.
- Multiple-comparison correction (Holm/Bonferroni) across the many
  model×domain×metric tests.
- Trained stereotype/occupation-association classifier.
- Human or LLM-judge-based utility scoring.
- "Run Mitigation" interactive button in the dashboard (live inference from
  the UI).
