import uuid

from pydantic import BaseModel, Field


class BasePersonalNotification(BaseModel):
    user_id: uuid.UUID


class InputFilmSelectionNotification(BasePersonalNotification):
    """
    Данная модель предназначена для еженедельного
    оповещения пользователей персонально
    """

    films_ids: list[uuid.UUID]


class InputFilmReleaseNotification(BasePersonalNotification):
    """
    Данная модель предназначена для ежемесячного
    оповещения всех пользователей

    watched_count: всего просмотренно за месяц
    """

    films_ids: list[uuid.UUID]
    watched_count: int


class InputWelcomeNotification(BasePersonalNotification):
    """
    Данная модель предназначена для оповещения
    пользователей, которые только что зарегистрировались
    """

    pass


class InputManagerNotification(BaseModel):
    users_ids: list[uuid.UUID]
    producer_id: uuid.UUID
    subject: str
    body: str


class BaseOutputNotification(BaseModel):
    user_id: uuid.UUID
    producer_id: uuid.UUID
    subject: str


class OutputFilmSelectionNotification(BaseOutputNotification):
    films_ids: list[uuid.UUID]
    template_name: str


class OutputFilmReleaseNotification(BaseOutputNotification):
    films_ids: list[uuid.UUID]
    watched_count: int
    template_name: str


class OutputWelcomeNotification(BaseOutputNotification):
    template_name: str


class OutputManagerNotification(BaseOutputNotification):
    body: str
