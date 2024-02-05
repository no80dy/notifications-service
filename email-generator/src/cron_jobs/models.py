import uuid
from uuid import UUID

from pydantic import BaseModel, Field


class Notification(BaseModel):
    notification_id: UUID = Field(default_factory=uuid.uuid4)
    event_name: str


class OutputFilmReleaseMessage(Notification):
    """
       Данная модель предназначена для ежемесячного
       оповещения всех пользователей о новых фильмах в кинотеатре за последний месяц.
   """
    event_name: str = 'films_release'
    film_ids: list[UUID]
    month_release: int = Field(ge=1, le=12)


class OutputFilmSelectionMessage(Notification):
    """
    Данная модель предназначена для еженедельного
    оповещения пользователей персонально о фильмах, которые они лайкнули, но не посмотрели.
    """
    event_name: str = 'films_selection'
    user_id: UUID
    films_ids: list[UUID]
