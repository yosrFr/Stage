import json
from pathlib import Path

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database.session import get_db
from services.export_service import get_all_norm_info

router = APIRouter()


@router.get("/export_all/{norm_id}")
def export_all(norm_id: int, db: Session = Depends(get_db)):
    data = get_all_norm_info(db, norm_id)

    file_path = Path(f"exports/norm_{norm_id}.json")

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {
        "message": "Export successful",
        "file": str(file_path)
    }
