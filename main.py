from fastapi import FastAPI

from api.routes.export import router as export_router
from api.routes.rewrite import router as rewrite_router

app = FastAPI()

app.include_router(export_router)
app.include_router(rewrite_router)
