import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen3:8b"


def generate_text(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Send a prompt to Ollama API and return the generated text

    :param prompt: The full prompt string to send to the model
    :param model: The Ollama model to use for generation
    :return: The generated text string, stripped of leading and trailing whitespace

    Notes:
    - 'thinking' is disabled to prevent qwen's3 chain-of-thought tokens (<think>...</think> or bare /think)
      from leaking into the output
    - 'temperature' is very low (0.1) to reduce the model creativity which minimises drifting away from the source text
    """
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "thinking": False,
            },
        }
    )

    response.raise_for_status()

    return response.json()["response"].strip()
