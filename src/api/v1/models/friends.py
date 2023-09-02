from uuid import UUID

from pydantic import Field

from core.base_model import OrjsonBaseModel


class FriendReq(OrjsonBaseModel):
    user_id: UUID
    friend_id: UUID


class FriendResp(OrjsonBaseModel):
    msg: str


class FriendDataResp(OrjsonBaseModel):
    id: str
    login: str
    name: str


class AllFriendsDataResp(OrjsonBaseModel):
    friends: list[FriendDataResp] = Field(default_factory=list)
