import logging

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import exc as orm_exc

from core.config import pg_config
from db.models_data import FriendsData
from db.models_pg import Friends
from services.postgres import UserAlreadyExists

async_engine = create_async_engine(pg_config.url_async)


async def get_db():
    async with AsyncSession(async_engine) as session:
        yield session


async def insert_friend_db(friends_data: FriendsData, session):
    try:
        friend = Friends(**friends_data.dict())
        session.add(friend)
        await session.commit()
        await session.refresh(friend)
        logging.info(f'friend.id: {friend.id}')
        return friend.id

    except IntegrityError:
        session.rollback()
        logging.warning('Friend already exists')
        raise UserAlreadyExists('Friend already exists')

    except Exception as e:
        session.rollback()
        logging.error(e)
        raise e


async def delete_friend_db(friends_data: FriendsData, session):
    try:
        query = delete(Friends).where(
            Friends.user_id == friends_data.user_id,
            Friends.friend_id == friends_data.friend_id
        )
        await session.execute(query)
        await session.commit()
        return True

    except Exception as e:
        logging.error(e)
        return None


async def get_all_friend_ids_for_user_db(user_id: str, session):
    try:
        query = select(Friends.friend_id).where(Friends.user_id == user_id)
        friends = await session.execute(query).fetchall()
        friend_ids = [friend[0] for friend in friends]

        logging.warning(f'friend_ids: {friend_ids}')

        return friend_ids

    except Exception as e:
        logging.error(e)
        return None


async def get_friend_by_ids(friends_data: FriendsData, session):
    try:
        query = select(Friends).where(
            Friends.user_id == friends_data.user_id,
            Friends.friend_id == friends_data.friend_id
        )
        logging.warning(f'friends_data: {friends_data}')
        result = await session.execute(query)
        friend = result.fetchone()

        if friend is None:
            raise NoResultFound("Friend not found")

        logging.warning(f'Friend: {friend}')

        return friend

    except NoResultFound as e:
        logging.warning(str(e))
        return None

    except Exception as e:
        logging.error(str(e))
        return None
