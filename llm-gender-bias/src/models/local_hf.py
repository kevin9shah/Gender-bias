import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from src.models.base import BaseLLM

_DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"


class LocalHFModel(BaseLLM):
    """Wraps a local Hugging Face model (causal or seq2seq) behind BaseLLM."""

    def __init__(self, slot: str, hf_id: str, kind: str, family: str, seed: int = 42):
        self.name = slot
        self.hf_id = hf_id
        self.kind = kind
        self.family = family
        self.version = hf_id
        self._seed = seed

        self.tokenizer = AutoTokenizer.from_pretrained(hf_id)
        if kind == "seq2seq":
            self.model = AutoModelForSeq2SeqLM.from_pretrained(hf_id)
        else:
            self.model = AutoModelForCausalLM.from_pretrained(hf_id)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.to(_DEVICE)
        self.model.eval()

        self._has_chat_template = (
            kind == "causal" and getattr(self.tokenizer, "chat_template", None)
        )

    def _build_input(self, prompt: str) -> str:
        if self._has_chat_template:
            messages = [{"role": "user", "content": prompt}]
            return self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        return prompt

    def generate(self, prompt: str, max_new_tokens: int = 96) -> str:
        torch.manual_seed(self._seed)
        text_in = self._build_input(prompt)
        inputs = self.tokenizer(text_in, return_tensors="pt", truncation=True, max_length=768)
        inputs = {k: v.to(_DEVICE) for k, v in inputs.items()}

        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
            )

        if self.kind == "seq2seq":
            decoded = self.tokenizer.decode(out[0], skip_special_tokens=True)
        else:
            gen_tokens = out[0][inputs["input_ids"].shape[1]:]
            decoded = self.tokenizer.decode(gen_tokens, skip_special_tokens=True)

        return decoded.strip()
