from contextlib import asynccontextmanager

import uvicorn
from aiosmtplib import SMTP
from api.v1 import email, websocket
from core.config import settings
from fastapi import FastAPI
from integration import smtp


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with email.router.lifespan_context(app):
        smtp.smtp_client = SMTP(
            hostname=settings.mailhog_host, port=settings.mailhog_port
        )
        await smtp.smtp_client.connect()
        yield
        smtp.smtp_client.close()


app = FastAPI(
    description="notification worker",
    version="0.0.0",
    title=settings.project_name,
    docs_url="/worker/api/openapi",
    openapi_url="/worker/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(email.router)
app.include_router(websocket.router, tags=["websocket"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
