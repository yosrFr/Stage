import requests

from threatflow.AI.prompt_builder import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "mistral-nemo"


def generate_text(conversation: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": DEFAULT_MODEL,
            "messages": messages,
            "stream": False,
        },
    )
    response.raise_for_status()
    return response.json()["message"]["content"]