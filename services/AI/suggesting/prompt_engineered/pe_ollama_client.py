import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral-nemo"
SEED = 42


class OllamaError(Exception):
    """Raised when the Ollama call fails or returns something unusable."""


def generate_text(prompt: str) -> str:
    try:
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
    except requests.exceptions.RequestException as exc:
        raise OllamaError(f"Could not reach Ollama at {OLLAMA_URL}: {exc}") from exc

    data = response.json()

    if "error" in data:
        raise OllamaError(data["error"])

    if data.get("done_reason") == "length":
        raise OllamaError(
            f"Model output was truncated at num_predict before the findings array. "
            f"Raw output: {data['response']}"
        )

    return data["response"].strip()