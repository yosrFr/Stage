from typing import Any, Dict, List, Optional

import requests

from config import settings


class OllamaGenerationError(Exception):
    """
    Raised for any failure talking to Ollama: connection refused, timeout, non-2xx response,
    or an unexpected response shape.
    Callers (routes/services) should catch this specifically and turn it into a proper API error response,
    rather than letting a raw requests exception bubble up.
    """


def generate_completion(
        messages: List[Dict[str, Any]],
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        seed: Optional[int] = None,
        timeout_seconds: int = 120,
) -> str:
    """
    Send a chat-completion request to Ollama and return the generated text.
    """
    payload = {
        "model": model or settings.OLLAMA_MODEL,
        "messages": messages,
        "temperature": temperature if temperature is not None else settings.OLLAMA_TEMPERATURE,
        "seed": seed if seed is not None else settings.OLLAMA_SEED,
    }
    url = f"{settings.OLLAMA_BASE_URL}/chat/completions"

    try:
        response = requests.post(url, json=payload, timeout=timeout_seconds)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise OllamaGenerationError(
            f"Could not connect to Ollama at {settings.OLLAMA_BASE_URL}. "
            f"Is Ollama running (`ollama serve`) and is '{settings.OLLAMA_MODEL}' pulled? "
            f"Original error: {exc}"
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise OllamaGenerationError(
            f"Ollama request timed out after {timeout_seconds}s. The prompt may be too long, "
            f"or the model is taking longer than expected on this machine."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        raise OllamaGenerationError(
            f"Ollama returned an error (status {response.status_code}): {response.text}"
        ) from exc

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise OllamaGenerationError(
            f"Unexpected response shape from Ollama -- expected OpenAI-style "
            f"choices[0].message.content, got: {data}"
        ) from exc
