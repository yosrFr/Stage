from models.chapter_language import ChapterLanguage


def create_chapter_language(db, data):
    chapter_language = ChapterLanguage(**data)

    db.add(chapter_language)
    db.commit()
    db.refresh(chapter_language)

    return chapter_language


def create_many_chapter_languages(db, data: list[dict]):
    many_chapter_languages = [ChapterLanguage(**data) for data in data]

    db.add_all(many_chapter_languages)
    db.commit()

    for chapter_language in many_chapter_languages:
        db.refresh(chapter_language)

    return many_chapter_languages


def get_chapter_language(db, chapter_id, language_id):
    return (db.query(ChapterLanguage)
            .filter(ChapterLanguage.chapter_id == chapter_id and
                    ChapterLanguage.language_id == language_id)
            .first())


def update_chapter_language(db, chapter_id, language_id, data):
    chapter_language = get_chapter_language(db, chapter_id, language_id)

    if not chapter_language:
        return None

    for key, value in data.items():
        setattr(chapter_language, key, value)

    db.commit()
    db.refresh(chapter_language)

    return chapter_language


def delete_chapter_language(db, chapter_id, language_id):
    chapter_language = get_chapter_language(db, chapter_id, language_id)

    if chapter_language:
        db.delete(chapter_language)
        db.commit()

    return chapter_language
