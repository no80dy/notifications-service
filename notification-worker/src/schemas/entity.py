import uuid
from pydantic import BaseModel


class InputEmailMessage(BaseModel):
    email_from: str
    email_to: str
    subject: str
    body: str


class InputLikeCommentMessage(BaseModel):
    producer_id: uuid.UUID
    consumer_id: uuid.UUID
    comment_id: uuid.UUID
