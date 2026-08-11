import json

from services.AI.suggesting.finding_only.finding_suggestion_engine import suggest_findings

with open("finding_sugg_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

outputs_findings = []

for item in data:
    result = suggest_findings(item)
    outputs_findings.append({**item, "findings": result})

with open("findings.json", "w", encoding="utf-8") as f:
    json.dump(outputs_findings, f, ensure_ascii=False, indent=2)
