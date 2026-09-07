import csv
import os
import threading
from datetime import datetime, timezone

FIELDS = [
    "model", "model_version", "family", "domain", "scenario_id",
    "prompt_id", "prompt_variant", "counterfactual_id", "experiment",
    "gender", "name", "temperature", "timestamp", "prompt", "response",
]


class ResponseStore:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._file_exists = os.path.exists(path)
        self._fh = open(path, "a", newline="", encoding="utf-8")
        self._writer = csv.DictWriter(self._fh, fieldnames=FIELDS)
        self._lock = threading.Lock()
        if not self._file_exists:
            self._writer.writeheader()

    def write(self, row: dict):
        clean = {k: row.get(k, "") for k in FIELDS}
        with self._lock:
            self._writer.writerow(clean)
            self._fh.flush()

    def close(self):
        self._fh.close()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
