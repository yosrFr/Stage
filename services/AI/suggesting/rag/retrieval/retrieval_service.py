from typing import Any, Dict, List, Optional

from config import settings
from services.AI.suggesting.rag.retrieval import text_utils, embedding_service
from services.AI.suggesting.rag.retrieval.retrieval_schemas import (
    ControlQuery,
    FindingQuery,
    RetrievedExample,
    RetrievalResult,
)
from services.database.vectorstore import chroma_client


def _strict_filter(norm_title: str, language: int) -> Dict[str, Any]:
    return {"$and": [{"norm_title": norm_title}, {"language": language}]}


def _language_only_filter(language: int) -> Dict[str, Any]:
    return {"language": language}


def _candidate_pool_size() -> int:
    """How many raw candidates to pull from Chroma before reranking."""
    return settings.RETRIEVAL_TOP_K * settings.RETRIEVAL_CANDIDATE_POOL_MULTIPLIER


def _run_cascade(
        collection_name: str,
        query_embedding: List[float],
        norm_title: str,
        language: int,
) -> tuple[Dict[str, Any], bool, bool, bool]:
    """
    returns raw_chroma_result, used_language_norm_filter, used_language_only_filter, used_no_filter_fallback
    """
    pool_size = _candidate_pool_size()

    # strict (language + norm_title)
    result = chroma_client.query_collection(
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=pool_size,
        where=_strict_filter(norm_title, language),
    )
    if len(result["ids"][0]) >= settings.RETRIEVAL_MIN_POOL_SIZE:
        return result, True, False, False

    # language only
    result = chroma_client.query_collection(
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=pool_size,
        where=_language_only_filter(language),
    )
    if len(result["ids"][0]) >= settings.RETRIEVAL_MIN_POOL_SIZE:
        return result, False, True, False

    # no filter at all (cross-language/norm cold start)
    result = chroma_client.query_collection(
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=pool_size,
        where=None,
    )
    return result, False, False, True


def _score_and_rank(
        raw_result: Dict[str, Any],
        query_risk_level: Optional[int],
        query_non_conformity: str,
        top_k: int,
) -> List[RetrievedExample]:
    """
    Turn a raw Chroma query result into ranked RetrievedExample objects,
    applying the risk_level / non_conformity soft-boost.

    Chroma returns cosine DISTANCE since collections are created with hnsw:space="cosine"
    """
    ids = raw_result["ids"][0]
    metadatas = raw_result["metadatas"][0]
    distances = raw_result["distances"][0]

    scored: List[RetrievedExample] = []
    for metadata, distance in zip(metadatas, distances):
        similarity = 1.0 - distance

        boost = 0.0
        candidate_risk_level = metadata.get("risk_level")
        if (
                query_risk_level is not None
                and candidate_risk_level is not None
                and candidate_risk_level != settings.UNKNOWN_RISK_LEVEL_SENTINEL
                and candidate_risk_level == query_risk_level
        ):
            boost += settings.RETRIEVAL_RISK_LEVEL_BOOST

        if metadata.get("non_conformity") == query_non_conformity:
            boost += settings.RETRIEVAL_NON_CONFORMITY_BOOST

        final_score = similarity + boost

        candidate_risk_level_out = (
            None
            if candidate_risk_level is None or candidate_risk_level == settings.UNKNOWN_RISK_LEVEL_SENTINEL
            else candidate_risk_level
        )

        scored.append(
            RetrievedExample(
                control_id=metadata["control_id"],
                norm_title=metadata["norm_title"],
                control_title=metadata["control_title"],
                finding=metadata["finding"],
                measures=(metadata.get("measures") or None),
                risk_level=candidate_risk_level_out,
                non_conformity=metadata["non_conformity"],
                language=metadata["language"],
                similarity_score=similarity,
                final_score=final_score,
            )
        )

    scored.sort(key=lambda ex: ex.final_score, reverse=True)
    return scored[:top_k]


def retrieve_finding_examples(query: ControlQuery) -> RetrievalResult:
    """
    Endpoint 1 retrieval:
        given a new control's identity, find similar past controls that already have human-written findings.
    """
    query_text = text_utils.build_control_embedding_text(
        query.norm_title,
        query.control_title,
        text_utils.strip_html(query.control_description or ""),
    )
    query_embedding = embedding_service.embed_query(query_text)

    raw_result, used_strict, used_lang_only, used_fallback = _run_cascade(
        collection_name=settings.CHROMA_COLLECTION_FINDINGS,
        query_embedding=query_embedding,
        norm_title=query.norm_title,
        language=query.language,
    )

    candidate_pool_size = len(raw_result["ids"][0])
    ranked = _score_and_rank(
        raw_result,
        query_risk_level=query.risk_level,
        query_non_conformity=query.non_conformity,
        top_k=settings.RETRIEVAL_TOP_K,
    )

    return RetrievalResult(
        examples=ranked,
        used_language_norm_filter=used_strict,
        used_language_only_filter=used_lang_only,
        used_no_filter_fallback=used_fallback,
        candidate_pool_size=candidate_pool_size,
    )


def retrieve_measure_examples(query: FindingQuery) -> RetrievalResult:
    """
    Endpoint 2 retrieval:
        given a newly generated finding, find similar past findings that already have human-written measures.

    Query text = the finding text itself, searched against the measures collection.
    """
    query_text = text_utils.build_finding_embedding_text(query.finding_text)
    query_embedding = embedding_service.embed_query(query_text)

    raw_result, used_strict, used_lang_only, used_fallback = _run_cascade(
        collection_name=settings.CHROMA_COLLECTION_MEASURES,
        query_embedding=query_embedding,
        norm_title=query.norm_title,
        language=query.language,
    )

    candidate_pool_size = len(raw_result["ids"][0])
    ranked = _score_and_rank(
        raw_result,
        query_risk_level=query.risk_level,
        query_non_conformity=query.non_conformity,
        top_k=settings.RETRIEVAL_TOP_K,
    )

    return RetrievalResult(
        examples=ranked,
        used_language_norm_filter=used_strict,
        used_language_only_filter=used_lang_only,
        used_no_filter_fallback=used_fallback,
        candidate_pool_size=candidate_pool_size,
    )
