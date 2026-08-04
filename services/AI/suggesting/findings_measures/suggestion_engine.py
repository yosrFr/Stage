import json

from services.AI.ollama_client import generate_text
from services.AI.suggesting.findings_measures.prompt_builder import build_finding_suggestion_prompt, \
    build_measure_suggestion_prompt


def parse_json_list(raw: str) -> list:
    raw = raw.strip()
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
        raise ValueError("Expected a JSON list")
    except json.JSONDecodeError as e:
        raise ValueError(f"Model did not return valid JSON: {e}\nRaw output: {raw}")


def suggest_finding(data: dict) -> list:
    prompt = build_finding_suggestion_prompt(data)
    result = generate_text(prompt)

    result = result.strip()

    return parse_json_list(result)


def suggest_measures(data: dict):
    findings = suggest_finding(data)

    suggested_data = []

    for finding in findings:
        item_data = {**data, "finding": finding}

        prompt = build_measure_suggestion_prompt(item_data)
        result = generate_text(prompt)

        result = result.strip()

        suggested_data.append({"finding": finding, "measure": result})

    return suggested_data
