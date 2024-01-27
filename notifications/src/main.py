from contextlib import asynccontextmanager

import uvicorn
from api.v1 import emails
from core.config import settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    description="Сервис нотификаций",
    version="0.0.0",
    title=settings.project_name,
    docs_url="/notifications/api/openapi",
    openapi_url="/notifications/api/openapi.json",
    lifespan=lifespan,
)


app.include_router(emails.router, prefix="/notifications/api/v1", tags=["kafka"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
