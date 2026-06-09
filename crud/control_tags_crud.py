from models.control_tags import ControlTags


def create_control_tag(db, data):
    controlTag = ControlTags(**data)
    db.add(controlTag)
    db.commit()
    db.refresh(controlTag)
    return controlTag


def create_many_control_tags(db, data: list[dict]):
    many_control_tags = [ControlTags(**data) for data in data]

    db.add_all(many_control_tags)
    db.commit()

    for control_tag in many_control_tags:
        db.refresh(control_tag)

    return many_control_tags


def get_control_tag(db, control_tag_id):
    return db.query(ControlTags).filter(ControlTags.control_tag_id == control_tag_id).first()


def delete_control_tag(db, control_tag_id):
    controlTag = db.query(ControlTags).filter(ControlTags.control_tag_id == control_tag_id).first()

    if controlTag:
        db.delete(controlTag)
        db.commit()

    return controlTag
