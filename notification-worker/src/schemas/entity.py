from pydantic import BaseModel


class InputEmailMessage(BaseModel):
    email_from: str
    email_to: str
    subject: str
    body: str


class InputWebSocketMessage(BaseModel):
    producer_name: str
    consumer_name: str
