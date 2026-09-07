@echo off
echo == 1/5 generation ==
python experiments/run_generation.py

echo == 2/5 baseline ==
python experiments/run_baseline.py

echo == 3/5 stability ==
python experiments/run_stability.py

echo == 4/5 mitigation ==
python experiments/run_mitigation.py

echo == 5/5 fairness-utility ==
python experiments/run_fairness_utility.py

echo All done. Launch dashboard with: python -m streamlit run dashboard/app.py
