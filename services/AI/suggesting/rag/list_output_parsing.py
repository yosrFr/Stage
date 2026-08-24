import re
from typing import List

from services.AI.suggesting.rag.retrieval.output_cleanup import strip_llm_formatting_artifacts

# Matches a numbered list marker ("1.", "1)", "2 -") or a bullet ("-", "*", "•") at the start of a line.
_LIST_MARKER_PATTERN = re.compile(r"^\s*(?:\d+[\.\)]|[-*\u2022])\s*")

_NONE_SENTINELS = {"none", "no findings", "no findings needed", "no finding needed", "n/a"}


def parse_findings_list(raw_text: str) -> List[str]:
    """
    Turn the model's raw response into a list of finding strings.

    Handles:
    - The explicit "NONE" sentinel (case-insensitive, with or without trailing punctuation) -> returns [].
    - A numbered or bulleted list -> one entry per line, markers stripped.
    - A single unmarked line (model ignored the list format but only wrote one finding)
      -> treated as a single-item list, not discarded.
    - Stray label/quote artifacts per line, cleaned via the output_cleanup.
    """
    text = raw_text.strip()
    if not text:
        return []

    # Explicit "no findings" case.
    # Check the whole response, not just the first line, in case the model added trailing punctuation/whitespace.
    normalized = text.strip(" .!\n\t").lower()
    if normalized in _NONE_SENTINELS:
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # If NONE appears as a lone line among otherwise-empty output, also treat as zero.
    if len(lines) == 1 and lines[0].strip(" .!").lower() in _NONE_SENTINELS:
        return []

    findings: List[str] = []
    for line in lines:
        content = _LIST_MARKER_PATTERN.sub("", line).strip()
        content = strip_llm_formatting_artifacts(content, known_labels=["Finding"])
        if content:
            findings.append(content)

    return findings
