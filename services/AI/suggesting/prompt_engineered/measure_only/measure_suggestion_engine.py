from services.AI.suggesting.prompt_engineered.pe_ollama_client import generate_text
from services.AI.suggesting.prompt_engineered.measure_only.measure_prompt_builder import build_measure_suggestion_prompt


def suggest_measures(data: dict) -> str:
    """
    Suggests a measure using the configured model
    Builds a prompt from the input data,
    sends it to Ollama
    and cleans the response before returning
    """
    prompt = build_measure_suggestion_prompt(data)
    result = generate_text(prompt)

    result = result.strip()

    return result
