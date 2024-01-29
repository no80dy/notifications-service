import uvicorn
from core.config import settings
from fastapi import FastAPI
from api.v1 import email


app = FastAPI(
    description="Сервис нотификаций",
    version="0.0.0",
    title=settings.project_name,
    docs_url="/notifications/api/openapi",
    openapi_url="/notifications/api/openapi.json",
    lifespan=email.router.lifespan_context,
)

app.include_router(email.router, tags=["rabbitmq"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
