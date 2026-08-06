import json


def load_json(filename):
    with open(f"{filename}", "r", encoding="utf-8") as f:
        return json.load(f)


# Load all tables
norms = load_json("../../data/BSI_json/norm.json")
family_norms = load_json("../../data/BSI_json/family_norm.json")

categories = load_json("../../data/BSI_json/categories.json")
category_languages = load_json("../../data/BSI_json/category_languages.json")

chapters = load_json("../../data/BSI_json/chapters.json")
chapter_languages = load_json("../../data/BSI_json/chapter_languages.json")

controls = load_json("../../data/BSI_json/controls.json")
control_languages = load_json("../../data/BSI_json/control_languages.json")

control_tags = load_json("../../data/BSI_json/control_tag.json")
control_tag_languages = load_json("../../data/BSI_json/control_tag_language.json")

languages = load_json("../../data/TISAX/languages.json")


def get_language(language_id):
    for lang in languages:
        if lang["language_id"] == language_id:
            return lang["language"]

    return None


def get_norm_categories(norm_id):
    result = []

    for category in categories:

        if category["norm_id"] != norm_id:
            continue

        category_dict = {
            "category_id": category["category_id"],
            "id": category["id"],
            "category_language": []
        }

        for lang in category_languages:

            if lang["category_id"] == category["category_id"]:
                category_dict["category_language"].append({
                    "language_id": lang["language_id"],
                    "category_name": lang["category_name"],
                    "language": get_language(lang["language_id"])
                })

        result.append(category_dict)

    return result


def get_norm_chapters(norm_id):
    result = []

    for chapter in chapters:

        if chapter["norm_id"] != norm_id:
            continue

        chapter_dict = {
            "chapter_id": chapter["chapter_id"],
            "id": chapter["id"],
            "chapter_language": []
        }

        for lang in chapter_languages:

            if lang["chapter_id"] == chapter["chapter_id"]:
                chapter_dict["chapter_language"].append({
                    "title": lang["title"],
                    "objective": lang["objective"],
                    "language_id": lang["language_id"],
                    "language": get_language(lang["language_id"])
                })

        result.append(chapter_dict)

    return result


def get_norm_controls(norm_id):
    result = []

    for control in controls:

        if control["norm_id"] != norm_id:
            continue

        control_dict = {
            "control_id": control["control_id"],
            "id": control["id"],
            "norm_id": control["norm_id"],
            "category_id": control["category_id"],
            "chapter_id": control["chapter_id"],
            "control_tag_id": control["control_tag_id"],
            "control_language": [],
            "control_tag_languages": []
        }

        for lang in control_languages:

            if lang["control_id"] == control["control_id"]:
                control_dict["control_language"].append({
                    "title": lang["title"],
                    "description": lang["description"],
                    "language_id": lang["language_id"],
                    "language": get_language(lang["language_id"])
                })

        for tag_lang in control_tag_languages:

            if tag_lang["control_tag_id"] == control["control_tag_id"]:
                control_dict["control_tag_languages"].append({
                    "title": tag_lang["title"],
                    "language_id": tag_lang["language_id"],
                    "language": get_language(tag_lang["language_id"])
                })

        result.append(control_dict)

    return result


def get_family_norm(id):
    return next(
        (f for f in family_norms if f["family_norm_id"] == id),
        None
    )


def get_all_norm_info(norm_id):
    norm = next(
        n for n in norms
        if n["norm_id"] == norm_id
    )

    family = get_family_norm(norm["family_norm_id"])

    return {
        "norm_id": norm["norm_id"],
        "title": norm["title"],
        "description": norm["description"],
        "abbreviation": norm["abbreviation"],
        "publish_year": norm["publish_year"],

        "family_norm": {
            "family_norm_id": family["family_norm_id"],
            "name": family["name"]
        } if family else None,

        "categories": get_norm_categories(norm_id),
        "chapters": get_norm_chapters(norm_id),
        "controls": get_norm_controls(norm_id)
    }


# Generate output

norm_json = get_all_norm_info(5)

with open("output/exported_norm_BSI.json", "w", encoding="utf-8") as f:
    json.dump(norm_json, f, indent=4, ensure_ascii=False)

print("JSON generated successfully")
