import uuid

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
