from typing import List, Optional
from pydantic import BaseModel

from services.AI.suggesting.rag.retrieval.retrieval_schemas import FindingQuery


class MeasureGenerationRequest(BaseModel):
    """
    Internal, single-finding shape.
    What the prompt builder and retrieval actually consume.
    Not the endpoint's request body.
    """

    norm_title: str
    control_id: str
    control_title: str
    control_description: Optional[str] = None
    risk_level: Optional[int] = None
    non_conformity: str
    current_state: str
    language: int
    finding: str  # the ONE finding this request is generating a measure for

    def to_finding_query(self) -> FindingQuery:
        """
        Build the retrieval query from this request.
        Retrieval for measures is keyed on the FINDING TEXT (not the control text).
        """
        return FindingQuery(
            finding_text=self.finding,
            norm_title=self.norm_title,
            language=self.language,
            risk_level=self.risk_level,
            non_conformity=self.non_conformity,
        )


class MeasureBatchGenerationRequest(BaseModel):
    """
    endpoint 2 request body: shared control context + a list of findings.
    """

    norm_title: str
    control_id: str
    control_title: str
    control_description: Optional[str] = None
    risk_level: Optional[int] = None
    non_conformity: str
    current_state: str
    language: int
    findings: List[str]

    def to_single_requests(self) -> List[MeasureGenerationRequest]:
        """
        One MeasureGenerationRequest per finding, sharing the same control context.
        Order is preserved. This order is what keeps the final measures list aligned with the input findings list.
        """
        return [
            MeasureGenerationRequest(
                norm_title=self.norm_title,
                control_id=self.control_id,
                control_title=self.control_title,
                control_description=self.control_description,
                risk_level=self.risk_level,
                non_conformity=self.non_conformity,
                current_state=self.current_state,
                language=self.language,
                finding=finding_text,
            )
            for finding_text in self.findings
        ]
