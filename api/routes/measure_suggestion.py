from fastapi import APIRouter, HTTPException

from schema.measure_sugg_schema import MeasureSuggestionRequest
from services.AI.suggesting.prompt_engineered.measure_only.measure_suggestion_engine import suggest_measures

router = APIRouter(prefix="/suggestion", tags=["prompt_engineered"])


@router.post(
    "/pe_measures",
    summary="Suggest a measure for a finding",
    description="""
    Give the AI model a finding and its control context, it returns a suggested measure
    """
)
def measure_suggestion(request: MeasureSuggestionRequest):
    if not request.findings:
        return {"measures": []}

    shared_context = request.model_dump(exclude={"findings"})

    measures = []
    try:
        for finding_text in request.findings:
            data = dict(shared_context, finding=finding_text)
            measures.append(suggest_measures(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if len(measures) != len(request.findings):
        raise HTTPException(
            status_code=500,
            detail="Internal error: number of measures does not match number of findings.",
        )

    return {"measures": measures}
