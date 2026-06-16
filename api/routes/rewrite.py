import json
import copy
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File

from services.file_handler import rewrite_json

router = APIRouter(prefix="/paraphrase", tags=["paraphrase"])


@router.post(
    "/",
    summary="Paraphrase JSON descriptions and objectives",
    description="""
    Upload a JSON file, paraphrase all description and objective fields using the configured AI model 
    and create a new JSON file while preserving the original structure
    """
)
async def paraphrase(file: UploadFile = File(...)):
    try:
        content = await file.read()
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON file: {e}")

    try:
        result = rewrite_json(copy.deepcopy(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    output_filename = file.filename.replace(".json", "_paraphrased.json")

    output_dir = Path("exports")
    output_dir.parent.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / output_filename

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return {
        "message": "Export successful",
        "file": str(output_file)
    }
