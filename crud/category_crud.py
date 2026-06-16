from sqlalchemy.orm import joinedload

from models import CategoryLanguage
from models.category import Category


def create_category(db, data):
    category = Category(**data)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def create_many_categories(db, data: list[dict]):
    many_categories = [Category(**data) for data in data]

    db.add_all(many_categories)
    db.commit()

    for category in many_categories:
        db.refresh(category)

    return many_categories


def get_category(db, category_id):
    return db.query(Category).filter(Category.category_id == category_id).first()


def get_categories_by_norm_id(db, norm_id):
    return (db.query(Category)
            .options(joinedload(Category.category_languages)
                     .joinedload(CategoryLanguage.languages)
                     )
            .filter(Category.norm_id == norm_id)
            .all())


def update_category(db, category_id, data):
    category = get_category(db, category_id)

    if not category:
        return None

    for key, value in data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(db, category_id):
    category = get_category(db, category_id)

    if category:
        db.delete(category)
        db.commit()

    return category
