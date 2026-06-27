import numpy as np
from typing import Optional

# Lazy-loaded singleton for local model
_local_model = None


def _get_local_model():
    """Load SentenceTransformer model (singleton)."""
    global _local_model
    if _local_model is None:
        from sentence_transformers import SentenceTransformer
        _local_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _local_model


def embed_local(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings using local SentenceTransformer.
    Same model as existing create_embeddings.py: all-MiniLM-L6-v2
    Returns list of embedding vectors.
    """
    model = _get_local_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()


def embed_openai(texts: list[str], api_key: str, model: str = "text-embedding-3-small") -> list[list[float]]:
    """Generate embeddings using OpenAI API."""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    return [item.embedding for item in response.data]


def embed(
    texts: list[str],
    mode: str = "local",
    api_key: Optional[str] = None,
) -> list[list[float]]:
    """
    Unified embedding interface.
    mode: "local" (sentence-transformers) or "api" (OpenAI)
    """
    if mode == "api" and api_key:
        return embed_openai(texts, api_key)
    return embed_local(texts)


def embed_query(
    query: str,
    mode: str = "local",
    api_key: Optional[str] = None,
) -> list[float]:
    """Embed a single query string. Returns a single vector."""
    results = embed([query], mode=mode, api_key=api_key)
    return results[0]
