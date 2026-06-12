from services.json_processor import process_json


def rewrite_json(data: dict | list) -> dict | list:
    process_json(data)
    return data
