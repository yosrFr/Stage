from models.control_language import ControlLanguage

def create_control_language(db, data):
    controlLanguage = ControlLanguage(**data)
    db.add(controlLanguage)
    db.commit()
    db.refresh(controlLanguage)
    return controlLanguage

def get_control_language(db, control_id, language_id):
    return (db.query(ControlLanguage)
                        .filter(ControlLanguage.control_id == control_id and
                                ControlLanguage.language_id == language_id)
                        .first())

def update_control_language(db, control_id, language_id, data):
    controlLanguage = (db.query(ControlLanguage)
                        .filter(ControlLanguage.control_id == control_id and
                                ControlLanguage.language_id == language_id)
                        .first())

    if not controlLanguage:
        return None

    for key, value in data.items():
        setattr(controlLanguage, key, value)

    db.commit()
    db.refresh(controlLanguage)
    return controlLanguage

def delete_control_language(db, control_id, language_id, data):
    controlLanguage = (db.query(ControlLanguage)
                        .filter(ControlLanguage.control_id == control_id and
                                ControlLanguage.language_id == language_id)
                        .first())

    if controlLanguage:
        db.delete(controlLanguage)
        db.commit()

    return controlLanguage