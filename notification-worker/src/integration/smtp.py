from aiosmtplib import SMTP


smtp_client: SMTP | None = None


def get_smtp_client() -> SMTP:
	return smtp_client
