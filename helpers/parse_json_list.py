import json
import re

def parse_json_list(raw: str) -> list:
    text = raw.strip()

    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass

    unescaped = text.replace('\\"', '"')
    try:
        parsed = json.loads(unescaped)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass

    try:
        once = json.loads(text)
        if isinstance(once, str):
            twice = json.loads(once)
            if isinstance(twice, list):
                return twice
    except (json.JSONDecodeError, TypeError):
        pass

    # Extract a JSON array embedded in surrounding prose/preamble
    match = re.search(r"\[.*\]", text, flags=re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            try:
                parsed = json.loads(candidate.replace('\\"', '"'))
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass

    raise ValueError(f"Model did not return valid JSON after recovery attempts. Raw output: {raw}")