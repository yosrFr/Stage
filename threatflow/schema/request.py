from pydantic import BaseModel


class AssistRequest(BaseModel):
    item_id: int


class FollowupRequest(BaseModel):
    session_id: str
    question: str
