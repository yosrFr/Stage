from models.control_tags import ControlTags

def create_control_tag(db, data):
    controlTag = ControlTags(**data)
    db.add(controlTag)
    db.commit()
    db.refresh(controlTag)
    return controlTag

def get_control_tag(db, control_tag_id):
    return db.query(ControlTags).filter(ControlTags.control_tag_id == control_tag_id).first()


def delete_control_tag(db, control_tag_id):
    controlTag = db.query(ControlTags).filter(ControlTags.control_tag_id == control_tag_id).first()

    if controlTag:
        db.delete(controlTag)
        db.commit()

    return controlTag