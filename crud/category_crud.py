from models.category import Category

def create_category(db, data):
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db, category_id):
    return db.query(Category).filter(Category.category_id == category_id).first()

def update_category(db, category_id, data):
    category = db.query(Category).filter(Category.category_id == category_id).first()

    if not category:
        return None

    for key, value in data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category

def delete_category(db, category_id):
    category = db.query(Category).filter(Category.category_id == category_id).first()

    if category:
        db.delete(category)
        db.commit()

    return category