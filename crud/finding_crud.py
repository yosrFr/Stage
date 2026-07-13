from models.finding import Finding


def create_finding(db, data):
    finding = Finding(**data)

    db.add(finding)
    db.commit()
    db.refresh(finding)

    return finding


def create_many_findings(db, data: list[dict]):
    many_findings = [Finding(**data) for data in data]

    db.add_all(many_findings)
    db.commit()

    for finding in many_findings:
        db.refresh(finding)

    return many_findings


def get_finding(db, finding_id):
    return db.query(Finding).filter(Finding.finding_id == finding_id).first()


def update_finding(db, finding_id, data):
    finding = get_finding(db, finding_id)

    if not finding:
        return None

    for key, value in data.items():
        setattr(finding, key, value)

    db.commit()
    db.refresh(finding)

    return finding


def delete_finding(db, finding_id):
    finding = get_finding(db, finding_id)

    if finding:
        db.delete(finding)
        db.commit()

    return finding
