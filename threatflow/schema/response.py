from pydantic import BaseModel


class AssistResponse(BaseModel):
    session_id: str
    reply: str


class FollowupResponse(BaseModel):
    reply: str
