import uuid
from pydantic import BaseModel


class InputEmailMessage(BaseModel):
    email_from: str
    email_to: str
    subject: str
    body: str


class InputLikeCommentMessage(BaseModel):
    user_id: uuid.UUID
    producer_id: uuid.UUID
    comment_id: uuid.UUID
