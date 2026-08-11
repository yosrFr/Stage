import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral-nemo"

SEED = 42


def generate_finding_text(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "seed": SEED,
                "temperature": 0,
                "repeat_penalty": 1.0,
                "num_ctx": 4096,
                "num_predict": 1536,
            },
        },
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    if data.get("done_reason") == "length":
        raise Exception(
            f"Model output was truncated at num_predict before the findings array. "
            f"Raw output: {data['response']}"
        )

    return data["response"].strip()
