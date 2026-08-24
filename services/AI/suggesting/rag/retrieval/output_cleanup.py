import re
from typing import List, Optional

_WRAPPING_QUOTE_PAIRS = [
    ('"', '"'),
    ("'", "'"),
    ("\u201c", "\u201d"),  # curly double quotes “ ”
    ("\u2018", "\u2019"),  # curly single quotes ' '
]


def strip_llm_formatting_artifacts(text: str, known_labels: Optional[List[str]] = None) -> str:
    """
    Remove a leading "<Label>:" prefix and/or a single layer of wrapping quote characters around the entire remaining text.
    """
    cleaned = text.strip()

    for label in known_labels or []:
        pattern = rf"^{re.escape(label)}\s*:\s*"
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()

    if len(cleaned) >= 2:
        for start_q, end_q in _WRAPPING_QUOTE_PAIRS:
            if cleaned.startswith(start_q) and cleaned.endswith(end_q):
                cleaned = cleaned[1:-1].strip()
                break  # only strip ONE layer. Don't loop in case of nested legitimate quotes

    return cleaned
