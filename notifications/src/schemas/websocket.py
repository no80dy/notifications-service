import uuid
from pydantic import BaseModel


class InputCommentLikeMessage(BaseModel):
    producer_id: uuid.UUID
    consumer_id: uuid.UUID
    comment_id: uuid.UUID


class OutputComentLikeMessage(BaseModel):
    user_id: uuid.UUID
    consumer_id: uuid.UUID
    comment_id: uuid.UUID
