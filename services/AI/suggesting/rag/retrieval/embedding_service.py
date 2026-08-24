from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

from config import settings


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    """
    Load the embedding model once and cache it.
    """
    return SentenceTransformer(
        settings.EMBEDDING_MODEL_NAME,
        device=settings.EMBEDDING_DEVICE,
    )


def embed_passages(texts: List[str]) -> List[List[float]]:
    """
    Embed a batch of texts that will be STORED/INDEXED.
    Applies the "passage: " prefix required by the model.

    Returns a list of embedding vectors (one per input text, same order).
    """
    if not texts:
        return []

    prefixed = [f"passage: {t}" for t in texts]
    model = _get_model()
    vectors = model.encode(
        prefixed,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()


def embed_query(text: str) -> List[float]:
    """
    Embed a single SEARCH QUERY.
    Applies the "query: " prefix required by the model.
    """
    model = _get_model()
    vector = model.encode(
        f"query: {text}",
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vector.tolist()
