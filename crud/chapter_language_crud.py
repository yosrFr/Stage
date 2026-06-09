from models.chapter_language import ChapterLanguage


def create_chapter_language(db, data):
    chapterLanguage = ChapterLanguage(**data)
    db.add(chapterLanguage)
    db.commit()
    db.refresh(chapterLanguage)
    return chapterLanguage


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
    chapterLanguage = (db.query(ChapterLanguage)
                       .filter(ChapterLanguage.chapter_id == chapter_id and
                               ChapterLanguage.language_id == language_id)
                       .first())

    if not chapterLanguage:
        return None

    for key, value in data.items():
        setattr(chapterLanguage, key, value)

    db.commit()
    db.refresh(chapterLanguage)
    return chapterLanguage


def delete_chapter_language(db, chapter_id, language_id, data):
    chapterLanguage = (db.query(ChapterLanguage)
                       .filter(ChapterLanguage.chapter_id == chapter_id and
                               ChapterLanguage.language_id == language_id)
                       .first())

    if chapterLanguage:
        db.delete(chapterLanguage)
        db.commit()

    return chapterLanguage
