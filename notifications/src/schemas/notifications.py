import uuid

from pydantic import BaseModel, Field

from .emails import OutputEmailMessage


class NotificationModel(BaseModel):
    notification_id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    content: OutputEmailMessage
