from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionResponse(BaseModel):
    finding: Optional[str] = None
    measures: Optional[str] = None


class ControlRecord(BaseModel):
    norm_title: str
    control_id: str
    control_title: str
    control_description: Optional[str] = None
    language: int
    risk_level: Optional[int] = None
    non_conformity: str
    current_state: str
    question_responses: List[QuestionResponse] = Field(default_factory=list)

    def has_usable_examples(self) -> bool:
        """
        True if this record has at least one non-empty finding somewhere in its question_responses.
        Records with no findings at all (question_responses == [] or every finding is None/empty) can
        exist in the source data but must NOT be indexed as retrievable examples.
        """
        return any(
            qr.finding is not None and qr.finding.strip() != ""
            for qr in self.question_responses
        )


class IndexedExample(BaseModel):
    """
    One row as actually stored in ChromaDB.

    Every IndexedExample maps back to exactly one QuestionResponse from exactly one ControlRecord.
    If a control has 3 filled question_responses, it produces 3 separate IndexedExamples.
    """

    example_id: str
    norm_title: str
    control_id: str
    control_title: str
    control_description_clean: Optional[str] = None
    language: int
    risk_level: Optional[int] = None
    non_conformity: str
    finding: str
    measures: Optional[str] = None
    embedding_text: str
