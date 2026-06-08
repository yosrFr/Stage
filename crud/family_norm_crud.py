from models.family_norm import FamilyNorm

def create_family_norm(db, data):
    family_norm = FamilyNorm(**data)
    db.add(family_norm)
    db.commit()
    db.refresh(family_norm)
    return family_norm

def get_family_norm(db, family_norm_id):
    return db.query(FamilyNorm).filter(FamilyNorm.family_norm_id == family_norm_id).first()

def update_family_norm(db, family_norm_id, data):
    family_norm = db.query(FamilyNorm).filter(FamilyNorm.family_norm_id == family_norm_id).first()

    if not family_norm:
        return None

    for key, value in data.items():
        setattr(family_norm, key, value)

    db.commit()
    db.refresh(family_norm)
    return family_norm

def delete_family_norm(db, family_norm_id):
    family_norm = db.query(FamilyNorm).filter(FamilyNorm.family_norm_id == family_norm_id).first()

    if family_norm:
        db.delete(family_norm)
        db.commit()

    return family_norm