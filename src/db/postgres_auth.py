import logging

import psycopg2
from psycopg2.extras import DictCursor

from core.config import pg_auth_config


async def get_cursor() -> DictCursor:
    """Возвращает курсор для выполнения запросов"""
    try:
        logging.info('Connecting to Postgres_Auth')
        conn = psycopg2.connect(
            host=pg_auth_config.host,
            database=pg_auth_config.name,
            user=pg_auth_config.user,
            password=pg_auth_config.password
        )
        cursor = conn.cursor()
        return cursor

    except Exception:
        logging.error('Failed to connect to Postgres_Auth')
        raise


async def get_friend_data(friend_id):
    with await get_cursor() as cursor:
        cursor.execute("SELECT login, name FROM users WHERE id = %s", (friend_id,))
        result = cursor.fetchone()

        return result
