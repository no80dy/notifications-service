import aiosmtplib
from typing import Annotated
from email.message import EmailMessage
from functools import lru_cache
from email.mime.text import MIMEText


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
