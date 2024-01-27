import uuid

from pydantic import BaseModel


class UserInformationResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
