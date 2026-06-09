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


def update_control(db, control_id, data):
    control = db.query(Control).filter(Control.control_id == control_id).first()

    if not control:
        return None

    for key, value in data.items():
        setattr(control, key, value)

    db.commit()
    db.refresh(control)
    return control


def delete_control(db, control_id):
    control = db.query(Control).filter(Control.control_id == control_id).first()

    if control:
        db.delete(control)
        db.commit()

    return control
