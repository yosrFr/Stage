import json

with open("output/exported_norm_BSI.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ctrl_index = 0
while ctrl_index < len(data["controls"]):
    ctrl = data["controls"][ctrl_index]
    for ctrl_lang in ctrl["control_language"]:
        if "Diese Anforderung ist entfallen" in ctrl_lang["description"]:
            data["controls"].remove(ctrl)
            ctrl_index -= 1
        ctrl_index += 1

with open("output/exported_norm_BSI_filtered.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
