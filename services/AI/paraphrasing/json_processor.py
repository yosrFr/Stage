import logging
import re

from services.AI.paraphrasing.rewrite_engine import rewrite_value

from langdetect import detect, LangDetectException

TARGET_FIELDS = {"description", "objective"}

logging.basicConfig(
    filename="paraphrase.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

LANG_CODES = {"deutsch": "de", "english": "en"}

KEYWORD_RE = re.compile(
    r"<strong>\s*"
    r"(Must|Shall|Should|Need|"
    r"Muss|Soll|Sollte|"
    r"(?:Very\s+)?High\s+Protection|"
    r"(?:Sehr\s+)?Hoher\s+Schutz)"
    r"\s*</strong>",
    re.IGNORECASE
)


def process_json(obj) -> None:
    """
    Recursive function that runs through the JSON object and rewrites TARGET_FIELDS values in place.

    Checks in a nested structure whether the key is in the TARGET_FIELDS. If so, and the value is a non empty string,
    it is sent to the model for paraphrasing.

    The results are validated before being written back. If the validation fails the original value stays unchanged.
    """
    if isinstance(obj, dict):
        expected_lang = obj.get("language")

        for key, value in obj.items():
            if key in TARGET_FIELDS and isinstance(value, str) and value.strip():
                rewritten = rewrite_value(value, expected_lang=expected_lang)

                # Only overwrite if the model output passes validation, otherwise, the original value is preserved
                if is_valid_output(value, rewritten, expected_lang=expected_lang):
                    obj[key] = rewritten
                else:
                    # Logging the unchanged values
                    logging.info(f"Model output is invalid, the original value is unchanged. Original text: {value}")
            else:
                process_json(value)

    elif isinstance(obj, list):
        for item in obj:
            process_json(item)


def strip_html(s: str) -> str:
    """ Strip HTML tags from a string. """
    return re.sub(r"<[^>]+>", " ", s)


def is_valid_output(original: str, rewritten: str, expected_lang: str) -> bool:
    """
    Validates the generated paraphrase before overwriting the original JSON field.

    It is used to reduce hallucinated responses, extreme length changes and residual artifacts.

    It checks :
    - The response is non empty string
    - The output length must not be way shorter or longer than the original length to ensure that
      the model did not hallucinate, truncate or expand the content.
    - Residual artifacts
    - The only change is the omission of the html tags at the end of the text
    - The model didn't make any changes
    - The model's output language is different from the input
    - The model omitted the intro paragraph of the input
    """
    # Output must not be empty
    if not rewritten.strip():
        return False

    # Paraphrasing should produce the same amount of text as the original input
    ratio = len(rewritten) / len(original)
    if not (0.4 <= ratio <= 1.8):
        return False

    # Reject outputs with specific artifacts
    if any(artifact in rewritten for artifact in ["/think", "<think>", "It seems like your message"]):
        return False

    # If the only difference between the Input and the Output is <br><br> at the end
    if original == rewritten + "<br><br>":
        return False

    # If the model didn't make any changes
    if original == rewritten:
        return False

    # The model's output language is different from the input's
    if not is_same_language(rewritten, expected_lang):
        return False

    # Checks if the model omitted the intro paragraph of the input
    if not intro_paragraph_preserved(original, rewritten):
        return False

    return True


def is_same_language(rewritten: str, expected_lang: str) -> bool:
    """
    Checks whether the original language matches the expected language.

    Detects the language of the output and checks if it's in the same language as the input.

    :param rewritten: the output text
    :param expected_lang: the expected language
    """
    expected_code = LANG_CODES.get(expected_lang)

    try:
        return detect(strip_html(rewritten)) == expected_code
    except LangDetectException:
        return True


def intro_len(text: str) -> int:
    """ Returns the length of the intro paragraph. """
    m = KEYWORD_RE.search(text)

    return len(strip_html(text[:m.start()])) if m else 0


def intro_paragraph_preserved(original: str, rewritten: str) -> bool:
    """
    Checks whether the original paragraph preserves the intro paragraph of the input.

    Checks if the length of the output's intro paragraph is not less than half the size of the input's intro paragraph.
    """
    orig_intro = intro_len(original)

    if orig_intro < 20:
        return True

    return intro_len(rewritten) >= orig_intro * 0.5
