import uvicorn
from api.v1 import email
from core.config import settings
from fastapi import FastAPI
from integration import smtp
from contextlib import asynccontextmanager
from aiosmtplib import SMTP


@asynccontextmanager
async def lifespan(app: FastAPI):
    smtp.smtp_client = SMTP(hostname="127.0.0.1", port=1025)
    await smtp.smtp_client.connect()
    yield
    smtp.smtp_client.close()


app = FastAPI(
    description="Сервис воркер",
    version="0.0.0",
    title=settings.project_name,
    docs_url="/worker/api/openapi",
    openapi_url="/worker/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(email.router, prefix="/worker/api/v1", tags=["rabbitmq"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
