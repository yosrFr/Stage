import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/categories", tags=["categories"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

@router.get("/{norm}")
def get_categories(norm: str):
    folder = os.path.join(DATA_DIR, f"{norm.upper()}_json")

    lang_path = os.path.join(folder, "category_languages.json")
    cat_path = os.path.join(folder, "categories.json")

    if not os.path.exists(lang_path) or not os.path.exists(cat_path):
        raise HTTPException(status_code=404, detail=f"Fichiers introuvables pour la norme '{norm}'")

    with open(lang_path, "r", encoding="utf-8") as f:
        lang_data = json.load(f)

    with open(cat_path, "r", encoding="utf-8") as f:
        cat_data = json.load(f)

    id_by_category_id = {item["category_id"]: item.get("id") for item in cat_data}

    categories = [
        {
            "category_id": item["category_id"],
            "category_name": item["category_name"],
            "display_id": id_by_category_id.get(item["category_id"])
        }
        for item in lang_data
        if item.get("language_id") == 2
    ]

    return categories