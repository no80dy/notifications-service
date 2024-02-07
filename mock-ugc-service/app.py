import logging
import uuid
from http import HTTPStatus
from uuid import UUID

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mock UGC service",
    summary="Generate event - User liked another user comment",
    docs_url="/ugc/api/openapi",
    openapi_url="/ugc/api/openapi.json",
    prefix="/ugc/api/v1/",
)


NOTIFICATION_SERVICE_URL = "http://notifications:8000/notifications/api/v1/like"


class OutputCommentLikeMessage(BaseModel):
    """Уведомление о том, что Producer поставил лайк комментарию, который оставил Consumer."""

    notification_id: UUID = Field(default_factory=uuid.uuid4)
    event_name: str = "comment_likes"
    producer_id: UUID = Field(default_factory=uuid.uuid4)
    comment_id: UUID = Field(default_factory=uuid.uuid4)
    consumer_id: UUID = Field(default_factory=uuid.uuid4)


@app.get(
    "/post_event",
)
async def post_event() -> JSONResponse:
    message = OutputCommentLikeMessage()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                NOTIFICATION_SERVICE_URL, json=message.model_dump_json()
            )
            logging.info(response)
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"msg": "message was posted", "detail": response.text},
            )
    except httpx.ConnectError or httpx.ConnectTimeout as e:
        logging.error(e)
        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={"detail": "notification-service is not available"},
        )
