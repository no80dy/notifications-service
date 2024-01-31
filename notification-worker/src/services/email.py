from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import lru_cache
from typing import Annotated
from aiosmtplib import SMTP
from fastapi import Depends
from integration.smtp import get_smtp_client


html_message = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HTML5 Boilerplate</title>
  <link rel="stylesheet" href="styles.css">
</head>

<body>
  <h1>Page Title</h1>
  <script src="scripts.js"></script>
</body>

</html>
"""


class EmailService:
    def __init__(self, smtp_client: SMTP):
        self.smtp_client = smtp_client

    async def send_email(self, data: dict) -> None:
        message = MIMEMultipart()
        message["From"] = data["email_from"]
        message["To"] = data["email_to"]
        message["Subject"] = data["subject"]
        message.attach(MIMEText(html_message, "html", ))

        await self.smtp_client.send_message(
            message, sender="root@localhost", recipients="somebody@localhost"
        )

    async def handle_message(self, data: dict) -> None:
        await self.send_email(data)


@lru_cache
def get_email_service(
    smtp_client: Annotated[SMTP, Depends(get_smtp_client)]
):
    return EmailService(smtp_client)
