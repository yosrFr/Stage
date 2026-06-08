from models.category_language import CategoryLanguage

def create_category_language(db, data):
    categoryLanguage = CategoryLanguage(**data)
    db.add(categoryLanguage)
    db.commit()
    db.refresh(categoryLanguage)
    return categoryLanguage

def get_category_language(db, category_id, language_id):
    return (db.query(CategoryLanguage)
                        .filter(CategoryLanguage.category_id == category_id and
                                CategoryLanguage.language_id == language_id)
                        .first())

def update_category_language(db, category_id, language_id, data):
    categoryLanguage = (db.query(CategoryLanguage)
                        .filter(CategoryLanguage.category_id == category_id and
                                CategoryLanguage.language_id == language_id)
                        .first())

    if not categoryLanguage:
        return None

    for key, value in data.items():
        setattr(categoryLanguage, key, value)

    db.commit()
    db.refresh(categoryLanguage)
    return categoryLanguage

def delete_category_language(db, category_id, language_id, data):
    categoryLanguage = (db.query(CategoryLanguage)
                        .filter(CategoryLanguage.category_id == category_id and
                                CategoryLanguage.language_id == language_id)
                        .first())

    if categoryLanguage:
        db.delete(categoryLanguage)
        db.commit()

    return categoryLanguage