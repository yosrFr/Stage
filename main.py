from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.opportunities_router import router as opportunities_router
from api.routes.export import router as export_router
# from api.routes.paraphrase import router as rewrite_router
from api.routes.import_data import router as import_router
from api.routes.measure_suggestion import router as measure_suggestion_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(export_router)
# app.include_router(rewrite_router)
app.include_router(import_router)
app.include_router(measure_suggestion_router)
app.include_router(opportunities_router)
