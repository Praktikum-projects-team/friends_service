import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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


# Попытка связать таблицы в разных базах
# class Friends(Base):
#     __tablename__ = 'friends'
#     __bind_key__ = 'friends_postgres'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(
#         UUID(as_uuid=True),
#         ForeignKey('auth_postgres.users.id', ondelete='CASCADE'),
#         nullable=False
#     )
#     friend_id = Column(
#         UUID(as_uuid=True),
#         ForeignKey('auth_postgres.users.id', ondelete='CASCADE'),
#         nullable=False
#     )
#
#     # Определяем связь с таблицей "users" в другой базе данных
#     user = relationship('User', foreign_keys=[user_id])
#     friend = relationship('User', foreign_keys=[friend_id])
#
#
# class User(Base):
#     __tablename__ = 'users'
#     __bind_key__ = 'auth_postgres'  # Указываем имя подключения к другой базе данных
