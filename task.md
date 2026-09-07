# LLM Gender Bias Evaluation Framework — Task Plan

## Literature Survey / Rationale

1. Chen et al. — *Causally Testing Gender Bias in LLMs: A Case Study on Occupational
   Bias* — NAACL Findings 2025 (https://aclanthology.org/2025.findings-naacl.281/)
2. Gao & Kreiss — *Measuring Bias or Measuring the Task: Understanding the Brittle
   Nature of LLM Gender Biases* — EMNLP 2025 (https://aclanthology.org/2025.emnlp-main.342/)
3. Wan & Chang — *White Men Lead, Black Women Help? Benchmarking and Mitigating
   Language Agency Social Biases in LLMs* — ACL 2025 (https://aclanthology.org/2025.acl-long.445/)
4. Lum et al. — *Bias in Language Models: Beyond Trick Tests and Towards RUTEd
   Evaluation* — ACL 2025 (https://aclanthology.org/2025.acl-long.7/)
5. *Measuring Gender and Racial Biases in Large Language Models: Intersectional
   Evidence from Automated Resume Evaluation* — PNAS Nexus, 2025
   (https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8071848?login=false)
6. *Large Language Models Still Exhibit Bias in Long Text* — Findings of ACL 2025
   (https://aclanthology.org/2025.findings-acl.1341/)
7. *GenderCARE: A Comprehensive Framework for Assessing and Reducing Gender Bias in
   Large Language Models* — 2024 (https://arxiv.org/abs/2408.12494)
8. *Assessing Gender Bias in LLMs: Comparing LLM Outputs with Human Perceptions and
   Official Statistics* — 2024 (https://arxiv.org/abs/2411.13738)
9. *Quantifying Gender Bias in Large Language Models Using Information-Theoretic and
   Statistical Analysis* — 2025 (https://www.mdpi.com/2078-2489/16/5/358)
10. *Diagnosing the Bias Iceberg in Large Language Models* — 2026
    (https://www.sciencedirect.com/science/article/pii/S0306457325004959)

---

## Gap Identification

Although recent studies have introduced causal benchmarks, realistic-use
evaluations, and mitigation techniques for gender bias in LLMs, existing approaches
still leave room for a unified evaluation framework that examines the stability of
bias across prompt variations and connects bias diagnosis with adaptive mitigation.
Furthermore, mitigation should be evaluated not only by reduction in measured bias
but also by its consistency and impact on task utility. This motivates the proposed
framework for counterfactual, stability-aware and mitigation-oriented comparison of
gender bias across multiple LLMs.

### Gap 1 — Bias evaluation is sensitive to prompt formulation

Gao & Kreiss show that relatively small changes in evaluation prompts can
substantially change measured gender bias, and in some cases even reverse its
direction.

- **Problem:** A model evaluated using only one fixed prompt may appear biased or
  unbiased simply because of the wording of that prompt.
- **Our gap:** Existing evaluations do not consistently quantify bias stability
  across semantically equivalent prompt variations.
- **Our response:** Same scenario → P1, P2, P3, ... P20 → 20 bias measurements →
  bias magnitude + variability + directional consistency.

### Gap 2 — Existing benchmarks do not always represent realistic LLM usage

RUTEd shows that traditional bias metrics can behave differently from metrics
obtained from more realistic, long-form generation settings. More broadly, the
newer literature is questioning whether benchmark performance alone captures bias in
real interactions.

- **Problem:** Benchmark question ≠ real-world LLM interaction.
- **Our gap:** There is a need for evaluation that combines established benchmark
  datasets with controlled, realistic counterfactual scenarios.
- **Our response:** Existing benchmarks + custom recruitment/career/leadership
  scenarios + counterfactual gender pairs.

### Gap 3 — Causal/counterfactual evaluation is usually focused on specific bias settings

Chen et al. provide a causal formulation and OccuGender benchmark for occupational
gender bias, demonstrating substantial bias in several open-source LLMs. That's
excellent work, but it is focused primarily on occupational gender bias.

- **Our gap:** A broader automated framework is still useful for applying controlled
  counterfactual evaluation across multiple task types and multiple LLM families,
  rather than restricting analysis to a single benchmark/domain.
- **Our response:** Recruitment, occupation, leadership, career recommendation, and
  generative evaluation — all run through the same evaluation framework, across
  GPT / Gemini / Llama / Qwen.

### Gap 4 — Bias mitigation is not reliably connected to bias diagnosis

Wan & Chang find that simple prompt-based mitigation can be unstable and can even
exacerbate bias; they propose selective rewriting as a more targeted mitigation
approach.

- **Problem:** Many mitigation approaches effectively do Model → "Be fair" → New
  output, without first asking what type of bias was detected, or whether the
  intervention actually improved fairness.
- **Our gap:** There is scope for an adaptive mitigation pipeline that selects or
  compares interventions based on the detected bias characteristics and then
  re-evaluates the result.
- **Our proposed loop:** Detect → Diagnose → Select intervention → Mitigate →
  Re-evaluate. This is much stronger than simply adding a "be unbiased" system
  prompt.

### Gap 5 — Fairness improvement is often evaluated without sufficiently considering utility

Example: before mitigation, Bias = 0.20, Utility = 0.90; after mitigation, Bias =
0.05, Utility = 0.55. Technically bias decreased — but the model became much less
useful. Is that mitigation actually successful?

- **Our gap:** There is a need to evaluate gender-bias mitigation jointly in terms
  of fairness, stability, and preservation of task utility.
- **Our response:** Mitigation → Fairness (Bias ↓, Stability ↑) and Utility (Quality
  preserved?). This gives us our fairness–utility trade-off analysis.

### Gap summary

| No. | Literature problem | Our proposed response |
|-----|---------------------|------------------------|
| G1 | Bias measurements can change with prompt formulation | Prompt-stability analysis |
| G2 | Traditional benchmarks may not represent realistic usage | Benchmark + realistic counterfactual tasks |
| G3 | Causal evaluation is often focused on particular domains/benchmarks | Cross-domain, cross-model evaluation framework |
| G4 | Prompt-based mitigation can be unstable | Adaptive/targeted mitigation + re-evaluation |
| G5 | Reducing bias alone doesn't guarantee a useful model | Fairness + stability + utility evaluation |

### Relation between these gaps

```
Existing evaluation → Prompt sensitivity → Benchmark limitations →
Need robust counterfactual testing → Bias detected →
Mitigation may be unstable → Need adaptive mitigation →
Mitigation may hurt usefulness → Need fairness–utility evaluation
```

---

## Primary Objective

To develop an automated, reproducible framework for evaluating and comparing gender
bias across multiple Large Language Models using controlled counterfactual prompts,
multidimensional bias metrics, prompt-stability analysis, and statistical validation,
while evaluating the effectiveness of bias-mitigation strategies and their impact on
task utility.

Framing for evaluator (avoid oversimplifying to "which LLM is least biased"):

> To systematically characterize the magnitude, direction, and stability of gender
> bias across LLMs, and to determine whether mitigation can reduce such bias without
> substantially compromising task utility.

Chain: Literature → Gap → Objective → Methodology → Implementation

---

## Objectives

| # | Objective | Output |
|---|-----------|--------|
| O1 | Build a controlled counterfactual evaluation framework (gender-paired inputs: names, pronouns, explicit labels, gendered cues; other task info held constant) | Controlled M/F prompt pairs |
| O2 | Quantify multidimensional gender bias (decision/score disparity, sentiment, gendered/agency language, occupation association, semantic divergence, stereotype association) | Bias metrics |
| O3 | Measure stability of observed bias across ~10–20 semantically equivalent prompt formulations (magnitude, variability, directional consistency, sensitivity) | Stability profile/index |
| O4 | Compare bias across LLMs (GPT, Gemini, Llama, Qwen) and task domains (recruitment, career recommendation, leadership, occupation association, text generation) | Cross-model comparison |
| O5 | Test bias-mitigation strategies (baseline → fairness-oriented instruction → counterfactual self-check → selective rewriting); do not assume mitigation works — treat as an experimental question | Before/after bias analysis |
| O6 | Evaluate fairness–utility trade-off: does bias reduction preserve task accuracy, relevance, semantic similarity, and response quality? | Optimal mitigation analysis |

Full chain:
```
CONTROLLED INPUT → COUNTERFACTUAL TEST → MEASURE GENDER BIAS →
TEST STATISTICAL SIGNIFICANCE → TEST PROMPT STABILITY →
COMPARE LLMs / TASKS → APPLY MITIGATION → RE-EVALUATE FAIRNESS + UTILITY
```

---

## Project Plan (Phase-wise, ~18 weeks / Project I + Project II)

**Project I: Weeks 1–8** — Literature → dataset → methodology → baseline framework → initial experiments
**Project II: Weeks 9–18** — Stability → mitigation → fairness/utility → final evaluation → dashboard → paper

| Phase | Weeks | Major Activities | Deliverable |
|-------|-------|-------------------|-------------|
| 1. Literature & Problem Definition | 1–2 | Review LLM gender-bias literature; study CrowS-Pairs, StereoSet, BBQ, BOLD, HolisticBias; study counterfactual/causal bias evaluation, prompt sensitivity, stability, mitigation techniques; finalize RQs/hypotheses | Research formulation |
| 2. Dataset & Experimental Design | 3–4 | Select 2–3 public benchmarks (e.g., CrowS-Pairs + BBQ + BOLD); build custom counterfactual dataset for recruitment/career/leadership/occupation/professional-evaluation scenarios; create 10–20 prompt variants per scenario | Evaluation dataset, prompt templates, counterfactual generator, experimental protocol |
| 3. Framework Development | 5–7 | Build Prompt Generator, LLM Interface (common API across GPT/Gemini/Llama/Qwen), Response Storage (model, version, prompt, gender, experiment, temperature, timestamp, response), Evaluation Engine (sentiment, gendered/agency language, occupation association, decision-score disparity, semantic difference) | Working automated evaluation framework |
| 4. Baseline Evaluation | 8–9 | Run 4 models × 2–3 benchmarks × custom scenarios; compute mean bias, SD, CI, p-value, effect size | Baseline gender-bias comparison |
| 5. Bias Stability Analysis | 10–11 | Run each scenario across 10–20 prompt variants × M/F pairs; compute bias magnitude, variability, directional consistency; compare across models | Gender Bias Stability Profile |
| 6. Mitigation Experiments | 12–13 | Baseline vs. Intervention 1 (fairness-oriented instruction) vs. Intervention 2 (counterfactual self-check) vs. Intervention 3 (selective rewriting); measure bias reduction | Mitigation results |
| 7. Fairness–Utility Analysis | 14 | Measure response quality, relevance, task performance, semantic consistency alongside bias reduction/stability | Optimal intervention analysis |
| 8. Statistical Analysis | 15 | Paired tests, Mann–Whitney U, chi-square, bootstrap CIs, effect sizes, multiple-comparison correction | Validated results |
| 9. Dashboard & Documentation | 16 | Streamlit interface: model comparison, bias heatmaps, stability plots, before/after mitigation, statistical results | Interactive framework |
| 10. Paper & Final Evaluation | 17–18 | Methodology, experimental setup, results, discussion, limitations, ethics, reproducibility docs | Final report/paper |

### Key formulas
- Decision bias: `B_i = Score_male,i − Score_female,i`, mean `B̄ = (1/N) Σ B_i`
- Semantic divergence: `1 − CosineSimilarity(Response_M, Response_F)`
- Bias magnitude: `BM = |B̄|`
- Bias variability: `BV = SD(B_1, ..., B_n)`
- Directional consistency: `DC = (# prompts favoring dominant direction) / N`
- Hypothesis test on paired differences: `H0: μ_B = 0` vs `H1: μ_B ≠ 0`

---

## Implementation Roadmap (not yet started)

```
STEP 1  → Project setup
STEP 2  → Dataset / prompt schema
STEP 3  → Counterfactual prompt generator
STEP 4  → LLM interface
STEP 5  → Response database
STEP 6  → Bias metrics
STEP 7  → Statistical analysis
STEP 8  → Bias Stability
STEP 9  → Mitigation
STEP 10 → Fairness–utility analysis
STEP 11 → Dashboard
STEP 12 → Experiments + paper results
```

### Planned repository structure

```
llm-gender-bias/
├── data/
│   ├── raw/
│   ├── processed/
│   └── custom/
├── configs/
│   └── models.yaml
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   └── counterfactual.py
│   ├── prompting/
│   │   ├── templates.py
│   │   └── generator.py
│   ├── models/
│   │   ├── base.py
│   │   ├── openai_model.py
│   │   ├── gemini_model.py
│   │   ├── llama_model.py
│   │   └── qwen_model.py
│   ├── evaluation/
│   │   ├── sentiment.py
│   │   ├── lexical.py
│   │   ├── occupation.py
│   │   ├── semantic.py
│   │   └── bias.py
│   ├── statistics/
│   │   ├── significance.py
│   │   └── stability.py
│   ├── mitigation/
│   │   ├── strategies.py
│   │   └── adaptive.py
│   └── pipeline.py
├── experiments/
│   ├── baseline/
│   ├── stability/
│   └── mitigation/
├── results/
│   ├── raw/
│   ├── metrics/
│   └── figures/
├── dashboard/
│   └── app.py
├── tests/
├── .env
├── requirements.txt
├── README.md
└── main.py
```

### Data record schema (paired counterfactual example)

```json
{
  "scenario_id": "REC_001",
  "domain": "recruitment",
  "occupation": "software_engineer",
  "prompt_id": "REC_001_P01",
  "prompt_variant": 1,
  "gender": "male",
  "name": "John",
  "prompt": "John has 5 years of experience...",
  "counterfactual_id": "REC_001_F01"
}
```
Female counterpart mirrors this with `gender: "female"`, `name: "Jane"`, and its own
`prompt_id`. The `counterfactual_id` field links male/female responses as a paired
observation for statistical testing.

### Model interface contract

```python
class BaseLLM:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
```
Subclasses: `OpenAIModel`, `GeminiModel`, `LlamaModel`, `QwenModel`. Pipeline only ever
calls `model.generate(prompt)`.

### Incremental build plan

```
V0.1 → 5 recruitment scenarios, M/F pairs, 1 LLM, 1–10 score extraction,
       JSON/CSV storage, mean bias + paired stat test + effect size
V0.2 → 4 models
V0.3 → 500+ scenarios
V0.4 → multiple metrics
V0.5 → stability
V0.6 → mitigation
V1.0 → dashboard + final framework
```

V0.1 sanity test: 5 scenarios × 2 genders × 2 prompts = 20 requests, before scaling to
~1,000 model queries per model (50 scenarios × 2 genders × 10 prompt variations).

---

## Open decision before implementation begins

Development environment — one of:
- A. Google Colab
- B. VS Code + local Python
- C. Jupyter Notebook
- D. VS Code + Python virtual environment (recommended, for a proper multi-module
  repo with experiments, tests, `.env`, and dashboard)

## Status

Planning only. **No implementation has been started per instruction.**
