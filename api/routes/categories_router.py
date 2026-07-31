import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/categories", tags=["categories"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

@router.get("/{norm}")
def get_categories(norm: str):
    file_path = os.path.join(DATA_DIR, f"{norm.upper()}_json", "category_languages.json")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier introuvable pour la norme '{norm}'")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = [
        {"category_id": item["category_id"], "category_name": item["category_name"]}
        for item in data
        if item.get("language_id") == 2
    ]

    return categories