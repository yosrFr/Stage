from sqlalchemy.orm import joinedload

from models.norm import Norm


def create_norm(db, data):
    norm = Norm(**data)

    db.add(norm)
    db.commit()
    db.refresh(norm)

    return norm


def create_many_norms(db, data: list[dict]):
    many_norms = [Norm(**data) for data in data]

    db.add_all(many_norms)
    db.commit()

    for norm in many_norms:
        db.refresh(norm)

    return many_norms


def get_norm(db, norm_id):
    return db.query(Norm).filter(Norm.norm_id == norm_id).first()


def get_norm_with_options(db, norm_id):
    return (db.query(Norm)
            .options(joinedload(Norm.family_norm))
            .filter(Norm.norm_id == norm_id)
            .first())


def update_norm(db, norm_id, data):
    norm = get_norm_with_options(db, norm_id)

    if not norm:
        return None

    for key, value in data.items():
        setattr(norm, key, value)

    db.commit()
    db.refresh(norm)

    return norm


def delete_norm(db, norm_id):
    norm = get_norm_with_options(db, norm_id)

    if norm:
        db.delete(norm)
        db.commit()

    return norm
