from models.language import Language


def create_language(db, data):
    language = Language(**data)

    db.add(language)
    db.commit()
    db.refresh(language)

    return language


def create_many_languages(db, data: list[dict]):
    many_languages = [Language(**data) for data in data]

    db.add_all(many_languages)
    db.commit()

    for language in many_languages:
        db.refresh(language)

    return many_languages


def get_language(db, language_id):
    return db.query(Language).filter(Language.language_id == language_id).first()


def update_language(db, language_id, data):
    language = get_language(db, language_id)

    if not language:
        return None

    for key, value in data.items():
        setattr(language, key, value)

    db.commit()
    db.refresh(language)

    return language


def delete_language(db, language_id):
    language = get_language(db, language_id)

    if language:
        db.delete(language)
        db.commit()

    return language
