from fastapi import FastAPI
from omiye.api.routes import router as api_router

app = FastAPI(
    title="Omiye Master: Police Report Extraction",
    description="Vision-Language Model based extraction for police reports.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")
