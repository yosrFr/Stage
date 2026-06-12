import re

from services.ollama_client import generate_text
from services.prompt_builder import build_rewrite_prompt


def rewrite_value(text: str) -> str:
    prompt = build_rewrite_prompt(text)
    result = generate_text(prompt)

    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL)
    result = re.sub(r"\s*/think\s*$", "", result)
    result = re.sub(r"\s*/br>\s*$", "", result)  # malformed closing tag
    result = result.strip()

    return result
