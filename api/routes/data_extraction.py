import json
from pathlib import Path

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database.session import get_db
from services.database.data_extraction.extract_model_data import get_model_data

router = APIRouter(prefix="/extract_data", tags=["extract_data"])


@router.get(
    "/",
    summary="Extract all needed data from the database",
    description="Extract control title, language, risk level, maturity level, findings and measures from the database"
)
def extract_data(db: Session = Depends(get_db)):
    data = get_model_data(db)

    file_path = Path(f"exports/training_data.json")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {
        "message": "Extraction successful",
        "file": str(file_path)
    }
