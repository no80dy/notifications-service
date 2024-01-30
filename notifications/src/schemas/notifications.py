import uuid
from pydantic import BaseModel


class BaseNotificationPayload(BaseModel):
    user_id: uuid.UUID


class EmailNotificationSchema(BaseNotificationPayload):
    email_from: str
    email_to: str
    subject: str
    body: str


class PushNotificationSchema(BaseNotificationPayload):
    comment_id: uuid.UUID
    producer_id: uuid.UUID
