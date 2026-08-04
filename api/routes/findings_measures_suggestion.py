from fastapi import APIRouter, HTTPException

from services.AI.suggesting.findings_measures.suggestion_engine import suggest_measures

router = APIRouter(prefix="/suggestion", tags=["suggestion"])


@router.post(
    "/findings_measures",
    summary="Suggest findings and measures for controls",
    description="""
    Give the AI model audit data and it returns a suggested findings and measures for a control
    """
)
async def measure_suggestion(data: dict):
    try:
        result = suggest_measures(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result
