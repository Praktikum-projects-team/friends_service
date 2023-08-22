import json
from datetime import datetime
from http import HTTPStatus
from uuid import UUID, uuid4

from fastapi import HTTPException
from httpx import AsyncClient

from core.base_model import OrjsonBaseModel
from core.config import auth_config


class AdminUserInfoSchema(OrjsonBaseModel):
    id: UUID
    login: str
    created_at: datetime
    name: str
    is_superuser: bool
    roles: list[dict]


class Token(OrjsonBaseModel):
    access_token: str
    refresh_token: str


class AuthApi:
    def __init__(self):
        self.auth_header_key = 'Authorization'
        self.token_type = 'Bearer'
        self.x_request_id = 'x_request_id'
        self.token_checking_url = auth_config.host + '/api/v1/auth/check_access_token'
        self.get_user_info_url = auth_config.host + '/api/v1/admin/users'
        self.login = auth_config.host + '/api/v1/auth/login'

    async def check_token(self, token):
        async with AsyncClient() as client:
            auth_answer = await client.post(
                self.token_checking_url,
                headers={self.auth_header_key: self.token_type + ' ' + token, 'X-Request-Id': self.x_request_id},
            )
        if auth_answer.status_code == HTTPStatus.OK:
            body = auth_answer.json()
            return json.loads(body)
        if auth_answer.status_code == HTTPStatus.UNAUTHORIZED:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or expired token.")

    async def get_user_info(self, user_id: UUID):
        async with AsyncClient() as client:
            token = await self.get_token(
                login=auth_config.admin_login,
                password=auth_config.admin_password,
            )
            headers = {
                self.auth_header_key: f'{self.token_type} {token.access_token}',
                'X-Request-Id': str(uuid4()),
            }
            response = await client.get(
                url=f'{self.get_user_info_url}/{str(user_id)}',
                headers=headers
            )
            if response.status_code == HTTPStatus.NOT_FOUND:
                return None
            return AdminUserInfoSchema(**response.json())

    async def get_token(self, login: str, password: str):
        async with AsyncClient() as client:
            payload = {'login': login, 'password': password}
            headers = {'X-Request-Id': str(uuid4())}
            response = await client.post(self.login, json=payload, headers=headers)
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail='Invalid token or expired token.',
                )
            return Token(**response.json())


def get_auth_api():
    return AuthApi()
