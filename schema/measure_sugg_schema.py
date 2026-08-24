from typing import List, Optional
from pydantic import BaseModel


class MeasureSuggestionRequest(BaseModel):
    norm_title: str
    control_id: str
    control_title: str
    control_description: Optional[str] = None
    risk_level: Optional[int] = None
    non_conformity: str
    current_state: str
    language: int
    findings: List[str]
