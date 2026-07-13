from fastapi import FastAPI

from api.routes.export import router as export_router
from api.routes.paraphrase import router as rewrite_router
from api.routes.import_data import router as import_router
from api.routes.measure_suggestion import router as measure_suggestion_router

app = FastAPI()

app.include_router(export_router)
app.include_router(rewrite_router)
app.include_router(import_router)
app.include_router(measure_suggestion_router)
