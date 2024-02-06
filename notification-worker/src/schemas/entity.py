import uuid

from pydantic import BaseModel


class InputEmailMessage(BaseModel):
    email_from: str
    email_to: str
    subject: str
    body: str


class BaseInputNotificationPayload(BaseModel):
    user_id: uuid.UUID
    producer_id: uuid.UUID
    subject: str


class InputLikeCommentNotification(BaseInputNotificationPayload):
    comment_id: uuid.UUID


class InputGeneralEmailNotification(BaseInputNotificationPayload):
    body: str


class InputWelcomeNotification(BaseInputNotificationPayload):
    template_name: str


class InputFilmReleaseNotification(BaseInputNotificationPayload):
    films_ids: list[uuid.UUID]
    watched_count: int
    template_name: str


class InputFilmSelectionNotification(BaseInputNotificationPayload):
    films_ids: list[uuid.UUID]
    template_name: str


class InputManagerNotification(BaseInputNotificationPayload):
    body: str


class UserInformation(BaseModel):
    id: uuid.UUID
    username: str
    email: str
