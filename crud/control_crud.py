from sqlalchemy.orm import joinedload

from models import ControlTags, ControlLanguage, ControlTagLanguage
from models.control import Control


def create_control(db, data):
    control = Control(**data)

    db.add(control)
    db.commit()
    db.refresh(control)

    return control


def create_many_controls(db, data: list[dict]):
    many_controls = [Control(**data) for data in data]

    db.add_all(many_controls)
    db.commit()

    for control in many_controls:
        db.refresh(control)

    return many_controls


def get_control(db, control_id):
    return db.query(Control).filter(Control.control_id == control_id).first()


def get_controls_by_norm_id(db, norm_id):
    return (db.query(Control)
            .options(joinedload(Control.control_languages)
                     .joinedload(ControlLanguage.languages) and
                     joinedload(Control.control_tags)
                     .joinedload(ControlTags.control_tag_languages)
                     .joinedload(ControlTagLanguage.languages))
            .filter(Control.norm_id == norm_id)
            .all())


def update_control(db, control_id, data):
    control = get_control(db, control_id)

    if not control:
        return None

    for key, value in data.items():
        setattr(control, key, value)

    db.commit()
    db.refresh(control)

    return control


def delete_control(db, control_id):
    control = get_control(db, control_id)

    if control:
        db.delete(control)
        db.commit()

    return control
