from models.control_tags import ControlTags


def create_control_tag(db, data):
    control_tag = ControlTags(**data)

    db.add(control_tag)
    db.commit()
    db.refresh(control_tag)

    return control_tag


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
    control_tag = get_control_tag(db, control_tag_id)

    if control_tag:
        db.delete(control_tag)
        db.commit()

    return control_tag
