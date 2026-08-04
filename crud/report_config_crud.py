from models.report_config import ReportConfig


def get_report_config(db, family_norm_id: int):
    return db.query(ReportConfig).filter(
        ReportConfig.family_norm_id == family_norm_id
    ).first()


def get_or_create_report_config(db, family_norm_id: int):
    config = get_report_config(db, family_norm_id)
    if config:
        return config
    config = ReportConfig(
        family_norm_id=family_norm_id,
        list_abbreviation=[],
        maturity_levels=[],
        risk_levels=[]
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def update_report_config(db, family_norm_id: int, data: dict):
    config = get_or_create_report_config(db, family_norm_id)

    for field, value in data.items():
        if hasattr(config, field):
            setattr(config, field, value)

    db.commit()
    db.refresh(config)
    return config


def update_report_image(db, family_norm_id: int, field_name: str, image_base64: str):
    config = get_or_create_report_config(db, family_norm_id)
    if not hasattr(config, field_name):
        raise ValueError(f"Champ image invalide : {field_name}")
    setattr(config, field_name, image_base64)
    db.commit()
    db.refresh(config)
    return config