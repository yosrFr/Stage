from fastapi import FastAPI

from api.routes.export import router as export_router
from api.routes.paraphrase import router as rewrite_router
from api.routes.import_data import router as import_router
from api.routes.measure_suggestion import router as measure_suggestion_router
from api.routes.data_extraction import router as data_extraction_router
from api.routes.findings_measures_suggestion import router as findings_measures_suggestion_router
from api.routes.findings_suggestion import router as findings_suggestion_router
from threatflow.api.assist import router as assist_router
from threatflow.api.follow_up import router as followup_router

app = FastAPI()

app.include_router(export_router)
app.include_router(rewrite_router)
app.include_router(import_router)
app.include_router(measure_suggestion_router)
app.include_router(data_extraction_router)
app.include_router(findings_measures_suggestion_router)
app.include_router(findings_suggestion_router)
app.include_router(assist_router)
app.include_router(followup_router)