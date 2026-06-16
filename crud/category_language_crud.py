from models.category_language import CategoryLanguage


def create_category_language(db, data):
    category_language = CategoryLanguage(**data)

    db.add(category_language)
    db.commit()
    db.refresh(category_language)

    return category_language


def create_many_category_languages(db, data: list[dict]):
    many_category_languages = [CategoryLanguage(**data) for data in data]

    db.add_all(many_category_languages)
    db.commit()

    for category_language in many_category_languages:
        db.refresh(category_language)

    return many_category_languages


def get_category_language(db, category_id, language_id):
    return (db.query(CategoryLanguage)
            .filter(CategoryLanguage.category_id == category_id and
                    CategoryLanguage.language_id == language_id)
            .first())


def update_category_language(db, category_id, language_id, data):
    category_language = get_category_language(db, category_id, language_id)

    if not category_language:
        return None

    for key, value in data.items():
        setattr(category_language, key, value)

    db.commit()
    db.refresh(category_language)

    return category_language


def delete_category_language(db, category_id, language_id):
    category_language = get_category_language(db, category_id, language_id)

    if category_language:
        db.delete(category_language)
        db.commit()

    return category_language
