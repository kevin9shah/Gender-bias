# LLM Gender Bias Evaluation Framework — Review 1

See `architecture.md` (system design, model substitution rationale) and
`implementation.md` (scope, build order, honest limitations) in this folder.
`../task.md` has the full literature/gap/objective/project-plan writeup.

## Setup

```bash
pip install -r requirements.txt
```

## Run the full pipeline

```bash
./run_all.sh
```

This runs, in order: generation (loads 4 local models, produces all
counterfactual responses) → baseline evaluation → stability analysis →
mitigation experiments → fairness-utility analysis. All knobs (scenario
count, prompt-variant count, mitigation top-K) are in
`configs/experiment.yaml`.

Individual stages can be re-run independently once `results/raw/` exists,
e.g. `python3 experiments/run_baseline.py`.

## Dashboard

```bash
streamlit run dashboard/app.py
```

Reads precomputed CSVs from `results/metrics/` — no live model calls during
the demo.
