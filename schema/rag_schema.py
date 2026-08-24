from pydantic import BaseModel

from services.AI.suggesting.rag.retrieval.retrieval_schemas import RetrievalResult


class RetrievalDiagnostics(BaseModel):
    num_examples_used: int
    candidate_pool_size: int
    used_language_norm_filter: bool  # strict tier: same language + same norm
    used_language_only_filter: bool  # relaxed tier: same language only
    used_no_filter_fallback: bool  # cold-start tier: no filter at all
    is_low_confidence: bool


def build_retrieval_diagnostics(result: RetrievalResult) -> RetrievalDiagnostics:
    return RetrievalDiagnostics(
        num_examples_used=len(result.examples),
        candidate_pool_size=result.candidate_pool_size,
        used_language_norm_filter=result.used_language_norm_filter,
        used_language_only_filter=result.used_language_only_filter,
        used_no_filter_fallback=result.used_no_filter_fallback,
        is_low_confidence=result.is_low_confidence,
    )


class FindingGenerationResponse(BaseModel):
    findings: list[str]  # 0 or more. The model decides how many genuinely apply
    retrieval: RetrievalDiagnostics


class MeasureGenerationResponse(BaseModel):
    measures: list[str]  # same length and order as the request's findings list
    retrieval: list[RetrievalDiagnostics]  # one entry per finding, same order
