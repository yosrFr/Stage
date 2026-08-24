from fastapi import APIRouter, HTTPException

from schema.finding_sugg_schema import FindingSuggestionRequest
from services.AI.suggesting.prompt_engineered.finding_only.finding_suggestion_engine import suggest_findings

router = APIRouter(prefix="/suggestion", tags=["prompt_engineered"])


@router.post(
    "/pe_findings",
    summary="Suggest findings for controls",
    description="""
    Give the AI model audit data and it returns a suggested findings for a control
    """
)
def findings_suggestion(request: FindingSuggestionRequest):
    try:
        result = suggest_findings(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"findings": result}
