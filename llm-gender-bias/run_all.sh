#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "== 1/5 generation =="
python3 experiments/run_generation.py
echo "== 2/5 baseline =="
python3 experiments/run_baseline.py
echo "== 3/5 stability =="
python3 experiments/run_stability.py
echo "== 4/5 industry benchmarks =="
python3 experiments/run_benchmarks.py
echo "== 5/5 mitigation + fairness-utility =="
python3 experiments/run_mitigation.py
python3 experiments/run_fairness_utility.py
echo "All done. Launch dashboard with: streamlit run dashboard/app.py"
