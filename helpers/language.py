import re
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

GERMAN_MARKERS = re.compile(
    r"[äöüßÄÖÜ]|\b(nicht|werden|könnte|sind|keine|für|mit|ohne|und|der|die|das)\b",
    re.IGNORECASE
)


def detect_language(text: str) -> str:
    """
    Detects the language of a text and verifies the result against known German-specific markers to reduce false
    positives/negatives from langdetect, which is unreliable on short technical sentences.
    """
    if len(text.strip()) < 20:
        return "de" if GERMAN_MARKERS.search(text) else "en"

    try:
        lang = detect(text)
    except Exception:
        lang = "en"

    if lang == "de" and not GERMAN_MARKERS.search(text):
        lang = "en"

    return lang