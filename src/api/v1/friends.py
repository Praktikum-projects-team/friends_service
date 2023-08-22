import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.friends import AllFriendsDataResp, FriendReq, FriendResp
from services.auth import AuthApi
from services.friends import FriendsService, get_friends_service

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/',
    response_model=FriendResp,
    description='Добавление друга',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_friend(
        data: FriendReq,
        friends_service: FriendsService = Depends(get_friends_service)
) -> FriendResp:
    try:
        await friends_service.add_friend(data)
    except Exception as e:
        logging.error(e)
        return FriendResp(msg="Adding friend is failed")

    return FriendResp(msg="Friend added")


@router.delete(
    '/{friend_id}',
    response_model=FriendResp,
    description='Удаление друга',
    dependencies=[Depends(BaseJWTBearer())]
)
async def delete_friend(
        friend_id: str,
        token: str = Depends(BaseJWTBearer()),
        friends_service: FriendsService = Depends(get_friends_service)
) -> FriendResp:
    print()
    print(f'token: {token}')
    print()
    friend = await friends_service.delete_friend(token=token, friend_id=friend_id)

    if not friend:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Friend not found')

    return FriendResp(msg="Friend deleted")


@router.get(
    '/',
    response_model=AllFriendsDataResp,
    description='Получение всех друзей пользователя',
    dependencies=[Depends(BaseJWTBearer())]
)
async def get_all_friends_for_user(
        token: str = Depends(BaseJWTBearer()),
        friends_service: FriendsService = Depends(get_friends_service)
) -> AllFriendsDataResp:
    friends = await friends_service.get_all_friends_for_user(token=token)
    if not friends:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Friends not found')

    return AllFriendsDataResp(friends=friends)
