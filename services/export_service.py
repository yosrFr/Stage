from crud.category_crud import get_categories_by_norm_id
from crud.chapter_crud import get_chapters_by_norm_id
from crud.control_crud import get_controls_by_norm_id
from crud.norm_crud import get_norm_with_options


def get_norm_chapters(db, norm_id):
    chapters = get_chapters_by_norm_id(db, norm_id)

    result_chapters = []

    for chapter in chapters:
        chapter_dict = {
            "chapter_id": chapter.chapter_id,
            "id": chapter.id,
            "chapter_language": []
        }

        for c in chapter.chapter_languages:
            chapter_dict["chapter_language"].append({
                "title": c.title,
                "objective": c.objective,
                "language_id": c.language_id,
                "language": c.languages.language,
            })

        result_chapters.append(chapter_dict)

    return result_chapters


def get_norm_controls(db, norm_id):
    controls = get_controls_by_norm_id(db, norm_id)

    result_controls = []

    for control in controls:
        control_dict = {
            "control_id": control.control_id,
            "id": control.id,
            "control_language": [],
            "control_tags": []
        }

        for c in control.control_languages:
            control_dict["control_language"].append({
                "title": c.title,
                "description": c.description,
                "language_id": c.language_id,
                "language": c.languages.language,
            })

        result_controls.append(control_dict)

        if control.control_tags:
            for c in control.control_tags:
                control_dict["control_tags"].append({
                    "control_tag_id": c.control_tag_id,
                    "control_tag_language": {
                        "title": c.control_tags.title,
                        "language_id": c.control_tags.language_id,
                        "language": c.control_tags.language.language
                    }
                })

    return result_controls


def get_norm_categories(db, norm_id):
    categories = get_categories_by_norm_id(db, norm_id)

    result_category = []

    for category in categories:

        category_dict = {
            "category_id": category.category_id,
            "id": category.id,
            "category_language": []
        }

        for c in category.category_languages:
            category_dict["category_language"].append({
                "language_id": c.language_id,
                "category_name": c.category_name,
                "language": c.languages.language,
            })

        result_category.append(category_dict)

    return result_category


def get_all_norm_info(db, norm_id):
    norm = get_norm_with_options(db, norm_id)

    return {
        "norm_id": norm.norm_id,
        "title": norm.title,
        "description": norm.description,
        "abbreviation": norm.abbreviation,
        "publish_year": norm.publish_year,
        "family_norm": {
            "family_norm_id": norm.family_norm.family_norm_id,
            "name": norm.family_norm.name,
        },
        "categories": get_norm_categories(db, norm.norm_id),
        "chapters": get_norm_chapters(db, norm.norm_id),
        "controls": get_norm_controls(db, norm.norm_id),
    }
