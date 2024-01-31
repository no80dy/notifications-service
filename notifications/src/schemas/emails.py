import uuid

from pydantic import BaseModel, Field


class BasePersonalMessage(BaseModel):
    user_id: uuid.UUID


class InputFilmSelectionMessage(BasePersonalMessage):
    """
    Данная модель предназначена для еженедельного
    оповещения пользователей персонально
    """

    films_ids: list[uuid.UUID]


class InputFilmReleaseMessage(BasePersonalMessage):
    """
    Данная модель предназначена для ежемесячного
    оповещения всех пользователей

    watched_count: всего просмотренно за месяц
    """

    watched_count: int


class InputWelcomeMessage(BasePersonalMessage):
    """
    Данная модель предназначена для оповещения
    пользователей, которые только что зарегистрировались
    """

    pass


class InputManagerMessage(BaseModel):
    users_ids: list[uuid.UUID] = Field(..., default_factory=list)
    email_from: str
    subject: str
    body: str
