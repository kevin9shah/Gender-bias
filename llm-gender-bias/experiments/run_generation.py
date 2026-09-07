"""Generate all model responses for the counterfactual prompt set.

This is the only script that loads models and performs inference. It writes
one row per (model, prompt) to results/raw/responses_<run_id>.csv. All
downstream scripts (baseline/stability/mitigation/fairness_utility) read
from this file.
"""
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml

sys.path.insert(0, ".")

from src.data.scenarios import DOMAINS, scenarios_by_domain
from src.models.registry import load_models
from src.prompting.generator import generate_all
from src.storage.store import ResponseStore, now_iso

_progress_lock = threading.Lock()
_done = 0


def _run_one_model(slot, model, prompt_records, max_new_tokens, temperature, store, total, t0):
    global _done
    for rec in prompt_records:
        response = model.generate(rec.prompt, max_new_tokens=max_new_tokens)
        store.write({
            "model": slot,
            "model_version": model.version,
            "family": model.family,
            "domain": rec.domain,
            "scenario_id": rec.scenario_id,
            "prompt_id": rec.prompt_id,
            "prompt_variant": rec.prompt_variant,
            "counterfactual_id": rec.counterfactual_id,
            "experiment": "baseline_stability",
            "gender": rec.gender,
            "name": rec.name,
            "temperature": temperature,
            "timestamp": now_iso(),
            "prompt": rec.prompt,
            "response": response,
        })
        with _progress_lock:
            global _done
            _done += 1
            if _done % 10 == 0:
                elapsed = time.time() - t0
                rate = _done / elapsed
                eta = (total - _done) / rate if rate > 0 else float("inf")
                print(f"[gen] {_done}/{total} ({rate:.2f}/s, ETA {eta/60:.1f} min)")


def main():
    with open("configs/experiment.yaml") as f:
        cfg = yaml.safe_load(f)

    run_id = cfg["run_id"]
    default_max_tokens = cfg["generation"]["max_new_tokens"]
    temperature = cfg["generation"]["temperature"]
    n_per_domain = cfg["data"]["scenarios_per_domain"]
    n_variants = cfg["data"]["prompt_variants"]

    per_model_max_tokens = {
        spec["slot"]: spec.get("max_new_tokens", default_max_tokens) for spec in cfg["models"]
    }

    scenarios = []
    for domain in DOMAINS:
        scenarios.extend(scenarios_by_domain(domain)[:n_per_domain])

    print("[gen] loading models ...")
    models = load_models()

    print(f"[gen] generating prompt set ({len(scenarios)} scenarios, {n_variants} variants) ...")
    prompt_records = generate_all(scenarios, n_variants=n_variants)
    total = len(prompt_records) * len(models)
    print(f"[gen] {len(prompt_records)} prompts x {len(models)} models = {total} generations "
          f"(running one thread per model in parallel)")

    out_path = f"results/raw/responses_{run_id}.csv"
    store = ResponseStore(out_path)
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        futures = {
            pool.submit(
                _run_one_model, slot, model, prompt_records,
                per_model_max_tokens[slot], temperature, store, total, t0,
            ): slot
            for slot, model in models.items()
        }
        for fut in as_completed(futures):
            slot = futures[fut]
            fut.result()  # re-raises if the model thread crashed
            print(f"[gen] {slot} finished")

    store.close()
    print(f"[gen] done. wrote {out_path}")


if __name__ == "__main__":
    main()
