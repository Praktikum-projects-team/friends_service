import json
import logging
from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import ConnectError

from core.config import auth_config
from services.auth import AuthApi, get_auth_api


class BaseJWTBearer(HTTPBearer):
    """
    base class for jwt token checking
    """

    def __init__(self, auto_error: bool = True):
        super(BaseJWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = 'Bearer'

    async def __call__(
            self,
            request: Request,
            auth_api: AuthApi = Depends(get_auth_api)
    ):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(BaseJWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == self.token_type:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid authentication scheme.")
            token_payload = await self.verify_jwt(credentials.credentials, auth_api)
            if not token_payload:
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid token or expired token.")
            request.token_payload = token_payload  # type: ignore[attr-defined]
            return credentials.credentials
        else:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authorization code.")

    def decode_jwt(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, auth_config.jwt_secret, algorithms=[auth_config.jwt_algorithm])
            return json.loads(payload.get('user_info'))
        except jwt.PyJWTError:
            return {}

    def check_payload(self, jwt_payload):
        """"
        To be overriden if you expect to get certain values from user info (roles, for example)
        """
        return True

    async def verify_jwt(self, jwtoken: str, auth_api: AuthApi) -> dict:

        try:
            current_user = await auth_api.check_token(jwtoken)
        except ConnectError:
            logging.exception('auth api connection error')
            current_user = self.decode_jwt(jwtoken)

        if not self.check_payload(current_user):
            return {}

        return current_user
