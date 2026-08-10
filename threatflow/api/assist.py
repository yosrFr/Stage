import uuid

from fastapi import APIRouter, HTTPException

from threatflow.AI.ollama_client import generate_text
from threatflow.AI.prompt_builder import start_conversation, add_assistant_reply
from threatflow.fetch_item import fetch_item_by_id
from threatflow.schema.request import AssistRequest
from threatflow.schema.response import AssistResponse
from threatflow.session_store import sessions

router = APIRouter(prefix="/assist", tags=["assist"])


@router.post("/", response_model=AssistResponse)
def assist_me(request: AssistRequest):
    item = fetch_item_by_id(request.item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"No item found with id={request.item_id}")

    conversation = start_conversation(item)
    reply = generate_text(conversation)
    conversation = add_assistant_reply(conversation, reply)

    session_id = str(uuid.uuid4())
    sessions[session_id] = conversation

    return AssistResponse(session_id=session_id, reply=reply)