from email.message import EmailMessage
from email.mime.text import MIMEText
from functools import lru_cache
from typing import Annotated

import aiosmtplib


class EmailService:
    async def send_email(self, data: dict) -> None:
        message = EmailMessage()
        message["From"] = data["email_from"]
        message["To"] = data["email_to"]
        message["Subject"] = data["subject"]
        message.attach(MIMEText(data["body"], "html"))


@lru_cache
def get_email_service():
    return EmailService()
