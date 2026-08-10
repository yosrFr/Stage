from fastapi import APIRouter, HTTPException

from threatflow.AI.ollama_client import generate_text
from threatflow.AI.prompt_builder import add_followup, add_assistant_reply
from threatflow.schema.request import FollowupRequest
from threatflow.schema.response import FollowupResponse
from threatflow.session_store import sessions

router = APIRouter(prefix="/followup", tags=["followup"])


@router.post("/", response_model=FollowupResponse)
def ask_followup(request: FollowupRequest):
    conversation = sessions.get(request.session_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Session not found or expired. Please click 'Assist me' again.")

    conversation = add_followup(conversation, request.question)
    reply = generate_text(conversation)
    conversation = add_assistant_reply(conversation, reply)

    sessions[request.session_id] = conversation

    return FollowupResponse(reply=reply)