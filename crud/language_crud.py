from models.language import Language

def create_language(db, data):
    language = Language(**data)
    db.add(language)
    db.commit()
    db.refresh(language)
    return language

def get_language(db, language_id):
    return db.query(Language).filter(Language.language_id == language_id).first()

def update_language(db, language_id, data):
    language = db.query(Language).filter(Language.language_id == language_id).first()

    if not language:
        return None

    for key, value in data.items():
        setattr(language, key, value)

    db.commit()
    db.refresh(language)
    return language

def delete_language(db, language_id):
    language = db.query(Language).filter(Language.language_id == language_id).first()

    if language:
        db.delete(language)
        db.commit()

    return language