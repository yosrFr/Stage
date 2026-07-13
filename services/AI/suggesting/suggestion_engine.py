from services.AI.ollama_client import generate_text
from services.AI.suggesting.prompt_builder import build_rewrite_prompt


def suggest_text(text: str) -> str:
    """
    Suggests a measure using the configured model
    Builds a prompt from the input text,
    sends it to Ollama
    and cleans the response before returning
    """
    prompt = build_rewrite_prompt(text)
    result = generate_text(prompt)

    result = result.strip()

    return result
