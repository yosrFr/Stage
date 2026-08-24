import json

INPUT_JSON_PATH = "../../../test_input_files/training_data.json"

EXPECTED_TOP_LEVEL_FIELDS = [
    "norm_title",
    "control_id",
    "control_title",
    "control_description",
    "language",
    "risk_level",
    "non_conformity",
    "current_state",
    "question_responses",
]


def type_name(value) -> str:
    return type(value).__name__


def run(json_path: str) -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    n = len(raw_data)
    print(f"Number of records: {n}\n")

    if n == 0:
        print("File is an empty list.")
        return

    # Per field stats across all records
    field_presence = {f: 0 for f in EXPECTED_TOP_LEVEL_FIELDS}
    field_types = {f: set() for f in EXPECTED_TOP_LEVEL_FIELDS}
    field_null_count = {f: 0 for f in EXPECTED_TOP_LEVEL_FIELDS}
    unexpected_keys = set()

    qr_list_count = 0
    qr_not_list_count = 0
    qr_item_missing_finding_key = 0
    qr_item_missing_measures_key = 0
    qr_finding_null_count = 0
    qr_measures_null_count = 0
    qr_finding_types = set()
    qr_measures_types = set()

    for record in raw_data:

        record_keys = set(record.keys())
        unexpected_keys |= (record_keys - set(EXPECTED_TOP_LEVEL_FIELDS))

        for field in EXPECTED_TOP_LEVEL_FIELDS:
            if field in record:
                field_presence[field] += 1
                value = record[field]
                field_types[field].add(type_name(value))
                if value is None:
                    field_null_count[field] += 1

        qr = record.get("question_responses", None)
        if qr is None:
            continue
        if not isinstance(qr, list):
            qr_not_list_count += 1
            continue
        qr_list_count += 1
        for item in qr:
            if not isinstance(item, dict):
                continue
            if "finding" not in item:
                qr_item_missing_finding_key += 1
            else:
                qr_finding_types.add(type_name(item["finding"]))
                if item["finding"] is None:
                    qr_finding_null_count += 1
            if "measures" not in item:
                qr_item_missing_measures_key += 1
            else:
                qr_measures_types.add(type_name(item["measures"]))
                if item["measures"] is None:
                    qr_measures_null_count += 1

    for field in EXPECTED_TOP_LEVEL_FIELDS:
        present = field_presence[field]
        missing = n - present
        nulls = field_null_count[field]
        types = sorted(field_types[field]) or ["field never present"]
        print(
            f"- {field}: present in {present}/{n} records (missing key in {missing}), null in {nulls}, observed type(s)={types}")

    if unexpected_keys:
        print(f"\nUnexpected  keys found in the data (not in the model): {sorted(unexpected_keys)}\n")

    print(f"- records where question_responses is a proper list: {qr_list_count}/{n}")
    print(f"- records where question_responses exists but is NOT a list: {qr_not_list_count}")
    print(f"- question_response items missing the 'finding' key entirely: {qr_item_missing_finding_key}")
    print(f"- question_response items missing the 'measures' key entirely: {qr_item_missing_measures_key}")
    print(f"- 'finding' observed type(s) across all items: {sorted(qr_finding_types) or ['<none found>']}")
    print(f"- 'measures' observed type(s) across all items: {sorted(qr_measures_types) or ['<none found>']}")
    print(f"- 'finding' null count: {qr_finding_null_count}")
    print(f"- 'measures' null count: {qr_measures_null_count}")

    for field in ["norm_title", "control_id", "control_title", "control_description", "non_conformity"]:
        types = field_types[field]
        if types and types != {"str"}:
            print(f"- {field} has non-string type(s) present: {sorted(types)} -- model expects str.")
    for field in ["language", "risk_level"]:
        types = field_types[field]
        if types and types - {"int"}:
            print(f"- {field} has non-int type(s) present: {sorted(types)} -- model expects int.")
    if field_presence.get("current_state", 0) < n:
        print(
            f"- current_state key is MISSING entirely in {n - field_presence['current_state']} record(s) (not just null).")


if __name__ == "__main__":
    run(INPUT_JSON_PATH)
