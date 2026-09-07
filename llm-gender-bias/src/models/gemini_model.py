import os
import time

from google import genai

from src.models.base import BaseLLM


class GeminiModel(BaseLLM):
    def __init__(self, slot: str, model_id: str, family: str = "Google"):
        self.name = slot
        self.family = family
        self.version = model_id
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set (check .env)")
        self._client = genai.Client(api_key=api_key)
        self._model_id = model_id

    def generate(self, prompt: str, max_new_tokens: int = 96) -> str:
        for attempt in range(3):
            try:
                resp = self._client.models.generate_content(
                    model=self._model_id,
                    contents=prompt,
                    config={
                        "max_output_tokens": max_new_tokens,
                        "temperature": 0.7,
                        # gemini-3.6-flash cannot fully disable thinking; "low"
                        # is the minimum that avoids burning the whole token
                        # budget on hidden thoughts before any visible text.
                        "thinking_config": {"thinking_level": "low"},
                    },
                )
                return (resp.text or "").strip()
            except Exception as e:
                if attempt == 2:
                    return f"[GENERATION_ERROR: {e}]"
                time.sleep(2 * (attempt + 1))
        return ""
