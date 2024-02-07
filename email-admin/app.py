import uuid
from http import HTTPStatus
from typing import Annotated

import httpx
from auth import security_jwt
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx import ConnectError, ConnectTimeout
from pydantic import BaseModel, EmailStr, Field
from settings import settings

app = FastAPI(
    title="Email-admin service",
    summary="Admins send messages for group of users",
    docs_url="/email_admin/api/openapi",
    openapi_url="/email_admin/api/openapi.json",
    prefix="/email_admin/api/v1/",
)


class InputManagerMessage(BaseModel):
    users_ids: list[uuid.UUID] = Field(default_factory=uuid.uuid4)
    subject: str
    body: str


class OutputManagerMessage(BaseModel):
    users_ids: list[uuid.UUID] = Field(max_item=settings.max_emails_batch_size)
    producer_id: uuid.UUID
    subject: str
    body: str


@app.post(
    "/post_message",
    summary="Оправка сообщения группе пользователей",
    response_model=OutputManagerMessage,
)
async def post_message(
    message: InputManagerMessage,
    user_data: Annotated[dict, Depends(security_jwt)],
):
    """Так как пользователей может быть много отправка сообщения идет по 50 штук пользователей."""
    admin_id = user_data.get("user_id")
    message_dto = jsonable_encoder(message)
    user_ids = message_dto["users_ids"]

    # Отправляем сообщение со списком по 50 юзеров
    try:
        async with httpx.AsyncClient() as client:
            while user_ids:
                if len(user_ids) > settings.max_emails_batch_size:
                    out_user_ids = user_ids[: settings.max_emails_batch_size]
                    user_ids = user_ids[settings.max_emails_batch_size :]
                else:
                    out_user_ids = user_ids
                    user_ids = []

                out_message_dto = {
                    "users_ids": out_user_ids,
                    "producer_id": admin_id,
                    "subject": message_dto["subject"],
                    "body": message_dto["body"],
                }
                out_message = OutputManagerMessage(**out_message_dto)
                await client.post(
                    settings.notification_service_url,
                    data=out_message.model_dump(),
                )
        return JSONResponse(
            status_code=HTTPStatus.OK, content={"msg": "message is sent"}
        )
    except ConnectError or ConnectTimeout:
        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={
                "msg": "notification-service is not available",
            },
        )
