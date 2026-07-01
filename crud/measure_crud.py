from models.measure import Measure


def create_measure(db, data):
    measure = Measure(**data)

    db.add(measure)
    db.commit()
    db.refresh(measure)

    return measure


def create_many_measures(db, data: list[dict]):
    many_measures = [Measure(**data) for data in data]

    db.add_all(many_measures)
    db.commit()

    for measure in many_measures:
        db.refresh(measure)

    return many_measures


def get_measure(db, measure_id):
    return db.query(Measure).filter(Measure.measure_id == measure_id).first()


def update_measure(db, measure_id, data):
    measure = get_measure(db, measure_id)

    if not measure:
        return None

    for key, value in data.items():
        setattr(measure, key, value)

    db.commit()
    db.refresh(measure)

    return measure


def delete_measure(db, measure_id):
    measure = get_measure(db, measure_id)

    if measure:
        db.delete(measure)
        db.commit()

    return measure
