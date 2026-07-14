from crud.control_language_crud import get_control_language
from crud.finding_crud import get_finding_text
from crud.measure_crud import get_measures_by_response
from crud.questionResponse_crud import get_all_question_responses
from crud.responseFinding_crud import get_findings_by_response


def get_model_data(db):
    """
    Returns the data that will be fed to train the model.
    It contains control title, language, maturity level, non conformity, findings and measures
    """
    all_data = []

    question_responses = get_all_question_responses(db)

    for question_response in question_responses:
        data = {}
        response_id = question_response.response_id

        lang = question_response.audit.customer.language_id

        control_language = get_control_language(db, question_response.control_id, lang)

        data["control_title"] = control_language.title
        data["language"] = control_language.languages.language

        data["risk_level"] = question_response.risk_level
        data["non_conformity"] = question_response.non_conformity

        questions_responses = []

        findings = get_findings_by_response(db, response_id)
        measures = get_measures_by_response(db, response_id)

        max_elem = max(len(findings), len(measures))

        quest_resp = {}
        for i in range(max_elem):

            if len(findings) > i:
                quest_resp["finding"] = get_finding_text(db, findings[i].finding_id)
            quest_resp["finding"] = get_finding_text(db, findings[i - 1].finding_id)

            if len(measures) > i:
                quest_resp["measures"] = measures[i].measure_text
            quest_resp["measures"] = measures[i - 1].measure_text

            questions_responses.append(quest_resp)

        data["question_responses"] = questions_responses

        all_data.append(data)

    return all_data
