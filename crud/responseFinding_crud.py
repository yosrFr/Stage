from models import ResponseFinding


def create_response_findings(db, data):
    response_findings = ResponseFinding(**data)

    db.add(response_findings)
    db.commit()
    db.refresh(response_findings)

    return response_findings


def create_many_response_findings(db, data: list[dict]):
    many_response_findings = [ResponseFinding(**data) for data in data]

    db.add_all(many_response_findings)
    db.commit()

    for response_findings in many_response_findings:
        db.refresh(response_findings)

    return many_response_findings


def get_response_findings(db, response_id):
    return db.query(ResponseFinding).filter(ResponseFinding.response_id == response_id).first()


def update_response_findings(db, response_id, data):
    response_findings = get_response_findings(db, response_id)

    if not response_findings:
        return None

    for key, value in data.items():
        setattr(response_findings, key, value)

    db.commit()
    db.refresh(response_findings)

    return response_findings


def delete_response_findings(db, response_id):
    response_findings = get_response_findings(db, response_id)

    if response_findings:
        db.delete(response_findings)
        db.commit()

    return response_findings
