Write-Host "== 1/5 generation ==" -ForegroundColor Cyan
python experiments/run_generation.py

Write-Host "== 2/5 baseline ==" -ForegroundColor Cyan
python experiments/run_baseline.py

Write-Host "== 3/5 stability ==" -ForegroundColor Cyan
python experiments/run_stability.py

Write-Host "== 4/5 mitigation ==" -ForegroundColor Cyan
python experiments/run_mitigation.py

Write-Host "== 5/5 fairness-utility ==" -ForegroundColor Cyan
python experiments/run_fairness_utility.py

Write-Host "All done. Launch dashboard with: python -m streamlit run dashboard/app.py" -ForegroundColor Green
