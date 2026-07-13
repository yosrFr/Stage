from sqlalchemy.orm import joinedload

from models.user import User


def create_many_users(db, data: list[dict]):
    many_users = [User(**data) for data in data]
    try:
        db.add_all(many_users)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    for user in many_users:
        db.refresh(user)

    return many_users