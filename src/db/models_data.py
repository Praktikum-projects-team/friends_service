from uuid import UUID

from core.base_model import OrjsonBaseModel


class FriendsData(OrjsonBaseModel):
    user_id: UUID
    friend_id: UUID
