import logging
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.auth_bearer import BaseJWTBearer
from db.models_data import FriendsData
from db.postgres import (
    delete_friend_db,
    get_all_friend_ids_for_user_db,
    get_db,
    get_friend_by_ids,
    insert_friend_db
)
from db.postgres_auth import get_friend_data
from services.postgres import UserAlreadyExists

jwt_bearer = BaseJWTBearer()


class FriendsService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def add_friend(self, friends_data):
        try:
            friend_data = FriendsData(user_id=friends_data.user_id, friend_id=friends_data.friend_id)
            await insert_friend_db(friend_data, self.session)

        except IntegrityError:
            logging.warning('Friend already exists')
            raise UserAlreadyExists('Friend already exists')

    async def delete_friend(self, token, friend_id):
        user_info = jwt_bearer.decode_jwt(token)
        friend_data = FriendsData(user_id=user_info['id'], friend_id=friend_id)
        is_friend = await get_friend_by_ids(friend_data, self.session)
        if not is_friend:
            raise NoResultFound

        try:
            await delete_friend_db(friend_data, self.session)
            return True
        except Exception as e:
            logging.error(e)
            return None

    async def get_all_friends_for_user(self, token):
        user_info = jwt_bearer.decode_jwt(token)
        all_friends_data = list()

        try:
            friend_ids = await get_all_friend_ids_for_user_db(user_info['id'], self.session)

            for friend_id in friend_ids:
                # Для обращения по апи нужны админские права
                # friend_info = await get_auth_api().get_user_info(friend_id)
                friend_info = await get_friend_data(friend_id)
                friend_info_for_resp = {
                    'id': friend_id,
                    'login': friend_info[0],
                    'name': friend_info[1],
                }
                all_friends_data.append(friend_info_for_resp)

            return all_friends_data

        except Exception as e:
            logging.error(e)
            return None


@lru_cache()
def get_friends_service(
        session: AsyncSession = Depends(get_db),
) -> FriendsService:
    return FriendsService(session=session)
