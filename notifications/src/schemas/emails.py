import uuid

from pydantic import BaseModel, Field


class InputPersonalFilmSelection(BaseModel):
    """
    Данная модель предназначена для еженедельного
    оповещения пользователей персонально
    """

    user_id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    films_ids: list[uuid.UUID] = Field(..., default_factory=list)


class InputNewFilmsReleases(BaseModel):
    """
    Данная модель предназначена для ежемесячного
    оповещения всех пользователей

    watched_count: всего просмотренно за месяц
    """

    user_id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    watched_count: int


class InputWelcomeMessage(BaseModel):
    """
    Данная модель предназначена для оповещения
    пользователей, которые только что зарегистрировались
    """

    user_id: uuid.UUID = Field(..., default_factory=uuid.uuid4)


class OutputEmailMessage(BaseModel):
    """
    Данный класс содержит всю информацию, нуобходимую для передачи
    в воркер для отправки по email
    """

    email_from: str
    email_to: str
    subject: str
    body: str
