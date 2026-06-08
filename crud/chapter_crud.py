from models.chapter import Chapter

def create_chapter(db, data):
    chapter = Chapter(**data)
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter

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