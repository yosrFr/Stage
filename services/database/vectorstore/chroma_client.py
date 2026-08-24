from functools import lru_cache
from typing import Any, Dict, List, Optional

import chromadb

from config import settings


@lru_cache(maxsize=1)
def get_client() -> chromadb.ClientAPI:
    """
    Return a singleton persistent Chroma client, stored on disk at settings.CHROMA_PERSIST_DIR.
    Cached so we don't reopen the store on every call.
    """
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)


def get_collection(collection_name: str):
    """
    Get (or create, if it doesn't exist yet) a named collection.

    We use cosine similarity explicitly (via hnsw:space metadata) because our embeddings are normalized.
    """
    client = get_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def upsert_examples(
        collection_name: str,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
) -> None:
    """
    Insert or update a batch of examples in the given collection.

    :param ids: unique identifiers
    :param embeddings: the vectors produced by embedding_service.embed_passages
    :param documents: the human-readable text
    :param metadatas: everything we need back at retrieval time (control_id, norm_title, risk_level, non_conformity,
    language, finding, measures)
    """
    collection = get_collection(collection_name)
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query_collection(
        collection_name: str,
        query_embedding: List[float],
        top_k: int,
        where: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Run a similarity search against a collection, optionally restricted by a metadata filter.

    Returns Chroma's raw query result dict (ids, documents, metadatas, distances).
    """
    collection = get_collection(collection_name)

    # Chroma errors if `where` is an empty dict, so normalize to None.
    where = where or None

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
    )


def count(collection_name: str) -> int:
    """
    Number of items currently stored in a collection.
    Useful for diagnostics and for the cold-start.
    """
    return get_collection(collection_name).count()
