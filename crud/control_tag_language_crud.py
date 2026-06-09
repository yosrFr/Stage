from models.control_tag_language import ControlTagLanguage


def create_control_tag_language(db, data):
    controlTagLanguage = ControlTagLanguage(**data)
    db.add(controlTagLanguage)
    db.commit()
    db.refresh(controlTagLanguage)
    return controlTagLanguage


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
    controlTagLanguage = (db.query(ControlTagLanguage)
                          .filter(ControlTagLanguage.control_tag_id == control_tag_id and
                                  ControlTagLanguage.language_id == language_id)
                          .first())

    if not controlTagLanguage:
        return None

    for key, value in data.items():
        setattr(controlTagLanguage, key, value)

    db.commit()
    db.refresh(controlTagLanguage)
    return controlTagLanguage


def delete_control_tag_language(db, control_tag_id, language_id, data):
    controlTagLanguage = (db.query(ControlTagLanguage)
                          .filter(ControlTagLanguage.control_tag_id == control_tag_id and
                                  ControlTagLanguage.language_id == language_id)
                          .first())

    if controlTagLanguage:
        db.delete(controlTagLanguage)
        db.commit()

    return controlTagLanguage
