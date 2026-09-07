from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(_MODEL_NAME)


def cosine_similarity(text_a: str | None, text_b: str | None) -> float:
    if not text_a or not text_b or not isinstance(text_a, str) or not isinstance(text_b, str):
        return 0.0
    model = _get_model()
    emb = model.encode([text_a, text_b], normalize_embeddings=True)
    return float(np.dot(emb[0], emb[1]))


def cosine_divergence(text_a: str, text_b: str) -> float:
    return 1.0 - cosine_similarity(text_a, text_b)
