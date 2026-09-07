# Architecture — LLM Gender Bias Evaluation Framework

## 1. Scope of this build

This is the Review-1 implementation: a working, end-to-end pipeline covering
objectives O1–O6 (counterfactual generation, multidimensional bias metrics,
stability analysis, cross-model comparison, mitigation, fairness–utility
trade-off), run on real model outputs and real statistics. It targets ~70–80%
of the full project scope defined in `task.md`; gaps are listed in
`implementation.md` under "Not yet implemented."

## 2. Model sourcing decision (read this first)

The project plan names GPT / Gemini / Llama / Qwen. Review-1 uses **real
hosted APIs** for all four slots — no offline/local substitutes:

| Slot | Provider | Model | Notes |
|------|----------|-------|-------|
| `gpt_family` | Groq | `openai/gpt-oss-20b` | OpenAI's open-weight GPT-OSS model, hosted on Groq for low-latency inference. Not GPT-4/GPT-5 — that requires an OpenAI key, which we don't have for this review. Declared as a limitation. |
| `google_family` | Google (Gemini API) | `gemini-2.0-flash` | Real Gemini, official API. |
| `llama_family` | Groq | `llama-3.3-70b-versatile` | Real Meta Llama 3.3, 70B. |
| `qwen_family` | Groq | `qwen/qwen3-32b` | Real Alibaba Qwen 3, 32B. |

This is a stronger position than a local-only substitution: three of the four
slots are genuine frontier-class open models (70B/32B/20B parameters) from
their real model families, and the fourth is the actual commercial Gemini
API. The one declared gap is `gpt_family`: it is OpenAI's model, but the
open-weight GPT-OSS variant rather than proprietary GPT-4/5, because no
OpenAI API key was available for this review. This is stated in the
limitations section, not hidden.

The `BaseLLM` interface (Section 4) is provider-agnostic:
`GeminiModel`/`GroqModel` are both one-file subclasses that only implement
`.generate(prompt) -> str`. Swapping `gpt_family` to real OpenAI later, or
adding a fifth model, requires no changes to prompting, storage, evaluation,
statistics, or dashboard code. A `LocalHFModel` implementation (wrapping
`transformers`) also exists in `src/models/local_hf.py` as an offline
fallback if API quota/connectivity becomes an issue.

API keys are read from environment variables (`GEMINI_API_KEY`,
`GROQ_API_KEY`) via a local `.env` file, loaded through `python-dotenv` and
never hardcoded or logged.

## 3. System diagram

```
                  configs/experiment.yaml
                          │
                          ▼
              ┌───────────────────────┐
              │  Scenario Bank (data)  │  data/custom/scenarios.json
              │  4 domains x N cases   │
              └───────────┬────────────┘
                          ▼
              ┌───────────────────────┐
              │ Counterfactual +       │  src/prompting/
              │ Prompt-Variant Engine  │  templates.py, generator.py
              └───────────┬────────────┘
                          ▼
                  (scenario, domain, gender,
                   prompt_variant, prompt_text) records
                          │
                          ▼
              ┌───────────────────────┐
              │   BaseLLM interface    │  src/models/base.py
              │  ┌─────┬─────┬─────┐   │
              │  │GPT  │Google│Llama│Qwen  src/models/*.py
              │  └─────┴─────┴─────┘   │
              └───────────┬────────────┘
                          ▼
              ┌───────────────────────┐
              │   Response Store       │  src/storage/store.py
              │   results/raw/*.csv    │
              └───────────┬────────────┘
                          ▼
              ┌───────────────────────┐
              │  Evaluation Engine     │  src/evaluation/
              │  decision / sentiment /│  decision.py, sentiment.py,
              │  lexical / semantic    │  lexical.py, semantic.py, bias.py
              └───────────┬────────────┘
                          ▼
              ┌───────────────────────┐
              │  Statistics Engine     │  src/statistics/
              │  paired tests, CI,     │  significance.py, stability.py
              │  effect size, stability│
              └───────────┬────────────┘
                          ▼
        ┌─────────────────┴─────────────────┐
        ▼                                    ▼
┌───────────────────┐              ┌───────────────────────┐
│ Mitigation Engine  │              │ results/metrics/*.csv  │
│ src/mitigation/    │──feeds back─▶│ (baseline, stability,  │
│ 3 strategies        │              │  mitigation, fairness) │
└───────────────────┘              └───────────┬───────────┘
                                                 ▼
                                     ┌───────────────────────┐
                                     │  Streamlit Dashboard   │
                                     │  dashboard/app.py      │
                                     │  reads precomputed CSVs│
                                     └───────────────────────┘
```

Design decision: the dashboard **reads precomputed result files**, it does not
call models live. This is deliberate for a panel demo — no dependency on
model-loading latency or network access during presentation, and results are
reproducible/frozen at the time of the run.

## 4. Module contracts

### 4.1 `src/models/base.py`
```python
class BaseLLM(ABC):
    name: str            # e.g. "qwen_family"
    family: str          # e.g. "Qwen"

    def generate(self, prompt: str, max_new_tokens: int = 96) -> str: ...
```
All four local models (and any future API model) implement only this method.
The pipeline never branches on model type.

### 4.2 `src/data/scenarios.py`
Base scenarios are domain + role + fixed facts, gender-neutral except for a
`{name}` / `{pronoun}` slot. Example fields: `scenario_id`, `domain`,
`role_or_context`, `facts` (list of strings), `task_instruction_key`.

### 4.3 `src/prompting/templates.py` + `generator.py`
- `NAME_PAIRS`: list of (male_name, female_name) pairs, culturally common,
  matched for name length/familiarity as a confound control.
- `PROMPT_VARIANTS`: 8 semantically-equivalent instruction framings per domain
  (paraphrases of the task instruction — e.g. "Rate 1–10 and justify" vs
  "On a scale of 1 to 10, how suitable... explain your reasoning" vs a
  third-person evaluator framing, etc.). This is the mechanism behind O3
  (stability).
- `generate_counterfactual_set(scenario) -> list[PromptRecord]`: cross product
  of {male, female} × {variant 1..8}, each carrying a shared
  `counterfactual_id` linking the male/female pair for a given variant.

### 4.4 `src/storage/store.py`
Appends one row per (model, prompt_record, response) to
`results/raw/responses_<run_id>.csv` with the schema fixed in `task.md`
(model, model_version, prompt, gender, experiment, temperature, timestamp,
response) plus `scenario_id`, `domain`, `prompt_variant`, `counterfactual_id`.

### 4.5 `src/evaluation/`
- `decision.py::extract_score(text) -> float | None` — regex-based 1–10 score
  extraction (first standalone number 0–10, or "X/10" pattern).
- `sentiment.py::sentiment_score(text) -> float` — VADER compound score
  [-1, 1].
- `lexical.py::agency_communal_counts(text) -> dict` — counts of agentic vs
  communal words against a fixed lexicon (Wan & Chang-style agency word list),
  normalized by response length.
- `semantic.py::cosine_divergence(text_a, text_b) -> float` — 1 − cosine
  similarity of `sentence-transformers/all-MiniLM-L6-v2` embeddings.
- `bias.py::compute_pair_bias(male_row, female_row) -> BiasRecord` —
  aggregates all of the above into one row per counterfactual pair:
  `decision_bias`, `sentiment_bias`, `agency_bias`, `semantic_divergence`.

### 4.6 `src/statistics/`
- `significance.py`: paired t-test, Wilcoxon signed-rank (fallback when
  normality doesn't hold), Cohen's d for paired samples, bootstrap 95% CI on
  mean bias.
- `stability.py`: per (model, scenario) — bias magnitude `|mean(B)|`,
  variability `SD(B)` across the 8 variants, directional consistency
  `max(#favor_male, #favor_female) / 8`.

### 4.7 `src/mitigation/strategies.py`
Three interventions applied to the highest-|bias| scenarios found in
baseline:
1. `fairness_instruction` — prepend an explicit fairness instruction to the
   prompt ("Evaluate only on job-relevant qualifications; do not consider
   gender.").
2. `counterfactual_self_check` — two-step: get baseline answer, then prompt
   the model with both the original and the gender-swapped scenario and ask
   it to reconcile/justify any difference, keep the reconciled answer.
3. `selective_rewrite` — post-hoc: detect gendered/stereotyped language in the
   response via the lexical module, and prompt the model to rewrite only the
   flagged spans.

### 4.8 `src/evaluation/utility.py`
Utility is a **declared proxy** (no ground-truth labels exist for these
scenarios), computed as the mean of:
- `parseable`: whether a decision score could still be extracted (1/0),
- `semantic_similarity_to_baseline`: cosine similarity between mitigated and
  baseline response (did content change wildly?),
- `length_ratio`: `min(len_after, len_before) / max(len_after, len_before)`.

This is intentionally simple and is flagged in `implementation.md` as an area
a stronger Project-II iteration should replace with task-specific relevance
scoring or human/LLM-judge evaluation.

### 4.9 `dashboard/app.py`
Streamlit, four tabs: Baseline, Stability, Mitigation, Fairness–Utility. Each
tab loads the corresponding `results/metrics/*.csv` and renders tables +
matplotlib charts (bar charts per model/domain, stability scatter, trade-off
scatter).

## 5. Data flow summary

```
scenarios.json → prompt generator → raw responses (CSV)
raw responses → evaluation engine → paired bias records (CSV)
paired bias records → statistics engine → baseline + stability metrics (CSV)
baseline metrics → mitigation engine → mitigated responses (CSV)
mitigated responses → evaluation + utility → fairness-utility metrics (CSV)
all metrics CSVs → dashboard
```

## 6. Known constraints (to state to the panel proactively)

- Local models are far smaller (0.5B–1.1B params) than the frontier models
  named in the objectives; absolute bias numbers are not claimed to transfer
  to GPT-4/Gemini/Llama-3/Qwen-2.5-72B. The *methodology* (metrics, stability
  protocol, mitigation loop, fairness–utility trade-off) is what transfers.
- Scenario count and prompt-variant count are reduced from the full design
  (12 base scenarios × 4 domains, 8 variants instead of 20) to keep CPU
  generation time within a single run for this review. Scaling knobs are in
  `configs/experiment.yaml`.
- Utility is a proxy metric, not a validated task-quality measure.
