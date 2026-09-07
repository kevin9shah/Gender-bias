import requests

from src.models.base import BaseLLM

_OLLAMA_URL = "http://localhost:11434/api/generate"


def ollama_available(model_id: str) -> bool:
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        r.raise_for_status()
        names = [m["name"] for m in r.json().get("models", [])]
        return any(n == model_id or n.split(":")[0] == model_id.split(":")[0] for n in names)
    except requests.RequestException:
        return False


class OllamaModel(BaseLLM):
    def __init__(self, slot: str, model_id: str, family: str):
        self.name = slot
        self.family = family
        self.version = model_id
        self._model_id = model_id

    def generate(self, prompt: str, max_new_tokens: int = 96) -> str:
        try:
            r = requests.post(
                _OLLAMA_URL,
                json={
                    "model": self._model_id,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": max_new_tokens},
                },
                timeout=120,
            )
            r.raise_for_status()
            return r.json().get("response", "").strip()
        except requests.RequestException as e:
            return f"[GENERATION_ERROR: {e}]"
