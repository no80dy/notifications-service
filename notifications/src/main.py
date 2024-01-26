from contextlib import asynccontextmanager

import uvicorn
from api.v1 import emails
from core.config import settings
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker
from warehouse import rabbitmq


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq.rabbitmq_broker = RabbitBroker(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_login,
        password=settings.rabbitmq_password,
    )
    await rabbitmq.rabbitmq_broker.connect()
    await rabbitmq.configure_rabbit_exchange()
    await rabbitmq.configure_rabbit_queue()
    yield
    await rabbitmq.rabbitmq_broker.close()


app = FastAPI(
    description="Сервис нотификаций",
    version="0.0.0",
    title=settings.project_name,
    docs_url="/notifications/api/openapi",
    openapi_url="/notifications/api/openapi.json",
    lifespan=lifespan,
)


app.include_router(
    emails.router,
    tags=[
        "kafka",
    ],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
