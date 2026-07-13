from models import QuestionResponse


def create_question_responses(db, data):
    question_responses = QuestionResponse(**data)

    db.add(question_responses)
    db.commit()
    db.refresh(question_responses)

    return question_responses


def create_many_question_responses(db, data: list[dict]):
    many_question_responses = [QuestionResponse(**data) for data in data]

    db.add_all(many_question_responses)
    db.commit()

    for question_responses in many_question_responses:
        db.refresh(question_responses)

    return many_question_responses


def get_question_responses(db, response_id):
    return db.query(QuestionResponse).filter(QuestionResponse.response_id == response_id).first()


def update_question_responses(db, response_id, data):
    question_responses = get_question_responses(db, response_id)

    if not question_responses:
        return None

    for key, value in data.items():
        setattr(question_responses, key, value)

    db.commit()
    db.refresh(question_responses)

    return question_responses


def delete_question_responses(db, response_id):
    question_responses = get_question_responses(db, response_id)

    if question_responses:
        db.delete(question_responses)
        db.commit()

    return question_responses
