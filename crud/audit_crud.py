from sqlalchemy.orm import joinedload

from models.audit import Audit 


def create_many_audits(db, data: list[dict]):
    many_audits = [Audit(**data) for data in data]
    try:
        db.add_all(many_audits)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    for audit in many_audits:
        db.refresh(audit)

    return many_audits