import uuid

from pydantic import BaseModel


class UserInformation(BaseModel):
    id: uuid.UUID
    username: str
    email: str
