import json
import copy

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from services.file_handler import rewrite_json

router = APIRouter(prefix="/paraphrase", tags=["paraphrase"])


@router.post("/")
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
    formatted = json.dumps(result, ensure_ascii=False, indent=2)
    return Response(
        content=formatted,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{output_filename}"'},
    )