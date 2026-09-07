import os
import time

from groq import Groq

from src.models.base import BaseLLM


class GroqModel(BaseLLM):
    def __init__(self, slot: str, model_id: str, family: str, api_key_env: str = "GROQ_API_KEY",
                 extra_params: dict | None = None):
        self.name = slot
        self.family = family
        self.version = model_id
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise RuntimeError(f"{api_key_env} not set (check .env)")
        self._client = Groq(api_key=api_key)
        self._model_id = model_id
        # e.g. {"reasoning_effort": "none"} for Qwen -- some reasoning models
        # burn the whole max_tokens budget on hidden thinking otherwise,
        # leaving zero room for the actual answer.
        self._extra_params = extra_params or {}

    def generate(self, prompt: str, max_new_tokens: int = 96) -> str:
        for attempt in range(3):
            try:
                resp = self._client.chat.completions.create(
                    model=self._model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_new_tokens,
                    temperature=0.7,
                    reasoning_format="hidden",
                    **self._extra_params,
                )
                return (resp.choices[0].message.content or "").strip()
            except Exception as e:
                if attempt == 2:
                    return f"[GENERATION_ERROR: {e}]"
                time.sleep(2 * (attempt + 1))
        return ""
