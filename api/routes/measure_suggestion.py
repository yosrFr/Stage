from fastapi import APIRouter, HTTPException

from services.AI.suggesting.suggestion_engine import suggest_text

router = APIRouter(prefix="/suggestion", tags=["suggestion"])


@router.post(
    "/",
    summary="Suggest measures for findings",
    description="""
    Give the AI model a finding (text) and it returns a suggested measure (text)
    """
)
async def measure_suggestion(text: str):
    try:
        result = suggest_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result
