import logging

from services.rewrite_engine import rewrite_value

TARGET_FIELDS = {"description", "objective"}

logging.basicConfig(
    filename="paraphrase.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_json(obj) -> None:
    """
    Recursive function that runs through the JSON object and rewrites TARGET_FIELDS values in place.

    Checks in a nested structure whether the key is in the TARGET_FIELDS. If so, and the value is a non empty string,
    it is sent to the model for paraphrasing.

    The results are validated before being written back. If the validation fails the original value stays unchanged.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in TARGET_FIELDS and isinstance(value, str) and value.strip():
                rewritten = rewrite_value(value)
                # Only overwrite if the model output passes validation, otherwise, the original value is preserved
                if is_valid_output(value, rewritten):
                    obj[key] = rewritten
                else:
                    logging.info(f"Model output is invalid, the original value is unchanged. Original text: {value}")
                    obj[key] = value
            else:
                process_json(value)

    elif isinstance(obj, list):
        for item in obj:
            process_json(item)

    logging.shutdown()


def is_valid_output(original: str, rewritten: str) -> bool:
    """
    Validates the generated paraphrase before overwriting the original JSON field.

    It is used to reduce hallucinated responses, extreme length changes and residual artifacts.

    It checks :
    - The response is non empty string
    - The output length must not be way shorter or longer than the original length to ensure that
      the model did not hallucinate, truncate or expand the content.
    - Residual artifacts
    """
    # Output must not be empty
    if not rewritten.strip():
        return False

    # Paraphrasing should produce the same amount of text as the original input
    ratio = len(rewritten) / len(original)
    if not (0.5 <= ratio <= 1.5):
        return False

    # Reject outputs with specific artifacts
    if any(artifact in rewritten for artifact in ["/think", "<think>", "It seems like your message"]):
        return False

    # If the only difference between the Input and the Output is <br><br> at the end
    if original == rewritten + "<br><br>":
        return False

    return True
