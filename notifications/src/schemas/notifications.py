import uuid

from pydantic import BaseModel


class BaseNotificationPayload(BaseModel):
    user_id: uuid.UUID
    producer_id: uuid.UUID


class BaseEmailNotificationPayload(BaseNotificationPayload):
    subject: str


class EmailPersonalNotificationSchemaRefactor(BaseEmailNotificationPayload):
    template_name: str


class EmailGeneralNotificationSchemaRefactor(BaseEmailNotificationPayload):
    body: str


class PushNotificationSchema(BaseNotificationPayload):
    comment_id: uuid.UUID
