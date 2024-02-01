from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import lru_cache
from typing import Annotated

from aiosmtplib import SMTP
from fastapi import Depends
from integration.smtp import get_smtp_client


class EmailService:
    def __init__(self, smtp_client: SMTP):
        self.smtp_client = smtp_client

    async def send_email(self, data: dict) -> None:
        message = MIMEMultipart()
        message["From"] = data["email_from"]
        message["To"] = data["email_to"]
        message["Subject"] = data["subject"]
        message.attach(
            MIMEText(
                data["body"],
                "html",
            )
        )

        await self.smtp_client.send_message(
            message, sender="root@localhost", recipients="somebody@localhost"
        )

    async def handle_message(self, data: dict) -> None:
        await self.send_email(data)


@lru_cache
def get_email_service(smtp_client: Annotated[SMTP, Depends(get_smtp_client)]):
    return EmailService(smtp_client)
