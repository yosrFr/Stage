import json

from database.session import SessionLocal
from models import *


def export_all():
    db = SessionLocal()

    data = {}

    # family_norm
    data["family_norm"] = [
        {i.name: getattr(e, i.name) for i in FamilyNorm.__table__.columns}
        for e in db.query(FamilyNorm).all()
    ]

    # norm
    data["norm"] = [
        {i.name: getattr(e, i.name) for i in Norm.__table__.columns}
        for e in db.query(Norm).all()
    ]

    # chapter
    data["chapter"] = [
        {i.name: getattr(e, i.name) for i in Chapter.__table__.columns}
        for e in db.query(Chapter).all()
    ]

    # control_tags
    data["control_tags"] = [
        {i.name: getattr(e, i.name) for i in ControlTags.__table__.columns}
        for e in db.query(ControlTags).all()
    ]

    # category
    data["category"] = [
        {i.name: getattr(e, i.name) for i in Category.__table__.columns}
        for e in db.query(Category).all()
    ]

    # control
    data["control"] = [
        {i.name: getattr(e, i.name) for i in Control.__table__.columns}
        for e in db.query(Control).all()
    ]

    # language
    data["language"] = [
        {i.name: getattr(e, i.name) for i in Language.__table__.columns}
        for e in db.query(Language).all()
    ]

    # control_tag_language
    data["control_tag_language"] = [
        {i.name: getattr(e, i.name) for i in ControlTagLanguage.__table__.columns}
        for e in db.query(ControlTagLanguage).all()
    ]

    # chapter_language
    data["chapter_language"] = [
        {i.name: getattr(e, i.name) for i in ChapterLanguage.__table__.columns}
        for e in db.query(ChapterLanguage).all()
    ]

    # category_language
    data["category_language"] = [
        {i.name: getattr(e, i.name) for i in CategoryLanguage.__table__.columns}
        for e in db.query(CategoryLanguage).all()
    ]

    # control_language
    data["control_language"] = [
        {i.name: getattr(e, i.name) for i in ControlLanguage.__table__.columns}
        for e in db.query(ControlLanguage).all()
    ]

    db.close()

    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    export_all()
