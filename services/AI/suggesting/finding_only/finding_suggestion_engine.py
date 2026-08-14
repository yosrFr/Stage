from helpers.parse_json_list import parse_json_list
from services.AI.suggesting.ollama_client import generate_text
from services.AI.suggesting.finding_only.finding_prompt_builder import build_finding_suggestion_prompt


def suggest_findings(data: dict) -> list:
    prompt = build_finding_suggestion_prompt(data)
    result = generate_text(prompt)

    result = result.strip()

    return parse_json_list(result)
