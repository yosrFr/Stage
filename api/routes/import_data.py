import json

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database.session import get_db
from services.import_service import import_norm

router = APIRouter(prefix="/import", tags=["import"])


@router.post(
    "/import_data",
    summary="Import data from a JSON file into the database",
    description="Import the new paraphrased data from an external file into the database"
)
async def import_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON file: {e}")

    return import_norm(db, data)
