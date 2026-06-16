from models.control_tag_language import ControlTagLanguage


def create_control_tag_language(db, data):
    control_tag_language = ControlTagLanguage(**data)

    db.add(control_tag_language)
    db.commit()
    db.refresh(control_tag_language)

    return control_tag_language


def create_many_control_tag_languages(db, data: list[dict]):
    many_control_tag_languages = [ControlTagLanguage(**data) for data in data]

    db.add_all(many_control_tag_languages)
    db.commit()

    for control_tag_language in many_control_tag_languages:
        db.refresh(control_tag_language)

    return many_control_tag_languages


def get_control_tag_language(db, control_tag_id, language_id):
    return (db.query(ControlTagLanguage)
            .filter(ControlTagLanguage.control_tag_id == control_tag_id and
                    ControlTagLanguage.language_id == language_id)
            .first())


def update_control_tag_language(db, control_tag_id, language_id, data):
    control_tag_language = get_control_tag_language(db, control_tag_id, language_id)

    if not control_tag_language:
        return None

    for key, value in data.items():
        setattr(control_tag_language, key, value)

    db.commit()
    db.refresh(control_tag_language)

    return control_tag_language


def delete_control_tag_language(db, control_tag_id, language_id):
    control_tag_language = get_control_tag_language(db, control_tag_id, language_id)

    if control_tag_language:
        db.delete(control_tag_language)
        db.commit()

    return control_tag_language
