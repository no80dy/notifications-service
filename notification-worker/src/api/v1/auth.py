import http
import time
from typing import Optional

import jwt
from fastapi import (
	HTTPException,
	Request,
	WebSocketException,
	status
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import settings


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(
            token, settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if not credentials:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        if not credentials.scheme == 'Bearer':
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> Optional[dict]:
        return decode_token(jwt_token)


security_jwt = JWTBearer()