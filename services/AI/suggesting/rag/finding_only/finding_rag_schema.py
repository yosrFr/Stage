from typing import Optional
from pydantic import BaseModel

from services.AI.suggesting.rag.retrieval.retrieval_schemas import ControlQuery


class FindingGenerationRequest(BaseModel):
    norm_title: str
    control_id: str
    control_title: str
    control_description: Optional[str] = None
    risk_level: Optional[int] = None
    non_conformity: str
    current_state: str
    language: int

    def to_control_query(self) -> ControlQuery:
        """
        Build the retrieval query from this request.
        """
        return ControlQuery(
            norm_title=self.norm_title,
            control_id=self.control_id,
            control_title=self.control_title,
            control_description=self.control_description,
            risk_level=self.risk_level,
            non_conformity=self.non_conformity,
            language=self.language,
        )
