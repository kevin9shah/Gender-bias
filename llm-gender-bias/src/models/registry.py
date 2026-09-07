import os

import yaml
from dotenv import load_dotenv

from src.models.gemini_model import GeminiModel
from src.models.groq_model import GroqModel
from src.models.local_hf import LocalHFModel
from src.models.octopus_model import OctopusModel
from src.models.ollama_model import OllamaModel, ollama_available

# Project keys were provided in a file named .ENV; look for both spellings
# (macOS default filesystem is case-insensitive, but this keeps it portable).
for candidate in (".env", ".ENV", ".api_key_env", "../.env", "../.ENV", "../.api_key_env"):
    if os.path.exists(candidate):
        load_dotenv(candidate, override=True)
        break


def _build_gemini(spec):
    return GeminiModel(spec["slot"], spec["model_id"], spec["family"])


def _build_groq(spec):
    return GroqModel(spec["slot"], spec["model_id"], spec["family"],
                      api_key_env=spec.get("api_key_env", "GROQ_API_KEY"),
                      extra_params=spec.get("extra_params"))


def _build_local_hf(spec):
    return LocalHFModel(spec["slot"], spec["hf_id"], spec["kind"], spec["family"])


def _build_octopus(spec):
    return OctopusModel(
        slot=spec.get("slot", "octopus_family"),
        model_id=spec.get("model_id", "octopus-v1-debiased"),
        family=spec.get("family", "Octopus"),
        backbone_provider=spec.get("backbone_provider", "gemini"),
    )


def _build_ollama_or_groq(spec):
    """Prefer local Ollama (no API cost, no rate limit); fall back to Groq
    only if the local model isn't available."""
    ollama_id = spec["ollama_id"]
    if ollama_available(ollama_id):
        print(f"[registry]   -> using local Ollama ({ollama_id})")
        return OllamaModel(spec["slot"], ollama_id, spec["family"])
    print(f"[registry]   -> Ollama model '{ollama_id}' not found locally, "
          f"falling back to Groq ({spec['fallback_model_id']})")
    return GroqModel(spec["slot"], spec["fallback_model_id"], spec["family"],
                      api_key_env=spec.get("api_key_env", "GROQ_API_KEY"))


_BUILDERS = {
    "gemini": _build_gemini,
    "groq": _build_groq,
    "local_hf": _build_local_hf,
    "octopus": _build_octopus,
    "ollama_or_groq": _build_ollama_or_groq,
}


def load_models(config_path: str = "configs/experiment.yaml") -> dict:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    models = {}
    for spec in cfg["models"]:
        provider = spec["provider"]
        label = spec.get("model_id") or spec.get("hf_id") or spec.get("ollama_id")
        print(f"[registry] loading {spec['slot']} via {provider} ({label}) ...")
        models[spec["slot"]] = _BUILDERS[provider](spec)
    return models
