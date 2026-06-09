from fastapi import FastAPI

from api.routes.export import router as export_router

app = FastAPI()

app.include_router(export_router)