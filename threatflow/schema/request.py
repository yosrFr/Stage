from pydantic import BaseModel, Field


class AssistRequest(BaseModel):
    item_id: int


class FollowupRequest(BaseModel):
    session_id: str
    question: str = Field(..., min_length=1, max_length=2000)
