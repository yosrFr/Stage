from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class ControlQuery(BaseModel):
    """
    Input for retrieving past "control -> finding" examples.
    Mirrors the fields the finding-generation endpoint actually receives.
    """

    norm_title: str
    control_id: str
    control_title: str
    control_description: Optional[str] = None
    risk_level: Optional[int] = None
    non_conformity: str
    language: int


class FindingQuery(BaseModel):
    """
    Input for retrieving past "finding -> measures" examples.
    """

    finding_text: str
    norm_title: str
    language: int
    risk_level: Optional[int] = None
    non_conformity: str


class RetrievedExample(BaseModel):
    """
    One retrieved example, already ranked, ready to hand to a prompt builder.
    `similarity_score` is the raw semantic score before boosts.
    `final_score` includes the risk_level/non_conformity soft-boost and is
    what determines ranking order.
    """

    control_id: str
    norm_title: str
    control_title: str
    finding: str
    measures: Optional[str] = None
    risk_level: Optional[int] = None
    non_conformity: str
    language: int
    similarity_score: float
    final_score: float


class RetrievalResult(BaseModel):
    """
    Full result of a retrieval call, including diagnostic info a caller can use to judge confidence.
    """

    examples: List[RetrievedExample]
    used_language_norm_filter: bool  # True if the strict (language+norm) filter had enough candidates
    used_language_only_filter: bool  # True if we had to relax to language-only
    used_no_filter_fallback: bool  # True if we had to relax all the way (cross-language/norm cold start)
    candidate_pool_size: int  # how many candidates were available before final top_k selection

    @property
    def is_low_confidence(self) -> bool:
        """
        True if retrieval had to fall back past the norm-level filter, or found nothing at all.
        """
        return self.used_no_filter_fallback or len(self.examples) == 0
