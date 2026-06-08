from models.norm import Norm

def create_norm(db, data):
    norm = Norm(**data)
    db.add(norm)
    db.commit()
    db.refresh(norm)
    return norm

def get_norm(db, norm_id):
    return db.query(Norm).filter(Norm.norm_id == norm_id).first()

def update_norm(db, norm_id, data):
    norm = db.query(Norm).filter(Norm.norm_id == norm_id).first()

    if not norm:
        return None

    for key, value in data.items():
        setattr(norm, key, value)

    db.commit()
    db.refresh(norm)
    return norm

def delete_norm(db, norm_id):
    norm = db.query(Norm).filter(Norm.norm_id == norm_id).first()

    if norm:
        db.delete(norm)
        db.commit()

    return norm