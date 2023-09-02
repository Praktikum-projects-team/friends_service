import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


if TYPE_CHECKING:
    class Base:
        pass
else:
    Base = declarative_base()


class Friends(Base):
    __tablename__ = 'friends'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    friend_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='uq_user_friend'),
    )
