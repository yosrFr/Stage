from models.control_language import ControlLanguage


def create_control_language(db, data):
    control_language = ControlLanguage(**data)

    db.add(control_language)
    db.commit()
    db.refresh(control_language)

    return control_language


def create_many_control_languages(db, data: list[dict]):
    many_control_languages = [ControlLanguage(**data) for data in data]

    db.add_all(many_control_languages)
    db.commit()

    for control_language in many_control_languages:
        db.refresh(control_language)

    return many_control_languages


def get_control_language(db, control_id, language_id):
    return (db.query(ControlLanguage)
            .filter(ControlLanguage.control_id == control_id and
                    ControlLanguage.language_id == language_id)
            .first())


def update_control_language(db, control_id, language_id, data):
    control_language = get_control_language(db, control_id, language_id)

    if not control_language:
        return None

    for key, value in data.items():
        setattr(control_language, key, value)

    db.commit()
    db.refresh(control_language)

    return control_language


def delete_control_language(db, control_id, language_id):
    control_language = get_control_language(db, control_id, language_id)

    if control_language:
        db.delete(control_language)
        db.commit()

    return control_language
