from services.AI.suggesting.prompt_engineered.finding_only.json_list_utils import parse_json_list
from services.AI.suggesting.prompt_engineered.pe_ollama_client import generate_text
from services.AI.suggesting.prompt_engineered.finding_only.finding_prompt_builder import build_finding_suggestion_prompt


def suggest_findings(data: dict) -> list:
    """
    Suggests findings using the configured model.
    Builds a prompt from the input data,
    sends it to Ollama
    and cleans the response before returning
    """
    prompt = build_finding_suggestion_prompt(data)
    result = generate_text(prompt)

    result = result.strip()

    return parse_json_list(result)
