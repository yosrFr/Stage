import re

from services.ollama_client import generate_text
from services.prompt_builder import build_rewrite_prompt


def rewrite_value(text: str) -> str:
    """
    Paraphrases a text using the configured model
    Builds a prompt from the input text,
    sends it to Ollama,
    removes know model putput artifacts from the generated text
    and cleans the response before returning
    """
    prompt = build_rewrite_prompt(text)
    result = generate_text(prompt)

    # Remove <think>...</think> blocks including any content inside
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL)
    # Remove /think token that sometimes appears at the end of the output
    result = re.sub(r"\s*/think\s*$", "", result)
    # Remove malformed closing tag /br>
    result = re.sub(r"\s*/br>\s*$", "", result)
    result = result.strip()

    return result
