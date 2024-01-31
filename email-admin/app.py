import uuid
from http import HTTPStatus
from typing import Annotated

import httpx
from httpx import ConnectTimeout, ConnectError
from auth import security_jwt
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field


app = FastAPI(
    title='Email-admin service',
    summary='Admins send messages for group of users',
    docs_url="/email_admin/api/openapi",
    openapi_url="/email_admin/api/openapi.json",
    prefix="/email_admin/api/v1/"
)

MAX_EMAILS_BATCH_SIZE = 50
NOTIFICATION_SERVICE_URL = 'http://notifications:8000/notifications/api/v1/manager-message'
AUTH_SERVICE_URL = 'http://auth:8000/auth/api/v1/users/'


class InputManagerMessage(BaseModel):
    users_ids: list[uuid.UUID] = Field(default_factory=uuid.uuid4)
    subject: str
    body: str


class OutputManagerMessage(BaseModel):
    users_ids: list[uuid.UUID] = Field(max_item=MAX_EMAILS_BATCH_SIZE)
    email_from: EmailStr
    subject: str
    body: str


@app.post(
    '/post_message',
    summary='Оправка сообщения группе пользователей',
    response_model=OutputManagerMessage
)
async def post_message(
        message: InputManagerMessage,
        user_data: Annotated[dict, Depends(security_jwt)],
):
    """Так как пользователей может быть много отправка сообщения идет по 50 штук пользователей."""
    admin_id = user_data.get('user_id')

    # Получаем почту администратора от сервиса авторизации
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(AUTH_SERVICE_URL, params={'users_ids': [admin_id]})
            if response.status_code == HTTPStatus.OK:
                email_from = response.json()[0].get('email')
    except ConnectError or ConnectTimeout:
        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={
                'msg': 'auth-service is not available',
            }
        )

    message_dto = jsonable_encoder(message)
    user_ids = message_dto['users_ids']

    # Отправляем сообщение со списком по 50 юзеров
    try:
        async with httpx.AsyncClient() as client:
            while user_ids:
                if len(user_ids) > MAX_EMAILS_BATCH_SIZE:
                    out_user_ids = user_ids[:MAX_EMAILS_BATCH_SIZE]
                    user_ids = user_ids[MAX_EMAILS_BATCH_SIZE:]
                else:
                    out_user_ids = user_ids
                    user_ids = []

                out_message_dto = {
                    'users_ids': out_user_ids,
                    'email_from': email_from,
                    'subject': message_dto['subject'],
                    'body': message_dto['body'],
                }
                out_message = OutputManagerMessage(**out_message_dto)
                await client.post(NOTIFICATION_SERVICE_URL, json=out_message.model_dump())
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                'msg': 'message is sent'
            }
        )
    except ConnectError or ConnectTimeout:
        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={
                'msg': 'notification-service is not available',
            }
        )
