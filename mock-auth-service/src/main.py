import structlog
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi import Request, status
from fastapi.responses import JSONResponse

from api.v1 import users
from core.config import settings


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    description='Сервис по авторизации и аутентификации пользователей',
    version='1.0.0',
    title=settings.project_name,
    docs_url='/auth/api/openapi',
    openapi_url='/auth/api/openapi.json',
    default_response_class=JSONResponse,
    lifespan=lifespan
)


app.include_router(users.router, prefix='/auth/api/v1/users', tags=['users'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )