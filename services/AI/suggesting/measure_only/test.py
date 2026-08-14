import json

from services.AI.suggesting.measure_only.measure_suggestion_engine import suggest_measures

with open("../finding_only/findings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output_measures = []

for item in data:
    filtered_data = {}

    filtered_data["norm_family"] = item["norm_family"]
    filtered_data["control_title"] = item["control_title"]
    filtered_data["control_description"] = item["control_description"]
    filtered_data["maturity_level"] = item["maturity_level"]
    filtered_data["risk_level"] = item["risk_level"]
    filtered_data["current_state"] = item["current_state"]

    for finding in item["findings"]:
        filtered_data["finding"] = finding

        result = suggest_measures(filtered_data)
        output_measures.append({**filtered_data, "measure": result})

with open("measures.json", "w", encoding="utf-8") as f:
    json.dump(output_measures, f, ensure_ascii=False, indent=2)
