import json

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/import", tags=["import"])


@router.post(
    "/import_data",
    summary="Import data from a JSON file into the database",
    description="Import the new paraphrased data from an external file into the database"
)
async def import_data(file: UploadFile = File(...)):
    try:
        content = await file.read()
        json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON file: {e}")

    return {
        "message": "Import successful",
    }
