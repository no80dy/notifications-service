from contextlib import asynccontextmanager

import uvicorn
from api.v1 import emails, notifications, websocket
from core.config import settings
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker
from integration import mongodb, rabbitmq
from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.mongo_client = AsyncIOMotorClient(settings.mongodb_url)
    rabbitmq.rabbitmq_broker = RabbitBroker(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_login,
        password=settings.rabbitmq_password,
    )
    await rabbitmq.rabbitmq_broker.connect()
    await rabbitmq.configure_rabbit_queues()
    await rabbitmq.configure_rabbit_exchange()
    yield
    await rabbitmq.rabbitmq_broker.close()
    mongodb.mongo_client.close()


app = FastAPI(
    description="Сервис нотификаций",
    version="0.0.0",
    title=settings.project_name,
    docs_url="/notifications/api/openapi",
    openapi_url="/notifications/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(
    notifications.router, prefix="/notifications/api/v1", tags=["user_notifications"]
)
app.include_router(
    websocket.router, prefix="/notifications/api/v1", tags=["push_notifications"]
)
app.include_router(
    emails.router, prefix="/notifications/api/v1", tags=["email_notifications"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
