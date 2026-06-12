from services.rewrite_engine import rewrite_value

TARGET_FIELDS = {"description", "objective"}


def process_json(obj) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in TARGET_FIELDS and isinstance(value, str) and value.strip():
                rewritten = rewrite_value(value)
                obj[key] = rewritten if is_valid_output(value, rewritten) else value
            else:
                process_json(value)

    elif isinstance(obj, list):
        for item in obj:
            process_json(item)


def is_valid_output(original: str, rewritten: str) -> bool:
    if not rewritten.strip():
        return False
    ratio = len(rewritten) / len(original)
    if not (0.5 <= ratio <= 1.5):
        return False
    if any(artifact in rewritten for artifact in ["/think", "<think>", "It seems like your message"]):
        return False
    return True
