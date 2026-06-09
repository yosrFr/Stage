from models.chapter import Chapter


def create_chapter(db, data):
    chapter = Chapter(**data)
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


def create_many_chapters(db, data: list[dict]):
    many_chapters = [Chapter(**data) for data in data]

    db.add_all(many_chapters)
    db.commit()

    for chapter in many_chapters:
        db.refresh(chapter)

    return many_chapters


def get_chapter(db, chapter_id):
    return db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()


def update_chapter(db, chapter_id, data):
    chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()

    if not chapter:
        return None

    for key, value in data.items():
        setattr(chapter, key, value)

    db.commit()
    db.refresh(chapter)
    return chapter


def delete_chapter(db, chapter_id):
    chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()

    if chapter:
        db.delete(chapter)
        db.commit()

    return chapter
